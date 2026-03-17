---
name: ghost
description: Publish and manage content in Ghost CMS. Use for publishing posts, validating frontmatter, and understanding the Ghost sync workflow. Includes /publish and /validate commands.
---

# Ghost Skill

Publish content to Ghost CMS and manage the sync workflow.

## When to Use

- Publishing posts to Ghost (`/publish` command)
- Validating frontmatter before publishing (`/validate` command)
- Promoting drafts to published (`/promote` command)
- Understanding Ghost sync behaviour

## Quick Reference

**Source of truth:** This repo (not Ghost Admin)

**Publish flow:**
1. Edit in `content/drafts/*.md` or `content/posts/*.md`
2. Run `/validate` to check frontmatter
3. Run `/publish` to sync to Ghost

**Ghost will be overwritten** by the repo on every publish.

## Context Files

- `context/sync.md` - How repo ↔ Ghost sync works
- `context/api.md` - Ghost Admin API reference

## Commands

| Command | Purpose |
|---------|---------|
| `/publish` | Sync all content to Ghost |
| `/validate` | Check frontmatter validity |
| `/promote [slug]` | Move draft to posts and publish |
