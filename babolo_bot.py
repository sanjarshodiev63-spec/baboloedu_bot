#!/usr/bin/env python3
"""
Babolo O'qib Markazi - Telegram Bot (Ko'p tilli versiya)
Tillar: O'zbek, Rus, Ingliz, Tojik
Ishlatish: pip install python-telegram-bot==20.7
"""

import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler, CallbackQueryHandler
)

# =============================================
# BOT TOKEN
# =============================================
BOT_TOKEN = "8918790074:AAEtVRX-VIZ2DNyRkpbTDgd484j1e1mTF9Y"

# =============================================
# O'QUV MARKAZ MA'LUMOTLARI
# =============================================
MARKAZ_NOMI = "Babolo educational center"
MANZIL = "Ғӯлакандоз қишлоғи (маркази) Истиқлол биноси Даврон Самадов кӯчаси"
TELEFON = "+992 94 000 3000"
TELEFON2 = "+998 98 880 0708"
ISH_VAQTI_UZ = "Душ-Шан: 08:00 - 17:00"
ISH_VAQTI_RU = "Пн-Вс: 08:00 - 17:00"
ISH_VAQTI_EN = "Mon-Sun: 08:00 - 17:00"
ISH_VAQTI_TJ = "Душ-Шан: 08:00 - 17:00"
KARTA_RAQAM = "94 300 3000"
KARTA_EGASI = "Абдимуминова Муҳаббат Абдиҷабборовна"
BANK = "Dushanbe City"

# O'qituvchilar
OQITUVCHILAR = [
    {"ism": "Фозилова Мадинахон Одиловна",          "fan_uz": "Инглиз тили", "fan_ru": "Английский", "fan_en": "English", "fan_tj": "Англисӣ", "tajriba": 11, "emoji": "🇬🇧"},
    {"ism": "Самадова Хосият",                       "fan_uz": "Рус тили",    "fan_ru": "Русский",    "fan_en": "Russian", "fan_tj": "Русӣ",    "tajriba": 38, "emoji": "🇷🇺"},
    {"ism": "Шукурова Солиҳаҷон Йулдошовна",         "fan_uz": "Инглиз тили", "fan_ru": "Английский", "fan_en": "English", "fan_tj": "Англисӣ", "tajriba": 19, "emoji": "🇬🇧"},
    {"ism": "Ахмедҷонова Нилуфар Юсуфҷоновна",       "fan_uz": "Рус тили",    "fan_ru": "Русский",    "fan_en": "Russian", "fan_tj": "Русӣ",    "tajriba": 33, "emoji": "🇷🇺"},
    {"ism": "Бойматова Шахноза",                     "fan_uz": "Инглиз тили", "fan_ru": "Английский", "fan_en": "English", "fan_tj": "Англисӣ", "tajriba": 18, "emoji": "🇬🇧"},
    {"ism": "Абдимуминова Муҳаббат Абдиҷабборовна",   "fan_uz": "Администратор","fan_ru": "Администратор","fan_en": "Administrator","fan_tj": "Маъмур", "tajriba": 0, "emoji": "🗂"},
]

FANLAR = {
    "uz": ["Инглиз тили", "Рус тили"],
    "ru": ["Английский", "Русский язык"],
    "en": ["English", "Russian"],
    "tj": ["Англисӣ", "Русӣ"],
}

