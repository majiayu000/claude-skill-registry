# Verified Curated Layer

Tracks #259. The analysis tooling that produced these numbers landed in #260
(`scripts/audit_skill_assets.py`, `scripts/verify_upstream_assets.py`,
`scripts/fetch_curated_skills.py`).

## Problem

The archive stores only `SKILL.md` + `metadata.json` per skill. Bundled assets —
scripts, templates, reference documents — are never downloaded. Measured against
the 2026-04-21 snapshot of 227,820 skills:

| Metric | Value |
|---|---|
| Pure-markdown skills (no local file references) | 48.2% |
| Claimed-EXEC candidates (>=100 stars, deduped by repo+dir) | 348 |
| Verified to ship executable assets upstream | 79 (57 repos) |
| Verified to ship docs/template assets only | 53 |
| Claim is false — upstream dir is SKILL.md-only | 109 (31%) |
| Upstream deleted or moved within ~3 months of archiving | 106 (30%) |

Two independent defects follow:

1. **The durable part is missing.** A capable model can regenerate a prose
   how-to; it cannot regenerate a working script it has never seen. The archive
   keeps the regenerable half and drops the other one.
2. **The index asserts things it never checked.** A record claiming bundled
   scripts is wrong 31% of the time, and 30% of upstreams disappear within a
   quarter. Both are presented to users with no confidence signal.

Note the second defect is not fixed by fetching assets once. At the measured
rot rate a static curated layer is ~30% stale within a quarter of its build.
Continuous re-verification is a requirement of this design, not a later phase.

## Non-Goals

- Re-archiving the full 227k corpus with assets. The curated layer is additive;
  the existing archive keeps its current layout and behavior.
- Removing or unpublishing pure-markdown skills. They are down-ranked, not
  dropped — see "Ranking" below.
- Executing or sandboxing any fetched asset. This layer distributes files; it
  does not run them.

## Data Model

### Curated storage (data repo)

Curated skills live under a dedicated root so they never collide with the
canonical `<category>/<skill>/` archive layout:

```
curated/<owner>__<repo>/<skill-basename>/
  SKILL.md
  <full upstream directory contents, recursively>
  _provenance.json
```

`_provenance.json` is already written by `fetch_curated_skills.py`. It gains the
fields the verification loop needs:

```json
{
  "repo": "acme/tools",
  "dir": "skills/alpha",
  "commit_sha": "<tree sha the fetch resolved>",
  "stars": 512,
  "verdict": "EXEC",
  "fetched_files": 7,
  "errors": [],
  "source": "https://github.com/acme/tools/tree/<sha>/skills/alpha",
  "first_verified_at": "2026-08-01T00:00:00Z",
  "last_verified_at": "2026-08-01T00:00:00Z",
  "liveness": "live"
}
```

`commit_sha` is new and load-bearing: `source` currently pins `HEAD`, which makes
a provenance record unreproducible the moment upstream moves. Fetch must resolve
and record the concrete sha.

`liveness` is one of `live` (upstream dir present at last check), `moved`
(repo reachable, skill dir gone), `gone` (repo 404/deleted/private).

### Registry records

Shard records (`registry-shards/*.json`) gain one optional object. Absent means
unverified, which is the current state of every record:

```json
"assets": {
  "verdict": "EXEC" | "REF_ASSET" | "BARE",
  "liveness": "live" | "moved" | "gone",
  "last_verified_at": "2026-08-01T00:00:00Z",
  "curated_path": "curated/acme__tools/alpha"
}
```

`curated_path` is present only for fetched skills. `verdict` here is the
*verified* verdict from the upstream tree — never the regex guess from
`classify_skill_text`, which is the thing measured to be wrong 31% of the time.
The regex stays a candidate filter and must not reach a published record.

## Change

Phased so each phase ships something verifiable on its own.

### Phase 1 — verified curated layer

1. `scripts/fetch_curated_skills.py`: resolve and record `commit_sha`; write the
   `first_verified_at` / `last_verified_at` / `liveness` / `verdict` fields.
2. New `scripts/build_curated_manifest.py`: walk `curated/`, emit
   `curated-manifest.json` (schema_version, generated_at, counts by verdict,
   per-skill provenance summary with sha256 per file).
3. `sync-data.yml`: push `curated/**` to the data repo alongside the archive.
4. Seed the layer from the 132 already-verified skills (79 EXEC + 53 REF_ASSET).

### Phase 2 — continuous liveness verification

5. New workflow `verify-curated.yml`, weekly. Re-runs upstream verification over
   every curated skill (one tree call per repo, ~57 repos today) and updates
   `liveness` + `last_verified_at` in provenance and manifest.
6. A skill that goes `moved`/`gone` keeps its fetched files — the archived copy
   is the point — but is marked in the manifest and reported.
7. New `scripts/check_curated_liveness.py`: fails the workflow when the
   `gone`+`moved` share crosses a configured threshold, so silent decay of the
   whole layer surfaces as a red run rather than a quiet metric.

### Phase 3 — surface it

8. `rebuild_registry.py` joins the curated manifest into shard records, emitting
   the `assets` object.
9. `build_search_index.py` exposes `verdict` and `liveness` as filterable
   facets.
10. Ranking: verified `EXEC`/`REF_ASSET` with `liveness: live` sort above
    unverified records at equal relevance. Down-rank only — no record is hidden
    on the basis of a verdict.

## Failure Behavior

Consistent with the existing intake and sync gates, and with why the guard in
#262 fails closed: a verification stage that cannot determine an answer must not
publish an optimistic one.

- Upstream tree call fails → record `repo_error`, keep the previous verdict and
  `last_verified_at`, do **not** rewrite either to a fresher-looking value.
- Curated manifest missing or unreadable during a registry rebuild → the `assets`
  object is omitted entirely. Never emit a partial or defaulted verdict.
- A record must never carry `verdict` without a `last_verified_at`.

## Done When

- `curated/` in the data repo holds the 132 verified skills, each with a
  `_provenance.json` carrying a concrete `commit_sha` and a `liveness` value.
- `curated-manifest.json` is rebuilt by CI and its counts match a fresh walk of
  `curated/`.
- `verify-curated.yml` has completed at least one scheduled run that flips at
  least one skill's `liveness` on real upstream movement, with the change
  visible in the manifest diff.
- `check_curated_liveness.py` fails a run when the decayed share crosses the
  threshold — proven with a fixture, not asserted.
- Shard records for curated skills carry `assets.verdict` and
  `assets.last_verified_at`; records for unverified skills carry no `assets` key.
- Search exposes verdict/liveness facets, and a verified-live skill outranks an
  unverified one at equal relevance.
- Every new script has pytest coverage meeting the repo's changed-line gate.

## Open Questions

1. **Scale of the curated layer.** 132 skills is what the >=100-star EXEC filter
   yields. Lowering the star floor to 25 would widen the candidate pool
   substantially, at a proportional increase in tree API calls. Needs a decision
   before Phase 1 seeds.
2. **License propagation.** The archive stores `SKILL.md` under whatever the
   upstream license permits; fetching full directories redistributes source
   files, which is a materially different act. Phase 1 should record the
   upstream license in provenance and skip repos with no license file — this
   spec does not settle whether skipping or flagging is correct.
3. **Data repo size.** 132 skills / 1,228 files is negligible, but the growth
   curve depends on question 1 and needs a ceiling before the layer scales.
