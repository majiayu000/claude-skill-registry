---
name: gemini-workspace-bridge
description: Central authority for Claude-Gemini shared workspace architecture. Defines directory structure, artifact exchange, and file naming conventions. Use when setting up dual-CLI workflows, deciding where to store AI artifacts, or managing cross-CLI file exchange.
allowed-tools: Read, Glob, Grep, Bash
---

# Gemini Workspace Bridge

## Documentation Delegation

> **Documentation Source:** For authoritative workspace patterns and current conventions, query `gemini-cli-docs` skill.
> This skill provides integration guidance; `gemini-cli-docs` provides official Gemini CLI documentation.

## Overview

This skill defines the hybrid workspace architecture for Claude Code and Gemini CLI collaboration. It establishes conventions for file storage, artifact exchange, and cross-CLI communication.

## When to Use This Skill

**Keywords:** workspace structure, artifact storage, cross-cli, shared files, gemini artifacts, claude artifacts, file locations, where to store

**Use this skill when:**

- Setting up a project for dual-CLI workflow
- Deciding where to store AI-generated artifacts
- Understanding the hybrid tracked/gitignored strategy
- Managing cross-CLI file exchange

## Core Architecture

### Hybrid Approach

The workspace uses a **hybrid strategy**:

- **Tracked files**: Memory files, valuable artifacts (plans, reports)
- **Gitignored temp**: Session state, caches, transient outputs

### Directory Structure

```text
project-root/
├── CLAUDE.md                    # Source of truth (tracked)
├── GEMINI.md                    # Points to CLAUDE.md + overrides (tracked)
│
├── .claude/
│   ├── settings.json            # Claude Code configuration
│   └── temp/                    # (gitignored) Session artifacts
│       └── gemini-results/      # Parsed Gemini outputs
│
├── .gemini/
│   ├── settings.json            # Gemini CLI configuration
│   └── temp/                    # (gitignored) Gemini session state
│
└── docs/                        # (tracked) Persistent AI artifacts
    └── ai-artifacts/            # Version-controlled reports
        ├── explorations/        # Codebase exploration reports
        └── plans/               # Implementation plans
```

## Artifact Location Guide

### Decision Tree

```text
Is this artifact valuable long-term?
├── YES: Should others see it in git history?
│   ├── YES → docs/ai-artifacts/
│   └── NO  → .claude/temp/ or .gemini/temp/
└── NO: Is it session-specific?
    ├── YES → .claude/temp/ or .gemini/temp/
    └── NO  → Consider not storing it
```

### Location Matrix

| Artifact Type | Location | Tracked? | Rationale |
| --- | --- | --- | --- |
| Memory/context | `CLAUDE.md`, `GEMINI.md` | Yes | Core project knowledge |
| Implementation plans | `docs/ai-artifacts/plans/` | Yes | Want to see evolution |
| Exploration reports | `docs/ai-artifacts/explorations/` | Yes | Reference material |
| Session results | `.claude/temp/gemini-results/` | No | Transient |
| Second opinions | `.claude/temp/gemini-results/` | No | Transient |
| Checkpoints | `~/.gemini/history/<hash>/` | No | System-managed |
| Sync state | `.claude/temp/sync-state.json` | No | Internal tracking |

## Gitignore Recommendations

Add to project `.gitignore`:

```gitignore
# AI session artifacts (transient)
.claude/temp/
.gemini/temp/

# System-managed
.gemini/history/

# Keep these tracked:
# CLAUDE.md
# GEMINI.md
# docs/ai-artifacts/
```

## File Naming Conventions

### Timestamped Artifacts

Format: `{type}-{scope}-{timestamp}.md`

```bash
# Exploration reports
exploration-architecture-2025-11-30T12-00-00Z.md
exploration-dependencies-2025-11-30T14-30-00Z.md

# Implementation plans
plan-add-auth-2025-11-30T12-00-00Z.md
plan-refactor-db-2025-11-30T14-30-00Z.md
```

### Session Results

Format: `{operation}-{timestamp}.{json|md}`

```bash
# Raw Gemini results
query-2025-11-30T12-00-00Z.json
analysis-2025-11-30T12-00-00Z.json

# Processed results
analysis-summary-2025-11-30T12-00-00Z.md
```

## Workspace Initialization

### Initialize for Dual-CLI

