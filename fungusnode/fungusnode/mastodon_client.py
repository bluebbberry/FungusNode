import requests


class MastodonClient:
    def __init__(self, server_url, access_token):
        self.server_url = server_url
        self.access_token = access_token
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

    def post_status(self, status_text):
        url = f"{self.server_url}/api/v1/statuses"
        payload = {'status': status_text}

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error posting status: {e}")
            return None


# Example usage:
if __name__ == "__main__":
    # Replace these with your actual values
    mastodon_server = "https://your-mastodon-server.com"
    access_token = "your-access-token-here"

    client = MastodonClient(mastodon_server, access_token)

    status_text = "Hello, Mastodon! This is a test post using Python."
    result = client.post_status(status_text)

    if result:
        print("Status posted successfully!")
        print(f"ID: {result['id']}")
