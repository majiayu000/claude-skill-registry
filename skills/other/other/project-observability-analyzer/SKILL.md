---
name: project-observability-analyzer
description: Analyze projects and recommend observability integration. Use when adding observability to projects Claude Code works on.
---

# Project Observability Analyzer

Analyze project structure and recommend observability strategy for applications.

## Workflow

1. **Scan Project Structure** (files, dependencies, framework)
2. **Detect Framework** (Express, Next.js, FastAPI, Spring Boot, etc.)
3. **Identify Existing Logging** (Winston, Pino, Python logging, etc.)
4. **Detect Existing Observability** (Prometheus exporters, OTEL, APM agents)
5. **Analyze API Endpoints** (if web framework detected)
6. **Generate Recommendations**:
   - OTEL instrumentation points
   - Logging library configurations
   - Prometheus metrics to add
   - Docker compose integration
7. **Generate Integration Files**:
   - Updated docker-compose.yml (app + observability)
   - OTEL instrumentation code
   - Logger configuration
   - README with setup instructions

## Example Output

```markdown
## Project: Express.js REST API

**Framework**: Express.js 4.18.2
**Logging**: Winston (JSON format) ✅
**Observability**: None ❌

**Recommendations**:
1. Add express-prom-bundle for Prometheus metrics
2. Configure Winston → Loki (via Alloy)
3. Add OTEL auto-instrumentation for tracing
4. Integrate with LGTM stack

**Files Generated**:
- docker-compose-with-app.yml
- otel-instrumentation.js
- winston-loki-config.js
```

## Framework Templates
- Express.js integration
- Next.js integration
- FastAPI integration
- Spring Boot integration
