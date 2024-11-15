import os
import requests
import schedule
import time
from dotenv import load_dotenv

load_dotenv()

# Constants
TIKTOK_CLIENT_ID = os.getenv("TIKTOK_CLIENT_ID")
TIKTOK_CLIENT_SECRET = os.getenv("TIKTOK_CLIENT_SECRET")
NEXTCLOUD_URL = os.getenv("NEXTCLOUD_URL")
NEXTCLOUD_USERNAME = os.getenv("NEXTCLOUD_USERNAME")
NEXTCLOUD_PASSWORD = os.getenv("NEXTCLOUD_PASSWORD")
TIKTOK_ACCESS_TOKEN = None  # Placeholder for the access token

# Functions

def authenticate_tiktok():
    global TIKTOK_ACCESS_TOKEN
    # Implement OAuth 2.0 authentication to get access token
    print("Authenticating with TikTok...")
    TIKTOK_ACCESS_TOKEN = "your_access_token"  # Replace with actual token retrieval logic

def fetch_video_from_nextcloud():
    print("Fetching video from Nextcloud...")
    response = requests.get(NEXTCLOUD_URL + '/remote.php/dav/files/' + NEXTCLOUD_USERNAME + '/videos/',
                            auth=(NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD))
    
    if response.status_code == 200:
        video_files = response.json()  # Assume it returns a list of video files
        return video_files[0]  # Return the first video for simplicity
    else:
        print("Failed to fetch video:", response.status_code)
        return None

def post_video_to_tiktok(video_path):
    print(f"Posting video {video_path} to TikTok...")
    url = "https://open-api.tiktok.com/video/upload/"
    files = {'file': open(video_path, 'rb')}
    headers = {'Authorization': f'Bearer {TIKTOK_ACCESS_TOKEN}'}
    
    response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        print("Video posted successfully!")
    else:
        print("Failed to post video:", response.status_code)

def job():
    video = fetch_video_from_nextcloud()
    if video:
        post_video_to_tiktok(video)

# Scheduler
schedule.every().day.at("09:00").do(job)  # Schedule to run every day at 9 AM

if __name__ == "__main__":
    authenticate_tiktok()
    while True:
        schedule.run_pending()
        time.sleep(1)