# =============================================
# CONVERSATION STATES
# =============================================
LANG_SELECT, ISM, TELEFON_KIRISH, FAN_TANLASH = range(4)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================
# TARJIMALAR
# =============================================
TEXTS = {
    # --- TIL TANLASH ---
    "lang_select": {
        "uz": "🌐 Tilni tanlang / Выберите язык / Choose language / Забонро интихоб кунед:",
        "ru": "🌐 Tilni tanlang / Выберите язык / Choose language / Забонро интихоб кунед:",
        "en": "🌐 Tilni tanlang / Выберите язык / Choose language / Забонро интихоб кунед:",
        "tj": "🌐 Tilni tanlang / Выберите язык / Choose language / Забонро интихоб кунед:",
    },
    # --- XUSH KELIBSIZ ---
    "welcome": {
        "uz": "👋 Ассалому алайкум, {name}!\n\n🏫 <b>{markaz}</b> ботига хуш келибсиз!\n\nҚуйидаги бўлимлардан бирини танланг:",
        "ru": "👋 Здравствуйте, {name}!\n\n🏫 Добро пожаловать в бот <b>{markaz}</b>!\n\nВыберите один из разделов:",
        "en": "👋 Hello, {name}!\n\n🏫 Welcome to <b>{markaz}</b> bot!\n\nPlease choose a section:",
        "tj": "👋 Салом, {name}!\n\n🏫 Ба боти <b>{markaz}</b> хуш омадед!\n\nЯке аз бахшҳоро интихоб кунед:",
    },
    # --- MENYU TUGMALARI ---
    "btn_teachers": {
        "uz": "👨‍🏫 Ўқитувчилар",
        "ru": "👨‍🏫 Учителя",
        "en": "👨‍🏫 Teachers",
        "tj": "👨‍🏫 Муаллимон",
    },
    "btn_payment": {
        "uz": "💳 Тўлов маълумотлари",
        "ru": "💳 Данные оплаты",
        "en": "💳 Payment info",
        "tj": "💳 Маълумоти пардохт",
    },
    "btn_register": {
        "uz": "📝 Дарсга ёзилиш",
        "ru": "📝 Записаться на курс",
        "en": "📝 Enroll in course",
        "tj": "📝 Ба дарс навиштан",
    },
    "btn_contact": {
        "uz": "📞 Алоқа / Манзил",
        "ru": "📞 Контакты / Адрес",
        "en": "📞 Contact / Address",
        "tj": "📞 Тамос / Суроға",
    },
    "btn_language": {
        "uz": "🌐 Тилни ўзгартириш",
        "ru": "🌐 Сменить язык",
        "en": "🌐 Change language",
        "tj": "🌐 Иваз кардани забон",
    },
    "btn_cancel": {
        "uz": "❌ Бекор қилиш",
        "ru": "❌ Отмена",
        "en": "❌ Cancel",
        "tj": "❌ Бекор кардан",
    },
    "btn_map": {
        "uz": "🗺 Харитада кўриш",
        "ru": "🗺 Посмотреть на карте",
        "en": "🗺 View on map",
        "tj": "🗺 Дар харита дидан",
    },
    "btn_channel": {
        "uz": "📲 Telegram канал",
        "ru": "📲 Telegram канал",
        "en": "📲 Telegram channel",
        "tj": "📲 Канали Telegram",
    },
    "btn_paid": {
        "uz": "✅ Тўлов қилдим — чек юбориш",
        "ru": "✅ Оплатил — Отправить чек",
        "en": "✅ Paid — Send receipt",
        "tj": "✅ Пардохт кардам — Чек фиристодан",
    },
    # --- ALOQA ---
    "contact_title": {
        "uz": "📞 <b>Алоқа ва Манзил</b>\n{line}\n\n🏫 <b>{markaz}</b>\n\n📍 {manzil}\n\n📞 {tel1}\n📞 {tel2}\n\n🕐 {vaqt}\n\n💬 <i>Саволларингиз бўлса, қўнғироқ қилинг!</i>",
        "ru": "📞 <b>Контакты и Адрес</b>\n{line}\n\n🏫 <b>{markaz}</b>\n\n📍 {manzil}\n\n📞 {tel1}\n📞 {tel2}\n\n🕐 {vaqt}\n\n💬 <i>Если есть вопросы — звоните!</i>",
        "en": "📞 <b>Contact & Address</b>\n{line}\n\n🏫 <b>{markaz}</b>\n\n📍 {manzil}\n\n📞 {tel1}\n📞 {tel2}\n\n🕐 {vaqt}\n\n💬 <i>Call us if you have questions!</i>",
        "tj": "📞 <b>Тамос ва Суроға</b>\n{line}\n\n🏫 <b>{markaz}</b>\n\n📍 {manzil}\n\n📞 {tel1}\n📞 {tel2}\n\n🕐 {vaqt}\n\n💬 <i>Агар саволе дошта бошед, занг занед!</i>",
    },
    # --- TO'LOV ---
    "payment_title": {
        "uz": (
            "💳 <b>Тўлов Маълумотлари</b>\n{line}\n\n"
            "📞 {karta}\n👤 {egasi}\n🏦 {bank}\n\n"
            "📌 <b>Эслатма:</b>\n"
            "• Тўловдан сўнг чекни админга юборинг\n"
            "• Муаммо бўлса: 📞 {tel}"
        ),
        "ru": (
            "💳 <b>Данные Оплаты</b>\n{line}\n\n"
            "📞 {karta}\n👤 {egasi}\n🏦 {bank}\n\n"
            "📌 <b>Примечание:</b>\n"
            "• После оплаты отправьте чек администратору\n"
            "• При проблемах: 📞 {tel}"
        ),
        "en": (
            "💳 <b>Payment Information</b>\n{line}\n\n"
            "📞 {karta}\n👤 {egasi}\n🏦 {bank}\n\n"
            "📌 <b>Note:</b>\n"
            "• Send receipt to admin after payment\n"
            "• For issues: 📞 {tel}"
        ),
        "tj": (
            "💳 <b>Маълумоти Пардохт</b>\n{line}\n\n"
            "📞 {karta}\n👤 {egasi}\n🏦 {bank}\n\n"
            "📌 <b>Эзоҳ:</b>\n"
            "• Пас аз пардохт чекро ба админ фиристед\n"
            "• Дар мушкилот: 📞 {tel}"
        ),
    },
    # --- O'QITUVCHILAR ---
    "teachers_title": {
        "uz": "👨‍🏫 <b>Ўқитувчиларимиз</b>\n{line}\n\n",
        "ru": "👨‍🏫 <b>Наши Учителя</b>\n{line}\n\n",
        "en": "👨‍🏫 <b>Our Teachers</b>\n{line}\n\n",
        "tj": "👨‍🏫 <b>Муаллимони мо</b>\n{line}\n\n",
    },
    "teacher_row": {
        "uz": "{emoji} <b>{ism}</b>\n   📚 Фан: {fan}\n   🏆 {yil} йил тажриба\n\n",
        "ru": "{emoji} <b>{ism}</b>\n   📚 Предмет: {fan}\n   🏆 Опыт: {yil} лет\n\n",
        "en": "{emoji} <b>{ism}</b>\n   📚 Subject: {fan}\n   🏆 Experience: {yil} years\n\n",
        "tj": "{emoji} <b>{ism}</b>\n   📚 Фан: {fan}\n   🏆 Таҷриба: {yil} сол\n\n",
    },
    "teachers_footer": {
        "uz": "📞 Батафсил маълумот: {tel}",
        "ru": "📞 Подробнее: {tel}",
        "en": "📞 More info: {tel}",
        "tj": "📞 Маълумоти бештар: {tel}",
    },
    # --- DARSGA YOZILISH ---
    "enroll_start": {
        "uz": "📝 <b>Дарсга ёзилиш</b>\n{line}\n\nИсмингиз ва фамилиянгизни киритинг:\n<i>(Масалан: Алиев Жасур)</i>",
        "ru": "📝 <b>Запись на курс</b>\n{line}\n\nВведите ваше имя и фамилию:\n<i>(Например: Алиев Жасур)</i>",
        "en": "📝 <b>Course Enrollment</b>\n{line}\n\nEnter your first and last name:\n<i>(Example: Aliyev Jasur)</i>",
        "tj": "📝 <b>Ба дарс навиштан</b>\n{line}\n\nНоми ва насаби худро ворид кунед:\n<i>(Масалан: Алиев Ҷасур)</i>",
    },
    "enroll_phone": {
        "uz": "✅ Исм сақланди: <b>{ism}</b>\n\n📱 Телефон рақамингизни киритинг:\n<i>(Масалан: +992781658989)</i>",
        "ru": "✅ Имя сохранено: <b>{ism}</b>\n\n📱 Введите ваш номер телефона:\n<i>(Например: +992781658989)</i>",
        "en": "✅ Name saved: <b>{ism}</b>\n\n📱 Enter your phone number:\n<i>(Example: +992781658989)</i>",
        "tj": "✅ Ном сабт шуд: <b>{ism}</b>\n\n📱 Рақами телефони худро ворид кунед:\n<i>(Масалан: +992781658989)</i>",
    },
    "enroll_subject": {
        "uz": "📚 Қайси фанга ёзилмоқчисиз?",
        "ru": "📚 На какой предмет хотите записаться?",
        "en": "📚 Which subject would you like to enroll in?",
        "tj": "📚 Ба кадом фан навиштан мехоҳед?",
    },
    "enroll_done": {
        "uz": "✅ <b>Аризангиз қабул қилинди!</b>\n{line}\n\n👤 Исм: <b>{ism}</b>\n📱 Телефон: <b>{tel}</b>\n📚 Фан: <b>{fan}</b>\n\n⏳ Тез орада администратор сиз билан боғланади.\n📞 Саволлар учун: {markaz_tel}",
        "ru": "✅ <b>Ваша заявка принята!</b>\n{line}\n\n👤 Имя: <b>{ism}</b>\n📱 Телефон: <b>{tel}</b>\n📚 Предмет: <b>{fan}</b>\n\n⏳ Администратор свяжется с вами в ближайшее время.\n📞 Вопросы: {markaz_tel}",
        "en": "✅ <b>Your application is accepted!</b>\n{line}\n\n👤 Name: <b>{ism}</b>\n📱 Phone: <b>{tel}</b>\n📚 Subject: <b>{fan}</b>\n\n⏳ An administrator will contact you shortly.\n📞 Questions: {markaz_tel}",
        "tj": "✅ <b>Аризаи шумо қабул шуд!</b>\n{line}\n\n👤 Ном: <b>{ism}</b>\n📱 Телефон: <b>{tel}</b>\n📚 Фан: <b>{fan}</b>\n\n⏳ Администратор ба зудӣ бо шумо тамос мегирад.\n📞 Савол: {markaz_tel}",
    },
    "cancelled": {
        "uz": "❌ Бекор қилинди.",
        "ru": "❌ Отменено.",
        "en": "❌ Cancelled.",
        "tj": "❌ Бекор карда шуд.",
    },
    "unknown": {
        "uz": "❓ Илтимос, қуйидаги тугмалардан бирини танланг:",
        "ru": "❓ Пожалуйста, выберите одну из кнопок ниже:",
        "en": "❓ Please choose one of the buttons below:",
        "tj": "❓ Лутфан яке аз тугмаҳои зеринро интихоб кунед:",
    },
}

