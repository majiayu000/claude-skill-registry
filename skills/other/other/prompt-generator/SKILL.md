---
name: prompt-generator
description: "Generate optimized Claude Code prompts for any request. This is the main entry point for the prompt generation system. Use this skill whenever you need to create a prompt for a Claude Code session, generate a session prompt pack, prepare a multi-session plan, or translate a natural language request into a structured, actionable Claude Code prompt. Trigger on: 'generate a prompt for', 'create a prompt', 'help me write a prompt', 'what prompt should I use', '/generate-prompt', any use of the generate-prompt slash command, or when you want to ensure a Claude Code session starts with the right skills, context, glossary, and verification checklist loaded. Also trigger when someone wants to create session prompts similar to the S4-S9 pipeline prompt packs."
---

# Prompt Generator

The capstone skill that orchestrates the full prompt generation pipeline: discovery → classification → routing → generation. Produces ready-to-use Claude Code session prompts with glossary, verification checklist, and optional plan scaffolding.

---

## Phase 1 — Discover

Check if the skills registry is current:

```bash
REGISTRY="D:/ailocal/acm-ai/skills-registry.json"

# Check existence and age (regenerate if missing or >1 hour old)
if [ ! -f "$REGISTRY" ]; then
  echo "Registry missing — running skill-discovery"
  RUN_DISCOVERY=true
else
  # Check modification time (cross-platform: stat -c on Linux, stat -f on macOS)
  MTIME=$(stat -c "%Y" "$REGISTRY" 2>/dev/null || stat -f "%m" "$REGISTRY" 2>/dev/null)
  NOW=$(date +%s)
  AGE=$((NOW - MTIME))
  if [ $AGE -gt 3600 ]; then
    echo "Registry stale ($((AGE / 60)) min old) — running skill-discovery"
    RUN_DISCOVERY=true
  fi
fi
```

If `RUN_DISCOVERY=true`, invoke `/skill-discovery` to refresh the registry before proceeding.

Read `D:/ailocal/acm-ai/skills-registry.json` after confirming it is current.

---

## Phase 2 — Classify

Apply `/request-classifier` to the user's request. Produce a `RequestClassification` JSON.

If the classification is **ambiguous** (two types score within 1 point of each other, or the request contains mixed signals), present the candidate classifications to the user and ask for confirmation before proceeding:

```
I see two plausible classifications for your request:
  A) pipeline / complexity 6 / plan ON
  B) improvement / complexity 5 / plan ON

The strategies diverge here — A routes to a tmux team, B routes to a solo agent with subagent gates.
Which fits better, or shall I go with A (pipeline) since there are LangGraph signals?
```

---

## Phase 3 — Route

Apply `/prompt-router` with the confirmed classification + skills registry.

Produce a `PromptPlan` JSON. If the plan is **complex** (agent_strategy=tmux-team OR plan_mode=true with 5+ skills), present it for user confirmation before generating:

```
Routing plan:
  Type: pipeline / complexity 7 / plan mode ON
  Skills: /planning-with-files, /langgraph-fundamentals, /acm-observability, /pydantic-models-py
  Strategy: tmux-team (3 panes: orchestrator, backend-dev, verifier)
  Context7: LangGraph docs + LangChain docs
  Output: prompt-pack → docs/sprint-artifacts/prompt-packs/

Proceed? [Y/n]
```

---

## Phase 4 — Generate

### 4a — Load Template

Read the master template from:
```
D:/ailocal/acm-ai/.claude/skills/prompt-generator/references/prompt-template.md
```

### 4b — Build Glossary

Read the glossary builder:
```
D:/ailocal/acm-ai/.claude/skills/prompt-generator/references/glossary-builder.md
```

Select the domain(s) based on `domain_signals` from the classification:
- `extraction`, `pipeline`, `graph`, `node`, `langgraph` → **Pipeline domain**
- `component`, `page`, `UI`, `React`, `css`, `frontend` → **Frontend domain**
- Always include → **General domain**

Cap at 15 entries. Prioritize terms that appear in the user's original request text.

### 4c — Populate Template

Fill in all `{{ variable }}` placeholders:

