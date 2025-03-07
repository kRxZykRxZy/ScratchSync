# scratch_project.py

import requests
from .scratch_client import ScratchClient

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
