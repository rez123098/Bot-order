
import telebot
from telebot import types
import os

# Load configuration
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = os.getenv("OWNER_ID")
ADMIN_GROUP_ID = os.getenv("ADMIN_GROUP_ID")

bot = telebot.TeleBot(BOT_TOKEN)

# Products available
products = {
    'Kopi Ais': 10,
    'Teh Tarik': 8,
    'Milo': 5
}

# Command for /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Selamat datang! Pilih produk untuk order:", reply_markup=create_product_markup())

# Create product selection buttons
def create_product_markup():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for product in products:
        markup.add(product)
    return markup

# Handle user selection
@bot.message_handler(func=lambda message: message.text in products)
def handle_order(message):
    product = message.text
    bot.send_message(message.chat.id, f"Produk {product} telah dipilih. Sila buat pembayaran dan hantar resit.")
    send_qr_code(message)

# Send payment QR code
def send_qr_code(message):
    qr_code_path = "qr.png"  # Assume a QR image is present
    with open(qr_code_path, 'rb') as qr:
        bot.send_photo(message.chat.id, qr, caption="Sila bayar ke akaun berikut: Maybank 123456789")
    bot.send_message(message.chat.id, "Sila upload resit pembayaran.")

# Handle resit upload
@bot.message_handler(content_types=['document'])
def handle_resit(message):
    bot.send_message(ADMIN_GROUP_ID, f"Order baru dari {message.from_user.username}!
Resit: {message.document.file_name}")
    bot.send_message(message.chat.id, "Resit diterima, admin akan memproses pesanan anda.")

# Run the bot
bot.polling()
    