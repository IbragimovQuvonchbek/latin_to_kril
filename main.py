import threading
from transliterate import to_latin, to_cyrillic
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = "6464944022:AAFWKR9DghZocnZNAbm243TR14IQJxkwsRY"
updater = Updater(TOKEN)
dispatcher = updater.dispatcher

def start(update: Update, context: CallbackContext) -> None:
    answer = "Kirill-Lotin tarjimon botiga xush kelibsiz! Tarjima qilishni boshlash uchun quydagilardan birini tanlang\n/Krill_Lotin\n/Lotin_Krill"
    update.message.reply_text(answer)

def translate_text(text, direction):
    if direction == 'krill-latin':
        return to_latin(text)
    elif direction == 'latin-krill':
        return to_cyrillic(text)
    else:
        return "Noto'g'ri tarjima yo'nalishi"

def translation_handler(update: Update, context: CallbackContext) -> None:
    translation_direction = context.user_data.get('translation_direction')
    if translation_direction:
        translated_text = translate_text(update.message.text, translation_direction)
        update.message.reply_text(f'Tarjima: {translated_text}')
    else:
        update.message.reply_text("Tarjima yo'nalishi tanlanmagan")

def krltn_handler(update: Update, context: CallbackContext) -> None:
    context.user_data['translation_direction'] = 'krill-latin'
    update.message.reply_text('Kirill dan Lotin ga tarjima tanlandi! Matn kiriting:')

def ltnkrl_handler(update: Update, context: CallbackContext) -> None:
    context.user_data['translation_direction'] = 'latin-krill'
    update.message.reply_text('Lotin dan Kirill ga tarjima tanlandi! Matn kiriting:')

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("Krill_Lotin", krltn_handler))
dispatcher.add_handler(CommandHandler("Lotin_Krill", ltnkrl_handler))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, translation_handler))

def polling_thread():
    updater.start_polling()
    updater.idle()

polling_thread = threading.Thread(target=polling_thread)
polling_thread.start()

polling_thread.join()
