---
name: quality-detect-orphaned-code
description: |
  Detects orphaned code (files/functions that exist but are never imported or called in production),
  preventing "created but not integrated" failures. Use before marking features complete, before moving
  ADRs to completed, during code reviews, or as part of quality gates. Triggers on "detect orphaned code",
  "find dead code", "check for unused modules", "verify integration", or proactively before completion.
  Works with Python modules, functions, classes, and LangGraph nodes. Catches the ADR-013 failure pattern
  where code exists and tests pass but is never integrated.
allowed-tools:
  - Read
  - Grep
  - Bash
  - Glob
---

# Detect Orphaned Code

## Quick Start

Run orphan detection before marking any feature complete:

```bash
# Quick check for a specific module
grep -r "from.*your_module import\|import.*your_module" src/ --include="*.py" | grep -v test

# If output is EMPTY → Module is orphaned (not imported in production)

# Comprehensive orphan detection (if script exists)
./scripts/verify_integration.sh

# Check specific function usage
grep -r "your_function_name" src/ --include="*.py" | grep -v test | grep -v "^[^:]*:.*def "

# If output is EMPTY → Function is orphaned (never called)
```

## Table of Contents

1. When to Use This Skill
2. What This Skill Does
3. Types of Orphaned Code
4. Detection Methods
5. Step-by-Step Detection Process
6. Automated Detection Scripts
7. Integration with Quality Gates
8. Supporting Files
9. Expected Outcomes
10. Requirements
11. Red Flags to Avoid

## When to Use This Skill

### Explicit Triggers
- "Detect orphaned code"
- "Find dead code in the project"
- "Check for unused modules"
- "Verify no orphaned files exist"
- "Find code that's never imported"
- "Check for integration gaps"

### Implicit Triggers (PROACTIVE)
- **Before marking any feature complete**
- **Before moving ADR from in_progress to completed**
- **After creating new Python modules**
- **After major refactoring**
- **As part of pre-commit quality gates**
- **During code review**

### Debugging Triggers
- "Tests pass but feature doesn't work" (often orphaned code)
- "File exists but nothing happens when I run it"
- "Why isn't my new module being used?"
- "Code review found unused imports"

## What This Skill Does

This skill **detects code that exists but is never used**, preventing the ADR-013 failure mode:

**What it detects:**
1. **Orphaned modules** - Python files never imported in production code
2. **Orphaned functions** - Functions defined but never called
3. **Orphaned classes** - Classes defined but never instantiated
4. **Orphaned nodes** - LangGraph nodes never added to graph
5. **Dead code paths** - Code wired but conditionals never trigger

**What it prevents:**
- Marking incomplete features as "done"
- Moving ADRs to completed when code isn't integrated
- Accumulating technical debt (unused code)
- Confusion for future developers (why does this exist?)

**Why existing tools miss this:**
- **vulture** - Can be fooled by unit tests that import modules
- **mypy** - Only checks types, not usage
- **pytest** - Can pass 100% coverage on orphaned modules
- **ruff** - Checks style, not integration

**This skill complements those tools** by checking integration explicitly.

## Types of Orphaned Code

### Type 1: Orphaned Module (File Never Imported)

**Symptom:** Python file exists, has tests, but is never imported in production code

**Example:**
```python
# File: src/myapp/features/new_feature.py (175 lines)
def process_data(data: dict) -> Result:
    """Process data and return result."""
    # ... implementation ...
```

**Detection:**
```bash
$ grep -r "from.*new_feature import\|import.*new_feature" src/ --include="*.py" | grep -v test
(empty) ❌
```

**Root cause:** File created but never imported in integration point

**Fix:** Import in the consuming module

### Type 2: Orphaned Function (Defined But Never Called)

**Symptom:** Function exists in imported module but is never called

**Example:**
```python
# File: src/myapp/services/utils.py
def helper_function(x: int) -> int:  # Orphaned
    return x * 2

def another_function(x: int) -> int:  # Used
    return x + 1
```

