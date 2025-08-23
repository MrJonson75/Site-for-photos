import os
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()


def get_db_connection():
    """
    Устанавливает соединение с базой данных PostgreSQL, используя переменные окружения.

    Returns:
        psycopg2.connection: Объект соединения с базой данных.

    Raises:
        ValueError: Если отсутствуют необходимые переменные окружения (P_USER, P_PASSWORD, P_DB).
        psycopg2.Error: Если не удалось установить соединение с базой данных.
    """
    # Получаем переменные окружения для подключения к БД
    user = os.getenv("P_USER")
    password = os.getenv("P_PASSWORD")
    db = os.getenv("P_DB")

    # Выводим отладочную информацию о параметрах подключения
    print(f"Connecting to DB: user={user}, db={db}, host=db, port=5432")

    # Проверяем наличие всех необходимых переменных окружения
    if not all([user, password, db]):
        raise ValueError("Missing environment variables: P_USER, P_PASSWORD, or P_DB")

    # Устанавливаем соединение с базой данных
    return psycopg2.connect(
        user=user,
        password=password,
        host="db",
        port="5432",
        database=db
    )


def create_table():
    """
    Создает таблицу 'photos' в базе данных, если она еще не существует.

    Таблица содержит следующие поля:
    - id: Уникальный идентификатор (SERIAL PRIMARY KEY)
    - url: URL изображения (VARCHAR(255), NOT NULL)
    - thumbnail_url: URL миниатюры изображения (VARCHAR(255), NOT NULL)
    - description: Описание изображения (TEXT, необязательное)
    - upload_date: Дата загрузки (TIMESTAMP, по умолчанию CURRENT_TIMESTAMP)

    Raises:
        psycopg2.Error: Если произошла ошибка при создании таблицы.
    """
    connection = None
    cursor = None
    try:
        # Получаем соединение с базой данных
        connection = get_db_connection()
        cursor = connection.cursor()

        # SQL-запрос для создания таблицы photos
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS photos (
            id SERIAL PRIMARY KEY,
            url VARCHAR(255) NOT NULL,
            thumbnail_url VARCHAR(255) NOT NULL,
            description TEXT,
            upload_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        '''
        # Выполняем запрос
        cursor.execute(create_table_query)
        # Подтверждаем изменения
        connection.commit()
        print("Таблица photos успешно создана!")
    except (Exception, Error) as error:
        # Выводим сообщение об ошибке и выбрасываем исключение
        print("Ошибка при создании таблицы:", error)
        raise
    finally:
        # Закрываем курсор, если он был создан
        if cursor:
            cursor.close()
        # Закрываем соединение, если оно было установлено
        if connection:
            connection.close()


def delete_image(image_id):
    """
    Удаляет изображение из базы данных и соответствующие файлы из файловой системы.

    Args:
        image_id (int): Идентификатор изображения для удаления.

    Raises:
        ValueError: Если изображение с указанным ID не найдено.
        psycopg2.Error: Если произошла ошибка при выполнении SQL-запроса.
        OSError: Если произошла ошибка при удалении файлов.
    """
    connection = None
    cursor = None
    try:
        # Получаем соединение с базой данных
        connection = get_db_connection()
        cursor = connection.cursor()

        # Получаем URL изображения и миниатюры по ID
        cursor.execute("SELECT url, thumbnail_url FROM photos WHERE id = %s", (image_id,))
        result = cursor.fetchone()
        if not result:
            raise ValueError(f"Изображение с ID {image_id} не найдено")

        # Извлекаем URL изображения и миниатюры
        image_url, thumbnail_url = result

        # Удаляем запись из базы данных
        cursor.execute("DELETE FROM photos WHERE id = %s", (image_id,))
        connection.commit()

        # Формируем пути к файлам изображения и миниатюры
        image_path = os.path.join("/app", image_url.lstrip("/"))
        thumbnail_path = os.path.join("/app", thumbnail_url.lstrip("/"))

        # Удаляем файл изображения, если он существует
        if os.path.exists(image_path):
            os.remove(image_path)
        # Удаляем файл миниатюры, если он существует
        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)

        print(f"Изображение с ID {image_id} успешно удалено")
    except (Exception, Error) as error:
        # Выводим сообщение об ошибке и выбрасываем исключение
        print(f"Ошибка при удалении изображения: {error}")
        raise
    finally:
        # Закрываем курсор, если он был создан
        if cursor:
            cursor.close()
        # Закрываем соединение, если оно было установлено
        if connection:
            connection.close()