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
MANZIL = "G'ulakandoz qishloq'i (markazi), istiqlol binosi, Davron Samadov"
TELEFON = "+992 94 000 3000"
TELEFON2 = "+998 98 880 0708"
ISH_VAQTI_UZ = "Dush-Shan: 08:00 - 17:00"
ISH_VAQTI_RU = "Пн-Вс: 08:00 - 17:00"
ISH_VAQTI_EN = "Mon-Sun: 08:00 - 17:00"
ISH_VAQTI_TJ = "Душ-Шан: 08:00 - 17:00"
KARTA_RAQAM = "94 300 3000"
KARTA_EGASI = " Abdimuminova Muhabbat Abdijabborovna"
BANK = "dushanbe city"

# O'qituvchilar
OQITUVCHILAR = [
    {"ism": "Фозилова Мадинахон Одиловна", "fan_uz": "инглиз тили", "fan_ru": "Англиский", "fan_en": "english", "fan_tj": "Англисӣ", "tajriba": 11,  "emoji": "📐"},
    {"ism": "Самадова Хосият", "fan_uz": "рус тили","fan_ru": "русский", "fan_en": "russian",     "fan_tj": "русӣ",    "tajriba": 38,  "emoji": "🇬🇧"},
    {"ism": "Шукурова Солиҳаҷон Йулдошовна", "fan_uz": "инглиз тили",     "fan_ru": "Англиский",     "fan_en": "english",     "fan_tj": "Англисӣ",     "tajriba": 19,  "emoji": "⚡"},
    {"ism": "Ахмедҷонова Нилуфар Юсуфҷоновна",  "fan_uz": "рус тили",      "fan_ru": "русский",      "fan_en": "russian",   "fan_tj": "русӣ",      "tajriba": 33,  "emoji": "🧪"},
    {"ism": "Бойматова Шахноза", "fan_uz": "инглиз тили", "fan_ru": "Англиский", "fan_en": "english", "fan_tj": "Англисӣ", "tajriba": 18,  "emoji": "📐"},
    {"ism": "Абдимуминова Муҳабат Абдиҷабборовна", "fan_uz": "Администратор", "fan_ru": "Администратор", "fan_en": "Administrator", "fan_tj": "Маъмур", "tajriba": 0, "emoji": "🗂"},
]

