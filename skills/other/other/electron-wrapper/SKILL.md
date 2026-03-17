---
name: electron-wrapper
description: >
  Wrap a Bun web app into an Electron desktop app with native window management,
  auto-updates, code signing, and CI/CD distribution. Use when the user wants to
  create a native desktop application from an existing Bun-based web server,
  package it for macOS/Windows, set up auto-updating, or handle Electron UX
  concerns like drag regions and traffic lights. Also use when cutting releases
  or tagging versions for Electron apps.
---

# Electron Wrapper for Bun Web Apps

This skill guides wrapping an existing Bun web server into a native desktop app using Electron. It's based on a proven implementation that solved every major integration challenge.

## Architecture

**"Electron as chrome, Bun as server"** — Two runtimes working together:

- **Electron/Node.js** handles window management, native menus, auto-updates, and IPC
- **Bun** runs the actual web server with all your application logic

The Electron main process spawns a bundled Bun binary that runs your server, then loads `http://localhost:{port}` in a `BrowserWindow`. Your web app doesn't know or care that it's inside Electron — it's just a web page with an optional `window.electronAPI` bridge for native features.

This architecture means:
- Zero changes to your server code (it's still a standard Bun HTTP server)
- The web app works identically in a browser or in Electron
- Electron handles only what browsers can't: window chrome, system tray, auto-updates, file system access
- Two separate `node_modules` — Electron uses npm, your web app uses Bun

## Phase 1: Project Setup

Create the Electron subproject alongside your existing Bun web app.

**What to create:**
- `electron/` directory with its own `package.json` (npm, not Bun), two tsconfigs (ESM for main, CJS for preload), `electron-builder.yml`, and macOS entitlements
- `scripts/build-server.ts` for bundling the server
- `scripts/download-bun.ts` for downloading platform-specific Bun binaries
- Parent project changes: new scripts, tsconfig excludes, .gitignore entries

**Reference:** [project-setup.md](references/project-setup.md)

## Phase 2: Main Process

Build the Electron main process — the entry point, server spawning, window management, auto-updater, and preload bridge.

**Files to create:**

| File | Purpose |
|------|---------|
| `electron/src/main/index.ts` | App lifecycle, dev/prod mode, single-instance lock, IPC handlers |
| `electron/src/main/bun-server.ts` | Spawn bundled Bun, port selection, health polling, env var injection |
| `electron/src/main/window.ts` | BrowserWindow config, bounds persistence, security settings, navigation guards |
| `electron/src/main/updater.ts` | electron-updater setup, event forwarding to renderer |
| `electron/src/preload/index.ts` | contextBridge API with invoke/on patterns and unsubscribe support |

**Key decisions:**
- Dev mode uses `ELECTRON_DEV_URL` env var to connect to the external dev server (no internal Bun spawn)
- `autoDownload: false` — let users choose when to download updates
- Preload exposes only specific methods, never raw `ipcRenderer`
- Window persists bounds via `electron-store`

**Reference:** [main-process.md](references/main-process.md)

## Phase 3: Web App Adaptation

Adapt the existing web app to detect and respond to the Electron environment while remaining fully functional as a standalone web app.

**Changes to the web app:**

| Change | Details |
|--------|---------|
| Electron detection utility | `isElectron()`, `getElectronPlatform()`, `isMacElectron()`, `applyElectronDocumentAttributes()` |
| Type declarations | `window.electronAPI` with all properties optional |
| CSS drag regions | `.app-window-drag`/`.app-window-no-drag` classes, auto-exclude interactive elements |
| Traffic light spacing | `--electron-traffic-left` CSS variable (72px on macOS, 0px elsewhere) |
| Storage path | Env var for data directory, falling back to CWD |
| Static asset serving | Env var for static dir in production mode |
| Auto-update hook | `useElectronUpdater()` React hook with download/install controls |
| Update notification | Pill component showing available → downloading → ready states |
| Feature gating | Disable demo mode, hosted features when in Electron |

**Reference:** [web-adaptation.md](references/web-adaptation.md)

## Phase 4: Build & Distribution

Bundle everything, set up CI/CD, and handle code signing.

**Build pipeline:**
1. Build web app (`bun run build`)
2. Bundle server to single file (`Bun.build()` → `resources/server/index.js`)
3. Download platform-specific Bun binaries → `resources/bun/{platform}-{arch}/`
4. Compile Electron TypeScript (two passes: main ESM + preload CJS)
5. electron-builder packages everything with `extraResources`

**CI/CD:**
- GitHub Actions triggered by version tags (e.g., `v*`, `clippy-v*`)
- Matrix builds: macOS arm64/x64 on `macos-14`, Windows x64 on `windows-latest`
- `--publish never` in build step, separate publish job creates draft GitHub release
- Apple certificate import and notarization in CI

**Code signing:**
- macOS: Developer ID Application certificate, exported as base64 .p12
- Notarization via Apple ID + app-specific password
- 5 GitHub secrets required: `APPLE_CERTIFICATE`, `APPLE_CERTIFICATE_PASSWORD`, `APPLE_ID`, `APPLE_PASSWORD`, `APPLE_TEAM_ID`

**Icons:**
- macOS: `sips` + `iconutil` from source PNG → `.icns`
- Windows: `png-to-ico` npm package → `.ico`

**Reference:** [build-and-distribute.md](references/build-and-distribute.md)

## Cutting a Release

**Never build release artifacts locally.** CI has the signing certificates and notarization credentials. Local builds produce unsigned apps that macOS Gatekeeper will block.

### Release workflow:

1. **Bump version** in `electron/package.json`, commit, and merge to main
2. **Find the tag pattern** the CI workflow expects:
   ```bash
   grep -A2 'tags:' .github/workflows/*.yml
   ```
3. **Tag the merged commit on main:**
   ```bash
   git tag <pattern><version> origin/main
   git push origin <pattern><version>
   ```
4. **Monitor CI:**
   ```bash
   gh run list --workflow=<workflow>.yml --limit=1
   ```
5. **Review and publish** the draft release on GitHub

### Common mistakes:
- Running `electron-builder --publish always` locally — no notarization
- Using `gh release create` with local artifacts — unsigned
- Tagging before the version bump is merged — wrong version in build
- Tagging a feature branch instead of `origin/main`

See [pitfalls.md §13](references/pitfalls.md) for full details.

## Critical Pitfalls

Quick-reference list — see [pitfalls.md](references/pitfalls.md) for full details with symptoms and code examples.

| # | Pitfall | One-line fix |
|---|---------|-------------|
| 1 | ESM/CJS conflicts | `"type": "module"` + default import pattern for CJS packages |
| 2 | Preload must be CJS | Separate tsconfig with `"module": "CommonJS"` |
| 3 | `__dirname` unavailable | `fileURLToPath(import.meta.url)` polyfill |
| 4 | Dev mode MIME errors | Connect to external dev server via `ELECTRON_DEV_URL` |
| 5 | Bun version mismatch | Pin version in download script, match dev version |
| 6 | nvm PATH issues | `bash -lc` for spawned processes |
| 7 | Wrong storage path | Env var + `app.getPath("userData")` |
| 8 | White flash on open | `show: false` + `ready-to-show` + dark `backgroundColor` |
| 11 | `${platform}` != `process.platform` | Put Bun `extraResources` in `mac:`/`win:` sections with `darwin-`/`win32-` prefixes |
| 12 | Bun workspace hoists deps | Bundle main with esbuild + `createRequire` banner, or use npm for electron dir |
| 13 | Local builds aren't notarized | Always release via CI tags, never `electron-builder --publish` locally |

## Dev Workflow

The `electron:dev` command runs the full development environment:

```
npm run dev
  ├── concurrently
  │   ├── dev:web    → cd .. && bun run dev          (Bun dev server with HMR)
  │   └── dev:electron
  │       ├── wait-on http://localhost:3005           (wait for dev server)
  │       ├── npm run build                           (compile TS)
  │       └── ELECTRON_DEV_URL=... electron .         (launch Electron)
```

- The web dev server runs with HMR — changes reflect instantly
- Electron connects to the dev server instead of spawning its own Bun
- Preload and main process changes require restarting `electron:dev`
- Web app changes hot-reload automatically

To test production-like behavior locally:
```bash
bun run electron:pack    # builds everything, packages without installer
# Output in electron/release/
```

## Customization Checklist

When adapting this for a new project, update these project-specific values:

- [ ] App name in `electron-builder.yml` (`productName`, `appId`)
- [ ] Window title in `window.ts`
- [ ] Dev server port in `dev:electron` script and `dev` script
- [ ] Environment variable names (e.g., `APP_DATA_DIR`, `APP_STATIC_DIR`)
- [ ] `backgroundColor` in window config to match your app's theme
- [ ] `category` in `electron-builder.yml` mac section
- [ ] Repository URL in `electron/package.json`
- [ ] Bun version in `download-bun.ts`
- [ ] Icon assets in `electron/assets/`
