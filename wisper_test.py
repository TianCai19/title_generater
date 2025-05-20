import whisper
import time
import os
from video2mp3 import video_to_mp3

def whisper_transcribe(audio_file, model_name="tiny", model_dir="models"):
    """
    使用 Whisper 模型将音频文件转换为文本
    :param audio_file: 输入的音频文件路径
    :param model_name: 模型名称，默认为 "tiny"
    :param model_dir: 模型存储目录，默认为 "models"
    :return: 转录的文本内容和执行时间
    """
    start_time = time.time()
    
    # 检查输入文件是否存在
    if not os.path.exists(audio_file):
        print(f"错误：输入文件 {audio_file} 不存在")
        return None, 0
        
    try:
        # 加载模型
        model = whisper.load_model(model_name, download_root=model_dir)
        
        # 转录音频
        result = model.transcribe(audio_file)
        
        # 计算执行时间
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"音频转文本耗时: {execution_time:.2f} 秒")
        return result["text"], execution_time
    
    except Exception as e:
        end_time = time.time()
        print(f"转录过程中发生错误: {e}")
        print(f"尝试耗时: {end_time - start_time:.2f} 秒")
        return None, end_time - start_time

def video_to_text(video_file, temp_audio_file="temp_audio.mp3", model_name="tiny", model_dir="models", bitrate="64k"):
    """
    将视频文件转换为文本的完整流程（视频->音频->文本）
    :param video_file: 输入的视频文件路径
    :param temp_audio_file: 临时音频文件路径
    :param model_name: Whisper 模型名称
    :param model_dir: 模型存储目录
    :param bitrate: 音频比特率
    :return: 转录的文本内容、总执行时间、音频提取时间和转录时间
    """
    start_time = time.time()
    
    # 步骤1: 视频转音频
    print(f"步骤1: 正在将视频 '{video_file}' 转换为音频...")
    audio_success = video_to_mp3(video_file, temp_audio_file, bitrate)
    audio_end_time = time.time()
    audio_time = audio_end_time - start_time
    
    if not audio_success:
        return None, 0, audio_time, 0
    
    # 步骤2: 音频转文本
    print(f"步骤2: 正在将音频转换为文本...")
    text_result, transcribe_time = whisper_transcribe(temp_audio_file, model_name, model_dir)
    
    # 计算总执行时间
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"完整处理耗时: {total_time:.2f} 秒")
    return text_result, total_time, audio_time, transcribe_time

if __name__ == "__main__":
    # 示例用法1: 仅转录音频
    print("\n=== 音频转文本测试 ===")
    text, time_taken = whisper_transcribe("audio.mp3")
    if text:
        print(f"转录结果: {text}")
    
    # 示例用法2: 完整视频到文本流程
    print("\n=== 视频转文本测试 ===")
    input_video = "test_video.mp4"  # 替换为你的视频文件路径
    text, total_time, audio_time, transcribe_time = video_to_text(input_video)
    if text:
        print(f"视频转录结果: {text}")
        print(f"音频提取耗时: {audio_time:.2f} 秒")
        print(f"文本转录耗时: {transcribe_time:.2f} 秒")
        print(f"总耗时: {total_time:.2f} 秒")