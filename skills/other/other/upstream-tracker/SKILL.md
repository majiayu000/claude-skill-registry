---
name: upstream-tracker
description: "Manage upstream issue tracking for this project. Use when the user wants to log a bug or friction point in a vendor package or npm dependency, review open upstream items, resolve a tracked issue, run a trend review, generate the upstream observations section of a sprint retrospective, promote upstream observations to Basic Memory, or discover known friction from other projects. Trigger phrases: 'upstream', 'track this', 'vendor issue', 'log this bug', 'review upstream', 'trend review', 'cross-vendor', 'this is a bug in X', 'promote to memory', 'promote upstream', 'sync from memory', 'known friction', 'resolved upstream', 'mark as fixed', 'tool issue', 'action bug', or any mention of friction with an external package."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - mcp__basic-memory__search_notes
  - mcp__basic-memory__read_note
  - mcp__basic-memory__edit_note
---

# Upstream Tracker

Manage the `UPSTREAM-*.md` files that track bugs, feature requests, and friction
discovered in upstream packages while building this project.

## Tracking Files

### Vendor packages (permanent files)

Vendor packages are declared in `.claude/vendor-registry.json` (if it exists) as
an array of `{prefix, remote, branch, package}` objects, or as packages listed under
`workspaces` in `package.json`. Each vendor package gets a permanent
`UPSTREAM-<package-name>.md` tracking file that always exists, even when empty.

To discover which packages are vendors, read `.claude/vendor-registry.json` if
it exists, or inspect `package.json` workspaces. If neither is present, ask the
user which packages should be treated as permanent vendor fixtures.

### Non-vendor dependencies (ephemeral files)

Any npm dependency can get an `UPSTREAM-<package>.md` file when you encounter a
bug or limitation worth tracking (e.g., `UPSTREAM-umzeption.md`). Create the
file on first encounter. **Delete the file entirely once all its entries are
resolved** — there's no reason to keep an empty tracking file for a regular
dependency. To discover existing non-vendor files, glob for `UPSTREAM-*.md` and
exclude the known vendor files.

### Non-npm tools (ephemeral files)

Tools in the project's environment (Homebrew formulae, GitHub Actions, Docker
images, VSCode extensions) can also accumulate friction worth tracking. Create
an `UPSTREAM-<tool-type>--<name>.md` file on first encounter, using the same
ephemeral pattern: delete when all entries are resolved. See the file naming
convention in the Guidelines section for the tool-type prefix format.

### Shared structure

All upstream files share the same structure:
**Feature Requests** | **Bugs** | **Cross-Vendor Inconsistencies** | **Trend Reviews**

Non-vendor files typically only use **Feature Requests** and **Bugs** sections
(cross-vendor inconsistencies only apply when multiple vendor packages share an
API surface).

## Workflows

Determine which workflow the user needs based on their request. If ambiguous,
default to the most likely workflow based on context.

### 1. Log a new entry

When the user encounters upstream friction — a bug, a missing feature, an
awkward API, or a cross-vendor inconsistency — add it to the correct file.
Infer the details from the current conversation context: what code was being
written, what error occurred, what workaround was needed. The user shouldn't
have to re-explain something that's already visible in the session.

**Steps:**

1. Identify which upstream package is involved from the conversation context
   (the code being discussed, the error encountered, or the workaround applied).
   This can be a vendor package OR a regular npm dependency. This can also be a
   non-npm tool — a Homebrew formula, a Homebrew cask, a GitHub Action, a Docker
   image, or a VSCode extension. Use the `brew:<name>`, `cask:<name>`,
   `action:<owner>/<repo>`, `docker:<image>`, or `vscode:<ext>` prefix notation
   when identifying tools (consistent with `/tool-intel` from vp-knowledge).
1a. **Basic Memory pre-check.** If Basic Memory MCP tools are available, call
   `mcp__basic-memory__search_notes` with the package name. If a matching note
   exists and contains an `## Upstream Friction` section with entries related to
   the issue being logged, surface them to the user: "This friction is already
   tracked in Basic Memory from another project: \[summary]. Logging it locally
   as well so this project tracks it." Proceed regardless — this is informational,
   not a gate. If Basic Memory tools are not available, skip this step silently.
2. If the package is a non-vendor dependency and no `UPSTREAM-<package>.md`
   file exists yet, create it with this template:

   ```markdown
   ## Feature Requests

   _No entries yet._

   ## Bugs

   _No entries yet._
   ```

   Non-vendor files typically omit Cross-Vendor Inconsistencies and Trend
   Reviews sections unless the project uses multiple vendor packages sharing
   an API surface.
