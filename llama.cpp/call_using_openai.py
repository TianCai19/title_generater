import openai

# 初始化客户端，base_url 指向你的服务器地址和端口
client = openai.OpenAI(base_url="http://localhost:8080/v1", api_key="sk-no-key-required")

response = client.completions.create(
    model="llm",  # 对应启动时设置的 --alias
    prompt="Write a short poem about AI.",
    max_tokens=50,
    temperature=0.7,
)

print(response.choices[0].text)