LINE = "━" * 25

ISH_VAQTLAR = {
    "uz": ISH_VAQTI_UZ,
    "ru": ISH_VAQTI_RU,
    "en": ISH_VAQTI_EN,
    "tj": ISH_VAQTI_TJ,
}

FAN_KEYS = {
    "uz": "fan_uz",
    "ru": "fan_ru",
    "en": "fan_en",
    "tj": "fan_tj",
}

# =============================================
# YORDAMCHI FUNKSIYALAR
# =============================================

def get_lang(context: ContextTypes.DEFAULT_TYPE) -> str:
    return context.user_data.get("lang", "uz")

def t(key: str, lang: str, **kwargs) -> str:
    template = TEXTS[key][lang]
    kwargs["line"] = LINE
    try:
        return template.format(**kwargs)
    except Exception:
        return template

def bosh_menyu(lang: str):
    tugmalar = [
        [KeyboardButton(t("btn_teachers", lang)), KeyboardButton(t("btn_payment", lang))],
        [KeyboardButton(t("btn_register", lang)), KeyboardButton(t("btn_contact", lang))],
        [KeyboardButton(t("btn_language", lang))],
    ]
    return ReplyKeyboardMarkup(tugmalar, resize_keyboard=True)

def til_tanlash_menyu():
    tugmalar = [
        [KeyboardButton("🇺🇿 O'zbek"), KeyboardButton("🇷🇺 Русский")],
        [KeyboardButton("🇬🇧 English"), KeyboardButton("🇹🇯 Тоҷикӣ")],
    ]
    return ReplyKeyboardMarkup(tugmalar, resize_keyboard=True, one_time_keyboard=True)

LANG_MAP = {
    "🇺🇿 O'zbek":  "uz",
    "🇷🇺 Русский": "ru",
    "🇬🇧 English": "en",
    "🇹🇯 Тоҷикӣ": "tj",
}

# =============================================
# HANDLERS
# =============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌐 Tilni tanlang / Выберите язык / Choose language / Забонро интихоб кунед:",
        reply_markup=til_tanlash_menyu()
    )
    return LANG_SELECT

async def til_tanlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matn = update.message.text
    lang = LANG_MAP.get(matn)
    if not lang:
        await update.message.reply_text(
            "🌐 Tilni tanlang / Выберите язык / Choose language / Забонро интихоб кунед:",
            reply_markup=til_tanlash_menyu()
        )
        return LANG_SELECT
    context.user_data["lang"] = lang
    foydalanuvchi = update.effective_user
    await update.message.reply_text(
        t("welcome", lang, name=foydalanuvchi.first_name, markaz=MARKAZ_NOMI),
        parse_mode="HTML",
        reply_markup=bosh_menyu(lang)
    )
    return ConversationHandler.END

async def til_ozgartirish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌐 Tilni tanlang / Выберите язык / Choose language / Забонро интихоб кунед:",
        reply_markup=til_tanlash_menyu()
    )
    return LANG_SELECT

async def aloqa_manzil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    xabar = t("contact_title", lang,
              markaz=MARKAZ_NOMI,
              manzil=MANZIL,
              tel1=TELEFON,
              tel2=TELEFON2,
              vaqt=ISH_VAQTLAR[lang])
    inline = InlineKeyboardMarkup([
        [InlineKeyboardButton(t("btn_map", lang), url="https://maps.app.goo.gl/DAnAwNHjUMv82eGn9")],
        [InlineKeyboardButton(t("btn_channel", lang), url="https://t.me/+YlLgTaf9MIwyYmE6")],
        [InlineKeyboardButton("💬 WhatsApp", url="https://chat.whatsapp.com/FedvR6riKUh5UQCujxzSLB")]
    ])
    await update.message.reply_text(xabar, parse_mode="HTML", reply_markup=inline)

async def tolov_malumotlari(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    xabar = t("payment_title", lang,
              karta=KARTA_RAQAM,
              egasi=KARTA_EGASI,
              bank=BANK,
              tel=TELEFON)
    inline = InlineKeyboardMarkup([
        [InlineKeyboardButton(t("btn_paid", lang), url="https://t.me/@baboloeducation")]
    ])
    await update.message.reply_text(xabar, parse_mode="HTML", reply_markup=inline)

async def oqituvchilar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    fan_key = FAN_KEYS[lang]
    xabar = t("teachers_title", lang)
    for o in OQITUVCHILAR:
        xabar += t("teacher_row", lang,
                   emoji=o["emoji"],
                   ism=o["ism"],
                   fan=o[fan_key],
                   yil=o["tajriba"])
    xabar += t("teachers_footer", lang, tel=TELEFON)
    await update.message.reply_text(xabar, parse_mode="HTML")

async def noaniq_xabar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    await update.message.reply_text(t("unknown", lang), reply_markup=bosh_menyu(lang))

# =============================================
# DARSGA YOZILISH - ConversationHandler
# =============================================

async def darsga_yozilish_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    await update.message.reply_text(
        t("enroll_start", lang),
        parse_mode="HTML",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton(t("btn_cancel", lang))]], resize_keyboard=True
        )
    )
    return ISM

async def ism_olish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    if update.message.text == t("btn_cancel", lang):
        await update.message.reply_text(t("cancelled", lang), reply_markup=bosh_menyu(lang))
        return ConversationHandler.END
    context.user_data["ism"] = update.message.text
    await update.message.reply_text(
        t("enroll_phone", lang, ism=update.message.text),
        parse_mode="HTML"
    )
    return TELEFON_KIRISH

