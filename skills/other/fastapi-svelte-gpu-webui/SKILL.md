---
name: fastapi-svelte-gpu-webui
description: |
  Pattern for building web UIs for GPU-based CLI tools. Use when:
  (1) Wrapping a command-line tool with a web interface, (2) Building job queue
  systems for long-running GPU tasks, (3) Creating file upload/download workflows,
  (4) Need real-time progress updates via WebSocket, (5) Deploying to Kubernetes
  with GPU scheduling. Covers FastAPI backend, Svelte 5 frontend, NFS storage,
  and Terraform deployment.
author: Claude Code
version: 1.0.0
date: 2025-01-31
---

# FastAPI + Svelte GPU WebUI Pattern

## Problem
Many powerful tools are command-line only, making them inaccessible to non-technical
users. Building a web UI requires handling file uploads, job queuing, progress tracking,
and GPU resource scheduling.

## Context / Trigger Conditions
- You have a CLI tool that does heavy processing (ML inference, media conversion, etc.)
- Want to add a web interface for easier access
- Need to track long-running job progress
- Deploying to Kubernetes with GPU nodes
- Files need to persist across pod restarts (NFS storage)

## Solution Overview

### Directory Structure
```
project-web/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py        # REST endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   └── converter.py     # CLI wrapper + job manager
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # Pydantic models
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.svelte
│   │   ├── lib/
│   │   │   ├── FileUpload.svelte
│   │   │   ├── JobsList.svelte
│   │   │   └── ProgressBar.svelte
│   │   └── stores/
│   │       └── jobs.js
│   ├── package.json
│   └── vite.config.js
├── Dockerfile
└── README.md
```

### Backend: Job Manager Pattern
```python
# services/converter.py
import asyncio
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable
import subprocess

class Job:
    id: str
    filename: str
    status: str  # pending, processing, completed, failed
    progress: float
    created_at: datetime
    output_file: Optional[str]
    error: Optional[str]

class JobManager:
    def __init__(self, storage_path: str = "/mnt"):
        self.storage_path = Path(storage_path)
        self.jobs: dict[str, Job] = {}
        self.progress_callbacks: dict[str, list[Callable]] = {}

    def create_job(self, filename: str, **options) -> Job:
        job_id = str(uuid.uuid4())
        job = Job(
            id=job_id,
            filename=filename,
            status="pending",
            progress=0.0,
            created_at=datetime.now(),
            **options
        )
        self.jobs[job_id] = job
        return job

    async def run_conversion(self, job_id: str):
        job = self.jobs[job_id]
        job.status = "processing"

        input_path = self.storage_path / "uploads" / job.filename
        output_dir = self.storage_path / "outputs" / job_id
        output_dir.mkdir(parents=True, exist_ok=True)

        # Build command for CLI tool
        cmd = [
            "/path/to/cli-tool",
            str(input_path),
            "-o", str(output_dir),
            # Add other options...
        ]

        # Run with output capture for progress parsing
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        # Parse output for progress updates
        async def read_output(stream):
            while True:
                line = await stream.readline()
                if not line:
                    break
                line_str = line.decode().strip()
                # Parse progress from CLI output
                if "%" in line_str:
                    # Extract and update progress
                    self.update_progress(job_id, parsed_progress)

        await asyncio.gather(
            read_output(process.stdout),
            read_output(process.stderr)
        )

        returncode = await process.wait()

        if returncode == 0:
            output_files = list(output_dir.glob("*.m4b"))
            if output_files:
                job.output_file = output_files[0].name
                job.status = "completed"
        else:
            job.status = "failed"
            job.error = f"Exit code {returncode}"

job_manager = JobManager()
```

### Backend: API Routes
```python
# api/routes.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import shutil
import asyncio

router = APIRouter(prefix="/api")

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    upload_dir = Path("/mnt/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "size": file_path.stat().st_size}

@router.post("/jobs")
async def create_job(request: JobCreate):
    job = job_manager.create_job(filename=request.filename, ...)
    asyncio.create_task(job_manager.run_conversion(job.id))
    return job

@router.get("/jobs")
async def list_jobs():
    return job_manager.get_all_jobs()

@router.get("/jobs/{job_id}/download")
async def download_job(job_id: str):
    job = job_manager.get_job(job_id)
    if not job or job.status != "completed":
        raise HTTPException(404)
    output_path = Path("/mnt/outputs") / job_id / job.output_file
    return FileResponse(output_path, filename=job.output_file)
```

### Frontend: Svelte 5 Components
```svelte
<!-- FileUpload.svelte -->
<script>
  let { onUpload } = $props();
  let dragOver = $state(false);
  let uploading = $state(false);

  async function handleUpload(file) {
    uploading = true;
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/api/upload', {
      method: 'POST',
      body: formData
    });

    if (response.ok) {
      const data = await response.json();
      onUpload(data.filename);
    }
    uploading = false;
  }
</script>

<div class="dropzone"
     class:dragover={dragOver}
     ondragover={(e) => { e.preventDefault(); dragOver = true; }}
     ondragleave={() => dragOver = false}
     ondrop={(e) => { e.preventDefault(); handleUpload(e.dataTransfer.files[0]); }}>
  Drop file here
</div>
```

### Dockerfile
```dockerfile
FROM python:3.12-slim

# Install Node for frontend build
RUN apt-get update && apt-get install -y nodejs npm

# Build frontend
COPY frontend/ /app/frontend/
WORKDIR /app/frontend
RUN npm install && npm run build

# Install backend
COPY backend/ /app/backend/
WORKDIR /app/backend
RUN pip install -r requirements.txt

# Serve static files from FastAPI
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Terraform Deployment (GPU)
```hcl
resource "kubernetes_deployment" "myapp" {
  spec {
    template {
      spec {
        node_selector = { "gpu" : "true" }

        toleration {
          key      = "nvidia.com/gpu"
          operator = "Equal"
          value    = "true"
          effect   = "NoSchedule"
        }

        container {
          image = "myregistry/myapp@sha256:..."
          name  = "myapp"

          resources {
            limits = { "nvidia.com/gpu" = "1" }
          }

          volume_mount {
            name       = "data"
            mount_path = "/mnt"
          }
        }

        volume {
          name = "data"
          nfs {
            server = "10.0.10.15"
            path   = "/mnt/main/myapp"
          }
        }
      }
    }
  }
}
```

## Verification
1. Upload a file via the UI
2. Start a conversion job
3. Watch progress update in real-time
4. Download the completed file
5. Verify files persist across pod restarts

## Notes
- Use image digest for reliable deployments (see `k8s-docker-registry-cache-bypass` skill)
- NFS storage persists across pod restarts
- GPU node taints require matching tolerations
- Consider adding job persistence (database) for production use
- WebSocket can provide smoother progress updates than polling

## See Also
- `k8s-docker-registry-cache-bypass` - Fixing image cache issues
- `k8s-gpu-no-nvidia-devices` - GPU device troubleshooting
- `python-filename-sanitization` - Secure file handling
