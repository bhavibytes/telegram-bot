import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# ---------- UTIL ----------
def log_event(text):
    if ADMIN_CHAT_ID:
        bot.send_message(ADMIN_CHAT_ID, f"📊 <b>Bot Log</b>\n{text}")

# ---------- MAIN MENU ----------
def main_menu():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🛑 Report Cyber Crime", callback_data="report"),
        InlineKeyboardButton("🚨 Scam Alerts", callback_data="alerts"),
        InlineKeyboardButton("🧠 Scam Checker", callback_data="check"),
        InlineKeyboardButton("📞 Emergency Help", callback_data="emergency"),
        InlineKeyboardButton("🌐 Visit Website", url="https://cyberrakshak-7284e.web.app")
    )
    return kb

# ---------- START ----------
@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "🛡️ <b>Cyber Rakshak</b>\nYour personal cyber safety assistant 🇮🇳",
        reply_markup=main_menu()
    )
    log_event(f"User started bot: {msg.chat.id}")

# ---------- CALLBACK HANDLER ----------
@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    if call.data == "report":
        bot.send_message(
            call.message.chat.id,
            "🛑 <b>Report Cyber Crime</b>\n\n"
            "📌 National Portal:\n"
            "https://cybercrime.gov.in\n\n"
            "📞 Helpline: <b>1930</b>"
        )

    elif call.data == "alerts":
        bot.send_message(
            call.message.chat.id,
            "🚨 <b>Latest Scam Alerts</b>\n\n"
            "⚠️ Fake delivery SMS\n"
            "⚠️ WhatsApp job scam\n"
            "⚠️ Fake KYC calls\n\n"
            "Never share OTP / bank details."
        )

    elif call.data == "check":
        bot.send_message(
            call.message.chat.id,
            "🧠 <b>Scam Checker</b>\n\n"
            "📩 Send me the suspicious message or link."
        )
        bot.register_next_step_handler(call.message, scam_check)

    elif call.data == "emergency":
        bot.send_message(
            call.message.chat.id,
            "📞 <b>Emergency Help (India)</b>\n\n"
            "🚨 Cyber Crime: <b>1930</b>\n"
            "👮 Police: <b>112</b>\n"
            "🏦 Bank Fraud: Contact your bank immediately"
        )

# ---------- SCAM CHECKER ----------
def scam_check(msg):
    text = msg.text.lower()

    scam_keywords = [
        "otp", "lottery", "urgent", "kyc",
        "click link", "verify account",
        "free money", "prize", "bank blocked"
    ]

    score = sum(word in text for word in scam_keywords)

    if score >= 2:
        result = "🚨 <b>Likely SCAM</b>\n\n⚠️ Do NOT click links or share details."
    else:
        result = "✅ <b>Looks Safe</b>\n\nBut stay cautious."

    bot.send_message(msg.chat.id, result)
    log_event(f"Scam check by {msg.chat.id} | Score: {score}")

# ---------- KEEP ALIVE ----------
print("🤖 Cyber Rakshak Bot is running...")
bot.infinity_polling()
