---
version: 4.1.0-fractal
name: shellcheck-configuration
description: Master ShellCheck static analysis configuration and usage for shell script quality. Use when setting up linting infrastructure, fixing code issues, or ensuring script portability.
---

# ShellCheck Configuration and Static Analysis

Comprehensive guidance for configuring and using ShellCheck to improve shell script quality, catch common pitfalls, and enforce best practices through static code analysis.

## Do not use this skill when

- The task is unrelated to shellcheck configuration and static analysis
- You need a different domain or tool outside this scope

## Instructions

- Clarify goals, constraints, and required inputs.
- Apply relevant best practices and validate outcomes.
- Provide actionable steps and verification.
- If detailed examples are required, open `resources/implementation-playbook.md`.

## Use this skill when

- Setting up linting for shell scripts in CI/CD pipelines
- Analyzing existing shell scripts for issues
- Understanding ShellCheck error codes and warnings
- Configuring ShellCheck for specific project requirements
- Integrating ShellCheck into development workflows
- Suppressing false positives and configuring rule sets
- Enforcing consistent code quality standards
- Migrating scripts to meet quality gates

## ShellCheck Fundamentals

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [What is ShellCheck?](./sub-skills/what-is-shellcheck.md)
### 2. [Installation](./sub-skills/installation.md)
### 3. [.shellcheckrc (Project Level)](./sub-skills/shellcheckrc-project-level.md)
### 4. [Environment Variables](./sub-skills/environment-variables.md)
### 5. [SC1000-1099: Parser Errors](./sub-skills/sc1000-1099-parser-errors.md)
### 6. [SC2000-2099: Shell Issues](./sub-skills/sc2000-2099-shell-issues.md)
### 7. [SC2100-2199: Quoting Issues](./sub-skills/sc2100-2199-quoting-issues.md)
### 8. [SC3000-3999: POSIX Compliance Issues](./sub-skills/sc3000-3999-posix-compliance-issues.md)
### 9. [Minimal Configuration (Strict POSIX)](./sub-skills/minimal-configuration-strict-posix.md)
### 10. [Development Configuration (Bash with Relaxed Rules)](./sub-skills/development-configuration-bash-with-relaxed-rules.md)
### 11. [CI/CD Integration Configuration](./sub-skills/cicd-integration-configuration.md)
### 12. [.shellcheckrc for Project](./sub-skills/shellcheckrc-for-project.md)
### 13. [Pre-commit Hook Configuration](./sub-skills/pre-commit-hook-configuration.md)
### 14. [GitHub Actions Workflow](./sub-skills/github-actions-workflow.md)
### 15. [GitLab CI Pipeline](./sub-skills/gitlab-ci-pipeline.md)
### 16. [Suppressing Specific Warnings](./sub-skills/suppressing-specific-warnings.md)
### 17. [Common Violations and Fixes](./sub-skills/common-violations-and-fixes.md)
### 18. [Checking Multiple Files](./sub-skills/checking-multiple-files.md)
### 19. [Caching Results](./sub-skills/caching-results.md)
### 20. [Default Format](./sub-skills/default-format.md)
### 21. [GCC Format (for CI/CD)](./sub-skills/gcc-format-for-cicd.md)
### 22. [JSON Format (for parsing)](./sub-skills/json-format-for-parsing.md)
### 23. [Quiet Format](./sub-skills/quiet-format.md)
