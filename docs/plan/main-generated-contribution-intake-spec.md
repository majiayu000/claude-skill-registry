# Main Generated-Contribution Intake Architecture

## Objective

Keep `majiayu000/claude-skill-registry` as the public contribution front door
without making generated `skills/**` files authoritative. A contributor may
report or prepare a correction in main; maintainers own the cross-repository
port, preserve contributor attribution, merge the archive change in data, and
republish main from immutable core and data commits. Automation must reduce
maintainer work without executing contributor-controlled code or exposing a
cross-repository token before maintainer approval.

## Current Evidence

| Area | Evidence | Implication |
| --- | --- | --- |
| Public entrypoint | `majiayu000/claude-skill-registry` is the merged browsing artifact and receives issue #54 / PR #53 | Main must accept reports and proposed edits as intake even when it cannot merge them directly |
| Core authority | `AGENTS.md`, `scripts/sync_main_repo.sh`, and `.github/workflows/sync-data.yml` assign orchestration and generated-index behavior to core | Routing and validation logic belongs in core; main adapters stay thin |
| Archive authority | `claude-skill-registry-data/AGENTS.md` assigns archived `SKILL.md` and `metadata.json` bodies to data | Accepted content corrections must end as data commits |
| Publish lifecycle | Main `.github/workflows/publish-from-core.yml` accepts pinned `core_sha` and `data_sha`, rebuilds the artifact, writes provenance, validates canaries, and pushes | Existing publish handoff is the promotion mechanism; no second publisher is needed |
| Current guidance | Main's pull-request template says generated outputs must not be patched; core `CONTRIBUTING.md` previously described new-skill intake only | The contributor-facing contract rejects a reasonable correction without offering a maintained handoff |
| Existing validation | Core has security scanning, metadata checks, artifact API checks, category checks, and pipeline contract tests | Assisted intake should compose these checks rather than invent weaker substitutes |
| Incident | Main PR #53 correctly changes four generated copies; main issue #54 explains the source and AWS evidence; data PR #103 ports the correction with attribution | This is the manual reference run that automation must reproduce |

## Reference Models Considered

| Reference | Borrow | Do not copy | Source |
| --- | --- | --- | --- |
| Existing immutable publish handoff | Pinned core/data SHAs, provenance manifest, canary before promotion, replayable inputs | Full archive rebuild/discovery for every intake classification event | `.github/workflows/sync-data.yml`, main `.github/workflows/publish-from-core.yml` |
| Existing community-source intake | Explicit source-of-truth routing and deterministic validation before merge | Append-only `sources/community.json` semantics for edits to already archived bodies | `scripts/check_community_intake_diff.py`, `tests/test_check_community_intake_diff.py` |
| Manual issue #54 handoff | Human fact check, exact path mapping, contributor trailer, linked closeout | Requiring the external contributor to recreate the same patch across three repositories | main PR #53, data PR #103 |

## Chosen Architecture

Project shape: an agent/workflow system around three repositories, with an
immutable publish pipeline as the final projection.

State ownership model: the original main pull request owns the intake event
log; its immutable head SHA, labels, and linked data PR/publish provenance are
the authoritative lifecycle record, while data and main are projections at
different stages.

```text
product/app
  - main PR and issue surfaces
  - maintainer label or workflow-dispatch approval

core/domain
  - pure contribution classifier and path mapper
  - handoff manifest schema and validation policy
  - attribution and conflict decisions

runtime/application
  - classify -> approve -> port -> validate -> merge -> publish -> close
  - existing pinned-ref publish lifecycle

adapters/backends
  - thin main-owned GitHub workflow adapter
  - GitHub API reads and data-repository branch/PR writes
  - core build-index and main publish dispatches

testing/headless
  - fixture PR payloads and file lists
  - fake GitHub responses and generated handoff manifests
  - existing archive/security/publish contract tests
```

## Lifecycle And Handoff Manifest

The lifecycle is explicit and monotonic:

```text
reported
  -> classified
  -> maintainer_approved
  -> ported_to_data
  -> data_merged
  -> published_to_main
  -> closed
```

Any failed transition becomes `needs_maintainer` with a visible reason. It must
not be converted to a warning plus fallback.

The assisted port produces a JSON handoff artifact before any cross-repository
write:

```json
{
  "schema_version": 1,
  "source_repo": "majiayu000/claude-skill-registry",
  "source_pr": 53,
  "base_sha": "<main base sha>",
  "head_sha": "<immutable contributor head sha>",
  "base_data_sha": "<data sha from base provenance>",
  "author": {
    "login": "LeeroyHannigan",
    "name": "Lee",
    "email": "leeroyhannigan@yahoo.ie"
  },
  "files": [
    {
      "source_path": "skills/data/infra-architect/SKILL.md",
      "data_path": "data/infra-architect/SKILL.md",
      "base_blob_sha": "<sha>",
      "head_blob_sha": "<sha>"
    }
  ],
  "approved_by": "<maintainer login>"
}
```

