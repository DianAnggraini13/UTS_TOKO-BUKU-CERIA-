# Toko Buku Ceria API

REST API untuk pengelolaan data buku dan transaksi pada Toko Buku Ceria. Aplikasi ini dikembangkan menggunakan Python dan FastAPI dengan SQLite sebagai database. Sistem menyediakan fitur pengelolaan buku (CRUD), pemrosesan transaksi secara asynchronous, serta pengujian konkurensi untuk memastikan pengurangan stok berjalan dengan benar.

## 1. Deskripsi Proyek

Toko Buku Ceria API merupakan aplikasi berbasis REST API yang digunakan untuk mengelola persediaan buku dan transaksi pembelian.

Aplikasi ini memiliki beberapa fitur utama:

- Menampilkan seluruh data buku.
- Menampilkan detail buku berdasarkan ID.
- Menambahkan data buku baru.
- Memperbarui data buku.
- Menghapus data buku.
- Membuat transaksi pembelian dengan status awal `pending`.
- Memproses transaksi menggunakan `BackgroundTasks`.
- Memeriksa status transaksi.
- Menampilkan daftar transaksi berdasarkan status.
- Mengelola pengurangan stok agar tidak terjadi stok negatif.
- Melakukan pengujian beban menggunakan Locust.
- Melakukan pengujian konkurensi transaksi.
- Membandingkan performa aplikasi menggunakan 1 dan 4 worker.

## 2. Teknologi yang Digunakan

| Teknologi | Kegunaan |
|---|---|
| Python 3.10+ | Bahasa pemrograman |
| FastAPI | Framework REST API |
| SQLite | Database |
| aiosqlite | Koneksi database asynchronous |
| Pydantic | Validasi data API |
| Uvicorn | Menjalankan server ASGI |
| Locust | Pengujian beban API |
| asyncio | Pengelolaan proses asynchronous |

## 3. Struktur Folder Proyek

Struktur folder proyek Toko Buku Ceria:

```text
BUKU_CERIA/
│
├── main.py
├── database.py
├── models.py
│
├── routes/
│   ├── __init__.py
│   ├── resource.py
│   └── transaction.py
│
├── seed.py
├── test_race.py
├── locustfile.py
├── benchmark.py
├── run_server.py
├── requirements.txt
├── README.md
│
├── docs/
│   └── laporan_uts.pdf
│
└── buku_ceria.db
```

**Keterangan file:**

- `main.py`: Inisialisasi aplikasi FastAPI dan registrasi router.
- `database.py`: Mengatur koneksi serta inisialisasi database SQLite menggunakan aiosqlite.
- `models.py`: Mendefinisikan model dan validasi data menggunakan Pydantic.
- `routes/__init__.py`: Inisialisasi package routes.
- `routes/resource.py`: Mengatur endpoint pengelolaan data buku.
- `routes/transaction.py`: Mengatur endpoint transaksi dan pemrosesan transaksi.
- `seed.py`: Mengisi database dengan minimal 10 data awal buku.
- `test_race.py`: Melakukan pengujian konkurensi transaksi.
- `locustfile.py`: Mendefinisikan skenario pengujian beban API.
- `benchmark.py`: Mengatur pelaksanaan benchmark dan membandingkan hasil pengujian berdasarkan jumlah worker.
- `run_server.py`: Menjalankan server Uvicorn dengan jumlah worker yang ditentukan.
- `requirements.txt`: Daftar library yang dibutuhkan.
- `README.md`: Dokumentasi proyek.
- `docs/laporan_uts.pdf`: Dokumen laporan proyek.
- `buku_ceria.db`: Database SQLite untuk menyimpan data buku dan transaksi.

## 4. Persyaratan Instalasi

Sebelum menjalankan aplikasi, pastikan perangkat telah memiliki:

1. Python versi 3.10 atau lebih baru.
2. Visual Studio Code.
3. Git, jika ingin mengelola dan mengunggah proyek ke GitHub.
4. Koneksi internet untuk menginstal dependensi.

## 5. Instalasi Proyek

### A. Membuka Folder Proyek

Buka terminal di Visual Studio Code, kemudian arahkan terminal ke folder proyek:

```powershell
cd C:\vscode\BUKU_CERIA
```

### B. Membuat Virtual Environment

Jalankan perintah:

```powershell
python -m venv .venv
```

### C. Mengaktifkan Virtual Environment

