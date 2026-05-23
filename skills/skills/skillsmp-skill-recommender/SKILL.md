---
name: skillsmp-skill-recommender
description: Recommend best-fit SkillsMP skills for a project's stack and delivery goals. Use when building a production skill set for a new project, replacing weak skills with stronger alternatives, auditing current skill coverage, or comparing candidate skills before installation.
---

# SkillsMP Skill Recommender

Select high-fit SkillsMP skills for a specific project and return a practical `keep` / `replace` / `add` plan.

## When to Use This Skill

- Building a production skill set for a new project
- Replacing low-quality or low-fit skills in an existing stack
- Comparing candidate skills for the same capability
- Auditing whether current skills cover required delivery areas
- Creating a focused install list from a broad project description

## Invocation

User invokes this skill by describing the project they want to build.

Examples:
- "Use $skillsmp-skill-recommender to build a production skill stack for my project."
- "Use $skillsmp-skill-recommender and suggest skills even if my stack is not finalized yet."

## Input Contract (Required)

Extract these fields before ranking:

- target product type
- stack and frameworks (or enough constraints to select them)
- priority outcomes (e.g., speed, security, UX, CI/CD maturity)
- team level (solo/small team/enterprise-like)
- existing skill list (optional but preferred)

If enough context is present, continue to search.

If context is insufficient, ask clarifying questions before recommending.

## Clarifying Questions (If Needed)

Ask up to 5 short questions, only for missing critical inputs.

Prioritize in this order:

- what exactly to build
- required stack/constraints (or whether stack selection is needed first)
- expected production level
- must-have areas (security/testing/release/etc.)
- current skills to replace (if any)

Do not ask questions when the request is already sufficiently specific.

## Stack Selection (Required Before Search)

If the user did not provide a finalized stack, you must select one first.

Rules:

- infer the best-fit implementation stack from the product description, goals, constraints, and team size
- prefer practical production-ready defaults over exotic combinations
- state the chosen stack explicitly before skill search
- only after stack selection, run capability discovery and search queries for that chosen stack
- do not ask the user to choose stack unless there is a hard technical constraint conflict

Do not skip stack selection when stack is missing or vague.

## Capability Discovery (Dynamic)

Build groups from the user intent, not from a fixed preset.

Method:

- extract nouns (tools/platforms/domains)
- extract verbs (build/test/deploy/secure/monitor/optimize)
- merge overlaps into implementation-oriented groups
- add cross-cutting groups only when needed

Use `references/goal-query-map.md` only as a seed source.
Never force platform- or stack-specific groups unless they are requested or clearly implied.

## Search Strategy

Preferred sources:

1. SkillsMP website UI in MCP Playwright browser
2. Public SkillsMP docs pages only for orientation, not API querying

Run 2-6 focused queries per discovered group in the site search UI.

Execution method (required):

- open SkillsMP site with MCP Playwright browser
- navigate to the skills/catalog search interface
- if authentication is required, complete it via browser login/session flow
- type each query manually in the web search input and submit
- collect candidate skills from rendered UI results
- do not request or use API tokens for this workflow
- do not call API endpoints directly from terminal or HTTP client
- after collecting results, close the Playwright browser session before returning recommendations

Hard restriction:

- never use `curl`, `fetch`, or direct calls to SkillsMP API endpoints such as `/api/v1/skills/search` or `/api/v1/skills/ai-search` (token-protected)

Search quality rules:

- keep queries short and concrete
- avoid broad mega-queries
- collect at least top 5 candidates per group
- deduplicate by `id` and `githubUrl`

## Filtering and Ranking

Reject candidates when:

- they are repo-internal maintenance only
- they are stack-incompatible
- they are mirrors of a better canonical source
- description is vague and non-actionable

Use relevance tiers:

- Tier A: direct fit for high-priority groups
- Tier B: useful adjacent support
- Tier C: generic fallback

Rank with this priority:

1. relevance tier
2. practical stack fit
3. stars/forks as quality signal
4. recency signal if available

Never let stars override relevance.

## Decision Rules

For each current skill slot:

- Replace: clearly better relevance and quality
- Keep: already strong or no meaningful upgrade
- Add: missing capability not covered today

When no strong upgrade exists, explicitly keep.

## Output Format (Required Order)

Return sections in this exact order:

1. `Discovered Capability Groups`
2. `Top Install/Replace List`
3. `Replace Matrix`
4. `Keep As-Is`
5. `Coverage Check`
6. `Source Notes`

Each recommended skill must include:

- name
- source repo/author
- stars
- fit rationale
- priority (`P0` / `P1` / `P2`)
- source note from web UI search context

## Quality Bar

- Prefer canonical upstream sources.
- Prefer workflow-driven skills over vague guidance.
- Prefer reusable cross-project skills over one-repo internals.
- Mark uncertain recommendations explicitly.
- If context is still insufficient after clarification, say so.

## Reference

- Seed query map (non-exhaustive): `references/goal-query-map.md`
