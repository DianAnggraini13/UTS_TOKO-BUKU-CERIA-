
import asyncio
import httpx


BASE_URL = "http://127.0.0.1:8000"


async def kirim_transaksi(client, nama):
    response = await client.post(
        f"{BASE_URL}/transactions/",
        json={
            "buku_id": 1,
            "jumlah": 1
        }
    )

    print(f"{nama}:")
    print("Status:", response.status_code)
    print("Respons:", response.json())

    return response.json()


async def main():
    async with httpx.AsyncClient() as client:

        # Mengatur stok buku ID 1 menjadi 1
        await client.put(
            f"{BASE_URL}/buku/1",
            json={"stok": 1}
        )

        print("Mengirim dua transaksi secara bersamaan...\n")

        await asyncio.gather(
            kirim_transaksi(client, "Transaksi 1"),
            kirim_transaksi(client, "Transaksi 2")
        )

        print("\nMenunggu proses transaksi...")
        await asyncio.sleep(5)

        # Memeriksa stok akhir
        response = await client.get(
            f"{BASE_URL}/buku/1"
        )

        print("\nStok akhir buku:")
        print(response.json())

        # Memeriksa status transaksi
        response = await client.get(
            f"{BASE_URL}/transactions/"
        )

        print("\nRiwayat transaksi:")
        print(response.json())


if __name__ == "__main__":
    asyncio.run(main())