FANLAR = {
    "uz": ["Ingliz tili", "Rus tili"],
    "ru": ["Английский", ,  "Русский язык"],
    "en": ["English", "Russian"],
    "tj": ["Англисӣ","Русӣ"],
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
        "uz": "👋 Assalomu alaykum, {name}!\n\n🏫 <b>{markaz}</b> botiga xush kelibsiz!\n\nQuyidagi bo'limlardan birini tanlang:",
        "ru": "👋 Здравствуйте, {name}!\n\n🏫 Добро пожаловать в бот <b>{markaz}</b>!\n\nВыберите один из разделов:",
        "en": "👋 Hello, {name}!\n\n🏫 Welcome to <b>{markaz}</b> bot!\n\nPlease choose a section:",
        "tj": "👋 Салом, {name}!\n\n🏫 Ба боти <b>{markaz}</b> хуш омадед!\n\nЯке аз бахшҳоро интихоб кунед:",
    },
    # --- MENYU TUGMALARI ---
    "btn_teachers": {
        "uz": "👨‍🏫 O'qituvchilar",
        "ru": "👨‍🏫 Учителя",
        "en": "👨‍🏫 Teachers",
        "tj": "👨‍🏫 Муаллимон",
    },
    "btn_payment": {
        "uz": "💳 To'lov ma'lumotlari",
        "ru": "💳 Данные оплаты",
        "en": "💳 Payment info",
        "tj": "💳 Маълумоти пардохт",
    },
    "btn_register": {
        "uz": "📝 Darsga yozilish",
        "ru": "📝 Записаться на курс",
        "en": "📝 Enroll in course",
        "tj": "📝 Ба дарс навиштан",
    },
    "btn_contact": {
        "uz": "📞 Aloqa / Manzil",
        "ru": "📞 Контакты / Адрес",
        "en": "📞 Contact / Address",
        "tj": "📞 Тамос / Суроға",
    },
    "btn_language": {
        "uz": "🌐 Tilni o'zgartirish",
        "ru": "🌐 Сменить язык",
        "en": "🌐 Change language",
        "tj": "🌐 Иваз кардани забон",
    },
    "btn_cancel": {
        "uz": "❌ Bekor qilish",
        "ru": "❌ Отмена",
        "en": "❌ Cancel",
        "tj": "❌ Бекор кардан",
    },
    "btn_map": {
        "uz": "🗺 Xaritada ko'rish",
        "ru": "🗺 Посмотреть на карте",
        "en": "🗺 View on map",
        "tj": "🗺 Дар харита дидан",
    },
    "btn_channel": {
        "uz": "📲 Telegram kanal",
        "ru": "📲 Telegram канал",
        "en": "📲 Telegram channel",
        "tj": "📲 Канали Telegram",
    },
    "btn_paid": {
        "uz": "✅ To'lov qildim - Chek yuborish",
        "ru": "✅ Оплатил - Отправить чек",
        "en": "✅ Paid - Send receipt",
        "tj": "✅ Пардохт кардам - Чек фиристодан",
    },
    # --- ALOQA ---
    "contact_title": {
        "uz": "📞 <b>Aloqa va Manzil</b>\n{'━'*25}\n\n🏫 <b>{markaz}</b>\n\n📍 {manzil}\n\n📞 {tel1}\n📞 {tel2}\n\n🕐 {vaqt}\n\n💬 <i>Savollaringiz bo'lsa, qo'ng'iroq qiling!</i>",
        "ru": "📞 <b>Контакты и Адрес</b>\n{'━'*25}\n\n🏫 <b>{markaz}</b>\n\n📍 {manzil}\n\n📞 {tel1}\n📞 {tel2}\n\n🕐 {vaqt}\n\n💬 <i>Если есть вопросы — звоните!</i>",
        "en": "📞 <b>Contact & Address</b>\n{'━'*25}\n\n🏫 <b>{markaz}</b>\n\n📍 {manzil}\n\n📞 {tel1}\n📞 {tel2}\n\n🕐 {vaqt}\n\n💬 <i>Call us if you have questions!</i>",
        "tj": "📞 <b>Тамос ва Суроға</b>\n{'━'*25}\n\n🏫 <b>{markaz}</b>\n\n📍 {manzil}\n\n📞 {tel1}\n📞 {tel2}\n\n🕐 {vaqt}\n\n💬 <i>Агар саволе дошта бошед, занг занед!</i>",
    },
    # --- TO'LOV ---
    "payment_title": {
        "uz": (
            "💳 <b>To'lov Ma'lumotlari</b>\n{'━'*25}\n\n"
            "💳 {karta}\n👤 {egasi}\n🏦 {bank}\n\n"
            "📌 <b>Eslatma:</b>\n"
            "• To'lov har oyning 1-5 sanasi\n"
            "• To'lovdan so'ng chekni adminga yuboring\n"
            "• Muammo bo'lsa: 📞 {tel}"
        ),
        "ru": (
            "💳 <b>Данные Оплаты</b>\n{'━'*25}\n\n"
            "💳 {karta}\n👤 {egasi}\n🏦 {bank}\n\n"
            "📌 <b>Примечание:</b>\n"
            "• Оплата с 1 по 5 число каждого месяца\n"
            "• После оплаты отправьте чек администратору\n"
            "• При проблемах: 📞 {tel}"
        ),
        "en": (
            "💳 <b>Payment Information</b>\n{'━'*25}\n\n"
            "💳 {karta}\n👤 {egasi}\n🏦 {bank}\n\n"
            "📌 <b>Note:</b>\n"
            "• Payment due on 1st–5th of each month\n"
            "• Send receipt to admin after payment\n"
            "• For issues: 📞 {tel}"
        ),
        "tj": (
            "💳 <b>Маълумоти Пардохт</b>\n{'━'*25}\n\n"
            "💳 {karta}\n👤 {egasi}\n🏦 {bank}\n\n"
            "📌 <b>Эзоҳ:</b>\n"
            "• Пардохт аз 1 то 5-уми ҳар моҳ\n"
            "• Пас аз пардохт чекро ба админ фиристед\n"
            "• Дар мушкилот: 📞 {tel}"
        ),
    },
    # --- O'QITUVCHILAR ---
    "teachers_title": {
        "uz": "👨‍🏫 <b>O'qituvchilarimiz</b>\n{'━'*25}\n\n",
        "ru": "👨‍🏫 <b>Наши Учителя</b>\n{'━'*25}\n\n",
        "en": "👨‍🏫 <b>Our Teachers</b>\n{'━'*25}\n\n",
        "tj": "👨‍🏫 <b>Муаллимони мо</b>\n{'━'*25}\n\n",
    },
    "teacher_row": {
        "uz": "{emoji} <b>{ism}</b>\n   📚 Fan: {fan}\n   🏆 {yil} yil tajriba\n\n",
        "ru": "{emoji} <b>{ism}</b>\n   📚 Предмет: {fan}\n   🏆 Опыт: {yil} лет\n\n",
        "en": "{emoji} <b>{ism}</b>\n   📚 Subject: {fan}\n   🏆 Experience: {yil} years\n\n",
        "tj": "{emoji} <b>{ism}</b>\n   📚 Фан: {fan}\n   🏆 Таҷриба: {yil} сол\n\n",
    },
    "teachers_footer": {
        "uz": "📞 Batafsil ma'lumot: {tel}",
        "ru": "📞 Подробнее: {tel}",
        "en": "📞 More info: {tel}",
        "tj": "📞 Маълумоти бештар: {tel}",
    },
    # --- DARSGA YOZILISH ---
    "enroll_start": {
        "uz": "📝 <b>Darsga yozilish</b>\n{'━'*25}\n\nIsmingiz va familiyangizni kiriting:\n<i>(Masalan: Aliyev Jasur)</i>",
        "ru": "📝 <b>Запись на курс</b>\n{'━'*25}\n\nВведите ваше имя и фамилию:\n<i>(Например: Aliyev Jasur)</i>",
        "en": "📝 <b>Course Enrollment</b>\n{'━'*25}\n\nEnter your first and last name:\n<i>(Example: Aliyev Jasur)</i>",
        "tj": "📝 <b>Ба дарс навиштан</b>\n{'━'*25}\n\nНоми ва насаби худро ворид кунед:\n<i>(Масалан: Алиев Ҷасур)</i>",
    },
    "enroll_phone": {
        "uz": "✅ Ism saqlandi: <b>{ism}</b>\n\n📱 Telefon raqamingizni kiriting:\n<i>(Masalan: +998901234567)</i>",
        "ru": "✅ Имя сохранено: <b>{ism}</b>\n\n📱 Введите ваш номер телефона:\n<i>(Например: +998901234567)</i>",
        "en": "✅ Name saved: <b>{ism}</b>\n\n📱 Enter your phone number:\n<i>(Example: +998901234567)</i>",
        "tj": "✅ Ном сабт шуд: <b>{ism}</b>\n\n📱 Рақами телефони худро ворид кунед:\n<i>(Масалан: +998901234567)</i>",
    },
    "enroll_subject": {
        "uz": "📚 Qaysi fanga yozilmoqchisiz?",
        "ru": "📚 На какой предмет хотите записаться?",
        "en": "📚 Which subject would you like to enroll in?",
        "tj": "📚 Ба кадом фан навиштан мехоҳед?",
    },
    "enroll_done": {
        "uz": "✅ <b>Arizangiz qabul qilindi!</b>\n{'━'*25}\n\n👤 Ism: <b>{ism}</b>\n📱 Telefon: <b>{tel}</b>\n📚 Fan: <b>{fan}</b>\n\n⏳ Tez orada administrator siz bilan bog'lanadi.\n📞 Savollar uchun: {markaz_tel}",
        "ru": "✅ <b>Ваша заявка принята!</b>\n{'━'*25}\n\n👤 Имя: <b>{ism}</b>\n📱 Телефон: <b>{tel}</b>\n📚 Предмет: <b>{fan}</b>\n\n⏳ Администратор свяжется с вами в ближайшее время.\n📞 Вопросы: {markaz_tel}",
        "en": "✅ <b>Your application is accepted!</b>\n{'━'*25}\n\n👤 Name: <b>{ism}</b>\n📱 Phone: <b>{tel}</b>\n📚 Subject: <b>{fan}</b>\n\n⏳ An administrator will contact you shortly.\n📞 Questions: {markaz_tel}",
        "tj": "✅ <b>Аризаи шумо қабул шуд!</b>\n{'━'*25}\n\n👤 Ном: <b>{ism}</b>\n📱 Телефон: <b>{tel}</b>\n📚 Фан: <b>{fan}</b>\n\n⏳ Администратор ба зудӣ бо шумо тамос мегирад.\n📞 Савол: {markaz_tel}",
    },
    "cancelled": {
        "uz": "❌ Bekor qilindi.",
        "ru": "❌ Отменено.",
        "en": "❌ Cancelled.",
        "tj": "❌ Бекор карда шуд.",
    },
    "unknown": {
        "uz": "❓ Iltimos, quyidagi tugmalardan birini tanlang:",
        "ru": "❓ Пожалуйста, выберите одну из кнопок ниже:",
        "en": "❓ Please choose one of the buttons below:",
        "tj": "❓ Лутфан яке аз тугмаҳои зеринро интихоб кунед:",
    },
}

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
    """Foydalanuvchi tilini olish (default: uz)"""
    return context.user_data.get("lang", "uz")

