llama-server -m model.gguf --port 8080

# Basic web UI can be accessed via browser: http://localhost:8080
# Chat completion endpoint: http://localhost:8080/v1/chat/completions


Qwen/Qwen3-0.6B-GGUF:Q8_0

llama-server -m model.gguf --port 8080


./llama-server -hf Qwen/Qwen3-8B-GGUF:Q8_0 --jinja --reasoning-format deepseek -ngl 99 -fa -sm row --temp 0.6 --top-k 20 --top-p 0.95 --min-p 0 -c 40960 -n 32768 --no-context-shift

llama-server -hf Qwen/Qwen3-8B-GGUF:Q8_0 --jinja --reasoning-format deepseek -ngl 99 -fa -sm row --temp 0.6 --top-k 20 --top-p 0.95 --min-p 0 -c 40960 -n 32768 --no-context-shift


llama-server -hf Qwen/Qwen3-0.6B-GGUF:Q8_0 --jinja --reasoning-format deepseek -ngl 99 -fa -sm row --temp 0.6 --top-k 20 --top-p 0.95 --min-p 0 -c 40960 -n 32768 --no-context-shift



llama-server -hf Qwen/Qwen2.5-0.5B-Instruct-GGUF


/Users/zz/Library/Caches/llama.cpp 默认存放的位置



# start a server

# simple usage with server
llama-server -hf ggml-org/gemma-3-4b-it-GGUF

# using local file
llama-server -m gemma-3-4b-it-Q4_K_M.gguf --mmproj mmproj-gemma-3-4b-it-Q4_K_M.gguf


### suing a alias

--alias llm
llama-server -m gemma-3-4b-it-Q4_K_M.gguf --alias llm

how to use openai api to connect to the server


### other options
 -c 2048 是上下文长度，你可以根据需求调。
    