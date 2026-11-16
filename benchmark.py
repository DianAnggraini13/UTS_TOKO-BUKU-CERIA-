
import asyncio
import csv
import os
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import aiosqlite



BASE_DIR = Path(__file__).resolve().parent

BASE_URL = "http://127.0.0.1:8000"

SERVER_FILE = BASE_DIR / "run_server.py"
LOCUST_FILE = BASE_DIR / "locustfile.py"
DATABASE_FILE = BASE_DIR / "buku_ceria.db"

BOOK_ID = 1
INITIAL_STOCK = 1000

REQUESTS_PER_USER = 5
RUN_TIME = "30s"

SUMMARY_FILE = BASE_DIR / "hasil_ringkasan_benchmark.csv"



def check_port():

    try:
        connection = socket.create_connection(
            ("127.0.0.1", 8000),
            timeout=1
        )
        connection.close()

        return True

    except OSError:
        return False



def start_server(workers):

    print("\n" + "=" * 50)
    print(f"MENJALANKAN SERVER: {workers} WORKER")
    print("=" * 50)

    if check_port():
        raise RuntimeError(
            "Port 8000 masih digunakan. "
            "Hentikan server atau Locust yang masih berjalan."
        )

    process = subprocess.Popen(
        [
            sys.executable,
            str(SERVER_FILE),
            str(workers)
        ],
        cwd=BASE_DIR
    )

    # Menunggu server siap
    for _ in range(60):

        if process.poll() is not None:
            raise RuntimeError(
                "Server berhenti sebelum siap dijalankan."
            )

        try:
            urllib.request.urlopen(
                BASE_URL + "/",
                timeout=2
            )

            print("Server berhasil dijalankan.")
            return process

        except Exception:
            time.sleep(0.5)

    process.terminate()

    raise RuntimeError(
        "Server tidak berhasil dijalankan dalam 30 detik."
    )


def stop_server(process):

    if process is None:
        return

    print("\nMenghentikan server...")

    process.terminate()

    try:
        process.wait(timeout=10)

    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()

    time.sleep(2)

    print("Server berhasil dihentikan.")


async def reset_stock():

    if not DATABASE_FILE.exists():
        raise FileNotFoundError(
            "Database buku_ceria.db tidak ditemukan."
        )

    async with aiosqlite.connect(DATABASE_FILE) as db:

        cursor = await db.execute(
            "UPDATE buku SET stok = ? WHERE id = ?",
            (INITIAL_STOCK, BOOK_ID)
        )

        if cursor.rowcount == 0:
            raise RuntimeError(
                f"Buku dengan ID {BOOK_ID} tidak ditemukan."
            )

        await db.commit()

    print(
        f"Stok buku ID {BOOK_ID} berhasil diatur "
        f"menjadi {INITIAL_STOCK}."
    )


# ==========================================
# MEMBACA HASIL LOCUST
# ==========================================

