#!/bin/sh
set -e

echo "Starting llama-server on port 8080..."
# Create a log directory if it doesn't exist
mkdir -p /logs

# Redirect stdout and stderr to files
llama-server -hf Qwen/Qwen2.5-0.5B-Instruct-GGUF --alias llm --port 8080 > logs/llama_server.log 2> logs/llama_server_error.log &

echo "Starting Flask app on port 80..."
python restful/app.py