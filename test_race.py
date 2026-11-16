
import asyncio
import aiosqlite
import httpx

BASE_URL = "http://127.0.0.1:8000"
DATABASE_NAME = "buku_ceria.db"

# Gunakan ID buku khusus Race Condition
BUKU_ID = 15

STOK_AWAL = 1
JUMLAH_TRANSAKSI = 2


async def reset_stok():
    """Mengatur stok buku menjadi 1 sebelum pengujian."""
    async with aiosqlite.connect(DATABASE_NAME) as db:
        cursor = await db.execute(
            "UPDATE buku SET stok = ? WHERE id = ?",
            (STOK_AWAL, BUKU_ID)
        )

        if cursor.rowcount == 0:
            raise ValueError(f"Buku ID {BUKU_ID} tidak ditemukan")

        await db.commit()


async def cek_stok():
    """Memeriksa stok akhir buku."""
    async with aiosqlite.connect(DATABASE_NAME) as db:
        async with db.execute(
            "SELECT stok FROM buku WHERE id = ?",
            (BUKU_ID,)
        ) as cursor:
            hasil = await cursor.fetchone()

    if hasil is None:
        raise ValueError(f"Buku ID {BUKU_ID} tidak ditemukan")

    return hasil[0]


async def kirim_transaksi(client, nomor):
    """Mengirim satu transaksi."""
    try:
        response = await client.post(
            f"{BASE_URL}/transactions/",
            json={
                "buku_id": BUKU_ID,
                "jumlah": 1
            }
        )

        print(
            f"Transaksi {nomor}: "
            f"HTTP {response.status_code} - {response.text}"
        )

        return response.status_code

    except httpx.RequestError as error:
        print(f"Transaksi {nomor} gagal: {error}")
        return None


async def jalankan_pengujian(judul):
    print("\n" + "=" * 45)
    print(judul)
    print("=" * 45)

    await reset_stok()

    async with httpx.AsyncClient(
        timeout=30,
        follow_redirects=True
    ) as client:

        hasil = await asyncio.gather(
            *[
                kirim_transaksi(client, i)
                for i in range(1, JUMLAH_TRANSAKSI + 1)
            ]
        )

    # Menunggu background task selesai.
    await asyncio.sleep(5)

    stok_akhir = await cek_stok()

    print("\nHasil pengujian:")
    print("Respons transaksi:", hasil)
    print("Stok awal:", STOK_AWAL)
    print("Stok akhir:", stok_akhir)

    return stok_akhir


async def main():
    print("PENGUJIAN RACE CONDITION TOKO BUKU CERIA")

    stok = await cek_stok()

    print(f"\nBuku ID: {BUKU_ID}")
    print(f"Stok sebelum pengujian: {stok}")

    hasil = await jalankan_pengujian(
        "PENGUJIAN TRANSAKSI BERSAMAAN"
    )

    print("\n" + "=" * 45)
    print("KESIMPULAN PENGUJIAN")
    print("=" * 45)

    print("Stok awal:", STOK_AWAL)
    print("Stok akhir:", hasil)

    if hasil < 0:
        print("Race Condition terdeteksi: stok negatif.")
    elif hasil == 0:
        print("Stok aman: tidak negatif.")
    else:
        print("Stok masih tersisa:", hasil)


if __name__ == "__main__":
    asyncio.run(main())
