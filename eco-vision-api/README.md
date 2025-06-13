# Eco Vision API

Eco Vision API adalah backend untuk aplikasi klasifikasi sampah dengan pendekatan gamifikasi. Layanan ini dibangun menggunakan Django dan menerapkan autentikasi JWT lengkap dengan sistem EXP dan level pengguna.

## Struktur Proyek

```
├── eco_vision_api_django/   # kode Django dan Docker
│   ├── manage.py
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── eco_vision_api/
│       └── ...
├── openapi.yaml             # spesifikasi OpenAPI 3.1
```

### Django Apps

- **eco_vision_api_auth_app** – registrasi, login, token refresh, serta endpoint contoh yang dilindungi. Model `User` menyimpan level dan exp pengguna.
- **eco_vision_api_edu_app** – memuat model TensorFlow (`best_model.h5`) untuk mengklasifikasikan gambar dan memberi rekomendasi bank sampah terdekat.
- **eco_vision_api_bank_app** – menyimpan daftar bank sampah, jenis sampah (`WasteType`), serta jam operasional (`OpeningHour`).
- **eco_vision_api_leader_board_app** – menampilkan papan peringkat pengguna berdasarkan perolehan exp.

## OpenAPI

File [`openapi.yaml`](openapi.yaml) berisi dokumentasi lengkap REST API. Di awal file juga disediakan contoh konfigurasi Docker Compose sekaligus informasi masa berlaku token autentikasi.

```yaml
services:
  eco-vision-api:
    image: farizi/eco-vision-api:latest
    ports:
      - "8000:8000"
    volumes:
      - eco_db_data:/data

volumes:
  eco_db_data:
```

Token Access berlaku 5 menit sementara Refresh Token berlaku 1 hari.

Beberapa endpoint utama antara lain:
- `/auth/register` – registrasi pengguna baru.
- `/auth/login` – memperoleh token akses dan refresh.
- `/predict/` – klasifikasi gambar sampah dengan rekomendasi bank sampah.
- `/waste-banks` – daftar sekaligus pembuatan bank sampah baru.
- `/leaderboard/` – melihat papan peringkat pengguna.

## Menjalankan dengan Docker

1. Pastikan Docker dan Docker Compose terpasang.
2. Masuk ke direktori `eco_vision_api_django`.
3. Tarik image Docker terbaru: `docker pull farizi/eco-vision-api`
4. Jalankan `docker compose up` untuk menarik image dan memulai server di port 8000.

Script `entrypoint.sh` akan otomatis menjalankan migrasi, memuat data awal dari `initial_waste_types.json`, `initial_trash_can.json`, dan `initial_waste_bank.json`, lalu mengeksekusi Django `runserver` jika database belum ada.

## Catatan Tambahan

Dokumentasi HTML API akan otomatis di-deploy ke cabang `gh-pages` setiap kali `openapi.yaml` diperbarui (lihat workflow GitHub Actions).
Anda dapat melihat versi terbarunya di [https://tsfarizi.github.io/eco-vision-api/](https://tsfarizi.github.io/eco-vision-api/).