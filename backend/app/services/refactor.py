import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('models/gemini-2.5-flash')

def refactor_code_logic(legacy_code: str):
    """
    Takes old, messy code and transforms it into Modern Python.
    """
    prompt = f"""
    You are a Senior Python Architect. 
    Refactor the following legacy function into production-grade Python 3.12.
    
    Requirements:
    1. Add Type Hints (e.g. def func(x: int) -> int).
    2. Add a Google-style Docstring.
    3. Rename variables if they are unclear (e.g. change 'x' to 'price').
    4. Return ONLY the raw code. Do not wrap it in markdown ticks (```).
    
    Legacy Code:
    {legacy_code}
    """
    
    try:
        response = model.generate_content(prompt)
        # Clean up any markdown formatting Gemini might accidentally add
        clean_code = response.text.replace("```python", "").replace("```", "").strip()
        return clean_code
    except Exception as e:
        return f"# Error refactoring code: {str(e)}"