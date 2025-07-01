import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
import re

def extract_video_id(url):
    """Extract video ID from various YouTube URL formats."""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?]+)',
        r'youtube\.com\/embed\/([^&\n?]+)',
        r'youtube\.com\/v\/([^&\n?]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_video_info(api_key, video_id):
    """Get video information using YouTube Data API."""
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        # Get video details
        request = youtube.videos().list(
            part='snippet,statistics,contentDetails',
            id=video_id
        )
        response = request.execute()
        
        if not response['items']:
            return None
            
        video_data = response['items'][0]
        snippet = video_data['snippet']
        statistics = video_data['statistics']
        content_details = video_data['contentDetails']
        
        return {
            'title': snippet['title'],
            'description': snippet['description'],
            'channel_title': snippet['channelTitle'],
            'published_at': snippet['publishedAt'],
            'view_count': statistics.get('viewCount', 'N/A'),
            'like_count': statistics.get('likeCount', 'N/A'),
            'comment_count': statistics.get('commentCount', 'N/A'),
            'duration': content_details['duration']
        }
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def main():
    # Load API key from environment variable
    load_dotenv()
    api_key = os.getenv('YOUTUBE_API_KEY')
    
    if not api_key:
        print("Please set your YouTube API key in the .env file")
        return
    
    while True:
        url = input("\nEnter YouTube URL (or 'quit' to exit): ")
        if url.lower() == 'quit':
            break
            
        video_id = extract_video_id(url)
        if not video_id:
            print("Invalid YouTube URL")
            continue
            
        video_info = get_video_info(api_key, video_id)
        if video_info:
            print("\nVideo Information:")
            print(f"Title: {video_info['title']}")
            print(f"Channel: {video_info['channel_title']}")
            print(f"Published: {video_info['published_at']}")
            print(f"Views: {video_info['view_count']}")
            print(f"Likes: {video_info['like_count']}")
            print(f"Comments: {video_info['comment_count']}")
            print(f"Duration: {video_info['duration']}")
            print("\nDescription:")
            print(video_info['description'])
        else:
            print("Could not fetch video information")

if __name__ == "__main__":
    main() 