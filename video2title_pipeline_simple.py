# filepath: /Users/zz/codes/title_generater/video2title_pipeline_simple.py
import os
import time
from video2mp3 import video_to_mp3
from whisper.whisper_cpp import transcribe_audio_cpp
from text2title import generate_title

def video2title_pipeline_simplified(video_file_path: str):
    """
    Simplified pipeline to convert video to title.
    Uses default parameters and whisper_cpp for transcription.
    """
    print(f"Starting simplified pipeline for: {video_file_path}")
    start_time = time.time()

    base_name = os.path.splitext(os.path.basename(video_file_path))[0]
    # Create a temporary audio file in the same directory as the script or a designated temp folder
    # For simplicity, placing it in the script's directory with a unique enough name.
    temp_audio_file = f"{base_name}_temp_audio_for_simple_pipeline.mp3"
    
    # Step 1: Convert video to MP3
    # Relies on default bitrate and other params in video_to_mp3
    print("\n[Step 1/3] Converting video to MP3...")
    if not video_to_mp3(video_file_path, temp_audio_file):
        print("Failed to convert video to MP3. Exiting.")
        return None
    print(f"Video converted to MP3: {temp_audio_file}")

    # Step 2: Transcribe audio to text using whisper_cpp
    # Relies on default parameters in transcribe_audio_cpp
    print("\n[Step 2/3] Transcribing audio to text using whisper_cpp...")
    transcribed_text = transcribe_audio_cpp(temp_audio_file)
    
    print(f"Transcript (first 200 chars): {transcribed_text[:200]}...") # Optional

    # Step 3: Generate title from text
    # Relies on default prompt and other params in generate_title
    print("\n[Step 3/3] Generating title from text...")
    title = generate_title(text=transcribed_text) 
    
    if not title:
        print("Failed to generate title.")
        # Cleanup even if title generation fails
        if os.path.exists(temp_audio_file):
            try:
                os.remove(temp_audio_file)
                print(f"Cleaned up temporary audio file: {temp_audio_file}")
            except OSError as e:
                print(f"Error deleting temporary audio file {temp_audio_file}: {e}")
        return None
    print(f"Generated Title: {title}")

    # Cleanup temporary audio file
    if os.path.exists(temp_audio_file):
        try:
            os.remove(temp_audio_file)
            print(f"Cleaned up temporary audio file: {temp_audio_file}")
        except OSError as e:
            print(f"Error deleting temporary audio file {temp_audio_file}: {e}")

    end_time = time.time()
    print(f"\nSimplified pipeline completed in {end_time - start_time:.2f} seconds.")
    return title

if __name__ == "__main__":
    # Ensure you have a 'test_video.mp4' in the same directory as this script,
    # or change the path.
    test_video = "test_video.mp4" 
    
    if not os.path.exists(test_video):
        print(f"Test video '{test_video}' not found. ")
        print("Please place a video file named 'test_video.mp4' in the script's directory,")
        print("or update the 'test_video' variable in the script.")
        print("You can create a dummy test video using ffmpeg, e.g.:")
        print("ffmpeg -f lavfi -i testsrc=duration=5:size=320x240:rate=25 -f lavfi -i anoisesrc=duration=5 -c:v libx264 -c:a aac -strict experimental -shortest test_video.mp4")
    else:
        print(f"Attempting to process video: {test_video}")
        generated_title = video2title_pipeline_simplified(test_video)
        if generated_title:
            print(f"\n>>> Successfully generated title: {generated_title}")
        else:
            print("\n>>> Pipeline failed to generate a title.")

    # Example with another common video name, if it exists
    # alternative_video = "video.mp4"
    # if os.path.exists(alternative_video) and alternative_video != test_video:
    #     print(f"\nAttempting to process video: {alternative_video}")
    #     generated_title_2 = video2title_pipeline_simplified(alternative_video)
    #     if generated_title_2:
    #         print(f"\n>>> Successfully generated title for {alternative_video}: {generated_title_2}")
    #     else:
    #         print(f"\n>>> Pipeline failed for {alternative_video}.")
    # elif alternative_video != test_video:
    #     print(f"\nAlternative video '{alternative_video}' not found, skipping second example.")

