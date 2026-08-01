---
name: journey-mapper
description: Scans a codebase and generates a self-contained HTML service-design journey map — NN/g combined customer journey + service blueprint format. Use when the user wants to map user journeys, create journey maps, build service blueprints, or understand user flows from code. Prompts for codebase path if not supplied. Works with any tech stack.
---

# Journey Mapper

Reads a codebase, thinks like a service designer, and writes a single browser-ready HTML file with all inferred user journeys and service blueprints.

See `REFERENCE.md` in this skill's base directory for the JSON schema, NN/g methodology notes, and emotional arc heuristics.

## Quick start

If the codebase is not already in scope, ask:
> "Which directory should I scan? And where should I save the output HTML?"

## Workflow

**1. Gather context** — ask for anything not already in scope:

| Input | Default |
|---|---|
| Codebase path | Required — ask if missing |
| Output path | `journey-map.html` in codebase root |
| Product name | Used in the HTML title and rail heading |
| Extra context | Design docs, research, README, API specs |
| Scope | Full scan, or specific subdirectory for large codebases |

**2. Scan the codebase** — dispatch Explore, or use Grep + Read for targeted sweeps. Extract:
- Routes, screens, page components, entry points
- Auth roles, user types, permission models, tenant structures
- Onboarding flows, auth gates, redirect chains, feature flags
- API endpoints, background jobs, third-party integrations
- Email templates, push notifications, in-app alerts, webhook payloads
- Error states, empty states, loading patterns, blocked or warning states

For large codebases: routes first → components → API layer → notifications.

**3. Organise into NN/g structure** — think as a service designer:
- **2–5 actors** — who uses the system (infer from auth roles, user types, API consumers)
- **3–6 categories** — thematic groups (Onboarding, Core workflow, Admin, Recovery, Alternative paths…)
- **4–12 journeys** — one per meaningful end-to-end scenario; cover golden paths first, then error/recovery
- Each journey → **2–5 stages** → **2–4 moments** per stage

Per-moment fields to fill — every inferred value gets `[Assumption]` prefix:

| Field | Notes |
|---|---|
| `doing` | What the user physically does. Factual. No `[Assumption]`. |
| `frontstage` | What they see: UI, email, native prompt. Factual. |
| `backstage` | What the code does behind the scenes. Factual. |
| `support` | Which system, service, or API underpins this. Factual. |
| `thinking` | `[Assumption]` — inferred user thought at this moment. |
| `feeling` | Integer 1–5 (1 = very frustrated, 5 = delighted). Use 2–3 for friction-heavy moments. |
| `pain` | `[Assumption]` — inferred friction point. |
| `opportunity` | `[Assumption]` — inferred improvement idea. |
| `evidence` | Leave blank `""` — the human fills this from user research. |

See `REFERENCE.md` for emotional arc heuristics and a worked example.

**4. Generate the HTML:**
1. Read `TEMPLATE.html` from this skill's base directory (shown above when skill loads).
2. Replace `<title>Journey Maps</title>` with `<title>[Product name] — Journey Maps</title>`.
3. Replace the `.rail h1` text `Journey Maps` with the product name.
4. Replace **only** the `<script type="application/json" id="journeys-data">…</script>` block with your generated JSON.
5. Write the complete file to the output path. Do not modify anything else in the template.

**5. Report back:**
- Path the file was saved to
- Journey count · moment count · category count
- Coverage gaps: flows or actor types with thin codebase evidence
- 2–3 standout pain points inferred from error states, friction-heavy flows, or complex conditionals
