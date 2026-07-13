---
name: ln-63-release-publisher
description: "Prepares and publishes a tagged GitHub release from repository evidence. Use for an explicit release request; not for ordinary commits, packages, or community news."
---

# Release Publisher

Prepare a reproducible release and publish it only after the user approves the exact tag and notes.

## Tool Routing

| Need | Preferred capability | Fallback |
|---|---|---|
| Release boundary and commit evidence | Git history, tags, and diffs | Hosting API commit comparison |
| Existing release style and state | Authenticated GitHub CLI or connector | Public GitHub API for read-only evidence |
| Version and manifest scope | Canonical repository files | Stop when no authoritative version source exists |
| Release validation | Repository-native gates and clean checkout | Manual structural checks with reduced confidence |
| Tag and GitHub Release creation | Git plus authenticated GitHub CLI | `BLOCKED`; do not emulate release state in files |
| Installation verification | Isolated host configuration against Git source | Clean clone validation without install proof |

Use a temporary notes file for publication so Markdown, quotes, and code blocks are not reinterpreted by the shell. Keep credentials in the host credential store and never echo them.

Do not browse for generic release advice when repository policy and previous comparable releases answer the question. Use official host documentation only for current API or CLI behavior.

## Checklist

- [ ] Confirm the user explicitly requested a release and identify the repository, release target, and intended audience.
- [ ] Read repository release rules before selecting a version, tag shape, files, or publication sequence.
- [ ] Verify GitHub CLI availability, authentication, repository access, and permission to create releases.
- [ ] Require a clean worktree or explicitly exclude unrelated changes before release preparation.
- [ ] Fetch tags and the target branch; confirm local HEAD is synchronized with the remote release branch.
- [ ] Find the latest relevant tag and GitHub Release rather than assuming the newest tag belongs to this release line.
- [ ] Inspect commits and full commit bodies from the previous release boundary to the proposed release commit.
- [ ] Read the affected manifests, README, installation instructions, and user-facing migration notes.
- [ ] Treat commits and source diffs as evidence; use existing release notes only as secondary context.

## Version and Scope

- [ ] Use the repository's declared versioning policy; do not impose CalVer, SemVer, or a shared catalog version when none is specified.
- [ ] If the release target or tag is ambiguous, stop and ask instead of inventing a convention.
- [ ] Confirm the proposed tag does not already exist locally or remotely.
- [ ] Change versions only in canonical version fields identified by repository instructions.
- [ ] Update only plugins included in the release; do not bump unrelated manifests for visual consistency.
- [ ] Keep a new plugin at its approved initial version unless this release explicitly advances it.
- [ ] Ensure tag, manifest version, release title, and notes describe the same release unit.
- [ ] Document breaking installation or behavior changes in the repository's required migration surface.
- [ ] Do not create a `CHANGELOG.md` when repository policy says release notes and README are sufficient.

## Release Notes

- [ ] Read the most recent comparable releases and preserve useful house style without copying stale structure.
- [ ] Group changes by user outcome, not by file list or internal implementation chronology.
- [ ] Lead with why the release matters, then state the concrete behavior users receive.
- [ ] Include exact install or update commands only after verifying them against the current README and catalogs.
- [ ] Include migration steps for every confirmed breaking change, with old and new behavior clearly separated.
- [ ] Mention removed behavior plainly; do not disguise removal as simplification.
- [ ] Credit external contributors by verified handle and omit a contributors section for solo work.
- [ ] Link to canonical documentation and repository paths that exist at the release commit.
- [ ] Exclude claims about adoption, performance, compatibility, or counts that cannot be reproduced.
- [ ] Distinguish measured facts from interpretation and future intent.

## Validation and Approval

- [ ] Run every repository release gate and the relevant skill, plugin, marketplace, and product checks.
- [ ] Confirm both host catalogs remain aligned and the stable marketplace identifier is unchanged.
- [ ] Validate from a clean checkout of the exact proposed release commit when installation surfaces changed.
- [ ] Record commands, versions, exit codes, and skipped checks without exposing secrets.
- [ ] Present the exact version changes, tag, title, full notes, validation evidence, and planned commands.
- [ ] Wait for explicit user approval of that exact proposal before committing version changes, tagging, or publishing.
- [ ] Treat edits requested after approval as a new proposal requiring approval again.

## Publication

- [ ] Apply only approved metadata and documentation changes.
- [ ] Re-run release gates after the final edits.
- [ ] Commit and push the release commit using the authorized branch workflow.
- [ ] Confirm required CI succeeds on the release commit before creating the tag.
- [ ] Create an annotated or repository-standard tag pointing at the verified commit and push it without force.
- [ ] Create the GitHub Release from a file containing the approved notes to preserve Markdown and shell safety.
- [ ] Verify the published tag, target commit, title, body, and release URL through the hosting API.
- [ ] Test documented installation or update from the remote release source when applicable.
- [ ] Do not publish npm, PyPI, NuGet, container, or other packages unless separately authorized.
- [ ] Do not create a community announcement as an implicit side effect.

## Failure Handling

- [ ] If failure occurs before the tag is public, stop and preserve evidence; do not improvise a partial release.
- [ ] If a tag is public but release creation fails, report the exact partial state before taking corrective action.
- [ ] Never delete or move a published tag without explicit approval.
- [ ] Never overwrite an existing release or use force to conceal a bad release commit.

## Verdict

- `RELEASED` — tag and GitHub Release point to the verified commit and remote checks pass.
- `READY` — proposal and evidence are complete but publication awaits approval.
- `PARTIAL` — externally visible release state exists but verification or a later step failed.
- `BLOCKED` — release cannot proceed safely.

## Output Contract

Return release scope, version changes, tag and commit, full notes or release URL, validation evidence, publication state, verdict, and residual risks.

For `PARTIAL`, describe every externally visible object and obtain approval before deleting, moving, or replacing any of them.
