# Fast clone / update (repo has lots of files)

This project has two very different clone profiles:

- `claude-skill-registry-core`: pipeline + docs + indexes, relatively light
- `claude-skill-registry-data`: archived skill tree, very heavy

A normal `git clone` / `git pull` can feel slow because Git needs to update and scan a very large working tree.

If you only need the registry + tooling (scripts/docs) and not the full skill archive, use **partial clone + sparse checkout**.

## New clone (recommended)

```bash
git clone --filter=blob:none --sparse https://github.com/majiayu000/claude-skill-registry-core.git
cd claude-skill-registry-core
git sparse-checkout set --cone docs scripts sources schema
```

If you only need counts, prefer `registry_summary.json` instead of opening the full `registry.json`.

## Data repo clone (recommended)

If you need archived skills locally, do **not** full-clone the data repo first. Start shallow + blobless + sparse:

```bash
git clone --filter=blob:none --depth 1 --sparse https://github.com/majiayu000/claude-skill-registry-data.git
cd claude-skill-registry-data
git sparse-checkout init --cone
git sparse-checkout set development documents
```

Need more categories later?

```bash
git sparse-checkout add data design testing
```

## Existing clone: switch to sparse checkout

```bash
git sparse-checkout init --cone
git sparse-checkout set --cone docs scripts sources schema
```

## Get the full checkout (slow)

If you truly need everything:

```bash
git sparse-checkout disable
```

For the data repo, this is the expensive step. Avoid it unless you really need the entire archive on disk.

## Optional: Git performance tuning

These settings can help on large repos:

```bash
git config feature.manyFiles true
git config core.untrackedCache true
git maintenance start
```

## Don’t clone at all (fastest)

If you just want the data, prefer direct JSON fetches:

- Summary counts: `registry_summary.json` (GitHub raw)
- Full registry: `registry.json` (GitHub raw, much larger)
- Lightweight search: `docs/search-index.json` (or `.gz`)