def t(key: str, lang: str, **kwargs) -> str:
    """Tarjima olish"""
    template = TEXTS[key][lang]
    if kwargs:
        try:
            return template.format(**kwargs)
        except Exception:
            return template
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
    "🇺🇿 O'zbek":   "uz",
    "🇷🇺 Русский":  "ru",
    "🇬🇧 English":  "en",
    "🇹🇯 Тоҷикӣ":  "tj",
}

# =============================================
# HANDLERS
# =============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot ishga tushganda — til tanlash"""
    await update.message.reply_text(
        "🌐 Tilni tanlang / Выберите язык / Choose language / Забонро интихоб кунед:",
        reply_markup=til_tanlash_menyu()
    )
    return LANG_SELECT

async def til_tanlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tanlangan tilni saqlash"""
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
    """Tilni o'zgartirish"""
    await update.message.reply_text(
        "🌐 Tilni tanlang / Выберите язык / Choose language / Забонро интихоб кунед:",
        reply_markup=til_tanlash_menyu()
    )
    return LANG_SELECT

async def aloqa_manzil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    vaqt = ISH_VAQTLAR[lang]
    xabar = (
        t("contact_title", lang,
          markaz=MARKAZ_NOMI,
          manzil=MANZIL,
          tel1=TELEFON,
          tel2=TELEFON2,
          vaqt=vaqt)
        .replace("{'━'*25}", "━" * 25)
    )
    inline = InlineKeyboardMarkup([
        [InlineKeyboardButton(t("btn_map", lang), url="https://maps.google.com/?q=41.2995,69.2401")],
        [InlineKeyboardButton(t("btn_channel", lang), url="https://t.me/babolo_markaz")]
    ])
    await update.message.reply_text(xabar, parse_mode="HTML", reply_markup=inline)

