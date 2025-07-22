# Из базового образа
FROM python:3.12-slim

# Установка пакетов, которые понадобятся, и удаление лишних, чтобы уменьшить размер образа
# Устанавливем libjpeg-dev, libpng-dev, zlib1g-dev - необходимы для работы с изображениями
# build-essential и python3-dev - для компиляции Python-пакетов
RUN apt-get update && \
    apt-get install -y --no-install-recommends \    # - уменьшает размер образа
    build-essential \
    python3-dev \
    libjpeg-dev \
    libpng-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/* \                # - очищает кеш пакетов

# Устанавливаем curl и nodejs - для работы с фронтендом
RUN apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y nodejs

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]