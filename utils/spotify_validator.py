import requests
import os

class SpotifyValidator:
    def __init__(self):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.token_url = "https://accounts.spotify.com/api/token"
        self.search_url = "https://api.spotify.com/v1/search"
        self.access_token = self.get_access_token()

    def get_access_token(self):
        data = {"grant_type": "client_credentials"}
        response = requests.post(self.token_url, data=data, auth=(self.client_id, self.client_secret))
        return response.json().get("access_token")

    def validate_song(self, title, artist=None):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        query = f"track:{title}"
        if artist:
            query += f" artist:{artist}"
        params = {"q": query, "type": "track", "limit": 1}
        response = requests.get(self.search_url, headers=headers, params=params)
        tracks = response.json().get("tracks", {}).get("items", [])
        if tracks:
            track = tracks[0]
            return f"{track['name']} by {track['artists'][0]['name']}"
        return None