Untuk Windows PowerShell, jalankan:

```powershell
.\.venv\Scripts\Activate.ps1
```

Jika aktivasi berhasil, terminal akan menampilkan tanda `(.venv)`.

### D. Menginstal Dependensi

Pastikan terminal berada di folder utama proyek dan virtual environment sudah aktif. Kemudian jalankan:

```powershell
python -m pip install -r requirements.txt
```

Perintah tersebut akan menginstal seluruh library yang diperlukan oleh aplikasi.

## 6. Menjalankan Aplikasi

### A. Mengisi Database

Untuk mengisi database dengan data awal buku, jalankan:

```powershell
python seed.py
```

File `seed.py` menyediakan minimal 10 data buku sebagai data awal pengujian.

### B. Menjalankan Server untuk Pengembangan

Jalankan aplikasi menggunakan Uvicorn:

```powershell
uvicorn main:app --reload
```

Perintah tersebut menjalankan server FastAPI dalam mode pengembangan. Jika berhasil, server dapat diakses melalui alamat:

http://127.0.0.1:8000

### C. Menjalankan Server dengan Worker

Proyek juga menyediakan file `run_server.py` untuk menjalankan server dengan jumlah worker yang ditentukan.

Contoh menjalankan server menggunakan 1 worker:

```powershell
python run_server.py 1
```

Contoh menjalankan server menggunakan 4 worker:

```powershell
python run_server.py 4
```

Pengaturan worker ini digunakan dalam pengujian perbandingan performa aplikasi.

### D. Membuka Dokumentasi API

FastAPI menyediakan dokumentasi interaktif menggunakan Swagger UI.

Buka browser dan akses:

http://127.0.0.1:8000/docs

Melalui Swagger UI, pengguna dapat mencoba setiap endpoint API secara langsung.

## 7. Daftar Endpoint API

### A. Endpoint Pengelolaan Buku

| Method | Endpoint | Fungsi |
|---|---|---|
| GET | `/buku?skip=0&limit=10` | Menampilkan daftar buku |
| GET | `/buku/{buku_id}` | Menampilkan detail buku |
| POST | `/buku` | Menambahkan buku |
| PUT | `/buku/{buku_id}` | Memperbarui data buku |
| DELETE | `/buku/{buku_id}` | Menghapus buku |

### B. Endpoint Transaksi

| Method | Endpoint | Fungsi |
|---|---|---|
| POST | `/transactions` | Membuat transaksi baru |
| GET | `/transactions` | Menampilkan daftar transaksi |
| GET | `/transactions?status=pending` | Menampilkan transaksi berdasarkan status |
| GET | `/transactions/{id}` | Menampilkan detail transaksi |

### C. Status Transaksi

Sistem menggunakan beberapa status transaksi:

- **Pending**: Transaksi baru dibuat dan menunggu pemrosesan.
- **Processing**: Transaksi sedang diproses.
- **Completed**: Transaksi berhasil diselesaikan.
- **Failed**: Transaksi gagal diproses.

Alur perubahan status transaksi:

```text
Pending
   |
   v
Processing
   |
   v
Completed / Failed
```

## 8. Pengelolaan Stok dan Konkurensi

Sistem menggunakan mekanisme asynchronous untuk memproses transaksi tanpa harus membuat pengguna menunggu seluruh proses selesai ketika permintaan transaksi diterima.

Beberapa mekanisme yang diterapkan:

1. **BackgroundTasks** digunakan untuk menjalankan pemrosesan transaksi di latar belakang.
2. **asyncio.Lock** digunakan untuk mengatur akses bersamaan terhadap proses pengurangan stok.
3. **SQL Conditional Update** digunakan untuk memastikan stok hanya dikurangi apabila jumlah stok mencukupi.

Pengurangan stok menggunakan perintah SQL berikut:

```sql
UPDATE buku
SET stok = stok - ?
WHERE id = ? AND stok >= ?
```

Kondisi `stok >= ?` memastikan pengurangan hanya dilakukan jika jumlah stok mencukupi. Mekanisme ini membantu mencegah stok menjadi negatif ketika beberapa transaksi dilakukan secara bersamaan.

## 9. Pengujian Aplikasi

### A. Membersihkan Hasil Pengujian Sebelumnya

Sebelum melakukan pengujian ulang, bersihkan file hasil pengujian dalam format CSV agar hasil pengujian terbaru tidak tercampur dengan hasil sebelumnya.