async def telefon_olish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    if update.message.text == t("btn_cancel", lang):
        await update.message.reply_text(t("cancelled", lang), reply_markup=bosh_menyu(lang))
        return ConversationHandler.END
    context.user_data["telefon"] = update.message.text
    fan_list = FANLAR[lang]
    fan_tugmalar = [[KeyboardButton(fan)] for fan in fan_list]
    fan_tugmalar.append([KeyboardButton(t("btn_cancel", lang))])
    await update.message.reply_text(
        t("enroll_subject", lang),
        reply_markup=ReplyKeyboardMarkup(fan_tugmalar, resize_keyboard=True)
    )
    return FAN_TANLASH

async def fan_olish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    if update.message.text == t("btn_cancel", lang):
        await update.message.reply_text(t("cancelled", lang), reply_markup=bosh_menyu(lang))
        return ConversationHandler.END
    fan = update.message.text
    ism = context.user_data.get("ism")
    telefon = context.user_data.get("telefon")
    await update.message.reply_text(
        t("enroll_done", lang, ism=ism, tel=telefon, fan=fan, markaz_tel=TELEFON),
        parse_mode="HTML",
        reply_markup=bosh_menyu(lang)
    )
    # Admin ga xabar yuborish
    ADMIN_CHAT_ID = 7821601256
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"🆕 Yangi ariza!\n👤 {ism}\n📱 {telefon}\n📚 {fan}")
    return ConversationHandler.END

async def bekor_qilish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    await update.message.reply_text(t("cancelled", lang), reply_markup=bosh_menyu(lang))
    return ConversationHandler.END

# =============================================
# MAIN
# =============================================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    til_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(filters.Regex("^🌐"), til_ozgartirish),
        ],
        states={
            LANG_SELECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, til_tanlash)],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    yozilish_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex("^📝"), darsga_yozilish_start)
        ],
        states={
            ISM:            [MessageHandler(filters.TEXT & ~filters.COMMAND, ism_olish)],
            TELEFON_KIRISH: [MessageHandler(filters.TEXT & ~filters.COMMAND, telefon_olish)],
            FAN_TANLASH:    [MessageHandler(filters.TEXT & ~filters.COMMAND, fan_olish)],
        },
        fallbacks=[MessageHandler(filters.Regex("^❌"), bekor_qilish)],
    )

    app.add_handler(til_handler)
    app.add_handler(yozilish_handler)
    app.add_handler(MessageHandler(filters.Regex("^👨‍🏫"), oqituvchilar))
    app.add_handler(MessageHandler(filters.Regex("^💳"), tolov_malumotlari))
    app.add_handler(MessageHandler(filters.Regex("^📞"), aloqa_manzil))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, noaniq_xabar))
#!/usr/bin/env python3
"""
Babolo O'qib Markazi - Telegram Bot (Ko'p tilli versiya)
Tillar: O'zbek, Rus, Ingliz, Tojik
Ishlatish: pip install python-telegram-bot==20.7
"""

import logging
import json
import os
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler, CallbackQueryHandler
)

# =============================================
# BOT TOKEN
# =============================================
BOT_TOKEN = "8918790074:AAEtVRX-VIZ2DNyRkpbTDgd484j1e1mTF9Y"

# =============================================
# O'QUV MARKAZ MA'LUMOTLARI
# =============================================
MARKAZ_NOMI = "Babolo educational center"
MANZIL = "Ғӯлакандоз қишлоғи (маркази) Истиқлол биноси Даврон Самадов кӯчаси"
TELEFON = "+992 94 000 3000"
TELEFON2 = "+998 98 880 0708"
ISH_VAQTI_UZ = "Душ-Шан: 08:00 - 17:00"
ISH_VAQTI_RU = "Пн-Вс: 08:00 - 17:00"
ISH_VAQTI_EN = "Mon-Sun: 08:00 - 17:00"
ISH_VAQTI_TJ = "Душ-Шан: 08:00 - 17:00"
KARTA_RAQAM = "94 300 3000"
KARTA_EGASI = "Абдимуминова Муҳаббат Абдиҷабборовна"
BANK = "Dushanbe City"

# O'qituvchilar
OQITUVCHILAR = [
    {"ism": "Фозилова Мадинахон Одиловна",          "fan_uz": "Инглиз тили", "fan_ru": "Английский", "fan_en": "English", "fan_tj": "Англисӣ", "tajriba": 11, "emoji": "🇬🇧"},
    {"ism": "Самадова Хосият",                       "fan_uz": "Рус тили",    "fan_ru": "Русский",    "fan_en": "Russian", "fan_tj": "Русӣ",    "tajriba": 38, "emoji": "🇷🇺"},
    {"ism": "Шукурова Солиҳаҷон Йулдошовна",         "fan_uz": "Инглиз тили", "fan_ru": "Английский", "fan_en": "English", "fan_tj": "Англисӣ", "tajriba": 19, "emoji": "🇬🇧"},
    {"ism": "Ахмедҷонова Нилуфар Юсуфҷоновна",       "fan_uz": "Рус тили",    "fan_ru": "Русский",    "fan_en": "Russian", "fan_tj": "Русӣ",    "tajriba": 33, "emoji": "🇷🇺"},
    {"ism": "Бойматова Шахноза",                     "fan_uz": "Инглиз тили", "fan_ru": "Английский", "fan_en": "English", "fan_tj": "Англисӣ", "tajriba": 18, "emoji": "🇬🇧"},
    {"ism": "Абдимуминова Муҳаббат Абдиҷабборовна",   "fan_uz": "Администратор","fan_ru": "Администратор","fan_en": "Administrator","fan_tj": "Маъмур", "tajriba": 0, "emoji": "🗂"},
]

FANLAR = {
    "uz": ["Инглиз тили", "Рус тили"],
    "ru": ["Английский", "Русский язык"],
    "en": ["English", "Russian"],
    "tj": ["Англисӣ", "Русӣ"],
}

# =============================================
# ADMIN VA ELONLAR SOZLAMASI
# =============================================
ADMIN_CHAT_ID = 7821601256          # Admin Telegram ID
ELONLAR_FAYL = "elonlar.json"       # Elonlar saqlanadigan fayl

