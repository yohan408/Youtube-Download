from pytube import Playlist, YouTube
from tqdm import tqdm
import time

def download_video(video, path, resolution):
    # Filter streams by the specified resolution and progressive (includes audio)
    stream = video.streams.filter(res=resolution, progressive=True).first()
    
    # If no stream is found with the exact resolution, get the highest available resolution
    if not stream:
        stream = video.streams.filter(progressive=True).order_by('resolution').desc().first()
        print(f"Requested resolution {resolution} not available. Downloading highest resolution available: {stream.resolution}")
    else:
        print(f"Downloading {video.title} at resolution {resolution}")

    if stream:
        # Initialize tqdm progress bar
        with tqdm(total=stream.filesize, unit='B', unit_scale=True, desc=video.title) as pbar:
            # Define a callback function for showing progress
            def progress_function(chunk, file_handle, bytes_remaining):
                pbar.update(len(chunk))
            
            # Register the progress callback
            stream.download(output_path=path, on_progress_callback=progress_function)
        print(f"Downloaded {video.title}")
    else:
        print(f"Could not find a suitable stream for {video.title}")

def download_playlist(playlist_url, download_path='.', resolution='720p', retries=3):
    # Create Playlist object
    playlist = Playlist(playlist_url)
    
    print(f"Downloading playlist: {playlist.title}")
    print(f"Number of videos in playlist: {len(playlist.video_urls)}")
    
    for video_url in playlist.video_urls:
        success = False
        for attempt in range(retries):
            try:
                video = YouTube(video_url)
                print(f"Available resolutions for {video.title}:")
                for stream in video.streams.filter(progressive=True).order_by('resolution'):
                    print(f"{stream.resolution}")
                download_video(video, download_path, resolution)
                success = True
                break
            except Exception as e:
                print(f"Failed to download video {video_url} on attempt {attempt+1}. Error: {str(e)}")
                time.sleep(1)  # Wait a bit before retrying
        if not success:
            print(f"Failed to download video {video_url} after {retries} attempts.")


if __name__ == "__main__":
    # Replace this URL with the URL of the playlist you want to download
    playlist_url = "https://www.youtube.com/playlist?list=PLKa47oZvF_9o8OOkKCRVtzSlCAmyJYaMo"
    download_path = r"d:\yt playlist"
    resolution = "144p"  # E.g., '720p', '1080p', etc.
    
    download_playlist(playlist_url, download_path, resolution)


