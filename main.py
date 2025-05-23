from handlers import *
from telegram.ext import (Application, CommandHandler, MessageHandler, filters)

token_of_bot = '7651345538:AAEF75crnIbaBQUBppqom1fWQeKNJBaiN8U'

def main():
    app = Application.builder().token(token_of_bot).read_timeout(10).build()  # создание приложения бота

    # регистрируем обработчик команд
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help))

    # регистрация обработчика текстовых сообщений 
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, list_examples))

    # регистрация обработчика ошибок 
    app.add_error_handler(error)

    # запуск бота
    print('Бот запущен!')
    app.run_polling()

if __name__ == '__main__':
    main()