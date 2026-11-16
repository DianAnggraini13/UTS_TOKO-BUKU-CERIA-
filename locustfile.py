
import os

from locust import HttpUser, task, between
from locust.exception import StopUser


# Jenis pengujian: get atau post
SCENARIO = os.getenv("LOCUST_SCENARIO", "get")

# Jumlah request untuk setiap pengguna
REQUESTS_PER_USER = int(os.getenv("REQUESTS_PER_USER", "5"))


class BukuCeriaUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.request_count = 0

        if SCENARIO not in ["get", "post"]:
            raise ValueError("SCENARIO harus get atau post")

    @task
    def pengujian_buku_ceria(self):
        if SCENARIO == "get":
            self.client.get(
                "/buku?skip=0&limit=10",
                name="GET /buku"
            )

        elif SCENARIO == "post":
            self.client.post(
                "/transactions",
                json={
                    "buku_id": 1,
                    "jumlah": 1
                },
                name="POST /transactions"
            )

        self.request_count += 1

        if self.request_count >= REQUESTS_PER_USER:
            raise StopUser
