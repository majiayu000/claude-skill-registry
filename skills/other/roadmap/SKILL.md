---
name: roadmap
description: >
  · Capture, track, and prioritize ideas in gitignored ROADMAP.md. Triggers: 'roadmap',
  'ideas', 'feature ideas', 'competitive analysis', 'what should I build', 'feature backlog'.
  Not for project management or code review.
license: MIT
compatibility: "Requires git. Optional: gh (GitHub CLI) or glab (GitLab CLI) for PR tracking and competitive scanning"
metadata:
  source: iuliandita/skills
  date_added: "2026-04-05"
  effort: medium
  argument_hint: "[ideas... | update | scan <repo-url> | review]"
---

# Roadmap: Lightweight Project Idea Tracker

Manage a project's feature backlog in a gitignored ROADMAP.md. Quick idea capture, progress
tracking after PRs and releases, competitive intelligence from similar repos, and periodic
review to keep priorities honest.

Not a project management system. No phases, no execution plans, no milestones. Just a
scratchpad that evolves with the project.

## When to use

- Capturing feature ideas, brainstorms, or "what if" thoughts for a project
- Tracking which ideas shipped via PRs or releases
- Scanning competing or similar repos for feature inspiration
- Reviewing and prioritizing the idea backlog
- Bootstrapping a fresh ROADMAP.md for a project that doesn't have one
- User says "add to roadmap", "what should I build next", or "what are competitors doing"

## When NOT to use

- Structured project management with phases, milestones, execution plans
- Sprint or iteration planning with task dependencies
- Code review or PR review - use **code-review**
- Writing project docs or READMEs - use **update-docs**
- Factual drift in `ROADMAP.md` itself (stated version mismatch, shipped highlights out of date, `[planned]` / `[exploring]` items that already shipped) - use **update-docs**. This skill owns prioritisation and idea capture; update-docs owns keeping the file's stated facts honest.
- Tracking bugs or incidents - use issue trackers directly

---

## AI Self-Check

Before writing or modifying ROADMAP.md, verify:

- [ ] **Gitignored**: ROADMAP.md is in .gitignore (or user explicitly opted out of gitignoring)
- [ ] **No secrets**: entries don't contain API keys, internal URLs, or sensitive business info
- [ ] **Attribution preserved**: competitive intel cites the source repo or project
- [ ] **No duplicates**: new ideas don't repeat existing entries (check intent, not just wording)
- [ ] **Format preserved**: edits work within the existing file structure - don't reformat
      sections the user didn't ask to change
- [ ] **Shipped items attributed**: completed entries reference the PR, release, or commit
- [ ] **No hallucinated competitive data**: every feature, issue count, or user demand claim
      from a competitor repo is backed by an actual link or quote - not inferred
- [ ] **No priority inflation**: P0 items are genuine blockers, not aspirational wishes
- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Routing overlap checked**: overlapping skills, trigger terms, and "When NOT to use" boundaries are checked before returning guidance
- [ ] **Spec claims verified**: claims about tool behavior, output contracts, or repo conventions are checked against current docs, scripts, or skill files
- [ ] **Evidence quality marked**: competitive intel, user feedback, and assumptions are labeled with source and confidence
- [ ] **Backlog hygiene kept**: stale ideas are parked or deleted instead of endlessly reprioritized

## Roadmap Format

### Sections (fixed order)

Every ROADMAP.md uses these sections in this order. Empty sections can be omitted
but the order is not negotiable - consistency makes the file scannable. When adding
content to a previously omitted section, create it in the canonical position relative
to existing sections.

```markdown
# Roadmap

> Project: {name} | Updated: {date} | Current: v{version}
> Local planning doc, gitignored. Not a commitment.

## Snapshot

{1-2 paragraphs: project state, what the next milestone means, current focus}

## Exit Criteria

What "done" means for the next milestone. Each criterion has a verdict.

### {Criterion Name}

**Verdict**: Pass | Fail | Partial

- {Requirement}
- {Requirement}

## Now - P0

Blocks the next milestone or release. Active work only.

- [in-progress] {Description} - {area} | PR #{n}
- [planned] {Description} - {area}

## Next - P1

Committed direction. Happens after Now is clear.

- [planned] {Description} - {area}
- [exploring] {Description} - {area}

## Later - P2

Good ideas, no timeline. Revisit during review.

- {Description} - {context}

## Experiments

Low confidence. Build only with real demand signal.

- {Description} - {what would validate it}

## Shipped

### v{X.Y.Z} ({date})

- ~~{Description}~~ - {area} | PR #{n}, v{X.Y.Z} ({date})

## Competitive Intel

### {owner/repo}

- {Feature} ({relevant | weak signal | noise}) - {evidence}
- User demand: {issue links, discussion quotes, vote counts}

## Parked

Items deferred with reason.

- {Description} - {reason for parking}
```

### Item format

Items have two tiers depending on where they live:

**Active items (Now, Next)** - structured, with status and tracking:
```
- [status] Description - area | tracking
```

