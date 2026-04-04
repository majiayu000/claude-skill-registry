---
name: init-repo
description: Initialize a fork of GoodDocs with fork-specific defaults and a customized doc type.
---

# Skill: init-repo

## Purpose
Initialize a fork of GoodDocs with fork-specific defaults and a customized doc type.

## Behavior
1. Prompt the user for:
   - `repoName`
   - `docTypeDisplayName` (default: Design Docs)
   - `docTypeKey` (default: design-docs)
   - `docRoot` folder name under `docs/` (default derived from docTypeKey)
   - `defaultOwners` (comma-separated)
2. Create `repo.config.json` with:
   - `repoName`, `defaultDocTypeKey`, `defaultOwners` (array), and `createdAt` (YYYY-MM-DD).
3. Update `schema/doc_rules.json` so `docTypes[0]` matches the new doc type key, display name, and doc root.
4. If `docs/example` exists and the chosen doc root differs, rename it and update links in `docs/README.md`.
5. Run `python3 scripts/validate_docs.py` and fix issues before finishing.
