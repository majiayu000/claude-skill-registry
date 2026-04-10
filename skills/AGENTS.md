## Repository Policy (Archive-Only)
- **This repo stores archived skill contents only.**
- Canonical layout is `<category>/<skill>/SKILL.md` + `<category>/<skill>/metadata.json` at category folders in the repo root.
- Discovery, dedupe, registry generation, search-index generation, Pages, and publish orchestration belong in `claude-skill-registry-core`, not here.
- If behavior or docs conflict across repos, follow **core** implementation and sync others to match.

## Edit Routing
- Edit this repo for archived `SKILL.md` files, `metadata.json`, and archive-local documentation.
- Edit `claude-skill-registry-core` for workflows, scripts, pipeline docs, search/index outputs, and publish logic.
- Edit `claude-skill-registry` only for main-owned publish wiring that is intentionally excluded from core sync.

## Count And Freshness Rule
- Do not hardcode archive counts or dates in this repo's `README.md`.
- Prefer live badges or values sourced from `claude-skill-registry-core` `stats.json`.
- If a count looks wrong, fix the producer in `core` or rerun the `core` pipeline instead of patching numbers manually.

## Case-Conflict Policy
- No paths may differ only by case.
- Directory conflict suffix policy must match `core/scripts/utils.py`:
  - Prefer `{name}-{owner}-{repo}`.
  - Fallback: `-{short-hash}`.
  - If needed, append numeric disambiguators.
- Do not delete skills to resolve conflicts; rename them deterministically.
