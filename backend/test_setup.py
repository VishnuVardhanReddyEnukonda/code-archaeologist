import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: API Key not found!")
else:
    print(f"✅ Key found: {api_key[:5]}...")
    genai.configure(api_key=api_key)
    
    try:
        # UPDATED: Using the model available in your list
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        response = model.generate_content("Say 'Systems Functional' if you can hear me.")
        print(f"🤖 Gemini says: {response.text}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")