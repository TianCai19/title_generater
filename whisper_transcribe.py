import whisper
import time
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)

def whisper_transcribe(audio_file, model_name="tiny", model_dir="models", 
                      language=None, sentence_count=None, fp16=False):
    """
    使用 Whisper 模型将音频文件转换为文本，返回句子列表和完整文本
    
    参数：
        audio_file: 输入的音频文件路径
        model_name: 模型名称，默认为 "tiny"
        model_dir: 模型存储目录，默认为 "models"
        language: 指定语言，如 "zh"（中文），None 为自动检测
        sentence_count: 返回的句子数量，None 表示全部返回
        fp16: 是否使用半精度，CPU 上应设为 False
        
    返回：
        tuple: (完整文本, 句子列表, 执行时间)
    """
    start_time = time.time()
    
    # 检查输入文件是否存在
    if not os.path.exists(audio_file):
        print(f"[Whisper] 错误：输入文件 {audio_file} 不存在")
        return None, None, 0
        
    try:
        # 加载模型
        print(f"[Whisper] 正在加载 {model_name} 模型...")
        model = whisper.load_model(model_name, download_root=model_dir)
        print(f"[Whisper] 模型加载完成，使用模型: {model_name}")
        
        # 转录音频
        print(f"[Whisper] 开始转录音频: {os.path.basename(audio_file)}")
        
        # 准备转录参数
        transcribe_options = {
            "task": "transcribe",
            "verbose": False,
            "fp16": fp16
        }
        
        # 如果指定了语言，添加语言参数
        if language:
            transcribe_options["language"] = language
            
        # 进行转录
        result = model.transcribe(audio_file, **transcribe_options)
        
        # 提取句子列表
        sentences = [segment['text'] for segment in result['segments']]
        
        # 限制句子数量
        if sentence_count and isinstance(sentence_count, int) and 0 < sentence_count < len(sentences):
            selected_sentences = sentences[:sentence_count]
        else:
            selected_sentences = sentences
            
        # 将所选句子拼接为完整文本
        full_text = "\n".join(selected_sentences)
        
        # 计算执行时间
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"[Whisper] 转录完成！得到 {len(sentences)} 个句子")
        print(f"[Whisper] 音频转文本耗时: {execution_time:.2f} 秒")
        
        return full_text, sentences, execution_time
    
    except Exception as e:
        end_time = time.time()
        print(f"[Whisper] 转录过程中发生错误: {e}")
        print(f"[Whisper] 尝试耗时: {end_time - start_time:.2f} 秒")
        return None, None, end_time - start_time

if __name__ == "__main__":
    # 示例用法: 音频转文本测试
    audio_file = "temp_audio.mp3"  # 替换为你的音频文件路径
    
    # 基本用法示例
    print("\n=== 基本用法示例 ===")
    text, sentences, time_taken = whisper_transcribe(audio_file)
    if text:
        print(f"完整转录结果 (共 {len(sentences)} 句):\n{text}")
    
    # 高级用法示例：指定语言为中文，只取前5句
    print("\n=== 高级用法示例 ===")
    text_zh, sentences_zh, time_zh = whisper_transcribe(
        audio_file, 
        model_name="base", 
        language="zh",
        sentence_count=5
    )
    if text_zh:
        print(f"仅前5句 (中文模式):\n{text_zh}")
        
    # 提取特定句子示例
    if sentences and len(sentences) > 2:
        print("\n=== 提取特定句子示例 ===")
        # 提取第一句和最后一句，拼接
        first_last = f"开头: {sentences[0]}\n结尾: {sentences[-1]}"
        print(first_last)