---
name: cross-vendor-trust-gate
description: "Run the skill-factory final trust gate: operate trust-gate.sh, read skill.trust.json, and enforce --require-cross."
practices:
- measure-before-land
- evidence-driven-iteration
- cross-vendor-parity-as-a-gate
hexagonal_role: domain
consumes:
- skill
produces:
- trust-artifact
- stdout
context_rel:
- kind: shared-kernel
  with: heal-skill
skill_api_version: 1
context:
  window: fork
  intent:
    mode: task
  intel_scope: topic
metadata:
  tier: execution
  stability: experimental
  external_dependencies:
  - trust-gate.sh
  - jq
output_contract: 'artifacts: skill.trust.json (trust_level + trust_score) + a pass/fail verdict by exit code'
user-invocable: false
---
# cross-vendor-trust-gate — run the trust gate, read the trust, never hand-wave parity

**YOU MUST RUN THE GATE. Do not eyeball a skill and declare it trustworthy.** This
skill teaches you to operate the existing `trust-gate.sh` tool — the skill-factory's
final gate — to produce a queryable trust verdict for one skill before it lands.
It does NOT reimplement the gate; the gate is the authority.

The tool lives at `~/acfs/skill-pipeline/` (the `trust-gate.sh` script under its
`scripts/` directory — invoked by absolute path in every example below). It validates a
skill's **portable source side** (Claude-side: `SKILL.md`, `skill.spec.json`,
`scripts/validate.sh`) AND its **Codex parity side** (`skills-codex/<name>/`), then
writes a per-skill `skill.trust.json` artifact and exits with a verdict.

## The trust model — three levels, one artifact

The gate grades each skill into exactly one level (written to `skill.trust.json` as
`trust_level` + `trust_score`):

| Level | Score | Meaning |
|---|---|---|
| `fresh` | 0.25 | source side did not validate — not trustworthy |
| `single-validated` | 0.65 | source validates, but Codex parity is absent or red |
| `cross-validated` | 0.95 | source validates AND Codex parity validates — fully trusted |

**Cross-validated is the bar that matters.** A skill that only one vendor's runtime
can run is a single point of failure; cross-validation is the moat. `single-validated`
is "works on Claude, no Codex twin yet" — acceptable mid-build, not acceptable to land
when parity is required.

## The interface — flags you actually use

```
trust-gate.sh [--repo DIR] [--skill-dir DIR] [--codex-dir DIR] [--out FILE] [--require-cross] <skill-name>
```

| Flag | Default | What it does |
|---|---|---|
| `<skill-name>` | (required) | the skill to grade; positional, last arg |
| `--repo DIR` | `$HOME/dev/agentops` | repo root; source = `<repo>/skills/<name>`, codex = `<repo>/skills-codex/<name>` |
| `--skill-dir DIR` | `<repo>/skills/<name>` | override the portable source dir (for staged/fixture skills) |
| `--codex-dir DIR` | `<repo>/skills-codex/<name>` | override the Codex parity dir |
| `--out FILE` | `<skill-dir>/skill.trust.json` | where to write the trust artifact |
| `--require-cross` | off | **refuse to pass** unless level is `cross-validated` (exit 1 otherwise) |
| `-h`, `--help` | — | usage and exit 0 |

Requires `jq` on PATH (the gate calls `need jq` and exits 127 if missing).

## What the gate actually validates

**Source side** (must ALL pass for `source_pass=true`):
- `SKILL.md` exists, with `name:` and `description:` frontmatter
- `skill.spec.json` exists and parses as JSON (`jq -e .`)
- `scripts/validate.sh` is executable AND **runs to exit 0** — it actually runs your
  validator, not a grep
- (when grading a real AgentOps skill, not a fixture) the `verify-real-gate.sh`
  heal-strict check passes

**Codex parity side** (must ALL pass for `codex_pass=true`):
- `skills-codex/<name>/SKILL.md` and `prompt.md` exist
- Codex `SKILL.md` frontmatter is slim — ONLY `name` + `description`, no extra keys
- `prompt.md` has both a `## Steps` and a `## Guardrails` section

## Procedure — grade one skill before it lands

**Step 1 — Confirm the tool is reachable and `jq` is installed.** If `jq` is
missing the gate exits 127 — install it first.

```bash
test -f ~/acfs/skill-pipeline/scripts/trust-gate.sh && command -v jq
```

**Step 2 — Run a non-blocking grade first** (no `--require-cross`) to see where the
skill stands. This always writes the artifact even when the skill is not yet
cross-validated. The summary line on stdout is
`trust-gate: <name> <level> score=<n> artifact=<path>`.

```bash
bash ~/acfs/skill-pipeline/scripts/trust-gate.sh --repo ~/dev/agentops <skill-name>
```

**Step 3 — Read the artifact** to see exactly which check failed (do not guess):

```bash
jq '{trust_level, trust_score,
     source: .source_validation.pass, codex: .codex_validation.pass}' \
  ~/dev/agentops/skills/<skill-name>/skill.trust.json
# drill into failing checks:
jq '.source_validation.checks[] | select(.pass==false)' \
  ~/dev/agentops/skills/<skill-name>/skill.trust.json
jq '.codex_validation.checks[] | select(.pass==false)' \
  ~/dev/agentops/skills/<skill-name>/skill.trust.json
```

**Step 4 — Interpret the level:**

- `fresh` → fix the source side first (a `false` source check tells you which file);
  re-run Step 2.
- `single-validated` → source is good; the Codex twin is missing or malformed. Author
  `skills-codex/<name>/{SKILL.md,prompt.md}` (slim frontmatter, Steps + Guardrails),
  re-run Step 2.
- `cross-validated` → proceed to Step 5.

**Step 5 — Enforce the parity gate before landing.** Re-run WITH `--require-cross`; a
0 exit is your machine-checkable permission to land.

```bash
bash ~/acfs/skill-pipeline/scripts/trust-gate.sh --repo ~/dev/agentops --require-cross <skill-name>
echo "exit=$?"   # 0 = cross-validated, land it; 1 = below bar, do not land
```

**Step 6 — Grade a staged / out-of-repo skill** (not yet under `skills/`) with explicit
dirs:

```bash
bash ~/acfs/skill-pipeline/scripts/trust-gate.sh \
  --skill-dir /Users/bo/acfs/staged-skills/<name> \
  --codex-dir /Users/bo/acfs/staged-skills-codex/<name> \
  --out /tmp/<name>.trust.json <name>
```

## Reading the exit code (the verdict)

| Exit | Meaning |
|---|---|
| `0` | source validated (and, if `--require-cross`, cross-validated) — safe |
| `1` | source failed, OR `--require-cross` was set and the skill is below `cross-validated` |
| `2` | usage error (missing skill name or unknown flag) |
| `127` | `jq` not installed |

**Trust the exit code, not the prose.** When landing skills at scale the `--require-cross`
exit 0 is the gate; the `skill.trust.json` artifact is the audit trail a manager queries
later to tell `fresh` / `single-validated` / `cross-validated` skills apart.

## Guardrails

- Do not edit `trust-gate.sh` to make a skill pass — fix the skill, not the gate.
- A green `validate.sh` is necessary but not sufficient: the gate runs it, but `fresh`
  can still come from a missing spec or absent frontmatter. Read the failing check.
- `single-validated` is not a landing state when parity is required. Build the Codex
  twin, do not lower the bar.
- The gate writes `skill.trust.json` into the skill dir by default — that artifact is
  meant to be committed/queryable; use `--out` to redirect for staged skills.
