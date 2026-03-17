---
name: localsetup-skill-discovery
description: "Discover and recommend public skills from external registries (e.g. awesome lists, skill hubs). Use when the user is creating a new skill, importing a skill, or asking to find similar public skills. Maintains PUBLIC_SKILL_REGISTRY.urls and PUBLIC_SKILL_INDEX.yaml; returns top 5 similar matches with rich summaries and clear next actions."
metadata:
  version: "1.4"
---

# Skill discovery (public registries)

**Purpose:** Let users discover publicly available skills from external collections (e.g. awesome lists, skill hubs, or public registries) so they can reuse or adapt existing skills instead of building from scratch. Runs in conjunction with skill-creator and skill-importer: when the user is creating or importing a skill, recommend up to five similar public skills and offer clear next steps.

## When to use this skill

- User is **creating a new skill** (skill-creator flow): after they describe the skill or propose name/triggers, run discovery and recommend similar public skills before they draft.
- User is **importing skills** (skill-importer flow): optionally check public index for similar skills and suggest "consider these instead or in addition."
- User asks to **discover**, **find similar**, or **recommend public skills** for a topic or description.

## Registry and index

- **Public repo registry:** `_localsetup/docs/PUBLIC_SKILL_REGISTRY.urls`  - One URL per line (skill collections, awesome lists, GitHub repos). Lines starting with `#` are ignored. This defines where to look for public skills.
- **Public skill index:** `_localsetup/docs/PUBLIC_SKILL_INDEX.yaml`  - YAML with `schema_version`, `sources`, `updated` (ISO8601 date/datetime of last refresh), and `skills`. Each skill entry includes richer matching data: `summary_short`, `summary_long`, `capabilities`, `requirements`, `risk_flags`, `quality_signals`.
- **Project-maintained copies:** The framework's GitHub repository keeps its own copy of the registry and index. Users who do not want to maintain their own can download these files from the project repo (e.g. raw URLs from the default branch) or update the framework so `_localsetup/docs/` gets the latest; alternatively they can edit and refresh locally.

## Index refresh and prompts

- **Current date:** Obtain the current date from the environment (e.g. `date` on Linux/macOS, `Get-Date` in PowerShell) for all age calculations.
- **Index missing or never refreshed:** If the index file does not exist or `updated` is null/missing/empty, **always prompt the user** to build the index: e.g. "The public skill index has not been built yet. I can refresh it now from the registry URLs. Should I proceed?" Do not run discovery until the user agrees and the index is built, or the user declines.
- **Default minimum: 7 days.** Do not prompt to refresh if last refresh was less than 7 days ago. If `updated` is 7 or more days ago, **prompt to refresh**: e.g. "The index was last refreshed on YYYY-MM-DD (X days ago). Would you like to refresh it now?"
- **On every skill operation:** Whenever you use this skill (create, import, or discover), **remind the user**: "Last index refresh: YYYY-MM-DD (X days ago)." or "(X weeks ago)" or "(X years ago)" using the `updated` value and the current date. Then if the index is older than 7 days, add: "The index is over 7 days old. Would you like to refresh it now?" If the user says yes, perform the refresh (fetch registry URLs, parse, write YAML, set `updated` to now).
- **After refresh:** Write `updated` to the YAML with the current date/time (ISO8601) so the next run shows the correct "last refreshed" age.

## Post-refresh scrub (mandatory)

After every index refresh, the scrub step **must** run before the index is considered ready for discovery. The scrub catches dead URLs, stub/placeholder descriptions, and schema gaps that the refresh tool introduces automatically (e.g. Anthropic skills get generated placeholder descriptions; OpenClaw entries often have minimal or truncated text).

**Sequence (agent steps):**

1. **Refresh** - Run `python3 _localsetup/tools/refresh_public_skill_index.py`. Wait for completion and confirm the skill count written to stdout.
2. **Scrub dry-run** - Run `python3 _localsetup/tools/skill_index_scrub.py --skip-url-check`. This fetches real descriptions from upstream SKILL.md files for any stub entries and produces a GFM report. URL checking is skipped in normal flow to keep runtime short; run with full URL checking only when explicitly requested or before a public release.
3. **Review report** - Check the summary table. If "Fixable (upstream desc found)" > 0, proceed to step 4. If "Stub or too-short descriptions" > 0 but fixable count is 0, note the unfixable entries (upstream had no usable content) and accept them.
4. **Apply fixes** - Run `python3 _localsetup/tools/skill_index_scrub.py --skip-url-check --fix`. Confirm the "Applied fixes" count in the report.
5. **Done** - The index is now ready. Report summary to the user: total skills, stubs fixed, stubs unfixable (if any), `updated` timestamp.

**With URL check (optional, slower):** Add `--workers 20` and remove `--skip-url-check` to also validate liveness of all skill URLs. Recommended before publishing the index upstream or before a framework release. Use `--report FILE` to save the GFM report.

