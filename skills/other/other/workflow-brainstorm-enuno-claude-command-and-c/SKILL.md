---
name: workflow-brainstorm
description: "Use when you need to turn a vague idea into a confirmed design spec before implementation (new feature/component/behavior change). First check project context, then ask one question at a time, provide 2-3 options with trade-offs, finally output design in segments (~200-300 words each) with confirmation after each. Triggers: brainstorm, clarify idea, design spec, refine concept, requirement clarification."
---

# Brainstorming Ideas Into Designs

## Goal

Transform "vague ideas/requirements" into **actionable designs and specifications**, producing reusable file artifacts (rather than just staying in chat).

> Key requirement: **Ask only one question at a time**. If a topic is complex, break it into multiple rounds of Q&A—don't throw out a checklist all at once.

## Core Process (Must Follow)

### 0) Check Project Context First (Required When Repo Exists)

Before asking questions, quickly check:
- Key documentation: `README.md`, `docs/`, `design-system.md` (if exists)
- Tech stack and constraints: `package.json` / `Cargo.toml` / `pyproject.toml` etc.
- Structure overview: top-level directories, main modules
- Recent changes: `git log -n 10 --oneline` (if it's a git repo)

Output a **very brief** context summary: what you observed + possible constraint points (don't start designing yet).

### 1) Understand the Idea (One Question at a Time)

Goal is to gather the minimum information set (purpose / constraints / success criteria).

Rules:
- Each message asks **1 question** only
- Prefer multiple choice (reduce user's cognitive load), use open questions only when necessary
- Ask direction-determining questions first (goals/success criteria/non-goals), then details

### 2) Explore Solutions (2-3 Options + Trade-offs)

After you understand the requirements:
- Provide 2-3 options (A/B/C)
- Explain trade-offs for each (complexity/risk/iteration speed/long-term cost)
- **Give your recommended option first**, then explain why

### 3) Output Design (200-300 Word Segments + Confirm Each)

When you're confident you understand what needs to be done, start outputting the design spec.

Requirements:
- Output in segments (~200-300 words each)
- Ask for confirmation at the end of each segment: e.g., "Does this look good?"
- Design should at least cover:
  - Architecture and module boundaries
  - Core data flow (input → processing → output)
  - Error handling and edge cases
  - Testing and validation strategy (minimum viable set)

If user disagrees with a segment: go back to questioning/option phase to clarify—don't push forward.

## Artifacts and Persistence (Strongly Recommended)

### Write Design Document

Prefer writing to run directory (artifact-first):
- `run_dir/evidence/YYYY-MM-DD-<topic>-design.md`

If there's no `run_dir` but there is a `repo_root`:
- Create `runs/brainstorm/active/<run_id>/`, and write design to `evidence/`

> Note: Writing files is a write operation; if this is the user's project repo, confirm "should I persist to the project?" before writing.

### Enter Implementation (Optional)

After design is confirmed, ask one question to let user choose next step:
1. Enter implementation directly (recommend `workflow-ship-faster` or `workflow-feature-shipper`)
2. Write implementation plan first (persist as checklist items in `run_dir/tasks.md`, then wait for confirmation)
3. Need research/code reading first (split to `run_dir/evidence/parallel/<task-name>/` and do in parallel)

## Key Principles

- **One question at a time**: Never ask 5 questions in one message
- **Multiple choice preferred**: Help user respond faster and more effectively
- **YAGNI**: Actively remove "not needed yet" features from the design
- **Incremental validation**: Output design in segments, confirm each one
