---
name: generate-dockerfile
description: Generate optimized multi-stage Dockerfile
argument-hint: "[--runtime=dotnet|node] [--port=5000]"
tags: [codegen, docker, devops, container]
user-invocable: true
---

# Generate Dockerfile

Generate an optimized multi-stage Dockerfile with security best practices.

## What To Do

1. **Analyze project**: Detect runtime (.NET, Node.js, Python)
2. **Generate multi-stage Dockerfile**:
   - Build stage with SDK image
   - Publish stage with runtime image
   - Non-root user
   - Health check
   - .dockerignore
3. **Security**: No secrets in image, minimal base image, non-root user

## Arguments
- `--runtime=<dotnet|node|python>`: Target runtime
- `--port=<n>`: Exposed port (default: 5000)