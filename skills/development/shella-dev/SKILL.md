---
name: shella-dev
description: Index of shella development documentation and common commands. Auto-loaded when working on the repo.
user-invocable: false
---

# Shella Development Index

This skill provides pointers to documentation and quick reference for common tasks. **Read the referenced files for full details.**

## Documentation Map

| Topic | File | Key Content |
|-------|------|-------------|
| **Repo overview** | `/CLAUDE.md` | Monorepo structure, devtool commands, architecture diagram |
| **Daemon API** | `/apps/daemon/CLAUDE.md` | Endpoints, data models, plugin lifecycle, testing |
| **Web client** | `/apps/web/CLAUDE.md` | Layout system, routing, components |
| **iOS app** | `/apps/ios/CLAUDE.md` | Build scripts, simulator logging, project structure |
| **iOS run on device** | `/ios` skill | Build and deploy to physical iPhone over WiFi |
| **iOS WiFi debugging** | `/apps/ios/DEBUGGING_OVER_WIFI.md` | devicectl, os_log workarounds, debug UI patterns |
| **Mac app** | `/apps/mac/CLAUDE.md` | SwiftUI architecture, WebView inspector |
| **Plugin creation** | `/PLUGIN_CREATION_GUIDE.md` | How to create user plugins |

## Quick Reference

### Common Commands
```bash
npm run dt dev daemon        # Run daemon
npm run dt dev all -l        # Daemon + web with local plugins
npm run dt plugin list       # List plugins/instances
npm run dt plugin restart X  # Restart plugin (picks up server changes)
```

### iOS: Run on Device or Simulator
```bash
cd apps/ios
./scripts/run-device.sh   # Physical iPhone (auto-detects, builds, installs, launches)
./scripts/run.sh          # Simulator (iPhone 17 Pro)
```
Use `/ios` skill for full workflow. See `apps/ios/DEBUGGING_OVER_WIFI.md` for WiFi debugging tips.

### Key Paths
- Plugins: `~/.local/share/shella/plugins/`
- State: `~/.local/state/shella/registry.json`
- Logs: `~/.local/state/shella/dev.log`
- Bundled plugins source: `apps/daemon/bundled-plugins/`

### Ports
- 47100: Daemon API
- 47101-47199: Plugin instances
- 47200: Standalone plugin dev

### Debugging Endpoints
```bash
curl localhost:47100/health    # Daemon health
curl localhost:47100/plugins   # All plugins + instances
curl localhost:47100/registry  # Full state dump
```

## When to Read Full Docs

- **iOS logs/debugging over WiFi?** → Read `apps/ios/DEBUGGING_OVER_WIFI.md` (os_log, debug UI overlays)
- **Plugin lifecycle questions?** → Read `apps/daemon/CLAUDE.md`
- **Native app debugging?** → Read the relevant `CLAUDE.md` for that app
- **Release process?** → Check `scripts/` and root `CLAUDE.md`
