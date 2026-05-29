---
name: oops
description: "Zero-friction mistake capture. Analyzes recent conversation to extract lessons learned and stores them in global beads. Use when user says '/oops', 'save this mistake', 'remember this', or after fixing a bug."
allowed-tools: Bash, Read
---

# Oops - Mistake Learning System

You are an expert at extracting lessons learned from debugging sessions and storing them for future reference.

## When To Use

- User says `/oops` or "oops"
- User says "save this mistake" or "remember this"
- User says "that was a lesson" or "don't let me do that again"
- After successfully fixing a bug (offer to save)

## Inputs

- Recent conversation context (you have full access)
- The mistake that was made
- How it was fixed

## Outputs

- Lesson stored in global beads (~/.claude/.beads/)
- Confirmation message with lesson summary

## Workflow

### 1. Analyze Recent Conversation

Look back through the conversation to identify:
- **What we were trying to do** (the goal)
- **What went wrong** (the symptom)
- **Root cause** (why it failed)
- **How we fixed it** (the solution)
- **Tags** (technology areas: docker, git, python, networking, etc.)

### 2. Extract Lesson

Format the lesson as:
```
Title: [Concise description of the mistake and fix]
Tags: [Relevant technology tags]
Description:
- Root cause: [Why it happened]
- Fix: [What solved it]
- Prevention: [How to avoid next time]
```

### 3. Create Bead

```bash
cd ~/.claude && bd create "Lesson: [title]" \
  -t chore \
  -l lesson,[tag1],[tag2] \
  --description "Root cause: [root cause]

Fix: [fix]

Prevention: [prevention]

Project: [current project name]"
```

### 4. Confirm to User

```
Saved lesson: "[title]"
Tags: [tags]

You can query lessons with:
  /lessons [tag]    - Search by tag
  /lessons          - Show recent lessons
```

## Query Lessons (/lessons)

When user says `/lessons` or `/lessons [query]`:

```bash
# List all lessons
cd ~/.claude && bd list -l lesson --json

# Search by tag
cd ~/.claude && bd list -l lesson,[tag] --json

# Show recent 5
cd ~/.claude && bd list -l lesson --json | jq '.[:5]'
```

Format output as:
```
Found [N] lessons:
  [id] [date] [title] - Tags: [tags]
  [id] [date] [title] - Tags: [tags]
```

## Examples

### Example 1: Docker Networking

```
User: /oops

[Context: We just spent 20 minutes debugging why a container couldn't reach
localhost:8080, and fixed it by using host.docker.internal]

Claude: Analyzing recent conversation...

Extracted lesson:
- Mistake: Used localhost to reach host from Docker container
- Root cause: Container's localhost is its own loopback, not the host
- Fix: Use host.docker.internal (Mac/Windows) or 172.17.0.1 (Linux)

Creating bead...

Saved lesson: "Docker localhost isolation - use host.docker.internal"
Tags: docker, networking, containers
```

### Example 2: Git Workflow

```
User: remember this for next time

[Context: We accidentally committed to main instead of a feature branch]

Claude: Analyzing recent conversation...

Extracted lesson:
- Mistake: Committed directly to main branch
- Root cause: Forgot to create feature branch before starting work
- Fix: git reset HEAD~1, git checkout -b feature/x, git commit
- Prevention: Always run 'git branch' before starting work

Creating bead...

Saved lesson: "Git - always create feature branch before committing"
Tags: git, workflow
```

## Storage Details

- **Location**: `~/.claude/.beads/` (global, cross-project)
- **Format**: Beads with label "lesson"
- **Type**: chore (beads doesn't have a "lesson" type)
- **Query**: `bd list -l lesson` in ~/.claude directory

## Integration with Other Skills

- **Debugger**: After fixing a bug, debugger can suggest running /oops
- **SessionStart hook**: Loads recent lessons into context
- **Resume handoff**: Includes relevant lessons in context restoration

## Keywords

oops, save this mistake, remember this, lesson learned, don't do that again, lessons
