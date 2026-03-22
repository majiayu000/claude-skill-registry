---
name: taskflow
description: Build and run the full TaskFlow demo stack (Express backend + React frontend + mobile)
disable-model-invocation: true
allowed-tools: Bash
---

# TaskFlow Demo

Build and run the full-stack demo that showcases dart_node's capabilities.

## Run it

```bash
sh examples/run_taskflow.sh
```

This:
1. Kills any existing processes on ports 3000 and 8080
2. Builds backend, mobile, and frontend from Dart to JS
3. Starts the Express backend on **http://localhost:3000**
4. Starts the frontend dev server on **http://localhost:8080/web/**
5. Traps Ctrl+C for clean shutdown

## Ports

| Service | Port | How |
|---------|------|-----|
| Backend API (Express) | 3000 | `node examples/backend/build/server.js` |
| Frontend (static) | 8080 | `python3 -m http.server 8080` |
| Mobile (Expo) | — | `cd examples/mobile/rn && npm run ios` or `npm run android` |

## Prerequisites

Dependencies must be installed first. If the build fails, run:
```bash
./tools/pub_get.sh
```

Or use the Dev Container which runs `post-create.sh` automatically.

## Manual start (individual services)

Backend only:
```bash
dart run tools/build/build.dart backend && node examples/backend/build/server.js
```

Frontend only:
```bash
cd examples/frontend && bash build.sh && python3 -m http.server 8080
```
