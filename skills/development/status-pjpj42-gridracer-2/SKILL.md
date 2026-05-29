---
name: status
description: Show current project status - build, tests, git, simulator
model: haiku
allowed-tools:
  - Bash
  - Read
---

# Project Status

Quick overview of GridRacer project state.

## Checks

### 1. Git Status
```bash
echo "=== Git Status ==="
git status --short
git log --oneline -3
```

### 2. Build Check
```bash
echo "=== Build Check ==="
xcodebuild -scheme GridRacer -configuration Debug -destination 'generic/platform=iOS Simulator' build 2>&1 | grep -E "(SUCCEEDED|FAILED|error:)" | tail -5
```

### 3. Simulator Status
```bash
echo "=== Simulator ==="
xcrun simctl list devices booted 2>/dev/null | head -5 || echo "No simulators booted"
```

### 4. App Installed
```bash
echo "=== App Status ==="
xcrun simctl get_app_container booted trouarat.GridRacer 2>/dev/null && echo "App installed" || echo "App not installed"
```

## Output Format

```
GridRacer Status
================
Git: N files modified, branch: main
Build: SUCCEEDED / FAILED
Simulator: iPhone 16 (booted) / None
App: Installed / Not installed

Recent commits:
- abc1234 Last commit message
- def5678 Previous commit
```
