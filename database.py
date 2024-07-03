import sqlite3
import csv

# Подключение к базе данных SQLite
def init_db():
    conn = sqlite3.connect('films.db')
    cursor = conn.cursor()

    # Создание таблицы films
    cursor.execute('''CREATE TABLE IF NOT EXISTS films (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    genre TEXT,
                    image TEXT,
                    link TEXT,
                    rating REAL
                )''')

    # Открытие CSV файла для чтения
    with open('films_info.csv', mode='r') as csv_file:
        # Чтение данных из CSV файла по строкам
        csv_reader = csv.DictReader(csv_file)

        # Вставка данных в таблицу films
        for row in csv_reader:
            cursor.execute("""INSERT INTO films (name, genre, image, link, rating)
                                    VALUES (?, ?, ?, ?, ?)""",
                                    (row['Название'], row['Жанр'], row['Картинка'], row['Ссылка'], row['Рейтинг']))

    # Сохранение изменений в базе данных
    conn.commit()

    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()

    print("Данные о фильмах успешно импортированы в базу данных SQLite")

# Подключение к базе данных
def get_db_connection():
    conn = sqlite3.connect('films.db')
    return conn

# Получение случайного фильма
def get_random_film():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM films ORDER BY RANDOM() LIMIT 1")
    film = cursor.fetchone()
    cursor.close()
    conn.close()
    return film

# Получение списка жанров
def get_genres():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT genre FROM films")
    genres = cursor.fetchall()
    cursor.close()
    conn.close()
    return [genre[0] for genre in genres]

# Функция поиска по жанрам фильмов
def search_films_by_genre(genre):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM films WHERE genre LIKE ?""", ('%' + genre + '%',))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return [
        {
            "id": result[0],
            "name": result[1],
            "genre": result[2],
            "image": result[3],
            "link": result[4],
            "rating": result[5]
        }
        for result in results
    ]
