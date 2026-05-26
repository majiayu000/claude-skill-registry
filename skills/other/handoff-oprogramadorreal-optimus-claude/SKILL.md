---
description: >-
  Compacts the current conversation into a single self-contained handoff document under
  docs/handoffs/ so a fresh agent — a new session, a different AI tool, or another developer
  on a different machine — can resume the work by reading only that file. References committed
  artifacts (PRDs, plans, ADRs, issues, commits) by path or URL and inlines anything not yet
  pushed. Redacts secrets and PII. Includes a Suggested skills section pointing at the next
  optimus skills to run. Re-running on an existing handoff lets you enhance the shared doc or
  overwrite it. Use when pausing work that someone else or a future session will pick up, or
  when a long conversation needs a durable summary.
disable-model-invocation: true
---

# Handoff

Compact the current conversation into one self-contained, tool-agnostic Markdown document under `docs/handoffs/` that any fresh agent can resume from by reading only that file. Reference committed artifacts by path or URL; inline anything not yet pushed; redact secrets and PII.

## Step 1: Determine the focus and slug

If the user passed arguments, treat them verbatim as the next session's focus: echo them into the template's **Focus for next session** line and bias every later section toward that focus. Derive a kebab-case `<slug>` from the focus (e.g., "finish the migration tests" → `migration-tests`).

If no arguments were passed, infer the focus and slug from the conversation's most recent active thread, and state the inferred focus to the user in one line before continuing.

## Step 2: Locate the doc; decide create, enhance, or overwrite

Apply the detection algorithm in `$CLAUDE_PLUGIN_ROOT/skills/init/references/multi-repo-detection.md` to resolve the root. In a multi-repo workspace the handoff lives at the workspace root; otherwise at the repo/project root. The handoff folder is `docs/handoffs/` under that root.

Then branch:

- **`docs/handoffs/<slug>.md` exists** → read it, then use `AskUserQuestion` (header "Existing handoff", question "A handoff for this topic already exists. Enhance it or overwrite?"):
  - **Enhance** — "Merge new context; keep still-valid content and append a History line"
  - **Overwrite** — "Fresh rewrite; the prior version stays in git history"
- **No slug match, but `docs/handoffs/` holds other docs** → list them (filename · title · Last updated), then use `AskUserQuestion` (header "Existing handoffs", question "No handoff matches this topic. Continue an existing one or create new?"):
  - **Continue one** — pick a file via a follow-up `AskUserQuestion`, then treat it as **Enhance**
  - **Create new** — start a new handoff for this topic
- **Folder empty or absent** → create new.

## Step 3: Classify artifacts against version control

Resolve git state so the document references what survives on another clone and inlines what does not. Run, per repo (per child repo in a multi-repo workspace):

- `git rev-parse --show-toplevel` — if this fails it is not a git repo: skip the rest of this step, note "not a git repo" in **Origin**, and inline everything.
- `git rev-parse --abbrev-ref HEAD` and `git rev-parse --short HEAD` — branch and commit for **Origin**.
- `git status --porcelain` — modified / staged / untracked paths.
- `git ls-files <path>` — whether a given path is tracked.
- `git log --oneline @{upstream}..HEAD` — unpushed commits (fallback `origin/HEAD..HEAD`; no upstream or detached HEAD → treat local commits as unpushed).

Sort every artifact into three buckets:

1. **Tracked and pushed** → reference by repo-relative path / SHA / URL.
2. **Tracked-but-modified, staged-not-committed, or committed-not-pushed** → inline the relevant content (diff, file body, or commit message) — another clone will not have it.
3. **Untracked** → inline.

Qualify paths and SHAs with the repo name in a multi-repo workspace.

## Step 4: Draft or reconcile the document

Fill the embedded **Handoff document template** from what was actually discussed in this conversation.

- **New or overwrite** → write fresh.
- **Enhance** → preserve **Goal** and still-valid content; update **Current state** and **Next steps** to the latest reality (drop completed steps); add new decisions and artifacts; refresh **Last updated**; append one **History** line.

Rules:

- Never duplicate content that lives in a tracked artifact — reference it by path plus a one-line summary. Inline only bucket-2 and bucket-3 content from Step 3.
- Trust git state (Step 3) over chat memory when they conflict. If the current state is ambiguous, say so in one line rather than guessing.
- Keep the document tool-agnostic: refer to the resuming actor as "a fresh agent" or "a new session" — never name a specific AI product.

## Step 5: Redact inlined content

Scan everything you are about to **inline** (never paths or references) against the **Redaction patterns** table and replace matches with the exact marker `[REDACTED: <kind>]`, preserving structure — e.g. `DATABASE_URL=postgres://app:[REDACTED: password]@db:5432/app`.

A tracked-and-pushed file is referenced, never inlined — so a pushed secret is never copied in. Tracked-but-modified or committed-but-unpushed content is inlined (bucket 2) and must be redacted like any other inlined content. A file whose name looks like a secret (`.env`, `*.key`, `*.pem`, `*.pfx`, `credentials.*`, `secrets.*`, `*.sqlite`, `*.db` — the same set `/optimus:commit` warns about) is **never inlined with its values**, regardless of tracked state: reference it by path (if tracked) or by name with a "recreate from your secure source" note (if untracked or modified), adding a one-line caution. For text env files you may inline variable **names** only, never values; binary/opaque files (`*.pfx`, `*.sqlite`, `*.db`) are never inlined at all.

## Step 6: Build the Suggested skills section

Read `$CLAUDE_PLUGIN_ROOT/references/skill-handoff.md` for fresh-vs-continuation semantics. Apply the **Suggested skills — selection table** below against where this conversation left off, and render each suggestion self-contained:

