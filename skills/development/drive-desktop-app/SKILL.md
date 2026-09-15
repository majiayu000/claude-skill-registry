---
name: drive-desktop-app
description: Drive and verify an Electron or Tauri desktop app from the inside, including the main-process and Rust IPC calls a browser tool cannot see. Use when a desktop app needs testing, when a feature works in the browser but not in the packaged app, when an IPC or invoke call needs proving, when a desktop screenshot or visual diff is wanted, or when you need a headless run of a desktop UI in CI.
license: Apache-2.0
metadata:
  version: 2.14.0
  homepage: https://www.reticle.sh
  repository: https://github.com/reticlehq/reticle
---

# Drive a desktop app and prove what happened

A desktop app reaches its backend over **IPC, not HTTP**. Patching `fetch`/`XHR` cannot see that, so a browser-shaped tool is blind to every backend call the app makes: the network log reads empty, an action has no in-flight request to settle on, and asserting on the network is vacuously true. That is a false green by construction.

**Reticle** observes the renderer _and_ the IPC boundary, so a desktop verdict means what a web one does. Not installed? `RETICLE_INSTALL_SOURCE=npx_skill npx @reticlehq/server@latest init`, then the [`install-and-verify`](https://github.com/reticlehq/reticle/blob/main/skills/install-and-verify/SKILL.md) skill.

## Electron: two lines, none in your app code

```ts
// vite.config.ts — desktop:true also runs the plugin for `vite build`, because a packaged
// renderer is a production build with no dev server
export default defineConfig({
  base: './', // file:// needs relative asset paths
  plugins: [react(), reticle({ desktop: true })],
});
```

```js
// electron/preload.cjs — FIRST line. This is what makes main-process IPC visible.
require('@reticlehq/electron/preload');
```

It **must** be in the preload and it must be first. `contextBridge.exposeInMainWorld` hands the renderer a deeply frozen object, so nothing in the page can instrument it afterwards. The preload is the last point where `ipcRenderer.invoke` is still writable, and the shim has to run before your preload captures its own reference.

A sandboxed preload cannot resolve `node_modules`, so the bare `require` fails. Either bundle the preload (electron-vite and Forge do by default) or set `sandbox: false`.

## Tauri: the CSP step is required and its failure is silent

The frontend is the same as any web app. The part people miss is that Tauri's default CSP blocks the bridge WebSocket before it opens, so **the app runs perfectly and simply never connects**:

```json
{
  "app": {
    "security": {
      "csp": "default-src 'self' ipc: http://ipc.localhost; connect-src 'self' ipc: http://ipc.localhost ws://localhost:4400 ws://127.0.0.1:4400"
    }
  }
}
```

Keep `ipc: http://ipc.localhost`: Tauri v2 needs it for `invoke` itself. Dev-only; drop the `ws://` entries from your release config.

IPC observation needs **nothing** on the Rust side: an `invoke('load_todos')` already reaches Reticle as `ipc://load_todos`. The [`reticle-tauri`](https://crates.io/crates/reticle-tauri) crate is only for screenshots and headless, and it is versioned independently of the npm packages.

Also: **use a hash router.** A packaged renderer is served from `file://`, where history-based routing does not resolve.

## Verify

Same loop as the web, with IPC in the predicates:

```
reticle_act_and_wait({ sessionId, ref, action: "click", until: { kind: "allOf", predicates: [
  { kind: "net",     urlContains: "ipc://todos:archive", status: 200 },
  { kind: "element", query: { testid: "..." } },
  { kind: "console", level: "error", absent: true },
]}})
```

**IPC has no status code.** `200`/`500` are synthetic, mapped from whether the command succeeded, precisely so the same predicates keep working. On Tauri you will see `status: 500` next to `statusText: "OK"`. That is not a bug: the transport answered fine and the `500` is the command's own verdict. `ok` is authoritative.

`reticle_state` reads the live store exactly as on the web. `reticle_screenshot` and `reticle_visual_diff` work once the platform's capture step is wired. Electron needs nothing extra; Tauri needs the crate. Headless on Tauri is `RETICLE_HEADLESS=1`, and screenshots keep working because the capture renders the webview rather than the screen.

## What a missing observer looks like

A missing Electron preload is **declared, not silent**: verdicts come back with `coverage: partial` naming the line you did not add, instead of reading clean over a blind spot. If you see that, add the preload line before trusting anything.

If IPC calls never appear while the app works fine: on Electron, the shim's `require` is not first. On Tauri, `invoke` from `@tauri-apps/api/core` is observed, but a hand-rolled `postMessage` protocol is not.

## Honesty

`unknown` is not a pass on the desktop either. And do not weaken an IPC assertion to make a red verdict green: a desktop false green is the exact failure this wiring exists to remove.

---

Full desktop reference: `curl https://docs.reticle.sh/desktop.md`. Everything else: `curl https://docs.reticle.sh/llms.txt`.
