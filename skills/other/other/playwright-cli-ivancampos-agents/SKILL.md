---
name: playwright-cli
description: Translate natural-language browser automation requests into exact `playwright-cli` commands for interactive web testing and debugging. Use when requests involve opening/navigating pages, interacting with elements, capturing snapshots/screenshots/PDFs, using tabs, inspecting console/network, mocking routes, managing cookies/storage/state, configuring browser sessions, or controlling named Playwright CLI sessions.
---

# Playwright CLI

Use `playwright-cli` directly (already installed) to execute browser automation from natural-language requests.

## Quick Start

1. Verify the CLI is available:
   ```bash
   command -v playwright-cli >/dev/null 2>&1
   ```
2. Open a browser session:
   ```bash
   playwright-cli open https://example.com
   ```
3. Capture refs before ref-based commands:
   ```bash
   playwright-cli snapshot
   ```

## Natural-Language Execution Workflow

1. Parse the request into atomic actions.
2. Convert each action to command templates from `references/command-map.md`.
3. Run `playwright-cli snapshot` before commands that require element refs (`click`, `fill`, `check`, `select`, `hover`, `drag`, etc.) unless a fresh snapshot is already available.
4. Re-run `playwright-cli snapshot` after navigation or major DOM changes.
5. For assertions, prefer `playwright-cli eval` and parse the `### Result` value from stdout.
6. Treat `### Error` output as command failure, even when process exit code is `0`.
7. For screenshots, capture PNG first, then compress to JPEG with `ffmpeg` before final save/return.
8. Use explicit filenames when saving artifacts (screenshots, snapshots, PDFs, videos, storage state).
9. Return executed commands and key results (URLs, counts, file paths, errors).

## Command Mapping Rules

- Map intent verbs directly:
  - open/launch -> `open`
  - navigate -> `goto`
  - click/tap -> `click`
  - double click/double tap -> `dblclick`
  - type/input -> `type`
  - fill/set field -> `fill`
  - back/forward/refresh -> `go-back`/`go-forward`/`reload`
- Preserve user-provided optional flags and values.
- Omit optional args when unspecified.
- Use `-s=<name>` when the user asks for a named/session-isolated browser.
- Prefer native commands over `eval` and `run-code`; use `eval` or `run-code` only if no first-class command exists.
- Keep session names short and filesystem-safe (lowercase letters + numbers, no punctuation, target <= 12 chars) to avoid local socket path errors on macOS.

## Reliability Guardrails (Must Follow)

- Do not classify pass/fail from shell exit codes for `eval` or `run-code`.
- Always inspect command output:
  - If output contains `### Error`, treat as failure.
  - If output contains `### Result`, use that value for assertions.
- Prefer `eval` for boolean checks and DOM assertions.
- Use `run-code` for imperative Playwright flows only.
- `run-code` expects a valid JS expression; statements like bare `return ...` or `throw ...` are invalid.
- For JS snippets passed to `eval`, prefer expression-safe patterns:
  - Good: `Array.from(...).some(function(x){ ... })`
  - Risky in this CLI context: snippets that are parsed as non-expression wrappers.
- When user requests pass and fail screenshots:
  - Capture one screenshot per scenario after assertion.
  - Capture to temporary PNG, then convert with `ffmpeg` to JPEG as the final artifact.
  - Name final files with scenario status prefix, e.g. `pass-<name>.jpg`, `fail-<name>.jpg`.
  - Save a machine-readable index file (`results.txt` or JSON) mapping scenario -> status -> final JPEG artifact path.

## Screenshot Compression Rule (Required)

- Always return compressed JPEG screenshots, not raw PNG screenshots.
- Required flow:
  1. Capture screenshot to temporary PNG path.
  2. Compress to JPEG with `ffmpeg`.
  3. Return/report only the JPEG path.
- Default command pattern:
  ```bash
  playwright-cli screenshot --full-page --filename "$TMP_PNG"
  ffmpeg -y -i "$TMP_PNG" -q:v 4 "$FINAL_JPG"
  ```
- If `ffmpeg` is unavailable, stop and report the missing dependency instead of returning an uncompressed PNG.

## Session and Artifact Conventions

- Use default session unless the user requests named sessions.
- Keep multi-step flows in one session for continuity.
- Place generated artifacts in predictable paths when the user does not specify:
  - `output/playwright/*.jpg`
  - `output/playwright/*.pdf`
  - `output/playwright/*.json`
  - `output/playwright/*.zip`

## Full Command Coverage

Load `references/command-map.md` when mapping or validating command usage. It contains the complete command catalog for:

- Core
- Navigation
- Keyboard
- Mouse
- Save as
- Tabs
- Storage (state, cookies, localStorage, sessionStorage)
- Network
- DevTools
- Install
- Configuration
- Sessions
