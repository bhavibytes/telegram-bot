import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL")

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
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("Feature coming soon")

# ---------- MAIN ----------
def main():
    if not BOT_TOKEN or not RENDER_EXTERNAL_URL:
        raise ValueError("BOT_TOKEN or RENDER_EXTERNAL_URL is missing")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    PORT = int(os.environ.get("PORT", 10000))

    webhook_url = f"{RENDER_EXTERNAL_URL}/{BOT_TOKEN}"

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=webhook_url
    )

    print("✅ Bot running with webhook:", webhook_url)

if __name__ == "__main__":
    main()
