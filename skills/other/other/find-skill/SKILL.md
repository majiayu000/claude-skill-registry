---
name: find-skill
description: Discovers existing skills or creates new ones when the user asks for capabilities that don't exist.
user-invocable: true
argument-hint: "<search query>"
context: fork
agent: researcher
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Skill Discovery

When the user asks for a capability, search for it before saying "I can't".

## Usage

- `/find-skill <query>` — Search for a skill or vault knowledge matching the query
- Also triggers automatically on phrases like "how do I...", "is there a way to...", "can you...", "I wish you could..."

## Search Strategy

Execute these steps in order. Stop as soon as a strong match is found.

### Step 1: Search Existing Skills

Search `.claude/skills/` for matching SKILL.md files:

1. Use `Glob` to list all `.claude/skills/*/SKILL.md` files
2. Read each SKILL.md and check if:
   - The `name` or `description` in frontmatter matches the query keywords
   - The body content addresses the user's need
3. If a match is found, tell the user:
   > "There's already a skill for that: **<name>** — <description>"
   > Then explain how to use it.

### Step 2: Search Vault Learnings

Search `vault/learnings/` for related knowledge:

1. Use `Grep` to search `vault/learnings/*.md` for the query keywords
2. Also search by likely tags: extract keywords from the query and search for them in frontmatter `tags:` lines
3. If matches are found, summarize the relevant learnings:
   > "I don't have a dedicated skill for that, but I found related knowledge in the vault:"
   > - List matching entries with their titles and key insights
   > - If a learning has `status: resolved` and a working fix, present the solution

### Step 3: Search Vault Shared Knowledge

Search `vault/shared/` for conventions, tool gotchas, or project knowledge:

1. Use `Grep` to search `vault/shared/**/*.md` for query keywords
2. Present any matching conventions or known gotchas

### Step 4: Search Heartbeat Tasks

Check if there's an existing heartbeat task that addresses the need:

1. Use `Glob` to list `heartbeat-tasks/*.json` files
2. Read configs and check if any task's `prompt` or `name` relates to the query

### If No Match Found

If no matches found in any of the above, report your findings and suggest the user run `./scripts/extract-skill.sh <name>` to scaffold a new skill, or ask Claude to build it in the main conversation.

## Search Tips

- When extracting keywords from the user's query, strip common words ("how", "do", "I", "the", "is", "there", "a", "way", "to", "can", "you")
- Search for both the exact phrase and individual keywords
- Consider synonyms: "schedule" ↔ "heartbeat" ↔ "cron", "memory" ↔ "vault" ↔ "learnings", "deploy" ↔ "push" ↔ "release"
- Frontmatter `tags` and `pattern-key` are the most reliable search targets in vault files
