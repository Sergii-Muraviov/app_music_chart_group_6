from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('templates/index.html')
        elif pr_url.path == '/search':
            self.send_html_file('templates/search.html')
        elif pr_url.path.startswith('/static/'):
            self.send_static()
        else:
            self.send_html_file('templates/error.html')

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        try:
            with open(filename, 'rb') as file:
                self.wfile.write(file.read())
        except Exception as e:
            self.send_html_file('error.html', 404)

    def send_static(self):
        file_path = self.path[1:]
        mime_type, _ = mimetypes.guess_type(file_path)
        try:
            with open(file_path, 'rb') as file:
                self.send_response(200)
                self.send_header(
                    'Content-type',
                    mime_type or 'application/octet-stream'
                )
                self.end_headers()
                self.wfile.write(file.read())
        except Exception as e:
            self.send_html_file('error.html', 404)


def run(server_class=HTTPServer, handler_class=HttpHandler):
    port = 8080
    server_address = ('', port)
    local_server = server_class(server_address, handler_class)
    print(f"Сервер запущено на http://localhost:{port}")
    print("Натисніть Ctrl+C для зупинки сервера")
    try:
        local_server.serve_forever()
    except KeyboardInterrupt:
        print("\nЗупиняємо сервер ...")
    finally:
        local_server.server_close()
        print("Сервер успішно зупинено")


if __name__ == '__main__':
    run()