3. Classify the entry:
   - **Bug** — unexpected behavior, something that doesn't work as documented
   - **Feature Request** — a missing capability the package should have
   - **Cross-Vendor Inconsistency** — a pattern, convention, or API that one
     vendor package supports but another doesn't, creating friction for the
     consumer. Relevant when multiple vendor packages share an API surface.
4. Read the target `UPSTREAM-*.md` file
5. Compose the entry from the consumer app's perspective (focus on impact, not internals)
6. Add the entry under the correct section heading, using today's date

**Entry format for Feature Requests:**

```
- **Short title** (YYYY-MM-DD) — Description of the desired behavior and why
  it matters for the consuming app. [upstream: <url>]
  Ownership: upstream|us|shared · Workaround: none|partial|full — description
```

Upstream URL is optional — add if you've filed a feature request upstream.

**Entry format for Bugs:**

```
- **Short title** (YYYY-MM-DD) [blocking|degraded|minor] — What happens, how to
  reproduce, and the expected behavior. [upstream: <url>]
  Severity: blocking|degraded|minor · Ownership: upstream|us|shared · Workaround: none|partial|full — description
```

Severity tag in brackets is optional — use `blocking` (no workaround), `degraded`
(workaround exists but costly), or `minor` (edge case). Upstream URL is optional —
add if you file an issue or PR upstream.

**Entry format for Cross-Vendor Inconsistencies:**

```
- **Short title** (YYYY-MM-DD) — What the sibling package does, what this
  package lacks, and the consumer-side friction it causes.
  Ownership: upstream|us|shared · Workaround: none|partial|full — description
```

**Structured fields** (all optional — existing entries without them remain valid):

| Field | Values | When to use |
|-------|--------|-------------|
| `Severity:` | `blocking` · `degraded` · `minor` | Bugs only. How much this hurts day-to-day development. `blocking` = no workaround, `degraded` = workaround exists but costly, `minor` = edge case or minor inconvenience |
| `Ownership:` | `upstream` · `us` · `shared` | All entry types. Who needs to act: `upstream` = waiting on a release, `us` = we need to adapt or contribute a fix, `shared` = both sides need changes |
| `Workaround:` | `none` · `partial` · `full` — description | All entry types. `none` = no mitigation, `partial` = mitigation exists but incomplete, `full` = fully mitigated (describe how). Helps prioritize: entries with `none` are more urgent |

These fields go on a continuation line below the entry's main description line,
indented to match. They are metadata for triage and trend review — the main
description line remains the primary content. Omit fields that don't add useful
signal (e.g., skip `Workaround: none` when the severity already says `blocking`).

When adding the first entry to a section, replace the `_No entries yet._`
placeholder. Keep entries concise — 1-3 sentences. The title should be
scannable (e.g., "Missing session type export", not "Issue with types").

