---
name: requirement-analysis
description: "Use when a user brings a new requirement, feature request, or problem statement that needs to be analyzed, refined, and documented before any implementation begins. This skill guides the full requirements engineering process: stripping away solution bias to find the real need, refining requirements through structured dialogue, producing a formal PRD, and generating BDD acceptance criteria. It should NOT be used for technical design, architecture decisions, or implementation planning."
---

# Requirement Analysis

## Overview

Turn raw user requests into validated, testable requirement specifications through structured collaborative dialogue. The process starts by stripping away solution bias using the 5 Whys method, refines requirements via MoSCoW prioritization, produces a formal PRD, and generates BDD acceptance documents — all before any technical design or implementation begins.

## Scope Boundary

This skill covers the **requirements engineering** phase ONLY:
- **In scope**: Problem discovery, user story creation, requirement refinement, PRD writing, BDD acceptance criteria
- **Out of scope**: Technical design, architecture decisions, technology selection, implementation planning, deployment, operations

If the user attempts to discuss technical solutions during this process, acknowledge the input but redirect focus to the business problem: "That's a valid technical consideration — let's capture it as a constraint, but first confirm the business requirement."

## The Process

### Phase 1: Strip & Analyze — Discover the Real Need

**Goal**: Peel away solution-wrapped requests to reveal the genuine business pain point.

**Triggering signal**: The user's request contains specific technical paths (REST, WebSocket, batch, cron, etc.) or implementation details — this is a Candidate Solution, not a raw requirement.

**Method**: Apply the 5 Whys technique. Read `references/five-whys-method.md` for the complete guide and worked example.

**Execution rules**:
- Ask ONE question per message — never overwhelm with multiple questions
- Prefer multiple-choice format when possible to reduce cognitive load
- When detecting solution-wrapped language, gently redirect: "I notice this describes *how* to solve it — help me understand *what problem* you're facing?"
- Record the discovery from each question before asking the next
- Stop when answers converge to a stable business need

**Phase 1 output**: One or more **User Stories** in standard format:
> As a [role], I want [action], so that [value].

Present all discovered user stories to the user for confirmation before proceeding.

### Phase 2: Refine Requirements — Proposal Document

**Goal**: Turn validated user stories into a structured proposal with prioritized requirements.

**Step 2.1: Scope assessment**
- Determine if the need is **universal** (affects multiple teams/roles) or **specific** (single use case)
- Universal needs → platform-level capability
- Specific needs → targeted solution, consider low-cost alternatives

**Step 2.2: Requirement deep-dive**

For each user story, clarify:
- **Ambiguous terms**: Translate vague language ("real-time", "fast", "all") into measurable criteria
- **Non-functional requirements**: Extract performance, reliability, security constraints with specific thresholds
- **Priority**: Apply MoSCoW classification (Must / Should / Could / Won't)
- **Boundary conditions**: Identify edge cases, conflicts, and resolution rules
- **Open questions**: Record anything requiring stakeholder input

**Step 2.3: Write the Proposal**

Read `references/proposal-template.md` for the document template.

Write the proposal to: `docs/requirements/YYYY-MM-DD-<topic>-proposal.md`

Present the proposal to the user section by section (300-500 words per section), confirming each before moving on.

### Phase 3: PRD Specification

**Goal**: Transform the validated proposal into a formal, testable PRD.

Read `references/prd-template.md` for the document template.

**Execution rules**:
1. Write the PRD based on conversation history and the approved proposal
2. Write to: `docs/requirements/YYYY-MM-DD-<topic>-prd.md`
3. **Cross-check**: Compare every item in the proposal against the PRD — flag any gaps
4. If gaps exist, present them to the user for resolution before proceeding
5. Run the **BDD readiness check** (see checklist below) on every functional requirement

**BDD readiness checklist** — verify each requirement against all 6 dimensions:

| Dimension | Verification Question |
|---|---|
| Input/Output format | Are exact formats specified? (data types, structure, encoding) |
| Error & exception scenarios | Is every failure mode explicitly described? |
| Boundary & priority rules | Are conflict resolution rules defined? |
| State behavior | Is state persistence, isolation, and reset behavior clear? |
| Verifiable granularity | Can each behavior be independently tested with a single expected outcome? |
| Ambiguity check | Are there implicit assumptions different readers could interpret differently? |

Any dimension that fails → go back to the user with a targeted question. Do NOT silently assume defaults.

### Phase 4: BDD Acceptance Documents

**Goal**: Generate machine-parseable BDD acceptance criteria that map 1:1 to PRD requirements.

Read `references/bdd-template.md` for the JSON schema and writing guide.

**Execution rules**:
1. Create directory: `docs/requirements/YYYY-MM-DD-<topic>-bdd/`
2. Generate one JSON file per feature: `<feature-name>.json`
3. Each JSON file follows the schema defined in `references/bdd-template.md`
4. Set all `passes` and `overallPass` to `false` (not yet tested)
5. Cover: normal flows, error flows, boundary conditions for each feature
6. **Cross-check**: Compare every PRD functional requirement against BDD scenarios — ensure complete coverage
7. If coverage gaps found, add missing scenarios
8. Present the coverage mapping to the user for final validation

### Phase 5: Summary Report

After all documents are complete, present a summary to the user:

1. **User Stories** discovered (count and list)
2. **Proposal** file path and key decisions
3. **PRD** file path and requirement count (Must/Should/Could/Won't breakdown)
4. **BDD** directory path, feature count, and total scenario count
5. **Open questions** still unresolved (if any)
6. **Coverage status**: Confirm PRD ↔ BDD alignment is complete

## Key Principles

- **One question at a time** — never overwhelm with multiple questions in one message
- **Multiple choice preferred** — easier to answer than open-ended when possible
- **Separate problem from solution** — requirements describe WHAT, not HOW
- **Measurable over vague** — "response time < 200ms" not "fast"
- **Incremental validation** — present documents section by section, confirm each
- **No silent assumptions** — if ambiguous, ask; never fill in defaults
- **Scope discipline** — redirect technical/implementation discussions back to requirements