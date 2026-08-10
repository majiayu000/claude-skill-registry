---
name: software-desktop
description: "Guides cross-platform and native desktop development with Electron, Tauri, Flutter Desktop, MAUI, and platform-native frameworks. Use when choosing a stack or packaging installers."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.1"
last_validated: 2026-07-11
---

# Desktop Application Development

Build cross-platform and native desktop apps with correct architecture, security defaults, and distribution pipelines.

## Quick Reference

| Need | Recommended Tool / Framework |
|---|---|
| Cross-platform (JS/TS) | Electron — mature ecosystem, large community, Chromium-based |
| Cross-platform (Rust + Web) | Tauri — smaller bundles, stronger security model, OS webview, also targets iOS/Android from the same codebase (stable since Tauri 2.0, Oct 2024) |
| Cross-platform (Dart) | Flutter Desktop — shared mobile/desktop codebase; strongest on macOS, Windows/Linux slightly behind on package maturity |
| Cross-platform (.NET) | .NET MAUI — Windows (WinUI 3 host) + macOS (Mac Catalyst) only; **no native Linux desktop target** as of mid-2026 (an Avalonia-powered Linux/browser backend is in preview) |
| Cross-platform (Kotlin) | Compose Multiplatform — shared Android/desktop UI |
| Native macOS | SwiftUI (default for new apps) + AppKit interop for advanced window/menu chrome |
| Native Windows | WPF for mature Windows-only line-of-business apps (Microsoft ships it, but it's in maintenance mode); WinUI 3 for a modern Windows 11 look, at the cost of a thinner control/answer ecosystem |
| Native Linux | GTK (GNOME), Qt (KDE) |
| Auto-update | electron-updater (NSIS target) or Tauri's built-in updater; Sparkle 2 (macOS); **avoid Squirrel.Windows for new work — unmaintained, superseded by NSIS** |
| Code signing | Apple notarization via `notarytool`; Windows Authenticode via Azure Artifact Signing (formerly "Trusted Signing") or a traditional EV/OV cert; Linux (distro-specific) |
| Installers | electron-builder, Tauri bundler, create-dmg, Inno Setup, NSIS, AppImage/Flatpak/Snap |
| Tauri 2 capability system, plugin breaks, WebView2, EU Accessibility Act | [references/tauri-2-migration.md](references/tauri-2-migration.md) | Tauri 2 production guide |
| Verify .app codesign + notarization | [scripts/check_signing.sh](scripts/check_signing.sh) | macOS codesign/spctl/stapler; Windows signtool commented |

## When to Use This Skill

- Choosing a framework for a new desktop application
- Building Electron or Tauri apps with correct security and IPC patterns
- Implementing desktop-specific features: file system access, system tray, native menus, protocol handlers, drag-and-drop
- Setting up code signing, notarization, and installer pipelines
- Adding auto-update mechanisms to desktop apps
- Reviewing desktop application architecture or security posture
- Migrating from Electron to Tauri (or evaluating the tradeoff)

## When NOT to Use This Skill

- **Web-only frontends (SPA, SSR, static sites)** → [software-frontend](../software-frontend/SKILL.md)
- **Mobile apps (iOS, Android, React Native)** → [software-mobile](../software-mobile/SKILL.md)
- **CLI tools and developer utilities** → [software-devtools](../software-devtools/SKILL.md)
- **System architecture and service decomposition** → [software-architecture-design](../software-architecture-design/SKILL.md)
- **Security audits and threat modeling** → [software-security-appsec](../software-security-appsec/SKILL.md)

## Workflow

1. Confirm the platform scope, native integration needs, distribution targets, and team constraints.
2. Route web-only, mobile, CLI, or system-design work to the adjacent skill when desktop is not the core problem.
3. Choose the framework and packaging approach from the decision tree.
4. Apply the relevant architecture, distribution, update, and security guidance for that stack.
5. Verify current signing, notarization, and platform-policy details through the navigation sources before final advice.

## ASCII Flow

```text
Desktop app task
  -> Identify platform, runtime, distribution, and native integration needs
  -> Choose framework or use existing stack conventions
  -> Design window, lifecycle, storage, update, and permissions behavior
  -> Implement bounded slice with platform-specific tests
  -> Verify packaging, signing, crash reporting, and OS behavior
  -> Report release blockers and handoffs
```

## Before Reaching for a Framework: Does This Need to Be Desktop At All?

A meaningful fraction of "we need a desktop app" requests are better served by a PWA — no code signing, no update server, no per-OS QA matrix. Push back and confirm desktop is the right call before opening the decision tree below:

- No deep OS integration required (no system tray persistence, no global shortcuts, no raw filesystem/serial/USB access, no offline-first local database as the primary store) → a PWA (installable, `manifest.json` + service worker) likely covers it with a fraction of the packaging and signing burden.
- Users are already inside a Chromium-family browser and don't need to run at machine startup or survive without the browser installed → PWA.
- The ask genuinely needs OS-level integration (file associations, native menus/tray, background services, hardware access, MSI/enterprise deployment, App Store distribution) → proceed to a native or hybrid desktop framework below.
- When in doubt, prototype the PWA first — it is cheap to abandon and expensive to have skipped.

## Decision Tree

```text
Desktop framework selection (after confirming a PWA won't do):

START
├─ Need full native platform integration and max performance?
│  ├─ macOS only → SwiftUI (+ AppKit for custom chrome)
│  ├─ Windows only → WPF (mature, stable, in maintenance mode) or WinUI 3 (modern look, thinner ecosystem)
│  └─ Linux only → GTK or Qt
├─ Have a web app and want desktop distribution?
│  ├─ Team knows Node.js, needs mature plugins / deepest native integration → Electron
│  ├─ Bundle size, memory, and a stronger default security posture matter, team can absorb some Rust → Tauri
│  └─ Also need iOS/Android from the same codebase → Tauri (mobile targets stable since 2.0; feature parity with desktop plugins still catching up)
├─ Already have a Flutter mobile app?
│  └─ Flutter Desktop (shared codebase; strongest on macOS, fewer production-grade Windows/Linux packages)
├─ Already have a Compose Android app?
│  └─ Compose Multiplatform Desktop
├─ .NET team needing desktop?
│  ├─ Windows + macOS only, want one XAML codebase across mobile too → .NET MAUI (no native Linux target yet)
│  └─ Windows-only → WPF (mature) or WinUI 3 (modern, Store-friendly)
├─ Bundle size and memory footprint critical?
│  └─ Tauri (Rust backend, OS webview, no bundled Chromium — commonly single-digit-to-low-double-digit MB installers vs 100MB+ for Electron)
└─ Security-sensitive app?
   └─ Tauri (no Node.js in renderer, capability-scoped IPC, CSP by default) — or Electron with `contextIsolation`/`sandbox` enforced as non-negotiables if the team can't take on Rust
```

### Electron vs Tauri: the gates that actually decide it

- **Team skills**: Electron if the team is JS/TS-only with no Rust appetite; Tauri if the team can own a Rust backend (or keep it thin and mostly use plugins).
- **Binary size / memory**: Electron ships Chromium + Node in every install (~100MB+, ~200-300MB idle RAM); Tauri uses the OS webview (~5-10MB installers, ~30-40MB idle RAM) — material for low-bandwidth distribution or resource-constrained machines.
- **Webview fragmentation risk**: Windows is low-risk — WebView2 is evergreen and bundled with Windows 11 (bootstrap it for Windows 10). Linux is real risk for Tauri — it depends on WebKitGTK, and distro packaging of `webkit2gtk-4.0` vs `4.1` (soup2 vs soup3) is actively fragmenting: Ubuntu 24.04+/Fedora 40+ dropped 4.0 dev packages, upstream 4.0 support ends March 2026, and older LTS images may lack 4.1 entirely. Pin and test against your minimum supported distro before committing to Tauri on Linux.
- **Plugin/ecosystem maturity**: Electron's plugin and tooling ecosystem is larger and older; Tauri's is smaller but growing quickly, especially since mobile landed.
- **Migration cost**: Electron → Tauri is closer to a rewrite than a refactor (different process model, different IPC, no Node.js APIs) — get this choice right up front rather than planning to switch later.

## Electron Architecture

Electron apps run two process types: the **main process** (Node.js, one per app) and **renderer processes** (Chromium, one per window).

**Process model and IPC**:
- Main process owns lifecycle, native APIs, menus, tray, and file system access.
- Renderer processes display UI and must never have direct Node.js access.
- Preload scripts bridge main and renderer via `contextBridge.exposeInMainWorld`.
- All cross-process communication flows through typed IPC channels (`ipcMain.handle` / `ipcRenderer.invoke`).

**Security model (mandatory)**:
- `contextIsolation: true` — always. No exceptions.
- `nodeIntegration: false` — always. Preload scripts are the only bridge.
- `webSecurity: true` — never disable in production.
- `sandbox: true` — enable for renderer processes.
- Validate and sanitize all IPC inputs in the main process.
- Restrict `webContents.loadURL` to known origins; never load arbitrary remote content.

**Key anti-patterns**:
- `nodeIntegration: true` in BrowserWindow options — exposes full Node.js to renderer.
- Disabling `webSecurity` to work around CORS — opens the app to remote code execution.
- Loading remote URLs in the main renderer without origin restrictions.
- Passing unsanitized user input through IPC to Node.js APIs.

## Tauri Architecture

Tauri apps pair a **Rust backend** with a **webview frontend** (the OS-native webview, not bundled Chromium).

**Core design**:
- Rust backend defines commands (`#[tauri::command]`) exposed to the frontend via an IPC bridge.
- Frontend can be any web framework (React, Svelte, Vue, vanilla) — Tauri is frontend-agnostic.
- IPC is capability-scoped (Tauri 2's permission system, not the old v1 allowlist): only explicitly granted commands and scopes are available per window/origin. See [references/tauri-2-migration.md](references/tauri-2-migration.md).
- Plugin system for file system, shell, dialog, notification, clipboard, and custom extensions.
- Since Tauri 2.0 (stable Oct 2024), the same codebase also targets iOS and Android — evaluate this before reaching for React Native/Flutter if the team already owns a Tauri desktop app and mobile parity is "good enough," not full native.
- **Sidecar pattern**: bundle a separate native binary (a Python service, a compiled CLI, a heavier compute engine) alongside the app and invoke it as a child process from the Rust backend (`tauri-plugin-shell`'s sidecar API) — useful when logic can't or shouldn't be ported to Rust/JS.

**Security advantages over Electron**:
- No Node.js in the frontend — the webview has no access to system APIs by default.
- CSP enforced by default in production builds.
- Capability files scope IPC per window, preventing unintended API exposure.
- Smaller attack surface — no Chromium binary, fewer dependencies.

**Tradeoffs**:
- Webview rendering can differ across platforms (WebKit on macOS/Linux, WebView2 on Windows) — and Linux WebKitGTK versioning (`webkit2gtk-4.0` vs `4.1`) is an active distro-fragmentation risk; verify your minimum supported Linux target builds and runs before committing.
- Smaller plugin ecosystem compared to Electron (growing quickly, especially post-mobile-stable).
- Requires Rust knowledge for backend customization and for writing custom plugins.
- Mobile targets are stable but not yet at full desktop feature/plugin parity — verify a given plugin supports iOS/Android before assuming cross-target parity.

## Desktop-Specific Concerns

**File system access**:
- Use save/open dialogs via framework APIs (never raw `fs` in renderer).
- Implement recent files list using platform conventions.
- Register file associations for custom file types in installer config.

**System tray and menu bar**:
- System tray for background-running apps; respect platform conventions (macOS uses menu bar, Windows uses system tray).
- Build native menus with keyboard shortcuts that match platform expectations (Cmd on macOS, Ctrl on Windows/Linux).

**Native integrations**:
- Notifications: use OS notification APIs, respect Do Not Disturb / Focus modes.
- Global shortcuts: register sparingly, avoid conflicts with OS shortcuts.
- Protocol handlers / deep links: register custom URL schemes (`myapp://`) for OAuth callbacks and cross-app linking.
- Drag-and-drop: support file drops on app icon (macOS) and window content.
- Clipboard: read/write with proper content type handling (text, HTML, images).
- Multi-window management: track window state, restore positions, handle multi-monitor setups.

**Offline-first**:
- Desktop apps are offline by default. Design data sync, not data fetch.
- Use local storage (SQLite, IndexedDB, or app-specific files) as the source of truth.
- Sync to cloud when connectivity is available; handle merge conflicts.

## Distribution and Updates

**Code signing** (required for trusted distribution):
- macOS: Apple Developer ID certificate + notarization via `notarytool` (`altool` was removed by Apple in November 2023 — treat any `altool` reference as dead). Without notarization, Gatekeeper blocks the app.
- Windows: traditional EV/OV Authenticode certificates now require a hardware token or HSM per CA/Browser Forum baseline requirements (since June 2023), which breaks most CI pipelines. Microsoft's cloud-native alternative — **Azure Artifact Signing** (the GA name; it shipped as "Trusted Signing" in preview) — signs from CI without a physical token and is generally available for US/Canada/EU/UK-registered businesses and, more recently, verified individuals. Prefer it for new Windows signing pipelines; fall back to a traditional EV cert only if Artifact Signing's regional/eligibility requirements don't fit. Unsigned apps trigger SmartScreen warnings, and Windows 11 24H2's Smart App Control blocks unsigned/low-reputation executables outright.
- Linux: signing varies by distribution channel (Snap Store, Flathub have their own trust models; AppImage supports optional GPG detached signatures).

**Installer creation**:
- macOS: DMG (drag-to-Applications), PKG (scripted install). Use `create-dmg` or `electron-builder`.
- Windows: NSIS, Inno Setup, or MSI. `electron-builder` and Tauri bundler handle these.
- Linux: AppImage (portable), Flatpak (sandboxed), Snap (Ubuntu store), .deb/.rpm (distro-specific).

**Auto-update mechanisms**:
- Electron: `electron-updater` with GitHub Releases, S3, or custom server; target NSIS on Windows. Supports differential updates and signature verification.
- **Squirrel.Windows is dead for new projects** — the upstream project is unmaintained (PRs/issues no longer reviewed) and electron-updater's simplified auto-update flow doesn't support it. Migrate existing Squirrel-based installers to NSIS.
- Tauri: built-in updater plugin (`tauri-plugin-updater`) with mandatory Minisign (Ed25519) signature verification and configurable per-target endpoints. Tauri v1 keys are a different format and are not interchangeable with v2 — regenerate for v2.
- macOS native: Sparkle 2 (current major; adds sandboxed-app support and a modern install pipeline) for non-Electron/non-Tauri apps, or `tauri-plugin-sparkle-updater` / WinSparkle equivalents.
- Delta updates reduce download size for frequent releases.
- **Operational burden of self-hosting an update server**: signature-key custody, TLS-cert renewal, staged/canary rollout, and the ability to halt a bad release are real ongoing costs — most teams underestimate this until a bad build needs to be pulled. GitHub Releases (Electron) or a static object-store endpoint (Tauri) removes most of that burden versus a bespoke update server; only build custom infrastructure when you need staged rollout percentages or enterprise-specific channels the hosted options don't support.

**App store distribution**:
- Mac App Store: requires the App Sandbox entitlement and Apple review. Some Electron/Tauri APIs (raw filesystem access outside sandbox containers, some IPC/child-process patterns) are restricted or need sandbox-safe rewrites. Trade-off: MAS buys discoverability, trusted-install psychology, and Apple-run payments, at the cost of review latency, a 15-30% commission, and giving up your own update cadence/channel (App Store review turnaround, not your release pipeline, gates ship speed). Direct distribution (notarized DMG/PKG) keeps full control of updates and payments but forfeits Store discovery and requires you to run your own trust/update story end-to-end.
- Microsoft Store: supports MSIX packaging. Broader API access than Mac App Store; still subject to Store review and packaging constraints.
- Snap Store: straightforward for Linux; auto-update built in, but Snap's confinement model can restrict filesystem/device access similarly to sandboxing.

## Known Traps

- Developing only on one operating system and discovering packaging, permissions, or rendering failures after release.
- Treating auto-update as a later enhancement when desktop users will quickly diverge onto stale and insecure builds.
- Treating OS webviews as interchangeable: WebKit (macOS/Linux) and WebView2 (Windows) differ in CSS support, font rendering, and media codec availability — test on all three platforms before shipping.
- Shipping protocol handlers, file associations, or deep links without validating hostile input, duplicate launches, and auth callback flow.
- Depending on filesystem paths, tray behavior, or window chrome that only match one platform's conventions.
- Leaving crash reporting, update rollback, and corrupted local-state recovery undefined until after the first production incident.

## Common Anti-Patterns

- **Shipping Chromium when a webview suffices** — if you don't need Chromium-specific APIs, Tauri routinely cuts installer size from 100MB+ down to single-digit-to-low-double-digit MB and idle memory from ~200-300MB to ~30-40MB (exact numbers vary by app; re-benchmark your own build rather than quoting these as guarantees).
- **Storing secrets in the renderer process** — use the main/backend process with OS keychain integration (keytar, keyring).
- **Missing auto-update** — desktop apps without auto-update become permanently stale. Implement from day one.
- **Ignoring platform conventions** — macOS expects menus in the menu bar, Cmd+Q to quit, and native title bars. Windows expects different keyboard shortcuts and window chrome. Test on each target platform.
- **Not testing on all target platforms** — webview rendering and native API behavior differ. CI should build and test on macOS, Windows, and Linux.
- **Bundling development dependencies in production** — audit `package.json` dependencies vs devDependencies. Use `electron-builder`'s pruning or Tauri's Rust release profile.
- **Ignoring process crashes** — handle main process crashes gracefully. Implement crash reporting (Sentry, Crashpad).

## Scenarios

1. **New cross-platform app** — Confirm platform targets, team language constraints, and bundle size requirements. Route to the framework decision tree; apply Tauri 2 capability config or Electron security defaults as appropriate.
2. **Tauri 1 to Tauri 2 migration** — Audit the existing `tauri.conf.json` allowlist, run `cargo tauri migrate`, review generated capability files, update all plugin imports from `tauri::api::*` to `@tauri-apps/plugin-*`, and update frontend `invoke` calls to `@tauri-apps/api/core`.
3. **Code signing and notarization pipeline setup** — Confirm platform targets; apply notarytool for macOS (altool was removed), Azure Artifact Signing or an HSM/hardware-token-backed EV/OV cert for Windows (CA/Browser Forum has required hardware-protected private keys for both EV and OV code-signing since June 2023 — software-only cert files are no longer issuable), and GPG for AppImage on Linux. Check `references/april-platform-traps.md` for current platform requirements.
4. **EU Accessibility Act compliance check** — Determine if the app is in scope (B2C, EU distribution, post-June 2025). Audit against EN 301 549 / WCAG 2.1 AA: keyboard navigation, screen reader support, colour contrast, focus management on modals, and resize behaviour.
5. **Auto-update implementation** — Choose the updater for the framework (Tauri updater plugin with a Minisign keypair, or electron-updater targeting NSIS with signature verification). Do not adopt Squirrel.Windows for new projects — it is unmaintained. Implement from day one; retrofitting auto-update is expensive.
6. **"Do we even need a desktop app?" gate** — Before any of the above, check whether a PWA satisfies the actual requirement (see "Before Reaching for a Framework" above). Saves a packaging/signing/update pipeline entirely when it does.

## EU Accessibility Act

The European Accessibility Act (EAA) Directive 2019/882 entered enforcement on **28 June 2025** for new products. Desktop B2C apps distributed in the EU are in scope. The applicable technical standard is EN 301 549, which references WCAG 2.1 Level AA for software UIs. Existing products have until 28 June 2030 to conform; new products sold after June 2025 must conform immediately.

### EAA Compliance Checklist

- [ ] All functionality operable by keyboard alone (no mouse-only interactions)
- [ ] Screen reader tested: VoiceOver on macOS, NVDA or JAWS on Windows
- [ ] Minimum colour contrast 4.5:1 for normal text, 3:1 for large text (18pt+)
- [ ] UI does not clip or overlap at 200% text scale
- [ ] Focus visibly indicated and trapped inside modal dialogs
- [ ] No flashing content between 3–50 Hz (seizure risk)
- [ ] Alternative text on all non-decorative images and icons
- [ ] Error messages identify the field in error and suggest a fix

See `references/april-platform-traps.md` for framework-specific (Electron, Tauri, Flutter) guidance.

## Navigation

### References
- [references/framework-selection.md](references/framework-selection.md) — Electron vs Tauri vs Flutter Desktop vs .NET MAUI selection guidance
- [references/distribution-and-signing.md](references/distribution-and-signing.md) — packaging, code signing, notarization, and update rollout guidance
- [references/april-platform-traps.md](references/april-platform-traps.md) — Tauri 2 migration, Electron security defaults, WebView2 versioning, macOS / Windows permission changes, EU Accessibility Act, code signing, and auto-update traps
- [Skill Sources](data/sources.json): curated primary sources for desktop development.

### Related Skills

- [software-frontend](../software-frontend/SKILL.md) — Web frontend frameworks and SPA patterns
- [software-mobile](../software-mobile/SKILL.md) — Mobile app development (iOS, Android, cross-platform)
- [software-backend](../software-backend/SKILL.md) — Backend service patterns (relevant for Electron main process / Tauri Rust backend)
- [software-security-appsec](../software-security-appsec/SKILL.md) — Application security, threat modeling
- [ops-devops-platform](../ops-devops-platform/SKILL.md) — CI/CD pipelines for build and distribution
- [software-architecture-design](../software-architecture-design/SKILL.md) — System-level architecture decisions

## Freshness Protocol

When users ask version-sensitive questions about desktop frameworks, verify current information before answering.

### Trigger Conditions

- "What's the latest Electron version?"
- "Should I use Electron or Tauri?"
- "Is Flutter Desktop production-ready?"
- "What's new in Tauri v2 / v3?"
- "Is .NET MAUI stable for desktop?"

### How to Freshness-Check

1. Start from [data/sources.json](data/sources.json) (official docs, release notes, changelogs).
2. Run a targeted web search for the specific framework version or feature.
3. Prefer official project documentation and release announcements over blog posts.

### What to Report

- **Current landscape**: what is stable and widely used now
- **Emerging trends**: what is gaining traction (and why)
- **Deprecated/declining**: what is falling out of favor (and why)
- **Recommendation**: default choice + 1-2 alternatives, with trade-offs

## Fact-Checking

- Known bugs, regressions, framework/compiler/runtime footguns, and version-specific crash or workaround guidance must be verified against current primary web sources before being treated as current fact.
- Use web search/web fetch to verify current external facts, versions, pricing, deadlines, regulations, or platform behavior before final answers.
- Prefer primary sources; report source links and dates for volatile information.
- Re-check Electron security defaults, Tauri capability and updater behavior, Compose Desktop platform support, and MAUI packaging/notarization details before making version-sensitive recommendations.
- If web access is unavailable, state the limitation and mark guidance as unverified.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.

