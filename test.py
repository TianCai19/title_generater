import base64
import subprocess
import whisper
from llama_cpp import Llama
import time

# 计时装饰器
def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 耗时: {end_time - start_time:.2f} 秒")
        return result
    return wrapper

# 步骤1：Base64 解码
@timer_decorator
def decode_base64_video(base64_string, output_path):
    with open(output_path, "wb") as video_file:
        video_file.write(base64.b64decode(base64_string))
    return output_path

# 步骤2：提取音频
@timer_decorator
def extract_audio(video_path, audio_path):
    command = ["ffmpeg", "-i", video_path, "-vn", "-acodec", "copy", audio_path, "-y"]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return audio_path

# 步骤3：加速音频
@timer_decorator
def speed_up_audio(input_path, output_path, speed_factor=2.0):
    command = ["ffmpeg", "-i", input_path, "-filter:a", f"atempo={speed_factor}", "-vn", output_path, "-y"]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return output_path

# 步骤4：语音转文字
@timer_decorator
def speech_to_text(audio_path, model):
    result = model.transcribe(audio_path)
    return result["text"]

# 步骤5：生成标题
@timer_decorator
def generate_title(text, llm):
    prompt = f"基于以下歌词生成一个简洁的标题（不超过10个字）：\n{text}"
    response = llm(prompt, max_tokens=20, stop=["\n"], echo=False)
    return response["choices"][0]["text"].strip()

# 主函数
def main(base64_video_string):
    start_time = time.time()
  
    # 初始化模型（建议预加载，避免重复加载）
    whisper_model = whisper.load_model("tiny")
    llama_model = Llama(model_path="path_to_llama_3B_model.gguf", n_ctx=512)
  
    # 步骤1：解码 Base64
    video_path = "temp_video.mp4"
    decode_base64_video(base64_video_string, video_path)
  
    # 步骤2：提取音频
    audio_path = "temp_audio.mp3"
    extract_audio(video_path, audio_path)
  
    # 步骤3：加速音频
    fast_audio_path = "temp_audio_fast.mp3"
    speed_up_audio(audio_path, fast_audio_path, speed_factor=2.0)
  
    # 步骤4：语音转文字
    lyrics = speech_to_text(fast_audio_path, whisper_model)
    print(f"提取的歌词: {lyrics}")
  
    # 步骤5：生成标题
    title = generate_title(lyrics, llama_model)
    print(f"生成的标题: {title}")
  
    end_time = time.time()
    print(f"总耗时: {end_time - start_time:.2f} 秒")
    return title

if __name__ == "__main__":
    # 示例 Base64 字符串（实际使用时替换为真实数据）
    dummy_base64 = "placeholder_base64_string"
    main(dummy_base64)