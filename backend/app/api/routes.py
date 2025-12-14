from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
from neo4j import GraphDatabase
# --- 1. ADD NEW IMPORTS HERE ---
from pydantic import BaseModel
from app.services.ingest_demo import ingest_code_snippet
from app.services.refactor import refactor_code_logic 
from app.services.test_generator import generate_unit_tests # <--- NEW

router = APIRouter()

# --- 2. ADD THE REQUEST MODEL HERE ---
class RefactorRequest(BaseModel):
    code: str

# Create a temporary folder to store uploaded files
UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/analyze-file")
async def analyze_file(file: UploadFile = File(...)):
    """
    Endpoint where React will send the code file.
    """
    try:
        file_location = f"{UPLOAD_DIR}/{file.filename}"
        
        # 1. Save the file temporarily
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 2. Read the content
        with open(file_location, "r", encoding="utf-8") as f:
            code_content = f.read()

        # 3. Trigger the AI + Graph Logic
        ingest_code_snippet(file.filename, code_content)
        
        return {
            "message": "File processed successfully", 
            "filename": file.filename,
            "status": "stored_in_graph"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Database Connection
driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI", "bolt://localhost:7687"), 
    auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "password123"))
)

@router.get("/graph")
async def get_graph():
    """
    Fetches the entire graph from Neo4j and formats it for React Flow.
    """
    query = """
    MATCH (n)-[r]->(m)
    RETURN n, r, m
    LIMIT 100
    """
    
    nodes = []
    edges = []
    node_ids = set() # To track duplicates
    
    with driver.session() as session:
        result = session.run(query)
        
        for record in result:
            source = record["n"]
            target = record["m"]
            rel = record["r"]
            
            # Process Source Node
            if source.element_id not in node_ids:
                label = "File" if "File" in source.labels else "Function"
                nodes.append({
                    "id": source.element_id,
                    "type": "default",
                    "data": { 
                        "label": source.get("name"),
                        "code": source.get("code", "No code available"),
                        "explanation": source.get("explanation", "No analysis available")
                    },
                    "position": { "x": 0, "y": 0 } 
                })
                node_ids.add(source.element_id)
            
            # Process Target Node
            if target.element_id not in node_ids:
                label = "File" if "File" in target.labels else "Function"
                nodes.append({
                    "id": target.element_id,
                    "type": "default",
                    "data": { 
                        "label": target.get("name"),
                        "code": target.get("code", "No code available"),
                        "explanation": target.get("explanation", "No analysis available")
                    },
                    "position": { "x": 0, "y": 0 }
                })
                node_ids.add(target.element_id)
                
            # Process Edge
            edges.append({
                "id": rel.element_id,
                "source": source.element_id,
                "target": target.element_id,
                "label": rel.type
            })
            
    return {"nodes": nodes, "edges": edges}

# --- 3. ADD THE REFACTOR ENDPOINT AT THE BOTTOM ---
@router.post("/refactor")
async def trigger_refactor(request: RefactorRequest):
    """
    Receives code, sends it to Gemini, returns modern code.
    """
    modern_code = refactor_code_logic(request.code)
    return {"refactored_code": modern_code}

@router.post("/generate-tests")
async def trigger_tests(request: RefactorRequest): # We can reuse the RefactorRequest model since it just needs 'code'
    """
    Generates Unit Tests for the given function.
    """
    test_code = generate_unit_tests(request.code)
    return {"test_code": test_code}