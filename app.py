import uvicorn
import logging
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import os
from PIL import Image
import uuid
from dotenv import load_dotenv
from utils.utils import get_db_connection, create_table

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
os.makedirs("logs", exist_ok=True)
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
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Создание директорий
os.makedirs("static/images", exist_ok=True)
os.makedirs("static/thumbnails", exist_ok=True)
os.makedirs("static/js", exist_ok=True)

# Создание таблицы в базе данных
create_table()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    logger.info("Доступ к домашней странице")
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/images/", response_class=HTMLResponse)
async def images(request: Request):
    logger.info("Доступ к странице галереи")
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, url, thumbnail_url, description, upload_date FROM photos")
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
    except Exception as error:
        logger.error(f"Ошибка при получении изображений из БД: {error}")
        images = []
    return templates.TemplateResponse("images.html", {"request": request, "images": images})

@app.get("/upload/", response_class=HTMLResponse)
async def upload_page(request: Request):
    logger.info("Доступ к странице загрузки")
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/upload/", response_class=HTMLResponse)
async def upload_image(request: Request, image: UploadFile = File(...), description: str = Form(None)):
    allowed_extensions = {'.jpg', '.png', '.gif'}
    max_file_size = 5 * 1024 * 1024

    file_extension = os.path.splitext(image.filename)[1].lower()
    if file_extension not in allowed_extensions:
        logger.error(f"Неверный формат файла: {image.filename}")
        return templates.TemplateResponse("upload.html", {
            "request": request,
            "message": "Разрешены только файлы формата .jpg, .png или .gif"
        })

    image.file.seek(0, os.SEEK_END)
    file_size = image.file.tell()
    image.file.seek(0)
    if file_size > max_file_size:
        logger.error(f"Файл слишком большой: {image.filename}, размер: {file_size} байт")
        return templates.TemplateResponse("upload.html", {
            "request": request,
            "message": "Размер файла не должен превышать 5 МБ"
        })

    if not image.content_type.startswith("image/"):
        logger.error(f"Неверный тип файла: {image.filename}, контент-тип: {image.content_type}")
        return templates.TemplateResponse("upload.html", {
            "request": request,
            "message": "Файл должен быть изображением"
        })

    file_name = f"{uuid.uuid4()}{file_extension}"
    thumbnail_name = f"thumb_{file_name}"
    image_path = os.path.join("static/images", file_name)
    thumbnail_path = os.path.join("static/thumbnails", thumbnail_name)

    with open(image_path, "wb") as f:
        f.write(await image.read())

    with Image.open(image_path) as img:
        img.thumbnail((64, 64))
        img.save(thumbnail_path, quality=85)

    try:
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

if __name__ == "__main__":
    logger.info("Сервер запущен на http://127.0.0.1:8000")
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)