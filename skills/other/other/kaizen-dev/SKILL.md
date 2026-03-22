---
name: kaizen-dev
description: Development workflow for Kaizen - branching, commits, testing
---
Development workflow:

**New feature**: `git checkout -b feat/<name>` from main
**Commits**: Use conventional commits (feat:, fix:, docs:, infra:, refactor:)
**Before commit**: Run /validate
**Key files**:
  - manifests/ — K8s YAML organized by node/function
  - scripts/ — Deployment and utility scripts
  - docs/ — Architecture and decision documents
  - CLAUDE.md — Project context (keep under 4KB)
  - .taskmaster/ — Task Master state and PRD

Task context: $ARGUMENTS
