---
name: product-context-docs
description: Create and update in-repo product context documentation in /docs (product profile, features, sitemap, architecture, tech stack). Use when asked to document a product, bootstrap /docs structure, or refresh product/tech context docs for a repo.
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Write, Edit
argument-hint: "[optional: product context doc request]"
read-only: false
destructive: false
idempotent: true
open-world: false
user-invocable: true
tags: product, docs, context
capabilities: product.docs.create, product.docs.update
activation-intents: document product, bootstrap docs, refresh product context
activation-events: user-prompt
activation-artifacts: docs/**, README.md
risk-level: low
---

# Product Context Docs

## Overview

Use this skill to create or update product context documentation under `/docs` in the current repository. Keep the docs accurate, concise, and easy to scan, and preserve existing content when it is already correct.

## Workflow

1. Locate the repo root (use the current working directory unless told otherwise).
2. Read existing context first: `README.md`, `docs/` (if present), product briefs, and any architecture or design notes.
3. Ask targeted questions only for missing essentials: product name, target users, key jobs-to-be-done, differentiators, primary user flows, core features, and any technical constraints.
4. Ensure the folder structure exists: `/docs/product` and `/docs/tech`.
5. Create or update the default doc set (see below). Reuse existing content and update deltas rather than rewriting everything.
6. Cross-link the docs where helpful (e.g., features to architecture, sitemap to features).
7. Call out assumptions explicitly and mark placeholders as `TODO` when information is missing.

## Default Doc Set

Create or maintain these files as the minimum set:

- `/docs/product/product-profile.md` (product summary, users, value, metrics)
- `/docs/product/product-features.md` (feature list, scope, status)
- `/docs/product/sitemap.md` (information architecture and core flows)
- `/docs/tech/architecture.md` (system overview, components, data flows)
- `/docs/tech/tech-stack.md` (languages, frameworks, infra, tooling)

Add additional docs only when requested or clearly needed (e.g., `/docs/product/glossary.md`, `/docs/tech/security.md`).

## Templates

Use the templates in `assets/templates/` as starting points. Copy the closest template into `/docs/...` and fill it with repo-specific details:

- `assets/templates/product-profile.md`
- `assets/templates/product-features.md`
- `assets/templates/sitemap.md`
- `assets/templates/architecture.md`
- `assets/templates/tech-stack.md`

## Writing Guidelines

- Use Markdown with short sections, tables, and bullet lists.
- Prefer concrete details over generic language.
- Use Mermaid diagrams for architecture when it clarifies flows.
- Keep each doc independently readable; repeat minimal context where needed.
- Preserve correct existing content and only change what is outdated or missing.
