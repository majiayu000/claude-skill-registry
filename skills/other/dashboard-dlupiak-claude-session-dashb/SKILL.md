---
name: dashboard
description: Open the Claude Session Dashboard in the browser. Starts it first if not already running. Checks for and installs updates before starting.
user-invocable: true
---

# Open Dashboard

## Steps

### 1. Check if dashboard is running

Run: `lsof -i :3000 -sTCP:LISTEN`

- If output is non-empty → dashboard is already running, skip to step 4
- If empty → go to step 2

### 2. Check for updates

Check whether the dashboard is installed globally or via npx, then compare versions:

```bash
INSTALLED=$(npm list -g claude-session-dashboard --depth=0 --json 2>/dev/null | node -p "try{JSON.parse(require('fs').readFileSync(0,'utf8')).dependencies?.['claude-session-dashboard']?.version||''}catch(e){''}" 2>/dev/null)
LATEST=$(npm view claude-session-dashboard version 2>/dev/null)
echo "installed=${INSTALLED} latest=${LATEST}"
```

- If `INSTALLED` is empty → using npx (always fetches latest automatically, no update needed)
- If `INSTALLED` is non-empty and differs from `LATEST` → update is available, go to step 3
- If versions match → skip to step 4

### 3. Install update

A newer version is available. Install it:

```bash
npm install -g claude-session-dashboard@latest
```

Report to the user: "Updated claude-session-dashboard from vX.X.X to vY.Y.Y."

### 4. Start the dashboard

If not already running, start in background:

```bash
nohup npx claude-session-dashboard --port 3000 >> "$HOME/.claude/dashboard.log" 2>&1 & disown
```

Wait for it to be ready:

```bash
npx wait-on http://localhost:3000 --timeout 15000 2>/dev/null || sleep 5
```

### 5. Open in browser

```bash
open http://localhost:3000
```

Report to the user that the dashboard is open at http://localhost:3000.
