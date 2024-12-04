import json
from pytube import YouTube, Playlist
import os
import yt_dlp
from yt_dlp import YoutubeDL

fileName = 'youtube.txt'

def load_data():
    try:
        with open(fileName, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
def save_data_helper(videos):
    with open(fileName, 'w') as file:
        json.dump(videos, file, indent=4)

def format_duration(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def list_all_videos(videos):
    for index, video in enumerate(videos, start=1):
        print(f"{index}. Name: {video['name']}, Duration: {video['time']}")

def fetch_video_details(url):
    try:
        ydl_opts = {}
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get('title', 'Unknown Title')
            duration = format_duration(info_dict.get('duration', 0))
            return title, duration
    except Exception as e:
        print(f"Error fetching video details: {e}")
        return None, None

def add_video(videos):
    url = input("Enter YouTube video link: ")
    name, duration = fetch_video_details(url)
    if name and duration:
        videos.append({'name': name, 'time': duration, 'url': url})
        save_data_helper(videos)
        print(f"Added: {name} ({duration})")
    else:
        print("Failed to fetch video details.")

def update_video(videos):
    list_all_videos(videos)
    index = int(input("Enter video number to update: "))
    if 1 <= index <= len(videos):
        url = input("Enter new YouTube video link: ")
        try:
            ydl_opts = {}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)  
                name = info.get('title', 'Unknown Title')
                duration = info.get('duration', 0)
                formatted_duration = format_duration(duration)
                videos[index - 1] = {'name': name, 'time': formatted_duration, 'url': url}
                save_data_helper(videos)
                print(f"Updated: {name} ({formatted_duration})")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Invalid index selected")

def delete_video(videos):
    list_all_videos(videos)
    index = int(input("Enter video number to delete: "))
    if 1 <= index <= len(videos):
        del videos[index - 1]
        save_data_helper(videos)
        print("Video deleted successfully.")
    else:
        print("Invalid index selected")

import yt_dlp

def download_video(videos):
    list_all_videos(videos)
    index = int(input("Enter video number to download: "))
    if 1 <= index <= len(videos):
        url = videos[index - 1]['url']
        try:
            output_path = "downloads/"
            ydl_opts = {
                'format': 'best',  
                'outtmpl': f'{output_path}%(title)s.%(ext)s',  
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            print(f"Video downloaded from: {url}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Invalid index selected")


import yt_dlp

def process_playlist(videos):
    url = input("Enter YouTube playlist link: ")
    try:
        ydl_opts = {
            'quiet': True,  
            'extract_flat': True,  
            'skip_download': True,  
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(url, download=False)

        if 'entries' not in playlist_info:
            print("Error: Provided URL is not a playlist.")
            return

        print(f"Processing playlist: {playlist_info.get('title', 'Unknown Playlist')}")

        for video in playlist_info['entries']:
            if video: 
                name = video.get('title', 'Unknown Title')
                duration = video.get('duration', 0)
                duration_formatted = format_duration(duration)
                video_url = video.get('url', '')
                videos.append({'name': name, 'time': duration_formatted, 'url': f"https://www.youtube.com/watch?v={video_url}"})
        
        save_data_helper(videos)
        print(f"Added all videos from playlist: {playlist_info.get('title', 'Unknown Playlist')}")

    except Exception as e:
        print(f"Error: {e}")


def main():
    videos = load_data()
    if not os.path.exists("downloads/"):
        os.makedirs("downloads/")
        
    while True:
        print('\nYoutube Manager | Choose an option')
        print('1. List all videos')
        print('2. Add a video')
        print('3. Update previous video')
        print('4. Delete video')
        print('5. Download video')
        print('6. Process playlist')
        print('7. Exit')
        choice = input('Enter your choice: ')

        match choice:
            case '1': list_all_videos(videos)
            case '2': add_video(videos)
            case '3': update_video(videos)
            case '4': delete_video(videos)
            case '5': download_video(videos)
            case '6': process_playlist(videos)
            case '7': break
            case _: print("Invalid choice!")

if __name__ == "__main__":
    main()
