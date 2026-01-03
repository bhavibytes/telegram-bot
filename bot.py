import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

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
        "🛡️ Welcome to *Cyber Rakshak*\nYour cyber safety assistant",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text("🚧 Feature coming soon!")

# ---------- MAIN ----------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Cyber Rakshak Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
