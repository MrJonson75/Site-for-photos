import uvicorn
from fastapi import FastAPI, Request, File, UploadFile, HTTPException, Form
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
# Монтирование папки static для обслуживания статических файлов (CSS, изображения)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Создание директорий для хранения изображений и миниатюр
os.makedirs("static/images", exist_ok=True)
os.makedirs("static/thumbnails", exist_ok=True)

# Демонстрационный список фотографий (хранится в памяти для примера)
demo_images = [
    # {
    #     "id": 1,
    #     "url": "/static/images/photo1.jpg",
    #     "thumbnail_url": "/static/thumbnails/thumb1.jpg",
    #     "description": "Закат на пляже",
    #     "upload_date": datetime(2025, 6, 1, 12, 0).strftime("%Y-%m-%d %H:%M")
    # }

]

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
    """Рендерит страФорму для загрузки изображения."""
    context = {
        "request": request,
    }
    return templates.TemplateResponse("upload.html", context=context)

# Обработчик POST-запроса для загрузки изображения
@app.post("/upload/", response_class=HTMLResponse)
async def upload_image(request: Request, image: UploadFile = File(...), description: str = Form(None)):
    """
    Обрабатывает загрузку изображения:
    - Проверяет, что файл является изображением.
    - Сохраняет оригинал и создает миниатюру.
    - Добавляет информацию об изображении в demo_images.
    - Возвращает страницу upload.html с сообщением об успехе.
    """
    # Проверка, что загруженный файл является изображением
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Файл должен быть изображением")

    # Генерация уникального имени файла с использованием UUID
    file_extension = image.filename.split('.')[-1]
    file_name = f"{uuid.uuid4()}.{file_extension}"
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

    # Подготовка контекста для рендеринга страницы с сообщением
    context = {
        "request": request,
        "message": "Изображение успешно загружено!"
    }
    return templates.TemplateResponse("upload.html", context=context)

# Запуск сервера с помощью uvicorn
if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)