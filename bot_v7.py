# Bot Telegram untuk OSINT V7
# Jalankan bot ini untuk menerima perintah OSINT dari Telegram

import telebot
import osint_v7

TOKEN = "7275073146:AAGlJkPAhdhhmRLU5CiLF3nFSeeTWjZV_ic"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start", "help"])
def start(msg):
    bot.reply_to(msg, "Kirim /scan <nomor> untuk OSINT.
Contoh: /scan 081234567890")

@bot.message_handler(commands=["scan"])
def scan(msg):
    try:
        nomor = msg.text.split(" ")[1]
        bot.reply_to(msg, f"🔎 Memproses {nomor}...")
        hasil = osint_v7.proses(nomor)
        bot.reply_to(msg, hasil)
    except:
        bot.reply_to(msg, "Format salah. Gunakan: /scan 081234567890")

bot.infinity_polling()


@bot.message_handler(content_types=["photo"])
def handle_image(msg):
    try:
        file_info = bot.get_file(msg.photo[-1].file_id)
        downloaded = bot.download_file(file_info.file_path)
        filename = f"image_{msg.message_id}.jpg"
        with open(filename, "wb") as f:
            f.write(downloaded)
        hasil = osint_v7.reverse_image_search_gimage(filename)
        bot.reply_to(msg, hasil)
        os.remove(filename)
    except Exception as e:
        bot.reply_to(msg, f"Terjadi kesalahan: {str(e)}")
