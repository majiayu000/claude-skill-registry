---
name: git-branch-namer
description: Use only when the user explicitly asks for a git branch name. Output one strong recommendation in a consistent pattern, with minimal, high-signal rationale.
metadata:
  short-description: Name git branches
---

# Git Branch Namer

Suggest a git branch name that encodes type, scope, and intent with minimal redundancy.

## Output

Provide:

* One recommended branch name.
* One sentence explaining the chosen type, scope, and intent.
* 2–4 alternatives only if the user asks for options.

## Default Pattern

Use `<type>/<scope>/<intent>` unless the user specifies another convention.

## Type

Choose the smallest accurate change class:

`feat`, `fix`, `chore`, `refactor`, `docs`, `test`, `perf`.

## Scope

Name the primary area being changed.

Guidelines:

* Prefer stable product, module, or capability scopes when the change is broadly reusable.
* Use interface or integration scopes only when the work is confined to that boundary.
* If multiple areas are touched, pick the dominant one or the user’s stated goal.

Examples:

* Product, module, capability: `scheduler`, `auth`, `billing`, `search`
* Interface or integration when accurate: `cli`, `rest`, `sdk`, `webhook`

## Intent

Use a concise verb-first kebab-case phrase. Avoid repeating scope words unless it adds clarity.

Good:

* `feat/auth/rotate-keys`
* `fix/search/dedupe-results`

Avoid:

* `feat/auth/auth-rotate-keys`
* `fix/search/search-dedupe-results`

## Heuristics

* Optimize for information density. Do not repeat obvious repo context.
* Make type, scope, and intent complementary rather than redundant.
* Do not overfit scope to a single interface if the capability is broader.
* If the user specifies a preferred pattern, follow it and briefly note tradeoffs when relevant.
* Ask one short clarification only when type or scope cannot be inferred safely.
