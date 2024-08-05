from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler
)

# Вставьте ваш токен сюда
TOKEN = '7328569831:AAEshHviq0MFmBxzPisRKeAFoHXNFW8TbKM'

# Этапы разговора
ASK_LINK, ONE_MORE_VIDEO, CHOOSE_OPTION, WAIT_FOR_PAYMENT = range(4)

# Ответы
ONE_VIDEO = 'Скачать одно видео'
UNLIMITED = '150р и безлимит'

# Стартовое сообщение
START_MESSAGE = 'Привет, я помогу тебе скачать видео из инстаграм. Скидывай ссылку на видео.'

# Начало взаимодействия
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(START_MESSAGE)
    return ASK_LINK

# Получение и обработка ссылки
async def get_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    link = update.message.text
    modified_link = link.replace('www.', 'dd')
    await update.message.reply_text('Держи видос!')
    await update.message.reply_text(modified_link)
    reply_keyboard = [[ONE_VIDEO, UNLIMITED]]
    await update.message.reply_text(
        'Ты можешь ещё один раз скачать видео бесплатно. Если хочешь безлимитно скачивать видео, то с тебя 150р.',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return CHOOSE_OPTION

# Обработка выбора пользователя
async def choose_option(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_choice = update.message.text
    if user_choice == ONE_VIDEO:
        await update.message.reply_text('Скидывай ссылку на видео.')
        return ONE_MORE_VIDEO
    elif user_choice == UNLIMITED:
        await update.message.reply_text('Переведите 150р на Сбербанк реквизиты: 1234567890')
        await update.message.reply_text('После оплаты напишите "Оплачено"')
        context.user_data['unlimited'] = True
        return WAIT_FOR_PAYMENT

async def check_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text.lower() == "оплачено":
        await update.message.reply_text('Оплата прошла успешно! Скидывай ссылку на видео.')
        return ASK_LINK
    else:
        await update.message.reply_text('Пожалуйста напишите "Оплачено" после перевода средств.')
        return WAIT_FOR_PAYMENT

# Закачка одного дополнительного видео
async def one_more_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    link = update.message.text
    modified_link = link.replace('www.', 'dd')
    await update.message.reply_text('Держи видос!')
    await update.message.reply_text(modified_link)
    await update.message.reply_text(UNLIMITED)
    return WAIT_FOR_PAYMENT

async def unlimited_videos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    link = update.message.text
    modified_link = link.replace('www.', 'dd')
    await update.message.reply_text('Держи видос!')
    await update.message.reply_text(modified_link)
    await update.message.reply_text('Скидывай ссылку на видео.')
    return ASK_LINK

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Пока!')
    return ConversationHandler.END

def main():
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ASK_LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_link)],
            CHOOSE_OPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_option)],
            WAIT_FOR_PAYMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_payment)],
            ONE_MORE_VIDEO: [MessageHandler(filters.TEXT & ~filters.COMMAND, one_more_video)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)

    application.run_polling()

if __name__ == '__main__':
    main()