def elonlar_yuklash() -> list:
    """JSON fayldan elonlarni o'qish"""
    if not os.path.exists(ELONLAR_FAYL):
        return []
    try:
        with open(ELONLAR_FAYL, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def elonlar_saqlash(elonlar: list):
    """Elonlarni JSON faylga yozish"""
    with open(ELONLAR_FAYL, "w", encoding="utf-8") as f:
        json.dump(elonlar, f, ensure_ascii=False, indent=2)

# =============================================
# CONVERSATION STATES
# =============================================
LANG_SELECT, ISM, TELEFON_KIRISH, FAN_TANLASH, ELON_MATN = range(5)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================
# TARJIMALAR
# =============================================
TEXTS = {
    # --- TIL TANLASH ---
    "lang_select": {
        "uz": "🌐 Tilni tanlang / Выберите язык / Choose language / Забонро интихоб кунед:",
        "ru": "🌐 Tilni tanlang / Выберите язык / Choose language / Забонро интихоб кунед:",
        "en": "🌐 Tilni tanlang / Выберите язык / Choose language / Забонро интихоб кунед:",
        "tj": "🌐 Tilni tanlang / Выберите язык / Choose language / Забонро интихоб кунед:",
    },
    # --- XUSH KELIBSIZ ---
    "welcome": {
        "uz": "👋 Ассалому алайкум, {name}!\n\n🏫 <b>{markaz}</b> ботига хуш келибсиз!\n\nҚуйидаги бўлимлардан бирини танланг:",
        "ru": "👋 Здравствуйте, {name}!\n\n🏫 Добро пожаловать в бот <b>{markaz}</b>!\n\nВыберите один из разделов:",
        "en": "👋 Hello, {name}!\n\n🏫 Welcome to <b>{markaz}</b> bot!\n\nPlease choose a section:",
        "tj": "👋 Салом, {name}!\n\n🏫 Ба боти <b>{markaz}</b> хуш омадед!\n\nЯке аз бахшҳоро интихоб кунед:",
    },
    # --- MENYU TUGMALARI ---
    "btn_teachers": {
        "uz": "👨‍🏫 Ўқитувчилар",
        "ru": "👨‍🏫 Учителя",
        "en": "👨‍🏫 Teachers",
        "tj": "👨‍🏫 Муаллимон",
    },
    "btn_payment": {
        "uz": "💳 Тўлов маълумотлари",
        "ru": "💳 Данные оплаты",
        "en": "💳 Payment info",
        "tj": "💳 Маълумоти пардохт",
    },
    "btn_register": {
        "uz": "📝 Дарсга ёзилиш",
        "ru": "📝 Записаться на курс",
        "en": "📝 Enroll in course",
        "tj": "📝 Ба дарс навиштан",
    },
    "btn_contact": {
        "uz": "📞 Алоқа / Манзил",
        "ru": "📞 Контакты / Адрес",
        "en": "📞 Contact / Address",
        "tj": "📞 Тамос / Суроға",
    },
    "btn_language": {
        "uz": "🌐 Тилни ўзгартириш",
        "ru": "🌐 Сменить язык",
        "en": "🌐 Change language",
        "tj": "🌐 Иваз кардани забон",
    },
    "btn_elonlar": {
        "uz": "📣 Elonlar",
        "ru": "📣 Объявления",
        "en": "📣 Announcements",
        "tj": "📣 Эълонҳо",
    },
    "btn_cancel": {
        "uz": "❌ Бекор қилиш",
        "ru": "❌ Отмена",
        "en": "❌ Cancel",
        "tj": "❌ Бекор кардан",
    },
    "btn_map": {
        "uz": "🗺 Харитада кўриш",
        "ru": "🗺 Посмотреть на карте",
        "en": "🗺 View on map",
        "tj": "🗺 Дар харита дидан",
    },
    "btn_channel": {
        "uz": "📲 Telegram канал",
        "ru": "📲 Telegram канал",
        "en": "📲 Telegram channel",
        "tj": "📲 Канали Telegram",
    },
    "btn_paid": {
        "uz": "✅ Тўлов қилдим — чек юбориш",
        "ru": "✅ Оплатил — Отправить чек",
        "en": "✅ Paid — Send receipt",
        "tj": "✅ Пардохт кардам — Чек фиристодан",
    },
    # --- ALOQA ---
    "contact_title": {
        "uz": "📞 <b>Алоқа ва Манзил</b>\n{line}\n\n🏫 <b>{markaz}</b>\n\n📍 {manzil}\n\n📞 {tel1}\n📞 {tel2}\n\n🕐 {vaqt}\n\n💬 <i>Саволларингиз бўлса, қўнғироқ қилинг!</i>",
        "ru": "📞 <b>Контакты и Адрес</b>\n{line}\n\n🏫 <b>{markaz}</b>\n\n📍 {manzil}\n\n📞 {tel1}\n📞 {tel2}\n\n🕐 {vaqt}\n\n💬 <i>Если есть вопросы — звоните!</i>",
        "en": "📞 <b>Contact & Address</b>\n{line}\n\n🏫 <b>{markaz}</b>\n\n📍 {manzil}\n\n📞 {tel1}\n📞 {tel2}\n\n🕐 {vaqt}\n\n💬 <i>Call us if you have questions!</i>",
        "tj": "📞 <b>Тамос ва Суроға</b>\n{line}\n\n🏫 <b>{markaz}</b>\n\n📍 {manzil}\n\n📞 {tel1}\n📞 {tel2}\n\n🕐 {vaqt}\n\n💬 <i>Агар саволе дошта бошед, занг занед!</i>",
    },
    # --- TO'LOV ---
    "payment_title": {
        "uz": (
            "💳 <b>Тўлов Маълумотлари</b>\n{line}\n\n"
            "📞 {karta}\n👤 {egasi}\n🏦 {bank}\n\n"
            "📌 <b>Эслатма:</b>\n"
            "• Тўловдан сўнг чекни админга юборинг\n"
            "• Муаммо бўлса: 📞 {tel}"
        ),
        "ru": (
            "💳 <b>Данные Оплаты</b>\n{line}\n\n"
            "📞 {karta}\n👤 {egasi}\n🏦 {bank}\n\n"
            "📌 <b>Примечание:</b>\n"
            "• После оплаты отправьте чек администратору\n"
            "• При проблемах: 📞 {tel}"
        ),
        "en": (
            "💳 <b>Payment Information</b>\n{line}\n\n"
            "📞 {karta}\n👤 {egasi}\n🏦 {bank}\n\n"
            "📌 <b>Note:</b>\n"
            "• Send receipt to admin after payment\n"
            "• For issues: 📞 {tel}"
        ),
        "tj": (
            "💳 <b>Маълумоти Пардохт</b>\n{line}\n\n"
            "📞 {karta}\n👤 {egasi}\n🏦 {bank}\n\n"
            "📌 <b>Эзоҳ:</b>\n"
            "• Пас аз пардохт чекро ба админ фиристед\n"
            "• Дар мушкилот: 📞 {tel}"
        ),
    },
    # --- O'QITUVCHILAR ---
    "teachers_title": {
        "uz": "👨‍🏫 <b>Ўқитувчиларимиз</b>\n{line}\n\n",
        "ru": "👨‍🏫 <b>Наши Учителя</b>\n{line}\n\n",
        "en": "👨‍🏫 <b>Our Teachers</b>\n{line}\n\n",
        "tj": "👨‍🏫 <b>Муаллимони мо</b>\n{line}\n\n",
    },
    "teacher_row": {
        "uz": "{emoji} <b>{ism}</b>\n   📚 Фан: {fan}\n   🏆 {yil} йил тажриба\n\n",
        "ru": "{emoji} <b>{ism}</b>\n   📚 Предмет: {fan}\n   🏆 Опыт: {yil} лет\n\n",
        "en": "{emoji} <b>{ism}</b>\n   📚 Subject: {fan}\n   🏆 Experience: {yil} years\n\n",
        "tj": "{emoji} <b>{ism}</b>\n   📚 Фан: {fan}\n   🏆 Таҷриба: {yil} сол\n\n",
    },
    "teachers_footer": {
        "uz": "📞 Батафсил маълумот: {tel}",
        "ru": "📞 Подробнее: {tel}",
        "en": "📞 More info: {tel}",
        "tj": "📞 Маълумоти бештар: {tel}",
    },
    # --- DARSGA YOZILISH ---
    "enroll_start": {
        "uz": "📝 <b>Дарсга ёзилиш</b>\n{line}\n\nИсмингиз ва фамилиянгизни киритинг:\n<i>(Масалан: Алиев Жасур)</i>",
        "ru": "📝 <b>Запись на курс</b>\n{line}\n\nВведите ваше имя и фамилию:\n<i>(Например: Алиев Жасур)</i>",
        "en": "📝 <b>Course Enrollment</b>\n{line}\n\nEnter your first and last name:\n<i>(Example: Aliyev Jasur)</i>",
        "tj": "📝 <b>Ба дарс навиштан</b>\n{line}\n\nНоми ва насаби худро ворид кунед:\n<i>(Масалан: Алиев Ҷасур)</i>",
    },
    "enroll_phone": {
        "uz": "✅ Исм сақланди: <b>{ism}</b>\n\n📱 Телефон рақамингизни киритинг:\n<i>(Масалан: +992781658989)</i>",
        "ru": "✅ Имя сохранено: <b>{ism}</b>\n\n📱 Введите ваш номер телефона:\n<i>(Например: +992781658989)</i>",
        "en": "✅ Name saved: <b>{ism}</b>\n\n📱 Enter your phone number:\n<i>(Example: +992781658989)</i>",
        "tj": "✅ Ном сабт шуд: <b>{ism}</b>\n\n📱 Рақами телефони худро ворид кунед:\n<i>(Масалан: +992781658989)</i>",
    },
    "enroll_subject": {
        "uz": "📚 Қайси фанга ёзилмоқчисиз?",
        "ru": "📚 На какой предмет хотите записаться?",
        "en": "📚 Which subject would you like to enroll in?",
        "tj": "📚 Ба кадом фан навиштан мехоҳед?",
    },
    "enroll_done": {
        "uz": "✅ <b>Аризангиз қабул қилинди!</b>\n{line}\n\n👤 Исм: <b>{ism}</b>\n📱 Телефон: <b>{tel}</b>\n📚 Фан: <b>{fan}</b>\n\n⏳ Тез орада администратор сиз билан боғланади.\n📞 Саволлар учун: {markaz_tel}",
        "ru": "✅ <b>Ваша заявка принята!</b>\n{line}\n\n👤 Имя: <b>{ism}</b>\n📱 Телефон: <b>{tel}</b>\n📚 Предмет: <b>{fan}</b>\n\n⏳ Администратор свяжется с вами в ближайшее время.\n📞 Вопросы: {markaz_tel}",
        "en": "✅ <b>Your application is accepted!</b>\n{line}\n\n👤 Name: <b>{ism}</b>\n📱 Phone: <b>{tel}</b>\n📚 Subject: <b>{fan}</b>\n\n⏳ An administrator will contact you shortly.\n📞 Questions: {markaz_tel}",
        "tj": "✅ <b>Аризаи шумо қабул шуд!</b>\n{line}\n\n👤 Ном: <b>{ism}</b>\n📱 Телефон: <b>{tel}</b>\n📚 Фан: <b>{fan}</b>\n\n⏳ Администратор ба зудӣ бо шумо тамос мегирад.\n📞 Савол: {markaz_tel}",
    },
    "cancelled": {
        "uz": "❌ Бекор қилинди.",
        "ru": "❌ Отменено.",
        "en": "❌ Cancelled.",
        "tj": "❌ Бекор карда шуд.",
    },
    "elonlar_title": {
        "uz": "📣 <b>Elonlar</b>\n{line}\n\n",
        "ru": "📣 <b>Объявления</b>\n{line}\n\n",
        "en": "📣 <b>Announcements</b>\n{line}\n\n",
        "tj": "📣 <b>Эълонҳо</b>\n{line}\n\n",
    },
    "elonlar_empty": {
        "uz": "📭 Hozircha elon mavjud emas.",
        "ru": "📭 Пока нет объявлений.",
        "en": "📭 No announcements at the moment.",
        "tj": "📭 Айни ҳол эълоне вуҷуд надорад.",
    },
    "elon_sana": {
        "uz": "📅 <i>{sana}</i>\n",
        "ru": "📅 <i>{sana}</i>\n",
        "en": "📅 <i>{sana}</i>\n",
        "tj": "📅 <i>{sana}</i>\n",
    },
    # --- ADMIN PANEL ---
    "admin_help": {
        "uz": (
            "🔧 <b>Admin panel</b>\n━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "📣 <b>Elon qo'shish:</b>\n"
            "  /elon_qosh — yangi elon yozish\n\n"
            "🗑 <b>Elon o'chirish:</b>\n"
            "  /elon_uch — elon raqami bo'yicha o'chirish\n\n"
            "📋 <b>Barcha elonlar:</b>\n"
            "  /elon_list — elonlar ro'yxati (raqamlari bilan)\n\n"
            "💡 <i>Elon qo'shganda faqat matn yozing — sana avtomatik qo'shiladi.</i>"
        ),
        "ru": (
            "🔧 <b>Панель администратора</b>\n━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "📣 <b>Добавить объявление:</b>\n"
            "  /elon_qosh — написать новое объявление\n\n"
            "🗑 <b>Удалить объявление:</b>\n"
            "  /elon_uch — удалить по номеру\n\n"
            "📋 <b>Все объявления:</b>\n"
            "  /elon_list — список объявлений с номерами\n\n"
            "💡 <i>При добавлении просто напишите текст — дата добавляется автоматически.</i>"
        ),
        "en": (
            "🔧 <b>Admin Panel</b>\n━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "📣 <b>Add announcement:</b>\n"
            "  /elon_qosh — write a new announcement\n\n"
            "🗑 <b>Delete announcement:</b>\n"
            "  /elon_uch — delete by number\n\n"
            "📋 <b>All announcements:</b>\n"
            "  /elon_list — list announcements with numbers\n\n"
            "💡 <i>Just write the text — date is added automatically.</i>"
        ),
        "tj": (
            "🔧 <b>Панели маъмур</b>\n━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "📣 <b>Илова кардани эълон:</b>\n"
            "  /elon_qosh — эълони нав навиштан\n\n"
            "🗑 <b>Нест кардани эълон:</b>\n"
            "  /elon_uch — тавассути рақам нест кардан\n\n"
            "📋 <b>Ҳамаи эълонҳо:</b>\n"
            "  /elon_list — рӯйхати эълонҳо бо рақамҳо\n\n"
            "💡 <i>Танҳо матн нависед — сана худкор илова мешавад.</i>"
        ),
    },
    "unknown": {
        "uz": "❓ Илтимос, қуйидаги тугмалардан бирини танланг:",
        "ru": "❓ Пожалуйста, выберите одну из кнопок ниже:",
        "en": "❓ Please choose one of the buttons below:",
        "tj": "❓ Лутфан яке аз тугмаҳои зеринро интихоб кунед:",
    },
}

LINE = "━" * 25

ISH_VAQTLAR = {
    "uz": ISH_VAQTI_UZ,
    "ru": ISH_VAQTI_RU,
    "en": ISH_VAQTI_EN,
    "tj": ISH_VAQTI_TJ,
}

FAN_KEYS = {
    "uz": "fan_uz",
    "ru": "fan_ru",
    "en": "fan_en",
    "tj": "fan_tj",
}

# =============================================
# YORDAMCHI FUNKSIYALAR
# =============================================

def get_lang(context: ContextTypes.DEFAULT_TYPE) -> str:
    return context.user_data.get("lang", "uz")

def t(key: str, lang: str, **kwargs) -> str:
    template = TEXTS[key][lang]
    kwargs["line"] = LINE
    try:
        return template.format(**kwargs)
    except Exception:
        return template

def bosh_menyu(lang: str):
    tugmalar = [
        [KeyboardButton(t("btn_teachers", lang)), KeyboardButton(t("btn_payment", lang))],
        [KeyboardButton(t("btn_register", lang)), KeyboardButton(t("btn_contact", lang))],
        [KeyboardButton(t("btn_elonlar", lang)), KeyboardButton(t("btn_language", lang))],
    ]
    return ReplyKeyboardMarkup(tugmalar, resize_keyboard=True)

def til_tanlash_menyu():
    tugmalar = [
        [KeyboardButton("🇺🇿 O'zbek"), KeyboardButton("🇷🇺 Русский")],
        [KeyboardButton("🇬🇧 English"), KeyboardButton("🇹🇯 Тоҷикӣ")],
    ]
    return ReplyKeyboardMarkup(tugmalar, resize_keyboard=True, one_time_keyboard=True)

LANG_MAP = {
    "🇺🇿 O'zbek":  "uz",
    "🇷🇺 Русский": "ru",
    "🇬🇧 English": "en",
    "🇹🇯 Тоҷикӣ": "tj",
}

# =============================================
# HANDLERS
# =============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌐 Tilni tanlang / Выберите язык / Choose language / Забонро интихоб кунед:",
        reply_markup=til_tanlash_menyu()
    )
    return LANG_SELECT

