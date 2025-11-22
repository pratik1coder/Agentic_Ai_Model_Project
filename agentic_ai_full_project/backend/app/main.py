from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.agent import CompanyResearchAgent
import os

app = FastAPI(title="Agentic Company Research Assistant (Backend)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

agent = CompanyResearchAgent()

class ChatRequest(BaseModel):
    message: str
    company: str = None
    focus: str = "overview"
    depth: str = "standard"

@app.post('/api/chat')
async def chat(req: ChatRequest):
    try:
        resp = await agent.handle_user_message(req.message, company=req.company, focus=req.focus, depth=req.depth)
        return {"status":"ok","response":resp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/api/research')
async def research(req: ChatRequest):
    try:
        plan = await agent.run_research(req.company or req.message, focus=req.focus, depth=req.depth)
        return {"status":"ok","plan":plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/health')
async def health():
    return {"status":"ok"}

@app.get('/local-assignment')
async def local_assignment():
    path = '/mnt/data/AI Agent Building Assignment - Eightfold.pdf'
    if os.path.exists(path):
        return FileResponse(path, filename='AI Agent Building Assignment - Eightfold.pdf')
    return {"status":"missing"}
