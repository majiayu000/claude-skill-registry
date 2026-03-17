---
name: makefile-dogfooder
description: 'Use this skill BEFORE releasing any plugin to verify Makefile coverage.
  Use when analyzing Makefile completeness before releasing plugins, identifying gaps
  during plugin maintenance, scoring Makefiles against best practices, verifying Makefiles
  support standard developer workflows. Do not use when writing initial Makefiles
  from scratch. DO NOT use when: debugging specific build target failures. DO NOT
  use when: creating custom non-standard build systems.'
author: Claude Skills
modules: true
---
## Table of Contents

- [Overview](#overview)
- [Workflow](#workflow)
- [1. Discovery Phase](#1-discovery-phase)
- [2. Analysis Phase](#2-analysis-phase)
- [3. Testing Phase](#3-testing-phase)
- [4. Generation Phase](#4-generation-phase)
- [Modules](#modules)
- [Discovery Module](#discovery-module)
- [Analysis Module](#analysis-module)
- [Testing Module](#testing-module)
- [Generation Module](#generation-module)
- [Examples](#examples)
- [Analyze a Single Plugin](#analyze-a-single-plugin)
- [Test All Plugins](#test-all-plugins)
- [Full Analysis with Auto-Apply](#full-analysis-with-auto-apply)
- [Quick Check](#quick-check)
- [Output Formats](#output-formats)
- [Text Output](#text-output)
- [JSON Output](#json-output)
- [Best Practices](#best-practices)
- [For Leaf Plugins](#for-leaf-plugins)
- [For Aggregator Makefiles](#for-aggregator-makefiles)
- [Target Naming](#target-naming)
- [Integration](#integration)
- [With Slash Commands](#with-slash-commands)
- [With CI/CD](#with-ci-cd)
- [With Development Workflow](#with-development-workflow)
- [Performance Considerations](#performance-considerations)
- [Troubleshooting](#troubleshooting)
- [Common Issues](#common-issues)
- [Debug Mode](#debug-mode)
- [Contributing](#contributing)
- [License](#license)


# Makefile Dogfooder Skill

Analyzes Makefiles to identify gaps in user-facing functionality, safely tests existing targets, and generates missing targets with contextually appropriate templates.

## Overview

This skill provides detailed Makefile analysis and enhancement for the claude-night-market project. It helps validate that all plugins have complete, consistent, and functional Makefile targets that support common user workflows.

## Workflow

### 1. Discovery Phase
```bash
# Find all Makefiles and extract targets
makefile_dogfooder.py --scope all --mode analyze
```
**Verification:** Run the command with `--help` flag to verify availability.

The discovery phase:
- Recursively searches for Makefile, makefile, GNUmakefile, and *.mk files
- Parses target definitions with dependencies and commands
- Extracts variable assignments and include statements
- Builds dependency graphs and detects plugin type (leaf vs aggregator)

### 2. Analysis Phase
```bash
# Analyze against best practices
makefile_dogfooder.py --mode analyze --output json
```
**Verification:** Run the command with `--help` flag to verify availability.

The analysis phase evaluates:
- **Essential targets** (help, clean, .PHONY) - 20 points each
- **Recommended targets** (test, lint, format, install, status) - 10 points each
- **Convenience targets** (demo, dogfood, check, quick-run) - 5 points each
- **Anti-patterns** (missing .PHONY, no error handling)
- **Consistency** across multiple Makefiles

### 3. Testing Phase
```bash
# Safely test existing targets
makefile_dogfooder.py --mode test
```
**Verification:** Run `pytest -v` to verify tests pass.

The testing phase performs:
- Syntax validation with `make -n`
- Help target functionality checks
- Variable dependency verification
- Common runtime issue detection

### 4. Generation Phase
```bash
# Generate missing targets
makefile_dogfooder.py --mode full --apply
```
**Verification:** Run the command with `--help` flag to verify availability.

The generation phase creates:
- **Demo targets** to showcase plugin functionality
- **Dogfood targets** for self-testing
- **Quick-run targets** for common workflows
- **Check-all targets** for aggregator Makefiles

## Modules

### Discovery Module
**File**: `modules/analysis.md`
- detailed file discovery algorithms
- Target parsing with metadata extraction
- Dependency graph construction
- Inventory creation with validation

### Analysis Module
**File**: `modules/analysis.md`
- Target taxonomy and best practices
- Anti-pattern detection rules
- Consistency checking algorithms
- Scoring and recommendation engine

### Testing Module
**File**: `modules/testing.md`
- Safe execution patterns
- Target categorization (safe/conditional/risky)
- Help system validation
- Error detection mechanisms

### Generation Module
**File**: `modules/generation.md`
- Template library for common targets
- Context-aware generation patterns
- Interactive customization workflow
- Plugin-type-specific templates

## Examples

### Analyze a Single Plugin
```bash
makefile_dogfooder.py --plugin abstract --mode analyze
```
**Verification:** Run the command with `--help` flag to verify availability.

### Test All Plugins
```bash
makefile_dogfooder.py --scope plugins --mode test
```
**Verification:** Run `pytest -v` to verify tests pass.

### Full Analysis with Auto-Apply
```bash
makefile_dogfooder.py --mode full --apply --output json
```
**Verification:** Run the command with `--help` flag to verify availability.

### Quick Check
```bash
makefile_dogfooder.py --scope root --mode analyze
```
**Verification:** Run the command with `--help` flag to verify availability.

## Output Formats

### Text Output
Human-readable summary with scores and recommendations:
```
**Verification:** Run the command with `--help` flag to verify availability.
=== Makefile Dogfooding Results ===
Scope: all
Mode: full
Makefiles analyzed: 10
Issues found: 23
Recommendations made: 15
```
**Verification:** Run the command with `--help` flag to verify availability.

### JSON Output
Machine-readable results for automation:
```json
{
  "scope": "all",
  "mode": "full",
  "makefiles_analyzed": 10,
  "details": [
    {
      "file": "plugins/abstract/Makefile",
      "score": 100,
      "issues": 0,
      "recommendations": 0
    }
  ]
}
```
**Verification:** Run the command with `--help` flag to verify availability.

## Best Practices

### For Leaf Plugins
- Always include: help, clean, test, lint
- Add demo target to showcase functionality
- Include dogfood target for self-testing
- Use shared includes from abstract when possible

### For Aggregator Makefiles
- Delegate to plugin Makefiles with pattern targets
- Include check-all target for detailed validation
- Maintain consistent target naming across plugins
- Provide helpful aggregate status information

### Target Naming
- Use kebab-case for target names
- Include brief description with `##` comment
- Group related targets with prefixes (test-, dev-, docs-)
- Follow alphabetical ordering for readability

## Integration

### With Slash Commands
The skill integrates with the `/make-dogfood` slash command for easy access:
```bash
/make-dogfood --scope plugins --mode full
```
**Verification:** Run the command with `--help` flag to verify availability.

### With CI/CD
Include in GitHub Actions for automated Makefile validation:
```yaml
- name: Validate Makefiles
  run: makefile_dogfooder.py --mode test --output json
```
**Verification:** Run `pytest -v` to verify tests pass.

### With Development Workflow
Run as part of pre-commit hooks:
```yaml
- repo: local
  hooks:
    - id: makefile-dogfooding
      entry: makefile_dogfooder.py
      language: system
      args: [--mode, analyze]
```
**Verification:** Run the command with `--help` flag to verify availability.

## Performance Considerations

- **Large Projects**: Use `--scope` to limit analysis scope
- **Quick Checks**: Use `--mode analyze` for fastest feedback
- **CI Environments**: Use `--mode test` without `--apply` for safe validation

## Troubleshooting

### Common Issues

1. **Parse Errors**: Check for complex Makefile syntax with conditionals
2. **Timeouts**: Use `--mode analyze` instead of `--mode test` for slow targets
3. **Missing Variables**: validate all referenced variables are defined
4. **Permission Errors**: Check file permissions for Makefile access

### Debug Mode
Enable verbose output for troubleshooting:
```bash
makefile_dogfooder.py --mode analyze --output json | jq '.details[] | select(.issues > 0)'
```
**Verification:** Run the command with `--help` flag to verify availability.

## Contributing

To extend the skill:

1. **Add New Templates**: Update the generation module with new target patterns
2. **Enhance Analysis**: Add new rules to the analysis module
3. **Improve Testing**: Add new test patterns to the testing module
4. **Report Issues**: Create bug reports with example Makefiles

## License

MIT License - see LICENSE file for details.
