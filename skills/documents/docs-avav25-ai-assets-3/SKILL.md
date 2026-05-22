---
name: docs
description: Documentation workflow for updating markdown docs, technical writing, PRDs, release notes, and public content without touching application source code.
---

# Documentation

Use this workflow for documentation-only changes.

## Scope

Allowed:

- Markdown docs
- PRDs
- ADRs
- Release notes
- Blog or marketing copy

Not allowed:

- Application source code
- Build config
- Infrastructure code
- Dependency manifests

## 1. Gather Context

Read:

1. Root `AGENTS.md`
2. Relevant scoped `AGENTS.md`
3. Existing docs in the target area
4. Related code only when needed for technical accuracy

## 2. Classify the Content

Identify whether the change is:

- Internal technical docs
- Product or planning docs
- Public-facing marketing or blog content
- Release communication

## 3. Write

Rules:

- English only unless the user requests otherwise
- Match existing terminology
- Keep examples technically accurate
- Prefer concise, scannable structure

For public content, include SEO-aware structure where relevant.

## 4. Verify

Check:

- Links resolve
- Terminology matches project conventions
- Formatting is consistent
- No code or config files were changed

## 5. Report

Summarize the files changed and any follow-up review recommended.