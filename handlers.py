from telegram import Update
from telegram.ext import ContextTypes
import random
from datetime import datetime, time

class Bot_time:
    def __init__(self):
        self.time = None
    
    def bot_start(self):
        self.time = datetime.now()
        print(f"Бот запущен в {self.time}")

time_bot = Bot_time()

class Bot_messages:
    def __init__(self, max_size=15):
        self.list_for_bot = []
        self.max_size = max_size

    def bot_list(self, element: str) -> list:
        if element not in self.list_for_bot:
            self.list_for_bot.append(element)
        if len(self.list_for_bot) > self.max_size:
            del self.list_for_bot[random.randrange(len(self.list_for_bot))]
        return self.list_for_bot
bot_message = Bot_messages()

async def list_examples(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = time(update.message.text)
    if text < time_bot:
        return
    updated_list = bot_message.bot_list(text)
    await update.message.reply_text(random.choice(updated_list))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    await update.message.reply_text(f'Привет, {user_name}! Я подозреваю, \n что твой id: {user_id}')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Помощь: /start, /help')

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Ошибка: {context.error}")
    await update.message.reply_text('Произошла ошибка!')
