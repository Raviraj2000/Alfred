import re
from utils.image_processing import extract_raw_text
from utils.spotify_validator import SpotifyValidator

# List of noise keywords to filter out
NOISE_KEYWORDS = [
    "up next", "lyrics", "related", "playing from", "radio", 
    "save", "discover", "cuts", "familiar", "popular", "deep cuts"
]

def extract_rows(raw_text):
    """
    Extract rows from OCR output while preserving structure and removing noise.
    """
    rows = []
    for line in raw_text.splitlines():
        line = line.strip()
        # Skip empty lines and those containing noise keywords
        if line and not any(keyword in line.lower() for keyword in NOISE_KEYWORDS):
            rows.append(line)
    return rows


def combine_rows_into_songs(rows):
    """
    Combine OCR-detected rows into song and artist pairs.
    """
    songs = []
    i = 0
    while i < len(rows):
        title = rows[i]
        artist = rows[i + 1] if i + 1 < len(rows) else None

        # Check if the next row is likely an artist name
        if artist and len(artist.split()) <= 3:
            songs.append(f"{title} by {artist}")
            i += 2
        else:
            songs.append(title)
            i += 1
    return songs


def filter_songs(raw_text):
    """
    Filter and clean song titles and artist names from OCR output.
    """
    rows = extract_rows(raw_text)
    return combine_rows_into_songs(rows)


def extract_song_titles(image_path):
    """
    Extract and validate song titles from an image using SpotifyValidator.
    """
    # Step 1: Extract raw text using OCR
    raw_text = extract_raw_text(image_path)

    # Step 2: Filter songs from raw text
    songs = filter_songs(raw_text)

    # Step 3: Validate using Spotify API
    spotify_validator = SpotifyValidator()
    validated_songs = []
    for song in songs:
        if " by " in song:
            title, artist = song.split(" by ", 1)
            validated_song = spotify_validator.validate_song(title.strip(), artist.strip())
        else:
            validated_song = spotify_validator.validate_song(song)

        if validated_song:
            validated_songs.append(validated_song)
        else:
            print(f"Could not validate: {song}")  # Optional logging

    # Step 4: Return the list of validated songs
    return list(set(validated_songs))  # Remove duplicates
