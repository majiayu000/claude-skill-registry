---
name: spec-driven-collaboration
description: >
  Generate self-contained collaboration documents for sharing issues with external AI
  systems (Gemini, ChatGPT, etc.) with structural anti-skip enforcement
  (Execute-Verify-Record pattern at every step). Interactively gathers context, reads
  actual code files, loads constitutional constraints, and produces a complete 10-section
  package ready to paste into the target LLM. Use when the user wants to collaborate with
  another AI, share an issue for joint problem-solving, get a fresh perspective from a peer
  LLM, or needs help from an external AI that doesn't have access to the codebase. Make sure
  to use this skill whenever the user mentions cross-AI collaboration, sharing issues with
  Gemini/ChatGPT/Copilot, peer review from another AI, or wants a second opinion from
  an external LLM.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
model: opus
effort: High
---

# Spec-Driven Collaboration

Generate a self-contained collaboration document that packages an issue with actual code, constitutional constraints, analysis, and targeted questions for an external AI to review.

**Constitution files are THE LAW:** tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md

**If ambiguous or conflicts detected: HALT and use AskUserQuestion**

---

## Execution Model

This skill expands inline. After invocation, execute Phase 01 immediately. Do not wait passively, ask permission, or offer execution options.

**Self-Check (if ANY box is true = VIOLATION):**

- [ ] Stopping to ask about token budget
- [ ] Stopping to offer execution options
- [ ] Waiting passively after skill invocation
- [ ] Asking "should I execute this?"
- [ ] Skipping a phase because it "seems simple"
- [ ] Combining multiple phases into one
- [ ] Summarizing instead of loading a reference file
- [ ] Skipping verification because "I already wrote the file"

**IF any box checked:** EXECUTION MODEL VIOLATION. Go directly to Phase 01 now.

---

## Anti-Skip Enforcement Contract

This skill enforces structural anti-skip at every step using the Execute-Verify-Record pattern. Every mandatory step in every phase has three parts:

- **EXECUTE:** The exact action to perform (Read, Write, AskUserQuestion, Glob, Grep)
- **VERIFY:** How to confirm the action happened (file exists, content matches, count correct)
- **RECORD:** Confirmation that the step completed successfully

**Token Optimization Bias is PROHIBITED.** Do not skip, compress, or shortcut any step. Every phase step exists because a previous failure proved it necessary.

Prohibited rationalizations:
- "The template is simple enough to populate from memory" — Load the template file fresh.
- "I already read the constitution files" — Read them again in Phase 02.
- "The document is short, no need to verify" — Read it back to verify in Phase 05.
- "Phase 06 is just a display, I can skip it" — Execute it fully.
- "I can combine Phases 04 and 05" — Execute them separately, in order.

---

## Parameter Extraction

Extract parameters from conversation context set by the `/collaborate` command:

| Context Marker | Set By | Description |
|----------------|--------|-------------|
| `ISSUE_DESCRIPTION` | /collaborate | Issue description from user argument or AskUserQuestion |
| `TARGET_AI` | /collaborate | Target AI platform (default: "Gemini") |

**Extraction Method:**
1. Search conversation for `**Issue Description:**` marker → `ISSUE_DESCRIPTION`
2. Search conversation for `**Target AI:**` marker → `TARGET_AI`
3. If markers not found, search for natural language context about the issue
4. If still not found: AskUserQuestion to gather missing parameters

---

## Phase Table

| Phase | Name | File | Steps | Key Tools |
|-------|------|------|-------|-----------|
| 01 | Context Gathering | `phases/phase-01-context-gathering.md` | 4 | AskUserQuestion, Glob, Grep |
| 02 | Constitution Loading | `phases/phase-02-constitution-loading.md` | 3 | Read (×6 parallel) |
| 03 | Code Collection | `phases/phase-03-code-collection.md` | 4 | Read, Glob, Grep |
| 04 | Analysis & Template Population | `phases/phase-04-analysis-template.md` | 4 | Read |
| 05 | Document Generation | `phases/phase-05-document-generation.md` | 3 | Write, Read |
| 06 | Completion Report | `phases/phase-06-completion-report.md` | 2 | Display |

---

## Phase Orchestration Loop

```
FOR phase_num in [01, 02, 03, 04, 05, 06]:

    1. LOAD: Read(file_path="src/claude/skills/spec-driven-collaboration/phases/{phase_file}")
       Do NOT rely on memory of previous reads. Load the phase file FRESH.

    2. EXECUTE: Follow every step in the phase file (EXECUTE-VERIFY-RECORD triplets)
       - Each step's EXECUTE instruction tells you exactly what to do
       - Each step's VERIFY instruction tells you how to confirm it happened
       - Each step's RECORD instruction confirms completion

    3. GATE: Verify all gate conditions before proceeding to next phase
       IF any gate condition fails: HALT
```

**Critical:** Load each phase file fresh using Read(). Do not execute phases from memory.

---

## Success Criteria

- [ ] All 6 phases executed in sequence
- [ ] ISSUE_DESCRIPTION and TARGET_AI extracted
- [ ] AFFECTED_FILES identified (≥1 file)
- [ ] All 6 constitution files loaded and constraints extracted
- [ ] All affected files read with actual code captured
- [ ] Template loaded fresh from reference file
- [ ] All 10 sections populated (no empty sections, no placeholders)
- [ ] Document written to `tmp/collaborate-{target}-{slug}-{date}.md`
- [ ] Document verified by read-back (≥100 lines, all 10 section headers present)
- [ ] Completion report displayed to user

---

## Reference Files

| File | Purpose | Loaded In |
|------|---------|-----------|
| `references/collaboration-prompt-template.md` | 10-section output document template | Phase 04 |
| `references/context-gathering-guide.md` | Interactive context gathering patterns | Phase 01 |
| `references/code-collection-patterns.md` | File discovery, test finding, error capture | Phase 03 |
| `references/analysis-reasoning-guide.md` | Hypothesis ranking, constraint analysis, question crafting | Phase 04 |

---

## Error Handling

| Error | Phase | Resolution |
|-------|-------|------------|
| No issue description from command | 01 | AskUserQuestion for description |
| Affected file not found | 03 | Warn user, skip file, continue |
| Constitution file missing | 02 | HALT — constitution files are required |
| Template reference missing | 04 | HALT — verify skill installation |
| `tmp/` directory missing | 05 | Create it, then write |
| Write fails | 05 | Report error path, suggest manual creation |
| Document verification fails | 05 | HALT — re-examine document content |
