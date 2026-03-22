---
name: build-extension
description: Build, test, and package VSCode extensions in the dart_node repo
argument-hint: "[too-many-cooks|dart-node-vsix] [build|test|package|install]"
disable-model-invocation: true
allowed-tools: Bash
---

# Build VSCode Extensions

This repo has two VSCode extension components:

| Component | Location | What it is |
|-----------|----------|------------|
| **dart_node_vsix** | `packages/dart_node_vsix/` | The SDK package — Dart bindings for the VSCode extension API (commands, tree views, webviews, status bar, etc.) |
| **too_many_cooks** | `examples/too_many_cooks_vscode_extension/` | A concrete extension built with that SDK — multi-agent coordination UI |

## too-many-cooks extension

**Full build** (MCP server + extension + .vsix package):
```bash
bash examples/too_many_cooks_vscode_extension/build.sh
```

This does:
1. Compiles MCP server: `dart compile js` → `add_preamble.dart` → `server_node.js`
2. Compiles extension: `dart compile js` → `wrap-extension.js` bridge → `out/lib/extension.js`
3. Packages: `vsce package` → `.vsix` file

**Test** (runs Mocha tests under a real VSCode instance):
```bash
cd examples/too_many_cooks_vscode_extension && npm run pretest && npm test
```
On headless Linux, prefix with `xvfb-run -a`.

**Install into VSCode**:
```bash
code --install-extension examples/too_many_cooks_vscode_extension/*.vsix
```

## dart_node_vsix SDK package

**Test the SDK** (Dart tests compiled to JS, run in VSCode):
```bash
cd packages/dart_node_vsix && npm install && npm run compile && npm test
```

**What it provides** — Dart bindings for:
- `commands`, `window`, `workspace`, `statusBar`
- `TreeView`, `Webview`, `OutputChannel`
- `ExtensionContext`, `Disposable`
- `Mocha` test API bindings
- JS interop helpers (`Promise`, `EventEmitter`)

## Architecture

Both use the same pattern: Dart → `dart compile js` → wrapper script → VSCode-compatible JS module.

The wrapper scripts (`scripts/wrap-extension.js`, `scripts/wrap-tests.js`) bridge dart2js output to VSCode's CommonJS `require`/`module.exports` system and inject polyfills (navigator, self) needed by dart2js async scheduling.
