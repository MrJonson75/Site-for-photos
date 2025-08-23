import os
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def get_db_connection():
    user = os.getenv("P_USER")
    password = os.getenv("P_PASSWORD")
    db = os.getenv("P_DB")
    print(f"Connecting to DB: user={user}, db={db}, host=db, port=5432")  # Для отладки
    if not all([user, password, db]):
        raise ValueError("Missing environment variables: P_USER, P_PASSWORD, or P_DB")
    return psycopg2.connect(
        user=user,
        password=password,
        host="db",
        port="5432",
        database=db
    )

def create_table():
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS photos (
            id SERIAL PRIMARY KEY,
            url VARCHAR(255) NOT NULL,
            thumbnail_url VARCHAR(255) NOT NULL,
            description TEXT,
            upload_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        '''
        cursor.execute(create_table_query)
        connection.commit()
        print("Таблица photos успешно создана!")
    except (Exception, Error) as error:
        print("Ошибка при создании таблицы:", error)
        raise
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def delete_image(image_id):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        # Получаем URL изображения и миниатюры
        cursor.execute("SELECT url, thumbnail_url FROM photos WHERE id = %s", (image_id,))
        result = cursor.fetchone()
        if not result:
            raise ValueError(f"Изображение с ID {image_id} не найдено")

        image_url, thumbnail_url = result
        # Удаляем запись из базы данных
        cursor.execute("DELETE FROM photos WHERE id = %s", (image_id,))
        connection.commit()

        # Удаляем файлы из файловой системы
        image_path = os.path.join("/app", image_url.lstrip("/"))
        thumbnail_path = os.path.join("/app", thumbnail_url.lstrip("/"))
        if os.path.exists(image_path):
            os.remove(image_path)
        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)

        print(f"Изображение с ID {image_id} успешно удалено")
    except (Exception, Error) as error:
        print(f"Ошибка при удалении изображения: {error}")
        raise
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