**Detection:**
```bash
$ grep -r "helper_function" src/ --include="*.py" | grep -v test | grep -v "def helper_function"
(empty) ❌  # Only definition, no call-sites

$ grep -r "another_function" src/ --include="*.py" | grep -v test | grep -v "def another_function"
src/myapp/main.py:45:    result = another_function(5)  ✅  # Has call-site
```

**Root cause:** Function created but never invoked

**Fix:** Call the function where needed, or remove it

### Type 3: Orphaned Class (Defined But Never Instantiated)

**Symptom:** Class exists but is never instantiated or subclassed

**Example:**
```python
# File: src/myapp/models/new_model.py
class NewModel:
    def __init__(self, data: dict) -> None:
        self.data = data
```

**Detection:**
```bash
$ grep -r "NewModel" src/ --include="*.py" | grep -v test | grep -v "class NewModel"
(empty) ❌  # Only definition, no instantiation
```

**Root cause:** Class created but never used

**Fix:** Instantiate where needed, or remove

### Type 4: Orphaned LangGraph Node (Node File Exists But Not in Graph)

**Symptom:** Node factory function exists but is never added to graph

**Example:**
```python
# File: src/myapp/graph/architecture_nodes.py
async def create_architecture_review_node(agent):
    """Create architecture review node."""
    # ... implementation ...
```

**Detection:**
```bash
$ grep "architecture_nodes" src/myapp/graph/builder.py
(empty) ❌  # Not imported in builder

$ grep "add_node.*architecture_review" src/myapp/graph/builder.py
(empty) ❌  # Not added to graph
```

**Root cause:** Node created but never wired into graph

**Fix:** Import and add to graph in builder.py

### Type 5: Dead Code Path (Code Wired But Conditional Never Triggers)

**Symptom:** Code is integrated but the path to reach it never executes

**Example:**
```python
# In builder.py
if settings.enable_experimental_features:  # Never True in production
    graph.add_node("experimental", experimental_node)
```

**Detection:**
```bash
# Check configuration
$ grep "enable_experimental_features" .env
# Not set (defaults to False)

# Check logs for execution
$ grep "experimental" logs/*.log
(empty) ❌  # Never executes
```

**Root cause:** Conditional never true in practice

**Fix:** Enable the condition or remove the dead path

## Detection Methods

### Method 1: Manual Grep (Quick Check)

**For a specific module:**
```bash
# Check if module is imported
grep -r "from.*MODULE_NAME import\|import.*MODULE_NAME" src/ --include="*.py" | grep -v test

# Expected: At least one import line from production code
# If empty: Module is orphaned
```

**For a specific function:**
```bash
# Check if function is called
grep -r "FUNCTION_NAME" src/ --include="*.py" | grep -v test | grep -v "def FUNCTION_NAME"

# Expected: At least one call-site
# If empty: Function is orphaned
```

**For a specific class:**
```bash
# Check if class is instantiated
grep -r "CLASS_NAME(" src/ --include="*.py" | grep -v test | grep -v "class CLASS_NAME"

# Expected: At least one instantiation
# If empty: Class is orphaned
```

### Method 2: Comprehensive Script (Automated)

**Script: `scripts/verify_integration.sh`**

```bash
#!/bin/bash
# Detects orphaned modules (created but never imported in production)

set -e

echo "=== Orphan Detection ==="

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

orphaned=0
checked=0

for file in $(find src/ -name "*.py" -type f | sort); do
    module=$(basename "$file" .py)
    dir=$(dirname "$file")

    # Skip special files
    [[ "$module" == "__init__" ]] && continue
    [[ "$module" == "__main__" ]] && continue
    [[ "$module" == "main" ]] && continue
    [[ "$module" == *"test"* ]] && continue

    checked=$((checked + 1))

    # Check if module is imported (excluding self and tests)
    imports=$(grep -r -E "import\s+.*\b${module}\b|from\s+.*\b${module}\b\s+import" src/ \
              --include="*.py" 2>/dev/null | \
              grep -v "$file" | \
              grep -v "test_" | \
              grep -v "__pycache__" | \
              wc -l | tr -d ' ')

    if [ "$imports" -eq 0 ]; then
        # Check if exported via __init__.py
        init_file="$dir/__init__.py"
        init_export=0
        if [ -f "$init_file" ]; then
            init_export=$(grep -c "\b$module\b" "$init_file" 2>/dev/null || echo "0")
        fi

        if [ "$init_export" -eq 0 ]; then
            echo -e "${YELLOW}⚠️  ORPHANED:${NC} $file"
            echo "   No production imports found"
            orphaned=$((orphaned + 1))
        fi
    fi
done

echo ""
echo "=== Results ==="
echo "Modules checked: $checked"

if [ $orphaned -gt 0 ]; then
    echo -e "${RED}❌ ERROR: $orphaned orphaned module(s) found${NC}"
    echo ""
    echo "These files exist but are never imported in production code."
    echo "Either wire them up or remove them."
    exit 1
fi

echo -e "${GREEN}✅ All modules are integrated${NC}"
exit 0
```

