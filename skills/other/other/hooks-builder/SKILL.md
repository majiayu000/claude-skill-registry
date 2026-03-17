---
name: hooks-builder
type: standard
depth: extended
description: >-
  Creates Claude Code hooks executing shell commands, prompt evaluations, or multi-turn agents at 15 lifecycle events. Use when building PreToolUse validation, PostToolUse formatting, PermissionRequest auto-approval, Stop/SubagentStop evaluation, TeammateIdle prevention, TaskCompleted gating, Setup provisioning, SessionStart context injection, or deterministic agent control via blocking/non-blocking hooks.
---

# [H1][HOOKS-BUILDER]
>**Dictum:** *Deterministic behavior requires hooks; prompts fail execution guarantees.*

<br>

Build Claude Code hooks—shell commands, prompt evaluations, or multi-turn agents execute at 15 agent lifecycle events.

**Tasks:**
1. Read [index.md](./index.md) — Reference file listing for navigation
2. Read [lifecycle.md](./references/lifecycle.md) — 14 events, input schemas, exit codes, blocking behavior
3. Read [schema.md](./references/schema.md) — Configuration structure, matchers, JSON responses, hook types
4. (integration) Read [integration.md](./references/integration.md) — Environment variables, context injection
5. (scripting) Read [scripting.md](./references/scripting.md) — Python standards, security patterns
6. (recipes) Read [recipes.md](./references/recipes.md) — Proven implementation patterns
7. (troubleshooting) Read [troubleshooting.md](./references/troubleshooting.md) — Known issues, platform workarounds
8. (prose) Load `style-standards` skill — Voice, formatting, constraints
9. Validate — Quality gate; see §VALIDATION

**Scope:**
- *Event Selection:* Choose hook type by automation goal (blocking vs observing).
- *Configuration:* Author settings.json entries with matchers and timeouts.
- *Response Handling:* Control agent via exit codes, JSON responses, or prompt evaluation.

[REFERENCE]: [index.md](./index.md) — Complete reference file listing

---
## [1][EVENT_SELECTION]
>**Dictum:** *Automation goal determines hook type; blocking capability varies by event.*

<br>

**Decision Gate:**<br>
- *Intercept before execution?* → PreToolUse (validate/block/modify parameters)
- *Control permission dialogs?* → PermissionRequest (auto-approve/deny)
- *React after completion?* → PostToolUse (format, lint, add context)
- *React after failure?* → PostToolUseFailure (error handling, retry logic)
- *Inject at session boundaries?* → SessionStart (context), UserPromptSubmit (per-message)
- *One-time provisioning?* → Setup (tool installation, dependency setup via `claude --init`)
- *Evaluate task completion?* → Stop/SubagentStop (prompt/agent type for LLM judgment)
- *Coordinate teams?* → TeammateIdle (prevent idle), TaskCompleted (validate completion)
- *Observe subagent lifecycle?* → SubagentStart/SubagentStop (logging)

**Blocking Events (exit 2 blocks action):**

| [INDEX] | [EVENT]           | [EXIT_2_EFFECT]                                       |
| :-----: | ----------------- | ----------------------------------------------------- |
|   [1]   | PreToolUse        | Blocks tool call; stderr shown to Claude              |
|   [2]   | PermissionRequest | Denies the permission                                 |
|   [3]   | UserPromptSubmit  | Blocks prompt processing; erases prompt from context  |
|   [4]   | Stop              | Prevents Claude from stopping; continues conversation |
|   [5]   | SubagentStop      | Prevents subagent from stopping                       |
|   [6]   | TeammateIdle      | Prevents teammate from going idle; stderr = feedback  |
|   [7]   | TaskCompleted     | Prevents task completion; stderr = feedback to model  |

**Non-blocking Events (exit 2 shows stderr only):**

| [INDEX] | [EVENT]            | [EXIT_2_EFFECT]                              |
| :-----: | ------------------ | -------------------------------------------- |
|   [1]   | PostToolUse        | Shows stderr to Claude (tool already ran)    |
|   [2]   | PostToolUseFailure | Shows stderr to Claude (tool already failed) |
|   [3]   | SessionStart       | Shows stderr to user only                    |
|   [4]   | Setup              | Shows stderr to user only                    |
|   [6]   | SessionEnd         | Shows stderr to user only                    |
|   [7]   | Notification       | Shows stderr to user only                    |
|   [8]   | SubagentStart      | Shows stderr to user only                    |
|   [9]   | PreCompact         | Shows stderr to user only                    |

