---
name: release
description: 'Prepare release communication and check release readiness. Modes — notes (writes PUBLIC-NOTES.md), changelog (prepends CHANGELOG.md), summary (internal brief), migration (breaking-changes guide), prepare (full pipeline: audit → notes + changelog + summary + migration if breaking changes), audit (pre-release readiness check: blockers, docs alignment, version consistency, Common Vulnerabilities and Exposures (CVEs)). Use whenever the user says "prepare release", "write changelog", "what changed since v1.x", "prepare v2.0", "write release notes", "am I ready to release", "check release readiness", or wants to announce a version to users.'
argument-hint: <mode> [range] | migration <from> <to> | prepare <version> | audit [version]
allowed-tools: Read, Write, Bash, Grep, Glob, TaskCreate, TaskUpdate
---

<objective>

Prepare release communication based on what changed. The output format adapts to the audience and context — user-facing release notes, a CHANGELOG entry, an internal release summary, or a migration guide for breaking changes.

</objective>

<inputs>

Mode comes **first**; range or version follows:

| Invocation                       | Arguments                                    | Writes to disk                                                                              |
| -------------------------------- | -------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `/release notes [range]`         | optional git range (default: last-tag..HEAD) | `PUBLIC-NOTES.md`                                                                           |
| `/release changelog [range]`     | optional git range                           | Prepends `CHANGELOG.md`                                                                     |
| `/release summary [range]`       | optional git range                           | `tasks/output-release-<date>.md`                                                            |
| `/release migration <from> <to>` | two version tags, e.g. `v1.2 v2.0`           | Terminal only                                                                               |
| `/release prepare <version>`     | version to stamp, e.g. `v1.3.0`              | All artifacts: audit → `PUBLIC-NOTES.md` + `CHANGELOG.md` + summary + migration if breaking |
| `/release audit [version]`       | optional target version                      | Terminal readiness report                                                                   |

If no mode is given, defaults to `notes`. `prepare` is the full release pipeline — it runs audit first, then generates all artifacts for the version; use it when you are ready to cut a release rather than drafting individual documents.

</inputs>

<workflow>

**Task tracking**: per CLAUDE.md, create tasks (TaskCreate) for each major phase. Mark in_progress/completed throughout. On loop retry or scope change, create a new task.

## Mode Detection

Parse `$ARGUMENTS` by the first token:

```bash
FIRST=$(echo "$ARGUMENTS" | awk '{print $1}')
REST=$(echo "$ARGUMENTS" | cut -d' ' -f2-)
```

| First token                     | Mode      | Routing                                                                                                                                              |
| ------------------------------- | --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `prepare`                       | prepare   | Skip to **Mode: prepare**                                                                                                                            |
| `audit`                         | audit     | Skip to **Mode: audit**                                                                                                                              |
| `migration`                     | migration | Set `FROM=$(echo $REST \| awk '{print $1}')`, `TO=$(echo $REST \| awk '{print $2}')`, `RANGE="$FROM..$TO"`, continue Steps 1–5 with migration format |
| `notes`, `changelog`, `summary` | as named  | Set `RANGE="$REST"` (empty = default); continue Steps 1–5                                                                                            |
| *(none or bare range)*          | notes     | Set `RANGE="$ARGUMENTS"`; continue Steps 1–5                                                                                                         |

## Step 1: Gather changes

```bash
# Use $RANGE from Mode Detection, or fall back to last-tag..HEAD
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || git rev-list --max-parents=0 HEAD)
RANGE="${RANGE:-$LAST_TAG..HEAD}"

# One-liner overview (navigation index)
git log $RANGE --oneline --no-merges

# Full commit messages — read these to catch BREAKING CHANGE footers,
# co-authors, and details omitted from the subject line
git log $RANGE --no-merges --format="--- %H%n%B"

# File-level diff stat — confirms what areas actually changed
git diff --stat $(echo "$RANGE" | sed 's/\.\./\ /')

# PR titles, bodies, and labels for merged PRs (richer context than commits)
TRUNK=$(git remote show origin 2>/dev/null | grep 'HEAD branch' | awk '{print $NF}')
gh pr list --state merged --base "${TRUNK:-main}" --limit 100 \
  --json number,title,body,labels,mergedAt 2>/dev/null
```

