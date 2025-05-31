# curl http://127.0.0.1:8081/inference \
#     -H "Content-Type: multipart/form-data" \
#     -F file="@temp_audio.mp3" \
#     -F language="zh" \
#     -F task="transcribe" \
#     -F temperature="0.0" \
#     -F response_format="json"


# {"text":"學妹考慮熱舞社嗎?社長超帥是北街舞大賽冠軍\n什麼?想加烘焙社?\n那邊工具費貴到哭\n你看我們社服是橋梯還有夜光logo\n"}

import logging

from timeit_decorator import timeit

import requests
import os

@timeit()
def transcribe_audio_cpp(audio_file_path: str) -> str:
    """
    Transcribes an audio file using a local Whisper.cpp server.

    Args:
        audio_file_path: Path to the audio file.

    Returns:
        The transcribed text.
    """
    port= 8081  # Default port for the Whisper.cpp server
    url = f"http://127.0.0.1:{port}/inference"
    
    if not os.path.exists(audio_file_path):
        return "Error: Audio file not found."

    try:
        with open(audio_file_path, 'rb') as f:
            files = {'file': (os.path.basename(audio_file_path), f, 'audio/mpeg')} # Assuming mp3, adjust if needed
            data = {
                'language': 'zh',
                'task': 'transcribe',
                'temperature': '0.0',
                'response_format': 'json'
            }
            
            response = requests.post(url, files=files, data=data)
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            result = response.json()
            return result.get("text", "Error: 'text' field not found in response.")
            
    except requests.exceptions.RequestException as e:
        return f"Error: Request failed: {e}"
    except ValueError: # Includes JSONDecodeError
        return "Error: Failed to decode JSON response."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

if __name__ == '__main__':
    # Example usage:
    # Create a dummy audio file for testing if it doesn't exist
    audio_file = "temp_audio.mp3"

    if os.path.exists(audio_file):
        print(f"Transcribing {audio_file}...")
        # Note: The dummy file will likely cause an error on the server side
        # as it's not a valid audio file.
        # Replace 'temp_audio.mp3' with a path to an actual audio file for a real test.
        transcribed_text = transcribe_audio_cpp(audio_file)
        print("\nTranscribed Text:")
        print(transcribed_text)
    else:
        print(f"Test file {audio_file} not found. Skipping example usage.")