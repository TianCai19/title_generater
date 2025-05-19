import subprocess
import os
import time  # 添加time模块导入

def video_to_mp3(input_file, output_file, bitrate="192k"):
    """
    将视频文件转换为 MP3 音频文件
    :param input_file: 输入的视频文件路径
    :param output_file: 输出的 MP3 文件路径
    :param bitrate: 音频比特率，默认 192k
    :return: 转换是否成功
    """
    # 启动计时
    start_time = time.time()
    
    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"错误：输入文件 {input_file} 不存在")
        return False

    # 构建 ffmpeg 命令
    command_old = [
        "ffmpeg",
        "-i", input_file,        # 输入文件
        "-vn",                   # 去掉视频流
        "-acodec", "libmp3lame", # 使用 MP3 编码
        "-ab", bitrate,          # 设置比特率
        "-y",                    # 自动覆盖输出文件
        output_file              # 输出文件
    ]

    command = [
    "ffmpeg",
    "-i", input_file,        # 输入文件
    "-vn",                   # 去掉视频流
    "-acodec", "libmp3lame", # 使用 MP3 编码
    "-ab", bitrate,          # 设置比特率
    "-ar", "16000",          # 设置采样率为 16 kHz（语音足够）
    "-preset", "ultrafast",  # 使用最快的编码预设（可能会稍微影响音质）
    "-y",                    # 自动覆盖输出文件
    output_file              # 输出文件
]

    
    try:
        # 执行命令并捕获输出
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # 结束计时
        end_time = time.time()
        execution_time = end_time - start_time
        
        if result.returncode == 0:
            print(f"成功转换 {input_file} 到 {output_file}")
            print(f"转换耗时: {execution_time:.2f} 秒")
            return True
        else:
            print(f"转换失败：{result.stderr}")
            print(f"尝试耗时: {execution_time:.2f} 秒")
            return False
    except FileNotFoundError:
        # 结束计时
        end_time = time.time()
        print("错误：未找到 ffmpeg，请确保已安装并添加到系统路径中")
        print(f"尝试耗时: {end_time - start_time:.2f} 秒")
        return False
    except Exception as e:
        # 结束计时
        end_time = time.time()
        print(f"发生错误：{e}")
        print(f"尝试耗时: {end_time - start_time:.2f} 秒")
        return False

# 示例用法
if __name__ == "__main__":
    input_video = "test_video.mp4"  # 替换为你的视频文件路径
    output_audio = "myaudio.mp3"  # 替换为输出的 MP3 文件路径
    video_to_mp3(input_video, output_audio, bitrate="64k")
