---
name: script-kit-architecture
description: Script Kit GPUI codebase architecture. Use when navigating the codebase, understanding module structure, or tracing data flow. Covers repository structure, SDK deployment, configuration, and secondary windows.
---

# Script Kit Architecture

Overview of the Script Kit GPUI codebase structure.

## Repository Structure (Key Modules)

`src/`
- `main.rs` - app entry + window setup + main render loop + ErrorNotification UI
- `error.rs` - `ScriptKitError`, `ErrorSeverity`, `NotifyResultExt`
- `theme.rs` - theme system
- `prompts.rs` - ArgPrompt, DivPrompt, EditorPrompt
- `actions.rs` - ActionsDialog
- `protocol.rs` - stdin JSON protocol + `ParseResult`
- `scripts.rs` - script loading + execution instrumentation
- `config.rs` - config loading + defaults
- `executor.rs` - bun execution + timing spans + structured logging
- `watcher.rs` - file watchers
- `panel.rs` - macOS panel configuration
- `perf.rs` - perf timing utilities
- `logging.rs` - dual-output logging (JSONL + pretty/compact)
- `lib.rs` - exports
- `utils.rs` - shared utilities
- `notes/` - Notes window module
- `ai/` - AI chat window module

Logs: `~/.scriptkit/logs/script-kit-gpui.jsonl`

## SDK Deployment Architecture

SDK source: `scripts/kit-sdk.ts`

Two-tier deployment:
1. **Build time (dev):** `build.rs` copies `scripts/kit-sdk.ts` to `~/.scriptkit/sdk/`
2. **Compile time:** `executor.rs` embeds via `include_str!("../scripts/kit-sdk.ts")`
3. **Runtime:** `ensure_sdk_extracted()` writes embedded SDK to `~/.scriptkit/sdk/kit-sdk.ts`
4. **Execution:** `bun run --preload ~/.scriptkit/sdk/kit-sdk.ts <script>`

Tests import `../../scripts/kit-sdk` (repo path). Production uses runtime-extracted SDK.

tsconfig mapping:
```json
{ "compilerOptions": { "paths": { "@scriptkit/sdk": ["./sdk/kit-sdk.ts"] } } }
```

## User Configuration (`~/.scriptkit/config.ts`)

```ts
import type { Config } from "@scriptkit/sdk";
export default {
  hotkey: { modifiers: ["meta"], key: "Semicolon" },
  padding: { top: 8, left: 12, right: 12 },
  editorFontSize: 16,
  terminalFontSize: 14,
  uiScale: 1.0,
  builtIns: { clipboardHistory: true, appLauncher: true },
  bun_path: "/opt/homebrew/bin/bun",
  editor: "code"
} satisfies Config;
```

Rust helpers (use these; they handle defaults):
- `config.get_editor_font_size()` (default 14)
- `config.get_terminal_font_size()` (default 14)
- `config.get_padding()` (top 8, left/right 12)
- `config.get_ui_scale()` (default 1.0)
- `config.get_builtins()` (clipboardHistory/appLauncher default true)
- `config.get_editor()` (default `"code"`)

Font sizing:
- Editor: `line_height = font_size * 1.43`
- Terminal: `line_height = font_size * 1.3`

## References

- [System Diagrams](references/diagrams.md) - Architecture, state machine, execution flow diagrams
- [Notes Window](references/notes-window.md) - Notes module details
- [AI Window](references/ai-window.md) - AI chat module details
- [Gotchas](references/gotchas.md) - Common issues and fixes
- [Vibrancy](references/vibrancy.md) - macOS vibrancy/blur patterns
