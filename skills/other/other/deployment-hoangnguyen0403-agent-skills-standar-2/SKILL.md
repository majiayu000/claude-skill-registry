---
name: NestJS Deployment
description: Docker builds, Memory tuning, and Graceful shutdown.
metadata:
  labels: [nestjs, deployment, docker, k8s]
  triggers:
    files: ['Dockerfile', 'k8s/**', 'helm/**']
    keywords: [Dockerfile, max-old-space-size, shutdown hooks]
---

# Deployment & Ops Standards

## **Priority: P1 (OPERATIONAL)**

Docker optimization and production deployment standards for NestJS applications.

## Docker Optimization

- **Multi-Stage Builds**: Mandatory.
  1. **Build Stage**: Install `devDependencies`, build NestJS (`nest build`).
  2. **Run Stage**: Copy only `dist` and `node_modules` (pruned), use `node:alpine`.
- **Security**: Do not run as `root`.
  - **Dockerfile**: `USER node`.

## Runtime Tuning (Node.js)

- **Memory Config**: Container memory != Node memory.
  - **Rule**: Explicitly set Max Old Space.
  - **Command**: `node --max-old-space-size=XXX dist/main`
  - **Calculation**: Set to ~75-80% of Kubernetes Limit. (Limit: 1GB -> OldSpace: 800MB).
- **Graceful Shutdown**:
  - **Signal**: Listen to `SIGTERM`.
  - **NestJS**: `app.enableShutdownHooks()` is mandatory.
  - **Sleep**: Add a "Pre-Stop" sleep in K8s (5-10s) to allow Load Balancer to drain connections before Node process stops accepting traffic.

## Init Patterns

- **Database Migrations**:
  - **Anti-Pattern**: Running migration in `main.ts` on startup.
  - **Pro Pattern**: Use an **Init Container** in Kubernetes that runs `npm run typeorm:migration:run` before the app container starts.
