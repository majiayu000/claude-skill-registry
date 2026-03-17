---
name: archive-src
description: Use when the user wants a minimal source-only archive for upload or checkpoint. Creates a tar.gz with just src/ and tests/ directories.
---

# Archive Source + Tests

Package only `src/` and `tests/` into a compact `.tar.gz` archive.

## What's Included

- `src/**` - All source code
- `tests/**` - All test files (integration, property, smoke, simulation, diagnostic, corpus)
- `Cargo.toml` - Project manifest (needed for context)

## What's Excluded

Everything else: benches, fuzz, docs, config files, lock file, CI, `.claude/`, `.github/`, binaries.

## Workflow

Run from the project root:

```bash
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
ARCHIVE="scanner-rs-src-${TIMESTAMP}.tar.gz"
git ls-files -z -- 'src/' 'tests/' 'Cargo.toml' \
  | grep -zZv -e '\.pack$' -e '\.bin$' \
  | tar czf "${ARCHIVE}" --null -T -
echo "Created ${ARCHIVE} ($(du -h "${ARCHIVE}" | cut -f1))"
```

Report the archive name and size to the user when done.
