---
name: vibe-check
version: 0.1.2
description: Audit code for "vibe coding sins" — patterns that indicate AI-generated code was accepted without proper review. Produces a scored report card with fix suggestions.
author: Anvil AI
tags: [code-quality, code-review, ai-audit, vibe-coding, linting, security, python, typescript, javascript, discord, discord-v2]
---

# 🎭 Vibe Check

Audit code for "vibe coding" — AI-generated code accepted without proper human review. Get a scored report card with specific findings and fix suggestions.

## Trigger

Activate when the user mentions any of:
- "vibe check"
- "vibe-check"
- "audit code"
- "code quality"
- "vibe score"
- "check my code"
- "review this code for vibe coding"
- "code review"
- "vibe audit"

## Instructions

### 1. Determine the Target

Ask the user what code to analyze. Accepted inputs:
- **Single file:** `app.py`, `src/utils.ts`
- **Directory:** `src/`, `.`, `my-project/`
- **Git diff:** last N commits, staged changes, or branch comparison

### 2. Run the Analysis

```bash
# Single file or directory
bash "$SKILL_DIR/scripts/vibe-check.sh" TARGET

# With fix suggestions
bash "$SKILL_DIR/scripts/vibe-check.sh" --fix TARGET

# Git diff (last 3 commits)
bash "$SKILL_DIR/scripts/vibe-check.sh" --diff HEAD~3

# Staged changes with fixes
bash "$SKILL_DIR/scripts/vibe-check.sh" --staged --fix

# Save to file
bash "$SKILL_DIR/scripts/vibe-check.sh" --fix --output report.md TARGET
```

### 3. Present the Report

The output is a Markdown report. Present it directly — it's designed to be screenshot-worthy.

### Discord v2 Delivery Mode (OpenClaw v2026.2.14+)

When the conversation is happening in a Discord channel:

- Send a compact summary first (grade, score, file count, top 3 findings), then ask if the user wants the full report.
- Keep the first message under ~1200 characters and avoid wide Markdown tables in the first response.
- If Discord components are available, include quick actions:
  - `Show Top Findings`
  - `Show Fix Suggestions`
  - `Run Diff Mode`
- If components are not available, provide the same follow-ups as a numbered list.
- Prefer short follow-up chunks (<=15 lines per message) when sending the full report.

### Quick Reference

| Command | Description |
|---------|-------------|
| `vibe-check FILE` | Analyze a single file |
| `vibe-check DIR` | Scan directory recursively |
| `vibe-check --diff` | Check last commit's changes |
| `vibe-check --diff HEAD~5` | Check last 5 commits |
| `vibe-check --staged` | Check staged changes |
| `vibe-check --fix DIR` | Include fix suggestions |
| `vibe-check --output report.md DIR` | Save report to file |

### Sin Categories (what it checks)

| Category | Weight | What It Catches |
|----------|:------:|-----------------|
| Error Handling | 20% | Missing try/catch, bare exceptions, no edge cases |
| Input Validation | 15% | No type checks, no bounds checks, trusting all input |
| Duplication | 15% | Copy-pasted logic, DRY violations |
| Dead Code | 10% | Unused imports, commented-out blocks, unreachable code |
| Magic Values | 10% | Hardcoded strings/numbers/URLs without constants |
| Test Coverage | 10% | No test files, no test patterns, no assertions |
| Naming Quality | 10% | Vague names (data, result, temp, x), misleading names |
| Security | 10% | eval(), exec(), hardcoded secrets, SQL injection |

### Scoring

- **A (90-100):** Pristine code, minimal issues
- **B (80-89):** Clean code with minor issues  
- **C (70-79):** Decent but lazy patterns crept in
- **D (60-69):** Needs human attention
- **F (<60):** Heavy vibe coding detected

### Notes for the Agent

- **The report is the star.** Present it in full — it's designed to look great.
- After presenting, offer to run `--fix` mode if they didn't already.
- Suggest the README badge: `![Vibe Score](https://img.shields.io/badge/vibe--score-XX%2F100-COLOR)`
- For large codebases, suggest focusing on specific directories or using `--diff` mode.
- If no LLM API key is set, the tool falls back to heuristic analysis (less accurate but still useful).
- **Supported languages (v1):** Python, TypeScript, JavaScript only.

## References

- `scripts/vibe-check.sh` — Main entry point
- `scripts/analyze.sh` — LLM code analysis engine (with heuristic fallback)
- `scripts/git-diff.sh` — Git diff file extractor
- `scripts/report.sh` — Markdown report generator
- `scripts/common.sh` — Shared utilities and constants

## Examples

### Example 1: Audit a Directory

**User:** "Vibe check my src directory"

**Agent runs:**
```bash
bash "$SKILL_DIR/scripts/vibe-check.sh" src/
```

**Output:** Full scorecard with per-file breakdown, category scores, and top findings.

### Example 2: Check with Fixes

**User:** "Review this code for vibe coding and suggest fixes"

**Agent runs:**
```bash
bash "$SKILL_DIR/scripts/vibe-check.sh" --fix src/
```

**Output:** Scorecard + unified diff patches for each finding.

### Example 3: Git Diff Mode

**User:** "Check the code quality of my last 3 commits"

**Agent runs:**
```bash
bash "$SKILL_DIR/scripts/vibe-check.sh" --diff HEAD~3
```

**Output:** Scorecard focused only on recently changed files.
