---
name: meta-loop-efficiency
description: Weekly startup-loop skill efficiency audit. Scans lp-* + startup-loop + draft-outreach skills with deterministic heuristics (wc-l, grep, ls), emits a ranked opportunity artifact, and fires a planning anchor only on new-to-HIGH findings.
---

# /meta-loop-efficiency

Weekly audit of startup-loop skill files. Read-only scan. Writes one committed artifact per run.

## Invocation

```
/meta-loop-efficiency                     # default scan, commit artifact
/meta-loop-efficiency --threshold <N>    # custom line threshold (default 200)
/meta-loop-efficiency --dry-run          # print findings; do not commit
# implementation path: pnpm --filter scripts startup-loop:meta-loop-efficiency-audit -- --dry-run
```

## Operating Mode

**AUDIT ONLY** — no skill file modifications permitted.
Writes and commits one artifact per run (skipped on `--dry-run`).
Use the script-backed audit engine in `scripts/src/startup-loop/diagnostics/meta-loop-efficiency-audit.ts` for report generation.

## Audit Scope

In-scope: all `lp-*` prefix skills + `startup-loop` + `draft-outreach`.
Out-of-scope: `idea-*`, `meta-*`, `ops-*`, `review-*`, `biz-*`, `guide-*` — never scan these.
Canonical list derived from the startup-loop Stage Model in `startup-loop/SKILL.md`.

**No scope override is supported by design.** Non-loop skill families have different
invocation patterns and their own improvement cadences. For a full cross-portfolio scan,
run this skill against each family directory manually as a one-off operator action.

## Heuristics

All heuristics operate over ALL `.md` files in each skill directory (SKILL.md + modules/ + others), not SKILL.md alone.

### H0 — Duplicate candidate detection

SHA256-hash the content of each in-scope `SKILL.md` (normalize whitespace). Group skills with identical hashes. Emit a "Possible duplicates" section for any group of ≥2. Advisory only; does not affect H1–H3 scoring.

### H1 — Size / modularization

Threshold applies to `SKILL.md` orchestrator line count only:
- `wc -l SKILL.md` > threshold AND no `modules/` → **monolith** (strong signal)
- `wc -l SKILL.md` > threshold AND has `modules/` → **bloated-orchestrator** (weaker signal)
- `wc -l SKILL.md` ≤ threshold → **compliant**

Additional: if `modules/` exists and any module exceeds 400 lines → **module-monolith** advisory (logged, not ranked).

### H2 — Dispatch adoption gap

- `dispatch_refs_any_md`: count of `subagent-dispatch-contract` matches across ALL `.md` files in the skill directory
- `phase_matches_any_md`: matches of anchored heading pattern `^#{1,6}\s+(Phase|Stage|Domain|Step)\s+[0-9]+` across ALL `.md` files
- `dispatch_refs_any_md == 0` AND `phase_matches_any_md ≥ 3` → **dispatch-candidate**

**Implementation note (H2):** Use `grep -h` to suppress filenames before counting — `grep -c` with a single file omits the `filename:` prefix, causing `awk -F:` to produce wrong counts. Correct pattern:
```bash
find "$skill" -name "*.md" -exec grep -hE "^#{1,6} (Phase|Stage|Domain|Step) [0-9]+" {} \; | wc -l
```

### H3 — Wave dispatch adoption

Applies only to skills that reference `lp-do-build` as their execution skill AND have `phase_matches_any_md ≥ 3` (filters out skills that merely name lp-do-build as a downstream step).
If `wave-dispatch-protocol.md` is not referenced in any `.md` file in the directory → **wave-candidate** (advisory).

### H4 — Deterministic extraction opportunity

Detect skills where deterministic content likely belongs in executable/data artifacts (`.ts`, `.json`, `.yaml`) rather than prose:
- `deterministic_signal_count`: count matches across all skill `.md` for algorithmic markers (`regex`, `schema`, `validation contract`, `sort`, `dedupe`, `threshold`, `parse`, `normalize`, `map`, `filter`, `step-by-step decision table`)
- `artifact_ref_count`: count references to `.ts`, `.json`, `.yaml`, `.yml` in the skill directory docs
- If `deterministic_signal_count ≥ 6` AND `artifact_ref_count == 0` → **deterministic-extraction-candidate**

Advisory intent: trigger an idea to move repeatable logic into typed code/data artifacts with tests, not just split markdown.

### H5 — Shrink-without-simplification (anti-gaming)

Flag suspicious "line target passes" that likely just reshuffle prose:
- Compare current vs previous audit per skill using:
  - `SKILL.md` line delta
  - total `.md` footprint delta in the skill directory (`SKILL.md + modules/ + other .md`)