### Method 3: Integration Test (LangGraph-Specific)

**Test: `tests/integration/test_graph_completeness.py`**

```python
"""Verify all expected nodes are in the compiled graph."""

import pytest
from langgraph.checkpoint.memory import MemorySaver

from myapp.graph.builder import create_coordination_graph


# List ALL nodes that should be in the graph
EXPECTED_NODES: list[str] = [
    "query_claude",
    "analyze_task",
    "architecture_review",  # Add new nodes here
    # ... other nodes
]


@pytest.mark.asyncio
async def test_all_expected_nodes_in_graph() -> None:
    """Verify all expected nodes are wired into the graph."""
    graph = await create_coordination_graph(MemorySaver())
    actual_nodes = list(graph.get_graph().nodes.keys())

    # Filter internal nodes
    actual_nodes = [n for n in actual_nodes if not n.startswith("__")]

    missing = [n for n in EXPECTED_NODES if n not in actual_nodes]

    assert not missing, (
        f"Nodes in EXPECTED_NODES but not in graph: {missing}. "
        f"Either wire these nodes into builder.py or remove from EXPECTED_NODES."
    )
```

## Step-by-Step Detection Process

### Step 1: Identify Candidates

List all Python files that could be orphaned:

```bash
# Find all .py files (excluding tests and special files)
find src/ -name "*.py" -type f | \
  grep -v __pycache__ | \
  grep -v test_ | \
  grep -v __init__.py | \
  sort
```

**Output:** List of candidate files to check

### Step 2: Check Each Candidate

For each file from Step 1:

```bash
# Extract module name
MODULE=$(basename "$file" .py)

# Check for imports
echo "Checking: $MODULE"
grep -r "from.*$MODULE import\|import.*$MODULE" src/ --include="*.py" | grep -v test

# If empty → ORPHANED
# If has lines → Check if they're from production code
```

### Step 3: Categorize Results

**Category A: Clearly Integrated**
- Multiple imports from production code
- Functions called in multiple places
- Part of critical paths

**Category B: Suspicious (Needs Review)**
- Only one import (fragile)
- Imported but functions never called
- Only imported in edge cases

**Category C: Orphaned**
- No imports at all
- Only imported in tests
- Imported but conditional never triggers

### Step 4: Generate Report

```bash
# Example report
echo "=== Orphan Detection Report ==="
echo ""
echo "ORPHANED (Category C):"
echo "  - src/features/architecture_nodes.py (CRITICAL)"
echo "  - src/utils/old_helper.py"
echo ""
echo "SUSPICIOUS (Category B):"
echo "  - src/features/experimental.py (only 1 import, in disabled code)"
echo ""
echo "INTEGRATED (Category A):"
echo "  - src/core/main.py"
echo "  - src/services/coordinator.py"
```

### Step 5: Take Action

**For Category C (Orphaned):**
1. If needed: Wire into system (import + call)
2. If not needed: Remove file
3. Update tests if removed

**For Category B (Suspicious):**
1. Review import locations
2. Check if code is actually used
3. Consider making integration more robust

**For Category A (Integrated):**
1. No action needed
2. Consider adding to integration test

## Automated Detection Scripts

### Script 1: verify_integration.sh (Complete)

**Location:** `scripts/verify_integration.sh`

