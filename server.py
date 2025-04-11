import http.server
from backend import my_handler


with http.server.HTTPServer(("127.0.0.1", 8000), my_handler.MyHandler) as httpd:
    httpd.serve_forever()


