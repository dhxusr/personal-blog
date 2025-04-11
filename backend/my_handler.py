"""
My http Handler class for my personal blog

- MyHandler
"""

from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs
from backend.sub_functions import create_article, delete_article, edit_article, edit_page, show_article
from pathlib import Path
import base64


USER = "dhx"
PASSWD = "admin"

MAIN_PATH = Path("pages")
ADMIN_PATH = MAIN_PATH / "admin"
ARTICLES_PATH = MAIN_PATH / "articles"
GUEST_PATH = MAIN_PATH / "index.html"

#http status code
OK = 200
NOT_FOUND = 404
REDIRECTED = 303
HEADER = ["Content-type", "text/html"]


class MyHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        status = OK
        header = HEADER

        # checking if the user is athenticated
        authenticated = self.authenticated(self.headers["Authorization"])
        path = Path(self.path[1:])
        parent = path.parent
        
        if not authenticated and parent == ADMIN_PATH:
            self.send_auth_request()
        
        # if not authenticated and is trying to access to other paths   
        elif (
            not authenticated 
            and (parent != MAIN_PATH and parent != ARTICLES_PATH and str(parent) != '/')
        ):
            path = GUEST_PATH
        
        try:
            if parent.full_match(ARTICLES_PATH):
                data = show_article(path)
            
            elif authenticated and parent.full_match(ADMIN_PATH / "edit"):
                 article_file = path.with_name(f"{path.stem}.json").name
                 data = edit_page(article_file)

            else:
                with open(path, 'rb') as page:
                    data = page.read()
            
        except FileNotFoundError:
            status = NOT_FOUND
            data = bytes("<h1>404 Not Found</h1>", "UTF-8")
        
        except IsADirectoryError:
            status = REDIRECTED
            header = ["Location", "/pages/index"]
            with open(GUEST_PATH, 'rb') as page: 
                data = page.read()
        
        self.send_response(status)
        self.send_header(header[0], header[1])
        self.end_headers()
            
        if isinstance(data, list):
            self.wfile.writelines(data)

        else:
            self.wfile.write(data)
    
    
    def do_POST(self):
        
        path = Path(self.path)
        header = ["Location", "/pages/admin/index.html"]
        status = REDIRECTED

        if self.headers["Content-Length"]:
            #getting the body
            content_lenght = int(self.headers["Content-Length"])
            article = parse_qs(self.rfile.read(content_lenght).decode())
            article = {key:  value[0] for key, value in article.items()}
        
        if path.full_match("/pages/admin/create"):
            create_article(article)
            header[1] = "/pages/admin/new_article.html"

        elif path.parent.full_match("/pages/admin/delete"):
            name = path.name   
            delete_article(name)
         
        elif path.parent.full_match("/pages/admin/edit"):
            edit_article(article, path.name)

        else:
            status = NOT_FOUND
            header = ["Content-type", "text/html"]
             

        self.send_response(status)
        self.send_header(header[0], header[1])
        self.end_headers()
        if status == NOT_FOUND:
            self.wfile.write(b"<h1>404 Not Found</h1>")

    
    def authenticated(self, auth_header) -> bool:
        
        if not auth_header:
            return False
         
        auth_type, credentials = auth_header.split(" ", 1)
        
        if auth_type.lower() != "basic":
            return False

        decoded_credentials = base64.b64decode(credentials).decode("utf-8")
        user, passwd = decoded_credentials.split(":", 1)
        return user == USER and passwd == PASSWD

    
    def send_auth_request(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", "Basic realm='Admin authentication'")
        self.end_headers()
