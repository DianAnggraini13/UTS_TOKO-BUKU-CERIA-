
import aiosqlite

DATABASE_NAME = "buku_ceria.db"


async def get_db():
    async with aiosqlite.connect(DATABASE_NAME) as db:
        db.row_factory = aiosqlite.Row
        yield db


async def init_db():
    async with aiosqlite.connect(DATABASE_NAME) as db:

        await db.execute("""
            CREATE TABLE IF NOT EXISTS buku (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                judul TEXT NOT NULL,
                penulis TEXT NOT NULL,
                kategori TEXT NOT NULL,
                harga REAL NOT NULL CHECK (harga >= 0),
                stok INTEGER NOT NULL DEFAULT 0 CHECK (stok >= 0)
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER NOT NULL,
                qty INTEGER NOT NULL CHECK (qty > 0),
                status TEXT NOT NULL DEFAULT 'pending',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (item_id) REFERENCES buku(id)
            )
        """)

        await db.commit()
