
from locust import HttpUser, task, between


class BukuUser(HttpUser):

    wait_time = between(1, 3)

    # Melihat daftar buku
    @task(3)
    def lihat_semua_buku(self):
        self.client.get("/buku/")

    # Melihat detail buku
    @task(2)
    def lihat_detail_buku(self):
        self.client.get("/buku/1")

    # Melihat seluruh transaksi
    @task(1)
    def lihat_transaksi(self):
        self.client.get("/transactions/")

    # Membuat transaksi
    @task(1)
    def buat_transaksi(self):
        self.client.post(
            "/transactions/",
            json={
                "buku_id": 1,
                "jumlah": 1
            }
        )
