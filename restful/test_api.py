import requests
import base64
import os

# URL of the Flask API endpoint
API_URL = "http://127.0.0.1:80/item/title_generate" # Assuming port 80 as per app.py

# Path to the local test video
# Using a video from the root directory of the project
TEST_VIDEO_PATH = "../test_video.mp4" 

def test_title_generation():
    # Ensure the test video file exists
    if not os.path.exists(TEST_VIDEO_PATH):
        print(f"Error: Test video file not found at {os.path.abspath(TEST_VIDEO_PATH)}")
        return

    # Read the video file and encode it in base64
    try:
        with open(TEST_VIDEO_PATH, "rb") as video_file:
            video_b64 = base64.b64encode(video_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error reading or encoding video file: {e}")
        return

    # Prepare the request payload
    payload = {
        "video": video_b64,
        "meta": { # Example meta, as per 接口要求.md
            "itemId": "test_item_123",
            "content": "Test video content",
            "itemTime": 1739638300413,
            "title": "Original test video title",
            "url": "local/test_video.mp4",
            "duration": 10, # Example duration
            "categoryLevel1": "测试",
            "tag": "test, video, api",
            "coverUrl": "",
            "bloggerName": "test_blogger",
            "likeCnt": 0,
            "commentCnt": 0,
            "collectCnt": 0,
            "fansCnt": 0
        }
    }

    # Make the POST request
    print(f"Sending request to {API_URL} with video {TEST_VIDEO_PATH}...")
    try:
        response = requests.post(API_URL, json=payload, timeout=600) # Timeout as per requirement
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        
        # Print the response from the server
        print("Response status code:", response.status_code)
        print("Response JSON:", response.json())

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # First, ensure the Flask app (app.py) is running in a separate terminal.
    # Then, run this script to test the API.
    print("Starting API test...")
    test_title_generation()
    print("API test finished.")
