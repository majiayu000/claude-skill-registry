---
name: pensive:shared
description: 'DO NOT use directly: this skill is infrastructure for other pensive
  skills. This skill provides shared patterns consumed by other pensive skills. Use
  when other pensive skills need common patterns, creating new review skills, ensuring
  consistency across pensive plugin.'
category: review-infrastructure
tags:
- shared
- infrastructure
- review
- patterns
version: 1.4.0
estimated_tokens: 50
---

# Pensive Shared Review Infrastructure

This skill provides reusable modules and patterns shared across all pensive review skills.

## Purpose

Centralized infrastructure for:
- Common workflow patterns
- Output format templates
- Quality checklist patterns
- Evidence logging integration

## Module Structure

Available shared modules:
- See `modules/review-workflow-core.md` for the core 5-step workflow pattern
- See `modules/output-format-templates.md` for standard output structures
- See `modules/quality-checklist-patterns.md` for reusable quality checklists
- See `modules/code-quality-analysis.md` for deduplication and redundancy detection

## Usage

Review skills include these modules to inherit common patterns:

```yaml
includes:
  - ../shared/modules/review-workflow-core.md
  - ../shared/modules/output-format-templates.md
  - ../shared/modules/quality-checklist-patterns.md
```
**Verification:** Run the command with `--help` flag to verify availability.

## Consumers

All pensive review skills:
- `pensive:bug-review`
- `pensive:api-review`
- `pensive:architecture-review`
- `pensive:test-review`
- `pensive:rust-review`
- `pensive:makefile-review`
- `pensive:math-review`
- `pensive:unified-review`
- `pensive:code-refinement`
## Troubleshooting

### Common Issues

**Command not found**
Ensure all dependencies are installed and in PATH

**Permission errors**
Check file permissions and run with appropriate privileges

**Unexpected behavior**
Enable verbose logging with `--verbose` flag
