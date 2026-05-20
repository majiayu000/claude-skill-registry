---
name: commit-drafter
description: Automatically draft commit messages by analyzing git status and staged changes
version: 1.0.0
author: abereyes
triggers:
  - "draft a commit"
  - "draft commit"
  - "create commit message"
  - "write commit message"
  - "suggest commit message"
  - "generate commit message"
---

# Commit Message Drafter

Automatically generates commit messages by analyzing your staged changes.

## What It Does

- Analyzes git status and staged changes
- Extracts full diff content with statistics
- Provides structured context to Claude (the AI)
- Claude writes a meaningful commit message based on actual changes

## Usage

Just say:
- "draft a commit for me to review"
- "create a commit message"
- "suggest a commit message"

The skill will automatically:
1. Check git status
2. Extract file changes and statistics
3. Get the full diff content
4. Present context to Claude
5. Claude analyzes the changes and writes a clear, descriptive commit message
6. Return it for your review

## How It Works

Unlike template-based commit tools that just output placeholders, this skill provides **real git context** to Claude (the AI), who then writes a **meaningful commit message** based on understanding the actual code changes.

The script outputs:
- Files changed (added, modified, deleted, renamed)
- Change statistics (+insertions, -deletions)
- Full diff content showing exact changes
- Instructions for Claude to write the commit

Claude then reads this context and writes a commit message that actually describes what changed and why.

## Value

No more staring at `git diff` trying to write a commit message. No more useless templates with [TODO] placeholders. Claude reads your changes, understands them, and drafts a meaningful message automatically.
