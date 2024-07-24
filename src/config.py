import os
from dotenv import load_dotenv

# Загрузить переменные из .env-файла
load_dotenv()

# Получить значение переменной из .env-файла
BOT_TOKEN = os.getenv('BOT_TOKEN')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')

