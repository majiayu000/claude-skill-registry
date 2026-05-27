---
name: code-search
role: library
description: Searches GitHub for existing implementations, libraries, or patterns. Use when finding code examples or prior art on a topic during a research session.
alwaysApply: false
category: research
tags:
  - github
  - code
  - search
estimated_tokens: 200
model_hint: standard
---
# Code Search

## When To Use

- Finding existing implementations or libraries on GitHub
- Part of a `/tome:research` session or standalone search

## When NOT To Use

- Searching local codebase (use Grep or Explore agent)
- Academic literature (use `/tome:papers`)

Search GitHub for implementations of a given topic.

## Usage

Invoked as part of `/tome:research` or standalone.

## Workflow

1. Build search queries using
   `tome.channels.github.build_github_search_queries()`
2. Execute queries via WebSearch
3. Parse results via `parse_github_result()`
4. Optionally use GitHub API via
   `build_github_api_search()` for richer metadata
5. Rank via `rank_github_findings()`
6. Return Finding objects
