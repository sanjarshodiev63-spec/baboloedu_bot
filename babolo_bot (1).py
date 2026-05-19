#!/usr/bin/env python3
"""
Babolo O'qib Markazi - Telegram Bot
Ishlatish: pip install python-telegram-bot==20.7
"""

import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler, CallbackQueryHandler
)

# =============================================
# BOT TOKEN - BotFather dan olgan tokeningiz
# =============================================
BOT_TOKEN = "BU_YERGA_BOT_TOKENINI_KIRITING"

# =============================================
# O'QUV MARKAZ MA'LUMOTLARI - O'ZGARTIRING
# =============================================
MARKAZ_NOMI = "Babolo O'qib Markazi"
MANZIL = "📍 Toshkent sh., Chilonzor tumani, 5-mavze, 12-uy"
TELEFON = "📞 +998 90 123 45 67"
TELEFON2 = "📞 +998 91 234 56 78"
ISH_VAQTI = "🕐 Dush-Shan: 08:00 - 20:00"
KARTA_RAQAM = "💳 8600 1234 5678 9012"
KARTA_EGASI = "👤 Rahmatullayev Bobur"
BANK = "🏦 Kapitalbank"

# O'qituvchilar ro'yxati
OQITUVCHILAR = [
    {
        "ism": "Karimov Jasur",
        "fan": "Matematika",
        "tajriba": "8 yil tajriba",
        "emoji": "📐"
    },
    {
        "ism": "Rahimova Dilnoza",
        "fan": "Ingliz tili",
        "tajriba": "6 yil tajriba",
        "emoji": "🇬🇧"
    },
    {
        "ism": "Toshmatov Sanjar",
        "fan": "Fizika",
        "tajriba": "5 yil tajriba",
        "emoji": "⚡"
    },
    {
        "ism": "Nazarova Malika",
        "fan": "Kimyo",
        "tajriba": "7 yil tajriba",
        "emoji": "🧪"
    },
]

# Fanlar ro'yxati (darsga yozilish uchun)
FANLAR = ["Matematika", "Ingliz tili", "Fizika", "Kimyo", "Biologiya", "Rus tili"]

# =============================================
# CONVERSATION STATES
# =============================================
ISM, TELEFON_KIRISH, FAN_TANLASH = range(3)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================
# MENYULAR
# =============================================
def bosh_menyu():
    """Bosh menyu tugmalari"""
    tugmalar = [
        [KeyboardButton("👨‍🏫 O'qituvchilar"), KeyboardButton("💳 To'lov ma'lumotlari")],
        [KeyboardButton("📝 Darsga yozilish"), KeyboardButton("📞 Aloqa / Manzil")],
    ]
    return ReplyKeyboardMarkup(tugmalar, resize_keyboard=True)

# =============================================
# HANDLERS
# =============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot ishga tushganda"""
    foydalanuvchi = update.effective_user
    xabar = (
        f"👋 Assalomu alaykum, {foydalanuvchi.first_name}!\n\n"
        f"🏫 <b>{MARKAZ_NOMI}</b> botiga xush kelibsiz!\n\n"
        "Quyidagi bo'limlardan birini tanlang:"
    )
    await update.message.reply_text(
        xabar,
        parse_mode="HTML",
        reply_markup=bosh_menyu()
    )

async def aloqa_manzil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Aloqa va manzil ma'lumotlari"""
    xabar = (
        f"📞 <b>Aloqa va Manzil</b>\n"
        f"{'━' * 25}\n\n"
        f"🏫 <b>{MARKAZ_NOMI}</b>\n\n"
        f"{MANZIL}\n\n"
        f"{TELEFON}\n"
        f"{TELEFON2}\n\n"
        f"{ISH_VAQTI}\n\n"
        f"💬 <i>Savollaringiz bo'lsa, qo'ng'iroq qiling!</i>"
    )
    # Xarita tugmasi
    inline = InlineKeyboardMarkup([
        [InlineKeyboardButton("🗺 Xaritada ko'rish", url="https://maps.google.com/?q=41.2995,69.2401")],
        [InlineKeyboardButton("📲 Telegram kanal", url="https://t.me/babolo_markaz")]
    ])
    await update.message.reply_text(xabar, parse_mode="HTML", reply_markup=inline)

async def tolov_malumotlari(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """To'lov ma'lumotlari"""
    xabar = (
        f"💳 <b>To'lov Ma'lumotlari</b>\n"
        f"{'━' * 25}\n\n"
        f"{KARTA_RAQAM}\n"
        f"{KARTA_EGASI}\n"
        f"{BANK}\n\n"
        f"📌 <b>Eslatma:</b>\n"
        f"• To'lov har oyning 1-5 sanasi\n"
        f"• To'lovdan so'ng chekni adminga yuboring\n"
        f"• Muammo bo'lsa: {TELEFON}"
    )
    inline = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ To'lov qildim - Chek yuborish", url="https://t.me/babolo_admin")]
    ])
    await update.message.reply_text(xabar, parse_mode="HTML", reply_markup=inline)

