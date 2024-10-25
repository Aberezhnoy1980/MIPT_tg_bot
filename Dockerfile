# Установка Python из официального базового образа
FROM python:3.9.6
# Установка рабочей директории внутри будущего контейнера
WORKDIR /app
# Копирование всех файлов приложения в контейнер
COPY . /app
RUN pip3 install --no-cache-dir -r requirements.txt
# Экспорт порта, на котором будет работать приложение
EXPOSE 8000
# Запуск тестового Python-приложения
CMD ["python3", "aiogram_run.py"]