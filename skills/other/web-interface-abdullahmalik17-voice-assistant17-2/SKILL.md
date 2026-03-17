---
name: web-interface
description: |
  Build and deploy a Next.js web interface for the Voice Assistant with real-time voice/chat capabilities.
  Use this skill when: (1) Creating a web-based voice assistant UI, (2) Setting up FastAPI WebSocket backend,
  (3) Implementing browser-based voice recording without Picovoice, (4) Deploying with Docker for global access,
  (5) Integrating push-to-talk or browser wake word detection, (6) Building scalable agentic web systems.
---

# Web Interface Skill for Voice Assistant

Build a production-ready Next.js web interface that connects to the Voice Assistant backend.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      BROWSER (Next.js)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ Voice Record │  │ Chat UI      │  │ Push-to-Talk/        │  │
│  │ (MediaRecorder)│ │ (React)     │  │ Wake Word (optional) │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│           │                │                    │               │
│           └────────────────┴────────────────────┘               │
│                            │ WebSocket                          │
└────────────────────────────┼────────────────────────────────────┘
                             │
┌────────────────────────────┼────────────────────────────────────┐
│                      BACKEND (FastAPI)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ WebSocket    │  │ REST API     │  │ Audio Streaming      │  │
│  │ Handler      │  │ Endpoints    │  │ Processor            │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│           │                │                    │               │
│           └────────────────┴────────────────────┘               │
│                            │                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Voice Assistant Core                         │  │
│  │  STT → Intent → Memory → Planner → Tools → LLM → TTS     │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Backend Setup (FastAPI with WebSocket)

Create `src/api/websocket_server.py`:

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import base64

app = FastAPI(title="Voice Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_json(self, websocket: WebSocket, data: dict):
        await websocket.send_json(data)

manager = ConnectionManager()

@app.websocket("/ws/voice")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            # Process audio/text and return response
            response = await process_message(data)
            await manager.send_json(websocket, response)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

### 2. Next.js Frontend Setup

Initialize project:
```bash
npx create-next-app@latest web --typescript --tailwind --app --src-dir
cd web && npm install
```

### 3. Docker Deployment

Use `docker-compose.yml` from `assets/docker/`.

## Implementation Steps

### Phase 1: Backend API
1. Create FastAPI WebSocket server - see `references/backend-api.md`
2. Add audio streaming endpoints
3. Integrate with existing Voice Assistant services

### Phase 2: Frontend
1. Set up Next.js project - see `references/nextjs-setup.md`
2. Create voice recording component with MediaRecorder API
3. Implement WebSocket client for real-time communication
4. Build chat UI with message history

### Phase 3: Wake Word Alternative
Since Picovoice requires API key, use these alternatives:
- **Push-to-Talk**: Space bar or button hold (recommended for web)
- **Voice Activity Detection**: Browser-based VAD
- **OpenWakeWord**: Open-source wake word (requires backend processing)

### Phase 4: Deployment
1. Containerize with Docker - see `assets/docker/`
2. Configure nginx reverse proxy
3. Set up SSL/TLS for production
4. Deploy to cloud (AWS/GCP/Azure) or self-host

## Key Components

| Component | Technology | Purpose |
|-----------|------------|---------|
| Frontend | Next.js 14 + TypeScript | Web UI |
| Styling | Tailwind CSS + shadcn/ui | Modern UI components |
| Voice | MediaRecorder API | Browser audio capture |
| Real-time | WebSocket | Bidirectional communication |
| Backend | FastAPI | API server |
| Container | Docker + docker-compose | Deployment |
| Proxy | nginx | SSL termination, load balancing |

## Reference Files

- `references/backend-api.md` - Complete FastAPI implementation
- `references/nextjs-setup.md` - Next.js project structure and components
- `references/deployment.md` - Docker and cloud deployment guide

## Assets

- `assets/docker/` - Docker configuration files
- `assets/web-template/` - Next.js boilerplate (if needed)
