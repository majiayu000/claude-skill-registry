---
name: collaborating-with-gemini
description: Use the Gemini CLI to consult Gemini and delegate coding tasks for prototyping, debugging, and code review. Supports multi-turn sessions via SESSION_ID. Optimized for low-token, file/line-based handoff.
metadata:
  short-description: Delegate to Gemini CLI
---

# Collaborating with Gemini (Codex)

Use Gemini CLI as a collaborator while keeping Codex as the primary implementer.

This skill provides a lightweight bridge script that returns structured JSON and supports multi-turn sessions via `SESSION_ID`.

## Core rules
- Gemini is a collaborator; you own the final result and must verify changes locally.
- Do not invoke `gemini` directly; always use the bridge script (`scripts/gemini_bridge.py`) so output/session handling stays consistent.
- Prefer file/line references over pasting snippets. Run the bridge with `--cd` set to the repo root (it sets the `gemini` process working directory). Use `--cd "."` only if your CWD is the repo root.
- For code changes, request **Unified Diff Patch ONLY** and forbid direct file modification.
- Always capture `SESSION_ID` and reuse it for follow-ups to keep the collaboration conversation-aware.
- Keep a short **Collaboration State Capsule** updated while this skill is active.
- Default timeout: when invoking via the Codex command runner, set `timeout_ms` to **600000 (10 minutes)** unless a shorter/longer timeout is explicitly required.
- Optional: pass `--sandbox` to run Gemini in sandbox mode.

## Quick start (shell-safe)

⚠️ If your prompt contains Markdown backticks (`` `like/this` ``), do **not** pass it directly via `--PROMPT "..."` (your shell may treat backticks as command substitution). Use a heredoc instead; see `references/shell-quoting.md`.

```bash
PROMPT="$(cat <<'EOF'
Review src/auth.py around login() and propose fixes.
OUTPUT: Unified Diff Patch ONLY.
EOF
)"
python3 .codex/skills/collaborating-with-gemini/scripts/gemini_bridge.py --cd "." --PROMPT "$PROMPT"
```

**Output:** JSON with `success`, `SESSION_ID`, `agent_messages`, and optional `error` / `all_messages`.

## Multi-turn sessions

```bash
# Start a session
PROMPT="$(cat <<'EOF'
Analyze the bug in foo(). Keep it short.
EOF
)"
python3 .codex/skills/collaborating-with-gemini/scripts/gemini_bridge.py --cd "." --PROMPT "$PROMPT"

# Continue the same session
PROMPT="$(cat <<'EOF'
Now propose a minimal fix as Unified Diff Patch ONLY.
EOF
)"
python3 .codex/skills/collaborating-with-gemini/scripts/gemini_bridge.py --cd "." --SESSION_ID "<SESSION_ID>" --PROMPT "$PROMPT"
```

## Prompting patterns (token efficient)

Use `assets/prompt-template.md` as a starter when crafting `--PROMPT`.

### 1) Ask Gemini to open files itself
Provide:
- Entry file(s) and approximate line numbers
- Objective and constraints
- Output format (diff vs analysis)

Avoid:
- Pasting large code blocks
- Multiple competing objectives in one request

### 2) Enforce safe output for code changes
Append this to prompts when requesting code:
- `OUTPUT: Unified Diff Patch ONLY. Strictly prohibit any actual modifications.`

### 3) Use Gemini for what it’s good at
- Alternative solution paths and edge cases
- UI/UX and readability feedback
- Review of a proposed patch (risk spotting, missing tests)

### 4) Sharing clipboard screenshots with Gemini

Gemini can only read files inside the workspace root (`--cd`). Codex saves clipboard PNGs into the OS temp directory (e.g. `${TMPDIR:-/tmp}`), which Gemini can’t access, and it may refuse ignored paths (e.g. `tmp/`). Copy the image into `.codex_uploads/`, then reference that path in your prompt. Delete screenshots when done. **Do not add `.codex_uploads/` to `.gitignore`**—Gemini refuses to read ignored paths.

```bash
mkdir -p .codex_uploads && cp "${TMPDIR:-/tmp}"/codex-clipboard-<id>.png .codex_uploads/
```

## Advanced flags
- `--sandbox`: Run Gemini in sandbox mode.
- `--model <name>`: Override the default Gemini model.
- `--return-all-messages`: Include all raw messages (tool calls, traces) in output JSON.

## Collaboration State Capsule
Keep this short block updated near the end of your reply while collaborating:

```text
[Gemini Collaboration Capsule]
Goal:
Gemini SESSION_ID:
Files/lines handed off:
Last ask:
Gemini summary:
Next ask:
```

## References
- `assets/prompt-template.md` (prompt patterns)
- `references/shell-quoting.md` (shell quoting/backticks)
