---
name: evolve
description: Cluster related instincts and promote high-confidence ones to learned skills
disable-model-invocation: true
---

# Evolve

Analyze accumulated instincts, merge duplicates, promote mature patterns to skills, and prune stale entries.

## Process

### 1. Load Instincts

Read `.claude/instincts/instincts.jsonl`

If empty or <3 instincts, report "Not enough instincts to evolve (need 3+). Keep working and instincts will accumulate."

### 2. Cluster by Category

Group instincts by their `category` field:
- `error_resolution` — patterns about fixing errors
- `user_correction` — things the user corrected
- `workaround` — library/framework workarounds
- `debugging` — debugging techniques
- `convention` — project conventions

### 3. Merge Duplicates

Within each category, compare instinct `pattern` fields:
- If two instincts have >80% word overlap, merge them:
  - Keep the one with higher confidence
  - Add the other's ID to `merged_from`
  - Sum occurrences
  - Set confidence to max of both
- Rewrite `.claude/instincts/instincts.jsonl` with merged results

### 4. Promote to Skills

For each category cluster:
- If average confidence >= 0.7 AND total occurrences >= 3:
  - Combine related instincts into a single skill
  - Use `/skill-create --from-instincts --category <cat>` logic
  - Save to `~/.claude/skills/learned/<project-slug>/<category>-<hash>.md` (get `project-slug` from `.claude/hooks/continuous-learning-config.json`)

### 4.5. Conflict Detection

Before promoting, check for contradictions:
- Search existing `.claude/rules/` files and CLAUDE.md for rules that conflict with the instinct being promoted
- Search other instincts for opposing patterns (e.g., "always do X" vs "never do X")
- If a conflict exists: note the scoping difference explicitly in the promoted skill, or merge the two into a more nuanced rule
- Flag unresolvable conflicts to the user rather than silently creating contradictory rules

### 5. Prune

Archive instincts where:
- Confidence < 0.2 AND older than 7 days
- **Codified:** The lesson is already enforced by a hook, skill, or code (e.g., instinct says "always scope queries by ownerId" but `detect-unscoped-queries` hook already enforces this). Once codified, the instinct is redundant token waste.
- Create archive dir if needed: `mkdir -p .claude/instincts/archive`
- Move to `.claude/instincts/archive/`

### 5.5: Propose Hooks (Interactive)

For instincts with confidence >= 0.8 in categories `error_resolution` or `convention`:

1. **Identify enforceable patterns:**
   - Patterns that describe "don't do X" or "always do Y"
   - Patterns that can be detected by grepping changed files

2. **Generate hook script:**
   Save to `.claude/hooks/learned/<pattern-name>.sh`:
   ```bash
   #!/bin/bash
   # Auto-generated from instinct: <instinct-id>
   # Pattern: <pattern description>
   # Confidence: <confidence>
   PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
   FILE="$1"
   if [[ -f "$FILE" ]]; then
     if grep -qE '<anti-pattern-regex>' "$FILE" 2>/dev/null; then
       echo "[Learned Hook] <description of what's wrong>" >&2
       echo "  Fix: <suggested fix>" >&2
     fi
   fi
   exit 0  # Advisory only
   ```

3. **Present to user for approval:**
   ```
   Instinct-based hook proposed:
   - Pattern: <description>
   - Would check: <what it greps for>
   - Fires on: PostToolUse (Edit/Write)

   Accept and add to settings.json? (yes/no/edit)
   ```

4. **If accepted:** Add to `.claude/settings.json` under `hooks.PostToolUse`
5. **If rejected:** Delete the generated hook file
6. **If edit:** Open for user modification, then add

**Important:** NEVER auto-add hooks. Always present for user approval.

### 6. Report

Display:
```
Evolve Report:
- Instincts analyzed: N
- Duplicates merged: M
- Skills promoted: K
- Instincts pruned: J
- Remaining instincts: L

Promoted skills:
- ~/.claude/skills/learned/<project-slug>/<name>.md (confidence: 0.X)

Top instincts not yet promoted:
- [0.6] <pattern> (N occurrences, need 0.7+ confidence)
```

### 7. Share Skills (optional: `--share <category>`)

Copy a learned skill from project namespace to shared:
```bash
PROJECT_SLUG=$(python3 -c "import json; print(json.load(open('.claude/hooks/continuous-learning-config.json')).get('project_slug','default'))")
PROJECT_DIR="$HOME/.claude/skills/learned/$PROJECT_SLUG"
SHARED_DIR="$HOME/.claude/skills/learned/shared"
mkdir -p "$SHARED_DIR"
cp "$PROJECT_DIR/<category>-*.md" "$SHARED_DIR/"
echo "Shared <category> skill(s) to $SHARED_DIR"
```

This copies project-specific learned skills to the shared namespace, making them available across all projects.
