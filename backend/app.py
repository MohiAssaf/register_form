import socketserver
import psycopg2
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from typing import Tuple
from db import db_connection, init_table


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/register':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            with open('../frontend/html/register.html', 'r') as file:
                html_page = file.read()
                self.wfile.write(html_page.encode('utf-8'))
        elif path == '/login':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            with open('../frontend/html/login.html', 'r') as file:
                html_page = file.read()
                self.wfile.write(html_page.encode('utf-8'))
            
        elif path == '/logged-in':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            with open('../frontend/html/logout.html', 'r') as file:
                html_page = file.read()
                self.wfile.write(html_page.encode('utf-8'))
        elif path == '/logout':
            self.send_response(302)
            self.send_header('Location', '/login')
            self.end_headers()
            
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')




class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    init_table()
    server_address = ('', 8000)
    httpd = ThreadedHTTPServer(server_address, RequestHandler)
    print('Starting server on port 8000...')
    httpd.serve_forever()
