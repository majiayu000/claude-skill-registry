---
name: quality-analysis
description: Use when checking code quality, finding violations, detecting complexity issues, or running QC checks. Provides scripts for linting, naming enforcement, dead code detection, and legacy code discovery.
---

# Quality Analysis Tools

**When to use:** Before committing, when reviewing code, or when investigating quality issues.

---

## run_qc.py

**Purpose:** Run all automated QC checks and generate a report.

**Use when:**
- Before committing changes
- After significant refactoring
- Periodic quality audits

**Usage:**

```bash
python scripts/run_qc.py
```

**Runs:**
- ruff check (linting)
- mypy (type checking)
- Naming convention checks
- And more

**Output:** Report saved to `qc_reports/<timestamp>_qc_report.txt`

---

## detect_slop.py

**Purpose:** Find complexity hotspots, architecture violations, and refactor targets.

**Use when:**
- Evaluating a file's maintainability
- Finding where to focus refactoring
- Checking for AI-generated "slop" patterns

**Usage:**

```bash
# Scan entire codebase
python scripts/detect_slop.py

# Scan specific directory
python scripts/detect_slop.py nomarr/interfaces/

# Scan specific file
python scripts/detect_slop.py nomarr/services/domain/tagging_svc.py

# HTML report
python scripts/detect_slop.py --format html

# Markdown report
python scripts/detect_slop.py --format md
```

**Detects:**
- High cyclomatic complexity (radon)
- Architecture violations (import-linter)
- Code smells (flake8 plugins)
- Commented-out code
- Overcomplicated patterns

**Decision rule:** Use on **one file or package at a time**. Summarize findings, propose focused refactor, iterate.

---

## check_naming.py

**Purpose:** Enforce Nomarr's naming conventions across the codebase.

**Use when:**
- Reviewing new code for naming compliance
- Finding naming violations before commit
- Verifying refactored code follows conventions

**Usage:**

```bash
# Check all files
python scripts/check_naming.py

# JSON output
python scripts/check_naming.py --format=json
```

**Checks (based on `scripts/configs/naming_rules.yaml`):**
- Service method naming (`<verb>_<noun>`)
- Module naming conventions
- Forbidden patterns (`api_*`, `*_for_admin`)

---

## check_dead_nodes.py

**Purpose:** Find unreachable code (functions, classes, methods not called from entrypoints).

**Use when:**
- Cleaning up unused code
- After major refactoring
- Periodic maintenance

**Usage:**

```bash
# Summary and likely dead nodes
python scripts/check_dead_nodes.py

# Verbose - list all unreachable nodes
python scripts/check_dead_nodes.py --verbose
python scripts/check_dead_nodes.py -v

# JSON output
python scripts/check_dead_nodes.py --format=json
```

**Requires:** Run `build_code_graph.py` first to generate the graph.

**Output shows:**
- Nodes not reachable from interface entrypoints
- Analysis of whether they're truly dead (checks imports, type usage, grep hits)

---

## find_legacy.py

**Purpose:** Find references to "legacy" or "backwards compatibility" in the codebase.

**Why:** Nomarr is pre-alpha. There should be NO legacy code or compatibility layers.

**Use when:**
- Ensuring no one added migration/shim code
- Cleaning up TODO comments about removing old code
- Pre-release quality check

**Usage:**

```bash
python scripts/find_legacy.py

# JSON output
python scripts/find_legacy.py --format=json

# Search specific directories
python scripts/find_legacy.py nomarr/services tests/unit
```

**Detects patterns:**
- `legacy`
- `backwards compatibility`
- `deprecated`
- `TODO...remove`
- `FIXME...remove`

**Expected result:** Zero matches. Any match is a violation of pre-alpha policy.

---

## Workflow: Quality Check Before Commit

```bash
# 1. Run full QC
python scripts/run_qc.py

# 2. Check for legacy patterns (should be empty)
python scripts/find_legacy.py

# 3. Check naming violations
python scripts/check_naming.py

# 4. Spot-check modified files for complexity
python scripts/detect_slop.py nomarr/services/domain/tagging_svc.py
```

---

## Workflow: Refactoring Triage

```bash
# 1. Find complexity hotspots
python scripts/detect_slop.py nomarr/workflows/ --format html

# 2. Open report, identify worst files

# 3. For each hotspot, analyze in detail
python scripts/detect_slop.py nomarr/workflows/processing/process_file_wf.py

# 4. Propose and apply focused refactor

# 5. Re-run to verify improvement
python scripts/detect_slop.py nomarr/workflows/processing/process_file_wf.py
```

---

## Key Rules

- **Use `detect_slop.py` on one file/package at a time** — don't try to fix everything from one giant report
- **`find_legacy.py` should always return zero results** — pre-alpha means no legacy code
- **Run `check_naming.py` before committing** — naming violations are enforcement, not cosmetic
