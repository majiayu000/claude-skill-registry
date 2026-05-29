---
name: ask-opencli
description: Ask Grok or Gemini via opencli (browser-session based, no API cost). Use when the user says "问 grok", "问 gemini", "ask grok", "ask gemini", "用 grok 查", "grok 怎么看", "让 gemini 分析", or wants a second opinion from Grok/Gemini without paying API tokens. Routes to opencli which drives the already-logged-in Chrome session.
---

# Ask via OpenCLI (Grok / Gemini)

Use `opencli` to query Grok or Gemini through the user's already-logged-in Chrome session. Zero API cost, fully driven by the existing browser session.

> **opencli 项目**：https://github.com/jackwener/opencli
> **安装**：`npm install -g @jackwener/opencli`（需要 Node ≥20）
> **首次运行**：`opencli doctor` 会自动引导安装 Chrome Browser Bridge 扩展
> **登录**：用装了扩展的 Chrome profile 打开 grok.com 和 gemini.google.com 登录一次
> **必须环境变量**：`export OPENCLI_BROWSER_COMMAND_TIMEOUT=300`（写进 shell rc）
> **更深度的多 AI 并行调研工作流**：use the `multi-ai-research` skill instead

**When to trigger**:
- User explicitly asks to query Grok or Gemini ("问一下 grok", "用 gemini 查", "让 grok 看看")
- User wants a second opinion / external advisor from Grok or Gemini
- User says "ask grok"/"ask gemini" or mentions these two as the information source

**When NOT to trigger**:
- User wants to use native Gemini CLI (`gemini -p`) → use `ask-gemini` skill instead
- User wants Claude's own opinion → answer directly
- User wants other AI (Doubao, Yuanbao, ChatGPT, etc.) → use other tools

## Model selection

If the user doesn't specify which model, default to **Grok** for real-time / social / news / tech-trend questions, and **Gemini** for long-form reasoning, research, coding, and document analysis.

If still ambiguous, ask the user which one to use before sending.

## ⚠️ 常见错误命令（直接 fail fast）

| ❌ 错误 | ✅ 正确 | 原因 |
|---|---|---|
| `opencli gemini chat "..."` | `opencli gemini ask "..."` | 没有 `chat` 子命令 |
| `opencli grok chat "..."` | `opencli grok ask "..."` | 只有 `ask` 子命令 |
| `opencli grok new` | `opencli grok ask "..." --new true` | grok 的"新对话"是 `ask` 的参数 |
| `opencli gemini query "..."` | `opencli gemini ask "..."` | 没有 `query` 子命令 |

**完整子命令速查**（运行 `opencli grok --help` 或 `opencli gemini --help` 查看）：

```
Grok:
  ask <prompt>                    # 唯一命令

Gemini:
  ask <prompt>                    # 最常用
  new                             # 开新对话
  deep-research <prompt>          # Deep Research 模式
  deep-research-result [query]    # 取 Deep Research 结果
  image <prompt>                  # 图片生成
```

## ⚠️ Critical: Two-layer timeout (from 2026-04-08 debugging)

opencli has **two independent timeout layers**, both must be set for grok to wait long enough:

1. **Inner**: `--timeout 300` — grok.com web response wait time
2. **Outer**: `OPENCLI_BROWSER_COMMAND_TIMEOUT=300` environment variable — entire browser command execution timeout (**default 60s**, hardcoded in `runtime.js:25`)

The outer takes **priority over** the inner. Setting only `--timeout 300` still gets killed at 60s. You MUST set both.

Source code: `.omx/reference/opencli/dist/src/runtime.js:25`:
```js
export const DEFAULT_BROWSER_COMMAND_TIMEOUT = parseEnvTimeout('OPENCLI_BROWSER_COMMAND_TIMEOUT', 60);
```

**Recommended**: add `export OPENCLI_BROWSER_COMMAND_TIMEOUT=300` to `~/.zshrc` so every grok/gemini call has room to breathe.

## Commands

### Grok (MANDATORY env var)

```bash
OPENCLI_BROWSER_COMMAND_TIMEOUT=300 opencli grok ask "{{PROMPT}}" --timeout 300 -f json
```

