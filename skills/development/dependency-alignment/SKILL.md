---
name: dependency-alignment
description: Dependency version alignment and conflict resolution for parallel development. Use when extracting dependencies from Tech Specs to ensure version compatibility with existing project dependencies and transitive dependencies.
user-invocable: false
---

# Dependency Version Alignment Skill

This skill resolves dependency versions during parallel decomposition to ensure compatibility with existing project dependencies and avoid transitive conflicts.

## When This Skill Activates

- During `parallel-decompose` Phase 1 (after dependency extraction, before manifest generation)
- When the cto-architect agent identifies dependencies from Tech Spec imports
- When validating manifest.json dependencies before execution

## Supported Ecosystems

| Ecosystem | Dependency Files | Package Manager | Resolution Tool |
|-----------|-----------------|-----------------|-----------------|
| Python | `pyproject.toml`, `requirements.txt`, `uv.lock` | uv, pip | `uv pip compile` |
| Node.js | `package.json`, `package-lock.json`, `yarn.lock` | npm, yarn, pnpm | `npm view`, `npm ls` |

## Detection Strategy

### Python Projects

1. Check for `pyproject.toml` (preferred - modern Python)
2. Fall back to `requirements.txt` (legacy)
3. Check for lock files: `uv.lock`, `poetry.lock`, `requirements.lock`

```bash
# Detection order
if [[ -f "pyproject.toml" ]]; then
  # Use pyproject.toml as source of truth
elif [[ -f "requirements.txt" ]]; then
  # Fall back to requirements.txt
fi
```

### Node.js Projects

1. Check for `package.json` (required)
2. Check for lock files: `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`

```bash
# Detection
if [[ -f "package.json" ]]; then
  # Node.js project detected
fi
```

## Resolution Commands

### Python with uv

```bash
# Step 1: Get currently installed/locked versions
uv pip freeze --format json

# Step 2: Resolve a new dependency against existing project
# Creates a temporary requirements and resolves compatible version
uv pip compile pyproject.toml \
  --extra-requirement "pydantic>=2.0" \
  --dry-run \
  --quiet 2>&1

# Step 3: Get the resolved version for a specific package
uv pip compile - <<< "pydantic>=2.0" --dry-run 2>&1 | grep "pydantic=="

# Alternative: Check latest compatible version
uv pip compile - <<< "pydantic>=2.0,<3.0" --dry-run 2>&1
```

**Parsing uv output:**
- Success: Extract pinned version from output (e.g., `pydantic==2.5.3`)
- Conflict: Parse error message for incompatible version ranges

### Node.js with npm

```bash
# Step 1: Get current dependency tree
npm ls --all --json 2>&1

# Step 2: Check what version would be installed
npm view zod@">=3.0" version --json

# Step 3: Check for peer dependency conflicts
npm install zod@">=3.0" --dry-run --json 2>&1

# Step 4: Explain dependency resolution
npm explain zod
```

**Parsing npm output:**
- Success: Extract resolved version from `npm view` output
- Conflict: Parse `ERESOLVE` errors for peer dependency issues

## Conflict Resolution Strategies

### Strategy 1: Pin to Compatible Version (Default)

When a requested version range can be satisfied:
1. Resolve to the latest version within the range
2. Pin to exact version in manifest
3. No warning needed

```
Requested: pydantic>=2.0
Resolved:  pydantic==2.5.3
```

### Strategy 2: Upgrade Existing Dependency

When new requirement needs a higher version than currently installed:
1. Check if upgrade is compatible with other dependencies
2. Move to `upgrade` list with pinned version
3. Resolution tool validates compatibility

```
Current:   requests==2.25.1
Requested: requests>=2.28
Resolved:  requests==2.31.0 (in upgrade list)
```

### Strategy 3: Find Compatible Range

When direct version causes conflict:
1. Find version that satisfies both constraints
2. Use the compatible version
3. Log the resolution for transparency

```
Existing:  sqlalchemy>=1.4,<2.0 (from another package)
Requested: sqlalchemy>=2.0
Conflict:  No compatible version
Action:    Error with explanation, requires manual resolution
```

## Output Format

Dependencies are output as **pinned version strings**:

### Python Format

```json
{
  "dependencies": {
    "python": {
      "add": ["pydantic==2.5.3", "sqlalchemy==2.0.25", "httpx==0.27.0"],
      "upgrade": ["requests==2.31.0"],
      "remove": [],
      "add_dev": ["pytest==7.4.3", "pytest-asyncio==0.21.1", "mypy==1.8.0"]
    }
  }
}
```

### Node.js Format

```json
{
  "dependencies": {
    "node": {
      "add": ["zod@3.22.4", "express@4.18.2", "@types/node@20.10.0"],
      "upgrade": ["axios@1.6.2"],
      "remove": [],
      "add_dev": ["typescript@5.3.3", "vitest@1.2.0", "eslint@8.56.0"]
    }
  }
}
```

**Format conventions:**
- Python: `package==version` (PEP 440)
- Node.js: `package@version` (npm convention)
- All versions are pinned (exact, not ranges)

## Integration with parallel-decompose

### Step 7b in Phase 1

After extracting dependencies from Tech Spec imports (Step 7), invoke this skill:

```markdown
7b. Align dependency versions (invoke `dependency-alignment` skill):
    - Detect project ecosystem (Python/Node.js)
    - For each extracted dependency:
      a. Query resolution tool for compatible version
      b. Check against existing project dependencies
      c. Resolve conflicts automatically
    - Output pinned versions for manifest.json
```

### Resolution Workflow

```
Tech Spec imports → Extract packages → Resolve versions → Pinned manifest

Example:
  from pydantic import BaseModel  →  pydantic (no version)
  from sqlalchemy import ...      →  sqlalchemy (no version)
                                  ↓
  uv pip compile --dry-run       →  pydantic==2.5.3
                                     sqlalchemy==2.0.25
                                  ↓
  manifest.json                  →  "add": ["pydantic==2.5.3", "sqlalchemy==2.0.25"]
```

## Error Handling

### Unresolvable Conflicts

When no compatible version exists:

```
ERROR: Cannot resolve dependency conflict

Package: sqlalchemy
Requested: >=2.0 (from Tech Spec)
Existing: <2.0 (required by flask-sqlalchemy==2.5.1)

Resolution options:
1. Upgrade flask-sqlalchemy to >=3.0 (supports SQLAlchemy 2.x)
2. Modify Tech Spec to use SQLAlchemy 1.4 API
3. Remove flask-sqlalchemy and use SQLAlchemy directly

Action required: Manual resolution before proceeding
```

### Network/Tool Unavailable

When resolution tools are unavailable:

```
WARNING: uv not available, falling back to version ranges

Dependencies will use version specifiers instead of pinned versions:
  "add": ["pydantic>=2.0", "sqlalchemy>=2.0"]

Run with uv installed for reproducible pinned versions.
```

## Best Practices

1. **Always resolve before execution**: Run resolution during decomposition, not during task execution
2. **Pin all versions**: Pinned versions ensure reproducibility across parallel agents
3. **Document conflicts**: Log any version adjustments for transparency
4. **Test resolution**: Validate resolved versions work together before multi-agent execution
5. **Lock files**: After successful execution, commit lock files (uv.lock, package-lock.json)
