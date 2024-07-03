from dotenv import load_dotenv
import os

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение значения переменной TOKEN из окружения
TOKEN = os.getenv("TOKEN")
