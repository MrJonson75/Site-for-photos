# Веб-приложение для хостинга изображений  
**Image Hosting Web Application**

Простое веб-приложение для загрузки, хранения и просмотра изображений, построенное на FastAPI с использованием Docker, Nginx, PostgreSQL и pgAdmin.  
*This is a simple web application for uploading, storing, and viewing images, built using FastAPI with Docker, Nginx, PostgreSQL, and pgAdmin.*

## Возможности  
**Features**

- **Загрузка изображений**: Поддержка форматов `.jpg`, `.png`, `.gif` с максимальным размером 5 МБ.  
  *Uploading images*: Supports `.jpg`, `.png`, `.gif` formats with a maximum size of 5 MB.  
- **Создание миниатюр**: Автоматическое создание миниатюр размером 64x64 пикселя.  
  *Creating thumbnails*: Automatically generates thumbnails of 64x64 pixels.  
- **Галерея изображений**: Просмотр загруженных изображений с возможностью копирования URL и скачивания.  
  *Image gallery*: View uploaded images with options to copy URLs and download.  
- **Хранение данных**: Метаданные изображений (URL, описание, дата загрузки) сохраняются в PostgreSQL.  
  *Data storage*: Image metadata (URL, description, upload date) is stored in PostgreSQL.  
- **Логирование**: Все действия (доступ к страницам, загрузка, ошибки) записываются в лог-файл с ротацией (до 5 файлов по 5 МБ).  
  *Logging*: All actions (page access, uploads, errors) are logged with rotation (up to 5 files of 5 MB each).  
- **Администрирование базы данных**: Управление PostgreSQL через pgAdmin.  
  *Database administration*: Manage PostgreSQL via pgAdmin.

## Технологии  
**Technologies**

- **Backend**: FastAPI (`0.116.0`) для обработки запросов и рендеринга шаблонов (Jinja2).  
  *Backend*: FastAPI (`0.116.0`) for handling requests and rendering templates (Jinja2).  
- **Frontend**: HTML, CSS, JavaScript с поддержкой drag-and-drop для загрузки.  
  *Frontend*: HTML, CSS, JavaScript with drag-and-drop support for uploads.  
- **База данных**: PostgreSQL (`17`) для хранения метаданных изображений.  
  *Database*: PostgreSQL (`17`) for storing image metadata.  
- **Обработка изображений**: Pillow (`11.3.0`) для создания миниатюр.  
  *Image processing*: Pillow (`11.3.0`) for creating thumbnails.  
- **Прокси**: Nginx (`latest`) для маршрутизации запросов и обслуживания статических файлов.  
  *Proxy*: Nginx (`latest`) for request routing and serving static files.  
- **Контейнеризация**: Docker и Docker Compose для упрощения развертывания.  
  *Containerization*: Docker and Docker Compose for easy deployment.  
- **Логирование**: Реализовано через `RotatingFileHandler` в Python.  
  *Logging*: Implemented using `RotatingFileHandler` in Python.  
- **pgAdmin**: Интерфейс для управления PostgreSQL.  
  *pgAdmin*: Interface for managing PostgreSQL.

## Требования  
**Requirements**

- Docker и Docker Compose.  
  *Docker and Docker Compose.*  
- Python 3.12 (для локального тестирования вне Docker).  
  *Python 3.12 (for local testing outside Docker).*  
- Node.js (опционально, для дополнительных скриптов, если используются).  
  *Node.js (optional, for additional scripts if used).*

## Структура проекта  
**Project Structure**

- **`Dockerfile`**: Описание сборки образа для FastAPI-приложения.  
  *`Dockerfile`*: Defines the build for the FastAPI application image.  
- **`docker-compose.yml`**: Конфигурация сервисов (FastAPI, Nginx, PostgreSQL, pgAdmin).  
  *`docker-compose.yml`*: Configuration for services (FastAPI, Nginx, PostgreSQL, pgAdmin).  
