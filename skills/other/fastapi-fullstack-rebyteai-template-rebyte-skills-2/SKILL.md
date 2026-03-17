---
name: fastapi-fullstack
description: Python full-stack with FastAPI, React, PostgreSQL, and Docker.
---

# FastAPI Full Stack

A Python full-stack application with FastAPI backend.

## Tech Stack

- **Backend**: FastAPI, Python
- **Frontend**: React
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy

## Prerequisites

- Python 3.11+
- Docker (recommended)

## Setup

### 1. Clone the Template

```bash
git clone --depth 1 https://github.com/tiangolo/full-stack-fastapi-template.git .
```

If the directory is not empty:

```bash
git clone --depth 1 https://github.com/tiangolo/full-stack-fastapi-template.git _temp_template
mv _temp_template/* _temp_template/.* . 2>/dev/null || true
rm -rf _temp_template
```

### 2. Remove Git History (Optional)

```bash
rm -rf .git
git init
```

### 3. Setup with Docker (Recommended)

```bash
docker compose up -d
```

### 4. Or Setup Manually

```bash
cd backend
pip install -r requirements.txt
```

## Development

With Docker:
```bash
docker compose up -d
```

Manual:
```bash
cd backend
uvicorn main:app --reload
```
