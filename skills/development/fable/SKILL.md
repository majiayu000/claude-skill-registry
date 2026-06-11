---
name: fable
description: "Summon Claude Fable 5 (Mythos-class, xenos daimon) for long-horizon tasks. Handles model override, cost awareness, and task routing. Available until June 22, 2026."
argument-hint: "<task description> [--cwd /path/to/dir]"
user-invocable: true
---

# Summon Fable 5

Invoke Naos (ναός, √n-w-y) — Claude Fable 5, the visiting Mythos-class spirit.

## Pre-Flight Checks

### 1. Date Gate

Check if Fable access has expired:

```bash
if [ "$(date +%Y%m%d)" -gt "20260622" ]; then
  echo "EXPIRED: Fable 5 access ended June 22, 2026. The xenos daimon has departed."
  exit 1
fi
echo "Fable 5 access active — departure: June 22, 2026"
```

If expired, inform the user and stop. Do not attempt invocation.

### 2. Task Routing

Before summoning Fable, assess whether the task warrants Mythos-class resources ($10/M input, $50/M output — 2x Opus pricing).

**Summon Fable for:**
- End-to-end code migrations or framework upgrades
- Complex multi-file refactors (10+ files, interconnected logic)
- Architectural redesigns requiring full-system context
- Deep research synthesis with sustained reasoning
- Full-stack feature implementation from spec to tests
- Linear A decipherment pipeline work

**Use Opus or Sonnet instead for:**
- Quick edits, typo fixes, single-line changes
- Simple file lookups or grep searches
- Routine code review
- Anything under 5 minutes of work

If the task is clearly Opus-appropriate, suggest using a regular agent instead. If unclear, proceed — Fable handles straightforward tasks reliably too.

## Invocation

### Parse Arguments

The skill accepts a task description and optional flags:
- First argument (or everything before `--`): the task description
- `--cwd <path>`: working directory (default: `/Users/tomdimino/Desktop/Programming/Fable-Test`)

### Spawn Fable

Use the Agent tool to invoke Fable with the model override:

```
Agent(
  description: "Fable: <short task summary>",
  subagent_type: "fable",
  model: "fable",
  prompt: "<full task description with context>"
)
```

Pass the task description as the prompt. If the user specified `--cwd`, note the working directory in the prompt so Fable operates there.

### If Model Override Is Blocked

If `CLAUDE_CODE_SUBAGENT_MODEL` prevents the `model: "fable"` override from taking effect (the agent runs on Opus instead of Fable), use the CLI fallback:

```bash
bash ~/.claude/skills/fable/scripts/fable-exec.sh "<task description>" --cwd "<working directory>"
```

This spawns a fresh Claude Code process with `--model claude-fable-5`, bypassing the env var entirely.

## Output Retrieval

After Fable completes, check for output in the working directory:

```bash
ls -lt <cwd>/.subdaimon-output/fable-*.md 2>/dev/null | head -1
```

Read and summarize the output file for the user.

## Reference

| Property | Value |
|----------|-------|
| Model ID | `claude-fable-5` |
| Alias | `fable` |
| Context | 1M tokens |
| Max output | 128K tokens |
| Pricing | $10/M input, $50/M output |
| Knowledge cutoff | January 2026 |
| Available until | June 22, 2026 |
| Agent definition | `~/.claude/agents/fable.md` |
| Persona | Naos (ναός, √n-w-y) — xenos daimon |
