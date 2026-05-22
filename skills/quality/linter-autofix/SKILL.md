---
model: haiku
name: Linter Autofix Patterns
description: Cross-language linter autofix commands and common fix patterns for biome, ruff, clippy, shellcheck, and more.
allowed-tools: Bash, Read, Edit, Grep
---

# Linter Autofix Patterns

Quick reference for running linter autofixes across languages.

## Autofix Commands

| Language | Linter | Autofix Command |
|----------|--------|-----------------|
| TypeScript/JS | biome | `bunx @biomejs/biome check --write .` |
| TypeScript/JS | biome format | `bunx @biomejs/biome format --write .` |
| Python | ruff | `ruff check --fix .` |
| Python | ruff format | `ruff format .` |
| Rust | clippy | `cargo clippy --fix --allow-dirty` |
| Rust | rustfmt | `cargo fmt` |
| Go | gofmt | `gofmt -w .` |
| Go | go mod | `go mod tidy` |
| Shell | shellcheck | apply shellcheck -f diff suggestions |

## Common Fix Patterns

### JavaScript/TypeScript (Biome)

**Unused imports**
```typescript
// Before
import { useState, useEffect, useMemo } from 'react';
// Only useState used

// After
import { useState } from 'react';
```

**Prefer const**
```typescript
// Before
let x = 5;  // Never reassigned

// After
const x = 5;
```

### Python (Ruff)

**Import sorting (I001)**
```python
# Before
import os
from typing import List
import sys

# After
import os
import sys
from typing import List
```

**Unused imports (F401)**
```python
# Before
import os
import sys  # unused

# After
import os
```

**Line too long (E501)**
```python
# Before
result = some_function(very_long_argument_one, very_long_argument_two, very_long_argument_three)

# After
result = some_function(
    very_long_argument_one,
    very_long_argument_two,
    very_long_argument_three,
)
```

### Rust (Clippy)

**Redundant clone**
```rust
// Before
let s = String::from("hello").clone();

// After
let s = String::from("hello");
```

**Use if let**
```rust
// Before
match option {
    Some(x) => do_something(x),
    None => {},
}

// After
if let Some(x) = option {
    do_something(x);
}
```

### Shell (ShellCheck)

**Quote variables (SC2086)**
```bash
# Before
echo $variable

# After
echo "$variable"
```

**Use $(...) instead of backticks (SC2006)**
```bash
# Before
result=`command`

# After
result=$(command)
```

## Quick Autofix (Recommended)

Auto-detect project linters and run all appropriate fixers in one command:

```bash
# Fix mode: detect linters and apply all autofixes
bash "${CLAUDE_PLUGIN_ROOT}/skills/linter-autofix/scripts/detect-and-fix.sh"

# Check-only mode: report issues without fixing
bash "${CLAUDE_PLUGIN_ROOT}/skills/linter-autofix/scripts/detect-and-fix.sh" --check-only
```

The script detects biome, eslint, prettier, ruff, black, clippy, rustfmt, gofmt, golangci-lint, and shellcheck. It reports which linters were found, runs them, and shows modified files. See [scripts/detect-and-fix.sh](scripts/detect-and-fix.sh) for details.

## Manual Workflow

1. Run autofix first: `ruff check --fix . && ruff format .`
2. Check remaining issues: `ruff check .`
3. Manual fixes for complex cases
4. Verify: re-run linter to confirm clean

## When to Escalate

Stop and use different approach when:
- Fix requires understanding business logic
- Multiple files need coordinated changes
- Warning indicates potential bug (not just style)
- Security-related linter rule
- Type error requires interface/API changes
