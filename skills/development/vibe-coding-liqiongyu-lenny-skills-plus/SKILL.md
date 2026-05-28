---
name: "vibe-coding"
description: "Turn an idea into a functional, demo-ready prototype using AI-assisted “vibe coding” (timeboxed build loop, prompt pack, build plan, demo script, and safety checks). Use for rapid prototyping and proving concepts in AI & Technology."
---

# Vibe Coding

## Scope

**Covers**
- Timeboxed, AI-assisted rapid prototyping (“vibe coding”) to produce a functional demo (not slides)
- Turning a rough idea into a buildable prototype spec + task board + prompt pack
- A tight iteration loop: generate → run → verify → adjust → log decisions
- “Build tools to build the thing” when it meaningfully speeds up the demo (timeboxed)
- Safe use of coding agents: least privilege, no secrets, small diffs, validation, rollback

**When to use**
- “Vibe code a working prototype we can demo in 30–90 minutes.”
- “Replace this Figma concept with a clickable prototype.”
- “I’m not an engineer—help me build a small app/tool with AI and ship a demo.”
- “Turn this AI feature idea into a proof-of-concept with a clear build loop and demo script.”

**When NOT to use**
- You need a production-grade system, hardening, scaling, or security review (use `building-with-llms` + engineering process).
- You need upstream problem framing, strategy, or PRD-level alignment (use `problem-definition`, `writing-prds`).
- The work is high-stakes/irreversible (payments, auth, medical, legal, safety-critical) without human owners and reviews.
- The request is “build anything” with no demo target; do intake first and narrow to one scenario.

## Inputs

**Minimum required**
- Prototype goal: what should a user be able to do in the demo (1–3 “happy path” tasks)
- Target user + context (who uses it, where it fits)
- Timebox (e.g., 30/60/90 minutes) + demo audience (internal, customer, exec)
- Platform preference (web app, mobile, CLI, spreadsheet, etc.) and constraints (privacy, data sensitivity)
- Data/integrations: mock data ok? any APIs needed? (default to mock)

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md) (3–5 at a time).
- If details remain missing, proceed with explicit assumptions and offer 2–3 options (e.g., mock vs real data; simple UI vs polished).
- If asked to run commands or write/modify files, request confirmation, keep changes in a dedicated folder, and include rollback guidance.

## Outputs (deliverables)

Produce a **Vibe Coding Prototype Pack** (in chat; or as files if requested), in this order:

1) **Vibe Coding Brief** (goal, demo scenario, non-goals, constraints, timebox)
2) **Prototype Spec** (user flow, screens/components, data model, acceptance criteria, “fake vs real” decisions)
3) **Prompt Pack** (copy/paste prompts to drive the coding agent safely and efficiently)
4) **Build Plan + Task Board** (vertical slices with checks/tests per slice)
5) **Demo Script + Runbook** (how to run, how to demo, what to say, what to avoid)
6) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)

## Workflow (7 steps)

### 1) Pick a single demo outcome (kill ambiguity fast)
- **Inputs:** Initial idea, timebox, target audience.
- **Actions:** Write a one-sentence demo promise (“In 60 minutes we will demo…”) + 3–5 non-goals. Choose one “hero” scenario and what can be faked.
- **Outputs:** Draft **Vibe Coding Brief**.
- **Checks:** The demo promise is specific, observable, and fits the timebox.

### 2) Define the prototype’s contract (what exists, what’s mocked)
- **Inputs:** Demo scenario, platform preference, constraints.
- **Actions:** Specify the minimum user flow, screens/components, and data shape. Decide: mock data vs real data; stub integrations vs live.
- **Outputs:** Draft **Prototype Spec**.
- **Checks:** Acceptance criteria exist for each user-visible step; “fake vs real” is explicit.

### 3) Set the build loop + guardrails (how we’ll vibe code safely)
- **Inputs:** Repo/app context (if any), constraints, desired stack.
- **Actions:** Create a **Prompt Pack** that forces: small diffs, clear file list, run instructions, and “ask before risky actions.” Create a task board of 3–8 vertical slices.
- **Outputs:** **Prompt Pack** + **Build Plan + Task Board**.
- **Checks:** Every slice has a Definition of Done and a quick validation method (manual steps or tests).

### 4) Scaffold the thinnest runnable slice (end-to-end)
- **Inputs:** Prompt pack, chosen platform/stack, prototype spec.
- **Actions:** Generate a minimal skeleton that runs. Implement the hero path with mock data. Capture run commands and known limitations.
- **Outputs:** Runnable prototype + run notes (for the runbook).
- **Checks:** A fresh user can run it in ≤ 5 minutes; the hero path is demonstrable.

### 5) Iterate in vertical slices (generate → run → verify → log)
- **Inputs:** Task board, working prototype.
- **Actions:** For each slice: request a plan + diff, apply changes, run, verify against acceptance criteria, and record decisions/bugs. Avoid broad refactors; prefer incremental improvements.
- **Outputs:** Updated prototype + iteration notes.
- **Checks:** Each slice ends with a user-visible improvement and a validated run.

### 6) Optional: build a tool to build the thing (timeboxed)
- **Inputs:** Repeated friction (editing, generating, transforming content).
- **Actions:** If it reduces time-to-demo, vibe code a tiny helper tool (editor, generator, script) and immediately use it to advance the prototype.
- **Outputs:** Helper tool + note on how it accelerates the workflow.
- **Checks:** The helper tool saves time within the current timebox; otherwise cut it.

### 7) Package the demo + quality gate + handoff
- **Inputs:** Prototype + all draft artifacts.
- **Actions:** Write the demo script + runbook. Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Finalize **Risks / Open questions / Next steps**.
- **Outputs:** Final **Vibe Coding Prototype Pack**.
- **Checks:** A stakeholder can demo it without you; risks and next steps are explicit and owned.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (30–60 min prototype):** “Use `vibe-coding` to build a demo-ready web prototype of an ‘AI meeting notes → action items’ tool. Mock the LLM output. Output the full Vibe Coding Prototype Pack.”  
Expected: brief + spec + prompt pack + task board + demo script; prototype plan defaults to mock data and a single hero flow.

**Example 2 (non-engineer builder):** “I’m a PM. Use `vibe-coding` to help me create a clickable prototype of an onboarding checklist app in 45 minutes. I need a demo script for my team.”  
Expected: tight scope, fake data, vertical slices, and a runbook optimized for demo reliability.

**Boundary example:** “Vibe code a production payments backend and deploy it.”  
Response: out of scope; propose a prototype-only approach (mock payments), identify required security/engineering owners, and recommend a separate production plan.

