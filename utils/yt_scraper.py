from youtube_dl import YoutubeDL
from utils.video import Video
import requests

class YtScraper:

    @staticmethod
    def search(query, num_results = 10):
        with YoutubeDL({'format':'bestaudio/best', 'noplaylist': 'True'}) as ydl:
            try:
                requests.get(query) # checks to see if query is a valid URL
            except:
                info = ydl.extract_info(f"ytsearch{num_results}:{query}", download=False)['entries']
                return [Video(title=x["title"],
                              url=x["webpage_url"],
                              duration=x["duration"],
                              channel=x["channel"],
                              source=x["formats"][0]["url"]) for x in info]
            else:
                info = ydl.extract_info(query, download=False)
                return [Video(title=info["title"],
                              url=info["webpage_url"],
                              duration=info["duration"],
                              channel=info["channel"],
                              source=info["formats"][0]["url"])]