import uvicorn
from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import os
from PIL import Image
import uuid

# Инициализация приложения FastAPI
app = FastAPI()
# Настройка Jinja2 для рендеринга шаблонов из папки templates
templates = Jinja2Templates(directory="templates")
# Монтирование папки static для обслуживания статических файлов (CSS, JS, изображения)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Создание директорий для хранения изображений, миниатюр и JavaScript-файлов
os.makedirs("static/images", exist_ok=True)
os.makedirs("static/thumbnails", exist_ok=True)
os.makedirs("static/js", exist_ok=True)

# Демонстрационный список фотографий (хранится в памяти для примера)
demo_images = []

# Обработчик GET-запроса для главной страницы
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Рендерит главную страницу index.html."""
    context = {
        "request": request,
    }
    return templates.TemplateResponse("index.html", context=context)

# Обработчик GET-запроса для страницы галереи
@app.get("/images/", response_class=HTMLResponse)
async def images(request: Request):
    """Рендерит страницу images.html с списком загруженных изображений."""
    context = {
        "request": request,
        "images": demo_images
    }
    return templates.TemplateResponse("images.html", context=context)

# Обработчик GET-запроса для страницы загрузки
@app.get("/upload/", response_class=HTMLResponse)
async def upload_page(request: Request):
    """Рендерит страницу upload.html с формой для загрузки изображения."""
    context = {
        "request": request,
    }
    return templates.TemplateResponse("upload.html", context=context)

# Обработчик POST-запроса для загрузки изображения
@app.post("/upload/", response_class=HTMLResponse)
async def upload_image(request: Request, image: UploadFile = File(...), description: str = Form(None)):
    """
    Обрабатывает загрузку изображения:
    - Проверяет формат файла (разрешены только .jpg, .png, .gif).
    - Проверяет размер файла (не более 5 МБ).
    - Проверяет, что файл является изображением.
    - Сохраняет оригинал и создает миниатюру.
    - Извлекает описание из формы и добавляет его в demo_images.
    - Возвращает страницу upload.html с сообщением об успехе или ошибке.
    """
    # Список разрешенных расширений файлов
    allowed_extensions = {'.jpg', '.png', '.gif'}
    # Максимальный размер файла (5 МБ в байтах)
    max_file_size = 5 * 1024 * 1024  # 5 MB

    # Проверка расширения файла
    file_extension = os.path.splitext(image.filename)[1].lower()
    if file_extension not in allowed_extensions:
        context = {
            "request": request,
            "message": "Разрешены только файлы формата .jpg, .png или .gif"
        }
        return templates.TemplateResponse("upload.html", context=context)

    # Проверка размера файла
    image.file.seek(0, os.SEEK_END)  # Перейти в конец файла для определения размера
    file_size = image.file.tell()  # Получить размер файла в байтах
    image.file.seek(0)  # Вернуться в начало файла для последующей обработки
    if file_size > max_file_size:
        context = {
            "request": request,
            "message": "Размер файла не должен превышать 5 МБ"
        }
        return templates.TemplateResponse("upload.html", context=context)

    # Проверка, что загруженный файл является изображением
    if not image.content_type.startswith("image/"):
        context = {
            "request": request,
            "message": "Файл должен быть изображением"
        }
        return templates.TemplateResponse("upload.html", context=context)

    # Генерация уникального имени файла с использованием UUID
    file_name = f"{uuid.uuid4()}{file_extension}"
    thumbnail_name = f"thumb_{file_name}"

    # Сохранение оригинального изображения в папку static/images
    image_path = os.path.join("static/images", file_name)
    with open(image_path, "wb") as f:
        f.write(await image.read())

    # Создание миниатюры (64x64 пикселя) с помощью Pillow
    thumbnail_path = os.path.join("static/thumbnails", thumbnail_name)
    with Image.open(image_path) as img:
        img.thumbnail((64, 64))
        img.save(thumbnail_path, quality=85)

    # Формирование данных для нового изображения, включая описание из формы
    new_image = {
        "id": len(demo_images) + 1,
        "url": f"/static/images/{file_name}",
        "thumbnail_url": f"/static/thumbnails/{thumbnail_name}",
        "description": description.strip() if description else "Без описания",
        "upload_date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    # Добавление нового изображения в список
    demo_images.append(new_image)

    # Подготовка контекста для рендеринга страницы с сообщением об успехе
    context = {
        "request": request,
        "message": "Изображение успешно загружено!"
    }
    return templates.TemplateResponse("upload.html", context=context)

# Запуск сервера с помощью uvicorn
if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)