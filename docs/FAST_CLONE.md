# Fast clone / update (repo has lots of files)

This repo tracks ~200k+ files. A normal `git clone` / `git pull` can feel slow because Git needs to update and scan a very large working tree.

If you only need the registry + tooling (scripts/docs) and not the full `skills/` tree, use **partial clone + sparse checkout**.

## New clone (recommended)

```bash
git clone --filter=blob:none --sparse https://github.com/majiayu000/claude-skill-registry.git
cd claude-skill-registry
git sparse-checkout set --cone docs scripts sources schema
```

Need a subset of skills later?

```bash
git sparse-checkout add skills/development
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

## Optional: Git performance tuning

These settings can help on large repos:

```bash
git config feature.manyFiles true
git maintenance start
```

## Don’t clone at all (fastest)

If you just want the data, you can fetch JSON directly:

- Full registry: `registry.json` (GitHub raw)
- Lightweight search: `docs/search-index.json` (or `.gz`)
