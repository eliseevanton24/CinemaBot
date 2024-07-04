import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, CallbackQuery
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from handlers import command_start_handler, choose_genre, show_film_by_genre, send_random_film, GenreCallbackData, RandomCallbackData
from config import TOKEN  # Импортируем TOKEN из config.py

# Инициализация экземпляра Bot
session = AiohttpSession()
bot = Bot(token=TOKEN, session=session)
bot._default_parse_mode = ParseMode.HTML

# Инициализация диспетчера и маршрутизатора
dp = Dispatcher()
router = Router()

# Регистрация обработчиков сообщений
router.message.register(command_start_handler, CommandStart())

# Регистрация обработчиков с фильтрацией callback data вручную
@router.callback_query(lambda c: c.data == "choose_genre")
async def process_choose_genre(callback_query: CallbackQuery):
    logging.info("Choosing genre")  # Отладочное сообщение
    await choose_genre(callback_query)

# Регистрация обработчика с использованием GenreCallbackData
@router.callback_query(GenreCallbackData.filter())
async def process_genre_callback(callback_query: CallbackQuery, callback_data: GenreCallbackData):
    await show_film_by_genre(callback_query, callback_data)

# Регистрация обработчика с использованием RandomCallbackData
@router.callback_query(RandomCallbackData.filter())
async def process_random_callback(callback_query: CallbackQuery, callback_data: RandomCallbackData):
    await send_random_film(callback_query, callback_data)

# Включение маршрутизатора в диспетчер
dp.include_router(router)

# Включение логирования
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# Основная функция для запуска бота
async def main():
    await dp.start_polling(bot)

# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())
