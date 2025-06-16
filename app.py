import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)          # Роут для главной страницы
async def index(request: Request):                       # Обработчик для главной страницы
    content = {
        "request": request,
    }
    return templates.TemplateResponse("index.html", context=content)

@app.get("/images/", response_class=HTMLResponse)          # Роут для страницы с картинками
async def images(request: Request):                      # Обработчик для страницы с картинками
    content = {
        "request": request,
    }
    return templates.TemplateResponse("images.html", context=content)

@app.get("/upload/", response_class=HTMLResponse)       # Роут для страницы с загрузкой картинок
async def upload(request: Request):     # Обработчик для страницы с загрузкой картинок
    content = {
        "request": request,
    }
    return templates.TemplateResponse("upload.html", context=content)



if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)