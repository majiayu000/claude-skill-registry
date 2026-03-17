---
name: docker-backend
description: Dockerizes backend projects with auto-detection, latest base images via web search, Dockerfile generation, and Makefile with port override support.
---

# Docker Backend Skill

This skill containerizes backend projects by detecting the tech stack, fetching the latest base image versions, generating a Dockerfile, and creating a Makefile with build/start/stop/restart targets.

## When to Invoke This Skill

Invoke this skill when ANY of these conditions are true:

1. **User asks to dockerize a backend**: "dockerize this project", "add Docker support", "containerize the backend"
2. **User needs a Dockerfile**: "create a Dockerfile", "I need Docker for this app"
3. **User needs Docker management**: "add make targets for Docker", "I need to manage Docker containers"
4. **Backend project lacks containerization**: Project has no Dockerfile but has backend code

## Prerequisites

- Docker installed and running
- Project has identifiable backend code (package.json, requirements.txt, go.mod, etc.)

## Workflow

### Step 1: Detect Backend Location

Check for backend project in this order:

```bash
# Check root first
ls package.json requirements.txt go.mod Cargo.toml pom.xml 2>/dev/null

# If not found, check ./backend/
ls backend/package.json backend/requirements.txt backend/go.mod 2>/dev/null
```

Set `BACKEND_PATH` to `./` or `./backend/` based on where manifest files are found.

### Step 2: Detect Tech Stack

Invoke the `tech-stack-analyzer` agent:

```
Task(subagent_type="tech-stack-analyzer", prompt="
Analyze the project at ${BACKEND_PATH}.
Focus on: primary language, runtime version, package manager
")
```

### Step 3: Get Latest Base Image Version

Use `exa-websearch` skill or WebSearch to find the latest base image:

**For Node.js:**
```
WebSearch: "Docker Hub node official image latest LTS version 2025"
```

**For Python:**
```
WebSearch: "Docker Hub python official image latest version 2025"
```

**For Go:**
```
WebSearch: "Docker Hub golang official image latest version 2025"
```

### Step 4: Generate Dockerfile

Create Dockerfile at `${BACKEND_PATH}/Dockerfile` using the appropriate template:

#### Node.js Template

```dockerfile
FROM node:${VERSION}-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Expose port
EXPOSE 3000

# Start application
CMD ["node", "dist/index.js"]
```

**Variations based on project:**
- If `src/index.ts` exists: Add build step, use `CMD ["node", "dist/index.js"]`
- If `src/index.js` exists: Use `CMD ["node", "src/index.js"]`
- If `server.js` exists: Use `CMD ["node", "server.js"]`
- If `package.json` has `"start"` script: Use `CMD ["npm", "start"]`

#### Python Template

```dockerfile
FROM python:${VERSION}-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port
EXPOSE 8000

# Start application
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Variations based on project:**
- If `manage.py` exists (Django): Use `CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]`
- If `app.py` exists (Flask): Use `CMD ["python", "app.py"]`
- If `main.py` exists: Use `CMD ["python", "main.py"]`

#### Go Template (Multi-stage)

```dockerfile
FROM golang:${VERSION}-alpine AS builder

WORKDIR /app

# Copy go mod files
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy source code
COPY . .

# Build binary
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

# Runtime stage
FROM alpine:latest

WORKDIR /app

# Copy binary from builder
COPY --from=builder /app/main .

# Expose port
EXPOSE 8080

# Start application
CMD ["./main"]
```

### Step 5: Validate Dockerfile

Run docker build to validate:

```bash
cd ${BACKEND_PATH}
docker build -t $(basename $(pwd))-test .
docker rmi $(basename $(pwd))-test
```

If build fails, analyze error and fix Dockerfile.

### Step 6: Create/Update Makefile

Check if Makefile exists at `${BACKEND_PATH}/Makefile`:

**If Makefile does NOT exist**, create it:

```makefile
# Docker configuration
IMAGE_NAME ?= $(shell basename $(CURDIR))
CONTAINER_NAME ?= $(IMAGE_NAME)-container
HOST_PORT ?= 8080
CONTAINER_PORT ?= 8080

.PHONY: build start stop restart logs clean

## Build Docker image
build:
	docker build -t $(IMAGE_NAME) .

## Start container (use HOST_PORT=XXXX to override)
start:
	docker run -d --name $(CONTAINER_NAME) -p $(HOST_PORT):$(CONTAINER_PORT) $(IMAGE_NAME)

## Stop and remove container
stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

## Restart container
restart: stop start

## Follow container logs
logs:
	docker logs -f $(CONTAINER_NAME)

## Remove container and image
clean: stop
	docker rmi $(IMAGE_NAME) || true
```

**If Makefile EXISTS**, append Docker targets if missing:

1. Check for existing `build:`, `start:`, `stop:`, `restart:` targets
2. If Docker targets don't exist, append them with `docker-` prefix:
   - `docker-build`, `docker-start`, `docker-stop`, `docker-restart`

### Step 7: Validate Makefile

Run validation:

```bash
cd ${BACKEND_PATH}
make build
make start
sleep 2
docker ps | grep $(basename $(pwd))
make stop
```

If validation fails, analyze and fix.

## Port Override Usage

Users can override the host port:

```bash
# Override at invocation
make start HOST_PORT=3000

# Or export before running
export HOST_PORT=3000
make restart

# Override both ports
make start HOST_PORT=3000 CONTAINER_PORT=3000
```

## Error Handling

### Dockerfile Build Fails

1. Check base image exists: `docker pull <base-image>`
2. Check COPY paths match actual file structure
3. Check CMD matches actual entry point file
4. For Node.js: Ensure `package-lock.json` exists for `npm ci`

### Makefile Validation Fails

1. Check Docker daemon is running: `docker info`
2. Check port is not in use: `lsof -i :${HOST_PORT}`
3. Check container name conflict: `docker ps -a | grep ${CONTAINER_NAME}`

## Example Invocation

**Scenario**: User says "dockerize this Node.js backend"

**Actions**:
1. Detect: Found `package.json` at `./`
2. Tech stack: Node.js 20.x with Express
3. Web search: Latest Node LTS is 24.12.0
4. Generate: Create `Dockerfile` with `FROM node:24-alpine`
5. Validate: `docker build` succeeds
6. Makefile: Create with all targets and `HOST_PORT` override
7. Validate: `make build restart` succeeds

## Do NOT Invoke When

- Project already has a well-configured Dockerfile
- User is working on frontend-only code
- User explicitly wants a different containerization approach (e.g., Podman, containerd)
- Project uses a non-standard build system that requires custom handling

## Supported Tech Stacks

| Stack | Manifest File | Default Port |
|-------|--------------|--------------|
| Node.js | package.json | 3000 |
| Python | requirements.txt, pyproject.toml | 8000 |
| Go | go.mod | 8080 |
| Rust | Cargo.toml | 8080 |
| Java | pom.xml, build.gradle | 8080 |

## Current Latest Base Images

These versions were current as of January 2025. Always use web search to get the latest:

| Stack | Image | Version |
|-------|-------|---------|
| Node.js LTS | node:24-alpine | 24.12.0 |
| Python | python:3.13-slim | 3.13 |
| Go | golang:1.25.5-alpine | 1.25.5 |
