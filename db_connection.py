import psycopg2
from dotenv import load_dotenv
import os
from models import UserContent
from typing import Optional
import logging
import hashlib
import random

load_dotenv()
db_password = os.getenv('db_password')

db_config = {
    "host": "localhost",
    "user": "postgres",
    "password": db_password,
    "database": "bd_ivashka_flat",
    "port": 5432,
    "client_encoding": "utf8"
}


def get_connection():
    return psycopg2.connect(**db_config)


# if get_connection():
#     print('okay, very good')


def save_content(content: UserContent) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            try:
                if content.content_type == 'text':
                    list_of_words_from_message = content.content_data.split()
                    if len(list_of_words_from_message) <= 9:
                        if check_dublicate_text(content.content_data, content.chat_id):
                            logging.info(f"Текстовый дубликат в чате {content.chat_id}")
                            return False
                        content_hash = get_text_hash(content.content_data)
                    elif content.content_type == 'image':
                        if check_dublicate_images(content.content_data, content.chat_id):
                            logging.info(f"Дубликат изображения в чате {content.chat_id}")
                            return False
                        content_hash = get_text_hash(content.content_data)

                cursor.execute(
                    """
                INSERT INTO user_content 
                (user_id, content_type, content_data, file_size, save_probability, content_hash, chat_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                    (content.user_id, content.content_type, content.content_data,
                     content.file_size, content.save_probability, content_hash, content.chat_id)
                )
                conn.commit()
                logging.info(f"Контент сохранён для чата {content.chat_id}")
                return True
            except Exception as e:
                logging.error(f"fucking mistake - {e}")
                return False
            

def get_random_content(chat_id: int) -> Optional[UserContent]:
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query_for_rand_id = """
                        SELECT id
                        FROM user_content
                        WHERE chat_id = %s
                        """
                cursor.execute(query_for_rand_id, (chat_id, ))

                id_list_of_the_chat = [row[0] for row in cursor.fetchall()]
                if not id_list_of_the_chat:
                    return None

                random_id = random.choice(id_list_of_the_chat)

                query = """
                        SELECT *
                        FROM user_content
                        WHERE id = %s
                        """
                cursor.execute(query, (random_id, ))
                result = cursor.fetchone()
                if result:
                    return UserContent(
                    id=result[0],
                    user_id=result[1],
                    content_type=result[2], 
                    content_data=result[3],
                    file_size=result[4],
                    save_probability=result[5],
                    created_at=result[6],
                    content_hash=result[7],
                    chat_id=result[8]
                    )
                return None
    except Exception as error:
        logging.error(f"get random content() - {error}")


def get_content_count(chat_id: int) -> int:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT COUNT(*) 
                FROM user_content
                WHERE chat_id = %s 
                """, (chat_id, )
            )
            return cursor.fetchone()[0]


def get_text_hash(data: str) -> str:
    normilized_text = data.strip()

    return hashlib.md5(normilized_text.encode('utf-8')).hexdigest()


def check_dublicate_text(content_data: str, chat_id: int) -> bool:
    if chat_id is None:
        raise ValueError("Chat_id не может быть None")
    with get_connection() as conn:
        with conn.cursor() as cursor:
            text_hash = get_text_hash(content_data)
            if chat_id:
                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM user_content
                    WHERE content_type = 'text'
                    AND content_hash = %s 
                    AND chat_id = %s
                    """, (text_hash, chat_id)
                )
            return cursor.fetchone()[0] > 0


def check_dublicate_images(content_data: str, chat_id: int) -> bool:
    if chat_id is None:
        raise ValueError("Chat_id не может быть None")
    with get_connection() as conn:
        with conn.cursor() as cursor:
            image_hash = get_text_hash(content_data)
            if chat_id:
                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM user_content
                    WHERE content_type = 'image'
                    AND content_hash = %s
                    AND chat_id = %s
                    """, (image_hash, chat_id)
                )
            return cursor.fetchone()[0] > 0

def delete_random_40_entires(chat_id: int):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                delete_query = """
                            DELETE FROM user_content 
                            WHERE id IN (
                            
                            SELECT id
                            FROM user_content
                            WHERE chat_id = %s
                            ORDER BY RANDOM()
                            LIMIT 40
                            )
                            """
                cursor.execute(delete_query, (chat_id, ))
                conn.commit()

    except Exception as e:
        logging.error(f'Тут произошёл такой вот fuck {e}')