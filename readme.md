# Image Hosting / Хостинг изображений

Простое веб-приложение для загрузки, просмотра и скачивания изображений с помощью FastAPI и Jinja2. Теперь с поддержкой Docker и Nginx!

A simple web application for uploading, viewing, and downloading images using FastAPI and Jinja2. Now with Docker and Nginx support!

---

## 📁 Структура проекта / Project Structure

```
project/
├── Dockerfile                # Инструкция сборки образа приложения / Application Docker build file
├── docker-compose.yml        # Компоновка сервисов: backend и nginx / Docker Compose file: backend + nginx
├── nginx.conf                # Конфигурация nginx / nginx configuration
├── requirements.txt          # Зависимости Python / Python dependencies
├── app.py                    # Основное приложение FastAPI / FastAPI main app
├── static/
│   ├── images/               # Загруженные изображения / Uploaded images
│   ├── thumbnails/           # Миниатюры / Thumbnails
│   └── style.css             # Стили / CSS styles
├── templates/                # Шаблоны Jinja2 / Jinja2 templates
│   ├── base.html
│   ├── index.html
│   ├── upload.html
│   └── images.html
└── logs/                     # Логи сервера / Server logs
```

---

## 🚀 Запуск через Docker / Run via Docker

1. **Построить и запустить контейнеры** / Build and start containers:

```bash
docker-compose up --build
```

2. **Открыть в браузере** / Open in browser:

```
http://localhost/
```

---

## 🔧 Возможности / Features

- ✉️ **Главная страница (**``**)**

  - Добро пожаловать, кнопки перехода к загрузке и галерее.
  - Welcome screen with buttons to upload or view gallery.

- 📷 **Страница загрузки (**``**)**

  - Загрузка изображения с описанием, поддержка drag-and-drop.
  - Upload image with optional description and drag-and-drop.

- 🌐 **Галерея (**``**)**

  - Просмотр миниатюр, модальные окна, копирование URL, скачивание.
  - View thumbnails, modals, copy image URLs, download images.

- ✉️ **Логирование**

  - Все действия и ошибки записываются в `logs/app.log`.
  - Logs all actions and errors to `logs/app.log`.

---

## 🛠️ Технологии / Technologies

- **Backend**: FastAPI (Python)
- **Frontend**: Jinja2 + CSS + JavaScript
- **Image processing**: Pillow
- **Reverse proxy**: Nginx
- **Containerization**: Docker & Docker Compose

---

## 🔒 Безопасность и ограничения / Security & Limitations

- ❌ Без аутентификации и БД (всё в памяти).

- No authentication or database (in-memory only).

- ❌ Поддержка только `.jpg`, `.png`, `.gif` (до 5 MB).

- Supports only `.jpg`, `.png`, `.gif` (up to 5 MB).

- ❌ Логи не ротуются.

- No log rotation.

---

## 📃 Лицензия / License

© 2025 Image Hosting. All rights reserved.