If the logged observation looks generalizable beyond this project (about the
package's behavior, not a project-specific integration choice), note that
workflow 6 (Promote to Basic Memory) can share it across projects later.

### 2. Review open items

Summarize the current state of all upstream tracking files (vendor and non-vendor).

**Steps:**

1. Glob for all `UPSTREAM-*.md` files and read them
2. Present a summary grouped by file, showing counts and listing open items
3. Flag anything that looks stale (older than ~3 months with no activity)

**Output format:**

```markdown
## Upstream Status

### <package-name>

- Feature Requests: N open
- Bugs: N open
- [list each with title and date]

### Notes

- [any stale items or observations]
```

If all files are empty, say so and suggest checking whether any known friction
points should be captured.

### 3. Resolve an entry

When an issue has been fixed upstream, simply delete it from the tracking
file. There's no need to keep resolved entries — the version control history
preserves what was tracked and when it was removed.

**Steps:**

1. Read the relevant `UPSTREAM-*.md` file
2. Find the entry (by title or user description)
3. Delete the entry from its section
4. For vendor files: if the section is now empty, restore the `_No entries yet._`
   placeholder
5. For non-vendor files: if the file has no remaining entries, **delete the
   file entirely** (`git rm`)
6. Mention the resolution in your commit message so the git log captures it
7. **Basic Memory annotation.** If Basic Memory MCP tools are available, call
   `mcp__basic-memory__search_notes` for the package name. If a matching note
   exists, call `mcp__basic-memory__read_note` to get its exact content. If the
   note has an `## Upstream Friction` section containing the resolved entry,
   call `mcp__basic-memory__edit_note` with `find_replace` to append
   `_(Resolved YYYY-MM-DD)_` to the entry's line. Match against the note's
   exact text from `read_note` — do not construct match strings from memory.
   **Annotate, never delete** — only workflow 6 (Promote to Basic Memory) moves
   entries to the `### Resolved` subsection during its prune pass. If no matching
   Basic Memory entry exists (it was never promoted), skip silently. If Basic
   Memory tools are not available, skip silently.

### 4. Trend review (quarterly)

Every 4th sprint, perform a cross-cutting analysis of all tracking files.

**Steps:**

1. Glob for all `UPSTREAM-*.md` files and read them
2. Analyze open items for common themes (e.g., recurring type export issues,
   similar API gaps across packages)
3. Look for cross-vendor inconsistencies — patterns or APIs that one vendor
   package supports but its siblings don't yet
4. Evaluate continued validity — are any open items obsolete or already
   addressed? Delete resolved items (they're preserved in git history).
5. Identify items that should be escalated, using these empirical timelines as
   guidance:
   - **Bugs** typically resolve in 5–10 sprints; items beyond 10 sprints warrant
     escalation (upstream PR, issue, or workaround acceptance)
   - **Feature requests** typically take 10–20 sprints; items beyond 20 sprints
     may never land — consider permanent workarounds or forks
   - **Cross-vendor inconsistencies** often resolve only on a next major version;
     track with low urgency unless actively blocking development
6. Add a Trend Review entry to each file's **Trend Reviews** section
7. Delete non-vendor UPSTREAM files that have no remaining open entries
8. Present findings to the user
9. **Promotion candidates.** Flag entries that have been open across multiple
   trend reviews AND have `Ownership: upstream` or `shared` — these are strong
   candidates for workflow 6 (Promote to Basic Memory). Suggest running it if
   any are found.

**Trend Review entry format:**

```
### Review — YYYY-MM-DD (Sprint N)

- **Themes:** [common patterns across open items]
- **Still valid:** [items confirmed as still relevant]
- **Recommend closing:** [items that are obsolete or low-priority]
- **Escalate:** [items past their expected resolution window — include upstream URL if filed]
```

### 5. Sprint retrospective support

Help generate the "Upstream observations" section of a sprint retrospective.

**Steps:**

1. Read all `UPSTREAM-*.md` files to understand current state
2. Review the conversation history for any vendor friction encountered during
   the session — workarounds, type issues, missing APIs, confusing behavior
3. Log any untracked items discovered from context (workflow 1)
4. Draft the upstream observations section for the retro
5. Note any entries that appear generalizable beyond this project — the
   retrospective may want to chain into workflow 6 (Promote to Basic Memory)
   after the retro is written.

### 6. Promote to Basic Memory

Promote generalizable upstream friction observations from project-local
UPSTREAM files into cross-project Basic Memory entity notes. This creates an
`## Upstream Friction` section in the target entity note (e.g., `npm/<package>`,
`brew/<name>`, `actions/<owner>/<repo>`). Use only MCP tools from this skill's
`allowed-tools` — `mcp__basic-memory__search_notes`, `mcp__basic-memory__read_note`,
`mcp__basic-memory__edit_note`. If Basic Memory MCP tools are not available,
report that promotion is unavailable and suggest checking Basic Memory manually.

**Steps:**

1. **Scan for candidates.** Glob all `UPSTREAM-*.md` files and read them.
   Identify entries that meet ALL of these criteria:
   - `Ownership:` is `upstream` or `shared` (skip `us` entries — those are
     integration choices, not package friction)
   - The observation is about the package/tool itself, not about how this
     specific project uses it
   - The entry has enough detail to be useful without project context
   - When ownership is absent, default to promoting unless clearly
     project-specific
2. **Present candidates to the user.** For each candidate, show:
   - Package or tool name and target type (npm, brew, cask, action, etc.)
   - Entry title and classification (Bug / Feature Request)
   - A draft generalized version with project-specific file paths stripped
   - Whether a Basic Memory note already exists for this package/tool
   Let the user approve, edit, or skip each candidate. Never auto-promote.
3. **Route by target type.** Search Basic Memory for an existing entity note
   using the routing table in `references/basic-memory-friction-format.md`.
4. **Write or flag.** For each approved candidate:
   - **Note exists, has `## Upstream Friction`** — call `mcp__basic-memory__edit_note`
     with `find_replace` to append the entry under the correct subsection
     (`### Bugs` or `### Feature Requests`). Anchor the match text to include
     the next `###` heading for uniqueness. Use `expected_replacements=1`.
     Always call `mcp__basic-memory__read_note` first and match against its
     exact text.
   - **Note exists, no `## Upstream Friction`** — call `mcp__basic-memory__edit_note`
     with `insert_before_section` on `Relations` to add the full
     `## Upstream Friction` section with the entry.
   - **No note exists** — do NOT create a thin note. Flag for enrichment:
     "No Basic Memory note for `<package>`. Run `/package-intel <package>`
     (or `/tool-intel <tool>` for non-npm tools) to create one, then re-run
     workflow 6 to attach friction entries."
   - Deduplicate by entry title before appending — if the entry title already
     appears in the friction section, skip it.
   - See `references/basic-memory-friction-format.md` for `edit_note` gotchas.
5. **Prune pass.** For entries in the Basic Memory note's `## Upstream Friction`
   section that are annotated with `_(Resolved ...)_`, offer to move them to
   the `### Resolved` subsection. The user confirms each. This is the only
   path that moves entries to Resolved — workflow 3 only annotates.
6. **Report.** Summarize what was promoted, pruned, skipped, and flagged for
   enrichment. Suggest verifying notes with
   `build_context("memory://npm/<package>")`.

See `references/basic-memory-friction-format.md` for the target section structure,
generalization transform rules, and `edit_note` gotchas.

**Division of labor:** This workflow owns the `## Upstream Friction` section of
entity notes in Basic Memory. The retrospective skill's step 7 owns
`engineering/*` notes (patterns, conventions, lessons). They do not overlap —
upstream friction is package-specific, learnings are domain-specific. For
upstream friction about specific packages or tools, use this workflow, not the
retrospective.

### 7. Sync from Basic Memory

Discover friction already known in Basic Memory for packages and tools this
project depends on, but not yet tracked in local UPSTREAM files. This is the
reverse of workflow 6 — it pulls cross-project knowledge into the current
project. If Basic Memory MCP tools are not available, report that sync is
unavailable and suggest checking Basic Memory manually.

**Steps:**

1. **Identify project dependencies.** Read `package.json` (for npm deps and
   workspace entries) and `.claude/vendor-registry.json` (for vendor packages).
   Build a list of packages and tools to check.
2. **Query Basic Memory.** For each dependency, call
   `mcp__basic-memory__search_notes` with the package name. Filter results to
   notes that contain an `## Upstream Friction` section with active (non-resolved)
   entries.
3. **Cross-reference with local UPSTREAM files.** For each Basic Memory friction
   entry found, check whether the project already has a matching entry in a
   local `UPSTREAM-*.md` file.
4. **Surface unknown friction.** Present entries found in Basic Memory but not
   tracked locally: "Basic Memory has known friction for `<package>` not tracked
   in this project: \[entry title — summary]. Want to add it to your UPSTREAM
   file?"
5. **Flag missing notes.** For packages that have UPSTREAM entries locally but
   no Basic Memory note, suggest `/package-intel <package>` or
   `/tool-intel <tool>` for enrichment — this enables future promotion via
   workflow 6.
6. **User decides.** For each surfaced entry: add to local UPSTREAM file (via
   workflow 1's logging steps), skip, or dismiss. The user stays in control.

This workflow is pull-based, not automatic. Invoke it when starting a new sprint,
onboarding to a project, or when you want cross-project awareness of known
friction patterns.

## Guidelines

- **File naming convention.** Use `UPSTREAM-<package-name>.md` with slashes
  replaced by `--`. Scoped packages drop the `@` prefix: `@voxpelli/typed-utils`
  becomes `UPSTREAM-voxpelli--typed-utils.md`, `umzeption` stays
  `UPSTREAM-umzeption.md`. For non-npm tools, prefix with the tool type:
  `UPSTREAM-brew--ripgrep.md`, `UPSTREAM-cask--docker.md`,
  `UPSTREAM-action--actions--checkout.md`, `UPSTREAM-docker--node.md`,
  `UPSTREAM-vscode--dbaeumer.vscode-eslint.md`.
- **Infer from context.** When the user asks to log an issue, look at what
  just happened in the session. Extract the relevant details — the package
  involved, the nature of the problem, the workaround used — rather than
  asking the user to repeat themselves.
- **Consumer perspective.** Write entries from the consuming app's point of view.
  Focus on impact: "Can't type-check session objects in route handlers" rather
  than "Missing type export in index.d.ts".
- **Package identification.** When unsure which package an issue belongs to,
  check package documentation or README, or trace the code that triggered the
  friction back to its source. For non-vendor packages, check `package.json`
  dependencies.
- **Cross-vendor awareness.** When logging an entry, consider whether it's
  really a cross-vendor inconsistency. If the project uses multiple vendor
  packages that share an API surface, file the entry against the package that
  needs to change.
- **Keep files lean.** Delete resolved entries — they're preserved in git
  history. No duplicate entries, no stale placeholders mixed with real entries.
  For non-vendor files, delete the file itself when all entries are resolved.
- **Basic Memory integration.** Workflows 1 and 3 check and annotate Basic
  Memory entries opportunistically when MCP tools are available. Workflows 6
  and 7 are dedicated Basic Memory operations — they require the MCP tools to
  function and will report unavailability if the tools are missing.