---
## [2][CONFIGURATION]
>**Dictum:** *Centralized configuration enables scope-aware hook precedence.*

<br>

| [INDEX] | [SCOPE] | [PATH]                        | [USE]                | [GIT]  |
| :-----: | ------- | ----------------------------- | -------------------- | :----: |
|   [1]   | User    | `~/.claude/settings.json`     | Global, all projects |  N/A   |
|   [2]   | Project | `.claude/settings.json`       | Shared, committed    | Commit |
|   [3]   | Local   | `.claude/settings.local.json` | Personal, testing    | Ignore |

**Precedence:** Local > Project > User. Same-event hooks from all scopes run in parallel.

**Snapshot:** Hooks captured at startup; mid-session edits require `/hooks` review to reload.

---
## [3][IMPLEMENTATION]
>**Dictum:** *Deterministic and evaluative patterns require distinct execution modes.*

<br>

| [INDEX] | [TYPE]  | [USE_CASE]                       | [TIMEOUT] | [CHARACTERISTICS]            |
| :-----: | ------- | -------------------------------- | :-------: | ---------------------------- |
|   [1]   | command | Validation, formatting, rules    |   600s    | Deterministic, shell scripts |
|   [2]   | prompt  | Complex evaluation, LLM judgment |    30s    | Single-turn, context-aware   |
|   [3]   | agent   | Tool-using evaluation            |    60s    | Multi-turn, up to 50 turns   |

**Prompt/Agent Eligible Events:** PreToolUse, PostToolUse, PostToolUseFailure, PermissionRequest, UserPromptSubmit, Stop, SubagentStop, TaskCompleted.

[CRITICAL] TeammateIdle does NOT support prompt or agent hooks — exit codes only.

**Prompt/Agent Response Schema:**
```json
{"ok": true}
{"ok": false, "reason": "Explanation shown to Claude"}
```

`ok: true` allows the action. `ok: false` blocks it with the provided reason.

**Command Hook Fields:**

| [INDEX] | [FIELD]         | [TYPE]  |   [DEFAULT]   | [EFFECT]                                  |
| :-----: | --------------- | ------- | :-----------: | ----------------------------------------- |
|   [1]   | `type`          | string  |       —       | `"command"`, `"prompt"`, or `"agent"`     |
|   [2]   | `command`       | string  |       —       | Shell command or script path              |
|   [3]   | `timeout`       | number  | type-specific | Seconds: command=600, prompt=30, agent=60 |
|   [4]   | `async`         | boolean |    `false`    | Background execution; non-blocking        |
|   [5]   | `statusMessage` | string  |       —       | Custom spinner text during execution      |
|   [6]   | `once`          | boolean |    `false`    | Run once per session (skills only)        |

**Prompt/Agent Hook Fields:**

| [INDEX] | [FIELD]  | [TYPE] | [DEFAULT]  | [EFFECT]                                       |
| :-----: | -------- | ------ | :--------: | ---------------------------------------------- |
|   [1]   | `prompt` | string |     —      | Instructions for LLM; `$ARGUMENTS` = hook JSON |
|   [2]   | `model`  | string | fast model | Model to use for evaluation                    |

---
## [4][SCRIPTING]
>**Dictum:** *Hook reliability requires functional pipeline patterns.*

<br>

Python 3.14+ with strict typing. Zero imperative patterns.

---
## [5][VALIDATION]
>**Dictum:** *Gates prevent incomplete artifacts.*

<br>

[VERIFY] Completion:
- [ ] Event: Selected correct hook type for automation goal.
- [ ] Blocking: Verified event supports blocking (7 events) or observing (8 events).
- [ ] Schema: Configuration structure validated per schema.md.
- [ ] Timeout: Correct units (seconds): command=600, prompt=30, agent=60.
- [ ] Integration: Environment variables and context injection applied.
- [ ] Scripting: Security patterns and tooling gates passed.
- [ ] Quality: JSON syntax valid, timeouts appropriate.

[REFERENCE] Operational checklist: [->validation.md](./references/validation.md)
