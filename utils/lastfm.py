import requests
import re
import os
from dotenv import load_dotenv
load_dotenv()

class LastFMValidator:
    def __init__(self):
        self.api_key = os.environ["LASTFM_API_KEY"]
        self.base_url = "http://ws.audioscrobbler.com/2.0/"

    def validate_song(self, song_title, artist_hint=None):
        """
        Validate a song title using the Last.fm API and prioritize the original artist.
        :param song_title: The song title to validate.
        :param artist_hint: Optional artist name to improve search accuracy.
        :return: Validated song as "Title by Artist", or None if not found.
        """
        params = {
            "method": "track.search",
            "track": song_title,
            "api_key": self.api_key,
            "format": "json",
            "limit": 5  # Fetch multiple results to allow prioritization
        }

        # If artist_hint is provided, include it in the query
        if artist_hint:
            params["artist"] = artist_hint

        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            tracks = data.get("results", {}).get("trackmatches", {}).get("track", [])
            if not tracks:
                return None

            # Filter results to prioritize original tracks
            for track in tracks:
                artist_name = track.get("artist", "").lower()
                track_name = track.get("name", "")
                if not re.search(r"(tribute|cover|karaoke|piano|guitar|made famous)", artist_name, re.IGNORECASE):
                    return f"{track_name} by {track['artist']}"

            # Fallback: Return the first match if no original track is found
            track = tracks[0]
            return f"{track['name']} by {track['artist']}"
        return None
