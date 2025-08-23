# 🖼️ Веб-приложение для хостинга изображений

**Image Hosting Web Application**

Простое веб-приложение для загрузки, хранения и просмотра изображений,
построенное на **FastAPI** с использованием **Docker**, **Nginx**,
**PostgreSQL** и **pgAdmin**.\
*A simple web application for uploading, storing, and viewing images,
built with FastAPI, Docker, Nginx, PostgreSQL, and pgAdmin.*

------------------------------------------------------------------------

## 🚀 Возможности \| Features

-   📤 **Загрузка изображений**: Поддержка `.jpg`, `.png`, `.gif`
    (максимум 5 МБ).\
    *Uploading images: Supports `.jpg`, `.png`, `.gif` (max size 5 MB).*

-   🖼️ **Создание миниатюр**: Автоматическая генерация 64×64 px.\
    *Thumbnails: Auto-generated (64×64 px).*

-   📑 **Галерея изображений**: Просмотр с возможностью копирования
    ссылки и скачивания.\
    *Image gallery: View, copy link, and download.*

-   🗑️ **Удаление изображений**: Удобная кнопка удаления прямо в
    галерее.\
    *Delete images: Simple delete button in gallery.*

-   📄 **Пагинация галереи**: Постраничный просмотр изображений (с
    навигацией «Предыдущая / Следующая»).\
    *Gallery pagination: Browse images with page navigation.*

-   🗃️ **Хранение данных**: PostgreSQL для метаданных (URL, описание,
    дата загрузки).\
    *Data storage: PostgreSQL stores metadata (URL, description, upload
    date).*

-   📝 **Логирование**: Все действия сохраняются с ротацией логов.\
    *Logging: Rotating logs for actions and errors.*

-   ⚙️ **Администрирование**: Управление базой через pgAdmin.\
    *Administration: Manage DB with pgAdmin.*

------------------------------------------------------------------------

## 🛠️ Технологии \| Technologies

-   **Backend**: FastAPI + Jinja2\
-   **Frontend**: HTML, CSS, JavaScript\
-   **Database**: PostgreSQL 17\
-   **Image processing**: Pillow (thumbnails)\
-   **Proxy**: Nginx\
-   **Containerization**: Docker, Docker Compose\
-   **DB Admin**: pgAdmin

------------------------------------------------------------------------

## 📂 Структура проекта \| Project Structure

-   `app.py` --- маршруты `/`, `/images/`, `/upload/`, `/delete/{id}`.\
    *`app.py` --- routes `/`, `/images/`, `/upload/`, `/delete/{id}`.*

-   `templates/` --- HTML-шаблоны (галерея, загрузка).\
    *`templates/` --- HTML templates (gallery, upload).*

-   `static/` --- CSS, JS, изображения и миниатюры.\
    *`static/` --- CSS, JS, images, thumbnails.*

-   `utils/` --- функции для работы с PostgreSQL.\
    *`utils/` --- functions for PostgreSQL.*

-   `docker-compose.yml`, `Dockerfile`, `nginx.conf` --- контейнеризация
    и прокси.\
    *`docker-compose.yml`, `Dockerfile`, `nginx.conf` ---
    containerization and proxy.*

-   `logs/` --- логи с ротацией.\
    *`logs/` --- rotating logs.*

-   `postgres_data/`, `pgadmin_data/` --- тома БД и pgAdmin.\
    *`postgres_data/`, `pgadmin_data/` --- DB and pgAdmin volumes.*

------------------------------------------------------------------------

## ⚡ Установка и запуск \| Installation and Setup

1.  Клонировать репозиторий \| Clone the repository

    ``` bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  Создать `.env` \| Create `.env`

    ``` env
    P_USER=postgres
    P_PASSWORD=your_strong_password_123
    P_DB=postgres
    PGADMIN_DEFAULT_EMAIL=admin@example.com
    PGADMIN_DEFAULT_PASSWORD=your_strong_password_456
    ```

3.  Запуск контейнеров \| Run containers

    ``` bash
    docker-compose up --build
    ```

4.  Доступ \| Access

    -   Веб-приложение: <http://localhost/>\
    -   Галерея: <http://localhost/images/>\
    -   Загрузка: <http://localhost/upload/>\
    -   pgAdmin: <http://localhost/pgadmin/>\
        *Web app: <http://localhost/>, Gallery: `/images/`, Upload:
        `/upload/`, pgAdmin: `/pgadmin/`*

------------------------------------------------------------------------

## 🎯 Использование \| Usage

-   **Загрузка \| Upload**\
    Перейдите на `/upload/`, выберите файл или перетащите его, добавьте
    описание.\
    *Go to `/upload/`, choose or drag-and-drop file, add description.*

-   **Просмотр \| Viewing**\
    Перейдите в `/images/`, откройте миниатюру, копируйте ссылку или
    скачивайте.\
    *Go to `/images/`, open thumbnail, copy link or download.*

-   **Удаление \| Delete**\
    В галерее нажмите кнопку **Удалить** → картинка исчезнет.\
    *Click **Delete** in gallery → image will be removed.*

-   **Пагинация \| Pagination**\
    Внизу страницы переключайтесь между страницами.\
    *Navigate pages with "Previous / Next".*

------------------------------------------------------------------------

## 🔒 Безопасность \| Security

-   Используйте сложные пароли в `.env`.\
-   *Use strong passwords in `.env`.*\
-   Ограничьте доступ к pgAdmin.\
-   *Restrict pgAdmin access.*

------------------------------------------------------------------------

## 📌 Будущие улучшения \| Future Improvements

-   🔑 Авторизация пользователей (OAuth2 / JWT).\
    *User authentication (OAuth2 / JWT).*

-   📦 Сжатие изображений для экономии места.\
    *Image compression to save space.*

