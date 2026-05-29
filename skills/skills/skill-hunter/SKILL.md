---
name: skill-hunter
description: Use when the user wants to find NEW external skills for a project, build a skill stack from external registries, or compare external options against project needs. Do not use for questions about how to use already-installed/local skills.
---

# Skill Hunter

## Overview

Analyze the repo and user goals to assemble a minimal, justified skill stack. Prefer official sources, inspect every candidate, and install only after user confirmation.

## Trigger phrases (use this skill when you hear)

- "Find new skills for this project"
- "Recommend external skills for [technology/domain]"
- "Which skills apply here?"
- "Compare external skills to what we have"
- "Are there better skills than what I have?"
- "What external skills exist for [X]?"
- "Help me find skills for [task]"

## Non-triggers (do not use this skill)

- "Which local skills should I use?"
- "How do I use these installed skills?"
- "Explain what this installed skill does"
- Requests limited to already-installed/local skills with no external discovery

## Required inputs (confirm before external search)

- Goals and priority tasks
- Trust policy / tiers to target (official-only vs allow maintained vs allow community)
- Category focus (pick any; default to "all categories" if not specified)

If any required input is missing, ask for it and stop. Do not list candidates or recommendations until the user answers or explicitly waives questions.

## Internal checks (do not ask the user unless blocked)

- Determine whether external browsing is available and allowed from the client config/tooling.
- If the client exposes a web/browse tool and there is no explicit “do not browse” instruction, treat browsing as granted and proceed without asking.
- Only ask the user about browsing if the client clearly indicates browsing is disabled or permission is explicitly denied.
- If `npx skills` is available, use it as the primary skills.sh discovery path.

## Workflow

Progress tracker (copy into your response and update as you go):
- [ ] Dossier: scanned project, identified stack and goals
- [ ] Questions: user answered or explicitly waived
- [ ] Discovery: searched required sources (skills.sh ☐ Context7 ☐ GitHub ☐)
- [ ] Inspection: read SKILL.md for 3+ candidates
- [ ] Overlap: capability matrix complete
- [ ] Recommendation: stack presented with confidence ratings
- [ ] Install: user confirmed, skills installed
- [ ] Verify: all skills load correctly

### 1) Build a project dossier
- Confirm project root; ask if unclear.
- Read: dependency manifests (`package.json`, `pyproject.toml`, `requirements*`, `go.mod`, `Cargo.toml`, `pom.xml`), `README*`, and `AGENTS.md`.
- Scan for existing installed skills (overlap awareness).
- If goals or constraints are still unclear after the above, also read: `docs/`, `CHANGELOG*`, CI configs, `Makefile`, infra/IaC files.
- Summarize: domain, stack, critical workflows, tools, constraints, and risks.

### 2) Ask clarifying questions (required)
- Ask clarifying questions **before any external search**.
- Do not ask which agent is in use; assume the current client.
- Proceed to Step 3 only after answers **or** an explicit user waiver such as “skip questions, assume defaults.”
- Do **not** treat “obvious” goals as a waiver; the waiver must be explicit.
- If the user waives questions, record the assumptions and state them in your response.
- Ask questions in **multiple‑choice, multi‑select** format with an **Other** option for custom text. Provide defaults based on the project dossier and allow “use defaults” as a one‑line answer.
  - **Goals (pick any):** Reliability/quality, UX/design, Integrations, Automation, Documentation, Performance, Other: ___
  - **Trust tiers (pick any):** Official‑only, Maintained, Community, Other: ___
  - **Categories (pick any):**
    - Product, UX & Content (frameworks, UI/a11y, design, SEO, copywriting)
    - DevOps & Delivery (deploy, CI/CD, hosting, environment setup)
    - Integrations & SaaS APIs (payments, CRM, auth, analytics)
    - Data & Documents (ETL, DBs, CSV/XLSX/PDF/DOCX/PPTX)
    - Quality & Safety (testing, debugging, security, performance, reliability)
    - Tooling & Automation (browser use, scraping, agent tools, workflow automation)
    - Planning & Orchestration (planning, strategy, task management, logging, subagents)
    - Other (user-defined): ___
- Do not present candidate lists or recommendations in this step.

