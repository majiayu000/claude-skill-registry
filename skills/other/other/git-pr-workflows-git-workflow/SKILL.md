---
version: 4.1.0-fractal
name: git-pr-workflows-git-workflow
description: "Orchestrate a comprehensive git workflow from code review through PR creation, leveraging specialized agents for quality assurance, testing, and deployment readiness. This workflow implements modern g"
---

# Complete Git Workflow with Multi-Agent Orchestration

Orchestrate a comprehensive git workflow from code review through PR creation, leveraging specialized agents for quality assurance, testing, and deployment readiness. This workflow implements modern git best practices including Conventional Commits, automated testing, and structured PR creation.

[Extended thinking: This workflow coordinates multiple specialized agents to ensure code quality before commits are made. The code-reviewer agent performs initial quality checks, test-automator ensures all tests pass, and deployment-engineer verifies production readiness. By orchestrating these agents sequentially with context passing, we prevent broken code from entering the repository while maintaining high velocity. The workflow supports both trunk-based and feature-branch strategies with configurable options for different team needs.]

## Use this skill when

- Working on complete git workflow with multi-agent orchestration tasks or workflows
- Needing guidance, best practices, or checklists for complete git workflow with multi-agent orchestration

## Do not use this skill when

- The task is unrelated to complete git workflow with multi-agent orchestration
- You need a different domain or tool outside this scope

## Instructions

- Clarify goals, constraints, and required inputs.
- Apply relevant best practices and validate outcomes.
- Provide actionable steps and verification.
- If detailed examples are required, open `resources/implementation-playbook.md`.

## Configuration

**Target branch**: $ARGUMENTS (defaults to 'main' if not specified)

**Supported flags**:
- `--skip-tests`: Skip automated test execution (use with caution)
- `--draft-pr`: Create PR as draft for work-in-progress
- `--no-push`: Perform all checks but don't push to remote
- `--squash`: Squash commits before pushing
- `--conventional`: Enforce Conventional Commits format strictly
- `--trunk-based`: Use trunk-based development workflow
- `--feature-branch`: Use feature branch workflow (default)

## Phase 1: Pre-Commit Review and Analysis

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [1. Code Quality Assessment](./sub-skills/1-code-quality-assessment.md)
### 2. [2. Dependency and Breaking Change Analysis](./sub-skills/2-dependency-and-breaking-change-analysis.md)
### 3. [1. Test Execution and Coverage](./sub-skills/1-test-execution-and-coverage.md)
### 4. [2. Test Recommendations and Gap Analysis](./sub-skills/2-test-recommendations-and-gap-analysis.md)
### 5. [1. Change Analysis and Categorization](./sub-skills/1-change-analysis-and-categorization.md)
### 6. [2. Conventional Commit Message Creation](./sub-skills/2-conventional-commit-message-creation.md)
### 7. [1. Branch Management](./sub-skills/1-branch-management.md)
### 8. [2. Pre-Push Validation](./sub-skills/2-pre-push-validation.md)
### 9. [1. PR Description Generation](./sub-skills/1-pr-description-generation.md)
### 10. [2. PR Metadata and Automation Setup](./sub-skills/2-pr-metadata-and-automation-setup.md)
