---
name: test-updates
description: 'Update and maintain tests following TDD/BDD principles with detailedquality
  assurance.Triggers: test updates, test maintenance, test generation, TDD workflow,BDD
  patterns, test coverage, pytest, test'
---

---
name: test-updates
description: |

Triggers: quality-assurance, test-generation, test, bdd, pytest
  Update and maintain tests following TDD/BDD principles with detailed
  quality assurance.

  Triggers: test updates, test maintenance, test generation, TDD workflow,
  BDD patterns, test coverage, pytest, test enhancement, quality assurance

  Use when: updating existing tests, generating new tests for features,
  enhancing test quality, ensuring detailed coverage, pre-commit validation

  DO NOT use when: auditing test suites - use pensive:test-review.
  DO NOT use when: writing production code - focus on implementation first.

  Run git-workspace-review first to understand which tests need updates.
version: 1.3.5
category: testing-automation
tags: [tdd, bdd, testing, quality-assurance, test-generation, pytest]
dependencies: [test-driven-development, git-workspace-review, file-analysis]
tools: [test_analyzer, test_generator, quality_checker]
usage_patterns:
  - test-maintenance
  - test-generation
  - test-enhancement
  - quality-validation
complexity: intermediate
estimated_tokens: 1500
---
## Table of Contents

