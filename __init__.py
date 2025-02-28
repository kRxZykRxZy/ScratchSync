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
                return response.json()  # This may vary, use the response data as needed
            else:
                print("Failed to fetch user profile.")
        except Exception as e:
            print(f"Error fetching user profile: {e}")
        return None

    def get_forum_topics(self, category_id):
        """ Fetch topics from a specific Scratch forum category. """
        url = f"https://scratch.mit.edu/discuss/4/{category_id}/"
        response = self.session.get(url)
        if response.status_code == 200:
            return response.json()  # Assuming the forum topics are returned in JSON format
        return None

    def post_forum_message(self, topic_id, message):
        """ Post a message to a specific forum topic. """
        if not self.logged_in:
            print("You need to be logged in to post a message.")
            return False
        post_url = f"https://scratch.mit.edu/discuss/{topic_id}/reply/"
        data = {
            'message': message,
            'csrf_token': self._get_csrf_token(self.session.get(f"https://scratch.mit.edu/discuss/{topic_id}/").text)
        }
        response = self.session.post(post_url, data=data)
        if response.status_code == 200:
            print("Message posted successfully.")
            return True
        print("Failed to post message.")
        return False

    def get_user_messages(self, user_id):
        """ Get all messages of a specific user. """
        url = f"https://scratch.mit.edu/users/{user_id}/messages/"
        response = self.session.get(url)
        if response.status_code == 200:
            return response.json()  # Returns a list of messages
        return None

    def get_user_forums_posts(self, user_id):
        """ Get all posts of a user on the forums. """
        url = f"https://scratch.mit.edu/users/{user_id}/forum_posts/"
        response = self.session.get(url)
        if response.status_code == 200:
            return response.json()  # Returns a list of posts made by the user in the forum
        return None

    def delete_forum_message(self, message_id):
        """ Delete a forum message by its ID. """
        delete_url = f"https://scratch.mit.edu/discuss/messages/{message_id}/delete/"
        response = self.session.post(delete_url)
        if response.status_code == 200:
            print("Message deleted successfully.")
            return True
        print("Failed to delete message.")
        return False

    def report_forum_topic(self, topic_id):
        """ Report a forum topic for violating the community guidelines. """
        report_url = f"https://scratch.mit.edu/discuss/topics/{topic_id}/report/"
        response = self.session.post(report_url)
        if response.status_code == 200:
            print("Forum topic reported successfully.")
            return True
        print("Failed to report forum topic.")
        return False

    def report_project(self, project_id):
        """ Report a Scratch project for violating the community guidelines. """
        report_url = f"https://scratch.mit.edu/projects/{project_id}/report/"
        response = self.session.post(report_url)
        if response.status_code == 200:
            print("Project reported successfully.")
            return True
        print("Failed to report project.")
        return False

    def change_signature(self, new_signature):
        """ Change the user’s signature. """
        if not self.logged_in:
            print("You need to be logged in to change your signature.")
            return False
        change_url = "https://scratch.mit.edu/users/edit_signature/"
        data = {
            'signature': new_signature,
            'csrf_token': self._get_csrf_token(self.session.get("https://scratch.mit.edu/users/edit_signature/").text)
        }
        response = self.session.post(change_url, data=data)
        if response.status_code == 200:
            print("Signature updated successfully.")
            return True
        print("Failed to change signature.")
        return False

    def get_forum_post_count(self, user_id):
        """ Get the total count of a user's forum posts. """
        posts = self.get_user_forums_posts(user_id)
        return len(posts) if posts else 0

    def get_total_comment_count(self, user_id):
        """ Get the total number of comments a user has made. """
        url = f"https://scratch.mit.edu/users/{user_id}/comments/"
        response = self.session.get(url)
        if response.status_code == 200:
            comments = response.json()
            return len(comments)
        return 0

    def get_followers_count(self, user_id):
        """ Get the total number of followers a user has. """
        url = f"https://scratch.mit.edu/users/{user_id}/followers/"
        response = self.session.get(url)
        if response.status_code == 200:
            followers = response.json()
            return len(followers)
        return 0

    def get_following_count(self, user_id):
        """ Get the total number of users a user is following. """
        url = f"https://scratch.mit.edu/users/{user_id}/following/"
        response = self.session.get(url)
        if response.status_code == 200:
            following = response.json()
            return len(following)
        return 0

    def get_project_count(self, user_id):
        """ Get the total number of projects a user has. """
        url = f"https://scratch.mit.edu/users/{user_id}/projects/"
        response = self.session.get(url)
        if response.status_code == 200:
            projects = response.json()
            return len(projects)
        return 0

    def get_all_projects(self, user_id):
        """ Get a list of all the user's projects. """
        url = f"https://scratch.mit.edu/users/{user_id}/projects/"
        response = self.session.get(url)
        if response.status_code == 200:
            return response.json()  # Returns a list of project details
        return []

class ScratchProject:
    def __init__(self, client, project_id):
        self.client = client
        self.project_id = project_id

    def get_stats(self):
        try:
            response = self.client.session.get(f"https://api.scratch.mit.edu/projects/{self.project_id}")
            if response.status_code == 200:
                project = response.json()
                return {
                    "views": project.get("stats", {}).get("views", 0),
                    "loves": project.get("stats", {}).get("loves", 0),
                    "favorites": project.get("stats", {}).get("favorites", 0)
                }
        except Exception as e:
            print(f"Error fetching project stats: {e}")
        return None

    def get_var(self, var_name):
        try:
            response = self.client.session.get(f"https://clouddata.scratch.mit.edu/projects/{self.project_id}")
            if response.status_code == 200:
                cloud_data = response.json()
                for var in cloud_data:
                    if var['name'] == var_name:
                        return var['value']
        except Exception as e:
            print(f"Error fetching cloud variable: {e}")
        return None

    def set_var(self, var_name, value):
        if not self.client.logged_in:
            print("Not logged in")
            return
        try:
            payload = {"name": var_name, "value": value}
            response = self.client.session.post(f"https://clouddata.scratch.mit.edu/projects/{self.project_id}/variables", json=payload)
            response.raise_for_status()
            print("Cloud variable updated")
        except Exception as e:
            print(f"Error setting cloud variable: {e}")
