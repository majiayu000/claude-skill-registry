# Claude Skill Registry (Data)

This repo contains the **archived skill contents** (the heavy, browsable skill files).

**Canonical layout**
- Category folders at repo root (e.g. `development/`, `documents/`, `data/`, …)
- Each skill lives under a category: `<category>/<skill>/SKILL.md` + `<category>/<skill>/metadata.json`
- Case conflicts are resolved with `{name}-{owner}-{repo}` suffixes (fallback: `-{short-hash}`).

**Archive size**
- **226,042** `SKILL.md` files (as of 2026-04-08)

**Where the index + site live**
- Core repo: https://github.com/majiayu000/claude-skill-registry-core
- Main repo (full archive + scripts): https://github.com/majiayu000/claude-skill-registry
