---
name: skills-browser
description: Visual skill discovery with fuzzy search, categorization, and usage stats for 43+ ONE_SHOT skills.
homepage: https://github.com/Khamel83/oneshot
allowed-tools: Read, Write, Edit, Bash
metadata: {"oneshot":{"emoji":"🔍","requires":{"bins":[]}}}
---

# /browse - ONE_SHOT Skill Discovery

**Find the right skill, fast.** Fuzzy search through 43 skills by name, category, or trigger phrase.

---

## When To Use

User says:
- `/browse [keyword]` - Fuzzy search skills
- `/browse --category` - List by category
- `/browse --stats` - Show skill categories
- "what skills do I have"
- "find skill for [task]"
- "skill for [keyword]"

---

## How It Works

**Parse the command:**
- `/browse testing` → Search for "testing" in skill names, descriptions, triggers
- `/browse --category` → Show all skills grouped by category
- `/browse --stats` → Show skill counts by category
- `/browse --list` → Compact list of all skills

**Search in:**
- Skill name
- Description text
- Trigger phrases
- Category classification

---

## Skill Categories

### Core (5 skills) - Use 90% of the time
| Skill | Triggers | Purpose |
|-------|----------|---------|
| front-door | "build me", "new project" | Interview → spec → plan |
| create-plan | "plan", "design" | Structured planning |
| implement-plan | "implement", "build it" | Execute with beads tracking |
| debugger | "bug", "broken", "fix" | Systematic debugging |
| code-reviewer | "review", "is this safe" | Quality + security review |

### Research (4 skills) - Token-free discovery
| Skill | Tokens | Purpose |
|-------|--------|---------|
| freesearch | FREE | Research via Exa API, 0 Claude tokens |
| dispatch | FREE | Route to local CLIs (codex/gemini/qwen) |
| deep-research | Uses tokens | Background research via Gemini CLI |
| search-fallback | Uses tokens | Fallback when WebSearch fails |

### Context Management (5 skills) - Always available
| Skill | Purpose |
|-------|---------|
| beads | Persistent task tracking (git-backed) |
| create-handoff | Save context before /clear |
| resume-handoff | Restore from handoff |
| failure-recovery | Recovery from stuck states |
| thinking-modes | Extended analysis (5 levels) |

### Autonomous (3 skills) - Headless execution
| Skill | Purpose |
|-------|---------|
| autonomous-builder | Idea → artifact (survives disconnect) |
| resilient-executor | Disconnect-proof via tmux |
| delegate-to-agent | Spawn isolated sub-agents |

### Development (7 skills)
| Skill | Triggers | Purpose |
|-------|----------|---------|
| refactorer | "refactor", "clean up" | Systematic refactoring |
| test-runner | "run tests", "coverage" | Test execution + analysis |
| performance-optimizer | "slow", "optimize" | Evidence-based optimization |
| parallel-validator | "validate", "check everything" | Run tests/lint/security in parallel |
| batch-processor | "rename across", "update all" | Apply changes to many files |
| auto-updater | (auto on session start) | Auto-update from GitHub |
| hooks-manager | "hooks", "lifecycle" | Git hooks automation |

### Operations (6 skills)
| Skill | Triggers | Purpose |
|-------|----------|---------|
| git-workflow | "commit", "PR", "push" | Conventional commits, PRs |
| docker-composer | "docker", "containerize" | Docker/Compose setup |
| ci-cd-setup | "CI", "CD", "pipeline" | GitHub Actions, pipelines |
| push-to-cloud | "deploy", "host this" | Deploy to OCI-Dev |
| remote-exec | "run on homelab", "ssh" | Execute on remote machines |
| observability-setup | "monitoring", "metrics" | Logging, metrics, alerts |

### Data & APIs (4 skills)
| Skill | Triggers | Purpose |
|-------|----------|---------|
| database-migrator | "migration", "schema" | Safe schema changes |
| api-designer | "design API", "REST" | API specifications |
| oci-resources | "oci database", "storage" | OCI free-tier resources |
| convex-resources | "convex", "reactive" | Convex backend for web apps |

### Documentation (1 skill)
| Skill | Triggers | Purpose |
|-------|----------|---------|
| documentation-generator | "update docs", "README" | Generate docs, ADRs |

### Secrets (2 skills)
| Skill | Triggers | Purpose |
|-------|----------|---------|
| secrets-vault-manager | "secrets", "env", "API keys" | SOPS/Age encryption |
| secrets-sync | "sync secrets", "pull secrets" | Two-way vault sync |

### Interview Control (3 skills)
| Skill | Purpose |
|-------|---------|
| full-interview | All 13+ questions (greenfield) |
| quick-interview | Q1,Q2,Q6,Q12 (experienced users) |
| smart-interview | Auto-detect depth (default) |

### Specialized (3 skills)
| Skill | Triggers | Purpose |
|-------|----------|---------|
| the-audit | "audit this", "make strategic" | Strategic communication filter |
| visual-iteration | "polish UI", "10/10" | Self-scoring design loop |
| skillsmp-browser | "browse skillsmp", "find skills" | External skill marketplace |

---

## Fuzzy Search Examples

```bash
/browse test        # → test-runner, parallel-validator
/browse deploy      # → push-to-cloud, ci-cd-setup
/browse secret      # → secrets-vault-manager, secrets-sync
/browse docker      # → docker-composer
/browse research    # → freesearch, deep-research, dispatch
/browse memory      # → beads, create-handoff, resume-handoff
/browse parallel    # → parallel-validator, batch-processor
/browse optimize    # → performance-optimizer, refactorer
/browse remote      # → remote-exec, push-to-cloud
/browse docs        # → documentation-generator
```

---

## Output Format

### Search Results
```
🔍 Found 3 skills matching "test":

1. test-runner
   Triggers: "run tests", "coverage", "pytest"
   Purpose: Run tests, analyze results, improve coverage
   Category: Development

2. parallel-validator
   Triggers: "validate", "check everything"
   Purpose: Run tests/lint/security in parallel
   Category: Development

3. debugger
   Triggers: "bug", "broken", "fix"
   Purpose: Systematic debugging
   Category: Core
```

### Category View
```
📁 ONE_SHOT Skills by Category (43 total)

Core (5):     front-door, create-plan, implement-plan, debugger, code-reviewer
Research (4): freesearch, dispatch, deep-research, search-fallback
Context (5):  beads, create-handoff, resume-handoff, failure-recovery, thinking-modes
...
```

### Stats View
```
📊 Skill Statistics

Total Skills:    43
Core:            5  (most used)
Development:     7
Operations:      6
Research:        4 (token-free available)
Data & APIs:     4
Context:         5
Autonomous:      3
```

---

## Implementation Notes

**Skill data source:** Read from `~/.claude/skills/*/SKILL.md` or use INDEX.md

**Fuzzy matching:** Use simple substring matching (case-insensitive)

**Categories:** Parse from SKILL.md frontmatter metadata or infer from INDEX.md

**Usage stats:** (Future) Track skill invocations via beads or log files

---

## Quick Wins from Research

Based on competitor analysis (Cline, SkillsMP, Cursor):
- Visual skill discovery is the #1 requested feature
- 43 skills is overwhelming without search
- Cline has `/browse` → ONE_SHOT needs it too

---

## Keywords

browse, skills, find skill, skill search, list skills, skill discovery, fuzzy search
