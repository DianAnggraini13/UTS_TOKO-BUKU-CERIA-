
import asyncio
import aiosqlite

from database import DATABASE_NAME, init_db


data_buku = [
    ("Laskar Pelangi", "Andrea Hirata", "Novel", 85000, 20),
    ("Bumi", "Tere Liye", "Fantasi", 90000, 15),
    ("Laut Bercerita", "Leila S. Chudori", "Novel", 95000, 12),
    ("Filosofi Teras", "Henry Manampiring", "Nonfiksi", 98000, 18),
    ("Atomic Habits", "James Clear", "Pengembangan Diri", 110000, 25),
    ("Negeri 5 Menara", "Ahmad Fuadi", "Novel", 88000, 20),
    ("Pulang", "Tere Liye", "Novel", 92000, 15),
    ("Dilan 1990", "Pidi Baiq", "Romantis", 75000, 10),
    ("Bumi Manusia", "Pramoedya Ananta Toer", "Sejarah", 100000, 14),
    ("Perahu Kertas", "Dee Lestari", "Romantis", 85000, 16)
]


async def seed():
    await init_db()

    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute("DELETE FROM transactions")
        await db.execute("DELETE FROM buku")

        await db.executemany(
            """
            INSERT INTO buku
            (judul, penulis, kategori, harga, stok)
            VALUES (?, ?, ?, ?, ?)
            """,
            data_buku
        )

        await db.commit()

    print("Berhasil menambahkan 10 data buku.")


if __name__ == "__main__":
    asyncio.run(seed())
