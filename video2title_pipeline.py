#!/usr/bin/env python3
# filepath: /Users/zz/codes/title_generater/video2title_pipeline.py

import os
import time
from video2mp3 import video_to_mp3
from whisper_transcribe import whisper_transcribe
from text2title import generate_title

def time_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[Timing] {func.__name__} 执行耗时 {end - start:.4f} 秒")
        return result
    return wrapper

@time_decorator
def video2title_pipeline(video_file, 
                        output_audio=None, 
                        audio_bitrate="64k", 
                        whisper_model="tiny", 
                        model_dir="models",
                        title_prompt="根据以下视频内容，生成一个简短且吸引人的标题:",
                        save_transcript=True):
    """
    完整的视频转标题流水线：将视频转为音频，然后转录为文本，最后生成标题
    
    参数：
        video_file (str): 输入视频文件的路径
        output_audio (str, optional): 输出的音频文件路径，若为None则自动生成
        audio_bitrate (str, optional): 音频比特率，默认为"64k"
        whisper_model (str, optional): Whisper模型名称，默认为"tiny"
        model_dir (str, optional): 模型存储目录，默认为"models"
        title_prompt (str, optional): 生成标题使用的提示词
        save_transcript (bool, optional): 是否保存转录文本，默认为True
        
    返回：
        dict: 包含每个步骤结果的字典，包括音频路径、转录文本和生成的标题
    """
    result = {
        "video_file": video_file,
        "audio_file": None,
        "transcript": None,
        "title": None
    }
    
    # 步骤1: 视频转音频
    if output_audio is None:
        base_name = os.path.splitext(os.path.basename(video_file))[0]
        output_audio = f"{base_name}_audio.mp3"
    
    print(f"\n[步骤 1/3] 正在将视频转换为音频: {video_file} -> {output_audio}")
    conversion_success = video_to_mp3(video_file, output_audio, bitrate=audio_bitrate)
    
    if not conversion_success:
        print("视频转音频失败，流程终止")
        return result
    
    result["audio_file"] = output_audio
    
    # 步骤2: 音频转文本
    print(f"\n[步骤 2/3] 正在使用Whisper转录音频为文本: {output_audio}")
    transcript, transcribe_time = whisper_transcribe(output_audio, model_name=whisper_model, model_dir=model_dir)
    
    if not transcript:
        print("音频转文本失败，流程终止")
        return result
    
    result["transcript"] = transcript
    
    # 如果需要保存转录文本
    if save_transcript:
        transcript_file = f"{os.path.splitext(output_audio)[0]}.txt"
        with open(transcript_file, 'w', encoding='utf-8') as f:
            f.write(transcript)
        print(f"转录文本已保存至: {transcript_file}")
    
    # 步骤3: 文本生成标题
    print(f"\n[步骤 3/3] 根据转录文本生成标题")
    title = generate_title(prompt=title_prompt, text=transcript)
    
    if title:
        result["title"] = title
        print(f"\n生成的标题: {title}")
    else:
        print("标题生成失败")
    
    return result


if __name__ == "__main__":
    # 使用示例
    video_file = "test_video.mp4"  # 替换为你的视频文件路径
    
    # 简单调用，使用默认参数
    result = video2title_pipeline(video_file)
    
    print("\n" + "="*50)
    print(f"处理结果摘要:")
    print(f"视频文件: {result['video_file']}")
    print(f"音频文件: {result['audio_file']}")
    if result['transcript']:
        print(f"转录文本: {result['transcript'][:100]}...")
    print(f"生成标题: {result['title']}")
    print("="*50)
    
    # 高级调用示例，自定义参数
    """
    result = video2title_pipeline(
        video_file="video.mp4",
        output_audio="custom_audio.mp3", 
        audio_bitrate="128k",
        whisper_model="small", 
        model_dir="my_models",
        title_prompt="创建一个富有创意且吸引人的标题:",
        save_transcript=True
    )
    """
