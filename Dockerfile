# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем необходимые системные зависимости
RUN apt-get update && apt-get install -y gcc libpq-dev

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл requirements.txt в контейнер
COPY requirements.txt /app/requirements.txt

# Копируем остальные файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r /app/requirements.txt

# Открываем порт для Flask-приложения
EXPOSE 5000

# Запуск Flask-приложения
CMD ["flask", "run", "--host=0.0.0.0"]
