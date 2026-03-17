---
name: fastapi
description: FastAPI development including async endpoints, Pydantic models, dependency injection, and OpenAPI documentation. Activate for FastAPI apps, async Python APIs, and modern Python web services.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# FastAPI Skill

Provides comprehensive FastAPI development capabilities for the Golden Armada AI Agent Fleet Platform.

## When to Use This Skill

Activate this skill when working with:
- FastAPI application development
- Async endpoint implementation
- Pydantic model definitions
- Dependency injection patterns
- OpenAPI/Swagger documentation

## Quick Reference

### Run Commands
\`\`\`bash
# Development
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# With Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
\`\`\`

## Application Structure

\`\`\`
app/
├── main.py
├── config.py
├── dependencies.py
├── routers/
│   ├── __init__.py
│   ├── agents.py
│   └── tasks.py
├── models/
│   ├── __init__.py
│   ├── agent.py
│   └── task.py
├── schemas/
│   ├── __init__.py
│   ├── agent.py
│   └── task.py
└── services/
    ├── __init__.py
    └── llm_service.py
\`\`\`

## Basic Application

\`\`\`python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routers import agents, tasks
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up...")
    yield
    # Shutdown
    print("Shutting down...")

app = FastAPI(
    title="Golden Armada Agent API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "golden-armada"}
\`\`\`

## Pydantic Schemas

\`\`\`python
# schemas/agent.py
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class AgentType(str, Enum):
    CLAUDE = "claude"
    GPT = "gpt"
    GEMINI = "gemini"

class AgentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    type: AgentType
    description: Optional[str] = None

class AgentCreate(AgentBase):
    pass

class AgentResponse(AgentBase):
    id: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
\`\`\`

## Router Example

\`\`\`python
# routers/agents.py
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List

from app.schemas.agent import AgentCreate, AgentResponse
from app.services.agent_service import AgentService
from app.dependencies import get_agent_service

router = APIRouter()

@router.post("/", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent: AgentCreate,
    service: AgentService = Depends(get_agent_service)
):
    """Create a new agent."""
    return await service.create(agent)

@router.get("/", response_model=List[AgentResponse])
async def list_agents(
    skip: int = 0,
    limit: int = 100,
    service: AgentService = Depends(get_agent_service)
):
    """List all agents."""
    return await service.list(skip=skip, limit=limit)

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: str,
    service: AgentService = Depends(get_agent_service)
):
    """Get agent by ID."""
    agent = await service.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent
\`\`\`

## Dependency Injection

\`\`\`python
# dependencies.py
from functools import lru_cache
from typing import Annotated
from fastapi import Depends

from app.config import Settings
from app.services.agent_service import AgentService
from app.services.llm_service import LLMService

@lru_cache
def get_settings():
    return Settings()

async def get_llm_service(
    settings: Annotated[Settings, Depends(get_settings)]
) -> LLMService:
    return LLMService(api_key=settings.anthropic_api_key)

async def get_agent_service(
    llm_service: Annotated[LLMService, Depends(get_llm_service)]
) -> AgentService:
    return AgentService(llm_service=llm_service)
\`\`\`

## Background Tasks

\`\`\`python
from fastapi import BackgroundTasks

@router.post("/tasks/{task_id}/execute")
async def execute_task(
    task_id: str,
    background_tasks: BackgroundTasks,
    service: TaskService = Depends(get_task_service)
):
    background_tasks.add_task(service.execute_async, task_id)
    return {"status": "accepted", "task_id": task_id}
\`\`\`

## WebSocket Support

\`\`\`python
from fastapi import WebSocket, WebSocketDisconnect

@router.websocket("/ws/{agent_id}")
async def agent_websocket(websocket: WebSocket, agent_id: str):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            response = await process_message(agent_id, data)
            await websocket.send_text(response)
    except WebSocketDisconnect:
        print(f"Agent {agent_id} disconnected")
\`\`\`
