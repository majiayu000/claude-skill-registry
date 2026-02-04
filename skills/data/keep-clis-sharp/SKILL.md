---
name: keep-clis-sharp
description: Audit and update CLI tools, npm packages, and repo scripts; ensure versions are current and documented. Use when the user says CLIs are outdated, tools need updating, keeping knives sharp, or when doing periodic tool maintenance.
---

# Keep CLIs Sharp (Tool Keeper)

You are the **tool keeper**: keep repo CLIs, npm deps, and scripts current and documented so JARVIS and humans can rely on them.

## When to use

- User says "CLIs are outdated", "keep our knives sharp", "update our tools", or "tool maintenance"
- Periodic upkeep (e.g. after major Node/npm or platform releases)
- Before a release or deep-work cycle

## Workflow

1. **Inventory** — List what to sharpen:
   - **npm:** Root `package.json`, `apps/jarvis-ui/package.json`, `olive-e2e/package.json`
   - **Platform CLIs:** Per `jarvis/TOOLS.md` → Platform CLIs (Maestro): Vercel, Railway, Stripe, Fly.io, Supabase, Netlify, Wrangler, Cursor
   - **Repo scripts:** Prefer scripts in `scripts/`; note any that call external CLIs or pinned versions

2. **Check versions** — Run, then interpret:
   - **npm (each package root):** `npm outdated` (or `npm ls --depth=0`). Note major vs minor/patch.
   - **CLIs:** `vercel --version`, `railway --version`, `stripe --version`, `supabase --version`, etc. Compare to latest from docs or `npm view <cli> version` if installed via npm.

3. **Update safely** — Prefer non-breaking first:
   - **npm:** `npm update` for in-range; for major bumps, update one dependency at a time, run tests, then commit.
   - **CLIs:** Install/upgrade via official method (e.g. `npm i -g vercel`, `brew upgrade supabase`, or vendor docs). Do not guess; check each CLI’s recommended install/upgrade path.

4. **Document** — Keep the shop ledger:
   - **jarvis/TOOLS.md** — If a CLI’s install/upgrade or recommended version changes, update the Platform CLIs table or “When to use” notes.
   - **RUNBOOK.md** — If a script or CLI command changes (e.g. new Supabase CLI flags), update the relevant section.
   - Optional: add a short “Last sharpened” note in a doc or CHANGELOG with date and what was updated.

## Conducting rules

- **One sweep, then report:** Run the checks; summarize what’s outdated, what you updated, and what you deferred (and why).
- **No destructive updates without confirmation:** For major version bumps or CLI upgrades that might change behavior, state the risk and ask before applying, or apply and suggest a quick test plan.
- **Prefer repo scripts:** If a task is already covered by a script in `scripts/`, use it; if an update invalidates a script, update the script and any docs that reference it.

## Quick checklist (copy and track)

```
- [ ] npm outdated (root, apps/jarvis-ui, olive-e2e)
- [ ] Platform CLIs: vercel, railway, stripe, supabase, fly, netlify, wrangler — version check
- [ ] Apply safe npm updates; document major bumps
- [ ] Update jarvis/TOOLS.md if CLI install/usage changed
- [ ] Update RUNBOOK.md if script/CLI commands changed
```

## Reference

- Tool inventory and CLI list: [reference.md](reference.md)
- Repo scripts and when to use: **jarvis/TOOLS.md** (Repairman29 Repo Automation, Platform CLIs)
