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
                        save_transcript=True,
                        language=None,
                        sentence_count=None,
                        keep_intermediate_files=False):
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
        language (str, optional): 指定转录语言，None为自动检测
        sentence_count (int, optional): 使用的句子数量，None为全部
        keep_intermediate_files (bool, optional): 是否保留中间文件（音频、文本），默认为False
        
    返回：
        dict: 包含每个步骤结果的字典，包括音频路径、转录文本和生成的标题
    """
    result = {
        "video_file": video_file,
        "audio_file": None,
        "transcript": None,
        "title": None,
        "transcript_file": None,
        "sentences_file": None
    }

    # Determine audio output path if not provided
    # This ensures output_audio is always defined for cleanup logic
    actual_output_audio = output_audio
    if actual_output_audio is None:
        base_name = os.path.splitext(os.path.basename(video_file))[0]
        output_dir = os.path.dirname(video_file) if os.path.dirname(video_file) else "."
        actual_output_audio = os.path.join(output_dir, f"{base_name}_audio.mp3")

    try:
        # 步骤1: 视频转音频
        print(f"\n[步骤 1/3] 正在将视频转换为音频: {video_file} -> {actual_output_audio}")
        conversion_success = video_to_mp3(video_file, actual_output_audio, bitrate=audio_bitrate)
        
        if not conversion_success:
            print("视频转音频失败，流程终止")
            return result # audio_file in result is still None or the original if provided and failed
        
        result["audio_file"] = actual_output_audio
        
        # 步骤2: 音频转文本
        print(f"\n[步骤 2/3] 正在使用Whisper转录音频为文本: {actual_output_audio}")
        transcript, sentences, transcribe_time = whisper_transcribe(
            actual_output_audio, 
            model_name=whisper_model, 
            model_dir=model_dir,
            language=language,
            sentence_count=sentence_count
        )
        
        if not transcript:
            print("音频转文本失败，流程终止")
            return result # transcript in result is still None
        
        result["transcript"] = transcript
        result["sentences"] = sentences
        
        if save_transcript:
            audio_dir = os.path.dirname(result["audio_file"])
            audio_base_name = os.path.splitext(os.path.basename(result["audio_file"]))[0]
            
            transcript_f_path = os.path.join(audio_dir, f"{audio_base_name}.txt")
            sentences_f_path = os.path.join(audio_dir, f"{audio_base_name}_sentences.txt")
            
            result["transcript_file"] = transcript_f_path
            result["sentences_file"] = sentences_f_path

            with open(transcript_f_path, 'w', encoding='utf-8') as f:
                f.write(transcript)
            with open(sentences_f_path, 'w', encoding='utf-8') as f:
                for i, sentence in enumerate(sentences, 1):
                    f.write(f"[{i}] {sentence}\n")
                    
            print(f"转录文本已保存至: {transcript_f_path}")
            print(f"分句版本已保存至: {sentences_f_path}")
        
        # 步骤3: 文本生成标题
        print(f"\n[步骤 3/3] 根据转录文本生成标题")
        title = generate_title(prompt=title_prompt, text=transcript)
        
        if title:
            result["title"] = title
            print(f"\n生成的标题: {title}")
        else:
            print("标题生成失败")
        
        return result

    finally:
        # 清理中间文件
        if not keep_intermediate_files:
            # Check and delete audio file
            if result.get("audio_file") and os.path.exists(result["audio_file"]):
                print(f"Pipeline: Deleting intermediate audio file: {result['audio_file']}")
                os.remove(result["audio_file"])
            
            # Check and delete transcript file
            if result.get("transcript_file") and os.path.exists(result["transcript_file"]):
                print(f"Pipeline: Deleting intermediate transcript file: {result['transcript_file']}")
                os.remove(result["transcript_file"])

            # Check and delete sentences file
            if result.get("sentences_file") and os.path.exists(result["sentences_file"]):
                print(f"Pipeline: Deleting intermediate sentences file: {result['sentences_file']}")
                os.remove(result["sentences_file"])

if __name__ == "__main__":
    # 使用示例
    video_file = "test_video.mp4"  # 替换为你的视频文件路径
    
    # 简单调用，使用默认参数 (不保留中间文件)
    # print("\n=== 简单调用 (不保留中间文件) ===")
    # result_default = video2title_pipeline(video_file)
    # print(f"处理结果: {result_default['title']}")

    # 调用并保留中间文件
    print("\n=== 调用并保留中间文件 ===")
    result_keep_files = video2title_pipeline(
        video_file=video_file,
        keep_intermediate_files=True, # 设置为 True 来保留文件
        save_transcript=True, # Ensure transcripts are created to test keeping them
        whisper_model="tiny",
        language="zh"
    )
    print(f"处理结果 (保留文件): {result_keep_files['title']}")
    if result_keep_files.get("audio_file") and os.path.exists(result_keep_files.get("audio_file")) :
        print(f"音频文件: {result_keep_files['audio_file']}")
    if result_keep_files.get("transcript_file") and os.path.exists(result_keep_files.get("transcript_file")):
        print(f"文本文件: {result_keep_files['transcript_file']}")
    if result_keep_files.get("sentences_file") and os.path.exists(result_keep_files.get("sentences_file")):
        print(f"分句文件: {result_keep_files['sentences_file']}")

    # 调用并不保留中间文件 (显式设置)
    print("\n=== 调用并不保留中间文件 (显式设置) ===")
    result_delete_files = video2title_pipeline(
        video_file=video_file, # Use a different video or ensure it's recreated if needed
        keep_intermediate_files=False, 
        save_transcript=True, # Ensure transcripts are created to test deleting them
        whisper_model="tiny",
        language="zh"
    )
    print(f"处理结果 (删除文件): {result_delete_files['title']}")
    if result_delete_files.get("audio_file"):
         print(f"音频文件路径 (应已被删除): {result_delete_files['audio_file']}, Exists: {os.path.exists(result_delete_files['audio_file'])}")
    if result_delete_files.get("transcript_file"):
        print(f"文本文件路径 (应已被删除): {result_delete_files['transcript_file']}, Exists: {os.path.exists(result_delete_files['transcript_file'])}")
    if result_delete_files.get("sentences_file"):
        print(f"分句文件路径 (应已被删除): {result_delete_files['sentences_file']}, Exists: {os.path.exists(result_delete_files['sentences_file'])}")

    # 高级调用示例，自定义参数
    # print("\n=== 高级调用示例 (不保留中间文件) ===")
    # result_advanced = video2title_pipeline(
    #     video_file="test_video.mp4",
    #     audio_bitrate="128k",
    #     whisper_model="base", 
    #     title_prompt="prompt.txt",
    #     save_transcript=True, # 即使save_transcript为True，如果keep_intermediate_files为False，也会删除
    #     language="zh",
    #     sentence_count=5,
    #     keep_intermediate_files=False
    # )
    # print(f"高级调用处理结果: {result_advanced['title']}")
