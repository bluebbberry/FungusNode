import requests
from dotenv import load_dotenv, dotenv_values
import os
# loading variables from .env file
load_dotenv()


class MastodonClient:
    def __init__(self):
        self.server_url = os.getenv("MASTODON_SERVER")
        self.access_token = os.getenv("ACCESS_TOKEN")
        self.mycelial_hashtags = self.get_tags_from_mycelial_hashtags_env_string(os.getenv("MYCERIAL_TAGS"))

    def get_tags_from_mycelial_hashtags_env_string(self, value):
        return value.split(';')

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

    def post_status_on_mycelial_hashtags(self, status_text):
        for hashtag in self.mycelial_hashtags:
            self.post_status(f"#{hashtag} {status_text}")

    def get_latest_statuses(self, hashtag):
        base_url = f"{self.server_url}/api/v1"

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Accept': 'application/json'
        }

        params = {
            'type': 'statuses',
            'tag': hashtag,
            'limit': 30
        }

        response = requests.get(f"{base_url}/timelines/tag/{hashtag}",
                                headers=headers,
                                params=params)

        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data)} latest statuses")
            statuses = data

            # Print first few statuses
            # print(f"Latest 30 statuses for #{hashtag}:")
            # for i, status in enumerate(statuses[:5], 1):
            #     print(f"\nStatus {i}:")
            #     print(f"ID: {status['id']}")
            #     print(f"Content: {status['content']}")
            #     print(f"Account: {status['account']['username']}")
            #     print(f"Posted at: {status['created_at']}")

            # Return all statuses
            return statuses
        else:
            print(f"Error: {response.status_code}")
            return None
