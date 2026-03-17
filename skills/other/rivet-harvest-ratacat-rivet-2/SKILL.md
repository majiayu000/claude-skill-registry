---
name: rivet-harvest
description: Capture decisions and requirements from conversation history. Use when user says "harvest", "capture decisions", or "save what we discussed" to persist architectural decisions into .rivet/systems.yaml.
user-invocable: true
allowed-tools: Bash, Read, Glob, Grep, Edit, Write, AskUserQuestion
---

# Rivet Harvest - Extract Decisions from Transcripts

Capture architectural decisions, requirements, and terminology from Claude Code conversation history and add them to .rivet/systems.yaml.

## Purpose

During AI-assisted development, valuable decisions get made in conversation:
- "We should use async-first for scale"
- "The Router must support nested routes"
- "Let's call this concept 'vibe coding'"

These decisions are valuable but ephemeral. Harvest extracts them and locks them into .rivet/systems.yaml so they persist.

## Prerequisites

- .rivet/systems.yaml must exist with at least one system defined
- Run scan first if no .rivet/systems.yaml exists

## What to Extract

### Requirements
Statements about what a system MUST do:
- "must support X"
- "needs to handle Y"
- "should always Z"

### Decisions
Architectural choices made during development:
- "we're going with X approach"
- "decided to use Y for Z"
- "async-first for scale"

### Terminology
New terms or concepts defined:
- "let's call this X"
- "X means Y in this codebase"
- Glossary entries

## Harvest Process

### Step 1: Read Current .rivet/systems.yaml

```bash
cat .rivet/systems.yaml
```

Understand existing systems so extracted items can be assigned correctly.

### Step 2: Locate Transcript History

Claude Code stores transcripts in `~/.claude/projects/<project-hash>/`.

```bash
# Find recent transcripts for this project
ls -lt ~/.claude/projects/*/transcripts/ 2>/dev/null | head -20
```

### Step 3: Parse Transcripts

Look for patterns indicating decisions, requirements, or terminology:

**Requirement patterns:**
- "must", "should", "needs to", "has to", "required"
- Context: usually follows discussion of a system or feature

**Decision patterns:**
- "decided", "going with", "we'll use", "chosen", "approach"
- Context: usually resolves a discussion or comparison

**Terminology patterns:**
- "let's call", "we define", "means", "refers to"
- Context: naming or concept clarification

### Step 4: Present Extracted Items

Show the user what was found:

```
Found 5 potential items to harvest:

Requirements:
  1. [Router] must support nested routes
  2. [API] needs to handle rate limiting

Decisions:
  3. [Router] async-first approach for scale
  4. [Database] PostgreSQL over SQLite

Terminology:
  5. vibe_coding: AI handles implementation while human guides

Which items should be added to .rivet/systems.yaml? (comma-separated numbers, or 'all')
```

### Step 5: Assign to Systems

For each selected item, confirm or reassign the target system:

```
Item: "must support nested routes"
Detected system: Router
[Enter] to confirm, or type system name to reassign:
```

### Step 6: Write to .rivet/systems.yaml

Add extracted items to the appropriate systems:

```yaml
systems:
  Router:
    description: URL routing and navigation
    requirements:
      - must support nested routes
    decisions:
      - async-first approach for scale
```

Add glossary terms to the project level:

```yaml
glossary:
  vibe_coding: AI handles implementation while human guides
```

## Usage

```
/rivet-harvest
```

The skill will:
1. Check for .rivet/systems.yaml (fail if missing)
2. Scan recent transcripts
3. Extract potential items
4. Present interactive selection
5. Write selected items to .rivet/systems.yaml

## Notes

- Items are deduplicated against existing .rivet/systems.yaml entries
- Each harvest is atomic - all selected items written in one commit
- Git auto-commits changes with descriptive message
