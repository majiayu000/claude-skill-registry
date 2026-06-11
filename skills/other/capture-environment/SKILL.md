---
name: capture-environment
description: Snapshot the computational environment for a replication package — detects the analysis stack (R / Stata / Python) and emits the right lockfiles (renv.lock + sessionInfo.txt, requirements.txt / environment.yml / uv.lock, Stata version + ado package list), records seeds and RNG kind, optionally writes a pinning Dockerfile, and produces a paste-ready "Computational requirements" block. Use when user says "capture the environment", "snapshot my dependencies", "pin the versions", "make a renv.lock / requirements.txt", "make this byte-reproducible", or before releasing a replication package to openICPSR / the AEA Data Editor.
argument-hint: "[project-dir] [--docker] [--no-verify] (project-dir defaults to repo root)"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash"]
effort: medium
---

# `/capture-environment` — snapshot the computational environment

A replication package that runs on the author's laptop in 2026 and nowhere else in 2029 is not reproducible. This skill captures the *exact* computational environment — language versions, package versions, seeds, RNG kind, and (optionally) the OS layer — so a referee, the AEA Data Editor, or future-you can reconstruct it. It detects which stack the project uses and emits the artifacts that stack's ecosystem expects, then verifies the lockfile installs clean.

**Core principle:** Pin everything a result depends on. Display rounding aside, a re-run on a pinned environment should reproduce the paper to the [`replication-protocol.md`](../../rules/replication-protocol.md) tolerances — *byte-identical* when the optional Dockerfile is used.

## When to use

- **Before releasing a replication package** to openICPSR, Zenodo, Dataverse, or a journal archive — the AEA Data Editor / DCAS standard expects a documented, version-pinned environment.
- **Before submission**, alongside [`/audit-reproducibility`](../audit-reproducibility/SKILL.md) — that skill checks the *numbers*; this one captures the *environment* those numbers were produced in (its `sessionInfo.txt` requirement is satisfied by this skill).
- **After adding or upgrading a package** mid-project — re-snapshot so the lockfile doesn't drift from what the code actually loads.
- **When handing a project to a co-author or RA** who needs to reconstruct your stack.

## Inputs

- `$0` — project directory. Defaults to the repo root. The skill looks under `scripts/R/`, `scripts/stata/`, `scripts/python/`.
- `--docker` — also emit a `Dockerfile` pinning OS + language version + system libraries for byte-identical reproduction.
- `--no-verify` — skip Phase 3 (the best-effort clean-install check). Useful in CI or when the toolchain isn't installed locally.

## Workflow

### Phase 0: Detect the stack

Glob for stack signals and decide which capture paths to run (a project may be multi-language — DiD in R, an IV robustness check in Stata):

| Signal | Stack | Capture path |
|---|---|---|
| `scripts/R/*.R`, `DESCRIPTION`, `renv/`, `*.Rproj` | **R** | renv + sessionInfo |
| `scripts/python/*.py`, `*.ipynb`, `pyproject.toml`, `requirements.txt`, `environment.yml`, `uv.lock` | **Python** | pip / conda / uv |
| `scripts/stata/*.do` | **Stata** | version + ado list |

If no signal is found, report and stop — there is no environment to capture.

### Phase 1: Capture per language