Cross-reference commit bodies against Pull Request (PR) descriptions — the canonical source of
truth for *why* a change was made. If a commit footer contains `BREAKING CHANGE:`,
it is a breaking change regardless of how it was labelled in the PR.

## Step 2: Classify each change

Section order (fixed — never reorder): 🚀 Added → ⚠️ Breaking Changes → 🌱 Changed → 🗑️ Deprecated → ❌ Removed → 🔧 Fixed

| Category             | Output section         | What goes here                                                                                                                                                                       |
| -------------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **New Features**     | 🚀 Added               | User-visible additions                                                                                                                                                               |
| **Breaking Changes** | ⚠️ Breaking Changes    | Existing code **stops working immediately** after upgrade — API removed, signature changed incompatibly, behavior changed with no fallback. Must be 100% certain it no longer works. |
| **Improvements**     | 🚀 Added or 🌱 Changed | Enhancements to existing behavior                                                                                                                                                    |
| **Performance**      | 🚀 Added or 🔧 Fixed   | Speed or memory improvements                                                                                                                                                         |
| **Deprecations**     | 🗑️ Deprecated          | Old API **still works** this release but is scheduled for removal — emits a warning, replacement exists                                                                              |
| **Removals**         | ❌ Removed             | Previously deprecated API now gone (this is what becomes a Breaking Change in the next cycle)                                                                                        |
| **Bug Fixes**        | 🔧 Fixed               | Correctness fixes                                                                                                                                                                    |
| **Internal**         | *(omit)*               | Refactors, Continuous Integration (CI), deps — omit unless user-impacting                                                                                                            |

**Breaking vs Deprecated**: if the old call still works (even with a warning), it is **Deprecated** — never Breaking Changes. Breaking Changes are strictly for changes where upgrading causes immediate failures with no compatibility period.

Filter out: merge commits, minor dep bumps, CI config, comment typos.
Always include: any breaking change, any behavior change, any new API surface.

## Step 3: Choose output format

Before writing, fetch the last 2–3 releases from the repo to check for project-specific formatting conventions:

```bash
gh release list --limit 3
gh release view <latest-tag>   # replace <latest-tag> with an actual tag from the list above; read the body to match style, tone, and structure
```

If the existing releases deviate significantly from the templates below (e.g., no emoji sections, different heading levels, prose-style entries), match their style. The templates below are the default — project conventions take precedence.

### Notes — user-facing, public (`notes`)

Omit any section that has no content.

Read the PUBLIC-NOTES template from .claude/skills/release/templates/PUBLIC-NOTES.tmpl.md and use it as the format for the notes output.

### CHANGELOG Entry (`changelog`)

Read the CHANGELOG entry template from .claude/skills/release/templates/CHANGELOG.tmpl.md and use it as the format.

### Internal Release Summary (`summary`)

Read the internal release summary template from .claude/skills/release/templates/SUMMARY.tmpl.md and use it as the format.

### Migration Guide (`migration`)

Read the migration guide template from .claude/skills/release/templates/MIGRATION.tmpl.md and use it as the format.

## Step 4: Writing guidelines

Read the writing guidelines from .claude/skills/release/guidelines/writing-rules.md and follow them.

After applying the guidelines above to polish the output, write to disk per mode:

- **`notes`**: write to `PUBLIC-NOTES.md` at the repo root. Notify: `→ written to PUBLIC-NOTES.md`
- **`changelog`**: prepend the entry to `CHANGELOG.md` after the `# Changelog` heading (create the file with that heading if it does not exist). Notify: `→ prepended to CHANGELOG.md`
- **`summary`**: save to `tasks/output-release-$(date +%Y-%m-%d).md`. Notify: `→ saved to tasks/output-release-$(date +%Y-%m-%d).md`
- **`migration`**: print to terminal only

## Step 5: Publish (after writing notes)