async def tolov_malumotlari(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    xabar = (
        t("payment_title", lang,
          karta=KARTA_RAQAM,
          egasi=KARTA_EGASI,
          bank=BANK,
          tel=TELEFON)
        .replace("{'━'*25}", "━" * 25)
    )
    inline = InlineKeyboardMarkup([
        [InlineKeyboardButton(t("btn_paid", lang), url="https://t.me/babolo_admin")]
    ])
    await update.message.reply_text(xabar, parse_mode="HTML", reply_markup=inline)

async def oqituvchilar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    fan_key = FAN_KEYS[lang]
    xabar = t("teachers_title", lang).replace("{'━'*25}", "━" * 25)
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
        t("enroll_start", lang).replace("{'━'*25}", "━" * 25),
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
        t("enroll_done", lang, ism=ism, tel=telefon, fan=fan, markaz_tel=TELEFON).replace("{'━'*25}", "━" * 25),
        parse_mode="HTML",
        reply_markup=bosh_menyu(lang)
    )
    # Admin ga xabar yuborish
    # ADMIN_CHAT_ID = 123456789
    # await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"🆕 Yangi ariza!\n👤 {ism}\n📱 {telefon}\n📚 {fan}")
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

    # Til tanlash uchun ConversationHandler
    til_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(
                filters.Regex("^🌐"),
                til_ozgartirish
            ),
        ],
        states={
            LANG_SELECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, til_tanlash)],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    # Darsga yozilish uchun ConversationHandler
    yozilish_handler = ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.Regex("^📝"),
                darsga_yozilish_start
            )
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

    print(f"🤖 {MARKAZ_NOMI} boti (Ko'p tilli) ishga tushdi!")
    app.run_polling()

if __name__ == "__main__":
    main()
