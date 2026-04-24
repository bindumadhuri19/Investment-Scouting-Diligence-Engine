"""
Test script to check which Claude models are available with your API key.
Run this to determine the correct model name for your account.
"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

def test_claude_models():
    """Test which Claude models are accessible."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found in .env file")
        return
    
    print("🔍 Testing Claude API models...\n")
    
    # Models to test (from newest to oldest)
    models = [
        "claude-3-5-sonnet-20240620",
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307",
    ]
    
    client = Anthropic(api_key=api_key)
    
    working_models = []
    
    for model in models:
        try:
            # Simple test message
            message = client.messages.create(
                model=model,
                max_tokens=50,
                messages=[{
                    "role": "user",
                    "content": "Respond with just: OK"
                }]
            )
            
            response_text = message.content[0].text
            print(f"✅ {model}")
            print(f"   Response: {response_text}")
            working_models.append(model)
            
        except Exception as e:
            error_msg = str(e)
            if "not_found_error" in error_msg:
                print(f"❌ {model} - NOT FOUND")
            elif "authentication_error" in error_msg:
                print(f"❌ {model} - AUTH ERROR (check API key)")
            elif "permission_error" in error_msg:
                print(f"⚠️  {model} - NO PERMISSION (upgrade tier needed)")
            else:
                print(f"❌ {model} - ERROR: {error_msg[:100]}")
    
    print("\n" + "="*60)
    if working_models:
        print(f"✅ Working models found: {len(working_models)}")
        print(f"📝 Recommended model: {working_models[0]}")
        print(f"\nTo use this model, update tools/synthesize_with_claude.py")
    else:
        print("❌ No working models found!")
        print("   Check your API key and account tier")
        print("   Visit: https://docs.anthropic.com/en/docs/models-overview")
    print("="*60)


if __name__ == "__main__":
    test_claude_models()
