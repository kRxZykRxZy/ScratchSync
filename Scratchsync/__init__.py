import requests
from bs4 import BeautifulSoup

class ScratchLogin:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = 'https://scratch.mit.edu'

    def connect_session(self, username, password):
        if not username or not password:
            raise ValueError("Username or password is missing")

        try:
            # Step 1: Get the login page to scrape necessary CSRF token
            login_url = f'{self.base_url}/login/'
            response = self.session.get(login_url)
            if response.status_code != 200:
                print(f"Failed to access login page. Status code: {response.status_code}")
                return

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Step 2: Scrape CSRF token (it may be in an input field or meta tag)
            csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'}).get('value')

            if not csrf_token:
                print("CSRF Token not found, cannot proceed with login.")
                return

            # Step 3: Prepare the login data to send
            login_data = {
                'username': username,
                'password': password,
                'csrfmiddlewaretoken': csrf_token
            }

            headers = {
                'User-Agent': 'Mozilla/5.0',
                'Referer': login_url
            }

            # Step 4: Send the login request
            login_response = self.session.post(login_url, data=login_data, headers=headers)

            # Step 5: Check if login was successful (successful login redirects)
            if login_response.url == self.base_url:
                print("Login successful!")
            else:
                print("Login failed. Please check your credentials.")

        except Exception as e:
            print(f"An error occurred: {e}")