**R** — emit two artifacts:
- `renv.lock` via `renv::snapshot()` (run `renv::init(bare = TRUE)` first if the project isn't renv-managed; snapshot records every package + version + source/remote and the R version). Honors the seed conventions in [`r-code-conventions.md`](../../rules/r-code-conventions.md).
- `sessionInfo.txt` via `Rscript -e "writeLines(capture.output(sessionInfo()), 'scripts/R/_outputs/sessionInfo.txt')"` — the human-readable companion `/audit-reproducibility` looks for.

**Python** — emit whichever matches the project's existing tooling (do not invent a new one):
- `uv.lock` (preferred when `pyproject.toml` + `uv` present — fully-resolved, hashed, cross-platform): `uv lock` / `uv export --format requirements-txt > requirements.txt`.
- `requirements.txt` via `pip freeze` (or `python -m pip freeze`) for a venv/pip project — pin `==` exactly.
- `environment.yml` via `conda env export --no-builds` for a conda project.
Always also record the interpreter version (`python --version`) in the report.

**Stata** — Stata has no lockfile, so capture the closest equivalents (mirrors [`stata-code-conventions.md`](../../rules/stata-code-conventions.md) §3):
- The pinned `version` line each `.do` file declares (e.g. `version 18`) — grep `scripts/stata/*.do` and report the version actually pinned.
- An ado/plus package inventory: a small `.do` that runs `which` on the user-installed commands the pipeline uses (`reghdfe`, `ivreg2`, `estout`/`esttab`, `rdrobust`, `csdid`, …) plus `ado dir` and `about`, logged to `scripts/stata/_outputs/sessionInfo.txt`.
- A note that Stata version pinning is *semantic* (`version 18` fixes command behavior), not a binary pin — the Dockerfile (Phase 2) cannot help here because Stata is licensed and not redistributable; record the exact Stata version + flavor (SE/MP/IC) + update level in the report so a replicator can match it.

### Phase 1b: Record seeds and RNG

Grep the analysis scripts for the master seed and RNG kind so the "Computational requirements" block can state them:
- **R**: `set.seed(YYYYMMDD)`, and `RNGkind()` — flag `"L'Ecuyer-CMRG"` if parallel/Monte Carlo work is present (see [`simulation-conventions.md`](../../rules/simulation-conventions.md)).
- **Stata**: `set seed` and `set sortseed`.
- **Python**: `numpy.random.default_rng(seed)` / `random.seed()` / framework seeds.

If the pipeline does randomized work (bootstrap, MC, RCT re-randomization, permutation inference) and **no** seed is found, surface it as a WARNING — an unseeded random result is not reproducible.

### Phase 2: Dockerfile (only with `--docker`)

Emit a `Dockerfile` that pins the OS + language version + system libraries for byte-identical reproduction:
- **R** → `FROM rocker/r-ver:<X.Y.Z>` (Rocker pins the R version), `COPY renv.lock`, `RUN R -e "renv::restore()"`, plus `apt-get install` for system libs the packages need (e.g. `libcurl4-openssl-dev`, `libgdal-dev` for spatial work).
- **Python** → `FROM python:<X.Y.Z>-slim`, `COPY requirements.txt` / `uv.lock`, `RUN pip install -r requirements.txt` (or `uv sync --frozen`).
- **Stata** → cannot pin the licensed binary; emit a `Dockerfile` stub that documents the expected Stata version + flavor and leaves the `stata` install/license step to the replicator (with a comment pointing at the AEA's guidance on Stata images).

Pin a digest where possible (`FROM image@sha256:…`) so the base image can't drift.

### Phase 3: Verify the lockfile installs clean (best-effort; skip with `--no-verify`)

Attempt a clean restore in a throwaway location and report PASS / FAIL — never overwrite the working environment:
- **R**: `renv::restore()` into a temp library, or `Rscript -e "renv::status()"` for a dry check.
- **Python**: `uv sync --frozen` / `pip install --dry-run -r requirements.txt` into a fresh venv.
- **Docker** (if `--docker`): `docker build` the image.

A FAIL here means the lockfile references a package version that can't be resolved (yanked release, private remote, platform-specific wheel). Report it; do not auto-edit the lockfile.

### Phase 4: Report

Print a paste-ready block and write it to `scripts/<lang>/_outputs/computational_requirements.md`:

```markdown
## Computational requirements

**Software:** R 4.4.1 (or: Stata 18.0 SE, update 2026-01-15; Python 3.12.3)
**OS used:** macOS 15.5 (arm64) — Dockerfile pins Ubuntu 24.04 for portability
**Key packages:** fixest 0.12.1, did 2.1.2 (full list in renv.lock)
**Random seeds:** set.seed(20260609); RNGkind("L'Ecuyer-CMRG") for the bootstrap
**Approx. runtime:** [author confirms — e.g. ~12 min, 8 cores]
**Lockfiles in package:** renv.lock, scripts/R/_outputs/sessionInfo.txt[, Dockerfile]
```

Pre-fill software/package/seed lines from the captured artifacts; leave runtime for the author to confirm.

## Output / artifacts

| Stack | Files written |
|---|---|
| R | `renv.lock`, `scripts/R/_outputs/sessionInfo.txt` |
| Python | `requirements.txt` *or* `environment.yml` *or* `uv.lock` (matching project tooling) |
| Stata | `scripts/stata/_outputs/sessionInfo.txt` (version + ado list) |
| Any (`--docker`) | `Dockerfile` |
| Always | `scripts/<lang>/_outputs/computational_requirements.md` (the paste-ready block) |

## Exit behavior

- **All captures succeeded, verify PASS (or `--no-verify`):** exit 0, requirements block printed.
- **A missing-seed WARNING on a randomized pipeline:** exit 0 with the warning surfaced — reproducibility is compromised but the snapshot still wrote.
- **Verify FAIL (lockfile won't resolve):** exit 1, so the skill can gate a pre-release `/commit`. Report the unresolvable package; do not silently "fix" the lockfile.
- **No stack detected in Phase 0:** exit 1 with the directories searched.

## Cross-references

- [`.claude/rules/replication-protocol.md`](../../rules/replication-protocol.md) — the tolerance contract a pinned environment is meant to reproduce.
- [`.claude/rules/r-code-conventions.md`](../../rules/r-code-conventions.md) — R seeding + output-path conventions this skill reads.
- [`.claude/rules/stata-code-conventions.md`](../../rules/stata-code-conventions.md) — §3 `sessionInfo.txt` + `version`-pinning the Stata path mirrors.
- [`.claude/rules/simulation-conventions.md`](../../rules/simulation-conventions.md) — L'Ecuyer streams for reproducible parallel/MC work.
- [`.claude/rules/confidential-data.md`](../../rules/confidential-data.md) — when raw data is restricted, the *environment* still ships even though the data does not; coordinate the README's "data availability" section with this block.
- [`/audit-reproducibility`](../audit-reproducibility/SKILL.md) — consumes the `sessionInfo.txt` this skill produces; run it after.
- [`/data-analysis`](../data-analysis/SKILL.md), [`/stata-replication`](../stata-replication/SKILL.md), [`/simulation-study`](../simulation-study/SKILL.md) — the pipelines whose environment this snapshots.
- [AEA Data Editor checklist](https://aeadataeditor.github.io/) / [openICPSR](https://www.openicpsr.org/) / DCAS — the external standards this skill targets.

## What this skill does NOT do

- **Re-run your analysis or check your numbers.** It captures the environment; [`/audit-reproducibility`](../audit-reproducibility/SKILL.md) verifies the manuscript's numeric claims against the outputs.
- **Package or de-identify data.** Lockfiles describe software, not data. Disclosure avoidance, de-identification, and data-availability statements are out of scope — see [`confidential-data.md`](../../rules/confidential-data.md).
- **Upgrade or "fix" your dependencies.** It records what the code currently uses. If a verify FAIL surfaces a yanked version, you decide whether to pin an alternative.
- **Pin a Stata binary.** Stata is licensed and not redistributable; the skill records the exact version/flavor/update so a replicator can match it, but cannot containerize it.
