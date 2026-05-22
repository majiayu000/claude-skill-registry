---
name: aiops-gordon
description: Setup and use Docker AI (Gordon) for intelligent container operations
allowed-tools: Bash, Write, Read, Glob
---

# Docker AI (Gordon) Setup Skill

## Quick Start

1. **Verify Docker Desktop** - Version 4.53+ required
2. **Enable Gordon** - Settings → Beta features → Toggle "Docker AI"
3. **Test Gordon** - Run `docker ai "What can you do?"`
4. **Use Gordon** - For building, debugging, and optimizing containers

## What is Docker AI (Gordon)?

Docker AI (codenamed Gordon) is an AI-powered assistant built into Docker Desktop that helps with:
- **Building containers** - Generate Dockerfiles from requirements
- **Debugging issues** - Analyze logs and errors
- **Optimizing images** - Reduce size and improve performance
- **Scanning vulnerabilities** - Security analysis
- **Explaining commands** - Learn Docker and Kubernetes

## Enabling Docker AI

### Docker Desktop 4.53+
1. Open Docker Desktop
2. Go to **Settings** → **Beta features**
3. Toggle on **"Docker AI"**
4. Click **"Get started"** or **"Enable"**
5. Accept terms and conditions

### Alternative: Docker CLI Extension
```bash
# If not using Docker Desktop, try CLI extension
# (Note: Gordon is primarily in Docker Desktop)
docker context list
# See if AI context is available
```

## Gordon Commands Reference

### Building Containers

```bash
# Generate Dockerfile from requirements
docker ai "Create a Dockerfile for FastAPI application with Python 3.13"

# Optimize existing Dockerfile
docker ai "Optimize this Dockerfile for smaller image size" < Dockerfile

# Create multi-stage Dockerfile
docker ai "Convert this to a multi-stage Dockerfile" < Dockerfile

# Generate docker-compose.yml
docker ai "Create a docker-compose file with frontend, backend, and mcp-server services"
```

### Debugging Issues

```bash
# Analyze startup failures
docker ai "Why is my container exiting immediately?"

# Debug build errors
docker ai "Fix this Docker build error" < error.log

# Troubleshoot networking
docker ai "Why can't container1 connect to container2?"

# Analyze logs
docker ai "Analyze these container logs for issues" < logs.txt
```

### Image Optimization

```bash
# Reduce image size
docker ai "Make this Dockerfile produce a smaller image"

# Optimize layer caching
docker ai "Optimize layer caching in this Dockerfile"

# Security scan
docker ai "Scan this image for security vulnerabilities" todo-backend:latest

# Best practices review
docker ai "Review this Dockerfile for security best practices"
```

### Multi-Service Orchestration

```bash
# Generate compose file
docker ai "Create docker-compose for Next.js frontend, FastAPI backend, PostgreSQL"

# Add health checks
docker ai "Add health checks to this docker-compose file"

# Configure networking
docker ai "Set up bridge networking for these 3 containers"
```

## Gordon Examples for Todo Project

### Frontend Dockerfile Generation
```bash
# Ask Gordon to create Next.js Dockerfile
docker ai "Create a production-ready Dockerfile for Next.js 16 with TypeScript, using multi-stage build, with nginx or standalone server"
```

**Expected output from Gordon**:
```dockerfile
# Gordon will generate optimized Dockerfile
# Review and save to frontend/Dockerfile
```

### Backend Dockerfile Generation
```bash
docker ai "Create a multi-stage Dockerfile for FastAPI with Python 3.13, SQLModel, and OpenAI dependencies"
```

### MCP Server Dockerfile
```bash
docker ai "Create a minimal Dockerfile for Python FastMCP server with minimal dependencies"
```

### Docker Compose Generation
```bash
docker ai "Create a docker-compose.yml file for:
- Frontend: Next.js on port 3000
- Backend: FastAPI on port 8000
- MCP Server: Python on port 8001
- Network: todo-network
- Health checks for all services
- Environment variables from .env file"
```

