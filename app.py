import uvicorn
from fastapi import FastAPI, Request, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import os
from PIL import Image
import uuid
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Создание директорий для изображений и миниатюр, если они не существуют
os.makedirs("static/images", exist_ok=True)
os.makedirs("static/thumbnails", exist_ok=True)

# Демонстрационный список фотографий
demo_images = [
    {
        "id": 1,
        "url": "/static/images/photo1.jpg",
        "thumbnail_url": "/static/thumbnails/thumb1.jpg",
        "description": "Закат на пляже",
        "upload_date": datetime(2025, 6, 1, 12, 0).strftime("%Y-%m-%d %H:%M")
    },
    {
        "id": 2,
        "url": "/static/images/photo2.jpg",
        "thumbnail_url": "/static/thumbnails/thumb2.jpg",
        "description": "Горный пейзаж",
        "upload_date": datetime(2025, 6, 2, 14, 30).strftime("%Y-%m-%d %H:%M")
    },
    {
        "id": 3,
        "url": "/static/images/photo3.jpg",
        "thumbnail_url": "/static/thumbnails/thumb3.jpg",
        "description": "Цветочное поле",
        "upload_date": datetime(2025, 6, 3, 9, 15).strftime("%Y-%m-%d %H:%M")
    }
]


@app.get("/", response_class=HTMLResponse)          # Роут для главной страницы
async def index(request: Request):                       # Обработчик для главной страницы
    content = {
        "request": request,
    }
    return templates.TemplateResponse("index.html", context=content)

@app.get("/images/", response_class=HTMLResponse)
async def images(request: Request):
    context = {
        "request": request,
        "images": demo_images
    }
    return templates.TemplateResponse("images.html", context=context)

@app.get("/upload/", response_class=HTMLResponse)
async def upload_page(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("upload.html", context=context)

@app.post("/upload/", response_class=HTMLResponse)
async def upload_image(request: Request, image: UploadFile = File(...), description: str = None):
    # Проверка типа файла
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Файл должен быть изображением")

    # Генерация уникального имени файла
    file_extension = image.filename.split('.')[-1]
    file_name = f"{uuid.uuid4()}.{file_extension}"
    thumbnail_name = f"thumb_{file_name}"

    # Сохранение оригинального изображения
    image_path = os.path.join("static/images", file_name)
    with open(image_path, "wb") as f:
        f.write(await image.read())

    # Создание миниатюры
    thumbnail_path = os.path.join("static/thumbnails", thumbnail_name)
    with Image.open(image_path) as img:
        img.thumbnail((64, 64))  # Размер миниатюры соответствует image-card img
        img.save(thumbnail_path, quality=85)

    # Добавление в список
    new_image = {
        "id": len(demo_images) + 1,
        "url": f"/static/images/{file_name}",
        "thumbnail_url": f"/static/thumbnails/{thumbnail_name}",
        "description": description or "Без описания",
        "upload_date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    demo_images.append(new_image)

    # Рендеринг страницы с подтверждением
    context = {
        "request": request,
        "message": "Изображение успешно загружено!"
    }
    return templates.TemplateResponse("upload.html", context=context)


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)