- If `SKILL.md` decreased by at least 20 lines but total `.md` footprint increased, and no new `.ts/.json/.yaml/.yml` references were introduced → **shrink-without-simplification**

This is advisory and should be called out as a quality risk, not counted as success.

## Ranking

Produce **three separate hierarchical ranked lists**. Do not merge H1, H2/H3, and H4/H5 signals.

### List 1 — Modularization opportunities (H1)

Rank within each tier by `SKILL.md` lines descending:
1. `high` tier — monolith or bloated-orchestrator
2. `medium` tier
3. `low` tier

### List 2 — Dispatch opportunities (H2 + H3)

Rank within each tier by `phase_matches_any_md` descending:
1. `high` tier — dispatch-candidate or wave-candidate
2. `medium` tier
3. `low` tier

### List 3 — Deterministic extraction and anti-gaming (H4 + H5)

Rank by severity:
1. `critical` — H5 `shrink-without-simplification`
2. `high` — H4 `deterministic-extraction-candidate` on high-tier skills
3. `medium` — H4 on medium-tier skills
4. `low` — H4 on low-tier skills

### Invocation tier assignments (fixed)

- **high**: startup-loop, lp-do-build, lp-do-plan, lp-do-replan, lp-do-sequence, lp-offer, lp-channels, lp-seo, lp-forecast, lp-do-fact-find
- **medium**: lp-launch-qa, lp-design-qa, lp-experiment, lp-design-spec, lp-prioritize, lp-site-upgrade
- **low**: lp-onboarding-audit, lp-assessment-bootstrap, lp-readiness, lp-baseline-merge, lp-measure, draft-outreach

Any `lp-*` skill not listed above defaults to **low** tier. Add new skills here when they enter the loop.

## Delta-Aware Planning Anchor

Always write the artifact. Emit planning anchor ONLY when findings are new:

1. Locate previous artifact: glob `docs/business-os/platform-capability/skill-efficiency-audit-[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9].md`, sort lexicographically, take last. Files not matching this exact pattern are excluded (lexicographic order equals timestamp order for this format).
2. For each skill flagged in List 1, List 2, or List 3:
   - Not in previous artifact → **new-to-HIGH** → emit planning anchor.
   - Already flagged → status: `known` (suppress anchor for that skill).
3. Any previously compliant skill now flagged → always emit planning anchor (regression).
4. No new items and no regressions → emit:
   > "No new HIGH opportunities since last audit (YYYY-MM-DD-HHMM). Known opportunities remain open — see previous anchor."

## Output Artifact

Path: `docs/business-os/platform-capability/skill-efficiency-audit-YYYY-MM-DD-HHMM.md`

Required header (first 6 lines of artifact body):
```
scan_timestamp: YYYY-MM-DD HH:MM
threshold: <N> lines
scope: lp-*, startup-loop, draft-outreach
git_sha: <HEAD SHA 7 chars>
previous_artifact: <filename or "none">
skills_scanned: <N>
```

Artifact sections:
1. **Scan summary** — header + scanned/compliant/opportunity counts
2. **Possible duplicates** (H0)
3. **List 1 — Modularization opportunities** (H1, hierarchical)
4. **List 2 — Dispatch opportunities** (H2/H3, hierarchical)
5. **List 3 — Deterministic extraction + anti-gaming** (H4/H5, hierarchical)
6. **Planning anchor** — when new-to-HIGH items exist: suggest `/lp-do-fact-find startup-loop-token-efficiency-v2`
7. **Delta status** — new-vs-known breakdown, regression flags

## Commit Guard

Before writing/committing the artifact:
1. Run `git status --porcelain`.
2. Stage ONLY the artifact file by explicit path: `git add docs/business-os/platform-capability/skill-efficiency-audit-<stamp>.md`
3. Verify with `git diff --cached --name-only` that only the artifact is staged.
4. If any unrelated files appear staged → abort; warn operator; do not commit.
5. Use writer lock: `scripts/agents/with-writer-lock.sh --wait-forever -- git commit`

Note: a dirty working tree (other unstaged changes) does NOT block the commit, provided
only the artifact file is staged. Use `--dry-run` to inspect output without committing.

## Heuristic Evolution

To extend or update this skill:
1. Add new heuristic `H<N>` section under `## Heuristics`.
2. Update `## Ranking` lists to include the new signal.
3. Add tier entries for any new `lp-*` skills added since last update.
4. Keep SKILL.md ≤200 lines; extract to `modules/heuristics.md` if needed.
