---
name: openseo-project-setup
description: >-
  Bind this repo to an OpenSEO project and prepare the local SEO state
  directories. Use this skill when starting SEO work on a fresh project, when
  `.seo/openseo.json` does not exist yet, when the OpenSEO project id is
  unknown, or when Google Search Console needs connecting before keyword or
  rank work can start. Triggers: "set up openseo", "link seo project",
  "connect gsc", "start seo for this site", "openseo project id".
category: seo
tier: nice-to-have
layer: foundation
reads:
  - brand/keyword-plan.md
  - brand/positioning.md
  - brand/audience.md
  - brand/competitors.md
  - brand/voice-profile.md
writes:
  - brand/keyword-plan.md
env_vars:
  - OPENSEO_API_KEY
  - OPENSEO_MCP_URL
triggers:
  - set up openseo
  - link seo project
  - connect gsc
  - start seo for this site
  - openseo project id
allowed-tools:
  - Bash(mktg catalog *)
  - Bash(mktg doctor *)
  - Bash(mktg run *)
---

# OpenSEO Project Setup

Bind the current repo to an OpenSEO project so every other `openseo-*` skill has a stable project id, and prepare mktg's local SEO state contract. This is a one-time-per-repo handshake, not an audit and not research.

## On Activation

Run these steps in order. Each has a fallback; never block on missing context.

### Step 1 — Check catalog readiness

```bash
mktg seo status --json --fields readiness,catalog,project,bindingCorrupt
```

- Exit 1 → the openseo catalog is missing; upgrade marketing-cli. Stop.
- `not_configured` → connect the hosted MCP with OAuth, or set `OPENSEO_API_KEY` in a private headless client. `OPENSEO_MCP_URL` is only a self-host endpoint override. Without a connection, stop after the gap note — research skills fall back to Exa with metrics `unknown`.
- Any `*_ready` state → proceed through that MCP client. Catalog `configured` means headless API-key readiness, not OAuth truth.

### Step 2 — Read brand grounding

Read `brand/keyword-plan.md` and `brand/positioning.md` if they exist (tolerate missing). The domain, audience, and positioning facts go into the project record. If `brand/` is all templates, note it and recommend `/cmo` foundation first — SEO inputs without positioning are guesses.

### Step 3 — Resolve the OpenSEO project

Via OpenSEO MCP: call `whoami`, then `list_projects`. Match the project to the user's domain. If ambiguous, ask which project. If no match exists, show the proposed name/domain/market and ask before calling `create_project` (a free shared-state mutation).

Do NOT call research tools to test connectivity — `whoami`/`list_projects` are the only probes allowed here (they are free; research calls spend DataForSEO credit).

After resolving the project, read `get_project_context`. Offer to merge verified mktg facts from positioning, audience, competitors, key pages, writing preferences, and goals through `update_project_context`. Show the fields first and confirm because this changes shared OpenSEO memory. Never overwrite a non-empty upstream field silently.

### Step 4 — Write the binding + state directories

Create or update `.seo/openseo.json`:

```json
{ "version": 1, "projectId": "<id>", "domain": "<domain>", "mcpUrl": "https://app.openseo.so/mcp", "linkedAt": "<iso>", "updatedAt": "<iso>" }
```

Create `.seo/` with `rank-snapshots/` if rank tracking is in scope. If `brand/keyword-plan.md` is a template, leave it alone — the first research run populates it; do not pre-fill with placeholders.

### Step 5 — Google Search Console

GSC is the richest first-party signal (striking-distance terms, cannibalization).

- **Hosted**: connect GSC in the OpenSEO project's Integrations page; verify with `get_search_console_performance`, then use `inspect_urls` for priority-page index evidence.
- **Self-host native**: configure `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, and a 32+ character `BETTER_AUTH_SECRET`, with the exact `/api/gsc/oauth/callback` URL. Self-hosting does not require a CSV fallback.
- **File fallback**: when OAuth is intentionally unavailable, place exports under `.seo/gsc/` and record date range/search type.

Never claim GSC is connected unless `get_search_console_performance` confirms it — it returns a "not connected" message otherwise.

### Step 6 — Recommend the next skill

| Situation | Next |
|---|---|
| No keyword plan yet | `openseo-keyword-research` |
| Has keyword list / GSC data | `openseo-keyword-clustering` |
| Market unclear | `openseo-competitive-landscape` |
| Known competitor | `openseo-competitor-analysis` |

## Anti-Patterns

- **Running research calls as a connectivity test** — because every OpenSEO research call can spend DataForSEO credit, and a setup handshake has no business spending money. `whoami` and `list_projects` are free; use only those.
- **Creating a project or overwriting shared context without confirmation** — because these are free but still mutate account state used by other people and agents. Show the intended change first.
- **Claiming GSC is connected without proof** — because downstream skills (keyword research's striking-distance strategy) silently change behavior based on that claim; a false positive turns first-party data into invented data. Verify with `get_search_console_performance` or say "not connected."
- **Pre-filling `brand/keyword-plan.md` with placeholder keywords** — because template-detection (SHA-256) and `mktg plan` health read placeholder content as "populated," and every downstream skill then trusts fake keywords. Leave the template until real research lands.
- **Forking state into a second project file** — because two project ids drift and every skill has to guess which is canonical. `.seo/openseo.json` is the single binding; update it, never duplicate it.
- **Asking the user 15 questions before writing anything** — because setup should orient, not assign homework. Capture what is known, mark the rest `unknown`, and let research skills fill gaps on demand.

## Close the loop

After writing files, log completion so `mktg plan` / `mktg status` count the work (bare `mktg run` only logs `loaded`):

```bash
mktg run openseo-project-setup --complete --writes <paths written> --result success --json
```

## Progressive Enhancement

| Level | Behavior |
|---|---|
| L0 (no envs, no MCP) | Gap note only; point at Exa-backed `keyword-research` with metrics `unknown` |
| L1 (`OPENSEO_API_KEY`) | Binding written; MCP-dependent steps documented as deferred |
| L2 (MCP connected) | Full project resolution + GSC live check |
| L3 (GSC connected) | `.seo/gsc/` or live GSC feeds keyword research + clustering directly |

---

*Adapted from [every-app/open-seo](https://github.com/every-app/open-seo) `.agents/skills/seo-project-setup` (MIT). Upstream workflow by the OpenSEO maintainers; mktg state contract, brand grounding, and cost discipline added here.*
