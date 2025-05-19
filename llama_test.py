# 使用Python调用llama-cli  
import os  
import subprocess  
  
model_path = "./models/qwen2.5-coder-0.5b-q8_0.gguf"  
prompt = "写一个计算斐波那契数列的Python函数"  
  
# 调用llama-cli  
result = subprocess.run(  
    ["./llama-cli", "-m", model_path, "-p", prompt, "-n", "512", "-no-cnv"],  
    capture_output=True,  
    text=True  
)  
  
# 打印输出  
print(result.stdout)