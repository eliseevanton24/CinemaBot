#Импорт модуля requests, который используется для отправки HTTP запросов.
import requests
#Импорт класса BeautifulSoup из модуля bs4, который используется для парсинга HTML и извлечения данных.
from bs4 import BeautifulSoup
import csv

#Определение класса FilmParser, который содержит методы для извлечения информации о фильмах.
class FilmParser:
    #Конструктор класса, инициализирующий объект парсера с переданным URL.
    def __init__(self, url):
        self.url = url
        self.soup = self.get_soup()
#Метод для получения объекта BeautifulSoup из HTML страницы.
    def get_soup(self):
        r = requests.get(self.url)
        return BeautifulSoup(r.text, 'html.parser')

#Метод для извлечения названий фильмов.
    def extract_film_names(self):
        film_names = []
        film_elements = self.soup.find_all('div', class_='bigtext')
        for film_elem in film_elements:
            film_name = film_elem.find('a', class_='titlefilm').text
            film_names.append(film_name)
        return film_names

#Метод для извлечения рейтингов фильмов.
    def extract_film_ratings(self):
        film_rates = []
        rate_elements = self.soup.find_all('div', class_='zhanr_rating')
        for rate_elem in rate_elements:
            rating = rate_elem.find('span', class_='rating-big')
            if rating:
                film_rates.append(rating.text.strip())
        return film_rates
#Метод для извлечения жанров фильмов.
    def extract_film_genres(self):
        genre_of_film = []
        genre_elements = self.soup.find_all('div', class_='textgray')
        specific_genres = ['драма', 'боевик', 'криминал', 'военный', 'фэнтези', 'приключения',
                           'комедия', 'фантастика', 'триллер', 'биографический', 'детский', 'аниме', 'детектив', 'вестерн',
                           'мистика','мелодрама']
        for genre_elem in genre_elements:
            if 'Жанр' in genre_elem.text:
                genre = genre_elem.find('a')
                if genre and genre.text.strip().lower() in specific_genres:
                    genre_of_film.append(genre.text.strip())
        return genre_of_film
#Метод для извлечения ссылок на изображения постеров фильмов.
    def extract_film_images(self):
        film_images = []
        film_images_tags = self.soup.find_all('div', class_='rating_leftposter')
        for tag in film_images_tags:
            img_tag = tag.find('img')
            if img_tag:
                img_src = img_tag.get('src')
                film_images.append("https://www.kinonews.ru/" + img_src)
        return film_images
#Метод для извлечения ссылок на страницы фильмов.
    def extract_film_links(self):
        film_links = []
        film_link_tags = self.soup.find_all('div', class_='rating_leftposter')
        for tag in film_link_tags:
            link_tag = tag.find('a')
            if link_tag:
                link_src = link_tag.get('href')
                film_links.append("https://www.kinonews.ru/" + link_src)
        return film_links
#Метод для извлечения информации о фильмах с одной страницы
    def extract_info_from_page(self, url):
        self.url = url
        self.soup = self.get_soup()

        film_names = self.extract_film_names()
        film_ratings = self.extract_film_ratings()
        film_genres = self.extract_film_genres()
        film_images = self.extract_film_images()
        film_links = self.extract_film_links()

        films_info = []
        for name, rating, genres, image, link in zip(film_names, film_ratings, film_genres, film_images, film_links):
            film_info = {
                "Название": name,
                "Жанр": genres,
                "Картинка": image,
                "Ссылка": link,
                "Рейтинг": rating
            }
            films_info.append(film_info)

        return films_info
#Метод для извлечения информации о фильмах с нескольких страниц.
    def fetch_films_from_multiple_pages(self, num_pages):
        all_films_info = []
        for page_num in range(1, num_pages + 1):
            url = f"https://www.kinonews.ru/top250imdb_p{page_num}/"
            films_info = self.extract_info_from_page(url)
            all_films_info.extend(films_info)

        return all_films_info

#создание экземпляра парсера с передачей URL в качестве аргумента
url = "https://www.kinonews.ru/top250imdb/"
parser = FilmParser(url)
films_info = parser.fetch_films_from_multiple_pages(5)

# Вывод информации о фильмах в консоль
for film in films_info:
    print("Название:", film["Название"])
    print("Жанр:", film["Жанр"])
    print("Картинка:", film["Картинка"])
    print("Ссылка:", film["Ссылка"])
    print("Рейтинг:", film["Рейтинг"])
    print()

# Запись информации о фильмах в CSV файл
with open('films_info.csv', mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["Название", "Жанр", "Картинка", "Ссылка", "Рейтинг"])
    writer.writeheader()
    for film in films_info:
        writer.writerow(film)

print("Информация о фильмах успешно записана в файл films_info.csv")