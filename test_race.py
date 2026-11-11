
import asyncio
import httpx


BASE_URL = "http://127.0.0.1:8000"
ITEM_ID = 1


async def kirim_transaksi(client):
    response = await client.post(
        BASE_URL + "/transactions",
        json={
            "item_id": ITEM_ID,
            "qty": 1
        }
    )

    print("Status:", response.status_code)
    print("Respons:", response.text)


async def test_race():
    async with httpx.AsyncClient() as client:

        print("Mengirim dua transaksi bersamaan...")

        await asyncio.gather(
            kirim_transaksi(client),
            kirim_transaksi(client)
        )

        print("Menunggu proses transaksi...")
        await asyncio.sleep(5)

        response = await client.get(
            BASE_URL + "/buku/" + str(ITEM_ID)
        )

        if response.status_code != 200:
            print("Gagal mengambil data buku.")
            print(response.text)
            return

        buku = response.json()

        print("\n===== HASIL PENGUJIAN =====")
        print("Judul buku:", buku["judul"])
        print("Stok akhir:", buku["stok"])

        if buku["stok"] < 0:
            print("Terjadi overselling!")
        else:
            print("Stok tidak negatif.")


if __name__ == "__main__":
    asyncio.run(test_race())
