# CI integration — `--ci` flag and sample workflows

Phase 3 adds non-interactive `--ci` mode to `/phx:deps-audit` for use
in GitHub Actions, CircleCI, GitLab CI, and similar runners. Pairs
with `--sarif <path>` (Phase 2) to feed results into the host
platform's code-scanning UI.

## `--ci` semantics

`--ci` makes three behavioral changes to the default audit:

1. **No interactive prompts.** `AskUserQuestion` would block forever
   in CI. `--ci` short-circuits all prompts to their conservative
   default (skip vetting, never auto-approve).
2. **Strict exit codes.** Three exit codes drive the gating decision:

   | Exit | Meaning |
   |------|---------|
   | 0 | Audit clean — no BLOCK findings |
   | 1 | One or more BLOCK findings — fail CI |
   | 2 | Required tool missing (e.g., `mix_audit` not installed and CI strictness demands it) — fail CI as misconfiguration, not a security finding |

3. **Machine-only output.** Stdout becomes JSON unless `--sarif <path>`
   is also supplied (in which case SARIF lands in the file and stdout
   stays JSON for log readability).

`--ci` implies `--no-llm` by default (LLM triage adds wall-time and
non-determinism unsuitable for CI). Override with `--ci --llm` when
running an explicit pre-merge audit job that has the budget.

## GitHub Actions

```yaml
name: Hex deps audit
on:
  pull_request:
    paths: ['mix.lock', 'mix.exs', 'hex_vet.exs']
  push:
    branches: [main]

jobs:
  deps-audit:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      security-events: write   # required for upload-sarif
    steps:
      - uses: actions/checkout@v6
        with:
          fetch-depth: 0       # full history so --base can diff against main
      - uses: erlef/setup-beam@v1
        with:
          otp-version: '27.x'
          elixir-version: '1.18.x'
      - name: Audit Hex deps
        run: |
          mix phx.deps_audit --ci \
            --base origin/main \
            --sarif audit.sarif
      - name: Upload SARIF to Code Scanning
        if: always()           # upload even on audit failure so reviewers see findings
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: audit.sarif
          category: phx-deps-audit
```

The `if: always()` on upload-sarif is critical: when the audit exits 1
on BLOCK findings, the job has `failed` status, and a strict
`if: success()` would skip the upload — leaving reviewers with no
in-UI feedback on what failed.

## CircleCI

```yaml
version: 2.1
jobs:
  deps-audit:
    docker:
      - image: hexpm/elixir:1.18.0-erlang-27.0.0-alpine-3.18.0
    steps:
      - checkout
      - run:
          name: Audit Hex deps
          command: |
            mix local.hex --force
            mix deps.get --only-prod
            mix phx.deps_audit --ci --base main --sarif /tmp/audit.sarif
      - store_artifacts:
          path: /tmp/audit.sarif
          destination: phx-deps-audit-sarif
workflows:
  pr:
    jobs: [deps-audit]
```

CircleCI lacks a native SARIF surface but `store_artifacts` keeps the
output downloadable. Pair with a separate job that posts a PR comment
referencing the artifact URL.

## GitLab CI

```yaml
deps-audit:
  stage: test
  image: hexpm/elixir:1.18.0-erlang-27.0.0-alpine-3.18.0
  before_script:
    - mix local.hex --force
    - mix deps.get --only-prod
  script:
    - mix phx.deps_audit --ci --base "${CI_DEFAULT_BRANCH}" --sarif audit.sarif
  artifacts:
    when: always
    paths: [audit.sarif]
    reports:
      sast: audit.sarif       # GitLab Ultimate SAST integration
```

GitLab Ultimate accepts SARIF as a SAST report. For lower tiers, fall
back to `artifacts.paths` and manual download.

## Drone CI

```yaml
kind: pipeline
type: docker
name: deps-audit

steps:
  - name: audit
    image: hexpm/elixir:1.18.0-erlang-27.0.0-alpine-3.18.0
    commands:
      - mix local.hex --force
      - mix deps.get --only-prod
      - mix phx.deps_audit --ci --base main --sarif audit.sarif
    when:
      paths:
        include: [mix.lock, mix.exs, hex_vet.exs]
```

Drone has no built-in SARIF UI; pair with a Slack notification step
that links to the run.

## Mix-task pattern (Phase 3+ companion)

The `--ci` flag works with `/phx:deps-audit` inside Claude Code AND
with the planned `mix phx.deps_audit` Mix task shipped by the
companion `phx_deps_vet` Hex package. Both surfaces share the same
exit-code rubric so CI workflows are portable between teams using
CC and teams using the Mix task directly.

Until the companion package ships, CI users run the audit via the
Claude Code CLI:

```bash
claude code -m "/phx:deps-audit --ci --base origin/main --sarif audit.sarif"
```

This requires the runner has Claude Code installed and authenticated.
For teams without that infrastructure, defer CI gating until the
companion Mix task ships.

## `mix format` post-Write pattern for `.exs` data files

Several workflows in this plugin scriptedly Write `.exs` files
(`hex_vet.exs` ledger updates, `hex_vet_seed.exs` regen). The
PostToolUse format hook in Claude Code rejects unformatted output —
when CI scripts use `Code.format_string!` + `File.write!` to round-
trip the file, the result still drifts from `mix format` if the
`.formatter.exs` has unusual locals_without_parens or similar.

Always run `mix format <path>` immediately after writing an `.exs`
data file, before committing:

```bash
mix run --no-mix-exs -e "..." # write the file via Code.format_string!
mix format hex_vet.exs        # belt-and-braces project-formatter alignment
git add hex_vet.exs
```

This pattern recurs across `seed-regen.yml`, `cassette-regen.yml`,
and any future regen workflow. Document it in those workflows'
README sections.

## Flag matrix

| Flag | CI use | Default |
|------|--------|---------|
| `--ci` | enable non-interactive mode | off |
| `--sarif <path>` | emit SARIF 2.1.0 | off |
| `--base <ref>` | diff against ref (Mode C) | `origin/main` in CI |
| `--no-llm` | skip LLM triage | implied by `--ci` |
| `--llm` | force LLM triage (override `--ci` default) | off |
| `--no-differential` | disable Phase 2 NDJSON subtract | off |
| `--json` | machine-readable stdout | implied by `--ci` |
| `--strict` | promote all WARN to BLOCK | off |

`--strict` is useful for "high-stakes deploy" pipelines: it makes any
WARN finding exit-code-1. Most CI jobs leave it off and rely on
`hex_vet.exs` `policy.block_on_unvetted: :strict` for gating instead.
