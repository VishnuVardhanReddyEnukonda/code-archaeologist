import os
import google.generativeai as genai
from neo4j import GraphDatabase
from dotenv import load_dotenv
from app.services.parser import extract_functions

# Setup
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('models/gemini-2.5-flash')

uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
auth = (os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "password123"))
driver = GraphDatabase.driver(uri, auth=auth)

def analyze_function(func_code):
    """Asks Gemini to explain a SINGLE function."""
    prompt = f"Explain this Python function in one specific sentence:\n\n{func_code}"
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except:
        return "Analysis failed."

def ingest_code_snippet(filename, code_content):
    print(f"🚀 Parsing Structure of {filename}...")
    
    # 1. Use Tree-Sitter to slice the code
    code_bytes = bytes(code_content, "utf8")
    functions = extract_functions(code_bytes)
    print(f"   found {len(functions)} functions.")

    # 2. Database Logic
    with driver.session() as session:
        # A. Create the File Node
        session.run("MERGE (f:File {name: $fname})", fname=filename)
        
        # B. Process each function
        for func in functions:
            print(f"   ... Analyzing {func['name']}()")
            explanation = analyze_function(func['code'])
            
            query = """
            MATCH (file:File {name: $fname})
            MERGE (func:Function {name: $func_name})
            ON CREATE SET func.code = $code, func.start_line = $start, func.explanation = $desc
            MERGE (file)-[:DEFINES]->(func)
            """
            
            session.run(query, 
                        fname=filename, 
                        func_name=func['name'], 
                        code=func['code'],
                        start=func['start_line'],
                        desc=explanation)
                        
    print(f"✅ Extracted {len(functions)} functions from {filename} into the Graph!")