async def til_tanlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matn = update.message.text
    lang = LANG_MAP.get(matn)
    if not lang:
        await update.message.reply_text(
            "🌐 Tilni tanlang / Выберите язык / Choose language / Забонро интихоб кунед:",
            reply_markup=til_tanlash_menyu()
        )
        return LANG_SELECT
    context.user_data["lang"] = lang
    foydalanuvchi = update.effective_user
    await update.message.reply_text(
        t("welcome", lang, name=foydalanuvchi.first_name, markaz=MARKAZ_NOMI),
        parse_mode="HTML",
        reply_markup=bosh_menyu(lang)
    )
    return ConversationHandler.END

async def til_ozgartirish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌐 Tilni tanlang / Выберите язык / Choose language / Забонро интихоб кунед:",
        reply_markup=til_tanlash_menyu()
    )
    return LANG_SELECT

async def aloqa_manzil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    xabar = t("contact_title", lang,
              markaz=MARKAZ_NOMI,
              manzil=MANZIL,
              tel1=TELEFON,
              tel2=TELEFON2,
              vaqt=ISH_VAQTLAR[lang])
    inline = InlineKeyboardMarkup([
        [InlineKeyboardButton(t("btn_map", lang), url="https://maps.app.goo.gl/DAnAwNHjUMv82eGn9")],
        [InlineKeyboardButton(t("btn_channel", lang), url="https://t.me/+YlLgTaf9MIwyYmE6")],
        [InlineKeyboardButton("💬 WhatsApp", url="https://chat.whatsapp.com/FedvR6riKUh5UQCujxzSLB")]
    ])
    await update.message.reply_text(xabar, parse_mode="HTML", reply_markup=inline)