### Debug Build Issues
```bash
# If build fails, paste the error
docker ai "I'm getting this error when building:
Error: ModuleNotFoundError: No module named 'fastapi'
How do I fix this?"

# Or redirect error file
docker ai "Fix the errors in this build log" < build-error.log
```

## Gordon Limitations

| Limitation | Notes |
|------------|--------|
| Cloud-only features | Some features require Docker Desktop Pro/Team |
| Context awareness | Gordon has limited context of your project structure |
| Complex networking | May struggle with advanced networking scenarios |
| Security scanning | Basic scanning only - use dedicated tools for production |

## Gordon vs Manual Docker

| Task | Gordon | Manual Docker |
|------|---------|----------------|
| Simple Dockerfile | Faster, optimized | More control |
| Debugging | Excellent - analyzes context | Requires manual investigation |
| Learning | Great for learning | Requires documentation |
| Production-ready | Good, but review manually | Full control |
| Custom requirements | May need manual edit | Full control |

## Best Practices with Gordon

1. **Always review output** - Gordon generates good code, but review before saving
2. **Iterative refinement** - Use follow-up prompts to refine Gordon's output
3. **Test locally** - Always test Dockerfiles generated by Gordon
4. **Version control** - Save Gordon's suggestions and iterate
5. **Learn from Gordon** - Understand why Gordon suggests certain patterns

## Integration with Other Skills

Combine Gordon with:
- **@docker-containerization-builder** - Use Gordon for Dockerfile, agent for full setup
- **@devops-kubernetes-builder** - Gordon helps debug K8s container issues
- **@aiops-helm-builder** - Use Gordon for chart image optimization

## Gordon Troubleshooting

| Issue | Fix |
|--------|-----|
| Gordon not available | Update Docker Desktop to 4.53+ |
| "Beta features" missing | Sign out and sign in to Docker Desktop |
| Gordon gives errors | Check Docker Desktop logs, try reinstall |
| Limited functionality | Check Docker subscription tier |

## Example Gordon Workflows

### Workflow 1: Generate Dockerfile
```bash
# Step 1: Ask Gordon
docker ai "Create Dockerfile for Next.js with TypeScript and Tailwind CSS"

# Step 2: Save output to file
# Copy Gordon's response to Dockerfile

# Step 3: Build and test
docker build -t test-image .
docker run --rm test-image
```

### Workflow 2: Debug Container Issue
```bash
# Step 1: Get container logs
docker logs <container-name> > logs.txt

# Step 2: Ask Gordon
docker ai "Analyze this log file and tell me what's wrong" < logs.txt

# Step 3: Apply fix
# Update Dockerfile or code based on Gordon's suggestion

# Step 4: Rebuild and test
docker build -t fixed-image .
docker run --rm fixed-image
```

### Workflow 3: Optimize Production Image
```bash
# Step 1: Build initial image
docker build -t todo-backend:latest ./backend

# Step 2: Check size
docker images todo-backend

# Step 3: Ask Gordon to optimize
docker ai "Reduce the size of this Dockerfile while maintaining all functionality" < backend/Dockerfile

# Step 4: Compare
docker build -t todo-backend:optimized ./backend
docker images | grep todo-backend
```

## Verification Checklist

After using Gordon:
- [ ] Gordon output reviewed and understood
- [ ] Generated files are saved with correct names
- [ ] Dockerfiles build without errors
- [ ] Containers start and run correctly
- [ ] Health checks pass
- [ ] Services can communicate
- [ ] Image size is reasonable
- [ ] Security scan shows no critical vulnerabilities

## Next Steps

After successful Docker setup with Gordon:
1. Test with `docker-compose up -d`
2. Load images to Minikube
3. Deploy with Kubernetes manifests
4. Convert to Helm charts

## References

- [Docker AI Documentation](https://docs.docker.com/ai/gordon/)
- [Docker Desktop Release Notes](https://docs.docker.com/desktop/release-notes/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Phase 4 Constitution](../../../prompts/constitution-prompt-phase-4.md)
- [Phase 4 Plan](../../../prompts/plan-prompt-phase-4.md)
