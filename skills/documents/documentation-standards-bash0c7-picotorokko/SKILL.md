---
name: Documentation Standards
description: Provides guidelines for maintaining and updating documentation alongside code changes. Use this when implementing features, fixing bugs, or changing APIs that affect user-facing documentation.
---

# Documentation Standards Skill

This skill guides AI agents on how to maintain and update documentation when making code changes.

## When to Use This Skill

Use this skill when:
- You're implementing a new feature and need to know which docs to update
- You're fixing a bug that affects user-facing behavior
- You're changing command APIs or signatures
- You're creating new templates or workflows
- You need clarity on documentation standards and structure

## Key Principles

1. **Documentation is Part of the Feature** — Update docs in the same commit as code changes
2. **No Historical Context** — Keep all .md files clean, forward-facing only
3. **Specification First** — `docs/SPECIFICATION.md` is the source of truth
4. **Clear Audience Separation** — User-facing vs. developer-facing sections
5. **Link Consistency** — All references point to current locations

## Files Maintained by This Skill

- `docs/SPECIFICATION.md` — Command specifications and behavior
- `docs/CI_CD_GUIDE.md` — User/developer CI/CD workflows
- `docs/MRBGEMS_GUIDE.md` — mrbgem development and usage
- `docs/DEVICE_TESTING_GUIDE.md` — Device testing procedures
- `docs/PROJECT_INITIALIZATION_GUIDE.md` — Project setup guide
- `README.md` — Quick start and overview
- `AGENTS.md` — This skill's documentation location

## Implementation Guide

See `update-guide.md` in this directory for the step-by-step implementation checklist.
