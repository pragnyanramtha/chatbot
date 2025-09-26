#!/usr/bin/env python3
"""
Script to check available Gemini models
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_available_models():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable is required")
        return
    
    genai.configure(api_key=api_key)
    
    try:
        print("Fetching available models...")
        models = genai.list_models()
        
        print("\nAvailable Gemini models:")
        print("-" * 50)
        
        for model in models:
            print(f"Name: {model.name}")
            if hasattr(model, 'display_name'):
                print(f"Display Name: {model.display_name}")
            if hasattr(model, 'description'):
                print(f"Description: {model.description}")
            if hasattr(model, 'supported_generation_methods'):
                print(f"Supported methods: {model.supported_generation_methods}")
            print("-" * 30)
            
    except Exception as e:
        print(f"Error fetching models: {e}")

if __name__ == "__main__":
    check_available_models()