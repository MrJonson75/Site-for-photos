# Используем минимальный базовый образ Python
FROM python:3.12-slim

# Обновление системы и установка необходимых зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        libjpeg-dev \
        libpng-dev \
        zlib1g-dev \
        curl \
    && curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \
    && apt-get install -y nodejs \
    && apt-get purge -y curl \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Установка Python-зависимостей
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода приложения
COPY . .

# Указываем порт (для наглядности)
EXPOSE 8000

# Команда запуска
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]