---
description: >-
  Compacts the current conversation into a single self-contained handoff document under
  docs/handoffs/ so a fresh agent — a new session, a different AI tool, or another developer
  on a different machine — can resume the work by reading only that file. References committed
  artifacts (PRDs, plans, ADRs, issues, commits) by path or URL and inlines anything not yet
  pushed. Redacts secrets and PII. Re-running on an existing handoff lets you enhance the shared
  doc or overwrite it. Use when pausing work that someone else or a future session will pick up,
  or when a long conversation needs a durable summary.
disable-model-invocation: true
---

# Handoff

Compact the current conversation into one self-contained, tool-agnostic Markdown document under `docs/handoffs/` that any fresh agent can resume from by reading only that file. Reference committed artifacts by path or URL; inline anything not yet pushed; redact secrets and PII.

## Step 1: Determine the slug and any focus

Derive a kebab-case `<slug>` from the user's arguments if given (e.g., "finish the migration tests" → `migration-tests`), otherwise from the conversation's most recent active thread; when no arguments were passed, state the inferred topic and slug in one line before continuing.

Record a **Focus for next session** only when the conversation gives a clear signal — verbatim user arguments, or an explicitly stated next objective. Never manufacture one: with no signal, omit the focus and leave forward direction to the resumer.

## Step 2: Locate the doc; decide create, enhance, or overwrite

Resolve the root with `$CLAUDE_PLUGIN_ROOT/skills/init/references/multi-repo-detection.md` — the workspace root in a multi-repo workspace, otherwise the repo/project root. The handoff folder is `docs/handoffs/` under that root. Then branch:

- **`<slug>.md` exists** → read it, then `AskUserQuestion`: **Enhance** (merge new context; keep still-valid content and append a History line) or **Overwrite** (fresh rewrite; the prior version stays in git history).
- **No slug match but other handoffs exist** → list them (filename · title · Last updated), then `AskUserQuestion`: **Continue one** (pick via a follow-up question, then treat as Enhance) or **Create new**.
- **Folder empty or absent** → create new.

## Step 3: Classify artifacts against version control

Resolve git state so the document references what survives on another clone and inlines what does not. Per repo (per child repo in a multi-repo workspace), find the branch and short HEAD SHA for **Origin**, each path's tracked / modified / staged / untracked status, and unpushed commits via `git log --oneline @{upstream}..HEAD` (fallback `origin/HEAD..HEAD`; no upstream or detached HEAD → treat local commits as unpushed). If the directory is not a git repo, note "not a git repo" in **Origin** and inline everything.

Sort every artifact into three buckets:

1. **Tracked and pushed** → reference by repo-relative path / SHA / URL (never inline).
2. **Tracked-but-modified, staged-not-committed, or committed-not-pushed** → inline the relevant content (diff, file body, or commit message) — another clone will not have it.
3. **Untracked** → inline.

Qualify paths and SHAs with the repo name in a multi-repo workspace.

## Step 4: Draft or reconcile the document

If the conversation has not already established the codebase's current state, briefly orient in the repo first so the document's factual claims reflect what is actually there — keep it light; this grounds the doc, it is not fresh exploration.

