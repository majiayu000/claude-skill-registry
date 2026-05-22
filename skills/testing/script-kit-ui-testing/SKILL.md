---
name: script-kit-ui-testing
description: UI testing protocol for Script Kit GPUI. Use when testing UI changes, running scripts, capturing screenshots, or debugging layout. Covers stdin JSON protocol, visual testing, and grid overlay.
---

# Script Kit UI Testing

All UI testing uses the stdin JSON protocol. Never pass scripts as CLI arguments.

## Stdin JSON Protocol

**Correct:**
```bash
echo '{"type":"run","path":"'"$(pwd)"'/tests/smoke/test-editor-height.ts"}' | \
  SCRIPT_KIT_AI_LOG=1 ./target/debug/script-kit-gpui 2>&1
```

**Wrong (does nothing):**
```bash
./target/debug/script-kit-gpui tests/smoke/hello-world.ts
```

Always set `SCRIPT_KIT_AI_LOG=1` when testing (saves ~70% tokens).

## Available Stdin Commands

```json
{"type":"run","path":"/abs/path/to/script.ts"}
{"type":"show"}
{"type":"hide"}
{"type":"setFilter","text":"search term"}
{"type":"showGrid","showBounds":true}
{"type":"hideGrid"}
{"type":"openNotes"}
{"type":"openAi"}
```

## Build-Test Loop

```bash
cargo build
echo '{"type":"run","path":"'"$(pwd)"'/tests/smoke/test-editor-height.ts"}' | \
  SCRIPT_KIT_AI_LOG=1 ./target/debug/script-kit-gpui 2>&1
```

Log filtering:
```bash
... | grep -iE 'RESIZE|editor|height_for_view|700'
tail -50 ~/.scriptkit/logs/script-kit-gpui.jsonl | grep -i resize
```

## Visual Testing (Screenshots)

Use SDK `captureScreenshot()` (captures **only the app window**). Save PNG to `.test-screenshots/`. **Read the PNG** to verify.

Blocked tools (do not use): `screencapture`, `scrot`, `gnome-screenshot`, `flameshot`, `maim`, ImageMagick `import`.

Minimal pattern:
```ts
import '../../scripts/kit-sdk';
import { mkdirSync, writeFileSync } from 'fs';
import { join } from 'path';

await div(`<div class="p-4 bg-blue-500 text-white rounded-lg">Test</div>`);
await new Promise(r => setTimeout(r, 500));

const shot = await captureScreenshot();
const dir = join(process.cwd(), '.test-screenshots');
mkdirSync(dir, { recursive: true });

const path = join(dir, `shot-${Date.now()}.png`);
writeFileSync(path, Buffer.from(shot.data, 'base64'));
console.error(`[SCREENSHOT] ${path}`);
process.exit(0);
```

## Grid Overlay

```bash
echo '{"type":"showGrid","showBounds":true}' | ./target/debug/script-kit-gpui
echo '{"type":"showGrid","showBounds":true,"showBoxModel":true,"showAlignmentGuides":true,"showDimensions":true}' | ./target/debug/script-kit-gpui
echo '{"type":"hideGrid"}' | ./target/debug/script-kit-gpui
```

Options: `gridSize` (default 8), `showBounds`, `showBoxModel`, `showAlignmentGuides`, `showDimensions`, `depth` ("prompts" | "all" | component names).

Color coding: prompts red, inputs teal, buttons yellow, lists mint, headers plum, containers sky.

## Programmatic Layout Info

SDK `getLayoutInfo()` returns:
```ts
interface LayoutInfo {
  windowWidth: number; windowHeight: number;
  promptType: string; // "arg"|"div"|"editor"|"mainMenu"|...
  components: LayoutComponentInfo[];
  timestamp: string;
}
```

## Anti-Patterns

- Running scripts via CLI args (must use stdin JSON)
- "I can't test without manual interaction" (use stdin + logs + screenshots)
- Not using `SCRIPT_KIT_AI_LOG=1`
- Capturing screenshot but not reading/verifying PNG
- Guessing at layout (use `captureScreenshot()` / `getLayoutInfo()` / grid overlay)

## References

- [Layout Info Details](references/layout-info.md) - Full LayoutComponentInfo interface
