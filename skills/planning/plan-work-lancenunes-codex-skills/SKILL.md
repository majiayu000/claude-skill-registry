---
name: plan-work
description: "Plan work before coding: do repo research, analyze options/risks, and ask clarifying questions before proposing an implementation plan. Use when the user asks for a plan, design/approach, scope breakdown, or implementation steps."
---

# Plan work

## Goal
Produce a plan that is:
- grounded in repo reality (research)
- explicit about decisions and risks (analysis)
- blocked on zero unknowns (Q&A before implementation steps)

## Inputs to ask for (if missing)
- Outcome/acceptance criteria (what "done" means).
- Constraints: time, backwards compatibility, performance, security, data migration.
- Target environment(s): local/stage/prod; any feature flags or rollout requirements.
- Non-goals (what not to do).

## Workflow (research -> analysis -> Q&A -> implementation)
1) Research (current state)
   - Read repo guidance first: `AGENTS.md`, `README.md`, `docs/` (only if needed).
   - Identify entrypoints and owners (backend/frontend/infra).
   - Find relevant code paths and patterns:
     - `rg` for symbols, endpoints, config keys, error strings
     - `git log -p` / `git blame` for history and intent when uncertain
   - If the plan depends on external behavior (framework/library/tooling), consult official docs, release notes or context7 (and call out versions/assumptions).
   - Capture findings as short bullets with file paths.
2) Analysis (what to change and why)
   - Restate requirements and assumptions.
   - List options (1-3) with tradeoffs; pick one and justify.
   - Identify risks/edge cases and what tests cover them.
   - Collect open questions.
3) Q&A gate (do not skip)
   - If there are open questions, ask them and stop.
   - Do not propose implementation steps until the user answers (or explicitly accepts assumptions).
   - First pass: ask 1-5 questions that eliminate whole branches of work.
   - Do not limit yourself to just 1-5 questions overall; continue asking until everything needed for a proper implementation plan is clarified.
   - Make questions scannable: numbered, short, multiple-choice when possible.
   - Include defaults/recommendations and a fast-path response (e.g., reply "defaults").
     - Do not label any option as the default within the option list; if needed, state defaults in a separate note.
   - Provide a low-friction "not sure" option when helpful.
   - You may add brief bracketed insights after options when there's a major upside or downside.
   - Separate "Need to know" from "Nice to know" when it reduces friction.
   - Structure options for compact replies (e.g., "1b 2a 3c") and restate selections in plain language.
   - Pause before acting until must-have answers arrive:
     - Do not run commands, edit files, or produce a plan that depends on unknowns.
     - Low-risk discovery is allowed if it does not commit to a direction (read-only, non-committing).
   - After answers, restate requirements in 1-3 sentences (constraints + success criteria), then proceed.
4) Implementation plan (only after Q&A)
   - Break into small steps in a sensible order.
   - Name likely files/dirs to change.
   - Include the tests to run (unit/integration/build) to validate the change.  
   - If the change spans modules, include coordination steps (contract changes, client regen, versioning).

## Q&A template (short, feature plan)
Before I start, I need: (1) question (2) question (3) question.
This is a starting set; I will continue with follow-up questions until everything needed for a proper implementation plan is clarified.

Need to know
1) 
   a) 
   b) 
   c) 
2) 
   a) 
   b) 
   c) 
3) C
   a) 
   b) 
   c) 
   d) 

Nice to know
4) 
   a) 
   b) 
   c) 

Reply with: "1a 2b 3c 4a" (or "propose" to have me choose and confirm).

## Deliverable
Use `references/plan-template.md` and fill it in.
