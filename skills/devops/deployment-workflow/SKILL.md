---
name: deployment-workflow
description: Deploy to HuggingFace Spaces, create releases, check deployment status, verify before release, push to production. Use when deploying, releasing, or checking deployment logs.
allowed-tools: Bash, Read
---

# Deployment Workflow

Complete guide for deploying CCBell Sound Generator to HuggingFace Spaces.

## Deployment Pipeline

```
git tag v1.0.0 → GitHub Actions → Build + Test → HuggingFace Spaces
```

## Pre-Deployment Checklist

Before creating a release, ALL checks must pass:

### 1. Backend Quality
```bash
cd backend && source .venv/bin/activate
ruff check .
ruff format --check .
ty check .
```

### 2. Frontend Quality
```bash
cd frontend
npm run lint
npx tsc --noEmit
npm run build
```

### 3. Docker Build Test
```bash
docker build -t ccbell-sound-generator .
```

### 4. Docker Run Test
```bash
docker run -d -p 7860:7860 --name ccbell-test ccbell-sound-generator
sleep 10
curl http://localhost:7860/api/health
docker stop ccbell-test && docker rm ccbell-test
```

## Creating a Release

### 1. Ensure Clean Git State
```bash
git status
git pull origin master
```

### 2. Create Version Tag
```bash
# Create annotated tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push to trigger deployment
git push origin v1.0.0
```

### 3. Monitor Deployment
- **GitHub Actions**: https://github.com/mpolatcan/ccbell-sound-generator/actions/workflows/deploy.yml
- **HuggingFace Space**: https://huggingface.co/spaces/mpolatcan/ccbell-sound-generator
- **Live App**: https://mpolatcan-ccbell-sound-generator.hf.space

## Checking Deployment Logs

Use the provided script:
```bash
./scripts/check-hf-space-logs.sh
```

Requires `secrets.env` with `HF_TOKEN` set:
```bash
cp secrets.env.example secrets.env
# Edit and add your HuggingFace token
```

## CI/CD Workflows

### CI Pipeline (on push/PR)
- Lint frontend (ESLint + TypeScript)
- Lint backend (ruff)
- Type check backend (ty)
- Build frontend (Vite)
- Build Docker image

### Deploy Pipeline (on version tag)
- Validate semver version
- Build application
- Update version in config
- Test Docker build
- Deploy to HuggingFace Spaces

## Required Secrets (GitHub)

| Secret | Description |
|--------|-------------|
| `HF_TOKEN` | HuggingFace API token with write access |
| `HF_USERNAME` | HuggingFace username/organization |

## Troubleshooting

### Common Issues

1. **Model download fails**: Check HF_TOKEN for gated model access
2. **Out of memory**: Use `small` model, check for memory leaks
3. **Container exits immediately**: Check `docker logs <container_id>`
4. **Health check fails**: Verify port 7860 is exposed

### Rollback

If deployment fails, the previous version remains active. To redeploy:
```bash
git tag -d v1.0.0  # Delete local tag
git push origin :refs/tags/v1.0.0  # Delete remote tag
# Fix issues, then recreate tag
```
