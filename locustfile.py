
from locust import HttpUser, task, between


class BukuCeriaUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def lihat_daftar_buku(self):
        self.client.get("/buku?skip=0&limit=10")

    @task(2)
    def lihat_detail_buku(self):
        self.client.get("/buku/1")

    @task(1)
    def lihat_transaksi(self):
        self.client.get("/transactions")
