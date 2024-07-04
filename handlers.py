from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters.callback_data import CallbackData
import database
import logging

# Фабрика callback data для жанров
class GenreCallbackData(CallbackData, prefix="genre"):
    action: str
    name: str
    index: int = 0

# Фабрика callback data для случайных фильмов
class RandomCallbackData(CallbackData, prefix="random"):
    action: str

# Обработчик команды /start
async def command_start_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Жанры", callback_data="choose_genre")],
        [InlineKeyboardButton(text="Рандомный фильм", callback_data=RandomCallbackData(action="get").pack())]
    ])
    await message.answer(f"Добро пожаловать, {message.from_user.first_name}! Выберите опцию:", reply_markup=keyboard)
    await message.delete()  # Удаление команды /start после использования

# Обработчик нажатия кнопки "Жанры"
async def choose_genre(callback_query: CallbackQuery):
    genres = database.get_genres()
    buttons = [
        InlineKeyboardButton(text=genre, callback_data=GenreCallbackData(action="show", name=genre).pack())
        for genre in genres
    ]

    # Создаем клавиатуру с кнопками в два ряда
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [buttons[i], buttons[i+1]] if i+1 < len(buttons) else [buttons[i]]
        for i in range(0, len(buttons), 2)
    ])

    await callback_query.message.answer("Выберите жанр:", reply_markup=keyboard)
    await callback_query.message.delete()

# Обработчик выбора фильма по жанру
async def show_film_by_genre(callback_query: CallbackQuery, callback_data: GenreCallbackData):
    genre = callback_data.name
    index = callback_data.index
    logging.info(f"Callback data index: {index}")  # Отладочное сообщение
    films = sorted(database.search_films_by_genre(genre), key=lambda x: x['rating'], reverse=True)
    logging.info(f"Films in genre '{genre}': {[film['name'] for film in films]}")  # Отладочное сообщение
    if index < len(films):
        film = films[index]
        logging.info(f"Showing film at index {index}: {film['name']} with rating {film['rating']}")  # Отладочное сообщение
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Вперед", callback_data=GenreCallbackData(action="show", name=genre, index=index+1).pack())]
        ])
        try:
            await callback_query.message.edit_text(
                text=f"Фильм: {film['name']}\nЖанр: {film['genre']}\nРейтинг: {film['rating']}\nСсылка: {film['link']}",
                reply_markup=keyboard
            )
            logging.info(f"Message sent successfully at index {index}")  # Отладочное сообщение
        except Exception as e:
            logging.error(f"Error sending message: {e}")  # Отладочное сообщение
    else:
        try:
            await callback_query.message.edit_text("Больше фильмов в этом жанре нет.")
            logging.info("No more films in this genre")  # Отладочное сообщение
        except Exception as e:
            logging.error(f"Error sending message: {e}")  # Отладочное сообщение

# Обработчик случайного фильма
async def send_random_film(callback_query: CallbackQuery, callback_data: RandomCallbackData):
    film = database.get_random_film()
    if film:
        await callback_query.message.answer(
            text=f"Случайный фильм: {film[1]}\nЖанр: {film[2]}\nРейтинг: {film[5]}\nСсылка: {film[4]}"
        )
        await callback_query.message.delete()
    else:
        await callback_query.message.answer("Фильмы не найдены.")
        await callback_query.message.delete()
