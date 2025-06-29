FROM python:3.11-slim

# Создаём системного пользователя „django“
RUN useradd -ms /bin/bash django

WORKDIR /app
COPY requirements.txt .

# Ставим зависимости без кеша, разворачиваем wheel-ы
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем исходники проекта
COPY . .

# Меняем владельца, чтобы процесс шёл не под root
RUN chown -R django:django /app
USER django

# Команда по умолчанию:
# 1. применяем миграции (если не применены)
# 2. запускаем дев-сервер на 0.0.0.0:8000
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
