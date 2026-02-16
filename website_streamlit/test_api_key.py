#!/usr/bin/env python3
"""
Test script to check OpenAI API key status and quota
"""

import os
from openai import OpenAI

# Try to read API key from application.properties
properties_path = os.path.join(
    os.path.dirname(__file__), 
    "springboot_backend", 
    "src", 
    "main", 
    "resources", 
    "application.properties"
)

openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    try:
        with open(properties_path, 'r') as f:
            for line in f:
                if line.startswith('openai.api.key='):
                    openai_api_key = line.split('=', 1)[1].strip()
                    break
    except Exception as e:
        print(f"Error reading application.properties: {e}")
        exit(1)

if not openai_api_key:
    print("❌ No API key found!")
    exit(1)

print(f"✅ API key found: {openai_api_key[:15]}...")
print("\nTesting API key...\n")

client = OpenAI(api_key=openai_api_key)

try:
    # Try a simple API call
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Say 'API key is working' if you can read this."}
        ],
        max_tokens=10
    )
    
    print("✅ SUCCESS! API key is working!")
    print(f"Response: {response.choices[0].message.content}")
    print("\nYour API key has quota available and is functioning correctly.")
    
except Exception as e:
    error_str = str(e)
    print(f"❌ ERROR: {error_str}\n")
    
    if "insufficient_quota" in error_str or "429" in error_str:
        print("=" * 60)
        print("QUOTA ERROR DETECTED")
        print("=" * 60)
        print("\nYour API key has insufficient quota. This usually means:")
        print("\n1. Free tier credits ($5) have been used up")
        print("2. Billing information needs to be added")
        print("   (Sometimes even free tier requires billing info)")
        print("3. Account needs a payment method")
        print("4. API key may have been disabled")
        print("\n" + "=" * 60)
        print("WHAT TO DO:")
        print("=" * 60)
        print("\n1. Check your usage: https://platform.openai.com/usage")
        print("2. Check your billing: https://platform.openai.com/account/billing")
        print("3. Add payment method if needed: https://platform.openai.com/account/billing")
        print("4. Verify API key is active: https://platform.openai.com/api-keys")
        print("\nNote: Even with free credits, OpenAI sometimes requires")
        print("billing information to be added to your account.")
        print("=" * 60)
    elif "invalid_api_key" in error_str or "401" in error_str:
        print("❌ Invalid API Key")
        print("Please verify your API key at: https://platform.openai.com/api-keys")
    else:
        print(f"Unexpected error: {error_str}")