**Usage:**
```bash
# Check entire project
./scripts/verify_integration.sh

# Expected output:
# === Orphan Detection ===
# ⚠️  ORPHANED: src/features/architecture_nodes.py
#    No production imports found
#
# === Results ===
# Modules checked: 45
# ❌ ERROR: 1 orphaned module(s) found
```

**Exit codes:**
- `0` - All modules integrated
- `1` - Orphaned modules found

**See:** Full script in Method 2 above

### Script 2: check_imports.sh (Focused)

**Location:** `scripts/check_imports.sh`

**Usage:**
```bash
# Check specific module
./scripts/check_imports.sh architecture_nodes

# Expected output:
# Checking module: architecture_nodes
# Production imports: 0
# Test imports: 2
# Status: ❌ ORPHANED (only test imports)
```

**Script:**
```bash
#!/bin/bash
# Check if a specific module is imported in production code

MODULE=$1

if [ -z "$MODULE" ]; then
  echo "Usage: $0 <module_name>"
  exit 1
fi

echo "Checking module: $MODULE"

# Count production imports
PROD=$(grep -r "from.*$MODULE import\|import.*$MODULE" src/ --include="*.py" | \
       grep -v test | wc -l | tr -d ' ')

# Count test imports
TEST=$(grep -r "from.*$MODULE import\|import.*$MODULE" tests/ --include="*.py" | \
       wc -l | tr -d ' ')

echo "Production imports: $PROD"
echo "Test imports: $TEST"

if [ "$PROD" -eq 0 ]; then
  if [ "$TEST" -gt 0 ]; then
    echo "Status: ❌ ORPHANED (only test imports)"
  else
    echo "Status: ❌ ORPHANED (no imports at all)"
  fi
  exit 1
else
  echo "Status: ✅ INTEGRATED"
  exit 0
fi
```

### Script 3: check_callsites.sh (Function-Level)

**Location:** `scripts/check_callsites.sh`

**Usage:**
```bash
# Check if function is called
./scripts/check_callsites.sh create_architecture_review_node

# Expected output:
# Checking function: create_architecture_review_node
# Definitions: 1
# Call-sites: 0
# Status: ❌ ORPHANED (defined but never called)
```

**Script:**
```bash
#!/bin/bash
# Check if a function is called in production code

FUNCTION=$1

if [ -z "$FUNCTION" ]; then
  echo "Usage: $0 <function_name>"
  exit 1
fi

echo "Checking function: $FUNCTION"

# Count definitions
DEFS=$(grep -r "def $FUNCTION" src/ --include="*.py" | wc -l | tr -d ' ')

# Count call-sites (excluding definitions and tests)
CALLS=$(grep -r "$FUNCTION" src/ --include="*.py" | \
        grep -v "def $FUNCTION" | \
        grep -v test | \
        wc -l | tr -d ' ')

echo "Definitions: $DEFS"
echo "Call-sites: $CALLS"

if [ "$CALLS" -eq 0 ]; then
  echo "Status: ❌ ORPHANED (defined but never called)"
  exit 1
else
  echo "Status: ✅ CALLED ($CALLS call-sites)"
  exit 0
fi
```

## Integration with Quality Gates

### Add to Pre-Commit Quality Gates

**In `quality-run-quality-gates` skill:**

```markdown
### Gate 6: Integration Verification (MANDATORY for new modules)

When the change involves new files or modules:

```bash
# Detect orphaned modules
./scripts/verify_integration.sh

# For LangGraph changes
uv run pytest tests/integration/test_graph_completeness.py -v
```

**Mandatory when:**
- Creating new `.py` files
- Adding new features
- Modifying integration points (builder.py, main.py, etc.)

**Failure means:** Code exists but won't execute at runtime.
```

### Add to ADR Completion Checklist

**In `create-adr-spike` skill:**

```markdown
### Phase 6: Integration Verification

Before moving ADR to completed:

- [ ] Run: `./scripts/verify_integration.sh` (passes)
- [ ] No orphaned modules detected
- [ ] All new modules imported in production code
- [ ] All new functions have call-sites
```

### Add to CI/CD Pipeline

