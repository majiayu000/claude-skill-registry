---
name: docker-cicd-patterns
description: >
  Use this skill when creating or modifying Dockerfiles, docker-compose files, GitHub Actions
  workflows, or deployment pipelines. Triggers on: container builds, CI/CD configuration,
  deployment automation, Azure Container App Jobs, Docker Hub, or any mention of "Docker",
  "container", "GitHub Actions", "workflow", "CI/CD", "pipeline", "deploy", or "build".
---

# Docker & CI/CD Patterns — DoclingOptimisation

## Dockerfile Standards
- Multi-stage build: builder (compile deps, pre-fetch models) + runtime (slim, non-root)
- Base image: `python:3.14-slim-bookworm` (pinned, not `:latest`)
- Non-root user: `docling:docling`
- uv for package management — `uv sync --frozen --no-dev`
- Models pre-fetched at build time (no network at runtime)
- CPU-only PyTorch from `https://download.pytorch.org/whl/cpu`
- `.dockerignore` excludes .git, .claude, .history, .firecrawl, logs, research docs

## Docker Compose (Local Dev)
- Compose-native limits (`mem_limit`, `cpus`) for Docker Desktop
- Volume mounts: `./input:/home/docling/input:ro`, `./output:/home/docling/output`
- Default threads: `DOCLING_NUM_THREADS=10` for local benchmarking

## Azure Container App Job
- This is a **batch/one-shot workload** — use Container App Jobs, NOT revision-based apps
- CPU profile: 4 vCPUs / 8 Gi, set `DOCLING_NUM_THREADS=4`
- GPU profile: NC8as-T4 / 8 vCPUs / 56 Gi, requires CUDA PyTorch build, set `DOCLING_DEVICE=cuda`
- Container registry: Docker Hub (migration to ACR planned)

## GitHub Actions
- Separate CI (lint, format-check, type-check) from CD (build, push to Docker Hub)
- Use `astral-sh/setup-uv@v4` for uv in CI
- Use `--frozen` for reproducible installs
- Pin action versions
- Use concurrency groups to cancel redundant runs
- For Docker Hub: use `docker/login-action@v3` + `docker/build-push-action@v6`

## Image Tagging
- `latest` for main branch
- `sha-<short-sha>` for every push
- Semantic version tags for releases
