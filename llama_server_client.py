#!/usr/bin/env python3
"""
A Python client for the llama-server API.

This script demonstrates how to make requests to the llama-server's chat completion endpoint.
The server follows an OpenAI-compatible API format.

Usage:
    python llama_server_client.py

Requirements:
    - requests library (pip install requests)
"""

import requests
import json
import argparse
import sys

# Default server configuration
DEFAULT_SERVER_URL = "http://localhost:8080"
DEFAULT_MODEL = "Qwen/Qwen3-0.6B-GGUF:Q8_0"  # Using one of the models from your server config

def chat_completion(server_url, messages, model=DEFAULT_MODEL, 
                    temperature=0.7, max_tokens=1024, 
                    stream=False, **kwargs):
    """
    Send a chat completion request to the llama-server.
    
    Args:
        server_url (str): URL of the llama-server
        messages (list): List of message objects with 'role' and 'content' keys
        model (str): Model identifier
        temperature (float): Sampling temperature (0.0 to 1.0)
        max_tokens (int): Maximum number of tokens to generate
        stream (bool): Whether to stream the response
        **kwargs: Additional parameters to pass to the API
        
    Returns:
        dict: The response from the server
    """
    endpoint = f"{server_url}/v1/chat/completions"
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": stream,
        **kwargs
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        if stream:
            response = requests.post(endpoint, json=payload, headers=headers, stream=True)
            response.raise_for_status()
            return response
        else:
            response = requests.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request to {endpoint}: {e}", file=sys.stderr)
        return {"error": str(e)}

def process_stream_response(response):
    """Process a streaming response from the server."""
    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8')
            if line.startswith("data: "):
                line = line[6:]  # Remove "data: " prefix
                if line.strip() == "[DONE]":
                    break
                try:
                    chunk = json.loads(line)
                    content = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
                    if content:
                        print(content, end="", flush=True)
                except json.JSONDecodeError:
                    print(f"Error parsing JSON: {line}", file=sys.stderr)
    print()  # Final newline after streaming completes

def main():
    parser = argparse.ArgumentParser(description="Client for llama-server API")
    parser.add_argument("--server", default=DEFAULT_SERVER_URL, help=f"Server URL (default: {DEFAULT_SERVER_URL})")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model name (default: {DEFAULT_MODEL})")
    parser.add_argument("--temp", type=float, default=0.6, help="Temperature (default: 0.6)")
    parser.add_argument("--max-tokens", type=int, default=1024, help="Max tokens to generate (default: 1024)")
    parser.add_argument("--stream", action="store_true", help="Stream the response")
    parser.add_argument("--prompt", help="Prompt to send to the model")
    parser.add_argument("--system", help="System message to provide context")
    
    args = parser.parse_args()
    
    # Get prompt from command line or input
    prompt = args.prompt
    if not prompt:
        print("Enter your prompt (Ctrl+D or Ctrl+Z to end):")
        prompt_lines = []
        try:
            for line in sys.stdin:
                prompt_lines.append(line)
        except KeyboardInterrupt:
            pass
        prompt = "".join(prompt_lines)
    
    # Prepare messages
    messages = []
    if args.system:
        messages.append({"role": "system", "content": args.system})
    messages.append({"role": "user", "content": prompt})
    
    print(f"\nSending request to {args.server} using model {args.model}...\n")
    
    # Send request
    if args.stream:
        response = chat_completion(
            args.server, messages, args.model, 
            temperature=args.temp, max_tokens=args.max_tokens, 
            stream=True
        )
        process_stream_response(response)
    else:
        response = chat_completion(
            args.server, messages, args.model, 
            temperature=args.temp, max_tokens=args.max_tokens
        )
        
        if "error" in response:
            print(f"Error: {response['error']}", file=sys.stderr)
        else:
            try:
                content = response["choices"][0]["message"]["content"]
                print(content)
            except (KeyError, IndexError):
                print("Unexpected response format:", file=sys.stderr)
                print(json.dumps(response, indent=2), file=sys.stderr)

if __name__ == "__main__":
    main()