```bash
# Create directory structure
mkdir -p .claude/temp/gemini-results
mkdir -p .gemini/temp
mkdir -p docs/ai-artifacts/explorations
mkdir -p docs/ai-artifacts/plans

# Create GEMINI.md if not exists
if [ ! -f "GEMINI.md" ]; then
  cat > GEMINI.md << 'EOF'
# GEMINI.md

@CLAUDE.md

## Gemini-Specific Overrides

You are Gemini CLI. You have access to:
- Large context window (exceeds typical LLM limits)
- Interactive PTY shell (vim, git rebase -i)
- Checkpointing with instant rollback
- Policy engine for tool control

When working with this codebase, prioritize bulk analysis
and exploration tasks that benefit from your large context.
EOF
fi

# Update .gitignore
grep -q ".claude/temp/" .gitignore 2>/dev/null || echo ".claude/temp/" >> .gitignore
grep -q ".gemini/temp/" .gitignore 2>/dev/null || echo ".gemini/temp/" >> .gitignore
```

## Artifact Exchange Patterns

### Pattern 1: Claude → Gemini (Context Handoff)

```bash
# Claude prepares context
cat CLAUDE.md relevant-files/* > .claude/temp/context-bundle.txt

# Gemini consumes
cat .claude/temp/context-bundle.txt | gemini "Analyze this context"
```

### Pattern 2: Gemini → Claude (Result Consumption)

```bash
# Gemini produces result
gemini "Explore architecture" --output-format json > .claude/temp/gemini-results/exploration.json

# Claude parses result
cat .claude/temp/gemini-results/exploration.json | jq -r '.response'
```

### Pattern 3: Persistent Artifacts

```bash
# For valuable artifacts that should be tracked
result=$(gemini "Create implementation plan" --output-format json)
echo "$result" | jq -r '.response' > docs/ai-artifacts/plans/plan-feature-$(date -u +%Y-%m-%dT%H-%M-%SZ).md
```

## Cleanup Strategies

### Automatic Cleanup (Session-based)

```bash
# Clean artifacts older than 7 days
find .claude/temp/gemini-results -type f -mtime +7 -delete
find .gemini/temp -type f -mtime +7 -delete
```

### Manual Cleanup

```bash
# Clear all session artifacts
rm -rf .claude/temp/*
rm -rf .gemini/temp/*
```

### Selective Cleanup

```bash
# Keep recent, delete old
find .claude/temp/gemini-results -name "*.json" -mtime +3 -delete
```

## Best Practices

### 1. Single Source of Truth

- `CLAUDE.md` is the authoritative memory file
- `GEMINI.md` imports from `CLAUDE.md` and adds overrides
- Don't duplicate information

### 2. Artifact Lifecycle

- Start in temp directories
- Promote valuable artifacts to `docs/ai-artifacts/`
- Clean up regularly

### 3. Clear Naming

- Use descriptive prefixes (exploration-, plan-, analysis-)
- Include timestamps for ordering
- Use ISO 8601 format (sortable)

### 4. Gitignore Discipline

- Temp directories should always be gitignored
- Memory files should always be tracked
- `docs/ai-artifacts/` should be tracked

## Related Skills

- `gemini-memory-sync` - CLAUDE.md ↔ GEMINI.md synchronization
- `gemini-exploration-patterns` - Exploration output standards
- `gemini-context-bridge` - Legacy context sharing patterns

## Related Commands

- `/sync-context` - Synchronize memory files
- `/gemini-explore` - Generates exploration reports
- `/gemini-plan` - Generates implementation plans

## Test Scenarios

### Scenario 1: Workspace Setup

**Query**: "How do I set up a project for Claude and Gemini collaboration?"
**Expected Behavior**:

- Skill activates on "workspace structure" or "cross-cli"
- Provides directory structure and initialization script
**Success Criteria**: User receives complete workspace setup workflow

### Scenario 2: Artifact Location

**Query**: "Where should I store Gemini exploration results?"
**Expected Behavior**:

- Skill activates on "artifact storage" or "where to store"
- Provides location matrix (tracked vs gitignored)
**Success Criteria**: User receives clear guidance on temp vs persistent storage

### Scenario 3: Cross-CLI Exchange

**Query**: "How do I pass context from Claude to Gemini?"
**Expected Behavior**:

- Skill activates on "artifact exchange" or "shared files"
- Provides context handoff pattern
**Success Criteria**: User receives file-based exchange workflow

## Version History

- v1.1.0 (2025-12-01): Added MANDATORY section, Test Scenarios, Version History
- v1.0.0 (2025-11-25): Initial release
