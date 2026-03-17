---
name: archive-full
description: Use when the user wants to package all source code into a tar.gz archive for upload or checkpoint. Creates a comprehensive archive excluding binaries and build artifacts.
---

# Archive Full Source

Package all source code in the repo into a single `.tar.gz` archive, excluding binaries and build artifacts.

## What's Included

All git-tracked files except:
- Binary files (`*.pack`, `*.bin`, `*.so`, `*.dylib`, `*.a`)
- Build artifacts (`target/`, `fuzz/target/`, `fuzz/artifacts/`, `fuzz/corpus/`)
- Generated files (`mutants.out*/`, `proptest-regressions/`, `tests/failures/`)
- OS files (`.DS_Store`)
- Existing archives (`*.tar.*`)
- Performance data (`perf.data`)

## Workflow

Run from the project root:

```bash
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
ARCHIVE="scanner-rs-full-${TIMESTAMP}.tar.gz"
git ls-files -z \
  | grep -zZv -e '\.pack$' -e '\.bin$' -e '\.so$' -e '\.dylib$' -e '\.a$' -e 'perf\.data' \
  | tar czf "${ARCHIVE}" --null -T -
echo "Created ${ARCHIVE} ($(du -h "${ARCHIVE}" | cut -f1))"
```

Report the archive name and size to the user when done.
