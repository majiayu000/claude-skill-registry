---
name: self-improve
description: Captures learnings, errors, and corrections to enable continuous improvement. Activates when a command fails, the user corrects Claude, a knowledge gap is discovered, or a better approach is found.
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Edit
---

# Self-Improvement Engine

You are a continuously learning agent. After every meaningful interaction, evaluate whether something was learned and log it.

## When to Log

### Errors (ERR) — Log when:
- A command returns a non-zero exit code
- An exception or stack trace appears
- Unexpected output or behavior occurs
- A timeout or connection failure happens
- A tool call is denied or fails

### Learnings (LRN) — Log when:
- The user corrects you ("No, that's wrong...", "Actually...", "Not like that...")
- You discover your knowledge is outdated or incorrect
- Documentation you referenced is wrong or has changed
- An API behaves differently than expected
- A better approach is discovered for something you've done before
- The user provides information you didn't know

### Feature Requests (FEAT) — Log when:
- The user asks for a capability that doesn't exist
- You realize a skill would make a recurring task easier
- The user says "I wish you could..." or "Can you..."

## How to Log

Each entry is an **individual markdown file** in `vault/learnings/` with YAML frontmatter.

### File Naming
- `vault/learnings/LRN-YYYYMMDD-XXX.md` for learnings
- `vault/learnings/ERR-YYYYMMDD-XXX.md` for errors
- `vault/learnings/FEAT-YYYYMMDD-XXX.md` for feature requests

To determine the next sequence number (XXX), list existing files in `vault/learnings/` matching today's date and the entry type prefix, then increment.

### Templates

See template files for the full frontmatter and body format:
- [templates/learning.md](templates/learning.md) — LRN template
- [templates/error.md](templates/error.md) — ERR template
- [templates/feature.md](templates/feature.md) — FEAT template

## Recurring Pattern Detection

Before creating a new entry:
1. List files in `vault/learnings/` and scan their frontmatter for matching `pattern-key` or overlapping `tags`
2. If a match is found:
   - Add a `[[wikilink]]` to the `related` list in both the existing and new file's frontmatter
   - Increment `recurrence-count` on the original file
   - Update `last-seen` date on the original file
   - Do NOT create a duplicate entry — only update the original
3. If no match, create a new entry file

## Promotion Rules

When a learning meets ALL of these criteria, flag it for promotion:
- `recurrence-count` >= 3
- Occurred across 2+ distinct tasks
- Within a 30-day window (`last-seen` - `first-seen` <= 30 days)

**Promotion process:**
1. Change `status` to `promoted` in the file's frontmatter
2. Append the learning to the `## Promoted Learnings` section of `CLAUDE.md`
3. Format: `- **[Area]**: Learning description (promoted YYYY-MM-DD, from LRN-XXXXXXXX-XXX)`

**Important**: Always ask the user for approval before promoting. Say:
> "I've noticed a recurring pattern: [description]. This has come up [N] times. Should I promote this to CLAUDE.md so I always remember it?"

## Skill Extraction

When a learning is valuable enough to become a reusable skill, it qualifies if:
- It has 2+ `[[wikilinks]]` in its `related` list
- Status is `resolved` with a verified working fix
- It required non-obvious debugging to discover
- It's broadly applicable across projects

To extract, create a new SKILL.md in `.claude/skills/<skill-name>/` with:
- `disable-model-invocation: true` (user must opt-in to new auto-generated skills)
- Clear description of what the skill does
- The learned workflow as step-by-step instructions

Always ask the user before creating a new skill.

## Daily Digest

When invoked with `/self-improve digest` or at the end of a long session, summarize:
- New entries added today (count by type) — check `vault/learnings/` for files with today's date
- Any patterns approaching promotion threshold (recurrence-count >= 2)
- Any feature requests that could be built quickly