Fill the **Handoff document template** from what was actually discussed. **New or overwrite** → write fresh. **Enhance** → keep still-valid content; update **Current state** (and **Goal**/**Next steps** if present) to current reality, dropping completed steps; preserve and extend the recorded decisions and open questions, promoting any the new work has resolved; add new artifacts; refresh **Last updated**; append one **History** line.

- Prioritize knowledge a fresh agent could not re-derive from the code or git history — decisions and why, alternatives considered and rejected, constraints, gotchas, and still-open questions. Include **Goal**, **Focus for next session**, and **Next steps** only when the conversation makes them genuinely clear; otherwise omit them.
- Never duplicate content that lives in a tracked artifact — reference it by path plus a one-line summary. Inline only bucket-2 and bucket-3 content.
- Trust git state over chat memory when they conflict; if the current state is ambiguous, say so in one line rather than guessing.
- Keep the document tool-agnostic: refer to the resuming actor as "a fresh agent" or "a new session" — never name a specific AI product.

## Step 5: Redact inlined content

Scan everything you are about to **inline** (never paths or references) against the **Redaction patterns** table and replace matches with the exact marker `[REDACTED: <kind>]`, preserving structure — e.g. `DATABASE_URL=postgres://app:[REDACTED: password]@db:5432/app`. A file whose name looks like a secret (the same set `/optimus:commit` warns about) is **never inlined with its values** regardless of tracked state — see the table's last two rows.

## Step 6: Write the document, then report and recommend

Write the filled template to `docs/handoffs/<slug>.md` under the root resolved in Step 2, creating `docs/handoffs/` if missing.

Report the written path; tell the user the document is redacted and safe to commit, and that any older handoffs in the folder remain (this is the latest for its topic). If the resolved root is a multi-repo workspace root that is not itself a git repo, note that the file is not yet under version control — suggest committing it inside a child repo or initializing version control at the root.

Recommend `/optimus:commit` so the handoff reaches the remote and other machines. Then emit the closing tip from `$CLAUDE_PLUGIN_ROOT/references/skill-handoff.md` — **Variant A**, substituting `<continuation-skill(s)>` with `/optimus:commit` and `<non-continuation-examples>` with `/optimus:code-review`, `/optimus:unit-test`. This tip is spoken to the user; it is never written into the document, which stays tool-agnostic.

## Handoff document template

Minimal-but-complete; omit any section with nothing to say — **Goal**, **Focus for next session**, and **Next steps** included, unless the conversation makes them genuinely clear. Ordering follows a cold reader's path: orient (Goal if present, Current state, decisions) → act (Next steps, if any) → reference (artifacts).

````markdown
# Handoff: <short title of the work>

- **Created:** <YYYY-MM-DD> · **Last updated:** <YYYY-MM-DD>
- **Origin:** <repo> @ `<branch>` · commit `<short-sha>` (<pushed | NOT pushed>)
- **Focus for next session:** <one line — include only if the user passed args or the conversation states the next objective; otherwise omit this bullet>
- **How to use this doc:** Resume cold; read top to bottom — everything is here or linked by repo-relative path.

## Goal
<Include only if the conversation establishes a clear objective. 1-3 sentences: the outcome and why. Omit if not clear.>

## Current state
<2-6 bullets: what is done, in progress, blocked. Prioritize what a fresh agent could not re-derive — decisions made and why.>

**Decisions, constraints & gotchas** (omit if none):
- <A decision made and why — and any alternative considered and rejected, with the reason.>
- <A non-obvious gotcha, or a constraint that gates the work.>

**Open questions** (omit if none):
- <Something the conversation left unresolved — what is undecided and what depends on it. Distinct from a rejected alternative: no decision was reached.>

## Next steps
<Include only if the conversation points to concrete follow-up actions; otherwise omit and leave direction to the resumer.>
1. <Concrete first action on resume.>

## Relevant files & artifacts
> Committed/tracked → referenced by repo-relative path / SHA / URL.
> Uncommitted or unpushed → content inlined below (won't exist on another machine).
> Anchor each reference on a durable identifier (a type / function / config name the resumer can search for) and say why it matters; never cite line numbers — a bare path can move under a refactor.

- `path/to/file.ts` — `SessionStore`: <why it matters> (tracked)
- Issue/PR: <URL> — <relevance>

### Inlined (not yet on remote) — omit if none
```diff
<the fragment that carries the decision — schema, type shape, state machine, or the changed lines that matter, not a full diff dump; or new-file body / unpushed commit message; secrets redacted>
```

## History (most recent first)
- <YYYY-MM-DD>: <one-line summary of what this session changed>

---
**Resume here:** open this file in a fresh session with any AI agent in this repo. If it has a Next steps section, begin at item 1; otherwise pick up from Current state and the decisions above.
````

## Redaction patterns

Applied only to **inlined** content. Marker format is exactly `[REDACTED: <kind>]`.

| Class | Catch | Marker |
|---|---|---|
| API keys / tokens | `sk-…`, `ghp_…`, `xox[bap]-…`, AWS `AKIA…`, Google `AIza…`, JWTs `eyJ…`, bearer | `[REDACTED: API key]` / `[REDACTED: token]` |
| Passwords / secrets | `password=`, creds in connection strings, `client_secret`, `-----BEGIN … PRIVATE KEY-----` | `[REDACTED: password]` / `[REDACTED: private key]` |
| Connection strings | `mongodb+srv://…:…@`, `mssql://…;Password=…` | `[REDACTED: connection string]` |
| PII | personal emails (keep role addresses like `support@`), phones, addresses, national IDs | `[REDACTED: PII]` |
| Env/secret files (text) | inlined `.env` / `*.key` / `*.pem` / `credentials.*` / `secrets.*` bodies | inline variable **names** only, never values |
| Binary/opaque secret files | `*.pfx` / `*.sqlite` / `*.db` bodies | **never inline** — reference by name with a "recreate from your secure source" note |

## Important

- Read-only except for the single file it writes (`docs/handoffs/<slug>.md`). It never stages, commits, or pushes.
