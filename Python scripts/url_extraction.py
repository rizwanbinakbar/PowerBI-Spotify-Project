import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
CLIENT_ID = "CLIENT ID"  # Replace with your Spotify client ID
CLIENT_SECRET = "CLIENT SECRET"  # Replace with your Spotify client secret

# Authenticate with Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

# Load the dataset
df = pd.read_csv('spotify_data_with_covers.csv', encoding='latin1')

# Function to fetch album cover URL from Spotify API
def fetch_album_cover(track_name, artist_name):
    try:
        # Search for the track on Spotify
        query = f"track:{track_name} artist:{artist_name}"
        results = sp.search(q=query, type='track', limit=1)
        if results['tracks']['items']:
            # Extract album cover URL
            return results['tracks']['items'][0]['album']['images'][0]['url']
        else:
            return None  # No results found
    except Exception as e:
        print(f"Error fetching cover for {track_name} by {artist_name}: {e}")
        return None

# Apply the function to each row in the dataset
df['cover_url'] = df.apply(lambda row: fetch_album_cover(row['track_name'], row["artist(s)_name"]), axis=1)

# Save the updated DataFrame to a new CSV file
df.to_csv('spotify_data_with_updated_covers.csv', index=False)