- **`nginx.conf`**: Конфигурация Nginx для маршрутизации запросов.  
  *`nginx.conf`*: Nginx configuration for request routing.  
- **`app.py`**: Основной файл FastAPI-приложения с маршрутами (`/`, `/images/`, `/upload/`).  
  *`app.py`*: Main FastAPI application file with routes (`/`, `/images/`, `/upload/`).  
- **`utils.py`**: Функции для подключения к PostgreSQL и создания таблицы `photos`.  
  *`utils.py`*: Functions for connecting to PostgreSQL and creating the `photos` table.  
- **`.env`**: Переменные окружения для PostgreSQL и pgAdmin.  
  *`.env`*: Environment variables for PostgreSQL and pgAdmin.  
- **`static/`**: Директория для хранения изображений, миниатюр и статических файлов (CSS, JS).  
  *`static/`*: Directory for storing images, thumbnails, and static files (CSS, JS).  
- **`templates/`**: HTML-шаблоны для рендеринга страниц.  
  *`templates/`*: HTML templates for rendering pages.  
- **`logs/`**: Директория для логов приложения.  
  *`logs/`*: Directory for application logs.  
- **`pgadmin_data/`**, **`pgadmin_config/`**, **`pgadmin_import/`**: Тома для pgAdmin.  
  *`pgadmin_data/`*, *`pgadmin_config/`*, *`pgadmin_import/`*: Volumes for pgAdmin.  
- **`postgres_data/`**: Том для данных PostgreSQL.  
  *`postgres_data/`*: Volume for PostgreSQL data.

## Установка и запуск  
**Installation and Setup**

1. **Клонируйте репозиторий**:  
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```
   *Clone the repository*:  
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Создайте файл `.env`**:  
   Скопируйте пример `.env.example` (если есть) или создайте `.env` в корне проекта:  
   ```env
   P_USER=postgres
   P_PASSWORD=your_strong_password_123
   P_DB=postgres
   PGADMIN_DEFAULT_EMAIL=admin@example.com
   PGADMIN_DEFAULT_PASSWORD=your_strong_password_456
   ```
   Замените `your_strong_password_123` и `your_strong_password_456` на сложные пароли.  
   *Create the `.env` file*:  
   Copy the example `.env.example` (if available) or create `.env` in the project root:  
   ```env
   P_USER=postgres
   P_PASSWORD=your_strong_password_123
   P_DB=postgres
   PGADMIN_DEFAULT_EMAIL=admin@example.com
   PGADMIN_DEFAULT_PASSWORD=your_strong_password_456
   ```
   Replace `your_strong_password_123` and `your_strong_password_456` with strong passwords.

3. **Запустите контейнеры**:  
   ```bash
   docker-compose up --build
   ```
   *Start the containers*:  
   ```bash
   docker-compose up --build
   ```

4. **Доступ к приложению**:  
   - Веб-приложение: `http://localhost/`  
   - Галерея: `http://localhost/images/`  
   - Страница загрузки: `http://localhost/upload/`  
   - pgAdmin: `http://localhost:5050` (прямой доступ) или `http://localhost/pgadmin/` (через Nginx)  
   *Access the application*:  
   - Web application: `http://localhost/`  
   - Gallery: `http://localhost/images/`  
   - Upload page: `http://localhost/upload/`  
   - pgAdmin: `http://localhost:5050` (direct access) or `http://localhost/pgadmin/` (via Nginx)

