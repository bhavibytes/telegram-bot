import os
import telebot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN missing")

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "🛡️ Cyber Rakshak Bot is LIVE!\n\nSend any message to test."
    )


@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, f"✅ You said: {message.text}")


print("🤖 Bot running...")
bot.infinity_polling()
