
import aiosqlite

from fastapi import APIRouter, Depends, HTTPException, Query

from database import get_db
from models import BukuCreate, BukuUpdate, BukuResponse


router = APIRouter(
    prefix="/buku",
    tags=["Buku"]
)


# GET: Menampilkan semua buku
@router.get("/", response_model=list[BukuResponse])
async def get_all_buku(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: aiosqlite.Connection = Depends(get_db)
):
    cursor = await db.execute(
        "SELECT * FROM buku ORDER BY id LIMIT ? OFFSET ?",
        (limit, skip)
    )

    rows = await cursor.fetchall()

    return [dict(row) for row in rows]


# GET: Menampilkan buku berdasarkan ID
@router.get("/{buku_id}", response_model=BukuResponse)
async def get_buku(
    buku_id: int,
    db: aiosqlite.Connection = Depends(get_db)
):
    cursor = await db.execute(
        "SELECT * FROM buku WHERE id = ?",
        (buku_id,)
    )

    row = await cursor.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Buku tidak ditemukan"
        )

    return dict(row)


# POST: Menambahkan buku
@router.post("/", response_model=BukuResponse, status_code=201)
async def create_buku(
    buku: BukuCreate,
    db: aiosqlite.Connection = Depends(get_db)
):
    cursor = await db.execute(
        """
        INSERT INTO buku (judul, penulis, kategori, harga, stok)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            buku.judul,
            buku.penulis,
            buku.kategori,
            buku.harga,
            buku.stok
        )
    )

    await db.commit()

    new_id = cursor.lastrowid

    cursor = await db.execute(
        "SELECT * FROM buku WHERE id = ?",
        (new_id,)
    )

    row = await cursor.fetchone()

    return dict(row)


# PUT: Memperbarui buku
@router.put("/{buku_id}", response_model=BukuResponse)
async def update_buku(
    buku_id: int,
    buku: BukuUpdate,
    db: aiosqlite.Connection = Depends(get_db)
):
    cursor = await db.execute(
        "SELECT * FROM buku WHERE id = ?",
        (buku_id,)
    )

    row = await cursor.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Buku tidak ditemukan"
        )

    data = buku.model_dump(exclude_unset=True)

    if not data:
        raise HTTPException(
            status_code=400,
            detail="Tidak ada data yang diperbarui"
        )

    for key, value in data.items():
        if value is None:
            raise HTTPException(
                status_code=422,
                detail=f"Field {key} tidak boleh null"
            )

    set_clause = ", ".join(
        f"{key} = ?" for key in data.keys()
    )

    values = list(data.values())
    values.append(buku_id)

    await db.execute(
        f"UPDATE buku SET {set_clause} WHERE id = ?",
        values
    )

    await db.commit()

    cursor = await db.execute(
        "SELECT * FROM buku WHERE id = ?",
        (buku_id,)
    )

    updated_row = await cursor.fetchone()

    return dict(updated_row)


# DELETE: Menghapus buku
@router.delete("/{buku_id}")
async def delete_buku(
    buku_id: int,
    db: aiosqlite.Connection = Depends(get_db)
):
    cursor = await db.execute(
        "SELECT * FROM buku WHERE id = ?",
        (buku_id,)
    )

    row = await cursor.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Buku tidak ditemukan"
        )

    await db.execute(
        "DELETE FROM buku WHERE id = ?",
        (buku_id,)
    )

    await db.commit()

    return {
        "pesan": "Buku berhasil dihapus"
    }
