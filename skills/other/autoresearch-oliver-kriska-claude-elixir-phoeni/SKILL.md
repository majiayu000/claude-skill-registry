---
name: lab:autoresearch
description: >
  Self-improving loop for plugin skills. Reads program.md, proposes one
  mutation per iteration, evaluates against deterministic scorer, keeps
  improvements via git, reverts failures. Targets weakest skill+dimension.
  Use with /loop for overnight runs.
effort: high
argument-hint: "[--skill NAME] [--strategy targeted|sweep|random] [--dry-run] [--max-iterations N]"
disable-model-invocation: true
---

# Autoresearch — Plugin Skill Self-Improvement

Iteratively improve plugin skills via the autoresearch pattern:
propose one mutation -> eval -> keep/revert -> repeat.

## Usage

```
/lab:autoresearch                           # Targeted: attack weakest skill+dimension
/lab:autoresearch --skill review            # Focus on one skill
/lab:autoresearch --strategy sweep          # Process all skills alphabetically
/lab:autoresearch --dry-run                 # Show what would change, don't commit
```

For overnight runs:

```
/loop 5m /lab:autoresearch --strategy sweep --max-iterations 200
```

## Iron Laws

1. **ONE mutation per iteration** — if description needs "and", split into two
2. **NEVER mutate read-only files** — check program.md before every write
3. **EVAL is deterministic** — always use the wrapper script, never LLM-judge
4. **REVERT on regression OR checks failure** — no exceptions
5. **LOG every iteration** — use `keep` or `revert` command (never skip)
6. **CHECK ideas.md before proposing** — don't rediscover known optimizations

## Wrapper Script Commands

All eval/git/journal operations go through ONE script. Do NOT run these manually.

```bash
# Find the weakest skill+dimension
python3 lab/autoresearch/scripts/run-iteration.py target --strategy targeted

# Score a skill (before mutation, to get baseline)
python3 lab/autoresearch/scripts/run-iteration.py score <skill-name>

# After mutation: score + checks + compare → verdict (KEEP or REVERT)
python3 lab/autoresearch/scripts/run-iteration.py eval <skill-name>

# Act on verdict:
python3 lab/autoresearch/scripts/run-iteration.py keep <skill> <dim> <old> <new> \
  --desc "what changed" --asi '{"hypothesis": "why", "mechanism": "how"}'

python3 lab/autoresearch/scripts/run-iteration.py revert <skill> <dim> <old> <new> \
  --desc "what was attempted" --asi '{"hypothesis": "why", "regression": "what broke", "avoid": "do not retry this"}'

# Check overall progress
python3 lab/autoresearch/scripts/run-iteration.py status
```

## Core Loop (ONE iteration)

### Step 1: Read State

1. Read `lab/autoresearch/program.md` (goals, mutable surface, rules)
2. Read `lab/autoresearch/ideas.md` if it exists (deferred optimizations)
3. Run: `python3 lab/autoresearch/scripts/run-iteration.py status`

### Step 2: Select Target

Run: `python3 lab/autoresearch/scripts/run-iteration.py target --strategy targeted`

Parse the JSON: `skill`, `dimension`, `failing_checks`. If `all_perfect` → STOP.

### Step 3: Read + Propose

1. Read target SKILL.md and its references/ listing
2. Read eval definition from `lab/eval/evals/{skill}.json`
3. Check `ideas.md` for deferred ideas about this skill
4. Check recent journal entries for prior failures on this skill (avoid repeats)
5. Consult `${CLAUDE_SKILL_DIR}/references/mutation-strategies.md`
6. Propose exactly ONE change targeting the failing checks

### Step 4: Apply + Evaluate

1. Apply the mutation via Edit tool
2. Run: `python3 lab/autoresearch/scripts/run-iteration.py eval <skill-name>`
3. Parse JSON → check `verdict` field

### Step 5: Keep or Revert

**If verdict is KEEP**:

```bash
python3 lab/autoresearch/scripts/run-iteration.py keep <skill> <dim> <old> <new> \
  --desc "..." --asi '{"hypothesis": "...", "mechanism": "..."}'
```

**If verdict is REVERT**:

```bash
python3 lab/autoresearch/scripts/run-iteration.py revert <skill> <dim> <old> <new> \
  --desc "..." --asi '{"hypothesis": "...", "regression": "...", "avoid": "..."}'
```

### Step 6: Ideas Backlog

If during analysis you discovered a promising optimization you can't act on now:

- Append it to `lab/autoresearch/ideas.md` as a bullet
- On next resume: prune stale/tried ideas, experiment with the rest

### Step 7: Continue or Stop

- All targets >= 0.95? Print "AUTORESEARCH_COMPLETE"
- Max iterations reached? Print "AUTORESEARCH_COMPLETE"
- 50 consecutive discards? Print "AUTORESEARCH_STUCK"
- Otherwise: immediately start Step 1 again

## References

- `${CLAUDE_SKILL_DIR}/references/mutation-strategies.md` — mutation type catalog
- `${CLAUDE_SKILL_DIR}/references/state-management.md` — git protocol, journaling
- `lab/autoresearch/program.md` — research agenda (read every iteration)
