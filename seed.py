
import asyncio
import aiosqlite

from database import DATABASE_NAME, init_db


DATA_BUKU = [
    ("Laskar Pelangi", "Andrea Hirata", "Novel", 85000, 20),
    ("Bumi", "Tere Liye", "Fantasi", 95000, 15),
    ("Laut Bercerita", "Leila S. Chudori", "Novel", 100000, 10),
    ("Filosofi Teras", "Henry Manampiring", "Pengembangan Diri", 89000, 12),
    ("Atomic Habits", "James Clear", "Pengembangan Diri", 120000, 18),
    ("Negeri 5 Menara", "Ahmad Fuadi", "Novel", 80000, 14),
    ("Pulang", "Tere Liye", "Novel", 90000, 11),
    ("Dilan 1990", "Pidi Baiq", "Romansa", 75000, 16),
    ("Bumi Manusia", "Pramoedya Ananta Toer", "Sejarah", 110000, 9),
    ("Perahu Kertas", "Dee Lestari", "Romansa", 85000, 13),
]


async def seed_database():
    await init_db()

    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.executemany(
            """
            INSERT INTO buku (judul, penulis, kategori, harga, stok)
            VALUES (?, ?, ?, ?, ?)
            """,
            DATA_BUKU
        )

        await db.commit()

    print("Berhasil menambahkan 10 data buku.")


if __name__ == "__main__":
    asyncio.run(seed_database())
