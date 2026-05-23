---
name: policyengine-api-v2
description: PolicyEngine API v2 - Next-generation microservices architecture with monorepo structure
---

# PolicyEngine API v2

The next-generation PolicyEngine API is a monorepo containing multiple microservices built with modern Python tooling.

## For Users 👥

### What is API v2?

API v2 is the next generation of the PolicyEngine API, currently in active development. When complete, it will replace the current Flask API with a more scalable, maintainable microservices architecture.

**Status:** 🚧 Active development (not yet in production)

**Key improvements over v1:**
- Microservices architecture for better scalability
- Modern Python tooling (Python 3.13+, uv package manager)
- Docker-based development and deployment
- Auto-generated OpenAPI specs and clients
- Supabase for database management

## For Analysts 📊

### When to Use v2

Currently, analysts should continue using the v1 API at `https://api.policyengine.org`.

API v2 is not yet ready for production use. Check the repository README for the latest status.

## For Contributors 💻

### Repository

**Location:** PolicyEngine/policyengine-api-v2

**Clone:**
```bash
git clone https://github.com/PolicyEngine/policyengine-api-v2
cd policyengine-api-v2
```

### Architecture Overview

API v2 is a **monorepo** containing multiple microservices:

**To see current structure:**
```bash
tree -L 2 .

# Expected structure:
# ├── api-full/        - Main API (port 8081)
# ├── api-simulation/  - Economic simulation (port 8082)
# ├── api-tagger/      - Deployment management (port 8083)
# ├── docker-compose.yml
# └── shared/          - Shared utilities
```

### Microservices

**1. api-full (port 8081)**
- Main API service
- Household calculations
- Policy management
- Most endpoints from v1

**2. api-simulation (port 8082)**
- Economic simulation engine
- Population-wide impact calculations
- Resource-intensive operations

**3. api-tagger (port 8083)**
- Deployment management
- Version tagging
- Release coordination

### Technology Stack

**To see current dependencies:**
```bash
# Check pyproject.toml in each service
cat api-full/pyproject.toml
cat api-simulation/pyproject.toml
cat api-tagger/pyproject.toml
```

**Key technologies:**
- **Python 3.13+** - Latest Python version
- **uv** - Fast Python package manager
- **Docker + Docker Compose** - Local development and deployment
- **Supabase** - PostgreSQL database with auth
- **OpenAPI** - API specification generation
- **FastAPI or Flask** - (check current implementation)

### Development Setup

**To start all services locally:**
```bash
# See current docker-compose setup
cat docker-compose.yml

# Start services
docker-compose up

# Services should be available at:
# - http://localhost:8081 (api-full)
# - http://localhost:8082 (api-simulation)
# - http://localhost:8083 (api-tagger)
```

**Alternative: Run individual service:**
```bash
cd api-full
uv pip install -e .
python main.py  # or whatever the entry point is
```

### Package Management with uv

API v2 uses `uv` instead of `pip` for faster dependency management:

**To see current uv usage:**
```bash
# Check if uv is used
cat pyproject.toml | grep -A 5 "tool.uv"

# Or check for uv.lock files
find . -name "uv.lock"
```

**Common uv commands:**
```bash
# Install dependencies
uv pip install -e .

# Add a dependency
uv add package-name

# Sync dependencies
uv sync
```

### Supabase Integration

**To see current Supabase setup:**
```bash
# Check for Supabase configuration
cat .env.example | grep SUPABASE
grep -r "supabase" . --include="*.py" | head -10

# Supabase client initialization
grep -r "create_client" . --include="*.py"
```

**Common patterns:**
```python
# Example (check actual implementation)
from supabase import create_client

supabase = create_client(supabase_url, supabase_key)

# Query
result = supabase.table('policies').select('*').execute()

# Insert
supabase.table('policies').insert({'data': policy}).execute()
```

### Design Tokens Integration

API v2 may integrate with design tokens from `policyengine-app-v2`:

