---
name: crystallize
description: "Distils repeating patterns from session logs and lessons.md into draft skill files. Run after ≥10 sessions to extract durable knowledge. Output: draft skills/ files + promotion report."
when_to_use: |
  Apply when:
  - CTO says /crystallize, "crystallize", or "extract knowledge"
  - Session count in .great_cto/logs/ reaches a multiple of 10 (auto-suggest)
  - User asks "what have we learned?" or "turn lessons into skills"
effort: high
allowed-tools: Read, Write, Glob, Grep, Bash, Agent
paths:
  - ".great_cto/logs/**"
  - ".great_cto/lessons.md"
  - "~/.great_cto/decisions.md"
  - "skills/**"
---

# Crystallize — distil session patterns into reusable skills

Invoke when the CTO says `/crystallize`, "crystallize", "extract knowledge", or
"what have we learned?". Also auto-suggested when session count is a multiple
of 10 (the session-end hook checks `.great_cto/.last-crystallize`).

The `knowledge-extractor` agent (Opus) does the heavy lifting. This skill
orchestrates the workflow and emits the final report.

**Session-end hint integration:** The session-end hook checks
`.great_cto/.last-crystallize` and suggests running `/crystallize` when the
session count exceeds `last_sessions + 10`. Run this skill after ≥10 sessions
to keep extracted skills current.

---

## Step 1 — Gather raw material

```bash
# Count sessions
SESSION_COUNT=$(ls .great_cto/logs/session-*-end.md 2>/dev/null | wc -l | tr -d ' ')
echo "Sessions: $SESSION_COUNT"

# Read lessons
cat .great_cto/lessons.md 2>/dev/null || echo "(no lessons yet)"

# Read cross-project decisions
cat ~/.great_cto/decisions.md 2>/dev/null | head -200 || echo "(none)"

# Find patterns that appear in ≥3 sessions
grep -h "^## pattern:" .great_cto/logs/session-*-end.md 2>/dev/null | sort | uniq -c | sort -rn | head -20

# Recent git log for context
git log --oneline --since="30 days ago" | head -30
```

If `SESSION_COUNT` is 0, tell the CTO: "No session logs found in
`.great_cto/logs/`. Run at least 10 sessions before crystallizing." Exit.

If `SESSION_COUNT` < 10, tell the CTO: "Only `{N}` sessions found. Patterns
are more reliable after ≥10 sessions. Proceed anyway? [yes/no]" Wait for
confirmation before continuing.

---

## Step 2 — Cluster patterns (via knowledge-extractor agent)

Spawn the `knowledge-extractor` agent with the gathered data as context:

```
Agent: knowledge-extractor
Task: |
  Read .great_cto/lessons.md and all files in .great_cto/logs/.
  Cluster lesson entries by pattern slug.
  For each cluster with ≥3 occurrences, write a draft skill file to
  skills/{domain}/SKILL.md (status: draft in frontmatter).
  If a skill for that domain already exists, append a new ## section instead
  of replacing the file.
  Infer domain from the pattern slug and its archetype tags.
  Return a structured summary: clusters found, drafts written, already-covered.
```

Wait for the agent to complete before proceeding to Step 3.

---

## Step 3 — Emit promotion report

After the agent completes, print:

```
CRYSTALLIZE REPORT
════════════════════════════════════════
Sessions analysed: {SESSION_COUNT}
Lessons found:     {LESSON_COUNT}
Clusters:          {CLUSTER_COUNT}
Draft skills:      {DRAFT_COUNT}  (in skills/{domain}/SKILL.md)
Already covered:   {COVERED_COUNT}  (pattern already in existing skill)
════════════════════════════════════════
Draft files:
  {list of paths and brief description per draft}

Next: review drafts, remove `status: draft` when satisfied.
Run /crystallize again after 10 more sessions.
════════════════════════════════════════
```

---

## Step 4 — Write .last-crystallize marker

After emitting the report, write the marker file:

```bash
SESSION_COUNT=$(ls .great_cto/logs/session-*-end.md 2>/dev/null | wc -l | tr -d ' ')
DRAFT_COUNT={P}   # from agent output
mkdir -p .great_cto
node -e "
const fs = require('fs');
fs.writeFileSync('.great_cto/.last-crystallize', JSON.stringify({
  ts: new Date().toISOString(),
  sessions: parseInt('$SESSION_COUNT') || 0,
  drafts: parseInt('$DRAFT_COUNT') || 0
}) + '\n');
"
```

---

## Step 5 — Auto-run cadence suggestion

If `SESSION_COUNT` is a multiple of 10 (and > 0), append to the report:

```
Auto-suggestion: you've completed {SESSION_COUNT} sessions. Consider running
`/crystallize` every 10 sessions to keep skills current.
```
