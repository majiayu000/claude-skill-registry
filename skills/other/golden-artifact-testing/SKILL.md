---
name: golden-artifact-testing
description: |-
  Use when designing or repairing golden-file, snapshot, fixture, or generated-artifact tests.
  Triggers:
practices:
- pragmatic-programmer
skill_api_version: 1
user-invocable: false
hexagonal_role: supporting
context:
  window: fork
  intent:
    mode: task
metadata:
  tier: judgment
  stability: experimental
  dependencies: []
  category: testing
  maturity: source
  clean_room: true
  owner: agentops
output_contract: 'golden_artifact_test_plan with sections: scope, artifact_contract, normalization, comparator_and_diff, fixture_ownership, approval_workflow, update_discipline, verification.'
---

# Testing Golden Artifacts

Use this skill when a test should lock down a produced artifact: generated code,
serialized JSON, command output, reports, migration files, rendered documents, or
other outputs where a reviewer needs to see the exact shape. A good golden test
answers one question: did the intended contract change, or did the implementation
drift?

## Operating Rule

A golden artifact is a reviewed contract, not a cache. The test may help produce
an updated candidate, but replacing the expected artifact must be an explicit
approval step with a readable diff and a named reason.

## Fit Check

Use golden artifacts when at least one of these is true:

- The artifact is the public or integration-facing behavior.
- The output has enough structure that individual assertions would miss
  ordering, formatting, omission, or compatibility regressions.
- Reviewers can make sense of a diff faster than they can reconstruct the
  expected output from many small assertions.
- The artifact is part of an approval workflow, such as generated docs, schemas,
  prompts, reports, migrations, or CLI transcripts.

Prefer ordinary assertions when the expected value is small, when the behavior is
purely numeric or boolean, or when the fixture would mostly encode incidental
implementation details.

## Design Workflow

1. Define the artifact contract.
   Name the user-visible behavior the artifact represents. Do not snapshot an
   entire directory or object graph just because it is easy to serialize.

2. Isolate generation from comparison.
   Generate the actual artifact into a temporary location, normalize it, then
   compare it with the committed expected artifact. Keep production code unaware
   of test update mode.

3. Normalize volatility before comparison.
   Remove or canonicalize timestamps, absolute paths, random IDs, hostnames,
   map ordering, locale-specific formatting, line endings, and other values that
   do not belong to the contract.

4. Compare with a stable diff.
   Text artifacts should fail with a unified diff or a structure-aware diff.
   Binary artifacts need a reviewable companion representation such as metadata,
   dimensions, checksums, extracted text, perceptual hash, or a generated preview.

5. Require explicit approval for updates.
   A failing test may write an actual artifact to a temporary path or an
   ignored candidate file. It must not silently overwrite the committed golden.

6. Verify update discipline.
   CI runs in read-only mode. Local update mode must be opt-in, deterministic,
   and followed by a clean rerun plus review of the changed fixture files.

## Normalization Checklist

- Sort maps, object keys, directory entries, and unordered collections.
- Format structured files canonically: stable JSON indentation, stable YAML key
  order when possible, normalized markdown whitespace, and LF line endings.
- Scrub absolute workspace paths to placeholders such as `<workspace>`.
- Replace timestamps, UUIDs, process IDs, ports, and random suffixes only when
  they are not part of the behavior under test.
- Seed randomness when random data matters to the scenario.
- Redact secrets before writing any actual or expected artifact.
- Keep normalizers narrow. A normalizer that deletes large sections of output is
  usually hiding the wrong contract.

## Stable Diff Rules

- Prefer small, named goldens over one large omnibus artifact.
- Keep generated actual files available on failure so the reviewer can inspect
  the full output, not only the diff excerpt.
- Use path-stable artifact names. Avoid test names that depend on package order,
  wall-clock time, or temporary directories.
- For structured data, compare the parsed form after canonical serialization
  when formatting is not part of the contract.
- For formatting-sensitive artifacts, compare the final bytes after line-ending
  normalization and make whitespace changes visible in the diff command.
- For binary outputs, commit a reviewable surrogate when the raw binary diff is
  not useful.

## Fixture Ownership

Every golden fixture needs one clear owner:

- The owning test, scenario, or package is named in the fixture path or filename.
- Shared fixtures are read-only inputs; generated expected artifacts are owned by
  the test that approves them.
- A fixture update should be attributable to one behavior change. If one code
  change updates unrelated goldens, split the work or explain the shared cause.
- Do not let two tests update the same expected file from different paths.
- Delete obsolete fixtures in the same change that removes the behavior they
  represented.

## Approval Workflow

Use a two-step workflow:

1. Read-only check.
   The default test command generates actual output, normalizes it, compares it
   to the committed expected artifact, and fails with a stable diff plus an
   update command hint.

2. Explicit update.
   A local maintainer runs an opt-in command or environment flag such as
   `UPDATE_GOLDENS=1`. The update writes expected artifacts deterministically,
   then the maintainer reviews the git diff and reruns the read-only test.

Approval is not complete until the diff has been reviewed. Never make CI update
goldens, and never make a passing test depend on uncommitted generated files.

## Update Discipline

- Update goldens in the same change as the behavior that requires them.
- Keep the reason visible in the commit, PR, bead, or test note.
- Regenerate the smallest fixture set that proves the change.
- Reject blanket "update all snapshots" churn unless the underlying behavior is
  intentionally global.
- Rerun the read-only test after update mode and confirm the working tree has
  only intended artifact changes.
- If a golden changes often without product behavior changing, fix the
  normalization or replace the golden with targeted assertions.

## Review Checklist

Before accepting a golden-artifact test, verify:

- The artifact contract is named and belongs in a golden test.
- The normalizer removes volatility without erasing meaningful behavior.
- Failures produce a diff a reviewer can act on.
- Update mode is explicit, local-only, deterministic, and documented by the test
  failure or nearby test helper.
- Fixture ownership is clear from paths, test names, or scenario names.
- The changed fixtures are reviewed as product evidence, not accepted as
  generated noise.

## Output Specification

When applying this skill, return a concise plan or review with these sections:

- Scope: artifact type, owning test surface, and behavior under contract.
- Artifact contract: what is intentionally frozen and what is excluded.
- Normalization: volatile fields and how they are canonicalized.
- Comparator and diff: command, helper, or assertion strategy.
- Fixture ownership: where expected artifacts live and who updates them.
- Approval workflow: read-only command, update command, and CI posture.
- Update discipline: review requirements and limits on fixture churn.
- Verification: commands run and residual risks.
