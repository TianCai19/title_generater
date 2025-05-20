llama-server -m model.gguf --port 8080

# Basic web UI can be accessed via browser: http://localhost:8080
# Chat completion endpoint: http://localhost:8080/v1/chat/completions


Qwen/Qwen3-0.6B-GGUF:Q8_0

llama-server -m model.gguf --port 8080


./llama-server -hf Qwen/Qwen3-8B-GGUF:Q8_0 --jinja --reasoning-format deepseek -ngl 99 -fa -sm row --temp 0.6 --top-k 20 --top-p 0.95 --min-p 0 -c 40960 -n 32768 --no-context-shift

llama-server -hf Qwen/Qwen3-8B-GGUF:Q8_0 --jinja --reasoning-format deepseek -ngl 99 -fa -sm row --temp 0.6 --top-k 20 --top-p 0.95 --min-p 0 -c 40960 -n 32768 --no-context-shift


llama-server -hf Qwen/Qwen3-0.6B-GGUF:Q8_0 --jinja --reasoning-format deepseek -ngl 99 -fa -sm row --temp 0.6 --top-k 20 --top-p 0.95 --min-p 0 -c 40960 -n 32768 --no-context-shift