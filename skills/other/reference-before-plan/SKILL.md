---
name: reference-before-plan
description: Research references before creating a Prime Agent plan. Use when repo-change planning needs downloaded projects, articles, papers, docs, per-reference analysis, adoption questions, language settings, and reviewer or criticizer subagents; exclude direct implementation-only, factual/explanation, trivial command-only, or explicit no-plan requests.
---

# Reference Before Plan

Use this skill when external references must shape the plan before implementation.

## Setup

1. Read `../_shared/references/prime-planning-workflow.md`, `../_shared/references/state-and-config.md`, and `../_shared/references/plan-artifact-template.md`.
2. Initialize state with `python3 scripts/optim_plans.py init --repo <target-repo> --topic <topic> --plan-level reference-before-plan --request-text <original-request>`.
3. Use `.git/optim-plans` for controller state and `docs/optim-plans/YYYY-MM-DD-topic/` for public artifacts.

## Required Reference Flow

1. Inspect the target Git repo read-only before external research so search terms match the actual codebase.
2. Search proactively for related projects, articles, papers, docs, and prior art.
3. Download or clone at least 3 credible references before writing `PLAN_v1.md`. Store large downloads outside the target repo by default under `~/.cache/optim-plans/refs/<repo-slug>/<topic>/`.
4. Record source metadata with `record-reference`: title, URL, kind, retrieval method, access date, local path, coverage, and evidence gaps.
5. For every reference, produce a structured analysis artifact and record it with `record-reference-analysis`. If a richer parser is unavailable, do a manual structured read and record any waiver with `record-reference-waiver`.
6. For every reference after analysis, ask at least 3 ref-specific adoption questions before using its ideas in `PLAN_v1.md`. Each question must be based on downloaded content, put the recommended option first, put `Other` second-last, and put `Auto-complete` last.
7. Block rather than pad if fewer than 3 credible references exist, unless the user explicitly narrows the topic or grants a waiver. `Auto-complete` cannot grant this waiver.
8. Continue with big-plan depth: at least 10 planning questions, required web research during brainstorming and refinement, no refinement limit, and at most five high-priority comments or questions per refinement round.

## REF_ANALYSIS.md

Include original request, repo evidence, attempted queries, selection criteria, selected and rejected references, local paths, structured analysis paths, adoption questions and answers, accepted ideas, rejected ideas, evidence gaps, user-granted waivers, and reviewer/criticizer settings used for the run.

Reference ideas are not eligible for `PLAN_v1.md` until their adoption question answers are recorded.