### 3) Discover candidate skills (evidence-based)
- Do not browse until required inputs are confirmed.
- If browsing is disabled or the client has no external search capability, skip external search and limit discovery to local skills; state the limitation clearly and stop.
- Search skill registries and sources using the client’s external search/browse capability (if available).
- If permission is granted and capability exists, you must perform external discovery and include a concise search log in the response.

Search targets:
- **skills.sh** via `npx skills find <query>` — outputs results directly in non-interactive environments; use freely.
- **Context7** registry via CLI search (see CLI guidance below).
- **GitHub search**: `SKILL.md in:path <technology>` — use as a fallback when registries return fewer than 2 candidates for a category, or for niche/specialized technologies.
- Optional: [Skills Directory](https://skillsdirectory.com) for curated, quality-reviewed skills.
- Optional: official vendor `.well-known/skills` endpoints (if the project vendor publishes them).

Prioritize skills.sh and Context7 via their official tools. Prefer official/trusted sources: skills created/maintained by the tool or company that owns the tech in the codebase. If a registry is unavailable, say so and fall back to GitHub search or the vendor's official docs.

Hard gates:
- skills.sh must be searched via `npx skills find <query>`.
- Context7 must be attempted via `ctx7 skills suggest` and/or `ctx7 skills search`.
- GitHub search should be used when registries return fewer than 2 candidates for a category, or when the technology is niche/specialized.
- If a source is unavailable, log the failure, mark it **unavailable** in the search summary, and proceed.
- Block only if all sources fail or if required sources were skipped without a stated reason.
- For each source, open at least one relevant skill detail page or repo entry (or explicitly state none were relevant).

Context7 CLI guidance:
- Context7 CLI commands (`ctx7 skills search`, `ctx7 skills suggest`) print results before showing an interactive selection prompt. Wrap them with `timeout 10` to capture results without hanging: `timeout 10 npx -y ctx7 skills suggest` or `timeout 10 npx -y ctx7 skills search "<query>"`. A timeout exit code (124) is expected; the results are in the captured output.
- If the project has dependency files (package.json, requirements.txt, pyproject.toml), run `ctx7 skills suggest` first to get dependency-aware recommendations. Record the output and use it to supplement keyword searches.
- Then run `ctx7 skills search "<query>"` for targeted category keywords.
- Do not attempt to interact with ctx7 selection prompts. Use the printed results as evidence and install separately via `npx skills add` or `ctx7 skills install` with explicit arguments.
- Context7 results include install counts and trust scores (0–10); use these as additional signals during inspection (Step 4).

Search matrix:
- Run `ctx7 skills suggest` once (covers all categories via dependency analysis).
- For each selected category, run at least one `npx skills find <query>`. Batch related categories into a single broad query where possible (e.g., "testing security" covers Quality & Safety).
- Use GitHub search for gaps — categories where registries returned fewer than 2 candidates.
- Default budget: 1 query per category for skills.sh, 1 suggest + 1–2 targeted searches for Context7, GitHub only as needed.
- Reuse the same query terms across sources when possible to keep coverage consistent.
- If a candidate is not discoverable via `npx skills find`, verify it with `npx skills add <repo> --list` before treating it as installable via Skills CLI.

Search tips:
- Use specific keywords (e.g., "react testing" beats "testing").
- Try synonyms (deploy/deployment, ci-cd, automation/workflow).
- Check popular sources when relevant (e.g., official vendor skills).

### 4) Inspect each candidate (no assumptions)
Inspection checklist:
- Open SKILL.md from the source and read frontmatter and body.
- Verify maintainer, license, and install method.
- Confirm the install path is actually supported by the source (Skills CLI vs repo vs package).
- Scan scripts/references for required tools and dependencies.
- Check activity signals (recent commits/releases, issues health).
- Confirm compatibility with the target agent (current client).
- Assess confidence (High/Medium/Low) using evidence you can verify: trust tier, recency/activity, documentation quality, project fit, and overlap. Do not invent install counts.
- Note required installs and security/data-access risks (network, secrets, write operations, privileged tooling).

Minimum evidence:
- If external browsing is permitted and available, inspect at least 3 external candidates (or all found, whichever is smaller).
- If no external candidates exist after exhaustive search, report that no relevant external skills were found and list the searches performed.
- If a candidate’s SKILL.md cannot be opened from the source, mark it **unverified** and exclude it from primary recommendations.

### 5) Evaluate quality and overlap
- Rate trust tier: Official / Maintained / Community.
- Create a capability matrix to avoid duplicate coverage.
- If a skill is not well established, label it as optional and do not recommend it by default.
- Consider local skills only to avoid overlap; never recommend them.
- If an external candidate matches a locally installed skill (same name or same repo), treat it as already installed and exclude it from recommendations; note it under Local Skills.

### 6) Recommend a stack (or variants)
- Provide a recommended stack only after required inputs are confirmed (or explicitly waived) and discovery/inspection is complete.
- Recommendations must be **external skills only**. Local skills can be mentioned as context but must never be included in the stack.
- If there is no clear single best choice, provide 2-3 variants with tradeoffs (coverage vs risk vs maintenance).
- For each skill, include purpose, source, trust tier, overlap notes, and a confidence rating (High/Medium/Low) with a 1–2 sentence rationale.
- Include the **install method per skill** (Skills CLI, Codex skill-installer, git clone, package upload, or vendor-specific).
- Do not include Low-confidence skills in the primary stack. List them separately under **Experimental / Unverified** with explicit caveats.
- If steps 3–5 were skipped when external browsing is available, respond with **incomplete: external discovery not finished** and list what is missing.
 - End with a **selection prompt** (multi‑choice) asking which stack to install at the **project level**. Allow “none” and custom text.

### 7) Confirm and install (agent-aware)
- Only install after the user confirms their chosen stack.
- For install steps by agent and CLI options, read `references/installation.md` **after** user confirmation.
- Default install target is the **current agent only**. Do not present an agent list unless the user explicitly requests a different agent or multi‑agent install.
- If the user specifies a different agent, install **only** for that agent (no auto‑detect, no extra agents).
- If the Skills CLI does not list the current agent, **do not proceed with CLI**. Use the agent‑specific project‑level path from `references/agent-skills.md` instead.
- Use the install method verified during inspection. Do not default to `npx skills add` unless the skill is sourced from a Skills CLI-supported repo/listing.
- If a skill wasn’t found via `npx skills find`, you must verify it with `npx skills add <repo> --list` before installing via Skills CLI.
- If a skill lacks a **verified install method for the current agent** (even if a source repo exists), do **not** attempt to hand-write or reconstruct it. Ask for authoritative install guidance or mark it unverified.
- If manual copying is required and the skill source is verified, read `references/agent-skills.md` for agent-specific paths, skill format, and discovery locations. Copy the exact skill folder and all bundled files (`scripts/`, `references/`, `assets/`) from the source.
- If the source repo has multiple skills or shared files, follow the multi‑skill guidance in `references/agent-skills.md` before copying.

### 8) Verify installation
After installing skills:
1. Confirm each skill folder exists at the expected path
2. Read each SKILL.md frontmatter to verify it loads
3. List installed skills to the user with a brief description
4. Suggest a quick "run/use" test for key skills

## Assumptions (only if user waives questions)

If the user explicitly waives questions, state the assumptions in your response. Defaults:
- Goals: recommend the best-fit skill stack for the project
- Trust policy: official-only
- Permission to browse: use existing permission; if none, ask before browsing
- Project root: current working directory
- Category focus: all categories

## Output format (concise)

If required inputs are missing: ask questions only and stop.

- **Project dossier**: stack, goals, constraints, key workflows
- **Search summary**: sources searched (ok/unavailable), queries used per category, total candidates found. Do not fabricate logs or links. For Context7, record CLI commands used or mark as unavailable.
- **Candidate table**: per candidate — name, source, trust tier, confidence (H/M/L), key finding from inspection
- **Local skills** (only if overlaps exist): list with overlap notes
- **Recommendations** (external only): primary stack + optional variants. Per skill: purpose, confidence + rationale, install method, requirements/risks.
- **Experimental / Unverified** (if any): Low-confidence skills with caveats
- **Assumptions** (if waiver was given)
- **Next step**: multi‑choice selection of stack to install (project‑level)
