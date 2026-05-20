---
name: self-improvement
description: Analyze conversation history to find friction patterns and suggest CLAUDE.md/skill improvements. Use when user wants to review what went wrong across sessions and systematically improve. (user)
allowed-tools: Read, Bash, Grep, Glob, Task
---

# Self-Improvement - Learn from History

Analyze Claude Code conversation history to find friction patterns, check what's already fixed, and suggest improvements.

## Instructions

### Phase 1: Find Conversations

```bash
# Get project directory (encode current path with dashes)
ls ~/.claude/projects/

# List today's conversations (or adjust -mtime for longer range)
ls -lt ~/.claude/projects/<encoded-path>/*.jsonl | head -20
```

### Phase 2: Parallel Analysis

Spawn Task agents (subagent_type: general-purpose) to analyze conversations in parallel. Each agent reads one .jsonl file and extracts:

1. What was user trying to accomplish?
2. Problems/friction that occurred (include user quotes showing frustration)
3. What worked well?
4. Repeated patterns or inefficiencies

For large files (>500KB), prioritize those - they contain the meatiest sessions.

### Phase 3: Synthesize

After all agents complete, combine findings:

- **Top friction patterns** ranked by frequency
- **What worked well** (don't lose these)
- **User frustration quotes** (raw evidence)

**Generalize aggressively.** Look for the meta-pattern behind specific issues.

### Phase 4: Cross-Reference

Read current documentation:
- Project CLAUDE.md
- User ~/.claude/CLAUDE.md
- Skills in .claude/skills/ and ~/.claude/skills/

For each friction pattern, classify:
- **Already fixed** - note location
- **Still missing** - needs addition

### Phase 5: Output

Create a markdown file (e.g., `CLAUDE_IMPROVEMENTS.md`) with:

```markdown
# Suggested CLAUDE.md Improvements

Based on analysis of N conversations from [date range].

## 1. [Issue Name]

**Problem:** [Description of friction]

**Suggested addition to [location]:**

\```markdown
[Proposed text]
\```

---

## Already Fixed

| Issue | Where |
|-------|-------|
| ... | ... |

---

## Potential Skills

| Skill | Purpose |
|-------|---------|
| ... | ... |

---

## Raw Friction Log

- "user quote 1"
- "user quote 2"
```

**Do not apply changes** - create the file for user review.

## Usage Examples

```
/self-improvement
/self-improvement last 3 days
/self-improvement refactoring
```
