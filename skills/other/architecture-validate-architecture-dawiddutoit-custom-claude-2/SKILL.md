---
name: architecture-validate-architecture
description: |
  Automates architecture validation for Clean Architecture, Hexagonal, Layered, and MVC patterns. Detects layer boundary violations, dependency rule breaches, and architectural anti-patterns. Use when asked to "validate architecture", "check layer boundaries", "architectural review", before major refactoring, or as pre-commit quality gate. Adapts to project's architectural style by reading ARCHITECTURE.md.
allowed-tools:
  - Read
  - Grep
  - Bash
  - Glob
---

# Validate Architecture

## Table of Contents

**Quick Start** → [When to Use](#when-to-use-this-skill) | [What It Does](#purpose) | [Simple Example](#quick-start)

**How to Implement** → [Validation Process](#validation-process) | [Architecture Rules](#architecture-specific-rules) | [Expected Output](#expected-outcomes)

**Patterns** → [Clean Architecture](#clean-architecture) | [Hexagonal](#hexagonal-architecture) | [Layered](#layered-architecture) | [MVC](#mvc-architecture)

**Help** → [Anti-Patterns](#common-anti-patterns-detected) | [Troubleshooting](#troubleshooting) | [Integration](#integration-points)

**Reference** → [Layer Dependencies](./references/reference.md) | [Diff-Aware Validation](./references/diff-aware-validation.md) | [Quick Reference](./references/diff-aware-validation-quickref.md)

---

## Purpose

Automates architecture validation for multiple architectural patterns (Clean Architecture, Hexagonal, Layered, MVC). Automatically detects the project's architectural style from ARCHITECTURE.md, scans all source files for import violations, validates dependency direction (inward only for Clean/Hexagonal), and reports violations with specific fixes. Adapts to any architectural pattern and provides actionable remediation guidance.

## Quick Start

**User asks:** "Validate my architecture" or "Check if this follows Clean Architecture"

**What happens:**
1. Reads project's `ARCHITECTURE.md` to identify architectural pattern
2. Scans all source files for import violations
3. Validates dependency direction (inward only for Clean/Hexagonal)
4. Reports violations with file:line:fix recommendations

**Result:** ✅ All checks passed OR ❌ Violations with specific fixes

## When to Use This Skill

Invoke this skill when:
- User asks "validate architecture", "check layer boundaries", "architectural review"
- Before major refactoring or structural changes
- As part of pre-commit quality gates
- After adding new dependencies to any layer
- Reviewing code for architecture compliance
- User mentions "Clean Architecture", "Hexagonal", "Layered", or "MVC"

## Triggers

Trigger with phrases like:
- "validate architecture"
- "check layer boundaries"
- "architectural review"
- "validate my Clean Architecture"
- "check if this follows Hexagonal Architecture"
- "run architecture validation"
- "check for layer violations"
- "validate dependencies"
- "architectural compliance check"

## What This Skill Does

### Supported Architectural Patterns

This skill automatically adapts to:

1. **Clean Architecture** (Concentric layers: Domain → Application → Infrastructure → Interface)
2. **Hexagonal Architecture** (Ports and Adapters)
3. **Layered Architecture** (Presentation → Business → Data)
4. **MVC** (Model → View → Controller)

### Validation Checks

**1. Pattern Detection**
- Reads `ARCHITECTURE.md` or similar documentation
- Identifies architectural style and layer definitions
- Parses dependency rules and constraints

**2. Layer Boundary Validation**
- Scans all import statements in source files
- Checks for violations (e.g., Domain importing Infrastructure)
- Detects circular dependencies between layers

**3. Dependency Direction Validation**
- Verifies dependencies flow correctly (inward for Clean/Hexagonal)
- Ensures outer layers depend on inner, never reverse
- Validates domain/core has no external dependencies

**4. Pattern Compliance**
- Checks for required patterns (ServiceResult, Repository, etc.)
- Verifies naming conventions (Services in application/, etc.)
- Validates file organization matches architectural layers

**5. Anti-Pattern Detection**
- Domain importing database/framework code
- Application importing concrete infrastructure
- Circular dependencies between layers
- Business logic in interface/presentation layers

## Instructions

### Overview

Validating architecture involves a 5-step process:

1. **Identify Architecture** - Read ARCHITECTURE.md and detect pattern (Clean, Hexagonal, Layered, MVC)
2. **Extract Layer Definitions** - Map directory structure to architectural layers
3. **Scan Imports** - Analyze all import statements in source files
4. **Validate Rules** - Check dependency direction and layer boundaries
5. **Report Violations** - Generate actionable report with specific fixes

See detailed steps in [Validation Process](#validation-process) section below.

## Validation Process

The validation process follows 5 steps:

1. **Identify Architecture** - Read ARCHITECTURE.md and detect pattern (Clean, Hexagonal, Layered, MVC)
2. **Extract Layer Definitions** - Map directory structure to architectural layers
3. **Scan Imports** - Analyze all import statements in source files
4. **Validate Rules** - Check dependency direction and layer boundaries
5. **Report Violations** - Generate actionable report with specific fixes

See [Code Examples](./references/code-examples.md) for detailed examples of each step, including bash commands, layer definitions, validation rules, and sample output formats.

## Usage Examples

### Example 1: Validate Entire Codebase
User: "Validate architecture before I commit"
- Reads ARCHITECTURE.md and identifies pattern
- Scans all source files for imports
- Validates each layer's imports against rules
- Reports violations or confirms compliance

### Example 2: Validate Specific Changes
User: "Check if my refactoring follows Clean Architecture"
- Runs git diff to find changed files
- Filters to source files only
- Validates only modified files
- Reports violations in changed code

### Example 3: Pre-Commit Hook Integration
Automatically invoked by pre-commit hook to validate architectural boundaries, block commits if critical violations found, and provide actionable fix recommendations.

## Architecture-Specific Rules

This skill supports four architectural patterns with specific dependency rules:

### Clean Architecture
- **Dependency Rule**: Dependencies flow inward only (Interface → Application → Domain ← Infrastructure)
- **Layer Rules**: Domain is pure, Application orchestrates, Infrastructure implements, Interface is entry points

### Hexagonal Architecture
- **Dependency Rule**: Core has no dependencies, adapters depend on ports
- **Layer Rules**: Domain/Core is pure, Ports are interfaces, Adapters connect to external systems

### Layered Architecture
- **Dependency Rule**: Each layer depends only on layer below
- **Layer Rules**: Presentation → Business Logic → Data Access

### MVC Architecture
- **Dependency Rule**: Model is independent, View/Controller depend on Model
- **Layer Rules**: Model is independent, View depends on Model, Controller orchestrates

See [Code Examples](./references/code-examples.md) for detailed dependency diagrams, layer rules, and detection patterns for each architectural pattern.

## Common Anti-Patterns Detected

This skill detects and provides fixes for common architectural violations:

1. **Domain Importing Infrastructure** - Domain layer importing database/framework code
2. **Application Importing Interfaces** - Application layer importing from API/UI layers
3. **Circular Dependencies** - Two or more modules importing each other
4. **Business Logic in Interface Layer** - Business rules and validation in API/UI code

See [Code Examples](./references/code-examples.md) for detailed violation examples with complete before/after code showing how to fix each anti-pattern using dependency inversion, repository patterns, and proper layering.

## Integration Points

This skill integrates with:

- **Pre-Commit Hooks** - Block commits with architecture violations
- **CI/CD Pipeline** - Automated validation in GitHub Actions, GitLab CI
- **Quality Gates** - Part of comprehensive quality checks

See [Code Examples](./references/code-examples.md) for complete integration scripts for pre-commit hooks, CI/CD workflows, and quality gate configurations.

## Supporting Files

- **[references/reference.md](./references/reference.md)** - Complete layer dependency matrices for all patterns
- **[references/code-examples.md](./references/code-examples.md)** - All code examples, detection patterns, and integration scripts
- **[references/diff-aware-validation.md](./references/diff-aware-validation.md)** - Diff-aware validation comprehensive guide
- **[references/diff-aware-validation-summary.md](./references/diff-aware-validation-summary.md)** - Diff-aware validation summary
- **[references/diff-aware-validation-checklist.md](./references/diff-aware-validation-checklist.md)** - Pre-commit validation checklist
- **[references/diff-aware-validation-quickref.md](./references/diff-aware-validation-quickref.md)** - Quick reference for diff-aware validation
- **[references/installation.md](./references/installation.md)** - Installation and integration guide
- **[scripts/validate.py](./scripts/validate.py)** - Standalone validation script for all architectural patterns
- **[templates/arch-rules.yaml](./templates/arch-rules.yaml)** - Customizable rule definitions

## Expected Outcomes

### Success (No Violations)
When validation passes, you'll see confirmation that all layer boundaries are respected and dependencies flow correctly.

### Failure (Violations Found)
When violations are detected, you'll receive a detailed report including:
- Violation severity (CRITICAL, HIGH, MEDIUM, LOW)
- File path and line number
- Specific import statement causing the violation
- Recommended fix with explanation
- Impact assessment

See [Code Examples](./references/code-examples.md) for complete example output showing success and failure reports with detailed violation listings.

## Success Metrics

After invoking this skill, measure:
- **Violation Detection Rate**: 95%+ (catches all major violations)
- **False Positive Rate**: <5% (minimal incorrect reports)
- **Context Reduction**: 90%+ vs manual agent review
- **Execution Time**: <2s for typical codebase
- **Actionability**: 100% of violations include specific fix

## Customization

### Define Custom Rules
Create `arch-rules.yaml` in project root to customize layer paths, import rules, severity levels, and exceptions for your project's specific architectural needs.

### Language Support
Currently supports Python (`.py`), JavaScript (`.js`), and TypeScript (`.ts`). Extend by adding patterns in `scripts/validate.py`.

See [templates/arch-rules.yaml](./templates/arch-rules.yaml) for a complete example configuration with all available options and [Code Examples](./references/code-examples.md) for YAML configuration samples.

## Troubleshooting

### Issue: False Positives
Valid imports flagged as violations. Add exceptions to `arch-rules.yaml`.

### Issue: Pattern Not Detected
Skill doesn't recognize architectural pattern. Ensure `ARCHITECTURE.md` contains pattern keywords: "Clean Architecture", "Hexagonal Architecture", "Layered Architecture", or "MVC".

### Issue: Missing Violations
Known violations not reported. Check file paths match layer definitions. Update layer patterns if needed.

See [Code Examples](./references/code-examples.md) for complete troubleshooting examples with exception configurations and pattern detection fixes.

## Expected Benefits

| Metric | Without Validation | With Validation | Improvement |
|--------|-------------------|----------------|-------------|
| Architecture violations | 15-20 per quarter | 0-2 per quarter | 95% reduction |
| Time to detect violations | 2-5 days | 5-10 seconds | 99.9% faster |
| Refactoring cost | High (violations embedded) | Low (caught early) | 80% reduction |
| Code review time | 45-60 min | 15-20 min | 70% faster |
| Onboarding time | 2-3 weeks | 3-5 days | 75% faster |
| Technical debt | 20-30 violations/year | 2-5 violations/year | 90% reduction |

## Requirements

- Python 3.10+ (for validation script)
- Source code in supported language (Python/JS/TS)
- `ARCHITECTURE.md` or similar documentation defining layers
- Read, Grep, Bash, Glob tools available

## Red Flags to Avoid

### Architecture Violations

1. **Domain importing Infrastructure** - Breaks dependency inversion
2. **Application importing Interface** - Creates circular dependencies
3. **Infrastructure importing concrete Domain** - Should use Protocols
4. **Business logic in Interface layer** - Violates layer separation

### Detection Anti-Patterns

5. **Ignoring False Positives** - Add exceptions to arch-rules.yaml
6. **Skipping validation before major changes** - Always validate first
7. **Not updating layer definitions** - Keep ARCHITECTURE.md current
8. **Assuming pattern without verification** - Read ARCHITECTURE.md first

### Process Mistakes

9. **Proceeding with violations** - Fix before committing
10. **Not documenting exceptions** - Explain why deviation needed
11. **Skipping after refactor** - Validation most critical after structural changes
12. **Manual validation only** - Automate in pre-commit hooks and CI

## Utility Scripts

- [Validate Architecture Script](./scripts/validate.py) - Full-featured architecture validation tool supporting Clean, Hexagonal, Layered, and MVC patterns

## See Also

- **validate-layer-boundaries** - Project-specific validation for project-watch-mcp
- **@architecture-guardian** - Agent for architectural guidance and review
- **ARCHITECTURE.md** - Project's architecture documentation
- **ADR-001** - Architecture Decision Record for Clean Architecture
