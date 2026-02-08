# Модуль http.server - стандартний модуль Python
# використовується для створення простого HTTP-сервера
# - HTTPServer: Клас для запуску сервера
# - BaseHTTPRequestHandler: Клас, який обробляє запити клієнтів
from http.server import HTTPServer, BaseHTTPRequestHandler

# Модуль urllib.parse використовується для роботи з URL-адресами,
# розбиття на частини шляху запиту (self.path) для визначення необхідного маршруту
import urllib.parse

# Модуль mimetypes допомагає визначити MIME-тип файлу
# (Multipurpose Internet Mail Extensions) на основі розширення файлу:
# - .html → text/html
# - .css  → text/css
# - .jpg  → image/jpeg
# - .js   → application/javascript
#
# MIME-тип використовується для коректної передачі файлів клієнту
# через HTTP-заголовок Content-Type
import mimetypes


# Клас HttpHandler наслідує базовий клас BaseHTTPRequestHandler
# та перевизначає необхідні методи для обробки HTTP-запитів
class HttpHandler(BaseHTTPRequestHandler):

    # Метод do_GET використовується для обробки GET-запитів
    # (викликається автоматично, коли клієнт надсилає GET-запит)
    def do_GET(self):

        """
        Кожен URL складається з декількох частин
        (наприклад: https://www.example.com/search?name=query):

        - Схема (Scheme): https:// - протокол доступу до ресурсу
        - Домен (Domain): www.example.com - адреса сайту
        - Шлях (Path): /search - шлях до сторінки
        - Запит (Query): ?name=query - параметри, які передаються на сервер
        """

        # urllib.parse використовується для розбору URL на компоненти
        # - urlparse: Розбирає шлях на компоненти (`path`, `query`)
        # - self.path: Зберігає шлях із запиту (`/`, `/search`, або `/unknown`)
        # - pr_url: Об'єкт, який містить необхідні компоненти URL
        pr_url = urllib.parse.urlparse(self.path)

        # Перевірка маршруту для відповіді на запит клієнта
        # Якщо клієнт запитує '/', сервер повертає головну сторінку
        if pr_url.path == '/':
            self.send_html_file('templates/index.html')

        # Якщо клієнт запитує '/search', сервер повертає сторінку пошуку
        elif pr_url.path == '/search':
            self.send_html_file('templates/search.html')

        # Обробка статичних файлів (CSS, JS)
        # Всі шляхи, що починаються зі '/static/', обробляються окремим методом send_static()
        elif pr_url.path.startswith('/static/'):
            self.send_static()

        # Всі інші шляхи (/unknown, /test тощо) повертають сторінку помилки error.html
        else:
            self.send_html_file('templates/error.html')

    def send_html_file(self, filename, status=200):
        """
        Відправлення HTML-файлу з директорії templates
        """

        # Отримуємо HTTP-статус відповіді (200-OK, 404-Not Found)
        self.send_response(status)

        # Додаємо HTTP-заголовок Content-Type, який повідомляє браузеру,
        # що відповідь містить HTML
        self.send_header('Content-type', 'text/html')

        # Завершуємо формування HTTP-заголовків
        self.end_headers()

        try:
            # Відкриваємо HTML-файл в режимі читання байтів ('rb')
            # Байтовий режим необхідний для коректної передачі даних клієнту
            with open(filename, 'rb') as file:
                # Зчитує вміст файлу та відправляє його клієнту
                self.wfile.write(file.read())
        except Exception as e:
            # Якщо під час відкриття або читання файлу виникла помилка,
            # повертається сторінка помилки `error.html` з кодом 404
            self.send_html_file('error.html', 404)

    def send_static(self):
        """
        Відправка статичних файлів (CSS, JS)
        """

        # Визначаємо шлях до файлу
        # self.path містить шлях із запиту (наприклад: /static/style.css)
        # Щоб отримати реальний шлях до файлу в проєкті,
        # прибираємо початковий слеш (/)
        file_path = self.path[1:]

        # Визначаємо MIME-type файлу на основі його розширення
        # - .css → text/css
        # - .js  → application/javascript
        # - .jpg → image/jpeg
        # mimetypes.guess_type повертає кортеж: mime_type, encoding
        mime_type, _ = mimetypes.guess_type(file_path)

        try:
            # Відкриваємо статичний файл в режимі читання байтів ('rb')
            with open(file_path, 'rb') as file:
                # Відправляємо HTTP-статус відповіді
                self.send_response(200)
                # Додаємо заголовок Content-Type
                # Якщо MIME-тип не визначений - використовується application/octet-stream
                self.send_header(
                    'Content-type',
                    mime_type or 'application/octet-stream'
                )
                # Завершуємо формування HTTP-заголовків
                self.end_headers()
                # Зчитуємо вміст файлу та відправляємо його клієнту
                self.wfile.write(file.read())
        except Exception as e:
            # Якщо файл не знайдено або виникла інша помилка,
            # повертаємо сторінку помилки `error.html` з кодом 404
            self.send_html_file('error.html', 404)

def run(server_class=HTTPServer, handler_class=HttpHandler):
    """
    Функція запускає локальний HTTP-сервер
    - server_class: клас сервера
    - handler_class: клас-обробник HTTP-запитів
    """

    # Порт, на якому буде працювати сервер
    # 8080 - популярний порт для локальної розробки
    port = 8080

    # Адреса сервера:
    # '' означає, що сервер буде доступний на всіх мережевих інтерфейсах
    # (зазвичай через localhost)
    # Тобто, інші пристрої в поточній локальній мережі теж зможуть підключитись
    # Якщо замість '' вказати '127.0.0.1', тоді сервер буде доступний тільки на поточному комп'ютері
    server_address = ('', port)

    # Створюємо екземпляр HTTP-сервера
    # Передаємо адресу та клас-обробник запитів
    local_server = server_class(server_address, handler_class)

    # Інформаційні повідомлення для користувача
    print(f"Сервер запущено на http://localhost:{port}")
    print("Натисніть Ctrl+C для зупинки сервера")

    try:
        # Запускаємо нескінченний цикл обробки запитів
        # Сервер слухає вхідні HTTP-запити, доки його не зупинять вручну
        local_server.serve_forever()
    except KeyboardInterrupt:
        # Обробляємо ситуацію, коли користувач натискає Ctrl+C
        # (коректне завершення роботи сервера)
        print("\nЗупиняємо сервер ...")
    finally:
        # Закриваємо сокет сервера та звільняємо ресурси
        # Команда виконується завжди, навіть якщо сталася помилка
        local_server.server_close()
        print("Сервер успішно зупинено")


# Точка входу в програму гарантує, що сервер запускається тільки під час
# прямого запуску файлу, а не при його імпорті в інший модуль
if __name__ == '__main__':
    run()