5. **Вход в pgAdmin**:  
   - URL: `http://localhost:5050` или `http://localhost/pgadmin/`.  
   - Email: `admin@example.com` (или значение `PGADMIN_DEFAULT_EMAIL` из `.env`).  
   - Пароль: `your_strong_password_456` (или значение `PGADMIN_DEFAULT_PASSWORD` из `.env`).  
   - Подключение к базе данных:  
     - Host: `db`  
     - Port: `5432`  
     - Username: `postgres` (или `P_USER`)  
     - Password: `your_strong_password_123` (или `P_PASSWORD`)  
     - Database: `postgres` (или `P_DB`)  
   *Log in to pgAdmin*:  
   - URL: `http://localhost:5050` or `http://localhost/pgadmin/`.  
   - Email: `admin@example.com` (or `PGADMIN_DEFAULT_EMAIL` from `.env`).  
   - Password: `your_strong_password_456` (or `PGADMIN_DEFAULT_PASSWORD` from `.env`).  
   - Database connection:  
     - Host: `db`  
     - Port: `5432`  
     - Username: `postgres` (or `P_USER`)  
     - Password: `your_strong_password_123` (or `P_PASSWORD`)  
     - Database: `postgres` (or `P_DB`)

## Использование  
**Usage**

- **Загрузка изображений**:  
  1. Перейдите на `http://localhost/upload/`.  
  2. Выберите файл (`.jpg`, `.png`, `.gif`, до 5 МБ) или используйте drag-and-drop.  
  3. Добавьте описание (опционально) и нажмите "Загрузить".  
  4. После успешной загрузки вы получите подтверждение.  
  *Uploading images*:  
  1. Go to `http://localhost/upload/`.  
  2. Select a file (`.jpg`, `.png`, `.gif`, up to 5 MB) or use drag-and-drop.  
  3. Add a description (optional) and click "Upload".  
  4. You will receive a confirmation upon successful upload.

- **Просмотр галереи**:  
  1. Перейдите на `http://localhost/images/`.  
  2. Просматривайте миниатюры, кликайте для открытия в модальном окне.  
  3. Копируйте URL или скачивайте изображения.  
  *Viewing the gallery*:  
  1. Go to `http://localhost/images/`.  
  2. Browse thumbnails, click to open in a modal window.  
  3. Copy URLs or download images.

- **Управление базой данных**:  
  1. Войдите в pgAdmin по адресу `http://localhost:5050` или `http://localhost/pgadmin/`.  
  2. Добавьте сервер с параметрами из `.env`.  
  3. Просмотрите таблицу `photos` для проверки метаданных загруженных изображений.  
  *Managing the database*:  
  1. Log in to pgAdmin at `http://localhost:5050` or `http://localhost/pgadmin/`.  
  2. Add a server using parameters from `.env`.  
  3. Check the `photos` table to verify metadata of uploaded images.

## Ограничения  
**Limitations**

- **Форматы файлов**: Поддерживаются только `.jpg`, `.png`, `.gif`.  
  *File formats*: Only `.jpg`, `.png`, `.gif` are supported.  
- **Размер файлов**: Максимум 5 МБ.  
  *File size*: Maximum 5 MB.  
- **Аутентификация**: Отсутствует в текущей версии, любой пользователь может загружать и просматривать изображения.  
  *Authentication*: Not implemented in the current version; any user can upload and view images.  
- **Логи**: Хранятся в `logs/app.log` с ротацией (до 5 файлов по 5 МБ).  
  *Logs*: Stored in `logs/app.log` with rotation (up to 5 files of 5 MB each).


## Безопасность  
**Security**

- Используйте сложные пароли для `P_PASSWORD` и `PGADMIN_DEFAULT_PASSWORD` в `.env`.  
  *Use strong passwords for `P_PASSWORD` and `PGADMIN_DEFAULT_PASSWORD` in `.env`.


## Будущие улучшения  
**Future Improvements**

- Добавить аутентификацию пользователей (например, через OAuth2 или JWT).  
  *Add user authentication (e.g., via OAuth2 or JWT).  
- Внедрить пагинацию в галерее для обработки большого количества изображений.  
  *Implement pagination in the gallery for handling large numbers of images.  
- Добавить возможность удаления изображений через интерфейс.  
  *Add the ability to delete images via the interface.  
- Реализовать сжатие изображений для экономии места.  
  *Implement image compression to save storage space.  
- Добавить мониторинг (Prometheus + Grafana) для отслеживания производительности.  
  *Add monitoring (Prometheus + Grafana) to track performance.