import os
from flask import Flask, request
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

BOT_TOKEN = os.getenv("BOT_TOKEN")
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ───────── KEYBOARD ─────────
def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton("🛡️ Cyber Safety Tips"),
        KeyboardButton("🚨 Report a Scam")
    )
    kb.add(
        KeyboardButton("📘 Learn Cyber Safety"),
        KeyboardButton("ℹ️ About Cyber Rakshak")
    )
    return kb

# ───────── COMMANDS ─────────
@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "🛡️ *Welcome to Cyber Rakshak*\n\n"
        "Your cyber safety assistant.\n\n"
        "Choose an option below 👇",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

# ───────── TEXT HANDLERS ─────────
@bot.message_handler(func=lambda m: True)
def handle_text(msg):
    text = msg.text.lower()

    if "safety" in text:
        bot.send_message(
            msg.chat.id,
            "🛡️ *Cyber Safety Tips*\n\n"
            "• Never share OTP\n"
            "• Verify links before clicking\n"
            "• Banks never ask for passwords\n"
            "• Enable 2FA everywhere",
            parse_mode="Markdown"
        )

    elif "report" in text:
        bot.send_message(
            msg.chat.id,
            "🚨 *How to Report a Cyber Crime (India)*\n\n"
            "1️⃣ Visit https://cybercrime.gov.in\n"
            "2️⃣ Call 1930 immediately\n"
            "3️⃣ Save screenshots & call logs",
            parse_mode="Markdown"
        )

    elif "learn" in text:
        bot.send_message(
            msg.chat.id,
            "📘 *Learning Modules Coming Soon*\n\n"
            "You’ll soon get:\n"
            "• Scam simulations\n"
            "• Quizzes\n"
            "• Awareness videos"
        )

    elif "about" in text:
        bot.send_message(
            msg.chat.id,
            "ℹ️ *Cyber Rakshak*\n\n"
            "Built to educate and protect users\n"
            "from cyber frauds & scams.\n\n"
            "🌐 cyber safety for everyone",
            parse_mode="Markdown"
        )

    else:
        bot.send_message(
            msg.chat.id,
            "❓ I didn’t understand that.\n\n"
            "Please choose an option from the menu 👇",
            reply_markup=main_menu()
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

# ───────── START ─────────
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{RENDER_EXTERNAL_URL}/webhook")

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
