---
name: research
description: "Read-only external knowledge gathering. Mirrors ODIN's canonical 5-tier doc-retrieval priority (Official docs → API refs → Books/papers → Tutorials → Community). Use whenever the user asks about library APIs, framework behavior, SDK migration, version-specific docs, vendor announcements, RFCs, or any external technical knowledge. Verifies claims against primary sources before synthesis. Invoke for any of: \"how does X library work\", \"what's the API for Y\", \"migration guide\", \"version changes in Z\", \"docs for\", or any named library/framework/SDK/API/CLI/service — even without naming /research."
---

# Research Command

Read-only external knowledge gathering. Walk the canonical 5-tier source ladder; cite every claim to a primary source; flag training-data-only assertions explicitly. Do NOT write, edit, or commit files.

## When to Apply / NOT

**Apply:**
- Library/framework/SDK/API docs — signatures, config options, migration
- Version-specific behavior — changelogs, deprecations, breaking changes
- Vendor announcements, RFCs, public web technical content
- Any named library, framework, SDK, API, CLI tool, or cloud service

**NOT apply:**
- Questions about a local repo's code — use a codebase exploration workflow instead
- Autonomous goal-directed research loops (multi-step, agent-driven)
- Implementation or file editing

## Process

1. **Identify subject** — extract the library, framework, SDK, API, CLI, or topic from the user's message. Capture version if stated (e.g., `pydantic@2.7`). If version unstated, resolve latest stable at Tier 1.
2. **Resolve identifier** — look up the canonical name and version from the library's official documentation surface. If no dedicated doc tool is available, use the subject name as the search query and proceed.
3. **Walk the source ladder** — start at Tier 1; proceed to the next tier only on hard failure (source unavailable, no results, clearly non-authoritative hit). State which tier was skipped and why.
4. **Cross-reference** — every factual claim must cite at least one primary source URL. Assertions derived solely from training data must carry `[Speculative — training data only]`.
5. **Synthesize** — produce Required Output with source URLs and `library@version` identifiers.

## Source Ladder

Priority order (canonical): 1) Official docs 2) API refs 3) Books/papers 4) Tutorials 5) Community

If a source category is unavailable or returns no authoritative results, skip it and move to the next tier — do not halt.

| Tier | Priority | Source type | Use when |
|------|----------|-------------|---------|
| 1 | Official docs | Library/framework official documentation site; SDK reference pages | Named library/framework/SDK with a published doc surface |
| 2 | API refs | API reference pages; repository README and docs folders | API signatures, types, configuration keys, repo-architecture details |
| 3 | Books/papers | RFCs; academic papers; vendor whitepapers; standards documents | Standards-body publications, deep technical specifications |
| 4 | Tutorials | Tutorial articles; blog posts; vendor how-to guides | Example-driven walkthroughs when reference docs are insufficient |
| 5 | Community | Repository issues and discussions; community forums; Q&A threads | Real-world usage patterns, upstream known issues, community workarounds |

## Required Output

1. **Subject identification** — canonical name + version (e.g., `pydantic@2.7.4`)
2. **Source-cited claims** — each claim: `[Claim] — Tier N, source: [URL or doc path]`
3. **Confidence labels** — `Verified` (Tier 1–2 primary source), `Probable` (Tier 3–4), `Speculative` (training data only — flag explicitly)
4. **Open questions** — claims unanswered after ladder exhaustion; state which tiers were attempted

## Anti-Patterns

- Inventing versions, API signatures, or config keys from training data without Tier 1 verification
- Skipping Tier 1 for a named library that has published docs — always attempt official docs first
- Opaque source attribution — every claim needs a citable source URL or an explicit `[Speculative]` label
- Re-entering a router or orchestrator skill from within this leaf skill — forbidden (recursion guard)
