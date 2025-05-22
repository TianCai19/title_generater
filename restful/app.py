import base64
import os
import uuid
from flask import Flask, request, jsonify
import sys
import requests # Added for Llama.cpp server check

# Add the parent directory to the Python path to import video2title_pipeline
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from video2title_pipeline import video2title_pipeline

app = Flask(__name__)

# Ensure the temporary directory for videos exists
TEMP_VIDEO_DIR = "temp_videos"
if not os.path.exists(TEMP_VIDEO_DIR):
    os.makedirs(TEMP_VIDEO_DIR)

LLAMA_CPP_SERVER_URL = "http://localhost:8080/v1" # Llama.cpp server URL

def is_llama_cpp_server_running():
    """Checks if the Llama.cpp server is running and accessible."""
    try:
        # Attempt to connect to a known endpoint, e.g., /models (often available)
        # or just the base URL if it responds to simple GET requests.
        # Here, we try to get the models list, assuming it's a standard OpenAI-compatible API.
        response = requests.get(f"{LLAMA_CPP_SERVER_URL}/models", timeout=2)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


@app.route('/item/title_generate', methods=['POST'])
def title_generate():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No input data provided"}), 400

        video_b64 = data.get('video')
        if not video_b64:
            return jsonify({"success": False, "error": "Missing video data"}), 400

        video_data = base64.b64decode(video_b64)
        temp_video_filename = f"{uuid.uuid4()}.mp4"
        temp_video_path = os.path.join(TEMP_VIDEO_DIR, temp_video_filename)

        with open(temp_video_path, 'wb') as f:
            f.write(video_data)

        print(f"[Debug] Starting pipeline for video: {temp_video_path}")
        pipeline_result = video2title_pipeline(
            video_file=temp_video_path,
            whisper_model="tiny",
            model_dir="../models",
            title_prompt="根据以下视频内容，生成一个简短且吸引人的标题:",
            save_transcript=False
        )
        
        generated_title = pipeline_result.get("title", "")
        if not generated_title:
            return jsonify({"success": False, "error": "Title generation failed, no title returned"}), 500

        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)
        
        temp_audio_path = pipeline_result.get("audio_file")
        if temp_audio_path and os.path.exists(temp_audio_path):
            os.remove(temp_audio_path) if os.path.abspath(temp_audio_path).startswith(os.path.abspath(TEMP_VIDEO_DIR)) else None

        return jsonify({"success": True, "title": generated_title})

    except Exception as e:
        if 'temp_video_path' in locals() and os.path.exists(temp_video_path):
            os.remove(temp_video_path)
        print(f"[Error] Exception in title_generate: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
