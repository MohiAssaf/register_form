import socketserver
from http.cookies import SimpleCookie
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
            
            with open('../frontend/html/profile.html', 'r') as file:
                html_page = file.read()
                self.wfile.write(html_page.encode('utf-8'))
        elif path == '/logout':
            self.send_response(302)
            self.send_header('Set-Cookie', 'sessionid=; Max-Age=0; Path=/')
            self.send_header('Location', '/login')
            self.end_headers()
        
        elif path == '/update-data':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            with open('../frontend/html/update_data.html', 'r') as file:
                html_page = file.read()
                self.wfile.write(html_page.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')
            
    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        content_len = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_len)
        data = parse_qs(post_data.decode('utf-8'))
        print(data)
        if path == '/register':
            first_name = data.get('first_name')[0]
            last_name = data.get('last_name')[0]
            email = data.get('email')[0]
            username = data.get('username')[0]
            password = data.get('password')[0]
            confirm_password = data.get('repassword')[0]
            
            if password != confirm_password:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Passwords do not match')
                return
            
            conn = db_connection()
            cursor = conn.cursor()
            
            cursor.execute("INSERT INTO users (first_name, last_name, email, username, password) VALUES (%s, %s, %s, %s, %s)",
                                (first_name, last_name, email, username, password))
            
            conn.commit()
            
            self.send_response(302)
            self.send_header('Location', '/login')
            self.end_headers()
            
        elif path == '/login':
            username = data.get('username')[0]
            password = data.get('password')[0]
            
            conn = db_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s",(username, password))
            user = cursor.fetchone()
            
            if user:
                self.send_response(302)
                self.send_header('Set-Cookie', f'username={username}; Path=/')
                self.send_header('Location', '/logged-in')
                self.end_headers()
            else:
                self.send_response(401)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Invalid credentials')
                
        elif path == '/update-data':
            cookie_header = self.headers.get('Cookie')
            if not cookie_header:
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b'Unauthorized')
                return
            
            cookie = SimpleCookie(cookie_header)
            username = cookie.get('username').value
            
            first_name = data.get('first_name')[0]
            last_name = data.get('last_name')[0]
            password = data.get('newpassword')[0]
            confirm_password = data.get('newrepassword')[0]
            
            if  password != confirm_password:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Passwords do not match')
                return
            
            conn = db_connection()
            cursor = conn.cursor()
            
            update_fields = []
            update_values = []

            
            if first_name:
                update_fields.append("first_name = %s")
                update_values.append(first_name)
            if last_name:
                update_fields.append("last_name = %s")
                update_values.append(last_name)
            if password:
                update_fields.append("password = %s")
                update_values.append(password)
                
            update_values.append(username)
            print(update_fields)
            print(update_values)
            
            cursor.execute(f"UPDATE users SET {', '.join(update_fields)} WHERE username = %s", tuple(update_values))
            conn.commit()
            
            self.send_response(302)
            self.send_header('Location', '/logged-in')
            self.end_headers()





class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    init_table()
    server_address = ('', 8000)
    httpd = ThreadedHTTPServer(server_address, RequestHandler)
    print('Starting server on port 8000...')
    httpd.serve_forever()
