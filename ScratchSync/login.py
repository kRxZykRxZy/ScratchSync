from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class ScratchLogin:
    def __init__(self, package_name):
        self.package_name = package_name

    def connect_and_login(self, username, password):
        try:
            if not username or not password:
                raise ValueError("Username or password is missing")

            # Connect session with provided username and password
            self.package_name.connect_session(username, password)

            # Set up the web driver (using Chrome in this example)
            driver = webdriver.Chrome()

            # Open the Scratch login page
            driver.get('https://scratch.mit.edu/login/')

            # Allow the page to load
            time.sleep(3)

            # Find username and password fields and login button
            username_field = driver.find_element(By.NAME, 'username')
            password_field = driver.find_element(By.NAME, 'password')

            # Enter the credentials
            username_field.send_keys(username)
            password_field.send_keys(password)
            password_field.send_keys(Keys.RETURN)

            # Allow time to log in
            time.sleep(5)

            print("Login successful!")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            driver.quit()

# Example usage
if __name__ == "__main__":
    import Package_name

    scratch_login = ScratchLogin(Package_name)
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    scratch_login.connect_and_login(username, password)
