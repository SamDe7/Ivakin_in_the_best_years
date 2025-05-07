from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

token_of_bot = '7651345538:AAEF75crnIbaBQUBppqom1fWQeKNJBaiN8U'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет, Я Захар Ивакин! Ты можешь использовать /help для списка команд')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Тебе пока ничего не доступно!')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('Ошибка!')
    if update:
        await update.message.reply_text('Произошла ошибка!')
    
def main():   # основная функция 
    app = Application.builder().token(token_of_bot).build()  # создание приложения бота

    # регистрируем обработчик команд
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help))

    # регистрируем обработчик текстовых сообщений 
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # регистрируем обработчик ошибок 
    app.add_error_handler(error)

    # запускаем бот
    print('Бот запущен!')
    app.run_polling()

if __name__ == "__main__":
    main()