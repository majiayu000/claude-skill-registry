---
name: customise-workflow
description: >-
  Customise the prd-taskmaster plugin workflow via curated brainstorm
  questions. The AI asks, the user answers in plain English, and the skill
  writes their preferences to .atlas-ai/config/atlas.json. Future runs of
  prd-taskmaster read that file and apply user preferences to phase gates,
  validation strictness, default provider, preferred execution mode, and
  template choice. For deeper tweaks beyond the curated questions, users can
  hand-edit files in .atlas-ai/customizations/. Use when the user says
  "customise workflow", "customize workflow", "adjust my PRD settings",
  "tune the skill", or wants to change how prd-taskmaster behaves.
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - AskUserQuestion
  - ToolSearch
  - mcp__atlas-engine
  - mcp__plugin_prd_go
  - mcp__plugin_prd-taskmaster_go
  - mcp__plugin_atlas-go_go
---

# customise-workflow

AI-driven workflow customisation for the `prd-taskmaster` plugin.
Replaces manual JSON editing. Part of the plugin's companion-skills family.

**Script**: `skills/customise-workflow/script.py` (all commands output JSON)
**Plugin config root**: `.atlas-ai/` (per-project, lives alongside TaskMaster's
`.taskmaster/`)

## When to Use

Activate when the user says: "customise workflow", "customize workflow",
"adjust PRD settings", "tune the skill", "change my defaults", or
"personalise prd-taskmaster".

Skip: generating a new PRD (use `/prd:go`), executing tasks (use
HANDOFF modes), or running research expansion (use `/expand-tasks`).

## The One Rule

**The AI asks the questions and writes the config. The user never manually
edits JSON. The config file is the output, not the input.** If the user wants
tweaks beyond the curated questions, point them at `.atlas-ai/customizations/`
(see "Customizations directory" below) — do not hand them raw JSON.

## Flow

```
LOAD → ASK → VALIDATE → WRITE → VERIFY
```

### Phase 1: LOAD current config

Run the script to load existing preferences (or defaults if first run):

```bash
python3 skills/customise-workflow/script.py load-config
```

Returns JSON with current preferences across 6 categories: provider,
validation, execution, template, autonomous, gates. Writes to
`.atlas-ai/config/atlas.json` if missing, seeding defaults.

### Phase 2: ASK curated questions

Read `questions/curated-questions.md` and ask each one via `AskUserQuestion`.
The questions are curated so plain-English answers map cleanly to config keys.
Example:

```
Q1: Which AI provider do you prefer for task generation?
  Options: Gemini (free, token-efficient), Claude Code (free, Max only),
           OpenAI GPT-4, Anthropic Direct API, OpenRouter, Ollama (local)

Q2: How strict should PRD validation be?
  Options: Strict (block on NEEDS_WORK), Normal (warn but allow GOOD+),
           Lenient (accept ACCEPTABLE+)

Q3: Which execution mode should prd-taskmaster default to?
  Options: A (Plan Mode), B (Ralph loop), C (Atlas Fleet), ...

...
```

Do NOT ask all questions at once. Ask one curated question at a time and
adapt follow-ups based on answers. (Same pattern as
`superpowers:brainstorming`.)

### Phase 3: VALIDATE answers

Run the script with each user answer as it arrives. The script validates the
answer against allowed values and returns either `ok: true` or a hint about
what's wrong.

```bash
python3 skills/customise-workflow/script.py validate-answer \
  --key provider_main --value gemini-cli
```

If validation fails, re-ask the question with the hint. Never write an invalid
value.

### Phase 4: WRITE config

After all curated questions are answered, commit the config:

```bash
python3 skills/customise-workflow/script.py write-config --input /tmp/answers.json
```

This writes to `.atlas-ai/config/atlas.json` in the current project.
Idempotent — re-running customise-workflow reads and updates the existing
file. The script creates the `.atlas-ai/config/` directory if missing.

### Phase 5: VERIFY

Show the user their final config and confirm it matches their intent:

```bash
python3 skills/customise-workflow/script.py show-config
```

If the user says "that's not what I meant" for any key, re-enter Phase 2 for
just that key, re-validate, and re-write.

## Script Commands Reference

| Command | Purpose |
|---|---|
| `load-config` | Load current `.atlas-ai/config/atlas.json` (or defaults) |
| `list-questions` | Return the curated question set as JSON |
| `validate-answer --key K --value V` | Validate a single answer |
| `write-config --input <file>` | Write validated answers to `.atlas-ai/config/atlas.json` |
| `show-config` | Display current config |
| `reset-config` | Delete `.atlas-ai/config/atlas.json` (back to defaults) |

## Config Schema

`.atlas-ai/config/atlas.json` has 6 top-level keys:

```json
{
  "provider": {
    "main": "gemini-cli|claude-code|anthropic|openai|openrouter|ollama|...",
    "model_main": "gemini-3-pro-preview|sonnet|gpt-4o|...",
    "research": "gemini-cli|perplexity|...",
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

Phase files (`skills/setup`, `skills/discover`, `skills/generate`,
`skills/handoff`, `skills/execute-task`) read this config at runtime and apply
user preferences before falling back to documented defaults.

## Customizations directory

For tweaks that go beyond the curated questions — custom template overrides,
provider-model mapping tables, gate hooks, per-phase overrides — users can
drop files into `.atlas-ai/customizations/`. This is the escape hatch for
power users. The curated questions cover the 80% case; the customization
directory covers everything else.

Expected layout:

```
.atlas-ai/
  config/
    atlas.json              # written by this skill
  customizations/           # user-editable, never overwritten by this skill
    templates/              # custom PRD templates
    prompts/                # provider prompt overrides
    gates/                  # custom gate predicates
    README.md               # user-authored notes
```

Rules:

1. This skill NEVER writes into `.atlas-ai/customizations/` — that's user
   territory.
2. Phase skills read `.atlas-ai/customizations/` as a fallback *after* the
   curated `atlas.json` but *before* documented defaults.
3. When a user asks for a setting not covered by curated questions, the AI
   proposes a customization file shape, the user edits, and the AI verifies
   the file parses.

## Critical Rules

1. Never ask the user to edit JSON directly — the skill asks curated questions
   and writes the file.
2. Questions are curated and AI-adapted, not a fixed form — adapt follow-ups
   to earlier answers.
3. Every answer is validated before being written (`validate-answer`).
4. Config is idempotent — re-running updates cleanly.
5. Config is per-project (lives in `.atlas-ai/config/`), not global.
6. Customization files live in `.atlas-ai/customizations/` and are
   user-authored — this skill never overwrites them.
7. Phase skills must GRACEFULLY FALL BACK to documented defaults when config
   keys are missing.
