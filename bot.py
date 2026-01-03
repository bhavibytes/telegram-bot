import os
from flask import Flask, request
import telebot

# =====================
# ENV VARIABLES
# =====================
BOT_TOKEN = os.getenv("BOT_TOKEN")
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# =====================
# LANGUAGE BUTTONS
# =====================
def language_buttons():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        telebot.types.InlineKeyboardButton("🇮🇳 हिंदी", callback_data="lang_hi")
    )
    return markup

# =====================
# MAIN MENU BUTTONS
# =====================
def main_menu(lang="en"):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)

    if lang == "hi":
        markup.add(
            telebot.types.InlineKeyboardButton("🛡️ साइबर सुरक्षा टिप्स", callback_data="tips_hi"),
            telebot.types.InlineKeyboardButton("🚨 साइबर फ्रॉड रिपोर्ट करें", callback_data="report_hi"),
            telebot.types.InlineKeyboardButton("📘 साइबर फ्रॉड सीखें", callback_data="learn_hi"),
            telebot.types.InlineKeyboardButton("ℹ️ Cyber Rakshak के बारे में", callback_data="about_hi")
        )
    else:
        markup.add(
            telebot.types.InlineKeyboardButton("🛡️ Cyber Safety Tips", callback_data="tips_en"),
            telebot.types.InlineKeyboardButton("🚨 Report Cyber Fraud", callback_data="report_en"),
            telebot.types.InlineKeyboardButton("📘 Learn About Frauds", callback_data="learn_en"),
            telebot.types.InlineKeyboardButton("ℹ️ About Cyber Rakshak", callback_data="about_en")
        )

    return markup

# =====================
# START COMMAND
# =====================
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "🛡️ *Welcome to Cyber Rakshak*\n\n"
        "Your trusted cyber safety assistant 👮‍♂️\n\n"
        "Please choose your language:",
        reply_markup=language_buttons(),
        parse_mode="Markdown"
    )

# =====================
# CALLBACK HANDLER
# =====================
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    bot.answer_callback_query(call.id)

    # ---------- LANGUAGE ----------
    if call.data == "lang_en":
        bot.edit_message_text(
            "✅ *Language set to English*\n\n"
            "How can I help you today?",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=main_menu("en"),
            parse_mode="Markdown"
        )

    elif call.data == "lang_hi":
        bot.edit_message_text(
            "✅ *भाषा हिंदी चुनी गई*\n\n"
            "मैं आपकी कैसे मदद कर सकता हूँ?",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=main_menu("hi"),
            parse_mode="Markdown"
        )

    # ---------- ENGLISH OPTIONS ----------
    elif call.data == "tips_en":
        bot.send_message(
            call.message.chat.id,
            "🛡️ *Cyber Safety Tips*\n\n"
            "• Never share OTP or passwords\n"
            "• Avoid unknown links\n"
            "• Use strong passwords\n"
            "• Enable 2-factor authentication",
            parse_mode="Markdown"
        )

    elif call.data == "report_en":
        bot.send_message(
            call.message.chat.id,
            "🚨 *Report Cyber Fraud*\n\n"
            "📞 National Cyber Crime Helpline: *1930*\n"
            "🌐 https://cybercrime.gov.in",
            parse_mode="Markdown"
        )

    elif call.data == "learn_en":
        bot.send_message(
            call.message.chat.id,
            "📘 *Common Online Frauds*\n\n"
            "• Phishing scams\n"
            "• Fake job offers\n"
            "• OTP frauds\n"
            "• UPI scams",
            parse_mode="Markdown"
        )

    elif call.data == "about_en":
        bot.send_message(
            call.message.chat.id,
            "ℹ️ *About Cyber Rakshak*\n\n"
            "Cyber Rakshak is an initiative to educate and protect users "
            "from cyber crimes through awareness and guidance.",
            parse_mode="Markdown"
        )

    # ---------- HINDI OPTIONS ----------
    elif call.data == "tips_hi":
        bot.send_message(
            call.message.chat.id,
            "🛡️ *साइबर सुरक्षा टिप्स*\n\n"
            "• OTP या पासवर्ड साझा न करें\n"
            "• अनजान लिंक पर क्लिक न करें\n"
            "• मजबूत पासवर्ड रखें\n"
            "• 2-स्टेप वेरिफिकेशन चालू रखें",
            parse_mode="Markdown"
        )

    elif call.data == "report_hi":
        bot.send_message(
            call.message.chat.id,
            "🚨 *साइबर फ्रॉड रिपोर्ट करें*\n\n"
            "📞 साइबर क्राइम हेल्पलाइन: *1930*\n"
            "🌐 https://cybercrime.gov.in",
            parse_mode="Markdown"
        )

    elif call.data == "learn_hi":
        bot.send_message(
            call.message.chat.id,
            "📘 *आम साइबर फ्रॉड*\n\n"
            "• फिशिंग स्कैम\n"
            "• नकली नौकरी ऑफर\n"
            "• OTP फ्रॉड\n"
            "• UPI स्कैम",
            parse_mode="Markdown"
        )

    elif call.data == "about_hi":
        bot.send_message(
            call.message.chat.id,
            "ℹ️ *Cyber Rakshak के बारे में*\n\n"
            "Cyber Rakshak एक पहल है जो लोगों को "
            "साइबर अपराधों से जागरूक और सुरक्षित रखने के लिए बनाई गई है।",
            parse_mode="Markdown"
        )

# =====================
# FLASK WEBHOOK
# =====================
@app.route("/webhook", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def home():
    return "Cyber Rakshak Bot is Live ✅"

# =====================
# MAIN
# =====================
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{RENDER_EXTERNAL_URL}/webhook")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
