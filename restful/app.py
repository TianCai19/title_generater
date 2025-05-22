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
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No input data provided"}), 400

    video_b64 = data.get('video')
    if not video_b64:
        return jsonify({"success": False, "error": "Missing video data"}), 400
    
    keep_intermediate_files = data.get('keep_intermediate_files', True)

    temp_video_path = None # Initialize to None
    try:
        video_data = base64.b64decode(video_b64)
        temp_video_filename = f"{uuid.uuid4()}.mp4"
        temp_video_path = os.path.join(TEMP_VIDEO_DIR, temp_video_filename)

        with open(temp_video_path, 'wb') as f:
            f.write(video_data)

        print(f"[Debug] Starting pipeline for video: {temp_video_path}")
        pipeline_result = video2title_pipeline(
            video_file=temp_video_path,
            whisper_model="tiny",
            model_dir="../models", # This path is relative to restful/app.py, adjust if pipeline expects absolute or different relative
            title_prompt="根据以下视频内容，生成一个简短且吸引人的标题:",
            # save_transcript is True by default in pipeline, so intermediate text files will be created 
            # and then handled by keep_intermediate_files logic within the pipeline.
            # No need to set save_transcript=False here unless specifically intended to never save them.
            keep_intermediate_files=keep_intermediate_files 
        )
        
        generated_title = pipeline_result.get("title", "")
        if not generated_title:
            # pipeline_result will contain paths to intermediate files if created.
            # The pipeline's finally block should handle their deletion if keep_intermediate_files is False.
            return jsonify({"success": False, "error": "Title generation failed, no title returned"}), 500

        return jsonify({"success": True, "title": generated_title})

    except Exception as e:
        print(f"[Error] Exception in title_generate: {str(e)}")
        # The pipeline's finally block should attempt to clean its own intermediate files.
        # We only need to worry about the temp_video_path created in this function.
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        # Always remove the uploaded temp video file created by the app
        if temp_video_path and os.path.exists(temp_video_path):
            print(f"[Debug] App: Deleting temporary uploaded video file: {temp_video_path}")
            os.remove(temp_video_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