Pastikan terminal berada di folder utama proyek:

```powershell
cd C:\vscode\BUKU_CERIA
```

Kemudian jalankan perintah berikut:

```powershell
Remove-Item .\hasil_*.csv -ErrorAction SilentlyContinue
```

Perintah tersebut menghapus file CSV yang namanya diawali `hasil_`, seperti file hasil pengujian Locust dan ringkasan benchmark. Perintah ini tidak menghapus file kode pengujian seperti `benchmark.py`, `locustfile.py`, dan `test_race.py`.

Untuk memeriksa file yang masih ada, jalankan:

```powershell
Get-ChildItem -File
```

### B. Pengujian Menggunakan Swagger UI

Pengujian endpoint dilakukan melalui Swagger UI:

http://127.0.0.1:8000/docs

Langkah pengujian:

1. Menjalankan server FastAPI.
2. Membuka Swagger UI.
3. Mencoba endpoint GET untuk melihat data buku.
4. Mencoba endpoint POST untuk menambahkan buku.
5. Mencoba endpoint PUT untuk memperbarui buku.
6. Mencoba endpoint DELETE untuk menghapus buku.
7. Mencoba endpoint POST transaksi.
8. Memeriksa perubahan status transaksi.

### C. Pengujian Konkurensi

Pengujian konkurensi dilakukan menggunakan file `test_race.py`.

Tujuannya adalah menguji kemampuan sistem dalam menangani beberapa transaksi yang mengakses stok buku secara bersamaan.

Jalankan perintah berikut dari folder utama proyek:

```powershell
python test_race.py
```

Hasil pengujian digunakan untuk memeriksa:

- Apakah beberapa transaksi dapat dikirim secara bersamaan.
- Apakah stok buku berkurang sesuai jumlah transaksi yang berhasil.
- Apakah sistem menolak transaksi ketika stok tidak mencukupi.
- Apakah stok akhir tetap berada pada nilai nol atau lebih.

### D. Pengujian Beban Menggunakan Locust

Locust digunakan untuk menguji kemampuan API dalam menangani banyak permintaan secara bersamaan.

Pastikan server FastAPI sudah berjalan di terminal pertama. Kemudian buka terminal kedua, arahkan ke folder utama proyek, dan aktifkan virtual environment.

**Pengujian skenario GET**

Pada Windows PowerShell, jalankan:

```powershell
$env:LOCUST_SCENARIO="get"
```

Kemudian jalankan Locust:

```powershell
locust -f locustfile.py --host http://127.0.0.1:8000
```

**Pengujian skenario POST**

Untuk menguji transaksi, ubah skenario menjadi:

```powershell
$env:LOCUST_SCENARIO="post"
```

Kemudian jalankan kembali perintah Locust:

```powershell
locust -f locustfile.py --host http://127.0.0.1:8000
```

Setelah Locust berhasil dijalankan, buka browser:

http://localhost:8089

Masukkan jumlah pengguna virtual (*Number of users*) dan laju penambahan pengguna (*Spawn rate*), kemudian mulai pengujian.

Hasil pengujian dapat dilihat melalui beberapa bagian:

- **Statistics**: Menampilkan jumlah request, response time, throughput, dan jumlah request yang gagal.
- **Charts**: Menampilkan grafik performa selama pengujian.
- **Failures**: Menampilkan daftar permintaan yang mengalami kegagalan.
- **Exceptions**: Menampilkan informasi kesalahan yang terjadi selama pengujian.

Pengujian ini bertujuan mengetahui kemampuan API dalam menangani permintaan dari pengguna virtual secara bersamaan.

### E. Pengujian Benchmark

Pengujian benchmark dilakukan menggunakan file `benchmark.py` dengan bantuan Locust untuk membandingkan performa aplikasi pada konfigurasi 1 worker dan 4 worker.

Pengujian mencakup dua skenario:

1. **GET**: Mengukur performa pengambilan data buku melalui endpoint `/buku`.
2. **POST**: Mengukur performa pembuatan transaksi melalui endpoint `/transactions`.

Jalankan perintah berikut dari terminal pada folder utama proyek:

```powershell
python benchmark.py
```

Program akan menjalankan pengujian pada masing-masing konfigurasi worker dan menghasilkan file ringkasan bernama `hasil_ringkasan_benchmark.csv`.

