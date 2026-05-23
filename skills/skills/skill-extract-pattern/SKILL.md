---
name: skill-extract-pattern
description: Extract patterns from coding agent sessions to improve existing skills or create new ones. Use after completing a work session where you used or needed a skill, when you discovered a new pattern, or when you want to capture workflow knowledge. Works with Claude Code, Pi, and Codex session files. Triggers on "extract pattern", "improve skill from session", "create skill from session", "analyze session".
---

# Skill Extract Pattern

## Purpose

Analyze coding agent session transcripts to extract reusable patterns and improve skills. Captures knowledge discovered during real work.

**Versioning note:** Changes to skills are versioned through feature branch commits, not dedicated skill commits.

## When to Use

**After a session where:**
- You used a skill and found gaps
- You discovered a new reusable pattern
- You figured out a workaround not documented
- You want to capture workflow knowledge

**For:**
- Improving existing skills based on real usage
- Creating new skills from discovered patterns
- Documenting edge cases and solutions

## Quick Start

```bash
# Extract current session and analyze
./scripts/extract-session.js > /tmp/session-transcript.txt

# Then use this skill to analyze and improve/create
```

## Session Extraction

The `extract-session.js` script finds and parses session files:

```bash
# Auto-detect (most recent session for current directory)
./scripts/extract-session.js

# Specify agent type
./scripts/extract-session.js --agent claude
./scripts/extract-session.js --agent pi
./scripts/extract-session.js --agent codex

# Different working directory
./scripts/extract-session.js --cwd /path/to/project

# Specific session file
./scripts/extract-session.js /path/to/session.jsonl
```

**Session locations:**
- **Claude Code:** `~/.claude/projects/<encoded-cwd>/*.jsonl`
- **Pi:** `~/.pi/agent/sessions/<encoded-cwd>/*.jsonl`
- **Codex:** `~/.codex/sessions/YYYY/MM/DD/*.jsonl`

## Workflow: Improve Existing Skill

### Step 1: Extract Session

```bash
./scripts/extract-session.js > /tmp/session-transcript.txt
```

### Step 2: Find the Skill

Locate existing skill:
- `~/.codex/skills/<skill-name>/SKILL.md`
- `~/.claude/skills/<skill-name>/SKILL.md`
- `~/.pi/agent/skills/<skill-name>/SKILL.md`

### Step 3: Analyze and Improve

Read the current skill, then analyze the transcript:

**Look for:**
- Where you struggled to use the skill
- What information was missing
- What examples would have helped
- What you figured out on your own
- Workarounds discovered
- Errors encountered and resolved

### Step 4: Apply Changes

Improve the skill:
1. Add missing instructions
2. Add examples for discovered use cases
3. Fix incorrect guidance
4. Make more concise where possible

### Step 5: Version Through Feature Work

Commit skill changes as part of feature branch work:

```bash
# NOT this (dedicated skill commit):
git commit -m "update skill"

# DO this (part of feature work):
git commit -m "feat: add user authentication
- Implement JWT tokens
- Add login/logout endpoints
- Update api-client skill with auth patterns discovered"
```

## Workflow: Create New Skill

### Step 1: Extract Session

```bash
./scripts/extract-session.js > /tmp/session-transcript.txt
```

### Step 2: Identify Pattern

Analyze transcript for:
- Core capability demonstrated
- Key commands, APIs, or patterns
- Common pitfalls and solutions
- Reusable workflow

### Step 3: Create Skill

Use skill-bootstrap to create initial skill, then skill-hardening if discipline-enforcing.

```markdown
New skill should capture:
1. The core workflow
2. Key commands/patterns
3. Pitfalls and how to avoid them
4. Example usage scenarios
```

### Step 4: Version Through Feature Work

```bash
git add .claude/skills/<new-skill>/
git commit -m "feat: implement CSV processor
- Add parsing logic
- Create csv-processor skill from patterns discovered"
```

## Why Extract from Sessions?

**Real vs. Theoretical:**
- Session patterns = actually worked
- Hypothetical patterns = might not work

**Context preserved:**
- Specific errors encountered
- Actual commands used
- Real rationalizations made

**Gap identification:**
- What was confusing?
- What was missing?
- What took too long?

## Tips for Good Extractions

### Look For

| Pattern | What to Capture |
|---------|-----------------|
| **Confusion** | Where did agent retry or change approach? |
| **Missing examples** | Specific commands or code discovered |
| **Workarounds** | What wasn't documented but needed? |
| **Errors** | What failed and how was it resolved? |
| **Success patterns** | What worked well? |

### Keep Skills Concise

- Focus on important information
- One excellent example beats many mediocre ones
- Remove narrative, keep patterns

## Integration with Other Skills

| Step | Skill | Purpose |
|------|-------|---------|
| 1 | skill-extract-pattern | Extract from session |
| 2 | skill-bootstrap | Create initial skill (if new) |
| 3 | skill-hardening | Bulletproof (if discipline-enforcing) |
| 4 | skill-evolve | Long-term iteration based on feedback |

## Example: Improving a Skill

**Session discovered:** API client skill missing auth error handling

**Transcript shows:**
- Agent struggled with 401 errors
- Had to figure out token refresh manually
- Eventually implemented retry logic

**Skill improvement:**
```markdown
## Error Handling

### Authentication Errors

Automatic token refresh on 401:

```python
if response.status_code == 401:
    refresh_token()
    retry_request()
```
```

**Commit as part of feature:**
```bash
git commit -m "feat: add user dashboard
- Implement dashboard UI
- Update api-client skill with auth error handling"
```

## Version

v1.0.0 (2025-01-28) - Pattern-extraction focused refactor of improve-skill