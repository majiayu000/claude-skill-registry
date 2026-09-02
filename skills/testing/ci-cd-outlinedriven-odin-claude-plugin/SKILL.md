---
name: ci-cd
description: 'Use when setting up or modifying CI/CD pipelines, quality gates, test runners, or deployment pipeline configuration through workflow files. Authors in-repository pipeline and deployment configuration with blocking gates, secret references, and rollback. Also handles configuring a deployment pipeline through CI or workflow files without triggering a deployment.'
---

# CI/CD and deployment configuration

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Setting up or modifying CI/CD pipelines, quality gates, test runners, deployment strategy, or configuring a deployment pipeline through workflow files. |
| Authority | Reversible local writes: may write CI workflow and deployment configuration files in the local repository. Does not execute deployments, publish, configure branch protection, place secrets in a remote manager, or make any remote mutation. |
| Side effect | Writes CI workflow and deployment configuration files locally; no deployment, publishing, credential, or remote mutation. |
| Done | Blocking gates in a fixed order, secret references via provider environment variables, a deployment stage with a rollback mechanism, and local schema validation are present. |

## Inputs

- The target repository and its CI provider (e.g., GitHub Actions). Required; detected from existing configuration or supplied by the user.
- The quality gates the project requires. Required; defaults to the fixed gate order below.
- The project ecosystem commands that realize each gate (lint, type-check, test, build, integration, security audit, bundle size). Required.
- The deployment target and its rollback strategy. Required when a deployment stage is in scope.
- Any required deployment secrets, environment names, or build commands. Supplied by the user; this skill does not invent credentials.
- An existing pipeline to modify. Optional; supply when modifying rather than creating.

## Procedure

1. Bound scope: confirm the work is authoring or modifying CI workflow and deployment configuration files in the repository. Do not run deployments, publish artifacts, configure branch protection, place secrets in a remote manager, or mutate remote systems. Enumerate the exact files this skill will create or edit and show the set to the user before mutation. Write only those files. Done when: scope is bounded to local config file authoring and the file set is enumerated.
2. Identify the CI provider and target ecosystem. Detect from existing configuration; if none exists, ask the user for the target platform and pipeline shape before creating any file. Done when: the provider and ecosystem are identified from existing config or supplied by the user.
3. Establish the fixed gate order that every PR and push to main must pass, in this sequence: lint, type check, unit tests, build, integration tests, E2E (optional), security audit, bundle size. The order is fixed across ecosystems; only the commands change (Node: `pnpm exec biome check .`, `pnpm exec tsc --noEmit`, `pnpm exec vitest run`, `pnpm run build`; Python: `uv run ruff check .`, `uv run ruff format --check .`, `uv run pyright`, `uv run pytest`, `uvx pip-audit`; Rust: `cargo clippy`, `cargo test`, `cargo build`, `cargo audit`). Do not add stages the user did not request. Done when: the fixed gate order is established with ecosystem-specific commands.
4. Make every gate blocking. No gate may be skipped. If lint fails, fix lint; if a test fails, fix the code. Do not disable the rule or skip the test. Done when: every gate is configured as blocking with no skip path.
5. Reference secrets via environment variables expected from the provider. Never store secrets in code or in workflow configuration files. The user places secrets in the provider's secret store out of band; this skill only writes the variable references. Done when: secrets are referenced as masked env vars in the workflow file, not stored in any committed file.
6. Author the deployment stage with a rollback mechanism. Configure the deployment pipeline stages (build, test, deploy) using the user-supplied platform, environment, and commands. Include a defined rollback step. Do not add stages the user did not request. Done when: the deployment stage has a rollback mechanism and only user-requested stages.
7. Validate the authored files locally. Run the project's local check set (lint, build, test) against the pipeline definition. If the platform provides a local validation command for the workflow file (e.g., `actionlint` for GitHub Actions), run it. Do not trigger a deployment. Done when: every local check and platform validation command is run with pass or fail recorded.
8. When a CI run has already failed, route the failure back to the agent that owns the change: copy the failing job name, the error text, and the repo state at failure, so the root cause is fixed rather than re-run. Skip this step when setting up a new pipeline that has no failure yet. Done when: the failure is routed to the owning agent with job name, error text, and repo state, or the step is skipped for a new pipeline.
9. Verify all gates are present, the pipeline runs on every PR and push to main, secrets are referenced via env vars, deployment has a rollback mechanism, and local schema validation passes. Done when: every done-predicate element is verified present.

## Failure and recovery

- Unsupported CI provider: stop and report; do not guess a provider-specific schema.
- Missing required ecosystem commands: stop and ask the user; do not invent commands.
- Gate failure: fix the code or configuration that caused the failure. Never disable the gate, skip the test, or re-run a flaky test; fix the flakiness.
- Secret leak in a config or code file: remove the secret from the file, rotate it, and re-reference it as an env var before proceeding.
- Missing rollback: do not mark deployment configuration done; add the rollback mechanism first.
- Validation fails: report the failing check with its file and line; do not mark the pipeline verified. Leave the edited files in place for the user to correct, or revert them to their prior state on user request.
- Partial result: keep all completed gate configuration, but do not commit a pipeline that is missing a blocking gate, a secret boundary, or a rollback. The blocked result is a report listing exactly which done-predicate element is missing and what was tried.
- Rollback: the edited CI or workflow files are version-controlled; restore them from VCS to the pre-edit state.

## Output

CI workflow and deployment configuration files in the repository implementing the fixed gate order, blocking gates, secret references via environment variables, a deployment rollback mechanism, and local schema validation, plus a report listing files written and per-check pass or fail status. No deployment triggered.
