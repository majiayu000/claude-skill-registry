---
name: opencode-copilot-opus
description: Use this skill when you need Codex to collaborate with GitHub Copilot Opus (via opencode), especially for architecture review, second-opinion validation, and iterative discussion that must continue in the same opencode session_id. Covers model selection for github-copilot/claude-opus-4.6, stable sandbox-safe invocation, session continuity with -c / -s, and troubleshooting common opencode errors.
---

# Opencode Copilot Opus

Use this skill to make Codex and Copilot Opus discuss the same topic in multiple rounds while preserving context in one opencode session.

## Run Workflow

1. Run environment precheck.
2. Start a new Opus review session.
3. Continue in the same session with `-c` or explicit `-s <session_id>`.
4. Bring Opus findings back to Codex and iterate.

Use the helper script:

```bash
~/.hermes/skills/autonomous-ai-agents/opencode-copilot-opus/scripts/opus_bridge.sh auth
~/.hermes/skills/autonomous-ai-agents/opencode-copilot-opus/scripts/opus_bridge.sh models
~/.hermes/skills/autonomous-ai-agents/opencode-copilot-opus/scripts/opus_bridge.sh new "请评审这个方案并给出风险清单"
~/.hermes/skills/autonomous-ai-agents/opencode-copilot-opus/scripts/opus_bridge.sh continue "补充背景：仅全范围检索"
~/.hermes/skills/autonomous-ai-agents/opencode-copilot-opus/scripts/opus_bridge.sh list-sessions
~/.hermes/skills/autonomous-ai-agents/opencode-copilot-opus/scripts/opus_bridge.sh run-session ses_xxx "继续上次结论，给8周计划"
```

## Session Continuity Rules

1. Use `new` for first prompt in a topic.
2. Use `continue` when the last opencode session is the one to extend.
3. Use `run-session <session_id>` when continuity must be deterministic.
4. Record the returned `session_id` in notes/logs for reproducibility.

## Prompt Pattern

Use a structured prompt to reduce drift:

```text
背景:
- 现状...
- 约束...

目标:
- 本轮需要确认的问题...

请输出:
1) 风险清单（按严重度）
2) 控制措施
3) 是否建议推进与边界条件
```

## Troubleshooting

Read `references/troubleshooting.md` when any opencode command fails.

Key fast fixes:

1. Cache permission error: set `XDG_CACHE_HOME=/tmp`.
2. Local config schema error: if `~/.config/opencode/opencode.json` has unsupported keys (e.g. `skills`), create a clean config copy and point `XDG_CONFIG_HOME` to it.
3. Wrong provider/model: use `github-copilot/claude-opus-4.6`.
4. GitHub Copilot `ECONNRESET` / `api.githubcopilot.com` network failures: run with
   `HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897`.
5. If safe mode (`OPENCODE_SAFE_MODE=1`, `XDG_CONFIG_HOME=/tmp`) triggers `Cannot find module ... opencode-*-auth`, rerun with `OPENCODE_SAFE_MODE=0` and a clean explicit `XDG_CONFIG_HOME`.

## Safety Notes

1. Keep opencode discussion read-only by default (no destructive shell operations).
2. Always require explicit confirmation before destructive git/system actions.
3. When Opus conclusions conflict with code reality, validate against local code before adopting.
