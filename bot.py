import os
from flask import Flask, request
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing")
if not RENDER_EXTERNAL_URL:
    raise ValueError("RENDER_EXTERNAL_URL is missing")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ───────── BOT COMMANDS ─────────

@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "🛡️ Welcome to *Cyber Rakshak*\n\n"
        "Your cyber safety assistant.\n\n"
        "Type /help to see what I can do.",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=["help"])
def help_cmd(msg):
    bot.send_message(
        msg.chat.id,
        "🆘 *Cyber Rakshak Help*\n\n"
        "• Scam awareness\n"
        "• Cyber safety tips\n"
        "• Report guidance\n\n"
        "More features coming soon 🚀",
        parse_mode="Markdown"
    )

# ───────── WEBHOOK ─────────

@app.route("/webhook", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def index():
    return "Cyber Rakshak Bot is Live ✅"

# ───────── START SERVER ─────────

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{RENDER_EXTERNAL_URL}/webhook")

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