**To check design token usage:**
```bash
# Look for design token imports
grep -r "design.*token\|designTokens" . --include="*.py"
grep -r "@policyengine/design" package.json

# Check if tokens are in dependencies
cat package.json | grep -A 5 "dependencies"
```

**If using npm design tokens:**
```bash
# Design tokens from app-v2
npm install @policyengine/design-tokens
```

### OpenAPI Specification

**To see current API spec generation:**
```bash
# Look for OpenAPI/Swagger setup
grep -r "openapi\|swagger" . --include="*.py"

# Check for spec files
find . -name "openapi*.json" -o -name "openapi*.yaml"

# If using FastAPI, specs auto-generated at /docs
```

### Testing

**To see current test setup:**
```bash
ls -la tests/
cat pytest.ini  # or pyproject.toml for pytest config
```

**Run tests:**
```bash
# All services
pytest

# Specific service
cd api-full && pytest

# With docker-compose
docker-compose run api-full pytest
```

### Migration from v1

**Key architectural differences:**

| Aspect | v1 (Flask monolith) | v2 (Microservices) |
|--------|---------------------|-------------------|
| Structure | Single Flask app | Multiple services |
| Database | Redis + Cloud SQL | Supabase (PostgreSQL) |
| Deployment | Google App Engine | Docker containers |
| Package manager | pip | uv |
| Python version | 3.9+ | 3.13+ |

**To understand migration patterns:**
```bash
# Compare endpoint implementations
# v1: policyengine-api/policyengine_api/endpoints/
# v2: api-full/endpoints/ (or similar)

# See what's been ported
git log --grep="migrate\|port" --oneline
```

### Common Development Tasks

**Task 1: Add New Endpoint to api-full**

1. **Find current endpoint pattern:**
   ```bash
   # Look at existing endpoints
   ls api-full/endpoints/  # or api-full/routes/
   cat api-full/endpoints/example.py
   ```

2. **Follow the pattern** (likely FastAPI or Flask)

3. **Update OpenAPI spec** (may be auto-generated)

4. **Add tests:**
   ```bash
   cat tests/test_endpoints.py
   ```

**Task 2: Work with Supabase**

```bash
# See current database schema
cat supabase/migrations/*.sql  # if using migrations

# Test database locally
docker-compose up supabase  # if in docker-compose
```

**Task 3: Use Design Tokens**

```bash
# Check if design tokens are integrated
grep -r "design.*token" .

# If using from app-v2, import them:
# (Actual implementation depends on current setup)
```

### Environment Variables

**To see required environment variables:**
```bash
cat .env.example

# Common variables:
# - SUPABASE_URL
# - SUPABASE_KEY
# - DATABASE_URL
# - API_PORT (8081, 8082, 8083)
```

### Monorepo Best Practices

**To see current monorepo structure:**
```bash
# List all services
ls -d */

# Check for shared code
ls shared/ common/ lib/  # (if exists)

# See inter-service dependencies
grep -r "../api-" pyproject.toml
```

**Pattern:**
- Each service should be independently deployable
- Shared code goes in `shared/` or similar
- Each service has its own tests
- Docker Compose for local multi-service development

## Related Skills

- **policyengine-api-skill** - v1 API patterns (for migration reference)
- **policyengine-core-skill** - Understanding the simulation engine
- **policyengine-us-skill** - Country model integration
- **policyengine-design-skill** - Design tokens and branding
- **policyengine-standards-skill** - Code quality standards

## Resources

**Repository:** https://github.com/PolicyEngine/policyengine-api-v2

**Related:**
- v1 API: https://github.com/PolicyEngine/policyengine-api
- App v2 (design tokens): https://github.com/PolicyEngine/policyengine-app-v2
- Supabase: https://supabase.com/docs

## Development Status

⚠️ **Important:** API v2 is in active development. Always check the repository README for:
- Current status and roadmap
- Breaking changes
- Migration timeline from v1
- Deployment instructions

**To see current status:**
```bash
cat README.md
git log -10 --oneline
```
