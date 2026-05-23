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

### 1) Build a project dossier
- Confirm project root; ask if unclear.
- Scan repo and subdirectories until the scope is unambiguous.
- Read key docs: `AGENTS.md`, `README*`, `docs/`, `CHANGELOG*`, `package.json`, `pyproject.toml`, `requirements*`, `go.mod`, `Cargo.toml`, `pom.xml`, `Makefile`, CI configs, infra/IaC files.
- Find domain keywords, APIs, and workflows using your agent's file discovery and content search tools.
- Summarize: domain, stack, critical workflows, tools, constraints, and risks.
- Inventory currently installed local skills for overlap awareness only.

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
- Context7 registry (use CLI search; see below)
- skills.sh via `npx skills find <query>` (preferred) or homepage leaderboard + detail pages
- GitHub search: `SKILL.md in:path <technology>`
- Optional: official vendor `.well-known/skills` endpoints (if the project vendor publishes them)

Prioritize Context7 and skills.sh via their official tools. Use direct GitHub searches as a secondary source for gaps or high‑value skills not found via registries.

Prefer official/trusted sources: skills created/maintained by the tool or company that owns the tech in the codebase. If a registry is unavailable, say so and fall back to GitHub search or the vendor's official docs.

Hard gates:
- Skills.sh must be searched via `npx skills find <query>` or the homepage leaderboard.
- Context7 must be attempted via CLI search (`ctx7 skills search ...` or `npx -y ctx7 skills search ...`).
- GitHub search should be performed for relevant technologies.
- If a source is unavailable, log the failure, mark it **unavailable** in the search log, and proceed.
- Block only if all sources fail or if required sources were skipped without a stated reason.
- Do not list candidates unless required sources were searched or you explicitly state why they were unavailable.
- For each source, open at least one relevant skill detail page or repo entry (or explicitly state none were relevant).

Context7 CLI guidance:
- Prefer `ctx7 skills search "<query>"` if installed.
- If not installed, try `npx -y ctx7 skills search "<query>"` (do not install skills; cancel after results list).
- If the CLI is interactive, record the results shown and exit without selection/installation.

Search matrix requirement:
- For each selected category, run at least one query per source (Context7, skills.sh, GitHub) unless that source is unavailable.
- Do not “sample” a few skills; cover each category × source. If the search budget is large, ask the user to cap it (default: 1 query per category per source).
- Reuse the same query terms across sources when possible to keep coverage consistent.
- For skills.sh, use `npx skills find <term>` or the homepage leaderboard plus `site:skills.sh <term>` web search to find relevant detail pages.
- If a candidate is not discoverable via `npx skills find`, verify it with `npx skills add <repo> --list` (or equivalent) before treating it as installable via Skills CLI.

Search tips (concise):
- Use specific keywords (e.g., “react testing” beats “testing”).
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
- If no external candidates exist after exhaustive search, return **blocked: insufficient external candidates** and list the searches performed.
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
- If steps 3–5 were not completed when external browsing is permitted, respond with **blocked: external discovery not completed** and list what is missing.
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

- Project dossier: stack, goals, constraints, key workflows
- Search log: tool + query + source domain (only when external search is used). Do not fabricate logs or links.
  - For Context7, record CLI commands used (ctx7 or npx) or mark as unavailable if CLI is not present.
- Required sources: Context7 (ok/unavailable), skills.sh (ok), GitHub (ok)
- Search matrix: categories × sources with queries used
- Inspection notes: per candidate
- Candidate skills: source + trust tier + inspection notes
- Local skills (awareness only): list but do not recommend
- Overlap analysis: what each skill covers and conflicts
- Recommendations (external only): primary stack + optional variants, each with confidence + rationale
- Experimental / Unverified: Low-confidence skills with explicit caveats (optional)
- Requirements & Risks: required installs/dependencies and any security/data-access risks per recommended skill
- Install method per skill (explicit)
- Checklist: Discovery ☐ Inspection ☐ Overlap ☐ Recommendation
- Assumptions (if any)
- Next step: multi‑choice selection of stack to install (project‑level)
