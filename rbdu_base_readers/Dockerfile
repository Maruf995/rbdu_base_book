# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем системные зависимости для PostgreSQL
RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean

# Задаем рабочую директорию
WORKDIR /app

# Запрещаем Python писать .pyc файлы и буферизовать вывод (полезно для логов Docker)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Копируем зависимости и устанавливаем их
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app/