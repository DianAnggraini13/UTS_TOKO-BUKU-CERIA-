
import asyncio
import aiosqlite

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    BackgroundTasks,
    Query
)

from database import get_db, DATABASE_NAME
from models import TransactionCreate


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

stock_lock = asyncio.Lock()


# Memproses transaksi di background
async def process_transaction(
    transaction_id: int,
    buku_id: int,
    jumlah: int
):
    async with aiosqlite.connect(DATABASE_NAME) as db:

        await db.execute(
            """
            UPDATE transactions
            SET status = 'processing',
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (transaction_id,)
        )

        await db.commit()

    # Simulasi proses transaksi
    await asyncio.sleep(3)

    # Mengamankan pengurangan stok
    async with stock_lock:

        async with aiosqlite.connect(DATABASE_NAME) as db:

            cursor = await db.execute(
                """
                UPDATE buku
                SET stok = stok - ?
                WHERE id = ? AND stok >= ?
                """,
                (jumlah, buku_id, jumlah)
            )

            if cursor.rowcount == 0:

                await db.execute(
                    """
                    UPDATE transactions
                    SET status = 'failed',
                        error_message = 'Stok buku tidak mencukupi',
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                    """,
                    (transaction_id,)
                )

            else:

                await db.execute(
                    """
                    UPDATE transactions
                    SET status = 'completed',
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                    """,
                    (transaction_id,)
                )

            await db.commit()


# POST: Membuat transaksi
@router.post("/", status_code=202)
async def create_transaction(
    data: TransactionCreate,
    background_tasks: BackgroundTasks,
    db: aiosqlite.Connection = Depends(get_db)
):
    cursor = await db.execute(
        "SELECT * FROM buku WHERE id = ?",
        (data.buku_id,)
    )

    buku = await cursor.fetchone()

    if buku is None:
        raise HTTPException(
            status_code=404,
            detail="Buku tidak ditemukan"
        )

    if buku["stok"] < data.jumlah:
        raise HTTPException(
            status_code=400,
            detail="Stok buku tidak mencukupi"
        )

    cursor = await db.execute(
        """
        INSERT INTO transactions (buku_id, jumlah, status)
        VALUES (?, ?, 'pending')
        """,
        (data.buku_id, data.jumlah)
    )

    transaction_id = cursor.lastrowid

    await db.commit()

    background_tasks.add_task(
        process_transaction,
        transaction_id,
        data.buku_id,
        data.jumlah
    )

    return {
        "pesan": "Transaksi berhasil diterima",
        "transaction_id": transaction_id,
        "status": "pending"
    }


# GET: Melihat seluruh transaksi atau berdasarkan status
@router.get("/")
async def get_transactions(
    status: str | None = Query(default=None),
    db: aiosqlite.Connection = Depends(get_db)
):
    valid_status = [
        "pending",
        "processing",
        "completed",
        "failed"
    ]

    if status is not None and status not in valid_status:
        raise HTTPException(
            status_code=400,
            detail="Status transaksi tidak valid"
        )

    if status:
        cursor = await db.execute(
            """
            SELECT * FROM transactions
            WHERE status = ?
            ORDER BY id DESC
            """,
            (status,)
        )
    else:
        cursor = await db.execute(
            """
            SELECT * FROM transactions
            ORDER BY id DESC
            """
        )

    rows = await cursor.fetchall()

    return [dict(row) for row in rows]


# GET: Melihat detail transaksi berdasarkan ID
@router.get("/{transaction_id}")
async def get_transaction(
    transaction_id: int,
    db: aiosqlite.Connection = Depends(get_db)
):
    cursor = await db.execute(
        """
        SELECT * FROM transactions
        WHERE id = ?
        """,
        (transaction_id,)
    )

    row = await cursor.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Transaksi tidak ditemukan"
        )

    return dict(row)
