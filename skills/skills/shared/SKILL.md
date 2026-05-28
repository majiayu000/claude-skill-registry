---
name: shared
description: |

Triggers: patterns, templates, specification, shared
  Shared infrastructure and patterns for spec-kit specification-driven development.

  Triggers: spec-kit patterns, tech-stack patterns, checklist dimensions,
  artifact structure, specification infrastructure, shared templates

  Use when: developing new spec-kit skills, referencing standard patterns,
  ensuring consistency across specification workflows

  DO NOT use directly: this skill is infrastructure for other spec-kit skills.

  Provides reusable patterns consumed by all spec-kit commands and skills.
category: infrastructure
tags: [shared, patterns, templates, specification]
provides:
  infrastructure: [tech-stack-patterns, checklist-dimensions, artifact-structure]
reusable_by: [all spec-kit skills and commands]
estimated_tokens: 200
---

# Shared Infrastructure

## Overview

Provides common patterns, templates, and infrastructure modules used across all spec-kit commands and skills. This skill exists to reduce duplication and maintain consistency in specification-driven development workflows.

## Purpose

This skill consolidates reusable components:
- Technology-specific patterns (ignore files, tooling configurations)
- Quality validation dimensions for requirements
- Artifact structure documentation (spec.md, plan.md, tasks.md, checklists)

## Modules

### tech-stack-patterns.md
Technology-specific patterns for common stacks and tools:
- Language-specific ignore patterns (Node.js, Python, Rust, Go, Java, C#)
- Common tool configurations (Docker, ESLint, Prettier, Terraform)
- Universal exclusions (.DS_Store, .vscode, .idea)

### checklist-dimensions.md
Quality validation dimensions for requirement testing:
- Completeness, Clarity, Consistency
- Measurability, Coverage, Edge Cases
- Non-Functional Requirements
- How to write "unit tests for requirements"

### artifact-structure.md
Spec-kit artifact organization and purpose:
- spec.md structure and role
- plan.md structure and role
- tasks.md structure and role
- checklists/ directory organization
- .specify/ feature directory layout

## Usage

This skill is automatically loaded by `speckit-orchestrator` and referenced by other spec-kit skills. It should not be loaded directly by commands.

## Related Skills

- `speckit-orchestrator`: Workflow coordination
- `spec-writing`: Specification creation
- `task-planning`: Task generation
## Troubleshooting

### Common Issues

**Command not found**
Ensure all dependencies are installed and in PATH

**Permission errors**
Check file permissions and run with appropriate privileges

**Unexpected behavior**
Enable verbose logging with `--verbose` flag