async def tolov_malumotlari(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    xabar = t("payment_title", lang,
              karta=KARTA_RAQAM,
              egasi=KARTA_EGASI,
              bank=BANK,
              tel=TELEFON)
    inline = InlineKeyboardMarkup([
        [InlineKeyboardButton(t("btn_paid", lang), url="https://t.me/@baboloeducation")]
    ])
    await update.message.reply_text(xabar, parse_mode="HTML", reply_markup=inline)

async def oqituvchilar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    fan_key = FAN_KEYS[lang]
    xabar = t("teachers_title", lang)
    for o in OQITUVCHILAR:
        xabar += t("teacher_row", lang,
                   emoji=o["emoji"],
                   ism=o["ism"],
                   fan=o[fan_key],
                   yil=o["tajriba"])
    xabar += t("teachers_footer", lang, tel=TELEFON)
    await update.message.reply_text(xabar, parse_mode="HTML")

async def noaniq_xabar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    await update.message.reply_text(t("unknown", lang), reply_markup=bosh_menyu(lang))

async def elonlar_korsatish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    elonlar = elonlar_yuklash()
    if not elonlar:
        await update.message.reply_text(t("elonlar_empty", lang), reply_markup=bosh_menyu(lang))
        return
    xabar = t("elonlar_title", lang)
    for i, elon in enumerate(elonlar, 1):
        sana = elon.get("sana", "")
        matn = elon.get("matn", "")
        xabar += f"{i}. 📅 <i>{sana}</i>\n{matn}\n\n"
    await update.message.reply_text(xabar, parse_mode="HTML", reply_markup=bosh_menyu(lang))

# =============================================
# ADMIN: ELON BOSHQARUVI
# =============================================

def is_admin(update: Update) -> bool:
    return update.effective_user.id == ADMIN_CHAT_ID

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return
    lang = get_lang(context)
    await update.message.reply_text(t("admin_help", lang), parse_mode="HTML")

async def elon_qosh_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return
    await update.message.reply_text(
        "📝 <b>Yangi elon matnini yozing:</b>\n\n"
        "<i>Faqat matnni yozing — sana avtomatik qo'shiladi.\n"
        "Bekor qilish uchun: /bekor</i>",
        parse_mode="HTML"
    )
    return ELON_MATN

async def elon_matn_olish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return ConversationHandler.END
    matn = update.message.text
    sana = datetime.now().strftime("%d.%m.%Y %H:%M")
    elon = {"matn": matn, "sana": sana}
    elonlar = elonlar_yuklash()
    elonlar.append(elon)
    elonlar_saqlash(elonlar)
    await update.message.reply_text(
        f"✅ <b>Elon qo'shildi!</b>\n\n"
        f"📅 {sana}\n{matn}\n\n"
        f"📋 Jami elonlar: <b>{len(elonlar)} ta</b>",
        parse_mode="HTML"
    )
    return ConversationHandler.END

async def elon_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return
    elonlar = elonlar_yuklash()
    if not elonlar:
        await update.message.reply_text("📭 Hozircha elon yo'q.")
        return
    xabar = f"📋 <b>Barcha elonlar ({len(elonlar)} ta):</b>\n━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    for i, elon in enumerate(elonlar, 1):
        xabar += f"<b>#{i}</b> | 📅 {elon.get('sana','')}\n{elon.get('matn','')}\n\n"
    xabar += "🗑 O'chirish: <code>/elon_uch [raqam]</code>\n<i>Masalan: /elon_uch 2</i>"
    await update.message.reply_text(xabar, parse_mode="HTML")

async def elon_uch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return
    args = context.args
    if not args or not args[0].isdigit():
        await update.message.reply_text(
            "❌ Raqam kiriting!\n<i>Masalan: /elon_uch 2</i>",
            parse_mode="HTML"
        )
        return
    n = int(args[0])
    elonlar = elonlar_yuklash()
    if n < 1 or n > len(elonlar):
        await update.message.reply_text(f"❌ #{n} raqamli elon topilmadi. Jami: {len(elonlar)} ta")
        return
    ochirilgan = elonlar.pop(n - 1)
    elonlar_saqlash(elonlar)
    await update.message.reply_text(
        f"✅ <b>#{n} elon o'chirildi!</b>\n\n{ochirilgan.get('matn','')}\n\n"
        f"📋 Qolgan elonlar: <b>{len(elonlar)} ta</b>",
        parse_mode="HTML"
    )

async def admin_bekor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Bekor qilindi.")
    return ConversationHandler.END

# =============================================
# DARSGA YOZILISH - ConversationHandler
# =============================================

async def darsga_yozilish_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    await update.message.reply_text(
        t("enroll_start", lang),
        parse_mode="HTML",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton(t("btn_cancel", lang))]], resize_keyboard=True
        )
    )
    return ISM

