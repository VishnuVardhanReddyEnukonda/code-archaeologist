import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('models/gemini-2.5-flash')

def generate_unit_tests(code_snippet: str):
    """
    Analyzes code and generates a complete unittest suite.
    """
    prompt = f"""
    You are a QA Automation Engineer. 
    Write a Python 'unittest' class to test the following function.
    
    Requirements:
    1. Include at least 3 test cases: a standard case, an edge case, and a failure case.
    2. Use 'unittest.TestCase'.
    3. Return ONLY the raw python code. No markdown.
    
    Function to test:
    {code_snippet}
    """
    
    try:
        response = model.generate_content(prompt)
        clean_code = response.text.replace("```python", "").replace("```", "").strip()
        return clean_code
    except Exception as e:
        return f"# Error generating tests: {str(e)}"