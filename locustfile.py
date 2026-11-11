
from locust import HttpUser, task, between


class BukuCeriaUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def daftar_buku(self):
        self.client.get("/buku")

    @task(2)
    def detail_buku(self):
        self.client.get("/buku/1")

    @task(1)
    def daftar_transaksi(self):
        self.client.get("/transactions")
