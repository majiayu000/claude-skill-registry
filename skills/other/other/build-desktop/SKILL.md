---
name: build-desktop
description: Build a new desktop app release (Electron). Triggers on "build desktop", "new release", "desktop release", "build the app"
---

# Build Desktop App Release

## Steps

1. **Bump version** in `desktop/package.json` (patch bump unless user specifies)
2. **Build dashboard** from `src/dashboard/`:
   ```bash
   cd src/dashboard && npx.cmd vite build
   ```
3. **Copy dist to desktop/**:
   ```bash
   cp -r dist/server dist/core dist/dashboard desktop/
   ```
   Note: `dist/server` and `dist/core` come from `tsc` (may have pre-existing TS errors — that's fine, the JS still emits). The dashboard comes from vite build above.
4. **Install desktop deps**:
   ```bash
   cd desktop && npm.cmd install
   ```
5. **Build executable** (Windows by default):
   ```bash
   cd desktop && npx.cmd electron-builder --win
   ```
   Output lands in `desktop/artifacts/` as an NSIS `.exe` installer.
6. **Commit** version bump + push
7. Optionally **create GitHub release** with `gh release create v0.x.x desktop/artifacts/*.exe`

## Key Facts

- App: `orch-desktop` — Electron 35+, ESM
- Config: `desktop/electron-builder.yml` (appId: `dev.orch.desktop`, product: `Orch`)
- Targets: `--win` (NSIS), `--mac` (DMG universal), `--linux` (AppImage)
- Port: 13011 (avoids dev server conflict)
- Credentials: `~/.orch/.env`
- CI: `.github/workflows/desktop-release.yml` builds all platforms on release
