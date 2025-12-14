from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes

app = FastAPI(title="The Code Archaeologist API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Allow the Frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Connect the routes
app.include_router(routes.router)

@app.get("/")
def read_root():
    return {"status": "System Online", "model": "Gemini 2.5 Flash"}