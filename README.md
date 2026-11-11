# Toko Buku Ceria API

REST API untuk pengelolaan data buku dan transaksi pada Toko Buku Ceria. Aplikasi ini dikembangkan menggunakan Python dan FastAPI dengan SQLite sebagai database. Sistem menyediakan fitur pengelolaan buku (CRUD), pemrosesan transaksi secara asynchronous, serta pengujian konkurensi untuk memastikan stok buku tidak mengalami pengurangan yang tidak sesuai.

## 1. Deskripsi Proyek

Toko Buku Ceria API merupakan aplikasi berbasis REST API yang digunakan untuk mengelola persediaan buku dan transaksi pembelian.

Aplikasi ini memiliki beberapa fitur utama:

- Menampilkan seluruh data buku.
- Menampilkan detail buku berdasarkan ID.
- Menambahkan data buku baru.
- Memperbarui data buku.
- Menghapus data buku.
- Membuat transaksi pembelian dengan status awal pending.
- Memproses transaksi menggunakan BackgroundTasks.
- Memeriksa status transaksi.
- Menampilkan daftar transaksi berdasarkan status.
- Mengelola pengurangan stok agar tidak terjadi stok negatif.
- Melakukan pengujian beban menggunakan Locust.
- Melakukan pengujian konkurensi transaksi.

## 2. Teknologi yang Digunakan

Teknologi dan library yang digunakan dalam pengembangan aplikasi ini:

| Teknologi | Kegunaan |
|---|---|
| Python 3.10+ | Bahasa pemrograman |
| FastAPI | Framework REST API |
| SQLite | Database |
| aiosqlite | Koneksi database asynchronous |
| Pydantic | Validasi data API |
| Uvicorn | Menjalankan server |
| Locust | Pengujian beban API |
| asyncio | Pengelolaan proses asynchronous |

## 3. Struktur Folder Proyek

Struktur folder proyek Toko Buku Ceria:

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
├── requirements.txt
├── README.md
│
├── docs/
│   └── laporan_uts.pdf
│
└── buku_ceria.db
Keterangan:

- main.py: Inisialisasi aplikasi FastAPI dan registrasi router.
- database.py: Mengatur koneksi serta inisialisasi database SQLite menggunakan aiosqlite.
- models.py: Mendefinisikan model dan validasi data menggunakan Pydantic.
- routes/__init__.py: Inisialisasi package routes.
- routes/resource.py: Mengatur endpoint pengelolaan data buku.
- routes/transaction.py: Mengatur endpoint transaksi dan pemrosesan transaksi.
- seed.py: Mengisi database dengan minimal 10 data awal buku.
- test_race.py: Melakukan pengujian konkurensi transaksi.
- locustfile.py: Mendefinisikan skenario pengujian beban API.
- requirements.txt: Daftar library yang dibutuhkan.
- README.md: Dokumentasi proyek.
- docs/laporan_uts.pdf: Dokumen laporan proyek.

## 4. Persyaratan Instalasi

Sebelum menjalankan aplikasi, pastikan perangkat telah memiliki:

1. Python versi 3.10 atau lebih baru.
2. Visual Studio Code.
3. Git (jika ingin mengunggah proyek ke GitHub).
4. Koneksi internet untuk menginstal dependensi.

## 5. Instalasi Proyek

### A. Membuka Folder Proyek

Buka terminal di Visual Studio Code, kemudian arahkan terminal ke folder proyek:

```powershell
cd C:\vscode\BUKU_CERIA
```

### B. Membuat Virtual Environment

Jalankan perintah:

powershell
python -m venv .venv

### C. Mengaktifkan Virtual Environment

Untuk Windows PowerShell:

powershell
.\.venv\Scripts\Activate.ps1

Jika aktivasi berhasil, terminal akan menampilkan tanda (.venv).

### D. Menginstal Dependensi

Pastikan terminal berada di folder utama proyek, kemudian jalankan:

powershell
pip install -r requirements.txt

Perintah tersebut akan menginstal seluruh library yang diperlukan oleh aplikasi.

## 6. Menjalankan Aplikasi

### A. Mengisi Database

Sebelum menjalankan aplikasi, isi database dengan data awal buku menggunakan perintah:

powershell
python seed.py

File seed.py menyediakan minimal 10 data buku sebagai data awal pengujian.

### B. Menjalankan Server

Jalankan aplikasi menggunakan Uvicorn:

powershell
uvicorn main:app --reload

Jika berhasil, server akan berjalan pada alamat:

http://127.0.0.1:8000

### C. Membuka Dokumentasi API

FastAPI menyediakan dokumentasi interaktif menggunakan Swagger UI.

Buka browser dan akses:

http://127.0.0.1:8000/docs

Melalui Swagger UI, pengguna dapat mencoba setiap endpoint API secara langsung.

## 7. Daftar Endpoint API

### A. Endpoint Pengelolaan Buku

| Method | Endpoint | Fungsi |
|---|---|---|
| GET | /buku?skip=0&limit=10 | Menampilkan daftar buku |
| GET | /buku/{buku_id} | Menampilkan detail buku |
| POST | /buku | Menambahkan buku |
| PUT | /buku/{buku_id} | Memperbarui data buku |
| DELETE | /buku/{buku_id} | Menghapus buku |

### B. Endpoint Transaksi

| Method | Endpoint | Fungsi |
|---|---|---|
| POST | /transactions | Membuat transaksi baru |
| GET | /transactions | Menampilkan daftar transaksi |
| GET | /transactions?status=pending | Menampilkan transaksi berdasarkan status |
| GET | /transactions/{id} | Menampilkan detail transaksi |

