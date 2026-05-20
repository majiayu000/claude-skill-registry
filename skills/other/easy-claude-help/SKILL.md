---
name: easy-claude-help
version: 1.0.0
description: '[Utilities] Configuration guide for the easy-claude framework — explain settings, guide users through configuring .ck.json.'
---

# easy-claude-help

[Utilities] Configuration guide for the easy-claude framework — explain available settings, guide user/AI through configuring `.claude/.ck.json`.

## When to Use

- User asks "how do I configure Claude?", "how do I disable workflow confirmations?", "how do I turn off hooks?"
- User wants to know what settings are available in easy-claude
- User says "configure workflow mode", "set power user mode", "disable workflow detection"
- AI needs to help user update their `.claude/.ck.json` configuration

## Quick Reference

### Config File Location

```
~/.claude/.ck.json        ← global (applies to all projects)
.claude/.ck.json          ← project (shared, committed to git)
.claude/.ck.local.json    ← personal override (gitignored, per-developer)
```

Each layer overrides the previous via deep merge — you only need to set values you want to override. Use `.ck.local.json` for personal preferences that shouldn't be committed (e.g., your own `codingLevel` or `workflow.confirmationMode`).

---

## Key Settings

### 1. Workflow Confirmation Mode

Controls whether workflow detection requires user confirmation before activating.

**Location:** `.claude/.ck.json` → `workflow.confirmationMode`

| Value      | Behavior                                                                                                                             |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `"always"` | (default) Always asks via AskUserQuestion before activating any workflow. Collaborative mode — best for most users.                  |
| `"never"`  | Auto-executes detected workflow without asking. Use `quick:` prefix behavior globally. Best for power users who trust the detection. |
| `"off"`    | Disables workflow detection entirely. Plain Claude behavior — no catalog injection, no confirmation gate, no overhead.               |

**Example — disable confirmation gate:**

```json
{
    "workflow": {
        "confirmationMode": "never"
    }
}
```

**Example — full opt-out (plain Claude):**

```json
{
    "workflow": {
        "confirmationMode": "off"
    }
}
```

> **Tip:** Even in `"always"` mode, you can prefix any prompt with `quick:` to skip confirmation for that prompt only (e.g., `quick: review the auth code`).

---

### 2. Coding Level

Controls the response style and verbosity level. Affects how Claude explains things.

**Location:** `.claude/.ck.json` → `codingLevel`

| Value | Style                                   |
| ----- | --------------------------------------- |
| `-1`  | (default) Disabled — no style injection |
| `0`   | ELI5 — explain like I'm 5               |
| `1`   | Junior developer                        |
| `2`   | Mid-level developer                     |
| `3`   | Senior developer                        |
| `4`   | Tech lead                               |
| `5`   | Expert/God mode — minimal explanation   |

**Example:**

```json
{
    "codingLevel": 4
}
```

---

### 3. Language Settings

Configure Claude's thinking and response language.

**Location:** `.claude/.ck.json` → `locale`

```json
{
    "locale": {
        "thinkingLanguage": "en",
        "responseLanguage": "fr"
    }
}
```

---

### 4. Assertions

Custom instructions injected into every session as reminders.

**Location:** `.claude/.ck.json` → `assertions`

```json
{
    "assertions": ["Always use TypeScript strict mode", "Prefer functional components over class components"]
}
```

---

### 5. Plan & Naming

Control plan file naming format and date pattern.

**Location:** `.claude/.ck.json` → `plan`

```json
{
    "plan": {
        "namingFormat": "{date}-{issue}-{slug}",
        "dateFormat": "YYMMDD-HHmm",
        "issuePrefix": "GH-"
    }
}
```

---

### 6. Paths

Override where plans and docs are stored.

**Location:** `.claude/.ck.json` → `paths`

```json
{
    "paths": {
        "docs": "docs",
        "plans": "plans"
    }
}
```

---

### 7. Reference Docs Staleness

Controls how old reference docs can be before the staleness gate activates.

**Location:** `.claude/.ck.json` → `referenceDocs.staleDays`

| Value   | Behavior                                                               |
| ------- | ---------------------------------------------------------------------- |
| `60`    | (default) Warn after 60 days, block prompts until scanned or dismissed |
| `1-365` | Custom threshold in days                                               |

**Example — relax to 90 days:**

```json
{
    "referenceDocs": {
        "staleDays": 90
    }
}
```

**How it works:**

1. On session start, checks `<!-- Last scanned: YYYY-MM-DD -->` in each reference doc
2. If any doc is older than `staleDays`, shows a warning listing stale docs
3. On next prompt, blocks until you run `/scan-all`, `/scan-*`, or type `skip scan`
4. `skip scan` dismisses the gate for 24 hours

> **Tip:** Run `/scan-all` to refresh all 10 reference docs at once.

---

## Quick Configuration Examples

### Power User Setup (minimal overhead)

```json
{
    "workflow": {
        "confirmationMode": "never"
    },
    "codingLevel": 5
}
```

### Opt-out Setup (plain Claude)

```json
{
    "workflow": {
        "confirmationMode": "off"
    }
}
```

### Team Setup (collaborative, Vietnamese responses)

```json
{
    "workflow": {
        "confirmationMode": "always"
    },
    "codingLevel": 3,
    "locale": {
        "responseLanguage": "vi"
    }
}
```

---

## How to Apply Config

**Default: always use `.claude/.ck.local.json`** (personal, gitignored) unless the user explicitly says "update project config", "update shared config", or "update .ck.json".

### AI Config Update Protocol

1. **Default → `.claude/.ck.local.json`** (personal override, not committed to git)
    - Read current local config: `Read .claude/.ck.local.json`
    - If file doesn't exist, create it with only the desired settings
    - If file exists, merge the new settings (preserve existing keys)
2. **Only if user explicitly requests** → `.claude/.ck.json` (shared, committed to git)
    - Use when user says "update project config", "share with team", "commit this setting"
3. Confirm to user what was changed and which file was updated

> Config changes take effect on the next prompt (no restart needed).
> `.ck.local.json` overrides `.ck.json` via deep merge — safe for personal preferences without affecting teammates.

---

## Schema Validation

`.ck.json` files are validated on load. Invalid values (wrong types, out-of-range numbers, unknown keys) emit stderr warnings but **never block** — config loading uses graceful degradation.

**What gets checked:**

- `confirmationMode` must be one of `"always"`, `"never"`, `"off"`
- `codingLevel` must be a number between -1 and 5
- `assertions` must be an array of strings
- Unknown top-level keys produce warnings (catches typos like `workfow`)

**CLI validation command:**

```bash
node .claude/hooks/lib/ck-config-schema.cjs .claude/.ck.json
```

---

## Workflow Settings (Advanced)

The workflow catalog itself lives in `.claude/workflows.json`. You can:

- Set `settings.enabled: false` to disable workflow injection entirely
- Change `settings.overridePrefix` (default `"quick:"`) for the per-prompt skip prefix

> **Note:** Prefer `.ck.json → workflow.confirmationMode` over editing `workflows.json` directly, as `.ck.json` supports global+local cascading.
