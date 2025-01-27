import requests ,re
from config import Config
from garbage import garbage_list

def clean_youtube_title(title: str, garbage_list: list) -> str:
    # Create a regex pattern to match any garbage terms
    pattern = r"\b(" + "|".join(re.escape(term) for term in garbage_list) + r")\b"
    # Replace matched terms with an empty string
    cleaned_title = re.sub(pattern, "", title, flags=re.IGNORECASE)
    # Remove extra whitespace
    return re.sub(r"\s+", " ", cleaned_title).strip()


# https://www.youtube.com/watch?v=EtbafaIU7gQ&list=RDMMEtbafaIU7gQ&start_radio=1
async def youtube_title_fetch(play_url:str):
    list_id = play_url.split("list=")[1].split("&")[0]
    list_urls = []
    print(list_id)
    api_url = (
            f"https://www.googleapis.com/youtube/v3/playlistItems"
            f"?part=snippet&playlistId={list_id}&maxResults=20&key={Config.YOUTUBE_API_KEY}"
        )
    response = requests.get(api_url)
    if response.status_code != 200:
            print(response.json())
            raise Exception("Failed to fetch playlist data from YouTube")
    
    data = response.json()
    print(response.json())
    
    for item in data["items"]:
        video_id = item["snippet"]["title"]
        list_urls.append(clean_youtube_title(title=video_id,garbage_list=garbage_list))   

    return list_urls     

