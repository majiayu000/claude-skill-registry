---
name: project-health
description: |
  AI-agent readiness auditing for project documentation and workflows. Evaluates whether
  future Claude Code sessions can understand docs, execute workflows literally, and resume
  work effectively. Use when onboarding AI agents to a project or ensuring context continuity.

  Includes three specialized agents: context-auditor (AI-readability), workflow-validator
  (process executability), handoff-checker (session continuity). Use PROACTIVELY before
  handing off projects to other AI sessions or team members.
---

# Project Health: AI-Agent Readiness Auditing

**Status**: Active
**Updated**: 2026-01-30
**Focus**: Ensuring documentation and workflows are executable by AI agents

## Overview

This skill evaluates project health from an **AI-agent perspective** - not just whether docs are well-written for humans, but whether future Claude Code sessions can:

1. **Understand** the documentation without ambiguity
2. **Execute** workflows by following instructions literally
3. **Resume** work effectively with proper context handoff

## When to Use

- Before handing off a project to another AI session
- When onboarding AI agents to contribute to a codebase
- After major refactors to ensure docs are still AI-executable
- When workflows fail because agents "didn't understand"
- Periodic health checks for AI-maintained projects

## Agent Selection Guide

| Situation | Use Agent | Why |
|-----------|-----------|-----|
| "Will another Claude session understand this?" | **context-auditor** | Checks for ambiguous references, implicit knowledge, incomplete examples |
| "Will this workflow actually execute?" | **workflow-validator** | Verifies steps are discrete, ordered, and include verification |
| "Can a new session pick up where I left off?" | **handoff-checker** | Validates SESSION.md, phase tracking, context preservation |
| Full project health audit | All three | Comprehensive AI-readiness assessment |

## Key Principles

### 1. Literal Interpretation

AI agents follow instructions literally. Documentation that works for humans (who fill in gaps) may fail for agents.

**Human-friendly** (ambiguous):
> "Update the config file with your settings"

**AI-friendly** (explicit):
> "Edit `wrangler.jsonc` and set `account_id` to your Cloudflare account ID (find it at dash.cloudflare.com → Overview → Account ID)"

### 2. Explicit Over Implicit

Never assume the agent knows:
- Which file you mean
- What "obvious" next steps are
- Environment state or prerequisites
- What success looks like

### 3. Verification at Every Step

Agents can't tell if something "feels right". Include verification:
- Expected output after each command
- How to check if a step succeeded
- What to do if it failed

## Agents

### context-auditor

**Purpose**: Evaluate AI-readability of documentation

**Checks**:
- Instructions use imperative verbs (actionable)
- File paths are explicit (not "the config file")
- Success criteria are measurable
- No ambiguous references ("that thing", "as discussed")
- Code examples are complete (not fragments)
- Dependencies/prerequisites stated explicitly
- Error handling documented

**Output**: AI-Readability Score (0-100) with specific issues

### workflow-validator

**Purpose**: Verify processes are executable when followed literally

**Checks**:
- Steps are discrete and ordered
- Each step has clear input/output
- No implicit knowledge required
- Environment assumptions documented
- Verification step after each action
- Failure modes and recovery documented
- No "obvious" steps omitted

**Output**: Executability Score (0-100) with step-by-step analysis

### handoff-checker

**Purpose**: Ensure session continuity for multi-session work

**Checks**:
- SESSION.md or equivalent exists
- Current phase/status clear
- Next actions documented
- Blockers/decisions needed listed
- Context for future sessions preserved
- Git checkpoint pattern in use
- Architecture decisions documented with rationale

**Output**: Handoff Quality Score (0-100) with continuity gaps

## Templates

### AI-Readable Documentation Template

See `templates/AI_READABLE_DOC.md` for a template that ensures AI-readability.

Key sections:
- **Prerequisites** (explicit environment/state requirements)
- **Steps** (numbered, discrete, with verification)
- **Expected Output** (what success looks like)
- **Troubleshooting** (common failures and fixes)

### Handoff Checklist

See `templates/HANDOFF_CHECKLIST.md` for ensuring clean session handoffs.

## Anti-Patterns

### 1. "See Above" References

```markdown
# Bad
As mentioned above, configure the database.

# Good
Configure the database by running:
`npx wrangler d1 create my-db`
```

### 2. Implicit File Paths

```markdown
# Bad
Update the config with your API key.

# Good
Add your API key to `.dev.vars`:
```
API_KEY=your-key-here
```
```

### 3. Missing Verification

```markdown
# Bad
Run the migration.

# Good
Run the migration:
`npx wrangler d1 migrations apply my-db --local`

Verify with:
`npx wrangler d1 execute my-db --local --command "SELECT name FROM sqlite_master WHERE type='table'"`

Expected output: Should show your table names.
```

### 4. Assumed Context

```markdown
# Bad
Now deploy (you know the drill).

# Good
Deploy to production:
`npx wrangler deploy`

Verify deployment at: https://your-worker.your-subdomain.workers.dev
```

## Relationship to Other Tools

| Tool | Focus | Audience |
|------|-------|----------|
| `project-docs-auditor` | Traditional doc quality (links, freshness, structure) | Human readers |
| `project-health` skill | AI-agent readiness (executability, clarity, handoff) | Claude sessions |
| `docs-workflow` skill | Creating/managing specific doc files | Both |

## Quick Start

1. **Full audit**: "Run all project-health agents on this repo"
2. **Check one aspect**: "Use context-auditor to check AI-readability"
3. **Before handoff**: "Use handoff-checker before I end this session"

## Success Metrics

A healthy project scores:
- **Context Auditor**: 80+ (AI can understand without clarification)
- **Workflow Validator**: 90+ (steps execute literally without failure)
- **Handoff Checker**: 85+ (new session can resume immediately)

Projects below these thresholds have documentation debt that will slow future AI sessions.
