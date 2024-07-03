CinemaBot
CinemaBot - это телеграм-бот, который предоставляет рекомендации по фильмам на основе жанров и случайного выбора. Этот бот использует данные из базы данных SQLite и позволяет пользователям взаимодействовать с ним через команды и кнопки в Telegram.

Возможности
Приветственное сообщение при запуске бота.
Выбор жанра для получения рекомендаций по фильмам.
Получение случайной рекомендации по фильму.
Данные хранятся в базе данных SQLite.
Асинхронные операции с использованием aiogram для работы с API Telegram.
Требования
Python 3.7+
Токен телеграм-бота, полученный от BotFather
База данных SQLite с информацией о фильмах
Установка
1. Клонируйте репозиторий:

git clone https://github.com/yourusername/yourrepository.git
cd yourrepository

2. Создайте и активируйте виртуальное окружение:

python3 -m venv venv
source venv/bin/activate

3. Установите зависимости:

pip install -r requirements.txt

4. Создайте файл .env и добавьте туда ваш токен:

echo "TOKEN=your_telegram_bot_token" > .env

Структура проекта

cinemabot.py: Основной файл для запуска бота.
handlers.py: Содержит обработчики команд и событий бота.
database.py: Обрабатывает подключения к базе данных и операции с ней.
config.py: Загружает конфигурацию из переменных окружения.
.gitignore: Указывает файлы и директории, которые нужно игнорировать в git.
requirements.txt: Список зависимостей проекта.

Использование

Запуск бота

Для запуска бота с использованием PM2:

pm2 start cinemabot.py --interpreter=python3

Для обеспечения автоматического перезапуска бота при перезагрузке системы:

pm2 startup
pm2 save

Для проверки статуса бота:

pm2 status

Команды бота

/start: Запускает бота и отображает приветственное сообщение с опциями выбора жанра или случайного фильма.

Кнопки Inline

Жанры: Отображает список жанров для выбора.

Рандомный фильм: Предоставляет случайную рекомендацию фильма.

Пример работы
Пользователь отправляет команду /start.
Бот отвечает приветственным сообщением и двумя кнопками: "Жанры" и "Рандомный фильм".
Пользователь нажимает на кнопку "Жанры".
Бот отображает список жанров.
Пользователь выбирает жанр.
Бот показывает рекомендацию фильма на основе выбранного жанра с кнопкой "Вперед" для просмотра других фильмов того же жанра.
Пользователь нажимает на кнопку "Рандомный фильм".
Бот показывает случайную рекомендацию фильма.
Вклад в проект
Сделайте форк репозитория.
Создайте новую ветку (git checkout -b feature-branch).
Сделайте коммиты ваших изменений (git commit -m 'Добавление новой функции').
Отправьте ваши изменения в репозиторий (git push origin feature-branch).
Создайте Pull Request для рассмотрения ваших изменений.

