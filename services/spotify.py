from fastapi import HTTPException, Response
import requests
from config import Config

def make_spotify_request(method: str, endpoint: str, **kwargs):
    """
    Helper function to make Spotify API requests with authentication and error handling.

    Args:
        method (str): HTTP method (GET, POST, PUT, DELETE, etc.).
        endpoint (str): Spotify API endpoint (e.g., '/v1/users/{user_id}/playlists').
        kwargs: Additional parameters such as headers, JSON data, etc.

    Returns:
        dict: JSON response from Spotify API.

    Raises:
        HTTPException: If the API call fails with a non-2xx status code.
    """
    url = f"{endpoint}"
    print("my url: ",url)
    
    headers = kwargs.get("headers", {})
    headers.update({
        "Authorization": f"Bearer {Config.SPOTIFY_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    })
    kwargs["headers"] = headers

    response = requests.request(method, url, **kwargs)

    # Handle errors
    if response.status_code not in range(200, 299):
        print(response.json())
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json().get('error', {}).get('message', 'Unknown error')
        )

    return response.json()


def create_playlist_request(url, playlist_name)-> dict:
     try:
        endpoint =  url
        payload = {
            "name": playlist_name,
            "public": False  # Set to False if you want the playlist to be private
        }
        
        return make_spotify_request("POST", endpoint, json=payload)
     except HTTPException as e:
        print(f'Error: {str(e)}')
        return {"error": str(e)}


def search_track_request(url, query)-> dict:
    try:
        params = {
            "q": query,
            "type": "track",
            "limit": 1 # Limit the number of search results
        }
        return make_spotify_request("GET", url, params=params)
    except HTTPException as e:
        return {"error": str(e)}
   

def add_track_to_playlist_request(url,track_uris)-> dict:
    try:
        payload = {
            "uris": track_uris
        }
        return make_spotify_request("POST",  url, json=payload)
    except HTTPException as e:
        return {"error": str(e)}


 


 