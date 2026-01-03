import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("https://cyber-rakshak-telegram-bot.onrender.com")  # Render URL

# ---------- KEYBOARD ----------
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛑 Report Cyber Crime", callback_data="report")],
        [InlineKeyboardButton("🚨 Scam Alerts", callback_data="alerts")],
        [InlineKeyboardButton("🧠 Scam Checker", callback_data="scam_check")],
        [InlineKeyboardButton("📞 Emergency Help", callback_data="emergency")],
        [InlineKeyboardButton("🌐 Visit Website", url="https://cyberrakshak-7284e.web.app")]
    ])

# ---------- HANDLERS ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛡️ Welcome to Cyber Rakshak\nYour cyber safety assistant",
        reply_markup=main_menu()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.message.reply_text("Feature coming soon")

# ---------- MAIN ----------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    PORT = int(os.environ.get("PORT", 10000))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=f"{https://cyber-rakshak-telegram-bot.onrender.com}/{BOT_TOKEN}"
    )

if __name__ == "__main__":
    main()
