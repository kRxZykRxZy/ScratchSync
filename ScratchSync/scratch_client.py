import requests
import json
from bs4 import BeautifulSoup

class ScratchClient:
    def __init__(self):
        self.session = None
        self.logged_in = False

    def login(self, username, password):
        """Logs into Scratch using the Session class."""
        try:
            self.session = Session.login_by_io(username, password)
            if self.session and self.session.username:
                print(f"Login successful as {self.session.username}")
                self.logged_in = True
                return True
            else:
                print("Login failed. Please check your credentials.")
                return False
        except Exception as e:
            print(f"Error during login: {e}")
            return False

    def check_logged_in(self):
        """Checks if still logged in."""
        if self.session:
            return self.session.username is not None
        return False

    def logout(self):
        """Logs out from Scratch."""
        if self.session:
            self.session.logout()
            self.logged_in = False
            print("Logged out successfully.")
        else:
            print("No active session to log out from.")

    def get_user_profile(self, username):
        """Fetches a user's Scratch profile."""
        try:
            response = requests.get(f"https://api.scratch.mit.edu/users/{username}")
            if response.status_code == 200:
                return response.json()
            else:
                print("Failed to fetch user profile.")
        except Exception as e:
            print(f"Error fetching user profile: {e}")
        return None


# Assuming Session has this method from the original code you posted
class Session:
    @classmethod
    def login_by_io(cls, username, password):
        """Logs into Scratch and returns a Session object."""
        login_url = "https://scratch.mit.edu/accounts/login/"
        login_data = json.dumps({
            "username": username,
            "password": password
        })

        session = requests.Session()
        response = session.post(
            login_url,
            data=login_data,
            headers={
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/json",
                "Referer": "https://scratch.mit.edu/",
                "Origin": "https://scratch.mit.edu/"
            }
        )

        if response.status_code == 200:
            try:
                res_data = response.json()
                if res_data.get('errors'):
                    print(f"Login failed: {res_data['errors']}")
                    return None

                print("Login successful!")

                # Extract session and CSRF tokens
                session_id = session.cookies.get('scratchsessionsid')
                csrf_token = session.cookies.get('scratchcsrftoken')

                return cls(
                    id=session_id,
                    username=res_data["user"]["username"],
                    xtoken=res_data["user"]["token"],
                )
            except json.JSONDecodeError:
                print("Failed to parse login response.")
        else:
            print(f"Login failed with status code {response.status_code}.")
        return None

    def __init__(self, id, username, xtoken):
        self.id = id
        self.username = username
        self.xtoken = xtoken
        self._headers = {
            "X-CSRFToken": "a",  # Scratch sets this to 'a' by default
            "X-Token": self.xtoken
        }
        self._cookies = {
            "scratchsessionsid": self.id,
            "scratchcsrftoken": "a",
        }

    def logout(self):
        """Logs out from the session."""
        requests.post(
            "https://scratch.mit.edu/accounts/logout/",
            headers=self._headers,
            cookies=self._cookies
        )
