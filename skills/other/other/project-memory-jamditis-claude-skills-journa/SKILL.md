---
name: project-memory
description: Generate CLAUDE.md project memory files that transfer institutional knowledge, not obvious information. Use when setting up new journalism projects, onboarding collaborators, or documenting project-specific quirks. Includes templates for editorial tools, event websites, publications, research projects, content pipelines, and digital archives.
---

# Project memory generator

Create CLAUDE.md files that transfer tribal knowledge, not obvious information. Think like a senior journalist onboarding a competent colleague—you don't explain how journalism works, you explain YOUR project's quirks.

## What belongs in CLAUDE.md

| Include | Don't include |
|---------|---------------|
| Project-specific quirks | How journalism works generally |
| YOUR naming conventions | Standard file organization |
| Commands with YOUR flags | Generic commands like "npm install" |
| Non-obvious architecture | Framework documentation |
| Common mistakes in THIS project | General best practices |
| External service configurations | Information already in comments |
| Source handling requirements | Basic ethics everyone knows |

## The deletion test

For every line you write, ask: "Would an experienced journalist already know this?"
- If yes → Delete it
- If no → Keep it

## Basic template structure

```markdown
# CLAUDE.md

## Project overview
[1-2 sentences maximum. What this does + who uses it.]

## Commands
[Only project-specific commands. Not generic ones.]

## Architecture
[Only non-obvious decisions. Where does X live? Why?]

## Patterns
[Only patterns unique to this project]

## Things to avoid
[Project-specific anti-patterns and gotchas]

## External dependencies
[APIs, services, credential locations]
```

## What to cut ruthlessly

**Generic commands everyone knows:**
```markdown
<!-- DELETE THIS -->
git add .      # Stage changes
npm install    # Install dependencies
```

**Obvious journalism patterns:**
```markdown
<!-- DELETE THIS -->
We verify facts before publishing. All quotes must be
attributed. Follow AP Style...
```

**Framework explanations:**
```markdown
<!-- DELETE THIS -->
React components live in /components. We use hooks
for state management...
```

## What to keep

**Project-specific quirks:**
```markdown
<!-- KEEP THIS -->
Source names in the spreadsheet use LAST, FIRST format
but the CMS expects FIRST LAST. The import script handles
this, but manual entries need flipping.
```

**Non-obvious architecture:**
```markdown
<!-- KEEP THIS -->
Embargo dates are stored in the CMS as NYC time but
displayed in the reader's local time. Server-side renders
use UTC. Check timezone handling before changing date code.
```

**Gotchas that burned you:**
```markdown
<!-- KEEP THIS -->
The AP feed disconnects silently after 4 hours. Cron job
at :00 checks connection and restarts if stale.
```

## Voice guidelines

- Direct and terse
- Like notes you'd leave for yourself
- No marketing language
- No "Welcome to..." introductions
- No "This project is..." padding

## Example: Good vs bad

**Bad (too verbose, obvious):**
```markdown
# CLAUDE.md

## Overview
Welcome to our newsroom's story tracking system! This is a
web application built with React and Node.js that helps
editors and reporters collaborate on stories.

## Getting started
First, make sure you have Node.js installed. Then:
npm install
npm start
```

**Good (tribal knowledge only):**
```markdown
# CLAUDE.md

## Overview
Story tracker for metro desk. React + Supabase.

## Gotchas
- Story slugs must be unique across ALL desks, not just metro
- "Hold" status doesn't stop the autopublish cron—use "Kill"
- Reporter dropdown caches for 1 hour; new hires won't appear

## Commands
npm run sync-ap  # Pull latest from AP, runs automatically at :15

## Credentials
Supabase key in 1Password "Metro Desk" vault, not .env
```

## Length guideline

A good CLAUDE.md is 50-150 lines. If it's longer, you're explaining too much. If it's shorter, you might be missing critical quirks.

## Journalism-specific templates

Templates are in the `templates/` directory:

| Template | Use for |
|----------|---------|
| `editorial-tool.md` | Newsroom tools, fact-checkers, AI assistants |
| `event-website.md` | Conferences, workshops, campaign sites |
| `publication.md` | Newsletters, podcasts, ongoing content series |
| `research-project.md` | Investigations, data journalism with defined scope |
| `content-pipeline.md` | CMS workflows, publishing automation |
| `digital-archive.md` | Historical collections, document repositories |

### Template selection guide

```
What are you building?
├── Tool for the newsroom → editorial-tool.md
├── Site for an event → event-website.md
├── Recurring content series → publication.md
├── One-time investigation → research-project.md
├── Publishing automation → content-pipeline.md
└── Archive/preservation → digital-archive.md
```

## How to use templates

1. Copy the appropriate template to your project root as `CLAUDE.md`
2. Fill in the bracketed placeholders with YOUR specifics
3. Delete any sections that don't apply
4. Add project-specific gotchas as you discover them
5. Keep it updated—stale CLAUDE.md files cause confusion

---

*The best CLAUDE.md files are written by people who've been burned by the quirks they're documenting.*
