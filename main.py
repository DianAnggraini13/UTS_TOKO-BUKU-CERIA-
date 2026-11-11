
import asyncio
import sqlite3
from contextlib import asynccontextmanager

from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Query,
    BackgroundTasks
)

from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from database import DATABASE_NAME, init_db, get_db


# Inisialisasi database
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


# Konfigurasi FastAPI
app = FastAPI(
    title="Buku Ceria API",
    description="REST API untuk pengelolaan toko buku dan transaksi",
    version="1.0.0",
    lifespan=lifespan,
    docs_url=None
)


# Halaman utama
@app.get("/", include_in_schema=False)
async def halaman_utama():
    return {
        "pesan": "Selamat Datang di Toko Buku Ceria"
    }


# Mengatur tampilan Swagger UI
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    response = get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI"
    )

    html = response.body.decode("utf-8")

    html = html.replace(
        '"deepLinking": true,',
        '''"deepLinking": true,
        "tagsSorter": "alpha",
        "operationsSorter": (a, b) => {
            const order = {
                "GET /buku": 1,
                "GET /buku/{buku_id}": 2,
                "POST /buku": 3,
                "PUT /buku/{buku_id}": 4,
                "DELETE /buku/{buku_id}": 5,
                "POST /transactions": 6,
                "GET /transactions": 7,
                "GET /transactions/{trx_id}": 8
            };

            const keyA = a.get("method").toUpperCase() + " " + a.get("path");
            const keyB = b.get("method").toUpperCase() + " " + b.get("path");

            return (order[keyA] || 99) - (order[keyB] || 99);
        },'''
    )

    return HTMLResponse(content=html)


# Model Pydantic untuk menambahkan buku
class BukuCreate(BaseModel):
    judul: str
    penulis: str
    kategori: str
    harga: float = Field(gt=0)
    stok: int = Field(ge=0)


# Model Pydantic untuk memperbarui buku
class BukuUpdate(BaseModel):
    judul: str
    penulis: str
    kategori: str
    harga: float = Field(gt=0)
    stok: int = Field(ge=0)


# Model Pydantic untuk membuat transaksi
class TransactionCreate(BaseModel):
    item_id: int = Field(gt=0)
    qty: int = Field(gt=0)

# Pengunci untuk mencegah race condition
stock_lock = asyncio.Lock()
# Fungsi background untuk memproses transaksi
async def proses_transaksi_background(
    trx_id: int,
    item_id: int,
    qty: int
):
    with sqlite3.connect(DATABASE_NAME) as db:

        # 1. Mengubah status menjadi processing
        db.execute(
            """
            UPDATE transactions
            SET status = 'processing'
            WHERE id = ?
            """,
            (trx_id,)
        )
        db.commit()

        # 2. Simulasi proses selama 3 detik
        await asyncio.sleep(3)

        # 3. Mengurangi stok jika masih mencukupi
        cursor = db.execute(
            """
            UPDATE buku
            SET stok = stok - ?
            WHERE id = ? AND stok >= ?
            """,
            (qty, item_id, qty)
        )

        if cursor.rowcount == 0:
            # Transaksi gagal
            db.execute(
                """
                UPDATE transactions
                SET status = 'failed'
                WHERE id = ?
                """,
                (trx_id,)
            )
        else:
            # Transaksi berhasil
            db.execute(
                """
                UPDATE transactions
                SET status = 'completed'
                WHERE id = ?
                """,
                (trx_id,)
            )

        db.commit()


# ==========================
# BAGIAN PENGELOLAAN BUKU
# ==========================

# 1. GET semua buku dengan pagination
@app.get("/buku", tags=["Buku"])
async def daftar_buku(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1),
    db=Depends(get_db)
):
    cursor = await db.execute(
        "SELECT * FROM buku ORDER BY id LIMIT ? OFFSET ?",
        (limit, skip)
    )

    data = await cursor.fetchall()

    return [dict(row) for row in data]


# 2. GET detail buku berdasarkan ID
@app.get("/buku/{buku_id}", tags=["Buku"])
async def detail_buku(
    buku_id: int,
    db=Depends(get_db)
):
    cursor = await db.execute(
        "SELECT * FROM buku WHERE id = ?",
        (buku_id,)
    )

    buku = await cursor.fetchone()

    if buku is None:
        raise HTTPException(
            status_code=404,
            detail="Buku tidak ditemukan"
        )

    return dict(buku)


