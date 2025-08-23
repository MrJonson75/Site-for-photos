import uvicorn
import logging
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import os
from PIL import Image
import uuid
from dotenv import load_dotenv
from utils.utils import get_db_connection, create_table, delete_image

# Загружаем переменные окружения из файла .env
load_dotenv()

# Настройка логирования
os.makedirs("logs", exist_ok=True)  # Создаем директорию для логов, если она не существует
log_handler = RotatingFileHandler(
    "logs/app.log", maxBytes=5*1024*1024, backupCount=5, encoding='utf-8'
)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[log_handler, logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Инициализация приложения FastAPI
app = FastAPI()
templates = Jinja2Templates(directory="templates")  # Настройка шаблонов Jinja2
app.mount("/static", StaticFiles(directory="static"), name="static")  # Подключение статических файлов

# Создание директорий для хранения изображений и скриптов
os.makedirs("static/images", exist_ok=True)
os.makedirs("static/thumbnails", exist_ok=True)
os.makedirs("static/js", exist_ok=True)

# Создание таблицы в базе данных при запуске приложения
create_table()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Отображает главную страницу приложения.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        TemplateResponse: HTML-ответ с рендерингом шаблона index.html.
    """
    logger.info("Доступ к домашней странице")
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/images/", response_class=HTMLResponse)
async def images(request: Request, page: int = 1, limit: int = 6):
    """
    Отображает страницу галереи с пагинацией изображений.

    Args:
        request (Request): Объект запроса FastAPI.
        page (int, optional): Номер страницы для пагинации. По умолчанию 1.
        limit (int, optional): Количество изображений на странице. По умолчанию 6.

    Returns:
        TemplateResponse: HTML-ответ с рендерингом шаблона images.html, содержащего список изображений и информацию о пагинации.

    Raises:
        Exception: Если произошла ошибка при получении данных из базы данных.
    """
    logger.info("Доступ к странице галереи")
    try:
        # Устанавливаем соединение с базой данных
        connection = get_db_connection()
        cursor = connection.cursor()

        # Считаем общее количество изображений
        cursor.execute("SELECT COUNT(*) FROM photos")
        total_images = cursor.fetchone()[0]

        # Вычисляем смещение для пагинации
        offset = (page - 1) * limit
        cursor.execute(
            "SELECT id, url, thumbnail_url, description, upload_date FROM photos ORDER BY upload_date DESC LIMIT %s OFFSET %s",
            (limit, offset)
        )

        # Формируем список изображений для отображения
        images = [
            {
                "id": row[0],
                "url": row[1],
                "thumbnail_url": row[2],
                "description": row[3],
                "upload_date": row[4].strftime("%Y-%m-%d %H:%M")
            }
            for row in cursor.fetchall()
        ]

        cursor.close()
        connection.close()

        # Вычисляем общее количество страниц
        total_pages = (total_images + limit - 1) // limit

    except Exception as error:
        logger.error(f"Ошибка при получении изображений из БД: {error}")
        images = []
        total_pages = 1
        page = 1

    return templates.TemplateResponse("images.html", {
        "request": request,
        "images": images,
        "page": page,
        "total_pages": total_pages
    })

@app.get("/upload/", response_class=HTMLResponse)
async def upload_page(request: Request):
    """
    Отображает страницу загрузки изображения.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        TemplateResponse: HTML-ответ с рендерингом шаблона upload.html.
    """
    logger.info("Доступ к странице загрузки")
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/upload/", response_class=HTMLResponse)
async def upload_image(request: Request, image: UploadFile = File(...), description: str = Form(None)):
    """
    Обрабатывает загрузку изображения, сохраняет его и миниатюру, а также записывает данные в базу данных.

    Args:
        request (Request): Объект запроса FastAPI.
        image (UploadFile): Загружаемый файл изображения.
        description (str, optional): Описание изображения. По умолчанию None.

    Returns:
        TemplateResponse: HTML-ответ с рендерингом шаблона upload.html и сообщением об успехе или ошибке.

    Raises:
        Exception: Если произошла ошибка при сохранении изображения в базу данных или файловую систему.
    """
    allowed_extensions = {'.jpg', '.png', '.gif'}  # Допустимые расширения файлов
    max_file_size = 5 * 1024 * 1024  # Максимальный размер файла (5 МБ)

    # Проверяем расширение файла
    file_extension = os.path.splitext(image.filename)[1].lower()
    if file_extension not in allowed_extensions:
        logger.error(f"Неверный формат файла: {image.filename}")
        return templates.TemplateResponse("upload.html", {
            "request": request,
            "message": "Разрешены только файлы формата .jpg, .png или .gif"
        })

    # Проверяем размер файла
    image.file.seek(0, os.SEEK_END)
    file_size = image.file.tell()
    image.file.seek(0)
    if file_size > max_file_size:
        logger.error(f"Файл слишком большой: {image.filename}, размер: {file_size} байт")
        return templates.TemplateResponse("upload.html", {
            "request": request,
            "message": "Размер файла не должен превышать 5 МБ"
        })

    # Проверяем тип содержимого файла
    if not image.content_type.startswith("image/"):
        logger.error(f"Неверный тип файла: {image.filename}, контент-тип: {image.content_type}")
        return templates.TemplateResponse("upload.html", {
            "request": request,
            "message": "Файл должен быть изображением"
        })

    # Генерируем уникальное имя файла
    file_name = f"{uuid.uuid4()}{file_extension}"
    thumbnail_name = f"thumb_{file_name}"
    image_path = os.path.join("static/images", file_name)
    thumbnail_path = os.path.join("static/thumbnails", thumbnail_name)

    # Сохраняем изображение
    with open(image_path, "wb") as f:
        f.write(await image.read())

    # Создаем и сохраняем миниатюру
    with Image.open(image_path) as img:
        img.thumbnail((64, 64))
        img.save(thumbnail_path, quality=85)

    try:
        # Сохраняем информацию об изображении в базу данных
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO photos (url, thumbnail_url, description)
            VALUES (%s, %s, %s)
            """,
            (f"/static/images/{file_name}", f"/static/thumbnails/{thumbnail_name}", description.strip() if description else "Без описания")
        )
        connection.commit()
        cursor.close()
        connection.close()
        logger.info(f"Успешная загрузка изображения: {file_name}, описание: {description}")
        message = "Изображение успешно загружено!"
    except Exception as error:
        logger.error(f"Ошибка при сохранении в БД: {error}")
        message = "Ошибка при сохранении изображения в базу данных"

    return templates.TemplateResponse("upload.html", {"request": request, "message": message})

@app.delete("/delete/{image_id}", response_class=RedirectResponse)
async def delete_image_endpoint(image_id: int):
    """
    Удаляет изображение из базы данных и файловой системы, перенаправляя на страницу галереи.

    Args:
        image_id (int): Идентификатор изображения для удаления.

    Returns:
        RedirectResponse: Перенаправление на страницу галереи (/images/).

    Raises:
        HTTPException: Если изображение не найдено или произошла ошибка при удалении.
    """
    try:
        # Удаляем изображение с помощью функции из utils
        delete_image(image_id)
        logger.info(f"Изображение с ID {image_id} успешно удалено")
        return RedirectResponse(url="/images/", status_code=303)
    except Exception as error:
        logger.error(f"Ошибка при удалении изображения с ID {image_id}: {error}")
        raise HTTPException(status_code=404, detail="Изображение не найдено или ошибка при удалении")

if __name__ == "__main__":
    # Запускаем сервер FastAPI
    logger.info("Сервер запущен на http://127.0.0.1:8000")
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)