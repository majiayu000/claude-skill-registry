---
name: doc-link-audit
description: Use before publishing documentation, merging a docs PR, or reporting a Markdown-heavy repo's navigation as complete — when you want ground-truth confirmation that internal links, heading anchors, and directory links resolve, without opening every file yourself.
---

# Doc Link Audit

## Overview

A dependency-free Python script that parses every `.md` file in a repo, resolves every `[text](target)` link, and reports what's actually broken: a missing file, a heading anchor that doesn't exist, or a page nothing else links to. It replicates GitHub's heading-slug algorithm exactly (including the double-hyphen case an em-dash produces) rather than a simplified approximation.

**Core principle:** A link checker that reports false positives on doc examples and fenced code blocks isn't worth reading a second time — teams turn it off. Excluding code spans and fenced blocks from the scan is not an optional nicety here, it's what makes the tool's output trustworthy enough to act on without re-verifying by hand.

## Usage

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/check_links.py [root_dir] [--check-external] [--exclude PATTERN]
```

- Defaults to `.`. Exit code 0 = clean, 1 = findings, 2 = usage error.
- `--exclude PATTERN` is a regex matched against each file path (e.g. `--exclude 'archive/|vendor/'`).
- `--check-external` additionally HEAD-requests every `http(s)://` link found (off by default — slow, needs network, and a timeout or 403 from an otherwise-fine site is not the same as a broken link).

## What it reports

| Section | Means |
|---|---|
| BROKEN LINKS | `[text](path)` where `path` doesn't resolve to a file, or `path#anchor` where the heading `anchor` doesn't exist in the target file |
| ORPHAN PAGES | A `.md` file no other `.md` file links to (excludes conventional entry points: README, INDEX, CHANGELOG, etc.) |
| EXTERNAL LINKS | `http(s)://` links found; only verified with `--check-external` |

A link to a directory (`[examples/](examples/)`) is treated as valid without checking for an `index.md` inside it — Markdown renderers differ on that resolution, so this script doesn't guess.

## Known limitation classes

This is a regex-and-string-position parser, not a real Markdown AST. Two situations it cannot fully solve:

1. **Pathological code-fence nesting** — a fenced block whose content itself contains a bare ` ``` ` line (e.g. showing fence syntax as an example) can confuse the opener/closer pairing. The script anchors fences to line boundaries (`` ^```lang\n...^```$ ``) which resolves the common case (adjacent untagged blocks — the bug this script's own first draft hit, self-diagnosed by running it against this library and getting 49 false positives before the fix), but a block genuinely nested inside another block will still mismatch. If you see a false positive pointing at `.md`/`.js`-shaped text inside what's clearly a code example, that's this limitation — exclude the file or accept the noise rather than trusting a hand-rolled fence parser to get arbitrary nesting right.
2. **Table cells and non-standard constructions** — `[text](target)`-shaped text that appears outside any fenced block or inline code span (rare, but possible inside a Markdown table cell with unusual escaping) is treated as a real link. Both single-backtick and double-backtick (`` `` `like this` `` ``, which permits literal single backticks inside) inline code spans are stripped correctly.

When in doubt, treat this script's report as "review these" not "these are definitely broken" — the same posture you'd take with any linter's edge cases.

## Remember

> Zero broken links reported means zero *file and anchor* problems. It says nothing about whether the content those links point to is any good, current, or the right thing to link to.