The author email is selected from a PR commit attributed to the PR author. If
GitHub does not expose one, use the author's GitHub noreply identity and record
that fallback in the handoff. Never invent an email address.

## Source Of Truth And Migration Debt

| Contract | Current source of truth | Consumers | Duplicates or forks | Action |
| --- | --- | --- | --- | --- |
| Archive bodies | Data `<category>/<skill>/{SKILL.md,metadata.json}` | Core builders, main `skills/**` mirror | Main mirror; upstream repository copy | Data remains authority; upstream sync is encouraged but not a merge prerequisite |
| Intake lifecycle | Today: comments across main/data PRs | Maintainers and contributors | No machine-readable handoff | P1 adds classification output; P2 adds the immutable handoff artifact |
| Path mapping | Main `skills/**` mirrors data root | Manual maintainer reasoning | None by contract, but stale main bases are possible | Remove exactly one `skills/` prefix and verify against base provenance/data blob |
| Attribution | Manual commit trailers | GitHub commit/PR UI | Contributor may have several commit identities | Preserve matching commit identity or explicit noreply fallback |
| Publish state | Main `provenance/merge-source.json` and publish status | Browsers, maintainers, rollback | Core/data default branches may advance later | Verify the exact pinned tuple, not only branch heads |
| Contributor guidance | Core `CONTRIBUTING.md` plus main-owned PR template | Contributors | Earlier guidance covered new sources but not archive corrections | P0 documents main as a supported intake surface |

Main `skills/**` is an intentional generated bridge. It remains until consumers
stop depending on the merged artifact; this design does not make it writable or
authoritative.

## Boundary Contracts

| Contract | Owner | Allowed dependencies | Forbidden dependencies | Tests |
| --- | --- | --- | --- | --- |
| Intake state | Original main PR | GitHub metadata, immutable SHAs, labels, linked PRs | Hidden local state as the only record | Fixture lifecycle transition table test |
| Classification | Core pure planner | PR metadata and changed-file descriptors | Network, git mutation, environment reads | `tests/test_plan_generated_contribution.py` |
| Path mapping | Core pure planner | POSIX relative paths, base provenance | Absolute paths, `..`, symlinks, case-only collisions | Traversal, collision, and prefix table tests |
| Approval | Main thin adapter | Maintainer label/workflow dispatch, GitHub actor permission | Automatic privileged action on untrusted PR open/synchronize | Event fixture and permission-policy test |
| Cross-repo effects | Approved port workflow | GitHub Contents/Git Data APIs or argument-array git calls | Shell interpolation of contributor paths; contributor workflow execution | Fake-adapter request snapshot; no-checkout assertion |
| Attribution | Core planner | GitHub commit identities and explicit noreply fallback | Guessed personal email; omitted original contributor | Trailer generation table test |
| Validation | Core pipeline | metadata schema, security scanner, diff checks | Silent scan failure; weakening existing gates | Existing scanner tests plus affected-file integration test |
| Publish | Existing main workflow | Pinned core/data SHAs, core sync script | Publishing from floating unverified refs | `tests/test_pipeline_contracts.py`; main canary status |
| Errors | Runtime/application | Typed reason codes surfaced in PR comment and job summary | Warning-and-continue for conflict, unsafe path, missing provenance, or failed scan | Failure matrix with asserted terminal state |
| Observability | Original PR plus workflow summaries | Stable marker comment, data PR link, run URLs, provenance tuple | Chat-only or local-only completion claim | Closeout fixture requires all links and SHAs |

## Initial Safety Envelope

Assisted porting initially supports only modifications to existing files:

- `skills/<category>/<skill>/SKILL.md`
- `skills/<category>/<skill>/metadata.json`

It rejects new files, deletions, renames, binary blobs, symlinks, submodules,
case-only path changes, more than 20 files, or more than 1 MiB total changed
content. Those cases remain valid contributions but require the manual runbook.

The workflow must read PR file/blob content through the GitHub API at the pinned
head SHA. It must never check out or execute contributor-controlled code in a
privileged `pull_request_target` job. Before writing data, it reads
`provenance/merge-source.json` from the PR base commit and requires every
current data target blob to match the corresponding blob at that provenance
`data_sha`; mismatch means `needs_maintainer`, not an automatic rebase.

## Issue And PR Map

| Issue/PR | Contract served | Status | Gap or follow-up |
| --- | --- | --- | --- |
| main issue #54 | Reported event and factual evidence | Open during manual run | Close only after published main is verified |
| main PR #53 | Contributor patch and attribution source | Open during manual run | Close with thanks, data PR, publish run, and upstream suggestion |
| data PR #103 | Archive source-of-truth correction | Merged | Use as the first manual reference run |
| Future core PR | Planner, tests, and contributor contract | Planned P1 | Must not include a privileged write workflow until P0 is reviewed |
| Future main PR | Thin main-owned event adapter | Planned P1/P2 | Main workflow stays an adapter; policy remains in core |

