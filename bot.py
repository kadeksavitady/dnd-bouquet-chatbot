import os
import json
import time
import telebot
from groq import Groq
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv()  # Muat variabel dari file .env

# ==========================================================
# 1. KREDENSIAL - diambil dari environment variable, BUKAN hardcode
# ==========================================================
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not TELEGRAM_TOKEN or not GROQ_API_KEY:
    raise RuntimeError(
        "TELEGRAM_TOKEN atau GROQ_API_KEY belum diset. "
        "Set sebagai environment variable atau lewat file .env."
    )

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

# ==========================================================
# 2. KONFIGURASI
# ==========================================================
MAX_HISTORY_MESSAGES = 20   # jumlah pesan (user+assistant) yang disimpan, di luar system prompt
RATE_LIMIT_SECONDS = 3      # jeda minimum antar pesan per user
HISTORY_DIR = "chat_histories"

os.makedirs(HISTORY_DIR, exist_ok=True)

SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "Kamu adalah asisten customer service virtual yang ramah untuk dnd.bouquet (Dear n Deep). "
        "Tugasmu menawarkan produk dnd.bouquet (Dear n Deep) kepada pelanggan, yaitu bouquet artificial "
        "flowers, bouquet pipecleaner (kawat bulu) flowers, bouquet fresh flowers, ataupun aksesoris "
        "seperti jepit rambut atau gantungan kunci dari pipecleaner (kawat bulu). Selain itu juga membantu "
        "pelanggan dalam memilih dan memesan produk tersebut. Jawab dengan ramah, gunakan sapaan 'Kak', "
        "dan batasi jawaban maksimal 2-3 paragraf pendek. "
        "PENTING: Kamu tidak bisa menampilkan foto atau gambar produk secara langsung. "
        "Jika pelanggan ingin melihat contoh produk, foto, katalog, atau desain, "
        "arahkan mereka ke Instagram dnd.bouquet dengan kalimat yang tetap nyambung dengan konteks percakapan sebelumnya. "
        "Contoh kalimat: 'Kak bisa langsung lihat-lihat koleksi dan foto produk kami di Instagram ya: "
        "https://www.instagram.com/dnd.bouquett/ — di sana Kakak bisa pilih desain yang paling cocok! 🌸'"
    ),
}


# Memori percakapan & rate-limit tracker in-memory
user_histories = {}
last_message_time = {}


# ==========================================================
# 3. UTIL
# ==========================================================
def history_path(chat_id):
    # chat_id Telegram selalu integer, aman dipakai di nama file
    return os.path.join(HISTORY_DIR, f"riwayat_chat_{chat_id}.json")


def load_history(chat_id):
    path = history_path(chat_id)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return [SYSTEM_PROMPT]


def save_history(chat_id):
    path = history_path(chat_id)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(user_histories[chat_id], f, indent=2, ensure_ascii=False)
    except OSError as e:
        print(f"Gagal menyimpan riwayat chat {chat_id}: {e}")


def trim_history(chat_id):
    """Jaga riwayat tetap pendek: system prompt + N pesan terakhir."""
    history = user_histories[chat_id]
    if len(history) > MAX_HISTORY_MESSAGES + 1:
        user_histories[chat_id] = [history[0]] + history[-MAX_HISTORY_MESSAGES:]


def is_rate_limited(chat_id):
    now = time.time()
    last = last_message_time.get(chat_id, 0)
    if now - last < RATE_LIMIT_SECONDS:
        return True
    last_message_time[chat_id] = now
    return False


# ==========================================================
# 4. HANDLER
# Hanya pesan bertipe teks yang diproses (foto/stiker/voice diabaikan aman)
# ==========================================================
@bot.message_handler(content_types=["text"])
def handle_message(message):
    chat_id = message.chat.id
    user_text = message.text

    if is_rate_limited(chat_id):
        bot.reply_to(message, "Mohon tunggu sebentar ya, Kak, sebelum kirim pesan berikutnya \U0001F64F")
        return

    if chat_id not in user_histories:
        user_histories[chat_id] = load_history(chat_id)

    user_histories[chat_id].append({"role": "user", "content": user_text})
    trim_history(chat_id)

    try:
        response = client.chat.completions.create(
            messages=user_histories[chat_id],
            model="qwen/qwen3.8-27b",
            temperature=0.7,
        )

        bot_reply = response.choices[0].message.content

        user_histories[chat_id].append({"role": "assistant", "content": bot_reply})
        trim_history(chat_id)
        save_history(chat_id)

        bot.reply_to(message, bot_reply)

    except Exception as e:
        bot.reply_to(message, "Mohon Maaf, sistem kami sedang sibuk. Mohon tunggu sebentar ya! 🙏")
        print(f"Terjadi error: {e}")


@bot.message_handler(func=lambda m: True, content_types=[
    "audio", "document", "photo", "sticker", "video", "voice", "location", "contact"
])
def handle_non_text(message):
    bot.reply_to(message, "Maaf Kak, saat ini aku hanya bisa membalas pesan teks ya \U0001F338")


# ==========================================================
# 5. RUN
# ==========================================================
if __name__ == "__main__":
    print("Bot dnd.bouquet sudah berjalan. Silakan chat bot kamu di Telegram!")
    bot.infinity_polling(timeout=30, long_polling_timeout=30)