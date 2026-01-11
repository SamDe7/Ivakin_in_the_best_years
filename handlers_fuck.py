from telegram.ext import ContextTypes
from telegram import Update
import random
from db_connection import save_content, get_random_content, get_content_count, delete_random_40_entires
from models import UserContent
from probability import probability_manager
import logging


def is_url(text: str) -> bool:
    url_patterns = [
        'http://', 'https://', 'www.', '.ru', '.com', 
        '.net', '.org', '.ua', '.рф', 't.me/', '@'
    ]
    
    text_lower = text.lower()
    return any(pattern in text_lower for pattern in url_patterns)


async def incoming_content(update: Update, user_id: int, chat_id: int):
    content = None
    try:
        count_content = get_content_count(chat_id)

        great_random_of_saving = random.random()
        saved_threshold = probability_manager.save_or_not(count_content)

        if update.message.text and not update.message.text.startswith('/'):
            if is_url(update.message.text):
                return
            text_from_user = update.message.text

            content = UserContent.get_from_telegram_message(user_id=user_id, 
                                                        chat_id=chat_id,
                                                        content_type='text', 
                                                        content_data=text_from_user,
                                                        save_probability=f"{saved_threshold:.3f}"
                                                        )
                
        elif update.message.photo:
            photo = update.message.photo[-1]
            content = UserContent.get_from_telegram_message(user_id=user_id,
                                                        chat_id=chat_id,
                                                        content_type='image',
                                                        content_data=photo.file_id,
                                                        save_probability=f"{saved_threshold:.3f}",
                                                        file_size=photo.file_size
                                                        )
    

        if content: 
            if great_random_of_saving < saved_threshold:
                saved = save_content(content)
            
                if saved:
                    count_after_saving = get_content_count(chat_id)
                    if count_after_saving > 200:
                        delete_random_40_entires(chat_id)
                else:
                    logging.info(f"Контент не сохранён для чата {chat_id} - это дубликат!")

    except Exception as e:
        logging.error(f"Произошла ошибка - {e}")

async def outgoing_content(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    try:
        count_content = get_content_count(chat_id)
        send_threshold = probability_manager.send_or_not(count_content)
    
        great_random_of_sending = random.random()
    
        random_content = get_random_content(chat_id)

        if random_content:
            if great_random_of_sending <= send_threshold:
                if random_content.content_type == 'text':
                    text_for_sending = random_content.content_data
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id, 
                        text=text_for_sending
                        )
                elif random_content.content_type == 'image':
                    await context.bot.send_photo(
                        chat_id=update.effective_chat.id,
                        photo=random_content.content_data
                    )
    except Exception as e:
        logging.error(f"FUUUCK - {e}")


async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.message.from_user.id
        chat_id = update.effective_chat.id     

        await incoming_content(update, user_id, chat_id)

        await outgoing_content(update, context, chat_id)
    except Exception as e:
        logging.error(f"Це повна {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.first_name
    await context.bot.send_message(text=f'Привет, {user_name}! \nЯ Захар Ивакин в лучшие годы', chat_id=update.effective_chat.id)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(text='Мы тут забиваемся', chat_id=update.effective_chat.id)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Произошла ошибка!')