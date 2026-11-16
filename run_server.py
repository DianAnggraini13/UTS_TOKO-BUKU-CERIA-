
import asyncio
import sys
import uvicorn


def main():
    # Pengaturan event loop untuk Windows
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(
            asyncio.WindowsSelectorEventLoopPolicy()
        )

    # Jumlah worker dari argumen terminal
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    print(f"Menjalankan Toko Buku Ceria dengan {workers} worker")

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        workers=workers,
        log_level="warning"
    )


if __name__ == "__main__":
    main()