# 3. POST menambahkan buku baru
@app.post("/buku", status_code=201, tags=["Buku"])
async def tambah_buku(
    data: BukuCreate,
    db=Depends(get_db)
):
    cursor = await db.execute(
        """
        INSERT INTO buku (judul, penulis, kategori, harga, stok)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            data.judul,
            data.penulis,
            data.kategori,
            data.harga,
            data.stok
        )
    )

    await db.commit()

    buku_id = cursor.lastrowid

    cursor = await db.execute(
        "SELECT * FROM buku WHERE id = ?",
        (buku_id,)
    )

    buku = await cursor.fetchone()

    return dict(buku)


# 4. PUT memperbarui buku berdasarkan ID
@app.put("/buku/{buku_id}", tags=["Buku"])
async def ubah_buku(
    buku_id: int,
    data: BukuUpdate,
    db=Depends(get_db)
):
    cursor = await db.execute(
        """
        UPDATE buku
        SET judul = ?, penulis = ?, kategori = ?, harga = ?, stok = ?
        WHERE id = ?
        """,
        (
            data.judul,
            data.penulis,
            data.kategori,
            data.harga,
            data.stok,
            buku_id
        )
    )

    if cursor.rowcount == 0:
        await db.rollback()
        raise HTTPException(
            status_code=404,
            detail="Buku tidak ditemukan"
        )

    await db.commit()

    cursor = await db.execute(
        "SELECT * FROM buku WHERE id = ?",
        (buku_id,)
    )

    buku = await cursor.fetchone()

    return dict(buku)


# 5. DELETE menghapus buku secara permanen
@app.delete("/buku/{buku_id}", tags=["Buku"])
async def hapus_buku(
    buku_id: int,
    db=Depends(get_db)
):
    cursor = await db.execute(
        "DELETE FROM buku WHERE id = ?",
        (buku_id,)
    )

    if cursor.rowcount == 0:
        await db.rollback()
        raise HTTPException(
            status_code=404,
            detail="Buku tidak ditemukan"
        )

    await db.commit()

    return {
        "pesan": "Buku berhasil dihapus"
    }


# ==========================
# BAGIAN TRANSAKSI
# ==========================

# 6. POST membuat transaksi
@app.post("/transactions", status_code=202, tags=["Transaksi"])
async def buat_transaksi(
    data: TransactionCreate,
    background_tasks: BackgroundTasks,
    db=Depends(get_db)
):
    # Memeriksa apakah buku tersedia
    cursor = await db.execute(
        "SELECT * FROM buku WHERE id = ?",
        (data.item_id,)
    )

    buku = await cursor.fetchone()

    if buku is None:
        raise HTTPException(
            status_code=404,
            detail="Buku tidak ditemukan"
        )

    # Memeriksa kecukupan stok
    if buku["stok"] < data.qty:
        raise HTTPException(
            status_code=400,
            detail="Stok buku tidak mencukupi"
        )

    # Menyimpan transaksi dengan status pending
    cursor = await db.execute(
        """
        INSERT INTO transactions (item_id, qty, status)
        VALUES (?, ?, 'pending')
        """,
        (data.item_id, data.qty)
    )

    await db.commit()

    trx_id = cursor.lastrowid

    # Menjalankan proses transaksi di background
    background_tasks.add_task(
        proses_transaksi_background,
        trx_id,
        data.item_id,
        data.qty
    )

    return {
        "id": trx_id,
        "item_id": data.item_id,
        "qty": data.qty,
        "status": "pending",
        "pesan": "Transaksi berhasil dibuat dan sedang menunggu proses"
    }


# 7. GET semua transaksi dengan filter status
@app.get("/transactions", tags=["Transaksi"])
async def daftar_transaksi(
    status: str = Query(
        default=None,
        pattern="^(pending|processing|completed|failed)$"
    ),
    db=Depends(get_db)
):
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

    data = await cursor.fetchall()

    return [dict(row) for row in data]


# 8. GET detail transaksi berdasarkan ID
@app.get("/transactions/{trx_id}", tags=["Transaksi"])
async def detail_transaksi(
    trx_id: int,
    db=Depends(get_db)
):
    cursor = await db.execute(
        "SELECT * FROM transactions WHERE id = ?",
        (trx_id,)
    )

    transaksi = await cursor.fetchone()

    if transaksi is None:
        raise HTTPException(
            status_code=404,
            detail="Transaksi tidak ditemukan"
        )

    return dict(transaksi)
