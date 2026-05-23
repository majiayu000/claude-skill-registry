---
name: spec-driven-workflow
description: SPEC-First planning workflow - explore codebase, gather requirements, create execution plan through dialogue (read-only)
---

# SKILL: Spec-Driven Workflow (Planning)

> **Purpose**: Analyze codebase and create SPEC-First execution plan through dialogue (read-only phase)
> **Target**: Planner Agent executing /00_plan command

---

## Quick Start

### When to Use This Skill
- Create new implementation plan
- Explore codebase for task requirements
- Gather user requirements through dialogue

### Quick Reference
```bash
# Invoked by: /00_plan "task description"
# Output: Complete plan in .pilot/plan/draft/ + user decision
```

---

## Core Philosophy

**Read-Only**: NO code modifications, only exploration/analysis/planning | **SPEC-First**: Requirements before implementation | **Efficient Dialogue**: Ask user only for business/intent; handle technical details autonomously or via GPT

## What This Skill Covers

**In Scope**: Codebase exploration (parallel agents), requirement gathering, SPEC-First plan (PRP framework), decision tracking, dialogue with question filtering
**Out of Scope**: Implementation → execute-plan/SKILL.md | Confirmation → confirm-plan/SKILL.md

---

## EXECUTION DIRECTIVE

**DIALOGUE PHASE - NOT EXECUTION**: ASK only when necessary (filter first) | WAIT for response | NEVER auto-execute /01_confirm or /02_execute | Selection ≠ Execution (user chooses approach → continue planning, NOT implement)

---

## Question Filtering (CRITICAL)

**Self-Decide** (do NOT ask): Technical details (file naming, folder structure), obvious patterns, standard practices, minor trade-offs
**Consult GPT First**: Architecture decisions, security, complex trade-offs (use gpt-delegation skill → "read-only" mode)
**MUST Consult GPT**: Architecture keywords OR confidence < 0.5 → MUST consult before AskUserQuestion (REFERENCE.md, gpt-delegation/SKILL.md)
**Ask User ONLY**: Business requirements, direction choices (2+ genuinely different outcomes), scope clarification, user intent ambiguity

---

## Execution Steps

## ⛔ MAIN ORCHESTRATOR RESTRICTIONS

**FORBIDDEN**: Direct codebase exploration (use explorer/researcher agents via Task tool), direct gate resolution without delegation
**MANDATORY**: Step 1 exploration (parallel agents), Step 1.9/1.10 gap investigation (agents before user), GPT via gpt-delegation
**EXCEPTIONS**: Keyword detection, pattern matching, draft file creation, question filtering
**WHY**: Subagent isolation = 50-80% context savings (CLAUDE.md:58-59)

---

### Step 0: Initialize Progress Tracking
Create TaskCreate entry for planning phase (TaskCreate analyzing - marks /00_plan start).

### Step 1: Explore Codebase
Launch explorer + researcher in parallel for comprehensive discovery.

### Step 1.5: Scope Clarity Check
**Triggers**: Completeness keywords, reference-based requests, ambiguous scope, multi-layer arch. **Action**: Ask user to select scope. **Details**: REFERENCE.md

### Step 1.6: Design Direction Check
**Triggers**: landing, marketing, redesign, beautiful, modern, premium, hero, pricing. **Action**: Ask aesthetic direction or use defaults. **Details**: REFERENCE.md

### Step 1.8: External Context Detection
**Triggers**: "Like X", external links, "Use API/library", refactor refs. **Action**: Capture context, create Context Pack. **Details**: REFERENCE.md

### Step 1.8.5: Context Manifest
Generate Manifest with Collected/Related/Missing Context tables. **Details**: REFERENCE.md

### Step 1.9: Absolute Certainty Gate
**Checklist**: Codebase understanding, Dependencies, Impact, Test strategy, Edge cases, Rollback. **Loop**: Max 30min. **Blocking**: Escalate to user. **Details**: REFERENCE.md

### Step 1.10: Readiness Gate
**Checklist**: Unknowns Enumerated, Assumptions Verified, Dependencies Clear, Criteria Measurable, Verification Plan, Rollback Plan. **Loop**: Max 3 retries. **Blocking**: Incomplete after MAX_RETRIES. **Details**: REFERENCE.md

