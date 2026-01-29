from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
from database import SessionLocal, init_db
from models import FormData
from agent import UUIDAgent
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="UUID Form Filler Agent API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Get LLM provider from environment (default to openai)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()

# Initialize agent based on provider
if LLM_PROVIDER == "lmstudio":
    print("Using LM Studio with locally hosted model")
    agent = UUIDAgent(
        provider="lmstudio",
        model=os.getenv("LMSTUDIO_MODEL", "gemma-3")
    )
else:
    print("Using OpenAI API")
    agent = UUIDAgent(
        api_key=os.getenv("OPENAI_API_KEY"),
        provider="openai",
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    )


class UUIDRequest(BaseModel):
    uuid: str


class FormResponse(BaseModel):
    uuid: str
    name: str
    email: str
    phone: str
    address: str
    company: str
    position: str
    notes: str


@app.get("/")
async def root():
    return {"message": "UUID Form Filler Agent API", "status": "running"}


@app.get("/api/uuids", response_model=List[str])
async def get_all_uuids():
    """Get list of all available UUIDs"""
    db = SessionLocal()
    try:
        form_data = db.query(FormData).all()
        return [data.uuid for data in form_data]
    finally:
        db.close()


@app.post("/api/get-form-data", response_model=FormResponse)
async def get_form_data(request: UUIDRequest):
    """Get form data by UUID using LLM agent"""
    db = SessionLocal()
    try:
        # First, try to get data from database
        form_data = db.query(FormData).filter(FormData.uuid == request.uuid).first()
        
        if not form_data:
            raise HTTPException(status_code=404, detail="UUID not found")
        
        # Use OpenAI agent to intelligently map and format the data
        agent_response = agent.map_uuid_to_form(
            uuid=request.uuid,
            raw_data={
                "name": form_data.name,
                "email": form_data.email,
                "phone": form_data.phone,
                "address": form_data.address,
                "company": form_data.company,
                "position": form_data.position,
                "notes": form_data.notes
            }
        )
        
        return FormResponse(**agent_response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        db.close()


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    llm_provider = os.getenv("LLM_PROVIDER", "openai").lower()
    return {
        "status": "healthy",
        "llm_provider": llm_provider,
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
        "lmstudio_enabled": llm_provider == "lmstudio"
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