**In `.github/workflows/quality.yml` (or equivalent):**

```yaml
- name: Detect Orphaned Code
  run: |
    ./scripts/verify_integration.sh
```

**Effect:** Prevents merging PRs with orphaned code

## Supporting Files

### References
- `references/orphan-detection-theory.md` - Why orphaned code occurs
- `references/adr-013-orphan-analysis.md` - Case study of ADR-013 orphaned code
- `references/vulture-vs-integration-check.md` - Why vulture isn't enough

### Examples
- `examples/orphan-module-detection.md` - Step-by-step module detection
- `examples/orphan-function-detection.md` - Step-by-step function detection
- `examples/fixing-orphaned-code.md` - How to fix orphaned code

### Scripts
- `scripts/verify_integration.sh` - Comprehensive orphan detection
- `scripts/check_imports.sh` - Module-specific import check
- `scripts/check_callsites.sh` - Function-specific call-site check

### Templates
- `templates/orphan-detection-report.md` - Report format for findings

## Expected Outcomes

### Successful Detection (No Orphans)

```bash
$ ./scripts/verify_integration.sh

=== Orphan Detection ===

Checking for orphaned modules in src/...

=== Results ===
Modules checked: 45
✅ All modules are integrated
```

### Failed Detection (Orphans Found)

```bash
$ ./scripts/verify_integration.sh

=== Orphan Detection ===

Checking for orphaned modules in src/...

⚠️  ORPHANED: src/temet_run/coordination/graph/architecture_nodes.py
   No production imports found

⚠️  ORPHANED: src/temet_run/coordination/graph/task_provider_nodes.py
   No production imports found

=== Results ===
Modules checked: 45
❌ ERROR: 2 orphaned module(s) found

These files exist but are never imported in production code.

To fix, either:
  1. Wire them up (add imports and call-sites)
  2. Remove them if no longer needed
  3. Export via __init__.py if they're part of the public API
```

### Integration Test Failure

```bash
$ uv run pytest tests/integration/test_graph_completeness.py -v

FAILED tests/integration/test_graph_completeness.py::test_all_expected_nodes_in_graph

AssertionError: Nodes in EXPECTED_NODES but not in graph: ['architecture_review', 'retrieve_tasks'].
Either wire these nodes into builder.py or remove from EXPECTED_NODES.
```

## Requirements

### Tools Required
- Read (to examine source files)
- Grep (to search for imports/calls)
- Bash (to run detection scripts)
- Glob (to find files)

### Environment Required
- Project structure with `src/` directory
- Standard Python project layout
- Ability to execute bash scripts

### Knowledge Required
- Understanding of Python import system
- Familiarity with project structure
- Knowledge of integration points (main.py, builder.py, etc.)

## Red Flags to Avoid

### Do Not
- ❌ Trust unit tests alone (they can import orphaned code)
- ❌ Assume code is integrated because it compiles
- ❌ Skip orphan detection for "small" changes
- ❌ Ignore orphan warnings as "false positives"
- ❌ Rely on vulture alone (can miss test-imported code)
- ❌ Mark features complete without running detection
- ❌ Move ADRs to completed without checking orphans

### Do
- ✅ Run orphan detection before marking work complete
- ✅ Add new modules to integration tests immediately
- ✅ Verify imports exist in production code (not just tests)
- ✅ Check both module-level and function-level orphans
- ✅ Fix orphans immediately (wire or remove)
- ✅ Add orphan detection to quality gates
- ✅ Update `EXPECTED_NODES` when adding nodes
- ✅ Treat orphan warnings as failures, not suggestions

## Notes

- This skill was created in response to ADR-013 (2025-12-07)
- ADR-013: 313 lines of orphaned code passed all quality gates
- Orphaned code can exist with 100% test coverage
- Unit tests can make orphaned code appear "alive" to dead code tools
- This skill complements vulture but checks integration explicitly
- Pair with `quality-verify-implementation-complete` for full coverage
- Integrate with `util-manage-todo` (Phase 2: Connection verification)

**Remember:** Code that exists but is never imported is technical debt. Detect and fix orphans before marking work complete.