### Step 2: Gather Requirements
Create User Requirements table (ID, Timestamp, User Input Original, Summary).

### Step 3: Create SPEC-First Plan
**PRP**: What (Functionality), Why (Context), How (Approach), Success Criteria. **Approach Selection**: One clear → present directly; multiple → ask user; technical → consult GPT.

### Step 3.5: Mandatory Oracle Consultation
GPT at 3 points: start (Analyst), mid (Architect), end (Reviewer). Fallback: WebSearch/Context7. **Details**: REFERENCE.md

### Step 4: Final User Decision
**NEVER auto-proceed to /01_confirm or /02_execute.** Ask user: A) Continue editing, B) Explore different, C) Run /01_confirm, D) Run /02_execute

---

## Core Concepts

### Context Pack
Goal, Inputs (Embedded), Derived Requirements, Assumptions & Unknowns, Traceability Map. **Details**: REFERENCE.md

### Decision Tracking
Draft file: User Requirements table, Decisions Log, Success Criteria with checkboxes. **Details**: REFERENCE.md

### Atomic SC Principle
"One SC = One File OR One Concern" - enables parallel execution, clear ownership. **Details**: REFERENCE.md

### Selection vs Execution
**When user says "Go with B"**: ✅ Continue planning (refine plan) | ❌ Start implementing. **Implementation**: Only when user runs `/01_confirm` → `/02_execute`. **Details**: REFERENCE.md

### Operational Certainty

**Binary**: **Verified** (with evidence) OR **Cannot Verify** (with artifact). **Evidence**: Code ref (file+lines), Test output (cmd+results), GPT log (ID+summary), User confirm (timestamp+response). **Cannot Verify**: Create artifact (what, why, needs) + notify user. **Details**: REFERENCE.md

### False Certainty Anti-Patterns

**BLOCKED Phrases** (never declare certainty with):

| Anti-Pattern | Example | Remedy |
|--------------|---------|--------|
| Vague language | "I think", "probably" | Use "Verified" OR "Cannot Verify" |
| Uncited claims | "Tests will pass" (no run) | Run command, cite output |
| Assumption as fact | "File exists" (not checked) | Verify with Read/Glob, cite result |
| Missing verification | "Pattern found" (no grep) | Execute verification, show output |
| Skipped exploration | "Didn't check X but confident" | Mark "Cannot Verify", create artifact |
| Implicit unknowns | Proceed without stating gaps | Enumerate unknowns explicitly |

**Enforcement**: Certainty Gate (Step 1.9) blocks if any anti-pattern detected. **Details**: REFERENCE.md

---

## PROHIBITED Actions

**Edit tool**: FORBIDDEN | **Write tool**: ONLY `.pilot/plan/draft/*.md` | **Plan files**: No creation without approval | **Auto-execute**: No /01_confirm or /02_execute | **Implementation**: Not after user selects approach | **Natural language**: Never triggers phase transition
**EXPLICIT COMMAND REQUIRED**: User must type `/01_confirm` or `/02_execute` to move phases.

---

## Further Reading

**Internal**: @.claude/skills/spec-driven-workflow/REFERENCE.md - Advanced planning patterns, detailed step implementation, context pack formats, decision tracking examples | @.claude/skills/parallel-subagents/SKILL.md - Parallel agent execution | @.claude/skills/gpt-delegation/SKILL.md - GPT consultation | @.claude/skills/confirm-plan/SKILL.md - Plan confirmation | @.claude/skills/execute-plan/SKILL.md - Plan execution

**External**: [SPEC-First Development](https://en.wikipedia.org/wiki/Specification_by_example) | [PRP Framework](https://pragprog.com/)

---

**⚠️ CRITICAL**: /00_plan is **read-only** - NO code modifications. **Filter questions**: Self-decide technical details, consult GPT for complex trade-offs, ask user only for business/intent. **Selection ≠ Execution**: When user chooses approach → continue planning, NOT implement. Implementation starts ONLY when user explicitly runs `/01_confirm` → `/02_execute`.

---

**Version**: claude-pilot 4.4.40