Or if env var already exported in shell:
```bash
opencli grok ask "{{PROMPT}}" --timeout 300 -f json
```

Flags:
- `--new true` — start a fresh chat (avoids polluting prior conversation context)
- `--web true` — use the hardened grok.com consumer web flow (better error messages)
- `--timeout 300` — MUST match or be lower than `OPENCLI_BROWSER_COMMAND_TIMEOUT`
- `-f json` — structured output (recommended over `--format plain` for parsing)

### Gemini

```bash
opencli gemini ask "{{PROMPT}}" --format plain
```

Gemini is more stable than grok and usually doesn't hit the 60s timeout. No env var required but adding it doesn't hurt:

```bash
OPENCLI_BROWSER_COMMAND_TIMEOUT=300 opencli gemini ask "{{PROMPT}}" --format plain
```

Flags:
- `--new true` — start a fresh chat
- `--timeout 90` — extend timeout for long answers (default 60s)

### Parallel dispatch (for multi-AI workflows)

To call grok and gemini in parallel from Claude Code, use the Bash tool with `run_in_background=true` for both calls in the same assistant turn. Claude Code will launch them concurrently and wait for task-completion notifications.

For deep cross-validation workflows (N internal sub-agents + 2 external AIs, confidence-tiered synthesis), **use the `multi-ai-research` skill** instead — it covers the full orchestration pattern.

## Prerequisites (check before running)

1. **opencli installed**: `opencli --version` should print a version.
2. **Chrome running with Browser Bridge extension loaded** — the extension is installed from `~/Desktop/code/AI/tools/opencli/extension/` via `chrome://extensions` → Developer mode → Load unpacked. If the extension is missing, `opencli doctor` will flag it.
3. **Logged in to the target site**:
   - Grok: `grok.com` must be logged in
   - Gemini: `gemini.google.com` must be logged in
4. **Daemon connectivity**: run `opencli doctor` once per session if unsure.

If any check fails, **do not fall back to another tool silently**. Report the missing prerequisite and ask the user to fix it (per U-23 no-silent-degradation rule).

## Execution protocol

1. Decide which model to use (Grok vs Gemini). If unclear, ask.
2. Build the prompt. Be explicit — these browser UIs have no system prompt so the full question must be self-contained.
3. Run the opencli command with `--format plain`.
4. Capture the response. If the command fails with a session/auth/challenge message, stop and surface the error to the user. Do NOT retry blindly.
5. Save an artifact (see below).
6. Report back to the user: model used, summary of response, and path to the artifact.

## Error handling

opencli will emit specific errors like:
- "Not logged in to grok.com" → ask user to log in
- "Composer not found" → DOM changed, ask user to open the site manually and retry
- "Session gated / challenge" → user needs to solve the challenge in Chrome manually
- Timeout → offer to retry with a longer `--timeout`

Do not swallow these. Report verbatim with the fix action.

## Artifact requirement

After every successful call, save a markdown artifact to:

```
.omx/artifacts/ask-opencli-<grok|gemini>-<slug>-<YYYYMMDD-HHMMSS>.md
```

Minimum sections:
1. **Original user task** — what the user asked you
2. **Model** — grok or gemini, plus any flags used (--new, --web, --timeout)
3. **Final prompt sent** — the exact string passed to `opencli ... ask`
4. **Raw response** — the full output from opencli
5. **Summary** — 2-3 bullets distilling the key points
6. **Action items / next steps** — what to do with this information

Keep the artifact even when the response is low quality — it documents that the query was made.

## Examples

```bash
# Quick factual question, Grok default path
opencli grok ask "最新的 Claude 4.6 定价和 4.5 有什么差别？" --format plain

# Long reasoning task, Gemini with extended timeout + fresh chat
opencli gemini ask "分析这段 Rust 代码的并发安全问题：..." --new true --timeout 120 --format plain

# Grok hardened web path with new chat
opencli grok ask "X 上这两天关于 agent framework 的讨论焦点是什么？" --web true --new true --format plain
```

Task: {{ARGUMENTS}}
