"""
CPU 直跑、尽量快的 Whisper 中文示例
核心策略：
1. 选小型号（base）降低计算量
2. 直接调用 whisper.transcribe 自动切片，避免手动 pad_or_trim 截断
3. 禁用 fp16（CPU 不支持），保持全精度
"""


import logging

from timeit_decorator import timeit



import whisper

# Configure logging
logging.basicConfig(level=logging.INFO)

# 载入较小的 base 模型，全部放在 CPU 上
model = whisper.load_model("turbo")#, device="cpu")

# 一行搞定长音频转写（可传路径或 numpy 数组）
@timeit()
def transcribe_audio():
    result = whisper.transcribe(
        model,
        "temp_audio.mp3",      # 音频文件
        language="zh",    # 强制中文，避免误判
        task="transcribe",
        fp16=False,       # CPU 必须关掉半精度
        verbose=False     # 静默模式，控制台更干净
    )
    return result

result = transcribe_audio()

sentences = [segment['text'] for segment in result['segments']]


# 打印完整文本
print(sentences)

long_string = "\n".join(sentences[:6])


print("=====")
print(long_string)
# print(result)
