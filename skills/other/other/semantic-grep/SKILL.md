---
name: semantic-grep
description: Run Semgrep static analysis scans with parallel execution and structured triage.
Use when: (1) scanning a codebase for security vulnerabilities, (2) running a
first-pass static analysis audit, (3) finding known bug patterns before code review.
Enforces scan-plan approval gate, scanner/triager split, and triage-required reporting.

category: audit
---

# Semgrep Security Scan

Run a Semgrep scan with automatic language detection, parallel execution, and structured triage. Uses Semgrep Pro for cross-file taint analysis when available.

## Prerequisites

Semgrep CLI must be installed:

```bash
semgrep --version
```

Optional — Semgrep Pro for cross-file analysis:

```bash
semgrep install-semgrep-pro
```

## When to Use

- Security audit of a codebase
- Finding vulnerabilities before code review
- Scanning for known bug patterns
- First-pass static analysis

## When NOT to Use

- Binary analysis
- Already have Semgrep CI configured in pipeline
- Creating custom Semgrep rules (separate concern)

## Workflow

### Step 1: Detect Languages and Pro Availability

```bash
# Check Pro availability
semgrep --pro --validate --config p/default 2>/dev/null && echo "Pro available" || echo "OSS only"

# Detect languages by file extension
find . -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.go" -o -name "*.rb" -o -name "*.java" -o -name "*.rs" -o -name "*.c" -o -name "*.cpp" \) | sed 's/.*\.//' | sort | uniq -c | sort -rn
```

Map findings to language categories (Python, JavaScript/TypeScript, Go, Ruby, Java, Rust, C/C++, Docker, Terraform).

### Step 2: Select Rulesets

Select rulesets based on detected languages:

- **Baseline** (always): `p/security-audit`, `p/secrets`
- **Per-language**: `p/python`, `p/javascript`, `p/go`, etc.
- **Framework-specific**: `p/django`, `p/react`, `p/nodejs`, etc.
- **Infrastructure**: `p/dockerfile`, `p/terraform`
- **Third-party** (required when language matches): Trail of Bits rules (`https://github.com/trailofbits/semgrep-rules`)

### Step 3: Present Plan and Get Approval

**This is a hard gate. Do not proceed without explicit user approval.**

Present the scan plan showing:

1. Target directory
2. Engine type (Pro/OSS)
3. Detected languages with file counts
4. All rulesets explicitly listed
5. Execution strategy (parallel scans per language)

Wait for the user to say "yes", "proceed", "approved", or equivalent. The original scan request is NOT approval of the plan.

### Step 4: Execute Parallel Scans

Create output directory:

```bash
mkdir -p semgrep-results-001
```

Spawn parallel scan tasks — one per language category. Each task runs all approved rulesets for that language simultaneously:

```bash
semgrep [--pro if available] \
  --metrics=off \
  --config [RULESET] \
  --json -o [OUTPUT_DIR]/[lang]-[ruleset].json \
  --sarif-output=[OUTPUT_DIR]/[lang]-[ruleset].sarif \
  [TARGET] &
```

Wait for all scans to complete. See [scanner-task-prompt.md](references/scanner-task-prompt.md) for the full scanner task template.

### Step 5: Triage Findings

Spawn parallel triage tasks — one per language category. Each task reads scan JSON results and source code context to classify findings as TRUE_POSITIVE or FALSE_POSITIVE.

See [triage-task-prompt.md](references/triage-task-prompt.md) for the full triage task template and decision tree.

### Step 6: Report Results

Collect results from all triage tasks and report:

- Total files scanned
- Rulesets used
- Raw findings count
- True positives after triage
- Breakdown by severity and category

## Common Mistakes

| Mistake | Correct Approach |
|---------|------------------|
| Running without `--metrics=off` | Always disable telemetry |
| Running rulesets sequentially | Run in parallel with `&` and `wait` |
| Reporting raw findings without triage | Always triage to remove false positives |
| Treating scan request as plan approval | Present plan, wait for explicit approval |
| Skipping third-party rulesets | Trail of Bits rules are required when language matches |
| Using OSS when Pro is available | Always check and prefer Pro for cross-file analysis |

## Limitations

1. OSS mode cannot track data flow across files
2. Pro cross-file analysis uses `-j 1` (single job) per ruleset
3. Triage requires reading code context — parallelized via tasks
4. Some false positive patterns require human judgment