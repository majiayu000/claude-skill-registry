---
name: Railway Deploy
description: This skill should be used when the user asks to "deploy to Railway", "deploy backend", "deploy Python app", "deploy Node.js server", "railway deployment", or mentions Railway hosting workflows.
version: 1.0.0
---

# Deploy to Railway

## Overview

Railway provides modern backend deployment with automatic builds, environment management, and database integration. This skill guides through production-ready Railway deployments for Python, Node.js, and other backend applications.

## Prerequisites Check

### Install Railway CLI
```bash
# Install via npm
npm install -g @railway/cli

# Install via curl (Unix/macOS)
curl -fsSL https://railway.app/install.sh | sh

# Install via Homebrew (macOS)
brew install railway
```

### Authentication
```bash
railway login
```

### Verify Setup
```bash
railway --version
railway whoami
```

## Project Configuration

### Railway Configuration File
Create `railway.json` in project root:

```json
{
  "deploy": {
    "startCommand": "python main.py",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Dockerfile Configuration
```dockerfile
# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Start command
CMD ["python", "main.py"]
```

### Python/FastAPI Configuration
```python
# main.py
import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Railway API",
    description="Production-ready API on Railway",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint for Railway"""
    return {
        "status": "healthy",
        "service": "railway-api",
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    return {"message": "Hello from Railway!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        access_log=True
    )
```

### Node.js/Express Configuration
```javascript
// server.js
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'railway-api',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
});

// Routes
app.get('/', (req, res) => {
  res.json({ message: 'Hello from Railway!' });
});

// Error handling
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
});
```

## Deployment Workflows

### Initial Project Setup
```bash
# Initialize Railway project
railway init

# Link to existing project
railway link [project-id]

# Create new project
railway new
```

### Environment Configuration
```bash
# Set environment variables
railway variables set NODE_ENV=production
railway variables set DATABASE_URL=${{Postgres.DATABASE_URL}}
railway variables set REDIS_URL=${{Redis.REDIS_URL}}

# List environment variables
railway variables

# Load local environment
railway run --service backend python main.py
```

### Database Integration
```bash
# Add PostgreSQL database
railway add postgres

# Add Redis cache
railway add redis

# Add MongoDB
railway add mongodb

# Check database status
railway status
```

### Deployment Commands
```bash
# Deploy current directory
railway up

# Deploy specific service
railway up --service backend

# Deploy with environment
railway up --environment production

# Deploy from Git
railway up --git-branch main
```

## Environment Management

### Multi-Environment Setup
```bash
# Create environments
railway environment create staging
railway environment create production

# Switch environments
railway environment use staging
railway environment use production

# List environments
railway environment list
```

### Environment Variables Management
```bash
# Service-specific variables
railway variables set --service backend API_KEY=your-key
railway variables set --service worker QUEUE_URL=redis://...

# Environment-specific variables
railway variables set --environment production SECRET_KEY=prod-secret
railway variables set --environment staging SECRET_KEY=staging-secret

# Template variables (shared across services)
railway variables set DATABASE_URL=${{Postgres.DATABASE_URL}}
```

### Secrets Management
```bash
# Add sensitive variables
railway variables set --service backend \
  JWT_SECRET=$(openssl rand -base64 32)

# Use Railway's secret interpolation
railway variables set API_URL="https://${{RAILWAY_PUBLIC_DOMAIN}}/api"
```

## Service Configuration

### Multi-Service Applications
```yaml
# railway.toml
[build]
builder = "NIXPACKS"

[[services]]
name = "backend"
source = "./backend"
[services.build]
buildCommand = "pip install -r requirements.txt"
startCommand = "python main.py"
[services.deploy]
healthcheckPath = "/health"
healthcheckTimeout = 300

[[services]]
name = "worker"
source = "./worker"
[services.build]
buildCommand = "pip install -r requirements.txt"
startCommand = "python worker.py"

[[services]]
name = "frontend"
source = "./frontend"
[services.build]
buildCommand = "npm run build"
startCommand = "npm start"
```

### Database Services
```bash
# PostgreSQL configuration
railway add postgres
railway variables set DATABASE_URL=${{Postgres.DATABASE_URL}}

# Redis configuration
railway add redis
railway variables set REDIS_URL=${{Redis.REDIS_URL}}

# MongoDB configuration
railway add mongodb
railway variables set MONGODB_URI=${{MongoDB.MONGODB_URI}}
```

## CI/CD Integration

### GitHub Actions
```yaml
# .github/workflows/railway-deploy.yml
name: Deploy to Railway

on:
  push:
    branches: [main, staging]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest

    - name: Run tests
      run: pytest

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Install Railway CLI
      run: npm install -g @railway/cli

    - name: Deploy to Railway
      run: railway up --service backend
      env:
        RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

### GitLab CI/CD
```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

variables:
  PYTHON_VERSION: "3.11"

test:
  stage: test
  image: python:$PYTHON_VERSION
  script:
    - pip install -r requirements.txt
    - pip install pytest
    - pytest

deploy_staging:
  stage: deploy
  image: node:18
  script:
    - npm install -g @railway/cli
    - railway up --service backend --environment staging
  environment:
    name: staging
  only:
    - staging

deploy_production:
  stage: deploy
  image: node:18
  script:
    - npm install -g @railway/cli
    - railway up --service backend --environment production
  environment:
    name: production
  only:
    - main
  when: manual
```

## Monitoring and Logging

### Application Logging
```python
# logging_config.py
import logging
import sys
from datetime import datetime

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Request logging middleware for FastAPI
from fastapi import Request
import time

async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    logger.info(
        f"Request: {request.method} {request.url} "
        f"Status: {response.status_code} "
        f"Time: {process_time:.4f}s"
    )

    return response
```

### Health Monitoring
```python
# health.py
import psutil
import asyncpg
from fastapi import HTTPException

async def check_database_health():
    """Check database connectivity"""
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute("SELECT 1")
        await conn.close()
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False

async def check_system_health():
    """Check system resources"""
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_percent = psutil.virtual_memory().percent

    return {
        "cpu_usage": cpu_percent,
        "memory_usage": memory_percent,
        "healthy": cpu_percent < 80 and memory_percent < 80
    }

@app.get("/health/detailed")
async def detailed_health_check():
    """Comprehensive health check"""
    db_healthy = await check_database_health()
    system_health = await check_system_health()

    if not db_healthy or not system_health["healthy"]:
        raise HTTPException(status_code=503, detail="Service unhealthy")

    return {
        "status": "healthy",
        "database": db_healthy,
        "system": system_health,
        "timestamp": datetime.utcnow().isoformat()
    }
```

### Railway Logging
```bash
# View logs
railway logs

# Follow logs in real-time
railway logs --follow

# Filter logs by service
railway logs --service backend

# Export logs
railway logs --json > app-logs.json
```

## Database Management

### PostgreSQL Setup
```python
# database.py
import asyncpg
import asyncio
from contextlib import asynccontextmanager

class DatabaseManager:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool = None

    async def connect(self):
        """Create connection pool"""
        self.pool = await asyncpg.create_pool(
            self.database_url,
            min_size=5,
            max_size=20,
            command_timeout=60
        )

    async def disconnect(self):
        """Close connection pool"""
        if self.pool:
            await self.pool.close()

    @asynccontextmanager
    async def get_connection(self):
        """Get database connection from pool"""
        async with self.pool.acquire() as connection:
            yield connection

# Migration script
async def run_migrations():
    """Run database migrations"""
    db = DatabaseManager(DATABASE_URL)
    await db.connect()

    async with db.get_connection() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

    await db.disconnect()
```

### Redis Integration
```python
# redis_client.py
import redis.asyncio as redis
import json

class RedisClient:
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.client = None

    async def connect(self):
        """Connect to Redis"""
        self.client = redis.from_url(
            self.redis_url,
            encoding="utf-8",
            decode_responses=True
        )

    async def disconnect(self):
        """Disconnect from Redis"""
        if self.client:
            await self.client.close()

    async def set_cache(self, key: str, value: dict, ttl: int = 3600):
        """Set cache with TTL"""
        await self.client.setex(key, ttl, json.dumps(value))

    async def get_cache(self, key: str):
        """Get cache value"""
        value = await self.client.get(key)
        return json.loads(value) if value else None

    async def delete_cache(self, key: str):
        """Delete cache key"""
        await self.client.delete(key)
```

## Performance Optimization

### Application Optimization
```python
# performance.py
from functools import wraps
import time
import asyncio

def async_lru_cache(maxsize: int = 128):
    """Async LRU cache decorator"""
    def decorator(func):
        cache = {}
        cache_order = []

        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = str(args) + str(sorted(kwargs.items()))

            if key in cache:
                # Move to end (most recently used)
                cache_order.remove(key)
                cache_order.append(key)
                return cache[key]

            # Execute function
            result = await func(*args, **kwargs)

            # Add to cache
            cache[key] = result
            cache_order.append(key)

            # Maintain maxsize
            while len(cache) > maxsize:
                oldest_key = cache_order.pop(0)
                del cache[oldest_key]

            return result

        return wrapper
    return decorator

# Connection pooling
from sqlalchemy.pool import QueuePool

engine = create_async_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    pool_pre_ping=True
)
```

### Resource Limits
```yaml
# railway.toml
[deploy]
healthcheckPath = "/health"
healthcheckTimeout = 300
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3

[build]
builder = "NIXPACKS"

[environment]
NODE_ENV = "production"
PORT = 8000

# Resource constraints
[resources]
memory = "1Gi"
cpu = "500m"
```

## Security Best Practices

### Environment Security
```python
# security.py
import os
from typing import Optional

class SecurityConfig:
    """Security configuration management"""

    def __init__(self):
        self.secret_key = self._get_required_env("SECRET_KEY")
        self.database_url = self._get_required_env("DATABASE_URL")
        self.allowed_origins = self._get_env_list("ALLOWED_ORIGINS")

    def _get_required_env(self, key: str) -> str:
        """Get required environment variable"""
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required environment variable {key} not set")
        return value

    def _get_env_list(self, key: str, default: Optional[str] = None) -> list:
        """Get environment variable as list"""
        value = os.getenv(key, default or "")
        return [item.strip() for item in value.split(",") if item.strip()]

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=security_config.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

### Input Validation
```python
# validation.py
from pydantic import BaseModel, validator
from typing import Optional
import re

class UserCreate(BaseModel):
    email: str
    password: str
    name: Optional[str] = None

    @validator('email')
    def validate_email(cls, v):
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', v):
            raise ValueError('Invalid email format')
        return v.lower()

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v
```

## Troubleshooting Common Issues

### Build Failures
```bash
# Check build logs
railway logs --service backend

# Debug build locally
railway run --service backend python main.py

# Clear build cache
railway up --service backend --no-cache
```

### Database Connection Issues
```python
# Connection testing
async def test_database_connection():
    """Test database connectivity"""
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        result = await conn.fetchval("SELECT version()")
        await conn.close()
        print(f"Database connected: {result}")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False
```

### Performance Issues
```bash
# Monitor resource usage
railway metrics --service backend

# Check service status
railway status --service backend

# Scale service
railway up --service backend --replicas 3
```

## Additional Resources

### Reference Files
For detailed deployment configurations, consult:
- **`references/railway-configurations.md`** - Comprehensive Railway configuration examples
- **`references/database-setup.md`** - Database integration and management
- **`references/monitoring-setup.md`** - Monitoring and alerting configuration

### Example Files
Working deployment examples in `examples/`:
- **`examples/fastapi-deployment.py`** - Complete FastAPI Railway setup
- **`examples/nodejs-express-deployment.js`** - Node.js Express deployment
- **`examples/docker-configuration.dockerfile`** - Production Dockerfile examples

### Scripts
Deployment utility scripts in `scripts/`:
- **`scripts/deploy-production.sh`** - Automated Railway deployment
- **`scripts/setup-database.py`** - Database initialization script
- **`scripts/health-check.py`** - Comprehensive health monitoring

Deploy robust backend applications with Railway's modern infrastructure and these production-ready configurations.