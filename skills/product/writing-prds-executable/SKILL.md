---
name: writing-prds-executable
description: >
  Draft, critique, or rewrite PRDs (product requirements / product specs) and adjacent artifacts (PR/FAQ,
  acceptance criteria, rollout plan). For AI/LLM features, also draft eval specs (LLM-as-judge) and prompt sets.
  Output must be in English. Use when the user asks for a PRD/spec/requirements/PRFAQ/evals/prompt sets,
  or needs help clarifying scope, success metrics, non-goals, user stories, or stakeholder alignment.
metadata:
  version: "1.0.0"
  language: "en"
allowed-tools: "Read,Write,Edit"
---

# Writing PRDs (Executable)

This skill turns messy ideas into **shippable artifacts**:
1) PR/FAQ (customer-first narrative)
2) PRD (scope + requirements + success metrics)
3) AI Eval Spec (requirements as executable evals) — AI only
4) Prompt Set / Prototype plan — AI only

Keep outputs crisp, concrete, and copy‑pasteable. Prefer bullets, tables, and numbered requirements over long prose.

## When to use

Use this skill when the user requests:
- a PRD / product requirements / product spec / requirements doc
- a PR/FAQ or “working backwards” narrative
- acceptance criteria, rollout plan, risks, dependencies
- AI/LLM behavior requirements, evals, judge rubric, prompt sets

## When NOT to use (redirect)

Do NOT use this skill as a substitute for:
- Company strategy / vision (use a vision/strategy skill)
- Roadmap prioritization across many initiatives (use prioritization/roadmap skill)
- Pure UX copywriting or marketing launch copy (use messaging/launch skills)

If legal/privacy/security constraints are material but unknown, first ask for constraints and the approval process.

## Quick decision: which artifact(s) to produce

If the user doesn’t specify, choose the minimal artifact that unlocks the next decision:

- Early / unclear idea → **PR/FAQ** first, then a lightweight PRD outline.
- Clear direction, need alignment / build plan → **PRD**.
- AI/LLM feature → **PRD + Eval Spec + Prompt Set** (required).
- “Improve this existing PRD/spec” → rewrite + gaps + open questions.

Templates:
- PRD: `assets/PRD_TEMPLATE.md`
- PR/FAQ: `assets/PRFAQ_TEMPLATE.md`
- Eval Spec: `assets/EVAL_SPEC_TEMPLATE.md`
- Prompt Set: `assets/PROMPT_SET_TEMPLATE.md`

Quality checks:
- Checklist: `references/QUALITY_CHECKLIST.md`
- Rubric: `references/QUALITY_RUBRIC.md`
- Question bank: `references/QUESTION_BANK.md`

## Intake: ask only what you must

Ask at most **5** high-leverage questions at a time (use `references/QUESTION_BANK.md`).
If the user can’t answer, proceed with explicit assumptions.

Minimum inputs to proceed:
1) Product/feature name + target user
2) Problem statement (what pain / why now)
3) Success metric(s) or a proxy
4) Constraints (time, platform, legal, data, dependencies)
5) Audience for the doc (exec decision? eng build? cross-functional alignment?)

## Output contract (always include)

Always include:
- Version + date + owner (or “TBD”)
- Goals and non-goals
- Requirements as numbered bullets (R1, R2…)
- Clear “Out of scope”
- Open questions (with owner / next step)

When producing multiple artifacts, output in this order:
1) PR/FAQ → 2) PRD → 3) Eval Spec → 4) Prompt Set

## Workflow A: Draft a PR/FAQ (customer-first)

Use when the idea is early or benefits are fuzzy.

1) Write the press release in external-facing, factual language.
2) Add FAQs for: customer, internal stakeholders, technical/ops, risks.
3) Include a hypothetical launch date (forces planning).
4) Extract “claims” from the PR (what must be true) → convert to requirements.

## Workflow B: Draft or rewrite a PRD (shippable requirements)

1) Start with a 5–10 line narrative (why this matters, for whom).
2) Define scope boundaries: goals, non-goals, assumptions.
3) Define users + key journeys (happy path + edge cases).
4) Translate into requirements:
   - Functional requirements (R1…)
   - Non-functional requirements (performance, reliability, accessibility, privacy)
5) Define success metrics + instrumentation.
6) Rollout plan + risks + mitigations.
7) End with open questions + decision log.

## Workflow C (AI only): Requirements as executable evals

Goal: make requirements testable.

1) List non‑negotiable behaviors (MUST / MUST‑NOT).
2) Build a test set: golden, adversarial, regression.
3) Write an LLM‑as‑judge rubric (scale + definitions + pass threshold).
4) Connect evals to shipping gates (pre‑launch + post‑launch monitoring).

## Workflow D (AI only): Prompt set + prototype plan

1) Provide a small prompt set that exercises core use cases + edge cases.
2) Specify expected outputs and guardrails.
3) Propose a minimal prototype plan if useful (what to mock vs build).

## Quality bar (before finalizing)

Run:
- `references/QUALITY_CHECKLIST.md`
- `references/QUALITY_RUBRIC.md`

Also include a brief circulation plan: who should review (Eng, Design, Data, Support, Marketing, Legal) and what feedback you need from each.

## Confidentiality

Treat user-provided information as confidential. Do not include secrets in outputs. If something looks sensitive, redact or replace with placeholders.