### C. Status Transaksi

Sistem menggunakan beberapa status transaksi:

- **Pending**: Transaksi baru dibuat dan menunggu pemrosesan.
- **Processing**: Transaksi sedang diproses.
- **Completed**: Transaksi berhasil diselesaikan.
- **Failed**: Transaksi gagal diproses.

Alur perubahan status transaksi:
text
Pending
   |
   v
Processing
   |
   v
Completed / Failed

## 8. Pengelolaan Stok dan Konkurensi

Sistem menggunakan mekanisme asynchronous untuk memproses transaksi tanpa harus menunggu seluruh proses selesai ketika permintaan transaksi diterima.

Beberapa mekanisme yang diterapkan:

1. **BackgroundTasks** digunakan untuk menjalankan pemrosesan transaksi di latar belakang.
2. **asyncio.Lock** digunakan untuk mengatur akses bersamaan terhadap proses pengurangan stok.
3. **SQL Conditional Update** digunakan untuk memastikan stok hanya dikurangi apabila jumlah stok mencukupi.

Pengurangan stok menggunakan kondisi:

```sql
UPDATE buku
SET stok = stok - ?
WHERE id = ? AND stok >= ?
```

Mekanisme tersebut membantu mencegah stok menjadi negatif ketika beberapa transaksi dilakukan secara bersamaan.

## 9. Pengujian Aplikasi

### A. Pengujian Menggunakan Swagger UI

Pengujian dilakukan melalui:

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

### B. Pengujian Konkurensi

Pengujian konkurensi dilakukan menggunakan file `test_race.py`.

Tujuannya adalah menguji apakah sistem dapat menangani beberapa transaksi yang mengakses stok buku secara bersamaan.

Jalankan perintah:

```powershell
python test_race.py
```

Hasil pengujian digunakan untuk memeriksa:

- Apakah beberapa transaksi dapat dikirim secara bersamaan.
- Apakah stok buku berkurang sesuai jumlah transaksi yang berhasil.
- Apakah sistem menolak transaksi ketika stok tidak mencukupi.
- Apakah stok akhir tetap berada pada nilai nol atau lebih.

### C. Pengujian Beban Menggunakan Locust

Locust digunakan untuk menguji kemampuan API dalam menangani banyak permintaan secara bersamaan.

Pastikan server FastAPI masih berjalan di terminal pertama.

Kemudian buka terminal kedua dan aktifkan virtual environment.

Jalankan perintah:

```powershell
locust -f locustfile.py --host http://127.0.0.1:8000
```

Setelah berhasil, buka browser:

http://localhost:8089

Masukkan jumlah pengguna virtual (Number of users) dan laju pengguna yang akan dijalankan (Spawn rate), kemudian mulai pengujian.

Hasil pengujian dapat dilihat melalui beberapa bagian:

- **Statistics**: Menampilkan jumlah request, response time, dan jumlah request yang gagal.
- **Charts**: Menampilkan grafik performa selama pengujian.
- **Failures**: Menampilkan daftar permintaan yang mengalami kegagalan.
- **Exceptions**: Menampilkan informasi kesalahan yang terjadi selama pengujian.

Pengujian ini bertujuan mengetahui kemampuan API dalam menangani permintaan dengan jumlah pengguna yang berbeda.

## 10. Pengelolaan Database

Aplikasi menggunakan SQLite sebagai sistem penyimpanan data.

Database diinisialisasi melalui fungsi init_db() yang dipanggil ketika aplikasi mulai dijalankan.

Tabel utama yang digunakan adalah tabel `buku, dengan atribut:

| Kolom | Tipe Data | Keterangan |
|---|---|---|
| id | INTEGER | Primary Key |
| judul | TEXT | Judul buku |
| penulis | TEXT | Nama penulis |
| kategori | TEXT | Kategori buku |
| harga | REAL | Harga buku |
| stok | INTEGER | Jumlah persediaan buku |

Kolom stok memiliki batasan agar nilainya tidak kurang dari nol.

## 11. Mengunggah Proyek ke GitHub

Untuk mengunggah proyek ke GitHub, lakukan langkah berikut:

1. Buat repository baru di GitHub.
2. Atur repository menjadi Public.
3. Buka terminal pada folder utama proyek.
4. Inisialisasi Git jika belum dilakukan.
5. Tambahkan seluruh file proyek yang diperlukan.
6. Commit perubahan.
7. Hubungkan folder lokal dengan repository GitHub.
8. Push proyek ke GitHub.

Contoh perintah Git:

bash
git init
git add .
git commit -m "Initial commit Toko Buku Ceria API"
git branch -M main
git remote add origin https://github.com/USERNAME/REPOSITORY.git
git push -u origin main

Ganti USERNAME dan REPOSITORY dengan username serta nama repository GitHub milik sendiri.

Pastikan folder .venv dan file yang tidak diperlukan tidak ikut diunggah ke repository.

## 12. Kesimpulan

Toko Buku Ceria API merupakan aplikasi REST API yang dikembangkan untuk mengelola data buku dan transaksi pembelian menggunakan FastAPI dan SQLite.

Aplikasi ini menerapkan operasi database asynchronous, pemrosesan transaksi menggunakan BackgroundTasks, serta mekanisme pengamanan stok melalui asyncio.Lock dan SQL Conditional Update.

Pengujian dilakukan menggunakan Swagger UI, skrip pengujian konkurensi, dan Locust untuk mengetahui kemampuan sistem dalam menangani permintaan secara bersamaan.

Dengan adanya aplikasi ini, pengelolaan data buku dan transaksi dapat dilakukan melalui endpoint API secara terstruktur dan terdokumentasi.
