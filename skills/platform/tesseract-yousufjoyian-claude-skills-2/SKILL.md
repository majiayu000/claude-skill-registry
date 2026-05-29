---
name: tesseract
description: Pull and start Tesseract - the Information Mapping Knowledge Engine with Firebase backend. Provides localhost and Tailscale URLs.
---

# Tesseract Manager

This skill manages the Tesseract application - pulling latest code, starting the dev server, and providing access URLs.

## Quick Reference

| Component | Location |
|-----------|----------|
| Git Repo | `/home/yousuf/local_workspaces/tesseract` |
| GitHub | `yousufjoyian/tesseract` |
| Firebase Project | `tesseract-kb-app` |

## Ports

| Service | Port |
|---------|------|
| Web UI (Vite) | 3000 |

## When to Use This Skill

Trigger phrases:
- "pull tesseract"
- "start tesseract"
- "tesseract status"
- "launch tesseract"

## What This Skill Does

1. **Pull latest** from GitHub to `/home/yousuf/local_workspaces/tesseract`
2. **Check if Vite running** on port 3000
3. **Start Vite** if not running
4. **Provide URLs** for localhost and Tailscale access

## Execution Steps

### Step 1: Pull Latest from GitHub

```bash
cd /home/yousuf/local_workspaces/tesseract && git pull
```

### Step 2: Check if Vite is Running

```bash
curl -s http://localhost:3000 > /dev/null && echo "Vite: UP" || echo "Vite: DOWN"
```

### Step 3: Start Vite if Not Running

```bash
cd /home/yousuf/local_workspaces/tesseract && npm run dev &
```

### Step 4: Get Tailscale IP

```bash
ip -4 addr show tailscale0 2>/dev/null | grep -oP '(?<=inet\s)\d+(\.\d+){3}'
```

### Step 5: Provide Access URLs

After all steps, output:

```
Tesseract Ready

Localhost:
  http://localhost:3000

Android (Tailscale):
  http://<TAILSCALE_IP>:3000

Services:
  Web UI:   http://localhost:3000  [UP/DOWN]
  Firebase: tesseract-kb-app
```

## Full Automated Script

Run all steps in sequence:

```bash
#!/bin/bash
echo "=== Tesseract Pull & Start ==="

# 1. Pull latest
echo "[1/4] Pulling latest from GitHub..."
cd /home/yousuf/local_workspaces/tesseract && git pull

# 2. Check if Vite is running
echo "[2/4] Checking Vite status..."
VITE_UP=$(curl -s http://localhost:3000 > /dev/null 2>&1 && echo "UP" || echo "DOWN")

# 3. Start Vite if not running
if [ "$VITE_UP" = "DOWN" ]; then
  echo "[3/4] Starting Vite dev server..."
  cd /home/yousuf/local_workspaces/tesseract && npm run dev &
  sleep 3
  VITE_UP=$(curl -s http://localhost:3000 > /dev/null 2>&1 && echo "UP" || echo "DOWN")
else
  echo "[3/4] Vite already running"
fi

# 4. Get Tailscale IP
TAILSCALE_IP=$(ip -4 addr show tailscale0 2>/dev/null | grep -oP '(?<=inet\s)\d+(\.\d+){3}' || echo "not connected")

# Output
echo ""
echo "[4/4] Status Report"
echo "========================================"
echo "  Tesseract"
echo "========================================"
echo ""
echo "Access URLs:"
echo "  Localhost:  http://localhost:3000"
echo "  Android:    http://$TAILSCALE_IP:3000"
echo ""
echo "Services:"
echo "  Web UI:     $VITE_UP"
echo "  Firebase:   tesseract-kb-app"
echo ""

if [ "$VITE_UP" = "DOWN" ]; then
  echo "WARNING: Vite failed to start. Check logs."
fi
```

## Features

Tesseract provides:
- **Thoughts** - AI-powered note taking and organization
- **Map** - Neural visualization of knowledge connections
- **Export** - Information Mapping document generation from raw text/DOCX

## Firebase Backend

| Service | Details |
|---------|---------|
| Auth | Google Sign-In |
| Firestore | Thoughts collection |
| Functions | `geminiProxy` for AI calls |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Vite not starting | Check node_modules exist, run `npm install` |
| Firebase errors | Check user is signed in |
| AI not responding | Check Firebase functions deployed |
| Tailscale not connected | Run `sudo tailscale up` |

## Architecture

```
GitHub (yousufjoyian/tesseract)
    ↓ git pull
local_workspaces/tesseract
    ↓ npm run dev
Browser → localhost:3000 or Tailscale:3000
    ↓
Firebase (auth, firestore, functions)
    ↓
Gemini API (via geminiProxy function)
```

## A2UI Embedding

For embedding Tesseract in the A2UI panel, use the generic `a2ui-embed` skill.
See: `~/local_workspaces/skills/a2ui-embed/SKILL.md`
