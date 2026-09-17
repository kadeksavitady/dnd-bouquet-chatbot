# dnd.bouquet Telegram Chatbot

Repositori ini berisi implementasi chatbot Telegram untuk asisten layanan pelanggan **dnd.bouquet (Dear n Deep)**. Proyek ini dibangun menggunakan Python dan mengintegrasikan Large Language Model (LLM) melalui **Groq API**.

Proyek ini disusun sebagai pemenuhan tugas Lab 01: *Simple Chatbot with Groq API* pada mata kuliah Large Language Modelling (LLM) Implementation.

## Fitur Utama

- **Integrasi Groq API:** Menggunakan model `qwen/qwen3.8-27b` (via Groq API) untuk memproses pesan dan menghasilkan teks balasan berbahasa Indonesia sesuai instruksi (*system prompt*). Model dapat diganti lewat environment variable `GROQ_MODEL` tanpa mengubah kode.
- **Manajemen Konteks Percakapan:** Chatbot mengingat konteks obrolan per pengguna. Sistem otomatis membatasi memori maksimal 20 pesan terakhir untuk mencegah *error token limit* dan menghemat biaya API.
- **Redirect ke Instagram untuk Konten Visual:** Karena bot tidak bisa mengirim gambar, jika pelanggan minta lihat foto/katalog/desain produk, bot otomatis mengarahkan ke akun Instagram [@dnd.bouquett](https://www.instagram.com/dnd.bouquett/) dengan kalimat yang tetap nyambung ke konteks percakapan.
- **Penyimpanan Riwayat Percakapan:** Setiap sesi percakapan disimpan lokal dalam format `.json` di folder `chat_histories/`, dan dimuat ulang otomatis saat bot di-restart.
- **Proteksi Spam (Rate Limiting):** Ada jeda minimum 3 detik antar pesan per pengguna untuk mencegah spam ke API Groq.
- **Penanganan Tipe Media:** Bot hanya merespons pesan teks. Pesan foto, dokumen, stiker, voice note, dll. dibalas dengan pesan standar tanpa membuat bot error.
- **Auto-retry Polling:** Menggunakan `infinity_polling()` agar bot lebih tahan terhadap gangguan koneksi.
- **Keamanan Kredensial:** Token Telegram dan API key Groq disimpan lewat file `.env`, tidak pernah di-hardcode di kode sumber.

## Prasyarat Sistem

Sebelum menjalankan program ini, pastikan Anda telah memiliki:

1. Python 3.9 atau versi yang lebih baru.
2. Token Telegram Bot (didapatkan dari [@BotFather](https://t.me/BotFather)).
3. Groq API Key (didapatkan dari [console.groq.com](https://console.groq.com)).

## Panduan Instalasi dan Penggunaan

**1. Clone Repositori**

```bash
git clone https://github.com/USERNAME_ANDA/dnd-bouquet-chatbot.git
cd dnd-bouquet-chatbot
```

**2. Instalasi Dependensi**

Instal pustaka Python yang dibutuhkan:

```bash
pip install pyTelegramBotAPI groq python-dotenv
```

**3. Konfigurasi Environment Variables**

Salin `.env.example` menjadi `.env`:

```bash
cp .env.example .env
```

Buka file `.env` dan isi dengan kredensial Anda:

```
TELEGRAM_TOKEN=masukkan_token_bot_telegram_di_sini
GROQ_API_KEY=masukkan_api_key_groq_di_sini
```

> File `.env` tidak boleh diunggah ke GitHub — sudah dimasukkan ke `.gitignore`.

**4. Menjalankan Chatbot**

Jalankan skrip utama melalui terminal:

```bash
python bot.py
```

Jika muncul pesan berikut, berarti sistem sudah aktif dan bot siap digunakan di Telegram:

```
Bot dnd.bouquet sudah berjalan. Silakan chat bot kamu di Telegram!
```

## Konfigurasi Tambahan

Beberapa parameter bisa disesuaikan langsung di `bot.py` atau lewat environment variable:

| Variabel               | Default                | Keterangan                                         |
|-------------------------|--------------------------|------------------------------------------------------|
| `GROQ_MODEL`            | `qwen/qwen3.8-27b`      | Model Groq yang digunakan                            |
| `MAX_HISTORY_MESSAGES`  | `20`                    | Jumlah pesan terakhir yang disimpan sebagai konteks  |
| `RATE_LIMIT_SECONDS`    | `3`                     | Jeda minimum antar pesan per pengguna                |
| `HISTORY_DIR`           | `chat_histories`        | Folder penyimpanan riwayat chat                      |

> Model Groq sewaktu-waktu bisa di-*deprecate*. Jika muncul error `model_not_found`, cek daftar model aktif di [Groq Console](https://console.groq.com/docs/models) dan perbarui `GROQ_MODEL`.

## Struktur Direktori

- `bot.py` — Skrip utama: logika chatbot, penanganan antarmuka Telegram, dan integrasi Groq API.
- `chat_histories/` — Folder (terbuat otomatis) untuk menyimpan log percakapan dalam format `.json`.
- `.env` — File konfigurasi kredensial (tidak diunggah ke GitHub).
- `.env.example` — Contoh format file `.env` tanpa kredensial asli.
- `.gitignore` — Daftar file dan folder yang diabaikan oleh Git.
- `README.md` — Dokumentasi proyek ini.

## Catatan Keamanan

- Token Telegram dan API key Groq wajib diisi lewat environment variable, jangan pernah di-hardcode di kode sumber.
- Folder `chat_histories/` berisi data percakapan pelanggan — jangan diunggah ke repo publik.

## Kontak

Dikembangkan untuk **dnd.bouquet (Dear n Deep)**.