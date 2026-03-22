---
name: security-patterns
description: >
  Use this skill when working on credentials, secrets, environment variables, Docker security,
  or any security-related concern. Triggers on: secrets management, credential handling,
  Docker security, environment variables, or mentions of "security", "secrets", "credentials",
  "env vars", or "vulnerability".
---

# Security Patterns — DoclingOptimisation

## Secrets Management
- Environment variables for all runtime configuration (DOCLING_* vars)
- Never hardcode API keys, tokens, or credentials in code
- Docker Hub credentials via GitHub Secrets in CI/CD
- Azure Container App secrets for runtime environment variables

## Docker Security
- Non-root user (`docling:docling`) in runtime image
- No dev dependencies in runtime stage
- Minimal runtime packages (only what's needed)
- No shell access in production (consider `--no-install-recommends`)
- Pin base image versions to prevent supply chain attacks

## Model Downloads
- Models pre-fetched at build time from HuggingFace Hub and ModelScope CDN
- `HF_HUB_ETAG_TIMEOUT=0` and `HF_HUB_DOWNLOAD_TIMEOUT=5` prevent runtime downloads
- Verify model integrity if moving to a private registry

## Input Validation
- PDF path validation in process.py (exists, is file, is readable)
- File size limits should be enforced at the Container App Job level
- Never trust user-provided paths without validation
