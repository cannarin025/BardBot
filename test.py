from utils.yt_scraper import YtScraper
import os

link = "https://www.youtube.com/watch?v=4BA2POUhCOM"
scraper = YtScraper()
dlpath = os.path.normpath(os.getcwd() + "/" + "DL")
#scraper.download_stream(scraper.get_stream(link), dlpath, "DLtest.mp3")
YtScraper.search(link)