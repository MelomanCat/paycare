FROM python:3.9-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        libffi-dev \
        libssl-dev \
        && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Сначала копируем и устанавливаем зависимости
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# ПОТОМ копируем ВСЕ остальные файлы проекта
COPY . .

# Проверяем, что скопировалось
RUN echo "=== Contents of /app ===" && ls -la
RUN echo "=== Contents of /app/tests ===" && ls -la tests/ || echo "No tests directory!"

ENTRYPOINT ["python3"]