| Placeholder | Source |
|---|---|
| `{{ session_title }}` | One-sentence goal from user's request |
| `{{ skill_directives }}` | `/skill-name` lines from `PromptPlan.selected_skills` |
| `{{ prerequisites }}` | Services/files that must exist before the session starts |
| `{{ glossary_table }}` | Built in step 4b |
| `{{ current_state }}` | Key state facts relevant to the request (branch, last sprint, etc.) |
| `{{ key_files_list }}` | Exact absolute paths for files the session will touch |
| `{{ plan_or_steps }}` | If plan_mode: scaffold plan format; else: "What to Change" section |
| `{{ strategy_config }}` | Agent strategy block from `PromptPlan.agent_config` |
| `{{ context7_section }}` | Context7 directives from `PromptPlan.context7_directives` (omit if empty) |
| `{{ verification_items }}` | Checklist items from `PromptPlan.verification_items` |
| `{{ files_summary }}` | NEW / MODIFY / MOVE counts from key files list |
| `{{ commit_message }}` | Conventional commit template (`feat:` / `fix:` / `refactor:`) |

### 4d — Plan Mode Scaffolding

If `plan_mode=true`, also create these files in `docs/sprint-artifacts/`:

**task_plan.md** skeleton:
```markdown
# Task Plan: {session_title}
Date: {YYYY-MM-DD}
Status: IN PROGRESS

## Goal
{one-sentence goal}

## Steps
- [ ] Step 1
- [ ] Step 2
...

## Risks
- (none identified yet)
```

**findings.md** skeleton:
```markdown
# Findings: {session_title}
Date: {YYYY-MM-DD}

## What Was Discovered
(populate during session)

## Decisions Made
(populate during session)
```

**progress.md** skeleton:
```markdown
# Progress: {session_title}
Date: {YYYY-MM-DD}

## Completed
(none yet)

## In Progress
(none yet)

## Blocked
(none yet)
```

---

## Phase 5 — Output

Select output format from `PromptPlan.output_format`:

### terminal (default)
Print directly with clear markers:
```
══════════════════════════════════════════
  GENERATED PROMPT — {session_title}
══════════════════════════════════════════
{populated template content}
══════════════════════════════════════════
```

### copy-paste
Print in a fenced code block so the user can copy it cleanly:
````
```prompt
{populated template content}
```
````

### prompt-pack
Save to `docs/sprint-artifacts/prompt-packs/{YYYY-MM-DD}-{slug}.md` where `{slug}` is the session title kebab-cased.

Print a confirmation:
```
Prompt pack saved to:
  docs/sprint-artifacts/prompt-packs/2026-03-13-fix-extraction-timeout.md
```

### --save flag override
If the user passed `--save`, always save to the prompt-pack path regardless of `output_format`, AND print to terminal.

---

## Quick Start

Three example invocations:

**1. Simple fix (terminal output, no plan):**
```
/generate-prompt "Fix the building sidebar not loading when source has 0 buildings"
```
→ Classifies as bug-fix/simple, routes to solo+systematic-debugging, outputs inline.

**2. Complex feature (saved prompt-pack + plan scaffolding):**
```
/generate-prompt "Add MinerU as a new extraction provider with fallback chain" --save --tmux
```
→ Classifies as pipeline/complex, routes to tmux-team+langgraph-fundamentals, saves to prompt-packs/, creates task_plan.md.

**3. Refactor with explicit format:**
```
/generate-prompt "Refactor pre-extraction stages to reduce LLM calls" --format prompt-pack
```
→ Classifies as improvement/medium, routes to solo+verification-before-completion, saves as prompt-pack.

---

## Flags Reference

| Flag | Effect |
|---|---|
| `--save` | Always save to prompt-packs/, also print to terminal |
| `--no-plan` | Force `plan_mode=false`, skip plan scaffolding |
| `--with-plan` | Force `plan_mode=true`, always scaffold task_plan.md |
| `--tmux` | Force `agent_strategy=tmux-team` regardless of classification |
| `--format terminal` | Print with markers (default) |
| `--format copy-paste` | Print in fenced code block |
| `--format prompt-pack` | Save to file only |

---

## Notes

- If `skills-registry.json` is missing, Phase 1 runs `/skill-discovery` automatically — this adds ~5 seconds but ensures accurate skill selection
- Plan scaffolding files are created relative to the repo root; the session prompt references them with absolute paths
- Context7 directives in the generated prompt are ready-to-execute — copy them verbatim at session start
- The generated prompt is designed to be pasted as the first message of a new Claude Code session, not run in the current conversation
