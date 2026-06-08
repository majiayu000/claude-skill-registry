---
name: rust-crate-release-readiness
description: |-
  Use when preparing a Rust crate release with metadata, semver, docs, tests, packaging, and rollback notes.
  Triggers:
skill_api_version: 1
user-invocable: false
hexagonal_role: supporting
practices:
- evidence-over-confidence
- release-readiness
- docs-as-code
consumes:
- Cargo.toml
- Cargo.lock
- crate-source
- crate-docs
- release-notes
produces:
- crate-release-readiness-report
- package-dry-run-evidence
- rollback-note
context_rel: []
context:
  window: inherit
  intent:
    mode: task
  sections:
    exclude:
    - HISTORY
  intel_scope: topic
metadata:
  tier: judgment
  stability: stable
  external_dependencies:
  - cargo
  - rustup
  - git
  clean_room: true
  owner: agentops
output_contract: 'crate_release_readiness_report with sections: candidate, metadata, semver, documentation, tests, package, dry_run, decision, rollback.'
---

# Rust Crate Release Readiness

Use this skill when a Rust crate is close to release and the work is no longer
"make the code pass tests"; it is "prove the crate is safe to publish." The
output is a readiness report with evidence, blockers, and rollback notes. It
does not upload the crate unless the user separately asks for publication.

## Critical Constraints

- **Never publish from an unverified tree.** Check the working tree, candidate
  commit, crate version, and package dry-run before any upload. A released crate
  version cannot be overwritten in normal registry workflows.
- **Semver is decided from the public contract, not the diff size.** A small
  signature change can be major; a large internal cleanup can be patch.
- **Package contents matter as much as tests.** A green test suite does not prove
  the tarball includes the README, license, generated code, fixtures, or build
  script inputs needed by downstream users.
- **Rollback is planned before release.** For a bad release, the usual recovery
  is a yank plus a fixed version, not an edit to the already-published version.

## Read Before Deciding

Inspect the crate and its release surface before running gates:

- `Cargo.toml`, workspace membership, package name, version, authors, license or
  license-file, description, repository, homepage, documentation, keywords,
  categories, readme, include/exclude, features, and publish registry settings.
- Public API surface in `src/lib.rs`, exported modules, feature-gated APIs,
  examples, benches, build scripts, macros, unsafe code, and generated bindings.
- Existing docs: README, changelog, migration notes, rustdoc comments, examples,
  release notes, and any registry-facing screenshots or generated docs.
- CI and local gates: fmt, clippy, test matrix, feature matrix, doc tests,
  minimal supported Rust version if declared, and platform-specific checks.
- Prior release history: latest tag, prior crate version, changelog entries,
  yanked versions, known compatibility constraints, and downstream breakage.

If a fact cannot be confirmed from files or command output, mark it as unknown
instead of guessing.

## Procedure

1. **Snapshot the candidate.**
   - Record `git status --short`, `git rev-parse HEAD`, and the crate path.
   - Record `cargo metadata --format-version 1 --no-deps` for package identity.
   - If the tree is dirty, stop unless the user explicitly wants a draft report.

2. **Check metadata.**
   - Confirm `Cargo.toml` has release-grade package fields: `name`, `version`,
     `edition`, `description`, `license` or `license-file`, `repository` when
     public, `readme` when one exists, and intentional `publish` settings.
   - Validate feature names and defaults. Optional dependencies should be
     explainable from the feature list.
   - Confirm README and license paths referenced by metadata exist.

3. **Choose the semver bump.**
   - Compare the candidate against the previous release tag or version.
   - Classify public-contract changes: removed items, signature changes, trait
     bound changes, feature default changes, MSRV increases, new APIs, bug fixes,
     behavior changes, and deprecations.
   - Pick major, minor, or patch from the highest-impact confirmed change.
   - Record the specific change that justifies the selected version.

