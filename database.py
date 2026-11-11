
import aiosqlite

DATABASE_NAME = "buku_ceria.db"


async def init_db():
    async with aiosqlite.connect(DATABASE_NAME) as db:

        # Membuat tabel buku
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

        # Membuat tabel transaksi
        await db.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                buku_id INTEGER NOT NULL,
                jumlah INTEGER NOT NULL CHECK (jumlah > 0),
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                error_message TEXT,
                FOREIGN KEY (buku_id) REFERENCES buku(id)
            )
        """)

        await db.commit()


async def get_db():
    async with aiosqlite.connect(DATABASE_NAME) as db:
        db.row_factory = aiosqlite.Row
        yield db