async def oqituvchilar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'qituvchilar ro'yxati"""
    xabar = f"👨‍🏫 <b>O'qituvchilarimiz</b>\n{'━' * 25}\n\n"
    for i, o in enumerate(OQITUVCHILAR, 1):
        xabar += (
            f"{o['emoji']} <b>{o['ism']}</b>\n"
            f"   📚 Fan: {o['fan']}\n"
            f"   🏆 {o['tajriba']}\n\n"
        )
    xabar += f"📞 Batafsil ma'lumot: {TELEFON}"
    await update.message.reply_text(xabar, parse_mode="HTML")

# =============================================
# DARSGA YOZILISH - ConversationHandler
# =============================================

async def darsga_yozilish_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Darsga yozilishni boshlash"""
    await update.message.reply_text(
        "📝 <b>Darsga yozilish</b>\n"
        f"{'━' * 25}\n\n"
        "Ismingiz va familiyangizni kiriting:\n"
        "<i>(Masalan: Aliyev Jasur)</i>",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardMarkup([["❌ Bekor qilish"]], resize_keyboard=True)
    )
    return ISM

async def ism_olish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ism olish"""
    if update.message.text == "❌ Bekor qilish":
        await update.message.reply_text("❌ Bekor qilindi.", reply_markup=bosh_menyu())
        return ConversationHandler.END

    context.user_data["ism"] = update.message.text
    await update.message.reply_text(
        f"✅ Ism saqlandi: <b>{update.message.text}</b>\n\n"
        "📱 Telefon raqamingizni kiriting:\n"
        "<i>(Masalan: +998901234567)</i>",
        parse_mode="HTML"
    )
    return TELEFON_KIRISH

async def telefon_olish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Telefon olish"""
    if update.message.text == "❌ Bekor qilish":
        await update.message.reply_text("❌ Bekor qilindi.", reply_markup=bosh_menyu())
        return ConversationHandler.END

    context.user_data["telefon"] = update.message.text

    # Fan tanlash tugmalari
    fan_tugmalar = [[KeyboardButton(fan)] for fan in FANLAR]
    fan_tugmalar.append([KeyboardButton("❌ Bekor qilish")])

    await update.message.reply_text(
        "📚 Qaysi fanga yozilmoqchisiz?",
        reply_markup=ReplyKeyboardMarkup(fan_tugmalar, resize_keyboard=True)
    )
    return FAN_TANLASH

async def fan_olish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fan tanlash va yakunlash"""
    if update.message.text == "❌ Bekor qilish":
        await update.message.reply_text("❌ Bekor qilindi.", reply_markup=bosh_menyu())
        return ConversationHandler.END

    fan = update.message.text
    ism = context.user_data.get("ism")
    telefon = context.user_data.get("telefon")

    # Foydalanuvchiga tasdiqlash
    await update.message.reply_text(
        f"✅ <b>Arizangiz qabul qilindi!</b>\n"
        f"{'━' * 25}\n\n"
        f"👤 Ism: <b>{ism}</b>\n"
        f"📱 Telefon: <b>{telefon}</b>\n"
        f"📚 Fan: <b>{fan}</b>\n\n"
        f"⏳ Tez orada administrator siz bilan bog'lanadi.\n"
        f"📞 Savollar uchun: {TELEFON}",
        parse_mode="HTML",
        reply_markup=bosh_menyu()
    )

    # Admin ga xabar yuborish (admin chat ID ni kiriting)
    # ADMIN_CHAT_ID = 123456789  # O'z chat ID ingizni kiriting
    # await context.bot.send_message(
    #     chat_id=ADMIN_CHAT_ID,
    #     text=f"🆕 Yangi ariza!\n👤 {ism}\n📱 {telefon}\n📚 {fan}"
    # )

    return ConversationHandler.END

async def bekor_qilish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Istalgan vaqt bekor qilish"""
    await update.message.reply_text("❌ Bekor qilindi.", reply_markup=bosh_menyu())
    return ConversationHandler.END

async def noaniq_xabar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Noto'g'ri xabar"""
    await update.message.reply_text(
        "❓ Iltimos, quyidagi tugmalardan birini tanlang:",
        reply_markup=bosh_menyu()
    )

# =============================================
# MAIN
# =============================================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Darsga yozilish conversation
    yozilish_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^📝 Darsga yozilish$"), darsga_yozilish_start)],
        states={
            ISM: [MessageHandler(filters.TEXT & ~filters.COMMAND, ism_olish)],
            TELEFON_KIRISH: [MessageHandler(filters.TEXT & ~filters.COMMAND, telefon_olish)],
            FAN_TANLASH: [MessageHandler(filters.TEXT & ~filters.COMMAND, fan_olish)],
        },
        fallbacks=[MessageHandler(filters.Regex("^❌ Bekor qilish$"), bekor_qilish)],
    )

    # Handlerlar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(yozilish_handler)
    app.add_handler(MessageHandler(filters.Regex("^📞 Aloqa / Manzil$"), aloqa_manzil))
    app.add_handler(MessageHandler(filters.Regex("^💳 To'lov ma'lumotlari$"), tolov_malumotlari))
    app.add_handler(MessageHandler(filters.Regex("^👨‍🏫 O'qituvchilar$"), oqituvchilar))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, noaniq_xabar))

    print(f"🤖 {MARKAZ_NOMI} boti ishga tushdi!")
    app.run_polling()

if __name__ == "__main__":
    main()
