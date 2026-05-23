---
name: cook-auto-parallel
description: "[Implementation] ⚡⚡⚡ Plan parallel phases & execute with fullstack-developer agents"
argument-hint: [tasks]
infer: true
---

**Ultrathink parallel** to implement: <tasks>$ARGUMENTS</tasks>

**IMPORTANT:** Activate needed skills. Ensure token efficiency. Sacrifice grammar for concision.

## ⚠️ Anti-Hallucination Reminder

**Before modifying ANY code:** Verify assumptions with actual code evidence. Search for usages, read implementations, trace dependencies. If confidence < 90% on any change, investigate first or ask user. See `.claude/skills/shared/anti-hallucination-protocol.md` for full protocol.

## Workflow

### 1. Research (Optional)
- Use max 2 `researcher` agents in parallel if tasks complex
- Use `/scout-ext` to search codebase
- Keep reports ≤150 lines

### 2. Parallel Planning
- Trigger `/plan-hard --parallel <detailed-instruction>`
- Wait for plan with dependency graph, execution strategy, file ownership matrix

### 3. Parallel Implementation
- Read `plan.md` for dependency graph
- Launch multiple `fullstack-developer` agents in PARALLEL for concurrent phases
  - Example: "Phases 1-3 parallel" → launch 3 agents simultaneously
  - Pass phase file path: `{plan-dir}/phase-XX-*.md`
  - Include environment info
- Wait for all parallel phases complete before dependent phases
- Sequential phases: launch one agent at a time

### 4. Testing
- Use `tester` subagent for full test suite
- NO fake data/mocks/cheats
- If fail: use `debugger`, fix, repeat

### 5. Code Review
- Use `code-reviewer` for all changes
- If critical issues: fix, retest

### 6. Project Management & Docs
- If approved: use `project-manager` + `docs-manager` in parallel
- Update plan files, docs, roadmap
- If rejected: fix and repeat

### 7. Final Report
- Summary of all parallel phases
- Guide to get started
- Ask to commit (use `git-manager` if yes)

**Example:** Phases 1-3 parallel → Launch 3 fullstack-developer agents → Wait → Phase 4 sequential

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
