#!/usr/bin/env python3
"""
Example usage of the llama server client for text generation tasks.

This script demonstrates how to use the llama-server client 
for various text generation tasks like title generation, summarization,
and question answering.
"""

import sys
import os
from llama_server_client import chat_completion

# Configure the server
SERVER_URL = "http://localhost:8080"
MODEL = "Qwen/Qwen3-0.6B-GGUF:Q8_0"  # Change to match your loaded model

def generate_title(text):
    """Generate a title for the given text."""
    messages = [
        {
            "role": "system",
            "content": "You are an expert at creating concise, engaging titles. "
                      "Create a title that captures the main idea of the text."
        },
        {"role": "user", "content": f"Please create a title for this text:\n{text}"}
    ]
    
    response = chat_completion(SERVER_URL, messages, MODEL, temperature=0.7, max_tokens=50)
    
    if "error" in response:
        return f"Error: {response['error']}"
    
    try:
        title = response["choices"][0]["message"]["content"].strip()
        return title
    except (KeyError, IndexError) as e:
        return f"Error processing response: {e}"

def summarize_text(text):
    """Generate a summary for the given text."""
    messages = [
        {
            "role": "system",
            "content": "You are an expert summarizer. Create a concise summary that captures "
                      "the key points of the text."
        },
        {"role": "user", "content": f"Please summarize this text:\n{text}"}
    ]
    
    response = chat_completion(SERVER_URL, messages, MODEL, temperature=0.5, max_tokens=200)
    
    if "error" in response:
        return f"Error: {response['error']}"
    
    try:
        summary = response["choices"][0]["message"]["content"].strip()
        return summary
    except (KeyError, IndexError) as e:
        return f"Error processing response: {e}"

def answer_question(context, question):
    """Answer a question based on the provided context."""
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that answers questions based only on the provided context."
        },
        {
            "role": "user", 
            "content": f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
        }
    ]
    
    response = chat_completion(SERVER_URL, messages, MODEL, temperature=0.3, max_tokens=300)
    
    if "error" in response:
        return f"Error: {response['error']}"
    
    try:
        answer = response["choices"][0]["message"]["content"].strip()
        return answer
    except (KeyError, IndexError) as e:
        return f"Error processing response: {e}"

def main():
    # Example usage with a sample text
    sample_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, 
    as opposed to the natural intelligence displayed by humans or animals. 
    Leading AI textbooks define the field as the study of "intelligent agents": 
    any system that perceives its environment and takes actions that maximize 
    its chance of achieving its goals. Some popular accounts use the term 
    "artificial intelligence" to describe machines that mimic "cognitive" 
    functions that humans associate with the human mind, such as "learning" 
    and "problem solving".
    """
    
    # Generate a title
    print("Generating title...")
    title = generate_title(sample_text)
    print(f"Title: {title}\n")
    
    # Generate a summary
    print("Generating summary...")
    summary = summarize_text(sample_text)
    print(f"Summary: {summary}\n")
    
    # Answer a question
    question = "What is the definition of AI according to leading textbooks?"
    print(f"Question: {question}")
    answer = answer_question(sample_text, question)
    print(f"Answer: {answer}")

if __name__ == "__main__":
    main()