**Shorthand for agents:** "refresh and scrub" means run steps 1-5 above in order.

## Workflow (agent steps)

1. **Check index and last refresh** - Read PUBLIC_SKILL_INDEX.yaml (or confirm it is missing). Get current date from the environment. If file missing or `updated` is null/empty: prompt user to build the index; do not continue until built or user declines. Otherwise compute age (days/weeks/years since `updated`) and show: "Last index refresh: <date> (<X days/weeks/years ago>)." If age >= 7 days, prompt: "The index is over 7 days old. Would you like to refresh it now?" If user says yes, run the **full refresh + scrub sequence** (see "Post-refresh scrub" above): refresh, dry-run scrub, apply fixes, report summary.
2. **Match and rank** - Read the user's intent (proposed skill description, or candidate skill name/description). Compare to each index entry using `summary_*`, `capabilities`, and `description` with keyword overlap and intent similarity. Return the **top 5** best matches. If fewer than 5 exist, return what is available.
3. **Present recommendations** - Always use the **default recommendation format** (see below). Each recommendation must include a concise but rich summary (2-4 sentences), constraints, and a clear recommendation status. After the formatted list, offer: "Would you like: **(1) In-depth summary** of each, **(2) Use a public skill** (I'll pull it from the source and run it through our import process so it's compliant), **(3) Continue on your own** (ignore these and keep creating/importing as planned), or **(4) Adapt from one** (use one as a base and customize)?" Ask the user to choose.
4. **Handle choice** - (1) For each of the top 5, fetch or summarize the skill (e.g. from README or SKILL.md) and present a short in-depth summary. (2) Resolve the skill URL (e.g. from awesome list to actual repo), then run the **skill-importer** workflow: fetch, run skill_importer_scan, validate, security screen, user selects, duplicate/overlap check, import. The result is a framework-compliant skill; no need to recreate. (3) Do nothing; continue with skill-creator or skill-importer as before. (4) Same as (2) but after import, help the user adapt the skill (edit name, description, add/remove sections) so it fits their case.

## Integration with skill-creator and skill-importer

- **Skill-creator:** After "Decide name and triggers" (and before or after "Duplicate, overlap, and namespace check"), run this discovery: get top 5 similar public skills, present the four options. If user picks (2) or (4), switch to import flow for the chosen public skill; then for (4) guide adaptation.
- **Skill-importer:** Before or after "User selects" which skills to import, optionally run discovery against the selected candidates and suggest: "Similar skills are available from public registries; would you like summaries or to pull one instead?"

## Default recommendation output format

Always present the top 5 (or fewer) matches in a ranked structure. Do not return bare names only.

Output contract:

1. Intro line naming the topic/query and the number of recommendations.
2. Ranked recommendations (`1..N`), one block per skill:
   - Skill name as clickable markdown link (`[name](url)`).
   - Summary (2-4 sentences) using index fields in this order: `summary_long`, fallback to `summary_short`, then `description`.
   - Why it fits this project or query (1-2 specific sentences).
   - Constraints/risks (use `requirements` and `risk_flags` when available).
   - Recommendation status: `import now`, `evaluate later`, or `skip`.
3. Optional compact comparison table only when the platform clearly supports markdown tables. If uncertain, skip table and keep ranked blocks.
4. End with the four next-action options.

Presentation fallback by platform capability:

- Rich markdown: ranked blocks plus optional table.
- Basic markdown: ranked blocks only.
- Plain text/ascii: ranked blocks with labeled lines (`Skill:`, `Summary:`, `Risks:`), no table.

## Options summary

| Option | Action |
|--------|--------|
| In-depth summary | For each of the top 5, fetch/summarize the skill and show what it does in detail. |
| Use public skill | Pull the skill from the source (e.g. GitHub), run through import (scan, validate, screen, duplicate check, import). User gets a compliant skill without recreating. |
| Continue on own | No change; user keeps creating or importing as they were. |
| Adapt from one | Same as "Use public skill" then help user customize (rename, edit description, add/remove content). |

## Reference

- _localsetup/docs/SKILL_DISCOVERY.md  - Registry and index format; post-refresh scrub sequence; when discovery runs; recommendation flow.
- _localsetup/docs/PUBLIC_SKILL_REGISTRY.urls  - One URL per line; where to look for public skills.
- _localsetup/docs/PUBLIC_SKILL_INDEX.yaml  - Index of skills for similarity; refresh + scrub before use.
- _localsetup/tools/refresh_public_skill_index.py  - Step 1 of the maintenance sequence: fetch from registries.
- _localsetup/tools/skill_index_scrub.py  - Step 2 of the maintenance sequence: audit and fix descriptions.
- Use with **localsetup-skill-creator** and **localsetup-skill-importer** when creating or importing.