async def ism_olish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    if update.message.text == t("btn_cancel", lang):
        await update.message.reply_text(t("cancelled", lang), reply_markup=bosh_menyu(lang))
        return ConversationHandler.END
    context.user_data["ism"] = update.message.text
    await update.message.reply_text(
        t("enroll_phone", lang, ism=update.message.text),
        parse_mode="HTML"
    )
    return TELEFON_KIRISH

async def telefon_olish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    if update.message.text == t("btn_cancel", lang):
        await update.message.reply_text(t("cancelled", lang), reply_markup=bosh_menyu(lang))
        return ConversationHandler.END
    context.user_data["telefon"] = update.message.text
    fan_list = FANLAR[lang]
    fan_tugmalar = [[KeyboardButton(fan)] for fan in fan_list]
    fan_tugmalar.append([KeyboardButton(t("btn_cancel", lang))])
    await update.message.reply_text(
        t("enroll_subject", lang),
        reply_markup=ReplyKeyboardMarkup(fan_tugmalar, resize_keyboard=True)
    )
    return FAN_TANLASH

async def fan_olish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    if update.message.text == t("btn_cancel", lang):
        await update.message.reply_text(t("cancelled", lang), reply_markup=bosh_menyu(lang))
        return ConversationHandler.END
    fan = update.message.text
    ism = context.user_data.get("ism")
    telefon = context.user_data.get("telefon")
    await update.message.reply_text(
        t("enroll_done", lang, ism=ism, tel=telefon, fan=fan, markaz_tel=TELEFON),
        parse_mode="HTML",
        reply_markup=bosh_menyu(lang)
    )
    # Admin ga xabar yuborish
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"🆕 Yangi ariza!\n👤 {ism}\n📱 {telefon}\n📚 {fan}")
    return ConversationHandler.END

async def bekor_qilish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    await update.message.reply_text(t("cancelled", lang), reply_markup=bosh_menyu(lang))
    return ConversationHandler.END

# =============================================
# MAIN
# =============================================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    til_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(filters.Regex("^🌐"), til_ozgartirish),
        ],
        states={
            LANG_SELECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, til_tanlash)],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    yozilish_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex("^📝"), darsga_yozilish_start)
        ],
        states={
            ISM:            [MessageHandler(filters.TEXT & ~filters.COMMAND, ism_olish)],
            TELEFON_KIRISH: [MessageHandler(filters.TEXT & ~filters.COMMAND, telefon_olish)],
            FAN_TANLASH:    [MessageHandler(filters.TEXT & ~filters.COMMAND, fan_olish)],
        },
        fallbacks=[MessageHandler(filters.Regex("^❌"), bekor_qilish)],
    )

    app.add_handler(til_handler)
    app.add_handler(yozilish_handler)

    # Admin: elon qo'shish conversation
    elon_qosh_handler = ConversationHandler(
        entry_points=[CommandHandler("elon_qosh", elon_qosh_start)],
        states={
            ELON_MATN: [MessageHandler(filters.TEXT & ~filters.COMMAND, elon_matn_olish)],
        },
        fallbacks=[CommandHandler("bekor", admin_bekor)],
    )
    app.add_handler(elon_qosh_handler)
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CommandHandler("elon_list", elon_list))
    app.add_handler(CommandHandler("elon_uch", elon_uch))
    app.add_handler(CommandHandler("bekor", admin_bekor))

    app.add_handler(MessageHandler(filters.Regex("^👨‍🏫"), oqituvchilar))
    app.add_handler(MessageHandler(filters.Regex("^💳"), tolov_malumotlari))
    app.add_handler(MessageHandler(filters.Regex("^📞"), aloqa_manzil))
    app.add_handler(MessageHandler(filters.Regex("^📣"), elonlar_korsatish))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, noaniq_xabar))

    print(f"🤖 {MARKAZ_NOMI} boti (Ko'p tilli) ishga tushdi!")
    app.run_polling()

if __name__ == "__main__":
    main()

    print(f"🤖 {MARKAZ_NOMI} boti (Ko'p tilli) ishga tushdi!")
    app.run_polling()

if __name__ == "__main__":
    main()
