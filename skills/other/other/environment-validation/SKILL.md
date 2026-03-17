---
name: environment-validation
description: Unify toolchain versions and validation rules (project, gitignored). Use when environment validation guidance is required.
allowed-tools:
  - Bash(rg --version)
  - Bash(fd --version)
  - Bash(ast-grep --version)
  - Bash(python3 --version)
  - Bash(go version)
  - Bash(lua -v)
  - Bash(plantuml --version)
  - Bash(dbml2sql --version)
  - Bash(which *)
  - Bash(command -v *)
---
## Purpose

Validate that the active development toolchain satisfies governance requirements (versions, availability, and basic configuration) and produce a concise status signal that downstream agents and skills can consume.

## IO Semantics

Input: Current shell/environment, installed tools, and configuration files.
Output: Validation results (pass/fail plus key findings) and remediation hints.
Side Effects: May trigger separate installation or remediation commands when invoked by higher-level workflows, but this skill itself should focus on detection and reporting.
