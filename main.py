from pytube import YouTube 
import requests 
import re
import os 

"""
REQUIREMENTS-

1. pytube: pip install pytube
2. requests: pip install requests
"""

def on_complete(stream, path):
    """
    Opens downloaded file with default media player
    """
    os.startfile(path)

def url_from_query(query):
    """
    Gets youtube URL from search query using requests
    """
    page = requests.get(f"https://www.youtube.com/results?search_query={"+".join(query.split())}")
    url = re.search(r"watch\?v=.{11}" ,page.text)
    if url:  
        return url.group()
    else:
        return None
    
def download_from_url(url):
    """
    Uses pytube library to download youtube video from URL
    """
    try:
            # call on_complete() when video finishes downloading
            video = YouTube(url, on_complete_callback=on_complete) 
            print(f"Playing {video.title}\n\n")
            t=video.streams.filter(only_audio=True)
            t[0].download()
            filename = video.title+'.mp4'
            
            return filename
    except Exception as e:
            print(f"An error occured, {e}")

def main_loop():
    filename = ""
    try:
        while True:
            userInp = input("Enter song name or youtube URL: \n")
            if filename:
                #if something was played before, delete the file
                try:
                    os.remove(filename)
                except Exception:
                    pass

            if "youtube.com" in userInp:
                filename = download_from_url(url=userInp)

            else:
                urlCode = url_from_query(userInp)
                if urlCode is None:
                    print("Song not found!\n")
                    continue
                else:
                    ytUrl = f"https://youtube.com/{urlCode}"
                    filename = download_from_url(url=ytUrl)
    except KeyboardInterrupt:
        # delete old file before exiting
        os.remove(filename)
        exit()

if __name__ == "__main__":
    main_loop()
