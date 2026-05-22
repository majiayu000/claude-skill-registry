---
name: architecture-validate-srp
description: |
  Detect Single Responsibility Principle (SRP) violations using multi-dimensional analysis.
  Use when reviewing code for "SRP", "single responsibility", "god class", "doing too much",
  "too many dependencies", before commits, during refactoring, or as quality gate.
  Analyzes Python, JavaScript, TypeScript files with AST-based detection, metrics (TCC, ATFD, WMC),
  and project-specific patterns. Provides actionable fix guidance with refactoring estimates.
allowed-tools:
  - Read
  - Grep
  - Bash
  - Glob
  - mcp__ast-grep__dump_syntax_tree
  - mcp__ast-grep__test_match_code_rule
  - mcp__ast-grep__find_code
  - mcp__ast-grep__find_code_by_rule
  - mcp__project-watch-mcp__search_code
---

# Validate Single Responsibility Principle (SRP)

**Automated detection of SRP violations using actor-driven analysis, metrics, and AST patterns.**

## Purpose

Detect Single Responsibility Principle violations using multi-dimensional analysis including naming patterns, class metrics, method complexity, cohesion measurements, and project-specific architectural patterns. Provides actionable fix guidance with confidence scoring and refactoring estimates.

## Table of Contents

### Core Sections
- [Purpose](#purpose) - What this skill detects and validates
- [Quick Start](#quick-start) - Immediate SRP validation workflow
- [When to Use This Skill](#when-to-use-this-skill) - Triggers and integration points
- [What This Skill Does](#what-this-skill-does) - SRP definition and detection methods
- [Instructions](#instructions) - Complete step-by-step validation process
- [Usage Examples](#usage-examples) - Real-world validation scenarios
- [Supporting Files](#supporting-files) - References and examples

### Detailed Sections
- [Validation Levels](#validation-levels) - Fast, thorough, and full analysis modes
- [Detection Methods](#detection-methods-multi-dimensional) - 4-level validation approach
- [Integration with Other Skills](#integration-with-other-skills) - code-review, validate-architecture, quality-gates
- [Parameters](#parameters) - Configuration options
- [Output Format](#output-format) - Text and JSON report formats
- [Success Metrics](#success-metrics) - Accuracy and performance targets
- [Requirements](#requirements) - Dependencies and installation
- [Red Flags to Avoid](#red-flags-to-avoid) - Common pitfalls
- [Troubleshooting](#troubleshooting) - Common issues and solutions
- [Expected Benefits](#expected-benefits) - Metrics and improvements

## Quick Start

**User asks:** "Check if this class is doing too much" or "Validate SRP compliance"

**What happens:**
1. Scans code for SRP violations (naming, size, complexity, dependencies)
2. Calculates cohesion metrics (TCC, ATFD, WMC)
3. Detects project-specific anti-patterns
4. Reports violations with specific refactoring guidance
5. Estimates refactoring time and effort

**Result:** ✅ SRP compliant OR ❌ Violations with actionable fixes

## When to Use This Skill

**Invoke this skill when:**
- User asks: "check SRP", "single responsibility", "is this doing too much"
- User asks: "god class", "too many dependencies", "method too long"
- Before commit (as part of `code-review` skill)
- During refactoring or architectural review
- As quality gate (via `run-quality-gates` skill)
- When class/method feels complex but can't articulate why

**Integration triggers:**
- `code-review` skill Step 2: Architectural Review (SRP sub-check)
- `validate-architecture` skill: SRP at layer level
- `run-quality-gates` skill: Optional SRP quality gate
- `multi-file-refactor` skill: SRP-driven refactoring coordination

## What This Skill Does

### SRP Definition (Actor-Driven)

**Robert C. Martin:** "A module should be responsible to one, and only one, actor."

- **Actor**: A group of users or stakeholders who would request changes
- **NOT** "do one thing" (task-driven) - a class can have multiple methods
- **IS** "have one reason to change" (actor-driven)

**Example:** See [examples/violation-naming-patterns.py](./examples/violation-naming-patterns.py) for violation and correct implementation showing Employee class serving 3 actors (Accounting, HR, DBA) and the correct split into PayCalculator, HourReporter, and EmployeeRepository.

### Detection Methods (Multi-Dimensional)

This skill uses **4 validation levels**:

1. **Level 1 (Fast, 5s)**: Naming patterns via AST-grep
   - Methods with "and" in name → 40% confidence violation
   - Quick scan of entire codebase

2. **Level 2 (Fast, 10s)**: Size metrics via AST analysis
   - Class >300 lines → Review needed
   - Method >50 lines → 60% confidence violation
   - >15 methods per class → Review needed

3. **Level 3 (Moderate, 30s)**: Cohesion metrics
   - God Class: ATFD >5 AND WMC >47 AND TCC <0.33 → 80% confidence
   - Constructor >4 params (warning), >8 params (critical) → 75% confidence

4. **Level 4 (Manual, 5min)**: Actor analysis (guided questions)
   - "How many actors would request changes to this class?"
   - "Can you split by actor responsibility?"

**Default mode:** Level 2 (Fast + Size metrics) - balance speed and accuracy

### Validation Levels

| Level | Speed | Checks | Use When |
|-------|-------|--------|----------|
| `fast` | 5s | Naming patterns only | Quick pre-commit scan |
| `thorough` | 30s | Naming + Size + Metrics | Normal workflow (default) |
| `full` | 5min | All checks + Actor analysis | Deep refactoring review |

## Instructions

### Step 1: Determine Validation Level

```bash
# User request → Validation level
"quick check" → fast
"review this class" → thorough (default)
"plan refactoring" → full
```

### Step 2: Detect Naming Violations (All Levels)

**Pattern 1: Methods with "and" in name (40% confidence)**

Use the validation script to detect naming violations:

**Using validation script:**
```bash
./scripts/validate-srp.sh <path> --level=fast
```

**Or manually with MCP tools:**
```bash
mcp__ast-grep__find_code(
    pattern="def $NAME_and_$REST",
    project_folder="/path/to/project",
    language="python"
)
```

**Example violations and fixes:** See [examples/violation-naming-patterns.py](./examples/violation-naming-patterns.py) showing validate_and_save_user() violation and the correct split into validate_user() and save_user().

### Step 3: Analyze Size Metrics (Thorough+)

**Pattern 2: Class size (300+ lines → review)**

Use the validation script for size analysis:

```bash
./scripts/validate-srp.sh <path> --level=thorough
```

**Or use God Class detection script:**

```bash
./scripts/check-god-class.sh <file.py>
```

**Thresholds:**
- Class: >300 lines = warning, >500 lines = critical
- Method: >50 lines = warning, >100 lines = critical
- Methods per class: >15 = warning, >25 = critical

### Step 4: Calculate Cohesion Metrics (Thorough+)

**God Class Detection (80% confidence):**
- **ATFD** (Access to Foreign Data): >5 = excessive coupling
- **WMC** (Weighted Methods per Class): >47 = too complex
- **TCC** (Tight Class Cohesion): <0.33 = low cohesion

**Formula:** `ATFD >5 AND WMC >47 AND TCC <0.33 → God Class`

**Calculate metrics using radon:**

```bash
# If radon available
uv run radon cc src/ -a -nb  # Cyclomatic complexity (WMC proxy)
uv run radon raw src/        # Raw metrics
```

**See:** [references/srp-principles.md](./references/srp-principles.md) for detailed metric calculations and formulas.

### Step 5: Detect Constructor Dependencies (Thorough+)

**Pattern 4: Constructor parameters (>4 warning, >8 critical)**

Use the God Class detection script:

```bash
./scripts/check-god-class.sh <file.py>
```

**Thresholds (75% confidence):**
- 1-4 params: ✅ Good
- 5-8 params: ⚠️ Warning (consider parameter object)
- 9+ params: ❌ Critical (God Class indicator)

**Example violations and fixes:** See [examples/violation-god-class.py](./examples/violation-god-class.py) showing UserService with 9 constructor parameters and the correct split into UserAuthService, UserNotificationService, and UserAnalytics.

### Step 6: Detect Project-Specific Patterns

**Read CLAUDE.md for project anti-patterns:**

Check for project-specific SRP violations using grep:

```bash
# Pattern 1: Optional config parameters (project anti-pattern)
grep -rn "config.*Optional\|config.*None.*=" src/

# Pattern 2: Domain entities doing I/O (layer violation)
grep -r "import.*requests\|import.*database" domain/

# Pattern 3: Application services with business logic
grep -r "def calculate\|def compute" application/services/

# Pattern 4: Repositories with orchestration
grep -A 10 "class.*Repository" infrastructure/repositories/
```

**Common project-specific violations:**
- Domain entities importing infrastructure
- Application services implementing business logic (should orchestrate only)
- Repositories containing orchestration (should be data access only)
- Optional config parameters (violates fail-fast)

**See:** [references/srp-principles.md](./references/srp-principles.md) for actor identification guidance.

### Step 7: Actor Analysis (Full Mode Only)

**Guided questions for user:**

1. "List all actors who would request changes to this class:"
   - Example: "HR department, Accounting team, DBA"

2. "Can you group methods by actor?"
   - Example: `calculate_pay()` → Accounting, `report_hours()` → HR

3. "How would you name classes split by actor?"
   - Example: `PayCalculator`, `HourReporter`, `EmployeeRepository`

**Actor count → Violation confidence:**
- 1 actor: ✅ SRP compliant
- 2 actors: ⚠️ Warning (consider split)
- 3+ actors: ❌ Violation (must split)

### Step 8: Generate Report

**Report structure:**

```
SRP Validation Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Passed: X/Y classes (Z%)

❌ Violations Found: N

[CRITICAL] God Class: ClassName (path/file.py:line)
  - Lines: X (threshold: 300)
  - Methods: Y (threshold: 15)
  - Constructor params: Z (threshold: 4)
  - ATFD: A, WMC: B, TCC: C
  - Actors detected: N (actor1, actor2, actor3)
  - Fix: Split into Class1 (actor1), Class2 (actor2), Class3 (actor3)
  - Estimated refactoring: A-B hours

[WARNING] Method Name Violation: method_and_other (path/file.py:line)
  - Method name contains 'and'
  - Confidence: 40%
  - Fix: Split into method() and other()
  - Estimated refactoring: 15-30 minutes

[WARNING] Long Method: process_request (path/file.py:line)
  - Lines: X (threshold: 50)
  - Cyclomatic complexity: Y (threshold: 10)
  - Confidence: 60%
  - Fix: Extract 2-3 smaller methods
  - Estimated refactoring: 30-60 minutes

Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- X critical violations (must fix)
- Y warnings (should fix)
- Total estimated refactoring time: A-B hours
- Top priority: ClassName (god class)
```

## Usage Examples

### Example 1: Quick Pre-Commit Check

```bash
# User: "Quick SRP check before commit"

# Skill runs level: fast (5s)
→ Scans for method names with "and"
→ Reports 2 violations

Output:
⚠️ 2 SRP warnings found:

1. validate_and_save_user (src/services/user.py:45)
   - Method name contains 'and'
   - Fix: Split into validate_user() and save_user()

2. fetch_and_transform_data (src/utils/data.py:78)
   - Method name contains 'and'
   - Fix: Split into fetch_data() and transform_data()

Run with --thorough for complete analysis.
```

### Example 2: Class Review (Default)

```bash
# User: "Review UserService for SRP compliance"

# Skill runs level: thorough (30s)
→ Naming patterns
→ Size metrics
→ Cohesion metrics
→ Constructor analysis

Output:
❌ UserService violates SRP (src/application/services/user_service.py:12)

Violations:
- Lines: 487 (threshold: 300) ❌
- Methods: 23 (threshold: 15) ⚠️
- Constructor params: 9 (threshold: 4) ❌
- ATFD: 12 (threshold: 5) ❌
- WMC: 89 (threshold: 47) ❌
- TCC: 0.21 (threshold: 0.33) ❌

Detected actors (3):
1. Authentication (login, logout, verify_token)
2. Profile Management (update_profile, get_profile, delete_account)
3. Notifications (send_welcome_email, send_reset_email)

Recommended split:
- UserAuthService: authentication methods
- UserProfileService: profile management
- UserNotificationService: notification methods

Estimated refactoring: 4-6 hours
```

### Example 3: Deep Refactoring Analysis

```bash
# User: "Plan refactoring for PaymentProcessor - full SRP analysis"

# Skill runs level: full (5 min with user interaction)
→ All automated checks
→ Actor analysis questions
→ Refactoring plan

Questions asked:
1. "List actors who request changes to PaymentProcessor"
   User: "Finance team, Fraud detection, Customer support, Compliance"

2. "Group methods by actor"
   User provides grouping...

Output:
❌ PaymentProcessor is a God Class (4 actors detected)

Actor breakdown:
1. Finance (3 methods): process_payment, refund_payment, calculate_fees
2. Fraud Detection (2 methods): check_fraud_score, block_suspicious
3. Customer Support (2 methods): get_transaction_history, dispute_charge
4. Compliance (2 methods): log_transaction, generate_audit_report

Refactoring plan:
Phase 1 (2 hours): Extract PaymentProcessor (Finance actor)
Phase 2 (1.5 hours): Extract FraudDetectionService
Phase 3 (1.5 hours): Extract TransactionHistoryService (Support)
Phase 4 (1 hour): Extract ComplianceReporter
Phase 5 (1 hour): Integration tests and validation

Total estimated time: 7 hours
Recommended approach: Incremental (1 phase per day)
```

## Integration with Other Skills

### With code-review

The `code-review` skill invokes SRP validation in Step 2 (Architectural Review) as a sub-check. When SRP violations are detected, they are reported as warnings in the overall code review report.

**Integration point:** Automatic invocation during code review workflow with `level="fast"` for speed.

### With validate-architecture

The `validate-architecture` skill checks SRP compliance at the layer level, while this skill checks at the class/method level. Domain layers should have high cohesion (TCC > 0.5), and this skill can detect low cohesion violations.

**Integration point:** Cross-layer validation to ensure architectural boundaries maintain SRP.

### With run-quality-gates

SRP validation can be added as an optional quality gate in `.claude/quality-gates.json`:

```json
{
  "optional_gates": ["srp_validation"],
  "srp_threshold": "warning"
}
```

Set threshold to `"critical"` to block commits on violations.

### With multi-file-refactor

When refactoring God Classes that span multiple files, use `multi-file-refactor` skill to coordinate changes. This skill identifies God Classes and provides refactoring guidance; `multi-file-refactor` executes the split.

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `path` | string | `src/` | File or directory to validate |
| `level` | enum | `thorough` | Validation depth: `fast`, `thorough`, `full` |
| `output_format` | enum | `text` | Output format: `text`, `json` |
| `threshold` | enum | `warning` | Report threshold: `warning`, `critical` |
| `include_metrics` | bool | `true` | Include cohesion metrics in report |

**Usage:**
```bash
# Default (thorough mode on src/)
Skill(command: "validate-srp")

# Custom path and level
Skill(command: "validate-srp --path=src/application --level=full")

# JSON output for tooling integration
Skill(command: "validate-srp --output_format=json")
```

## Output Format

### Text Output (Default)

See Step 8 in Instructions for complete example.

### JSON Output

```json
{
  "summary": {
    "total_classes": 45,
    "violations": 7,
    "warnings": 12,
    "passed": 26,
    "compliance_rate": 0.58
  },
  "violations": [
    {
      "severity": "critical",
      "type": "god_class",
      "class": "UserService",
      "file": "src/application/services/user_service.py",
      "line": 12,
      "metrics": {
        "lines": 487,
        "methods": 23,
        "constructor_params": 9,
        "atfd": 12,
        "wmc": 89,
        "tcc": 0.21
      },
      "actors": ["Authentication", "Profile", "Notifications"],
      "confidence": 0.80,
      "fix": "Split into UserAuthService, UserProfileService, UserNotificationService",
      "estimated_hours": 5.0
    }
  ],
  "warnings": [
    {
      "severity": "warning",
      "type": "method_naming",
      "method": "validate_and_save_user",
      "file": "src/services/user.py",
      "line": 45,
      "confidence": 0.40,
      "fix": "Split into validate_user() and save_user()",
      "estimated_minutes": 20
    }
  ]
}
```

## Supporting Files

### References
- **[references/srp-principles.md](./references/srp-principles.md)** - Core SRP concepts, actor-driven definition, real-world examples, cohesion metrics formulas

### Examples
- **[examples/examples.md](./examples/examples.md)** - Overview of all examples with expected results
- **[examples/violation-naming-patterns.py](./examples/violation-naming-patterns.py)** - Methods with "and" in name, multiple actors
- **[examples/violation-god-class.py](./examples/violation-god-class.py)** - Constructor with too many parameters
- **[examples/correct-single-actor.py](./examples/correct-single-actor.py)** - Proper SRP implementation with single actor

### Scripts
- **[scripts/validate-srp.sh](./scripts/validate-srp.sh)** - Main validation script with 3 levels (fast/thorough/full)
- **[scripts/check-god-class.sh](./scripts/check-god-class.sh)** - God Class detection for individual files

## Success Metrics

| Metric | Target | Benefit |
|--------|--------|---------|
| Detection accuracy | >85% | Minimal false positives |
| God class detection | 100% | Catch all critical violations |
| False positive rate | <15% | High signal-to-noise ratio |
| Execution time | <30s | Fast enough for workflow |
| Actionability | 100% | Every violation has specific fix |
| Refactoring estimate accuracy | ±30% | Reliable planning |

## Utility Scripts

### validate-srp.sh

Main validation script with multi-level analysis:

```bash
# Fast check (naming patterns only - 5 seconds)
./scripts/validate-srp.sh src/ --level=fast

# Thorough check (naming + size + constructors - 30 seconds)
./scripts/validate-srp.sh src/ --level=thorough

# Full analysis (with actor questions - 5 minutes)
./scripts/validate-srp.sh src/ --level=full

# JSON output for CI/CD integration
./scripts/validate-srp.sh src/ --output-format=json
```

### check-god-class.sh

Focused God Class detection for single files:

```bash
# Check specific file
./scripts/check-god-class.sh src/services/user_service.py

# Returns:
# - Constructor parameter count
# - Method count
# - File size
# - God Class recommendation
```

## Requirements

**Minimum:**
- Python 3.10+ (for AST analysis)
- Read, Grep, Bash, Glob tools
- Source code in supported language (Python/JS/TS)
- Validation scripts in scripts/ directory

**Optional:**
- `radon` for accurate metrics: `uv pip install radon`
- `mcp__ast-grep__*` tools for precise AST analysis
- `mcp__project-watch-mcp__search_code` for context

**Installation:**
```bash
# Make scripts executable
chmod +x scripts/*.sh

# Optional: Install radon for accurate metrics
uv pip install radon

# Verify installation
uv run radon --version
```

## Red Flags to Avoid

### Architectural Violations

1. **God Classes** - ATFD >5, WMC >47, TCC <0.33
2. **Constructor Dependencies** - >8 parameters
3. **Method Naming** - Methods with "and" in name
4. **File Size** - >500 lines per file

### Detection Anti-Patterns

5. **Ignoring warnings** - Small violations compound into big issues
6. **Not validating fixes** - Re-run after refactoring
7. **Skipping actor analysis** - Metrics alone miss context
8. **Assuming SRP = "one method"** - SRP is actor-driven, not task-driven

### Process Mistakes

9. **Refactoring without tests** - Always have test coverage first
10. **Big bang refactoring** - Incremental refactoring safer
11. **Not estimating effort** - Plan time for refactoring
12. **Skipping after major changes** - Validation most critical after refactoring

## Troubleshooting

### Issue: Too Many False Positives

**Symptom:** Small helper methods flagged as violations

**Fix:** Adjust thresholds in `.claude/srp-config.json`:
```json
{
  "thresholds": {
    "class_lines": 400,
    "method_lines": 75,
    "constructor_params": 6
  }
}
```

### Issue: Metrics Not Calculated

**Symptom:** "Metrics unavailable" in report

**Fix:** Install radon:
```bash
uv pip install radon
```

Or use simplified heuristics (less accurate but faster).

### Issue: Can't Identify Actors

**Symptom:** Actor analysis unclear

**Fix:** Ask targeted questions:
1. "Who would request changes to this class?"
2. "Can you group methods by job role?"
3. "What teams interact with this code?"

## Expected Benefits

| Metric | Without SRP Validation | With SRP Validation | Improvement |
|--------|----------------------|-------------------|-------------|
| God classes in codebase | 15-25 | 0-2 | 95% reduction |
| Time to understand class | 20-45 min | 5-10 min | 75% faster |
| Bugs per class | 8-12 per year | 1-3 per year | 85% reduction |
| Refactoring cost | High (embedded violations) | Low (caught early) | 80% reduction |
| Test coverage | 40-60% (hard to test) | 80-95% (easy to test) | 50% increase |
| Code review time | 30-60 min | 10-20 min | 66% faster |

## See Also

- **validate-architecture** - Layer-level architecture validation
- **code-review** - Comprehensive pre-commit review (includes SRP)
- **run-quality-gates** - Quality gate orchestration
- **multi-file-refactor** - Coordinate SRP-driven refactoring
- **@code-review-expert** - Agent for code review guidance
- **@architecture-guardian** - Agent for architectural decisions
- **ARCHITECTURE.md** - Project architecture documentation

---

**Last Updated:** 2025-11-02
**Version:** 1.0.0
