import http.server
from backend import my_handler


with http.server.HTTPServer(("192.168.0.18", 8000), my_handler.MyHandler) as httpd:
    httpd.serve_forever()


