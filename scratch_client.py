# scratch_client.py

import requests
import re

class ScratchClient:
    def __init__(self):
        self.session = requests.Session()
        self.logged_in = False

    def _login(self, username, password):
        login_url = "https://scratch.mit.edu/login/"
        login_page = self.session.get(login_url)

        if login_page.status_code != 200:
            print("Failed to fetch the login page.")
            return False

        csrf_token = self._get_csrf_token(login_page.text)

        login_data = {
            'username': username,
            'password': password,
            'csrf_token': csrf_token  # If applicable
        }

        login_action_url = "https://scratch.mit.edu/accounts/login/"
        response = self.session.post(login_action_url, data=login_data)

        if response.status_code == 200 and "My Stuff" in response.text:
            print("Login successful!")
            self.logged_in = True
            return True
        else:
            print("Login failed. Please check your credentials.")
            return False

    def _get_csrf_token(self, html_content):
        match = re.search(r'csrf_token" value="([^"]+)', html_content)
        if match:
            return match.group(1)
        return ''

    def check_logged_in(self):
        if self.logged_in:
            response = self.session.get("https://scratch.mit.edu/users/")
            if response.status_code == 200 and "My Stuff" in response.text:
                return True
        return False

    def logout(self):
        self.session.cookies.clear()
        self.logged_in = False
        print("Logged out successfully.")

    def get_user_profile(self, username):
        try:
            response = self.session.get(f"https://scratch.mit.edu/users/{username}")
            if response.status_code == 200:
                return response.json()
            else:
                print("Failed to fetch user profile.")
        except Exception as e:
            print(f"Error fetching user profile: {e}")
        return None
