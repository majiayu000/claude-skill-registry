---
name: web-research
version: 1.0.0
description: '[Research] Broad web search on a topic. Collect sources, validate credibility, build source map. Use when starting any research task.'
allowed-tools: Read, Write, Grep, Glob, WebSearch, WebFetch, TaskCreate
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting.

**Prerequisites:** **MUST READ** before executing:

- `.claude/skills/shared/web-research-protocol.md`

> **External Memory:** For complex or lengthy work (research, analysis, scan, review), write intermediate findings and final results to a report file in `plans/reports/` — prevents context loss and serves as deliverable.

> **Evidence Gate:** MANDATORY IMPORTANT MUST — every claim, finding, and recommendation requires `file:line` proof or traced evidence with confidence percentage (>80% to act, <80% must verify first).

## Quick Summary

**Goal:** Execute broad web search on a topic, collect and classify sources, build a structured source map.

**Workflow:**

1. **Define scope** — Parse topic, generate 5-10 search queries from varied angles
2. **Execute searches** — Run WebSearch for each query, collect results
3. **Source triage** — Classify each source by Tier (1-4), filter duplicates
4. **Build source map** — Write structured source list to working file
5. **Identify gaps** — Note underexplored angles for deep-research

**Key Rules:**

- Maximum 10 WebSearch calls per invocation
- Follow source hierarchy from web-research-protocol.md
- Output intermediate source map, not final report

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# Web Research

## Step 1: Define Search Scope

Parse the user's topic and generate 5-10 search queries that cover:

- **Definition/overview** — "what is {topic}"
- **Current state** — "{topic} 2026" or "{topic} latest"
- **Comparison** — "{topic} vs alternatives"
- **Data/statistics** — "{topic} market size" or "{topic} statistics"
- **Expert opinion** — "{topic} expert analysis" or "{topic} review"
- **Criticism/risks** — "{topic} challenges" or "{topic} risks"

## Step 2: Execute Searches

For each query:

1. Run `WebSearch` with the query
2. Record: title, URL, snippet, apparent source type
3. Stop at 10 WebSearch calls maximum

## Step 3: Source Triage

For each result, classify by Tier:

- **Tier 1:** .gov, .edu, official docs, peer-reviewed
- **Tier 2:** Industry reports, major publications
- **Tier 3:** Established blogs, verified experts, Wikipedia
- **Tier 4:** Forums, personal blogs, social media

Filter out duplicates (same URL or same content from syndication).

## Step 4: Build Source Map

Write to `.claude/tmp/_sources-{slug}.md`:

```markdown
# Source Map: {Topic}

**Date:** {date}
**Queries executed:** {count}
**Sources found:** {count} (Tier 1: N, Tier 2: N, Tier 3: N, Tier 4: N)

## Sources

| #   | Title | URL | Tier | Relevance | Notes         |
| --- | ----- | --- | ---- | --------- | ------------- |
| 1   | ...   | ... | 1    | High      | Official docs |

## Gaps Identified

- {angle not covered}
- {topic needing deeper research}
```

## Step 5: Identify Gaps

Review source map for:

- Missing perspectives (only positive sources? need criticism)
- Missing data types (no quantitative data? need statistics)
- Recency issues (all sources old? need current data)

Note gaps for the `deep-research` step.

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks using `TaskCreate`
- Always add a final review todo task to verify work quality and identify fixes/enhancements

---

## Workflow Recommendation

> **IMPORTANT MUST:** If you are NOT already in a workflow, use `AskUserQuestion` to ask the user:
>
> 1. **Activate `research` workflow** (Recommended) — web-research → deep-research → synthesis → review
> 2. **Execute `/web-research` directly** — run this skill standalone

---

## Next Steps

**MANDATORY IMPORTANT MUST** after completing this skill, use `AskUserQuestion` to recommend:

- **"/deep-research (Recommended)"** — Deep-dive into top sources
- **"/business-evaluation"** — If evaluating business viability
- **"Skip, continue manually"** — user decides

## Closing Reminders

**MANDATORY IMPORTANT MUST** break work into small todo tasks using `TaskCreate` BEFORE starting.
**MANDATORY IMPORTANT MUST** validate decisions with user via `AskUserQuestion` — never auto-decide.
**MANDATORY IMPORTANT MUST** add a final review todo task to verify work quality.
