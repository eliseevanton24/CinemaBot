import sqlite3
import csv

# Подключение к базе данных SQLite
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



#Функция поиска по названию фильма
def search_film(film_name):

    # Подключение к базе данных
    conn = sqlite3.connect('films.db')
    cursor = conn.cursor()

    # Выполнение запроса на поиск фильма
    cursor.execute("""SELECT * FROM films WHERE name LIKE ?""", ('%' + film_name + '%',))

    # Получение результата запроса
    result = cursor.fetchone()

    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()

    # Возврат словаря с информацией о фильме, если он найден
    if result:
        return {
            "id": result[0],
            "name": result[1],
            "genre": result[2],
            "image": result[3],
            "link": result[4],
            "rating": result[5]
        }

    # Возврат None, если фильм не найден
    else:
        return None


# Ввод названия фильма пользователем
film_name = input("Введите название фильма для поиска: ")

# Поиск фильма в базе данных
film_info = search_film(film_name)

# Вывод информации о фильме, если он найден
if film_info:
    print("Информация о фильме:")
    print(f"Название: {film_info['name']}")
    print(f"Жанр: {film_info['genre']}")
    print(f"Картинка: {film_info['image']}")
    print(f"Ссылка: {film_info['link']}")
    print(f"Рейтинг: {film_info['rating']}")
else:
    print("Фильм с таким названием не найден.")

#Функция поиска по жанрам фильмов
def search_films_by_genre(genre):

    # Подключение к базе данных
    conn = sqlite3.connect('films.db')
    cursor = conn.cursor()

    # Выполнение запроса на поиск фильмов по жанру
    cursor.execute("""SELECT * FROM films WHERE genre LIKE ?""", ('%' + genre + '%',))

    # Получение результата запроса
    results = cursor.fetchall()

    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()

    # Возврат списка словарей с информацией о фильмах
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


# Ввод жанра пользователем
genre = input("Введите жанр фильмов для поиска: ")

# Поиск фильмов в базе данных по жанру
films = search_films_by_genre(genre)

# Создание множества для хранения уже выведенных названий фильмов
seen_film_names = set()

# Вывод информации о фильмах, если они найдены
if films:
    print("Найденные фильмы:")
    for film in films:
        if film['name'] not in seen_film_names:
            print(f"Название: {film['name']}")
            print(f"Ссылка: {film['link']}")
            print(f"Рейтинг: {film['rating']}")
            print()
            seen_film_names.add(film['name'])
else:
    print("Фильмов с таким жанром не найдено.")