- the exact `/optimus:<skill> <args>` command,
- a one-line why,
- an explicit note phrased **for the resumer** — e.g. "do the work in a fresh session, then run `/optimus:commit` in that same session."

Do **not** copy skill-handoff.md's verbatim "stay in this conversation" wording into the document — it presumes the original conversation, which is gone by the time the doc is read.

## Step 7: Write the document

Write the filled template to `docs/handoffs/<slug>.md` under the root resolved in Step 2, creating `docs/handoffs/` if missing. If the resolved root is a multi-repo workspace root that is not itself a git repo, the file is not under version control — flag this in Step 8.

## Step 8: Report and recommend

Report the written path. Tell the user the document is redacted and safe to commit, that any older handoffs in the folder remain (this is the latest for its topic), and — if Step 7 flagged an untracked workspace root — that the doc is not yet under version control, suggesting they commit it inside a child repo or initialize version control at the root.

Recommend `/optimus:commit` so the handoff reaches the remote and other machines. Then choose the closing tip from `$CLAUDE_PLUGIN_ROOT/references/skill-handoff.md` based on what Step 6 produced:

- **If Step 6 emitted at least one non-continuation skill** → emit **Variant B** verbatim, substituting `<continuation-skill(s)>` with `/optimus:commit` and `<non-continuation-examples>` with those non-continuation skills.
- **If Step 6 emitted only continuation skills (e.g. `/optimus:commit`, `/optimus:pr`)** → emit **Variant A** verbatim, substituting `<continuation-skill(s)>` with `/optimus:commit` joined to Step 6's continuation skills via "and" (e.g. `` `/optimus:commit` and `/optimus:pr` ``) and `<non-continuation-examples>` with illustrative examples (`/optimus:code-review`, `/optimus:unit-test`).

Either way, omit Step 6's continuation skills (`/optimus:commit`, `/optimus:pr`) from the `<non-continuation-examples>` slot.

## Handoff document template

Minimal-but-complete; omit any section with nothing to say. Ordering follows a cold reader's path: orient (Goal, Current state) → act (Next steps) → reference (artifacts, skills).

````markdown
# Handoff: <short title of the work>

- **Created:** <YYYY-MM-DD> · **Last updated:** <YYYY-MM-DD>
- **Origin:** <repo> @ `<branch>` · commit `<short-sha>` (<pushed | NOT pushed>)
- **Focus for next session:** <one line — from the user's args if provided, else inferred>
- **How to use this doc:** You are resuming this work cold. Read top to bottom; everything you
  need is here or linked by repo-relative path. Then begin at Next steps item 1.

## Goal
<1-3 sentences: the outcome we are driving toward, and why. The destination, not a task list.>

## Current state
<2-6 bullets: what is done, what works, what is in progress, what is blocked.>

**Constraints that gate the next step** (omit if none):
- <e.g. API contract frozen — see docs/adr/0007-api.md>
- <e.g. must stay on Node 18; do not bump>

## Next steps
1. <Concrete first action — the thing to do on resume.>
2. <Next action.>

## Relevant files & artifacts
> Committed/tracked → referenced by repo-relative path / SHA / URL.
> Uncommitted or unpushed → content inlined below (won't exist on another machine).

- `path/to/file.ts` — <why it matters> (tracked)
- ADR/PRD: `docs/adr/0007-api.md` — <one-line relevance> (tracked)
- Issue/PR: <URL> — <relevance>
- Commit: `<short-sha>` <subject> (pushed)

### Inlined (not yet on remote) — omit if none
```diff
<minimal relevant uncommitted diff / new-file body / unpushed commit message, secrets redacted>
```

## Suggested skills
1. `/optimus:<skill> <args>` — <why> — <start a fresh session | run in your resuming session>.
2. <…>

## History (most recent first)
- <YYYY-MM-DD>: <one-line summary of what this session changed>

---
**Resume here:** start a fresh session with any AI agent in this repo, open this file, and begin at Next steps item 1.
````

## Suggested skills — selection table

Pick the first matching row top-to-bottom; emit its skills in order.

| Conversation state | Suggest, in order | Note for the resumer |
|---|---|---|
| Design/plan written, no code | `/optimus:tdd` | fresh session |
| Requirements unclear / need a design | `/optimus:brainstorm` | fresh session |
| JIRA/issue context needed first | `/optimus:jira PROJ-123` | fresh session |
| Code written, **not committed** | `/optimus:commit` → `/optimus:pr` | run both in your resuming session (they capture your reasoning) |
| Code committed, **no PR** | `/optimus:pr` | run in your resuming session |
| PR open, not reviewed | `/optimus:code-review` | fresh session |
| Review feedback applied | `/optimus:commit` → `/optimus:pr` (update) | run in your resuming session |
| Tests thin/missing | `/optimus:unit-test` | fresh session |
| Refactor pending (post-green) | `/optimus:refactor` | fresh session |
| Need isolated branch/worktree | `/optimus:branch` or `/optimus:worktree` | fresh session |
| Project not set up for AI dev | `/optimus:init` | fresh session |
| Run/onboarding docs missing | `/optimus:how-to-run` | fresh session |

**Subtlety:** the canonical chain is implement → `/optimus:commit` → `/optimus:pr` → `/optimus:code-review`. The "stay in this conversation" advice for continuation skills exists so intent is captured from the *implementation* conversation — but the handoff is read by a fresh agent in a new conversation, so the resumer cannot stay in the original. Render continuation skills as "do the work, then run `/optimus:commit` in that same session," never the verbatim "stay in this conversation" tip.

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
