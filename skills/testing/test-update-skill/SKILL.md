---
name: test-update
description: Use when testing auto-update functionality locally without publishing to GitHub Releases
---

# Test Auto-Update Locally

Test the Tauri auto-update flow with a mock release server.

## Quick Start

### 1. Build test release
```powershell
.\scripts\test-release.ps1              # minor bump (default)
.\scripts\test-release.ps1 -BumpType patch  # patch bump
```

### 2. Start mock server
```bash
node _test-releases/serve.js
```

### 3. Run app with test endpoint
```bash
set TAURI_UPDATER_ENDPOINT=http://localhost:3456/latest.json && npm run tauri dev
```

## Signing Requirement

For auto-update to work, set signing key BEFORE building:
```powershell
$env:TAURI_SIGNING_PRIVATE_KEY = "your-key-here"
.\scripts\test-release.ps1
```

Without signing: installer works manually, but auto-updater rejects it.

## Test Scenarios

| Scenario | How to Test |
|----------|-------------|
| Happy path | Follow steps, click "Update Now" |
| No update available | Edit `latest.json` version to match current |
| Network failure | Stop server before update check |
| "Later" dismissal | Click "Later", verify indicator dot |

## Full Documentation

See `_test-releases/README.md` for complete details including manual process.