def read_locust_result(csv_file):

    if not csv_file.exists():
        raise FileNotFoundError(
            f"Hasil Locust tidak ditemukan: {csv_file}"
        )

    with open(
        csv_file,
        mode="r",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        rows = list(csv.DictReader(file))

    for row in rows:

        if row.get("Name") == "Aggregated":

            return {
                "requests": int(
                    float(row.get("Request Count", 0))
                ),

                "failures": int(
                    float(row.get("Failure Count", 0))
                ),

                "throughput": float(
                    row.get("Requests/s", 0)
                ),

                "latency": float(
                    row.get("Average Response Time", 0)
                )
            }

    raise RuntimeError(
        "Baris Aggregated tidak ditemukan pada CSV Locust."
    )


# ==========================================
# MENJALANKAN PENGUJIAN LOCUST
# ==========================================

def run_locust(scenario, workers):

    if scenario == "get":
        users = 20

    else:
        users = 10

    spawn_rate = users

    prefix = BASE_DIR / (
        f"hasil_{scenario}_{workers}worker"
    )

    environment = os.environ.copy()

    environment["LOCUST_SCENARIO"] = scenario
    environment["REQUESTS_PER_USER"] = str(
        REQUESTS_PER_USER
    )

    command = [
        sys.executable,
        "-m",
        "locust",

        "-f",
        str(LOCUST_FILE),

        "--headless",

        "-H",
        BASE_URL,

        "-u",
        str(users),

        "-r",
        str(spawn_rate),

        "-t",
        RUN_TIME,

        "--csv",
        str(prefix),

        "--csv-full-history",

        "--only-summary"
    ]

    print("\n" + "-" * 50)
    print(f"SKENARIO: {scenario.upper()}")
    print(f"WORKER: {workers}")
    print(f"JUMLAH USER: {users}")
    print(
        f"TARGET REQUEST: "
        f"{users * REQUESTS_PER_USER}"
    )
    print("-" * 50)

    start_time = time.perf_counter()

    result = subprocess.run(
        command,
        cwd=BASE_DIR,
        env=environment,
        check=False
    )

    total_time = time.perf_counter() - start_time

    if result.returncode != 0:
        raise RuntimeError(
            f"Locust gagal menjalankan skenario {scenario}."
        )

    stats_file = Path(str(prefix) + "_stats.csv")

    stats = read_locust_result(stats_file)

    print("\nHASIL PENGUJIAN")
    print(f"Total Request : {stats['requests']}")
    print(f"Request Gagal : {stats['failures']}")
    print(f"Total Waktu   : {total_time:.2f} detik")
    print(
        f"Throughput    : "
        f"{stats['throughput']:.2f} req/s"
    )
    print(
        f"Latensi Rata-rata: "
        f"{stats['latency']:.2f} ms"
    )

    return {
        "scenario": scenario.upper(),
        "workers": workers,
        "total_time": total_time,
        "throughput": stats["throughput"],
        "latency": stats["latency"],
        "requests": stats["requests"],
        "failures": stats["failures"]
    }


# ==========================================
# MENYIMPAN RINGKASAN BENCHMARK
# ==========================================

def save_summary(results):

    headers = [
        "Skenario",
        "Worker",
        "Total Waktu (s)",
        "Throughput (req/s)",
        "Rata-rata Latensi (ms)",
        "Total Request",
        "Request Gagal"
    ]

    with open(
        SUMMARY_FILE,
        mode="w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow(headers)

        for result in results:

            writer.writerow([
                result["scenario"],
                result["workers"],
                round(result["total_time"], 2),
                round(result["throughput"], 2),
                round(result["latency"], 2),
                result["requests"],
                result["failures"]
            ])

    print("\nRingkasan tersimpan di:")
    print(SUMMARY_FILE.name)


# ==========================================
# PROGRAM UTAMA
# ==========================================

def main():

    results = []

    print("=" * 55)
    print("BENCHMARK TOKO BUKU CERIA")
    print("=" * 55)

    try:

        # Pengujian 1 worker dan 4 worker
        for workers in [1, 4]:

            server = None

            try:

                # Menjalankan server
                server = start_server(workers)

                # Pengujian GET
                get_result = run_locust(
                    "get",
                    workers
                )

                results.append(get_result)

                # Mengatur stok sebelum POST
                asyncio.run(reset_stock())

                # Pengujian POST
                post_result = run_locust(
                    "post",
                    workers
                )

                results.append(post_result)

                # Memberi waktu transaksi selesai diproses
                print(
                    "\nMenunggu transaksi selesai diproses..."
                )

                time.sleep(5)

            finally:

                stop_server(server)

        # Menyimpan seluruh hasil
        save_summary(results)

        print("\n" + "=" * 55)
        print("SEMUA PENGUJIAN BENCHMARK SELESAI")
        print("=" * 55)

    except Exception as error:

        print("\nBENCHMARK GAGAL:")
        print(error)

        raise


if __name__ == "__main__":
    main()
