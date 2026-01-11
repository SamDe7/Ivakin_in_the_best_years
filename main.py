from handlers_fuck import handle_messages, start, help, error
from telegram.ext import (Application, CommandHandler, MessageHandler, filters)
from telegram import BotCommand, Update
from dotenv import load_dotenv
import os


load_dotenv()

token = os.getenv("token")
token_of_bot = token

async def set_bot_commands(app):
    commands = [
        BotCommand('start', "Начать работу"),
        BotCommand('help', "Справка по командам"),
    ]
    await app.bot.set_my_commands(commands)

def main():
    app = Application.builder().token(token_of_bot).read_timeout(10).build()  # создание приложения бота
    app.post_init = set_bot_commands

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help))

    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_messages))
    

    app.add_error_handler(error)

    print('Бот запущен!')
    app.run_polling()

if __name__ == '__main__':
    main()