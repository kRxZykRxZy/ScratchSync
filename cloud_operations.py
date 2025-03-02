# cloud_operations.py

import requests

class CloudOperations:
    @staticmethod
    def get_var(client, project_id, var_name):
        try:
            response = client.session.get(f"https://clouddata.scratch.mit.edu/projects/{project_id}")
            if response.status_code == 200:
                cloud_data = response.json()
                for var in cloud_data:
                    if var['name'] == var_name:
                        return var['value']
        except Exception as e:
            print(f"Error fetching cloud variable: {e}")
        return None

    @staticmethod
    def set_var(client, project_id, var_name, value):
        if not client.logged_in:
            print("Not logged in")
            return
        try:
            payload = {"name": var_name, "value": value}
            response = client.session.post(f"https://clouddata.scratch.mit.edu/projects/{project_id}/variables", json=payload)
            response.raise_for_status()
            print("Cloud variable updated")
        except Exception as e:
            print(f"Error setting cloud variable: {e}")