## Compatibility And Deletion Plan

| Path or shim | Why it exists | Owner | Keep until | Delete or converge when |
| --- | --- | --- | --- | --- |
| Main `skills/**` mirror | Browsing and compatibility consumers require merged layout | Publish workflow | Consumers migrate or merged artifact remains a product requirement | Product decision removes merged distribution; never delete as intake cleanup |
| Manual maintainer port | Safest validated contribution path | Maintainers | Assisted workflow completes at least five successful reviewed ports with zero unauthorized writes | P2 becomes default; retain documented emergency fallback |
| Main routing comment/template | Explains generated boundary at public entrypoint | Main thin adapter | Assisted port UX makes the same contract visible before submission | Converge wording into app/bot UI; do not remove the contract |
| Upstream-sync suggestion | Prevents later refresh from restoring stale content | Maintainers/upstream owners | Downloader gains durable local override semantics or upstream accepts the fix | Keep as advice, never as a blocker for registry credit |

## P0/P1/P2 Roadmap

| Priority | Work | Files/modules | Done when | Verification |
| --- | --- | --- | --- | --- |
| P0 | Validate one manual port, preserve attribution, document main as supported intake, republish pinned refs | data PR #103; `CONTRIBUTING.md`; this spec; main PR template | Main contains the corrected four files; provenance names the merged data SHA; #53/#54 receive linked closeout | `git diff --check`; `gh pr view`; inspect merge trailer; inspect four main blobs; inspect `provenance/merge-source.json`; successful publish run |
| P1 | Add a read-only classifier that comments with exact routing and produces a validated handoff preview | core `scripts/plan_generated_contribution.py`; `tests/test_plan_generated_contribution.py`; main `.github/workflows/route-generated-contribution.yml` | External PRs touching generated archive files get one stable marker comment and no secrets/cross-repo writes | `pytest tests/test_plan_generated_contribution.py`; workflow fixture test; fork PR dry run |
| P2 | Add maintainer-approved assisted port to data and linked closeout; keep publish dispatch manual until the workflow has five reviewed successes | core port planner/adapter; main thin label-triggered workflow; data PR body contract | Maintainer label creates exactly one data PR from pinned blobs with attribution; conflicts and unsafe inputs stop visibly | planner/adapter tests; token-scope audit; fork PR integration; five-run precision log; existing pipeline and publish canary checks |
| P2 | Automate publish dispatch only after manual validation maturity gate | core/main dispatch adapter and contract tests | Merged data contribution dispatches one pinned publish and closes original only after canary success | replay test; provenance assertion; failed-publish retry test; `pytest tests/test_pipeline_contracts.py` |

## Maintainer Manual Runbook (P0)

1. Verify the main PR's factual claim and exact generated paths.
2. Resolve the PR base commit's `provenance/merge-source.json` and confirm the
   data targets have not diverged unexpectedly.
3. Create a clean data worktree from fresh `origin/main`.
4. Port only the intended archive edits and run the applicable diff, metadata,
   and security checks.
5. Commit with a `Co-authored-by` trailer for the original contributor; open
   and merge a linked data PR.
6. Dispatch main `publish-from-core.yml` with explicit current core SHA and the
   merged data SHA; dispatch core `build-index.yml` for Pages.
7. Verify the workflow result, main provenance tuple, and published file
   contents from GitHub rather than local memory.
8. Thank the contributor, link the data PR and publish evidence, invite an
   upstream correction without making it mandatory, then close the original
   PR and issue.

## Non-Goals

- Main generated files do not become a second source of truth.
- External PRs do not receive credentials or execute code in privileged jobs.
- P0 does not automatically merge, publish, or modify an upstream repository.
- The intake flow does not solve archive deduplication or introduce historical
  path compatibility aliases.
- An upstream PR is encouraged but is not required to credit or accept a valid
  registry correction.

## Open Questions

- Should P2 use a GitHub App installation token instead of a fine-grained PAT
  for the data repository? Default recommendation: GitHub App with repository-
  scoped `contents:write` and `pull_requests:write` permissions.
- Should assisted intake support corrections to bundled assets after the
  initial five-run gate? Default recommendation: keep assets manual until file
  type, size, and malware policies are specified separately.
- Who may apply the approval label? Default recommendation: repository users
  with maintain permission, checked through the GitHub permission API.

## Readiness

This specification is complete enough to execute P0 and sequence P1. P2 is not
declared automation-ready until the manual workflow has been validated and the
planner, permission, conflict, attribution, and fork-PR tests exist.
