---
name: customise-workflow
description: >-
  Customise the prd-taskmaster-v2 skill workflow via curated brainstorm
  questions. AI asks, user answers in plain English, the skill writes their
  preferences to .taskmaster/config/user-workflow.json. Future runs of
  prd-taskmaster read that file and apply user preferences to phase gates,
  validation strictness, default provider, preferred execution mode, and
  template choice. Use when user says "customise workflow", "adjust my PRD
  settings", "tune the skill", or wants to change how prd-taskmaster behaves.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - AskUserQuestion
---

# customise-workflow

AI-driven workflow customisation for prd-taskmaster-v2. Replaces manual JSON editing.

**Script**: `~/.claude/skills/prd-taskmaster-v2/companion-skills/customise-workflow/script.py` (all commands output JSON)

## When to Use

Activate: "customise workflow", "adjust PRD settings", "tune the skill", "change my defaults", "personalise prd-taskmaster".
Skip: generating a new PRD (use `/prd-taskmaster-v2`), executing tasks (use HANDOFF modes).

## The One Rule

**The AI asks the questions and writes the config. The user never manually edits JSON. The config file is the output, not the input.**

## Flow

```
LOAD → ASK → VALIDATE → WRITE → VERIFY
```

### Phase 1: LOAD current config

Run the script to load existing preferences (or defaults if first run):
```bash
python3 <skill-dir>/script.py load-config
```

Returns JSON with current preferences across 6 categories: provider, validation, execution, template, autonomous, gates.

### Phase 2: ASK curated questions

Read `questions/curated-questions.md` and ask each one via `AskUserQuestion`. The questions are structured so plain-English answers map cleanly to config keys. Example:

```
Q1: Which AI provider do you prefer for task generation?
  Options: Gemini (free, token-efficient), Claude Code (free, Max only),
           OpenAI GPT-4, Anthropic Direct API, OpenRouter, Ollama (local)

Q2: How strict should PRD validation be?
  Options: Strict (block on NEEDS_WORK), Normal (warn but allow GOOD+),
           Lenient (accept ACCEPTABLE+)

...
```

Do NOT ask all questions at once. Ask one at a time, adapt follow-ups based on answers. (Same pattern as `superpowers:brainstorming`.)

### Phase 3: VALIDATE answers

Run the script with each user answer as it arrives. The script validates the answer against allowed values and returns either `ok: true` or a hint about what's wrong.

```bash
python3 <skill-dir>/script.py validate-answer --key provider_main --value gemini-cli
```

### Phase 4: WRITE config

After all questions answered, commit the config:
```bash
python3 <skill-dir>/script.py write-config --input /tmp/answers.json
```

This writes to `.taskmaster/config/user-workflow.json` in the current project. Idempotent — re-running customise-workflow reads and updates the existing file.

### Phase 5: VERIFY

Show the user their final config and confirm it matches their intent:
```bash
python3 <skill-dir>/script.py show-config
```

## Script Commands Reference

| Command | Purpose |
|---|---|
| `load-config` | Load current user-workflow.json (or defaults) |
| `list-questions` | Return the curated question set as JSON |
| `validate-answer --key K --value V` | Validate a single answer |
| `write-config --input <file>` | Write validated answers to user-workflow.json |
| `show-config` | Display current config |
| `reset-config` | Delete user-workflow.json (back to defaults) |

## Config Schema

`user-workflow.json` has 6 top-level keys:

```json
{
  "provider": {
    "main": "gemini-cli|claude-code|anthropic|openai|openrouter|ollama|...",
    "model_main": "gemini-3-pro-preview|sonnet|gpt-4o|...",
    "research": "perplexity|gemini-cli|...",
    "model_research": "sonar-pro|gemini-3-pro-preview|...",
    "fallback": "gemini-cli|claude-code|...",
    "model_fallback": "gemini-3-flash-preview|haiku|..."
  },
  "validation": {
    "strictness": "strict|normal|lenient",
    "ai_review_default": true,
    "min_passing_grade": "EXCELLENT|GOOD|ACCEPTABLE|NEEDS_WORK"
  },
  "execution": {
    "preferred_mode": "A|B|C|D|E|F|G|H|I|J",
    "auto_handoff": true,
    "external_tool": "cursor|codex-cli|gemini-cli|..."
  },
  "template": {
    "default": "comprehensive|minimal",
    "custom_template_path": null
  },
  "autonomous": {
    "allow_self_brainstorm": true,
    "ralph_loop_auto_approve": true
  },
  "gates": {
    "skip_phase_0_if_validated": false,
    "skip_user_approval_in_discovery": false,
    "require_research_expansion": true
  }
}
```

Phase files read this config at runtime and apply user preferences before falling back to documented defaults.

## Critical Rules

1. Never ask the user to edit JSON directly — the skill asks questions and writes the file.
2. Questions are curated and AI-adapted, not a fixed form.
3. Every answer is validated before being written.
4. Config is idempotent — re-running updates cleanly.
5. Config is per-project (lives in `.taskmaster/config/`), not global.
6. Phase files must GRACEFULLY FALL BACK to documented defaults when config keys are missing.
