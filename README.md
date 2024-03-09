# Tubes1_FreeDiamonds

Tugas Besar Mata Kuliah IF2211 Strategi Algoritma 2024 - Pemanfaatan Algoritma Greedy dalam pembuatan bot permainan Diamonds

## Table of Contents
- [Algoritma Greedy](#algoritma-greedy-yang-diimplementasikan)
- [Requirements dan Instalasi](#requirement-program-dan-instalasi)
- [Cara Menjalankan Program](#cara-menjalankan-program)
- [Authors](#authors)

## Algoritma Greedy yang Diimplementasikan
Algoritma Greedy yang diimplementasikan berfokus pada pencarian diamond dengan densitas terbesar yang dihitung dari rasio nilai poin diamond terhadap jarak dari posisi bot ke diamond tersebut. Strategi ini memprioritaskan diamond dengan nilai poin lebih besar ketika densitasnya sama, dan berfokus pada diamond poin 1 terdekat ketika inventory hampir penuh.

## Requirement Program dan Instalasi

### Game Engine
- **Requirement yang Harus Di-install**:
  - Node.js
  - Docker desktop
  - Yarn

- **Instalasi dan Konfigurasi Awal**:
  1. Download dan extract source code game engine.
  2. Buka terminal di folder hasil extract.
  3. Masuk ke root directory.

     ```bash
     cd tubes1-IF2110-game-engine-1.1.0
     ```
  4. Install dependencies dengan Yarn.

     ```bash
     yarn
     ```
  5. Setup environment variables.

     - Windows:

       ```bash
       ./scripts/copy-env.bat
       ```

     - Linux/macOS:

       ```bash
       chmod +x ./scripts/copy-env.sh
       ./scripts/copy-env.sh
       ```

  6. Setup local database (pastikan Docker desktop sudah berjalan).

     ```bash
     docker compose up -d database
     ./scripts/setup-db-prisma.bat # Untuk Windows
     ./scripts/setup-db-prisma.sh # Untuk Linux/macOS
     ```

### Bot
- **Requirement yang Harus Di-install**:
  - Python

- **Instalasi dan Konfigurasi Awal**:
  1. Masuk ke direktori `src`

     ```bash
     cd src
     ```
  2. Install dependencies menggunakan pip.

     ```bash
     pip install -r requirements.txt
     ```

## Cara Menjalankan Program

### Build dan Run Game Engine
- **Build**:

  ```bash
  npm run build
  ```

- **Run**:

    ```bash
    npm run start
    ```

- **Menjalankan satu bot**:

    ```bash
    python main.py --logic FreeDiamonds --email=diamondsfree@email.com --name=diamonds --password=stimantap --team etimo
    ```

- **Menjalankan Multiple Bots**:

  **Untuk Windows**:
  ```
  ./run-bots.bat
  ```
  **Untuk Linux/macOS**:
  ```
  ./run-bots.sh
  ```

Perhatikan bot yang telah bergabung melalui frontend. Saat permainan selesai, final score akan muncul pada sisi kanan bawah.

**NOTE**:
1. Jika menjalankan beberapa bot, pastikan setiap email dan nama unik.
2. Email bisa apa saja asalkan mengikuti format email yang benar. Tidak harus email yang terdaftar.
3. Nama dan password bisa apa saja tanpa spasi.

## Authors
Kelompok FreeDiamonds
- Lidya Rahmatul Fitri - 10023485
- Rafii Ahmad Fahreza - 10023570
- Novelya Putri Ramadhani - 13522096
- Diana Tri Handayani - 13522104