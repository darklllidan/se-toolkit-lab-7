# Используем легковесный образ Python
FROM python:3.14.2-slim

# Копируем бинарник uv из официального образа
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости (без dev-пакетов)
RUN uv sync --frozen --no-dev

# Копируем весь исходный код бота
COPY . .

# Запускаем бота через uv
CMD ["uv", "run", "bot.py"]