Status values: `exploring`, `planned`, `in-progress`

Area values are project-specific shorthand for the component or domain (e.g., `ui`,
`api`, `backend`, `infra`, `docs`, `auth`). Infer from the project's structure. If
unclear, omit the area rather than guessing.

**Backlog items (Later, Experiments)** - lightweight, quick capture:
```
- Description - context or source
```

Items gain structure as they're promoted. A quick idea in Later becomes a tracked
item when it moves to Next.

**Shipped items** always get attribution:
```
- ~~Description~~ - area | PR #N (or MR #N), vX.Y.Z (date)
```

### When a ROADMAP.md already exists

Read the existing structure first. If it doesn't match this format:
- In **add** or **update** modes: work within the existing structure, don't restructure
- In **review** mode: suggest migrating to this format if the current one is disorganized
- If the user asks to restructure: migrate section by section, preserving all content

---

## Performance

- Keep roadmap edits small and frequent; avoid rewriting the whole backlog for one new idea.
- Limit active P0/P1 items so prioritization remains meaningful.
- Group duplicate ideas and link evidence instead of copying long notes repeatedly.

---

## Best Practices

- Tie each near-term item to a clear user, business, or technical outcome.
- Record exit criteria before implementation starts.
- Separate commitments from experiments so speculative work does not crowd delivery.

---

## Workflow

### Step 0: Activity Detection (runs on every invocation)

If no ROADMAP.md exists yet or no recent activity is found, skip silently.

Otherwise, check for recent project activity:

```bash
# Detect forge CLI: gh (GitHub), glab (GitLab), or git-only fallback
# GitHub
gh pr list --state merged --limit 10 \
  --json number,title,mergedAt 2>/dev/null
# GitLab
glab mr list --state merged --per-page 10 2>/dev/null

# Always available (portable - no GNU date required)
git tag --sort=-creatordate 2>/dev/null | head -5
git log --oneline --since="2 weeks ago" 2>/dev/null | head -15
```

