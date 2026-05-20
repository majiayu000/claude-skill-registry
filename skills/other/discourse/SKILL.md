---
name: discourse
description: >-
  Scan community discussion channels (HN, Lobsters, Reddit,
  tech blogs) for experience reports and opinions on a
  topic. Use when the user wants community perspectives
  on a technology or approach.
version: 1.8.4
alwaysApply: false
category: research
tags:
  - hackernews
  - reddit
  - lobsters
  - blogs
  - discourse
estimated_tokens: 200
model_hint: standard
---
# Discourse Search

## When To Use

- Gathering community opinions on a technology or approach
- Finding experience reports from HN, Reddit, or Lobsters

## When NOT To Use

- Academic research (use `/tome:papers`)
- Code examples (use `/tome:code-search`)

Scan community channels for discussions on a topic.

## Channels

- **Hacker News**: Algolia API at hn.algolia.com
- **Lobsters**: WebSearch with site:lobste.rs
- **Reddit**: JSON API (append .json to URLs)
- **Tech blogs**: WebSearch targeting curated domains

## Workflow

1. Build search URLs/queries per channel using
   `tome.channels.discourse.*` functions
2. Execute via WebFetch (APIs) or WebSearch (fallback)
3. Parse responses into Finding objects
4. Merge across sources with source attribution