**Human gate** — stop here and hand off to the user: the GitHub release must be created with project-level tooling (e.g. `gh release create`). Refer to the project's CLAUDE.md or `oss-maintainer` agent for the exact command. Resume after the release is live.

## Mode: prepare

**Trigger**: `/release prepare <version>` (e.g., `prepare v1.3.0` or `prepare 1.3.0`)

**Purpose**: Full release preparation pipeline — audit readiness first, then generate and write all artifacts. Use this when cutting a release; use individual modes (`notes`, `changelog`, `summary`) for drafting.

```bash
VERSION=$(echo "$ARGUMENTS" | awk '{print $2}')
[[ "$VERSION" != v* ]] && VERSION="v$VERSION"
DATE=$(date +%Y-%m-%d)
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || git rev-list --max-parents=0 HEAD)
RANGE="$LAST_TAG..HEAD"
```

### Phase 1: Readiness audit

Run all checks from **Mode: audit** with `$VERSION` as the target. Present the readiness table.

**If verdict is BLOCKED**: stop here. List the blockers and instruct the user to resolve them before re-running `/release prepare $VERSION`. Do not write any artifacts.

**If verdict is READY or NEEDS ATTENTION**: surface any warnings, then continue to Phase 2.

### Phase 2: Gather and classify changes

Run **Steps 1–2** to gather and classify all commits in `$RANGE`.

Note whether any **Breaking Changes** were classified — this gates Phase 3d.

### Phase 3: Write all artifacts

```bash
RELEASE_DIR="releases/$VERSION"
mkdir -p "$RELEASE_DIR"
```

Write each artifact in sequence:

**a. `releases/$VERSION/PUBLIC-NOTES.md`** — user-facing notes (Step 3 `notes` format).

**b. `CHANGELOG.md`** — prepend entry stamped `$VERSION — $DATE` (Step 3 `changelog` format) to the root `CHANGELOG.md`. This file is cumulative — it is not versioned per release. Create it with a `# Changelog` header if it does not exist.

**c. `releases/$VERSION/SUMMARY.md`** — internal summary (Step 3 `summary` format).

**d. `releases/$VERSION/MIGRATION.md`** — always written. If breaking changes were classified in Phase 2, use the Step 3 `migration` format. If no breaking changes, write a single line: `No breaking changes in this release.`

### Output

```
## Release prepare: $VERSION

### Audit
[readiness table from Phase 1, condensed]
[any warnings carried forward]

### Written
- `releases/$VERSION/PUBLIC-NOTES.md` — user-facing notes (N features, N fixes, N breaking changes)
- `CHANGELOG.md` — $VERSION entry prepended (root, cumulative)
- `releases/$VERSION/SUMMARY.md` — internal summary
- `releases/$VERSION/MIGRATION.md` — migration guide (N breaking changes, or "No breaking changes")

### Next steps
1. Review all written files
2. Bump version in the project manifest
3. Commit, push, open PR
4. On merge: create GitHub release from PUBLIC-NOTES.md
```

End your response with a `## Confidence` block per CLAUDE.md output standards.

## Mode: audit

**Trigger**: `/release audit [version]`

**Purpose**: Pre-release readiness check — surfaces outstanding work, alignment gaps, and blocking issues before cutting a release.

Read and execute all checks from `.claude/skills/release/templates/audit-checks.md`. Checks cover: version consistency across manifests, docs/CHANGELOG alignment, open blocking issues, dependency CVE scan, and unreleased commits since last tag.

End your response with a `## Confidence` block per CLAUDE.md output standards.

</workflow>

<notes>

- Filter noise (CI config, dep bumps, typos) unless they are user-impacting
- Public-facing output (release notes, changelogs, migration guides) is co-authored with `oss-maintainer` — follow its `<voice>` guidelines for human, direct tone
- Follow-up chains:
  - Before cutting a release → `/release audit [version]` to check readiness: blockers, docs alignment, version consistency, CVEs
  - Readiness confirmed → `/release prepare <version>` to run the full pipeline and write all artifacts
  - Release includes breaking changes → `/analyse` for downstream ecosystem impact assessment
  - `migration` content written → add to project docs and link from the CHANGELOG entry

</notes>
