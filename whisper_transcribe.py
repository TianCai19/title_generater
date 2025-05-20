import whisper
import time
import os

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
        print(f"[Whisper] 正在加载 {model_name} 模型...")
        model = whisper.load_model(model_name, download_root=model_dir)
        print(f"[Whisper] 模型加载完成，使用模型: {model_name}")
        
        # 转录音频
        print(f"[Whisper] 开始转录音频: {os.path.basename(audio_file)}")
        result = model.transcribe(audio_file)
          # 计算执行时间
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"[Whisper] 转录完成！")
        print(f"[Whisper] 音频转文本耗时: {execution_time:.2f} 秒")
        return result["text"], execution_time
    
    except Exception as e:
        end_time = time.time()
        print(f"[Whisper] 转录过程中发生错误: {e}")
        print(f"[Whisper] 尝试耗时: {end_time - start_time:.2f} 秒")
        return None, end_time - start_time

if __name__ == "__main__":
    # 示例用法: 音频转文本测试
    audio_file = "temp_audio.mp3"  # 替换为你的音频文件路径
    text, time_taken = whisper_transcribe(audio_file)
    if text:
        print(f"转录结果: {text}")