- [Overview](#overview)
- [Core Philosophy](#core-philosophy)
- [What It Is](#what-it-is)
- [Quick Start](#quick-start)
- [Quick Checklist for First Time Use](#quick-checklist-for-first-time-use)
- [detailed Test Update](#detailed-test-update)
- [Targeted Test Updates](#targeted-test-updates)
- [TDD for New Features](#tdd-for-new-features)
- [Using the Scripts Directly](#using-the-scripts-directly)
- [When to Use It](#when-to-use-it)
- [Workflow Integration](#workflow-integration)
- [Phase 1: Discovery](#phase-1:-discovery)
- [Phase 2: Strategy](#phase-2:-strategy)
- [Phase 3: Implementation](#phase-3:-implementation)
- [Phase 4: Validation](#phase-4:-validation)
- [Quality Assurance](#quality-assurance)
- [Examples](#examples)
- [BDD-Style Test Generation](#bdd-style-test-generation)
- [Test Enhancement](#test-enhancement)
- [Integration with Existing Skills](#integration-with-existing-skills)
- [Success Metrics](#success-metrics)
- [Troubleshooting FAQ](#troubleshooting-faq)
- [Common Issues](#common-issues)
- [Performance Tips](#performance-tips)
- [Getting Help](#getting-help)


# Test Updates and Maintenance

## Overview

detailed test management system that applies TDD/BDD principles to maintain, generate, and enhance tests across codebases. This skill practices what it preaches - it uses TDD principles for its own development and serves as a living example of best practices.

### Core Philosophy

- **RED-GREEN-REFACTOR**: Strict adherence to TDD cycle
- **Behavior-First**: BDD patterns that describe what code should do
- **Meta Dogfooding**: The skill's own tests demonstrate the principles it teaches
- **Quality Gates**: detailed validation before considering tests complete

## What It Is

A modular test management system that:
- Discovers what needs testing or updating
- Generates tests following TDD principles
- Enhances existing tests with BDD patterns
- Validate test quality through multiple lenses

## Quick Start

### Quick Checklist for First Time Use
- [ ] validate pytest is installed (`pip install pytest`)
- [ ] Have your source code in `src/` or similar directory
- [ ] Create a `tests/` directory if it doesn't exist
- [ ] Run `Skill(sanctum:git-workspace-review)` first to understand changes
- [ ] Start with `Skill(test-updates) --target <specific-module>` for focused updates

### detailed Test Update
```bash
# Run full test update workflow
Skill(test-updates)
```
**Verification:** Run `pytest -v` to verify tests pass.

### Targeted Test Updates
```bash
# Update tests for specific paths
Skill(test-updates) --target src/sanctum/agents
Skill(test-updates) --target tests/test_commit_messages.py
```
**Verification:** Run `pytest -v` to verify tests pass.

### TDD for New Features
```bash
# Apply TDD to new code
Skill(test-updates) --tdd-only --target new_feature.py
```
**Verification:** Run `pytest -v` to verify tests pass.

### Using the Scripts Directly

**Human-Readable Output:**
```bash
# Analyze test coverage gaps
python plugins/sanctum/skills/test-updates/scripts/test_analyzer.py --scan src/

# Generate test scaffolding
python plugins/sanctum/skills/test-updates/scripts/test_generator.py \
    --source src/my_module.py --style pytest_bdd

# Check test quality
python plugins/sanctum/skills/test-updates/scripts/quality_checker.py \
    --validate tests/test_my_module.py
```
**Verification:** Run `pytest -v` to verify tests pass.

**Programmatic Output (for Claude Code):**
```bash
# Get JSON output for programmatic parsing - test_analyzer
python plugins/sanctum/skills/test-updates/scripts/test_analyzer.py \
    --scan src/ --output-json

# Returns:
# {
#   "success": true,
#   "data": {
#     "source_files": ["src/module.py", ...],
#     "test_files": ["tests/test_module.py", ...],
#     "uncovered_files": ["module_without_tests", ...],
#     "coverage_gaps": [{"file": "...", "reason": "..."}]
#   }
# }

# Get JSON output - test_generator
python plugins/sanctum/skills/test-updates/scripts/test_generator.py \
    --source src/my_module.py --output-json

# Returns:
# {
#   "success": true,
#   "data": {
#     "test_file": "path/to/test_my_module.py",
#     "source_file": "src/my_module.py",
#     "style": "pytest_bdd",
#     "fixtures_included": true,
#     "edge_cases_included": true,
#     "error_cases_included": true
#   }
# }

# Get JSON output - quality_checker
python plugins/sanctum/skills/test-updates/scripts/quality_checker.py \
    --validate tests/test_my_module.py --output-json

# Returns:
# {
#   "success": true,
#   "data": {
#     "static_analysis": {...},
#     "dynamic_validation": {...},
#     "metrics": {...},
#     "quality_score": 85,
#     "quality_level": "QualityLevel.GOOD",
#     "recommendations": [...]
#   }
# }
```
**Verification:** Run `pytest -v` to verify tests pass.

## When to Use It

**Use this skill when you need to:**
- Update tests after code changes
- Generate tests for new features
- Improve existing test quality
- validate detailed test coverage

**Perfect for:**
- Pre-commit test validation
- CI/CD pipeline integration
- Refactoring with test safety
- Onboarding new developers

## Workflow Integration

### Phase 1: Discovery
1. Scan codebase for test gaps
2. Analyze recent changes
3. Identify broken or outdated tests

See `modules/test-discovery.md` for detection patterns.

### Phase 2: Strategy
1. Choose appropriate BDD style (see `modules/bdd-patterns.md`)
2. Plan test structure
3. Define quality criteria

### Phase 3: Implementation
1. Write failing tests (RED) - see `modules/tdd-workflow.md`
2. Implement minimal passing code (GREEN)
3. Refactor for clarity (REFACTOR)

See `modules/test-generation.md` for generation templates.

### Phase 4: Validation
1. Static analysis and linting
2. Dynamic test execution
3. Coverage and quality metrics

See `modules/quality-validation.md` for validation criteria.

## Quality Assurance

The skill applies multiple quality checks:
- **Static**: Linting, type checking, pattern validation
- **Dynamic**: Test execution in sandboxed environments
- **Metrics**: Coverage, mutation score, complexity analysis
- **Review**: Structured checklists for peer validation

## Examples

### BDD-Style Test Generation

See `modules/bdd-patterns.md` for additional patterns.
```python
class TestGitWorkflow:
    """BDD-style tests for Git workflow operations."""

    def test_commit_workflow_with_staged_changes(self):
        """
        GIVEN a Git repository with staged changes
        WHEN the user runs the commit workflow
        THEN it should create a commit with proper message format
        AND all tests should pass
        """
        # Test implementation following TDD principles
        pass
```
**Verification:** Run `pytest -v` to verify tests pass.

### Test Enhancement
- Add edge cases and error scenarios
- Include performance benchmarks
- Add mutation testing for robustness

See `modules/test-enhancement.md` for enhancement strategies.

## Integration with Existing Skills

1. **git-workspace-review**: Get context of changes
2. **file-analysis**: Understand code structure
3. **test-driven-development**: Apply strict TDD discipline
4. **skills-eval**: Validate quality and compliance

## Success Metrics

- Test coverage > 85%
- All tests follow BDD patterns
- Zero broken tests in CI
- Mutation score > 80%

## Troubleshooting FAQ

### Common Issues

**Q: Tests are failing after generation**
A: This is expected! The skill follows TDD principles - generated tests are designed to fail first. Follow the RED-GREEN-REFACTOR cycle:
1. Run the test and confirm it fails for the right reason
2. Implement minimal code to make it pass
3. Refactor for clarity

**Q: Quality score is low despite having tests**
A: Check for these common issues:
- Missing BDD patterns (Given/When/Then)
- Vague assertions like `assert result is not None`
- Tests without documentation
- Long, complex tests (>50 lines)

**Q: Generated tests don't match my code structure**
A: The scripts analyze AST patterns and may need guidance:
- Use `--style` flag to match your preferred BDD style
- Check that source files have proper function/class definitions
- Review the generated scaffolding and customize as needed

**Q: Mutation testing takes too long**
A: Mutation testing is resource-intensive:
- Use `--quick-mutation` flag for subset testing
- Focus on critical modules first
- Run overnight for detailed analysis

**Q: Can't find tests for my file**
A: The analyzer uses naming conventions:
- Source: `my_module.py` → Test: `test_my_module.py`
- Check that test files follow pytest naming patterns
- validate test directory structure is standard

### Performance Tips

- **Large codebases**: Use `--target` to focus on specific directories
- **CI integration**: Run validation in parallel with other checks
- **Memory usage**: Process files in batches for very large projects

### Getting Help

1. Check script outputs for detailed error messages
2. Use `--verbose` flag for more information
3. Review the validation report for specific recommendations
4. Start with small modules to understand patterns before scaling