If neither `gh` nor `glab` is available, note it once ("PR tracking unavailable -
install gh or glab for full coverage") and continue with git-only data (tags + commits).

If merged PRs or new releases look like they match open roadmap items, mention it
briefly before proceeding:

> "Heads up: PR #142 and v0.15.0 landed since the last roadmap update.
> Want me to check those off first, or continue with {requested mode}?"

Don't block. If the user ignores it, proceed with their request.

---

### Mode 1: Add Ideas (default)

Trigger: user throws ideas at the project, says "add to roadmap", or describes features.

#### Step 1: Bootstrap if needed

1. Check if ROADMAP.md exists in the project root (in monorepos, default to the git
   root unless the user specifies a package - if multiple ROADMAP.md files exist, ask)
2. If not, create it using the starter structure. Read the project's README, package.json,
   or equivalent to fill in the Snapshot section with real context
3. Check if ROADMAP.md is in .gitignore - if not, add it:
   ```
   # Project roadmap (local planning doc)
   ROADMAP.md
   ```
   Inform the user: "Added ROADMAP.md to .gitignore. Remove the entry if you want it tracked."

#### Step 2: Parse and place ideas

Extract actionable items from the user's input. For each idea:
- Write a clear, concise description (keep the user's voice - clean up only if unclear)
- Place it in the right priority tier (ask if genuinely ambiguous, default to P1)
- Add context: where the idea came from, what it enables, any constraints mentioned

Append to the appropriate section. Don't reorder existing items.

#### Step 3: Offer competitive scan

If the roadmap has no competitive intel section and this is the first batch of ideas, ask:

> "Want me to scan similar repos for feature ideas that might fit {project-name}?"

Ask once per session. If declined, don't ask again.

---

### Mode 2: Update / Check Off

Trigger: user says "update roadmap", asks to check off items, or after a PR merge / release.

If no ROADMAP.md exists, redirect to Mode 1 (bootstrap) first.

#### Step 1: Gather recent activity

```bash
# Always available (portable - no GNU date required)
git log --oneline --since="2 weeks ago" 2>/dev/null
git tag --sort=-creatordate 2>/dev/null | head -5

# GitHub
gh pr list --state merged --limit 20 \
  --json title,number,mergedAt 2>/dev/null
# GitLab
glab mr list --state merged --per-page 20 2>/dev/null
```

Adjust the time range if the user specifies one. If the user names specific PRs
directly (e.g., "PR #45"), fetch those with `gh pr view 45 --json title,mergedAt`
(or `glab mr view 45`) instead of relying on the time-windowed list.

#### Step 2: Match activity to roadmap items

Compare commit messages, PR titles, and release notes against open roadmap items.
Use semantic matching - "add dark mode support" matches "Dark mode theme option".

Present matches to the user before making changes:

> Found these potential matches:
> - PR #142 "Add dark mode toggle" -> matches "Dark mode theme option" (P1)
> - v0.15.0 release includes backup/restore -> matches "Backup and restore" (P0)
>
> Check these off?

#### Step 3: Update the file

If the user already stated which items shipped (e.g., "PR #45 adds dark mode"),
treat that as pre-confirmed - present the planned changes for review rather than
re-asking "check these off?"

For confirmed matches:
1. Apply strikethrough: `~~description~~`
2. Add attribution: `-- PR #N, vX.Y.Z (date)` (include both when a PR and release apply)
3. Move to the "Shipped" section (create it if missing), grouped by version or date

Update the "Last updated" line in the header.

---

### Mode 3: Competitive Scan

Trigger: user asks to scan competitors, provides repo URLs, or accepts the Mode 1 offer.

Read `references/competitive-scan.md` for target selection, forge CLI commands, strict
fit filtering, approval flow, and Competitive Intel formatting.

---

### Mode 4: Review / Prioritize

Trigger: user asks to review the roadmap, prioritize, or "what should I work on next".

#### Step 1: Load and summarize

Read ROADMAP.md. Present a summary:
- Item counts by priority tier
- Items currently in progress (if tracked)
- Recently shipped items
- Stale items: items untouched for 60+ days are candidates for archival or re-prioritization
  (use git blame or file modification dates to estimate age)

#### Step 2: Suggest actions

Based on the current state, flag any of these:
- **P0 items not being worked on** - supposed to be urgent; needs explanation or demotion
- **Items untouched 60+ days** - park with reason or promote; sitting isn't a priority
- **Related items scattered across tiers** - group into a cohesive effort
- **Shipped items still in active sections** - move to Shipped
- **Missing structure** - suggest organizational improvements

#### Step 3: Offer structural improvements

If the roadmap lacks clear organization, suggest improvements:
- Adding priority tiers if everything is a flat list
- Separating product work from promotion/go-to-market
- Adding a Snapshot section for project context
- Adding exit criteria for major milestones
- Creating an Experiments section for low-confidence ideas

Present suggestions. Apply only what the user approves.

#### Step 4: Apply changes

With user approval, reorganize, re-prioritize, park, or remove items. Never delete
silently - move to **Parked** with a reason, or confirm deletion explicitly.

---

## Reference Files

- `references/trigger-integration.md` - optional auto-trigger setup for Claude Code hooks,
  GitHub Actions, and git hooks. Read this when the user wants push-based roadmap updates
  instead of (or in addition to) the built-in activity detection.
- `references/competitive-scan.md` - competitor/repo scan workflow, evidence thresholds,
  and ROADMAP.md Competitive Intel formatting.

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** ROADMAP
- **Deliverable bucket:** `deliverables`
- **Mode:** conditional. When invoked to **analyze, review, audit, or improve** an existing roadmap (e.g., "review my ROADMAP.md"), emit the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table - and write the deliverable to `docs/local/deliverables/roadmap/<YYYY-MM-DD>-<slug>.md`. When invoked to **build or update a roadmap** (its primary mode, writing to the user's working-directory `ROADMAP.md`), respond freely without the contract; build-mode output goes to `ROADMAP.md` in the working directory, not to `docs/local/`.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Related Skills

- **browse** - competitive scan (Mode 3) may use browse for reading competitor repos
  and documentation when web fetch alone isn't sufficient
- **git** - update mode (Mode 2) reads git history and PR data to match shipped work
- **code-review** - reviews code correctness. This skill tracks what to build;
  code-review evaluates the code that implements it
- **update-docs** - updates project documentation AND audits ROADMAP.md for factual drift
  (header version, shipped highlights, items that already shipped but still listed as planned).
  This skill owns prioritisation, capture, and competitive intel; update-docs owns keeping
  the file's facts in sync with HEAD. Boundary: ideas + sequencing here, factual freshness there.

## Rules

1. **Gitignore by default.** Ensure ROADMAP.md is in .gitignore before creating or writing it.
   Skip only if the user explicitly asks to track it in git.
2. **Don't rewrite the file.** Edits are additive or targeted. Don't reformat, reorder, or
   restructure sections the user didn't ask to change.
3. **Attribute competitive intel.** Every idea from another repo gets a source tag. Never
   present external features as original ideas.
4. **Ask before checking off.** Present matches and let the user confirm. Don't auto-complete
   roadmap items based on fuzzy matches alone.
5. **One offer per session.** Ask about competitive scanning at most once. If declined, drop it.
6. **No priority inflation.** Default to P1 when priority is unclear. P0 is reserved for
   genuine blockers, not aspirational items.
7. **Preserve user voice.** Keep the user's phrasing when adding ideas. Clean up only when
   genuinely unclear.
8. **Work within existing structure.** If a ROADMAP.md exists, adapt to its format. Suggest
   structural changes through review mode, not silently during adds or updates.
9. **Headless mode.** In non-interactive contexts (`--bare`, Cursor Automations, Codex
   `exec`): skip confirmation prompts, apply only exact matches in Mode 2, add only
   strong-signal items in Mode 3, and don't offer competitive scans in Mode 1.