#### Hasil Pengujian Benchmark

Berikut merupakan hasil pengujian benchmark yang diperoleh:

| Skenario | Worker | Total Waktu (s) | Throughput (req/s) | Rata-rata Latensi (ms) | Total Request | Request Gagal |
|---|---:|---:|---:|---:|---:|---:|
| GET | 1 | 31.36 | 9.06 | 28.07 | 100 | 0 |
| POST | 1 | 31.39 | 5.07 | 86.82 | 50 | 0 |
| GET | 4 | 31.21 | 9.11 | 18.87 | 100 | 0 |
| POST | 4 | 31.33 | 4.75 | 74.52 | 50 | 0 |

#### Analisis Hasil Benchmark

Berdasarkan hasil pengujian, konfigurasi 4 worker menghasilkan rata-rata latensi yang lebih rendah dibandingkan konfigurasi 1 worker pada kedua skenario.

Pada skenario GET, throughput meningkat dari 9.06 req/s menjadi 9.11 req/s, sedangkan rata-rata latensi menurun dari 28.07 ms menjadi 18.87 ms.

Pada skenario POST, throughput mengalami penurunan dari 5.07 req/s menjadi 4.75 req/s. Namun, rata-rata latensi menurun dari 86.82 ms menjadi 74.52 ms.

Seluruh pengujian berhasil dijalankan tanpa request gagal. Hasil ini menunjukkan bahwa penambahan jumlah worker tidak selalu meningkatkan throughput pada setiap skenario, meskipun dapat menghasilkan waktu respons yang lebih rendah.

## 10. Pengelolaan Database

Aplikasi menggunakan SQLite sebagai sistem penyimpanan data.

Database diinisialisasi melalui fungsi `init_db()` yang dipanggil ketika aplikasi mulai dijalankan.

Tabel utama yang digunakan adalah tabel `buku`, dengan atribut:

| Kolom | Tipe Data | Keterangan |
|---|---|---|
| id | INTEGER | Primary Key |
| judul | TEXT | Judul buku |
| penulis | TEXT | Nama penulis |
| kategori | TEXT | Kategori buku |
| harga | REAL | Harga buku |
| stok | INTEGER | Jumlah persediaan buku |

Kolom `stok` memiliki batasan agar nilainya tidak kurang dari nol.

## 11. Mengunggah Proyek ke GitHub

Proyek dapat dikelola dan diunggah ke repository GitHub. Pastikan repository sudah dibuat dan folder proyek lokal telah terhubung dengan repository tersebut.

Untuk mengunggah perubahan terbaru, buka terminal pada folder utama proyek, kemudian jalankan perintah berikut secara berurutan.

**1. Memeriksa perubahan file**

```powershell
git status
```

**2. Menambahkan perubahan**

```powershell
git add .
```

**3. Membuat commit**

```powershell
git commit -m "Update project Toko Buku Ceria API"
```

**4. Mengunggah perubahan ke GitHub**

```powershell
git push origin main
```

Pastikan folder `.venv`, file cache Python, file sementara, dan hasil pengujian CSV tidak ikut diunggah ke repository. File yang tidak perlu diunggah dapat diatur melalui `.gitignore`.

Tambahkan aturan berikut ke dalam file `.gitignore`:

```gitignore
.venv/
__pycache__/
*.pyc
hasil_*.csv
```

Repository GitHub proyek:

https://github.com/DianAnggraini13/UTS_TOKO-BUKU-CERIA-.git

## 12. Kesimpulan

Toko Buku Ceria API merupakan aplikasi REST API yang dikembangkan untuk mengelola data buku dan transaksi pembelian menggunakan FastAPI dan SQLite.

Aplikasi ini menerapkan operasi database asynchronous, pemrosesan transaksi menggunakan BackgroundTasks, serta mekanisme pengamanan stok melalui asyncio.Lock dan SQL Conditional Update.

Pengujian dilakukan menggunakan Swagger UI, skrip pengujian konkurensi, dan Locust untuk mengetahui kemampuan sistem dalam menangani permintaan secara bersamaan. Pengujian benchmark juga dilakukan untuk membandingkan performa aplikasi dengan konfigurasi 1 worker dan 4 worker.

Dengan adanya aplikasi ini, pengelolaan data buku dan transaksi dapat dilakukan melalui endpoint API secara terstruktur dan terdokumentasi.