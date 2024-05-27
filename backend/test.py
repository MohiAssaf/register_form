import unittest
import threading
import requests
from server import RequestHandler, ThreadedHTTPServer



class TestServer(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):# start the server
        cls.server = ThreadedHTTPServer(('localhost', 8000), RequestHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        
    @classmethod
    def tearDownClass(cls):# shutdown the server
        cls.server.shutdown()
        
    def test_register_page_get(self):
        response = requests.get('http://localhost:8000/register')
        self.assertEqual(response.status_code, 200)
        
    def test_login_page_get(self):
        response = requests.get('http://localhost:8000/login')
        self.assertEqual(response.status_code, 200)
        
    def test_logged_in_page_get(self):
        response = requests.get('http://localhost:8000/logged-in')
        self.assertEqual(response.status_code, 200)
        
    def test_update_page_get(self):
        response = requests.get('http://localhost:8000/update-data')
        self.assertEqual(response.status_code, 401)
    
        
    def test_register_page_post(self):
        
        register_data = {
            'first_name': 'Mohamed',
            'last_name': 'assaf',
            'email': 'mohamedabuassaf@.com',
            'username': 'assafMo',
            'password': '12',
            'repassword': '12',
            'captcha': 'BHJ4KJ'
        }
        
        response = requests.post('http://localhost:8000/register', data=register_data, cookies={'captcha': 'BHJ4KJ'})
        self.assertEqual(response.status_code, 200)
        
        response = requests.post('http://localhost:8000/register', data=register_data, cookies={'captcha': 'BHJ4KJ'}) ## registering again with the same user test
        self.assertEqual(response.status_code, 400)
        
        
    def test_login_page_post(self):
        login_data = {
            'username': 'admin',
            'password': '12',
        }
        response = requests.post('http://localhost:8000/login', data=login_data)
        self.assertEqual(response.status_code, 200)
        
    def test_update_page_post(self):
        update_data = {
            'first_name': 'mish',
            'last_name': 'assaf',
            'newpassword': '12355',
            'newrepassword': '12355'
        }

        response = requests.post('http://localhost:8000/update-data', data=update_data, cookies={'username': 'mohi45dd4'})
        self.assertEqual(response.status_code, 200)
        
        
if __name__ == '__main__':
    unittest.main()