---
name: find-skills
model: fast
description: Discover and install agent skills from the open skills ecosystem. Use when user asks "how do I do X", "find a skill for", "is there a skill that can", wants to extend capabilities, or mentions needing help with a specific domain. Triggers on find skill, search skill, install skill, npx skills, skills.sh.
---

# Find Skills

Discover and install skills from the open agent skills ecosystem using `npx skills`.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install find-skills
```


## WHAT This Skill Does

Helps users find and install modular skill packages that extend agent capabilities with specialized knowledge, workflows, and tools.

## WHEN To Use

- User asks "how do I do X" where X might have an existing skill
- User says "find a skill for X" or "is there a skill for X"
- User asks "can you do X" where X is a specialized capability
- User wants to extend agent capabilities
- User mentions wishing they had help with a specific domain

**KEYWORDS**: find skill, search skill, install skill, add skill, npx skills, skills.sh

## The Workflow

### 1. Identify What They Need

Map their request to a search query:
- Domain: React, testing, design, deployment, etc.
- Task: writing tests, creating animations, reviewing PRs, etc.

### 2. Search for Skills

```bash
npx skills find [query]
```

**Examples:**
| User Request | Search Query |
|--------------|--------------|
| "How do I make my React app faster?" | `npx skills find react performance` |
| "Can you help with PR reviews?" | `npx skills find pr review` |
| "I need to create a changelog" | `npx skills find changelog` |

### 3. Present Results

When results are found:

```
I found a skill that might help! The "[skill-name]" skill provides [brief description].

To install it:
npx skills add [owner/repo@skill]

Learn more: https://skills.sh/[owner]/[repo]/[skill]
```

### 4. Install (If Requested)

```bash
npx skills add <owner/repo@skill> -g -y
```

- `-g` = install globally (user-level)
- `-y` = skip confirmation prompts

## Common Skill Categories

| Category | Example Queries |
|----------|-----------------|
| Web Development | react, nextjs, typescript, tailwind |
| Testing | testing, jest, playwright, e2e |
| DevOps | deploy, docker, kubernetes, ci-cd |
| Documentation | docs, readme, changelog, api-docs |
| Code Quality | review, lint, refactor, best-practices |
| Design | ui, ux, design-system, accessibility |

## When No Skills Found

```
I searched for skills related to "[query]" but didn't find any matches.

I can still help with this task directly. Would you like me to proceed?

If this is something you do often, you could create your own skill:
npx skills init my-skill-name
```

## NEVER

- Assume a skill exists without searching first
- Install skills without user confirmation
- Recommend creating a skill when an existing one would work
- Search with vague single-word queries (be specific: "react testing" not "testing")

## Key Commands Reference

| Command | Purpose |
|---------|---------|
| `npx skills find [query]` | Search for skills |
| `npx skills add <package>` | Install a skill |
| `npx skills add <pkg> -g -y` | Install globally, skip prompts |
| `npx skills check` | Check for updates |
| `npx skills update` | Update installed skills |
| `npx skills init` | Create a new skill |

**Browse all skills:** https://skills.sh/
