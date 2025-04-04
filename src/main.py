from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import os
from constants import TEMPLATES_DIR, DEFAULT_PORT


class WebStoreHandler(BaseHTTPRequestHandler):
    def _get_template_path(self, path):
        # Явное сопоставление путей с файлами
        routes = {
            '/': 'index.html',
            '/index.html': 'index.html',
            '/catalogue': 'catalogue.html',
            '/catalogue.html': 'catalogue.html',
            '/category-1': 'category-1.html',
            '/category-1.html': 'category-1.html',
            '/contacts': 'contacts.html',
            '/contacts.html': 'contacts.html'
        }
        return routes.get(path)

    def do_GET(self):
        try:
            path = urlparse(self.path).path
            template_file = self._get_template_path(path)

            if not template_file:
                self.send_error(404, "Page not found")
                return

            filepath = os.path.join(TEMPLATES_DIR, template_file)

            if not os.path.exists(filepath):
                self.send_error(404, f"Template {template_file} not found")
                return

            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))

        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")


def run(server_class=HTTPServer, handler_class=WebStoreHandler, port=DEFAULT_PORT):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Сервер запущен на порту {port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()


