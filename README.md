## Телеграм-бот - финансовый советник
<hr>
aiogram 3.13.1, SQLite3, request, Python 3.9.6

**Разработка бота продолжается**

Для локального запуска необходимо подготовить файл .env с токенами проекта. Например, вида:

```
BOT_TOKEN=<токен бота от BotFather>
BOT_ADMINS=<telegram_id пользователя с правами админа>
BOT_DB_PATH=<Путь к БД>
DB_LOGIN=<Логин учетной записи для работы с БД>
DB_PASSWORD=<Пароль учетной записи для работы с БД>
YANDEX_OAUTH_TOKEN = <Токен учетной записи Яндекс>
YANDEX_FOLDER_ID = 'ID подключенного сервиса YnandexCloud'
YANDEX_AIM_TOKEN = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
YGPT_API_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
```
настроить виртуальную среду (опционально). Создать:

`python -m venv .venv`

и активировать:

`
venv\Scripts\activate.bat для Windows`

`source venv/bin/activate - для Linux и MacOS.`

Также среду и версию интерпретатора можно настроить с помощью IDE

Установить зависимости можно с помощью файла requirements.txt и скрипта:

`pip3 install -r requirements.txt`

Файл requirements.txt может иметь следующий вид:

```
aiogram
APScheduler
python-decouple
requests
asyncio
pydantic-settings
yfinance
```

Каталог для данных, БД и таблицы создаются автоматически при первом запуске

Реализованы 
* сервис авторизации
* сервис взаимодействия с Московской биржей
* Подключен YandexGPT
* интеграция с SQLite, MOEX, YandexGPT, CBR

В разработке интеграция с CBR, суммаризация новостей, криптоинфо