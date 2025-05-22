#!/bin/sh
set -e

echo "Starting llama-server on port 8080..."
# Create a log directory if it doesn't exist
mkdir -p /app/logs

# Redirect stdout and stderr to files
llama-server -hf Qwen/Qwen2.5-0.5B-Instruct-GGUF --alias llm --port 8080 > /app/logs/llama_server.log 2> /app/logs/llama_server_error.log &

echo "Starting Flask app on port 80..."
exec python /app/restful/app.py