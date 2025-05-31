import subprocess
import os
import time

def video_to_mp3(input_file, output_file, bitrate="192k", start_time=None, duration=None):
    """
    将视频文件转换为 MP3 音频文件，支持裁剪指定时间段。
    :param input_file: 输入的视频文件路径
    :param output_file: 输出的 MP3 文件路径
    :param bitrate: 音频比特率，默认 192k
    :param start_time: 裁剪开始时间（例如 "00:00:00" 或秒数如 0），默认为 None (从头开始)
    :param duration: 裁剪持续时长（例如 "00:01:00" 或秒数如 60），默认为 None (到结尾)
    :return: 转换是否成功
    """
    # 启动计时
    process_start_time = time.time()

    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"错误：输入文件 {input_file} 不存在")
        return False

    # 构建 ffmpeg 命令
    command = ["ffmpeg"]

    # 如果指定了开始时间，将其添加到命令中（在 -i 之前，以便快速定位）
    if start_time is not None:
        command.extend(["-ss", str(start_time)])

    # 添加输入文件
    command.extend(["-i", input_file])

    # 如果指定了持续时长，将其添加到命令中
    if duration is not None:
        command.extend(["-t", str(duration)])

    # 添加其余的 ffmpeg 参数
    command.extend([
        "-vn",                   # 去掉视频流
        "-acodec", "libmp3lame", # 使用 MP3 编码
        "-ab", bitrate,          # 设置比特率
        "-ar", "16000",          # 设置采样率为 16 kHz（语音足够）
        "-preset", "ultrafast",  # 使用最快的编码预设（可能会稍微影响音质）
        "-y",                    # 自动覆盖输出文件
        output_file              # 输出文件
    ])

    try:
        # 执行命令并捕获输出
        # 使用 text=True (或 universal_newlines=True) 使 stdout 和 stderr 为字符串
        # check=False 允许我们手动检查 result.returncode
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
        # 结束计时
        process_end_time = time.time()
        execution_time = process_end_time - process_start_time

        if result.returncode == 0:
            print(f"成功转换 {input_file} 到 {output_file}")
            clip_details = []
            if start_time is not None:
                clip_details.append(f"从 {start_time} 开始")
            if duration is not None:
                clip_details.append(f"持续 {duration}")
            if clip_details:
                print(f"裁剪信息: {', '.join(clip_details)}")
            print(f"转换耗时: {execution_time:.2f} 秒")
            return True
        else:
            print(f"转换失败。FFmpeg 错误信息：\n{result.stderr}")
            print(f"执行的命令: {' '.join(command)}") # 打印执行的命令有助于调试
            print(f"尝试耗时: {execution_time:.2f} 秒")
            return False
    except FileNotFoundError:
        # 结束计时
        process_end_time = time.time()
        print("错误：未找到 ffmpeg，请确保已安装并添加到系统路径中")
        print(f"尝试耗时: {process_end_time - process_start_time:.2f} 秒")
        return False
    except Exception as e:
        # 结束计时
        process_end_time = time.time()
        print(f"发生错误：{e}")
        print(f"尝试耗时: {process_end_time - process_start_time:.2f} 秒")
        return False

# 示例用法
if __name__ == "__main__":
    # 确保你有一个名为 test_video.mp4 的文件，或者替换为你的视频文件路径
    # 为了使示例能运行，你可能需要创建一个虚拟的视频文件或使用一个实际存在的文件
    # 例如: ffmpeg -f lavfi -i testsrc=duration=120:size=1280x720:rate=30 -f lavfi -i sine=frequency=1000:duration=120 -c:v libx264 -c:a aac -shortest test_video.mp4
    
    input_video = "test_video.mp4"
    
    # 检查测试视频文件是否存在，如果不存在则提示
    if not os.path.exists(input_video):
        print(f"警告：测试视频文件 '{input_video}' 不存在。请创建它或修改脚本中的文件路径以便运行示例。")
        print("您可以使用以下 ffmpeg 命令创建一个2分钟的测试视频（如果已安装 ffmpeg）：")
        print("ffmpeg -f lavfi -i testsrc=duration=120:size=320x240:rate=25 -f lavfi -i anoisesrc=duration=120 -c:v libx264 -c:a aac -shortest test_video.mp4")
    else:
        output_audio_full = "test_audio_full.mp3"
        output_audio_first_minute = "test_audio_first_minute.mp3"
        output_audio_segment = "test_audio_segment.mp3"

        print(f"--- 转换 '{input_video}' 的完整音频 ---")
        video_to_mp3(input_video, output_audio_full, bitrate="128k")
        print("-" * 30)

        print(f"\n--- 转换 '{input_video}' 的前一分钟音频 (0s-60s) ---")
        # 提取前一分钟: start_time="0", duration="60"
        video_to_mp3(input_video, output_audio_first_minute, bitrate="64k", start_time="0", duration="60")
        print("-" * 30)

        print(f"\n--- 转换 '{input_video}' 从第10秒开始，持续30秒的音频片段 ---")
        # 提取从第10秒开始，持续30秒的片段: start_time="10", duration="30"
        # 时间也可以用 "HH:MM:SS" 格式，例如 start_time="00:00:10", duration="00:00:30"
        video_to_mp3(input_video, output_audio_segment, bitrate="64k", start_time="10", duration="30")
        print("-" * 30)

        print(f"\n--- 转换 '{input_video}' 从第1分30秒开始，到视频结尾的音频片段 ---")
        # 提取从第1分30秒 (90秒) 开始到结尾: start_time="90" (或 "00:01:30"), duration=None
        output_audio_from_90s = "test_audio_from_90s_to_end.mp3"
        video_to_mp3(input_video, output_audio_from_90s, bitrate="64k", start_time="90")
        print("-" * 30)