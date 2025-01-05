import requests
from dotenv import load_dotenv, dotenv_values
import os
# loading variables from .env file
load_dotenv()


class MastodonClient:
    def __init__(self):
        self.server_url = os.getenv("MASTODON_SERVER")
        self.access_token = os.getenv("ACCESS_TOKEN")

    def post_status(self, status_text):
        url = f"{self.server_url}/api/v1/statuses"
        payload = {'status': status_text}
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error posting status: {e}")
            return None