4. **Verify docs and examples.**
   - Run `cargo doc --no-deps` for the relevant package and feature set.
   - Run doc tests with `cargo test --doc` unless the crate has a documented
     reason they are unsupported.
   - Check README examples against the current package name, feature flags, and
     public API. Mark stale snippets as blockers.

5. **Run release gates.**
   - Baseline: `cargo fmt --all -- --check`.
   - Build: `cargo build --all-targets`.
   - Lints: `cargo clippy --all-targets -- -D warnings`.
   - Tests: `cargo test`.
   - Features: run `cargo test --all-features`; for feature-heavy crates, also
     test `--no-default-features` and important named feature sets.
   - Workspace crates: scope commands with `-p <crate>` when releasing one crate,
     but record whether workspace-wide failures affect the release.

6. **Inspect the package.**
   - Run `cargo package --list` and verify expected files are present and
     generated clutter, secrets, local fixtures, or huge artifacts are absent.
   - Run `cargo package` to build the distributable tarball locally.
   - Inspect warnings from packaging. Treat missing metadata, ignored files,
     duplicate license signals, or missing include paths as blockers unless
     intentionally documented.

7. **Run publish dry-runs.**
   - Run `cargo publish --dry-run` with the intended package, registry, target,
     and feature constraints.
   - Do not pass flags merely to make the dry-run quiet. If a warning matters to
     downstream users, fix the crate or record the risk.
   - If the target registry requires authentication, separate credential failure
     from crate-readiness failure.

8. **Write rollback notes.**
   - Record how to identify a bad release, who can yank it, and the exact command
     shape for yanking the affected version.
   - Record the follow-up path: fixed patch/minor version, changelog correction,
     downstream notification, and how to verify the repaired package.
   - Call out irreversible limits: the published version number and artifact
     contents cannot normally be replaced.

9. **Make the decision.**
   - GO only when metadata, semver, docs, tests, package inspection, and dry-run
     evidence are clean or risks are explicitly accepted.
   - NO-GO when any blocker remains. Each blocker must name the failing command
     or inspected file and the smallest next action.

## Report Shape

Write the result inline or as `CRATE-RELEASE-READINESS.md`:

```markdown
# Crate Release Readiness

## Candidate
- Crate:
- Version:
- Commit:
- Registry:
- Previous release:

## Metadata
- Result:
- Evidence:
- Blockers:

## Semver
- Decision:
- Justification:
- Public-contract changes:

## Documentation
- Result:
- Commands:
- Stale or missing docs:

## Tests
- Result:
- Commands and exit codes:
- Feature matrix:

## Package
- Result:
- `cargo package --list` findings:
- Warnings:

## Dry Run
- Result:
- Command:
- Warnings:

## Decision
- GO / NO-GO:
- Accepted risks:
- Next action:

## Rollback
- Yank authority:
- Yank command shape:
- Fixed-version plan:
```

## Quality Rubric

A crate passes only if all hold:

- The chosen version matches the highest-impact public-contract change.
- Registry-facing metadata is complete, accurate, and points to existing files.
- Rustdoc, README examples, tests, and feature checks reflect the package being
  released, not a neighboring workspace crate.
- `cargo package --list`, `cargo package`, and `cargo publish --dry-run` were run
  with the intended package and registry settings.
- The report includes rollback notes for yanking and issuing a fixed version.

## Common Failure Patterns

| Symptom | Likely Cause | Corrective Move |
| --- | --- | --- |
| Dry-run warns about missing README | Metadata points to a stale path | Fix `readme` or add the file, then rerun package and dry-run |
| Package excludes generated bindings | `include` is too narrow | Add the generated path or regenerate in `build.rs` |
| Tests pass but docs fail | Public examples drifted | Fix examples, then rerun `cargo test --doc` |
| Patch bump hides a breaking feature change | Semver review skipped feature defaults | Reclassify version and update changelog |
| Bad release already uploaded | No recovery plan | Yank the affected version if appropriate, then ship a fixed version |
