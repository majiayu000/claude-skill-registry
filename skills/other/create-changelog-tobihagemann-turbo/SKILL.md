---
name: create-changelog
description: "Create a CHANGELOG.md following keepachangelog.com conventions with version history backfilled from GitHub releases or git tags. Use when the user asks to \"create a changelog\", \"add a changelog\", \"initialize changelog\", \"start a changelog\", \"set up changelog\", \"generate changelog\", or \"backfill changelog\"."
---

# Create Changelog

Create a changelog backfilled with version history.

## Step 1: Run `/changelog-rules` Skill

Run `/changelog-rules` to load shared changelog conventions.

## Step 2: Backfill Version History

Collect release history from the most authoritative source available:

1. **GitHub releases** (preferred): Run `gh release list --limit 100 --json tagName,name,publishedAt,body` to get release notes. For each release, parse the body into changelog entries.
2. **Git tags** (fallback): If no GitHub releases exist, run `git tag --sort=-v:refname` to list tags. For each consecutive tag pair, run `git log <older-tag>..<newer-tag> --oneline` to collect commit summaries.

For each version, classify entries into the standard change types and apply the changelog-worthiness criteria per `/changelog-rules`.

## Step 3: Check for Existing Changelog

If the changelog file already exists, warn the user and confirm before overwriting.

## Step 4: Write Changelog

Write the changelog following the `/changelog-rules` file structure and conventions.

## Step 5: Present the Result

Briefly summarize how many versions were backfilled and which source was used (GitHub releases or git tags).
