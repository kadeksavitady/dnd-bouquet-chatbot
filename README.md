# dnd.bouquet Telegram Chatbot

Repositori ini berisi implementasi chatbot Telegram untuk asisten layanan pelanggan dnd.bouquet (Dear n Deep). Proyek ini dibangun menggunakan Python dan mengintegrasikan model Large Language Model (LLM) melalui Groq API. 

Proyek ini disusun sebagai pemenuhan tugas Lab 01: Simple Chatbot with Groq API pada mata kuliah Large Language Modelling (LLM) Implementation.

## Fitur Utama

- **Integrasi Groq API:** Menggunakan model Qwen (via Groq API) untuk memproses pesan dan menghasilkan teks balasan berbahasa Indonesia yang sesuai dengan instruksi (*System Prompt*).
- **Manajemen Konteks Percakapan:** Chatbot mampu mengingat konteks obrolan dalam satu sesi. Sistem secara otomatis membatasi memori maksimal 20 pesan terakhir untuk mencegah *error token limit*.
- **Penyimpanan Riwayat Percakapan:** Setiap sesi percakapan disimpan secara lokal ke dalam format `.json` di dalam folder `chat_histories/`.
- **Proteksi Spam (Rate Limiting):** Terdapat batasan jeda waktu (3 detik) untuk mencegah pengguna mengirim pesan secara beruntun (*spam*).
- **Penanganan Tipe Media:** Chatbot dikonfigurasi untuk hanya merespons pesan teks. Jika pengguna mengirim foto, dokumen, atau stiker, bot akan memberikan balasan standar.
- **Keamanan Kredensial:** Konfigurasi token dan API key disimpan secara terpisah menggunakan file `.env`.

## Prasyarat Sistem

Sebelum menjalankan program ini, pastikan Anda telah memiliki:
1. Python 3.10 atau versi yang lebih baru.
2. Token Telegram Bot (didapatkan dari @BotFather).
3. Groq API Key (didapatkan dari console.groq.com).

## Panduan Instalasi dan Penggunaan

**1. Clone Repositori**
```bash
git clone [https://github.com/kadeksavitady/dnd-bouquet-chatbot.git](https://github.com/USERNAME_ANDA/dnd-bouquet-chatbot.git)
cd dnd-bouquet-chatbot

**2. Instalasi Dependensi**
Instal pustaka Python yang dibutuhkan dengan menjalankan perintah berikut:
```pip install pyTelegramBotAPI groq python-dotenv
```

**3. Konfigurasi Environment Variables**
Buat sebuah file baru bernama .env di dalam folder utama proyek ini. Buka file tersebut dan masukkan kredensial Anda dengan format berikut:
```TELEGRAM_TOKEN=masukkan_token_bot_telegram_di_sini
GROQ_API_KEY=masukkan_api_key_groq_di_sini
```

**4. Menjalankan Chatbot**
Jalankan skrip utama melalui terminal:
```python bot.py
```
Jika muncul pesan "Bot dnd.bouquet sudah berjalan. Silakan chat bot kamu di Telegram!", berarti sistem sudah aktif dan bot siap digunakan di Telegram.

## Struktur Direktori

- bot.py : Skrip utama yang berisi logika chatbot, penanganan antarmuka Telegram, dan integrasi Groq API.
- chat_histories/ : Folder (terbuat otomatis) untuk menyimpan log percakapan dalam format .json.
- .env : File konfigurasi kredensial (tidak diunggah ke GitHub).
- .gitignore : Berisi daftar file dan folder yang diabaikan oleh sistem Git.
- README.md / README.txt : Dokumentasi informasi proyek.