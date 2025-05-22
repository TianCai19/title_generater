import time
import openai
import os

client = openai.OpenAI(base_url="http://localhost:8080/v1", api_key="sk-no-key-required")

def time_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[Timing] {func.__name__} executed in {end - start:.4f} seconds.")
        return result
    return wrapper

def log_io(prompt_content, text_content, title):
    """Log the input and output for debugging purposes"""
    print("\n" + "="*50)
    print("[INPUT - Prompt]:")
    print(prompt_content[:200] + "..." if len(prompt_content) > 200 else prompt_content)
    print("\n[INPUT - Text]:")
    print(text_content[:200] + "..." if len(text_content) > 200 else text_content)
    print("\n[OUTPUT - Title]:")
    print(title)
    print("="*50 + "\n")

@time_decorator
def generate_title(prompt=None, text=None):
    def _read_if_file(param):
        if param is None:
            return None
        if os.path.isfile(param):
            with open(param, 'r', encoding='utf-8') as f:
                return f.read()
        return param

    prompt_content = _read_if_file(prompt) or "Generate a title based on the following text:"
    text_content = _read_if_file(text) or ""
    full_prompt = f"{prompt_content}\n\n{text_content}"

    print(f"[Debug] Generating title with prompt length: {len(prompt_content)}, text length: {len(text_content)}")
    try:
        print(f"[Debug] Sending request to Llama.cpp API at {client.base_url}")
        response = client.completions.create(
            model="llm",
            prompt=full_prompt,
            max_tokens=20,
            temperature=0.7,
        )
        title = response.choices[0].text.strip()
        log_io(prompt_content, text_content, title)
        return title
    except Exception as e:
        print(f"[Error] Failed to generate title: {str(e)}")
        raise  # 重新抛出异常以便 Flask 视图函数捕获


if __name__ == "__main__":
    # 例子1：直接传字符串
    # title1 = generate_title(prompt="Create a concise title:", text="This is a sample text to generate a title for.")
    # print("Generated Title 1:", title1)

    # 例子2：传文件路径（假设当前目录有 prompt.txt 和 document.txt 两个文件）
    # prompt.txt 内容示例： "Create a creative title based on the text below:"
    # document.txt 内容示例： "Artificial Intelligence is transforming the world rapidly."
    title2 = generate_title(prompt="prompt.txt", text="test_video_audio.txt")
    
    print("Generated Title 2:", title2)
