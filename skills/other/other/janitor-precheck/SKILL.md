---
name: janitor-precheck
description: "Check if a new skill overlaps with your existing ones before installing. Use when the user wants to evaluate a skill before adding it, check for duplicates pre-install, or verify a GitHub skill won't conflict."
metadata:
  version: 1.1.0
---

# Pre-Install Overlap Check

Check if a new skill would duplicate existing ones before installing it.

## How to Run

```bash
bash ~/.claude/skills/skills-janitor/scripts/precheck.sh <github-url-or-path> [--json]
```

## Examples

```bash
# Check a GitHub repo
precheck.sh https://github.com/user/my-skill

# Check a specific skill folder in a repo
precheck.sh https://github.com/user/repo/tree/main/skills/my-skill

# Check a local path
precheck.sh ~/Downloads/some-skill/
```

## How It Works

1. Fetches the SKILL.md from the given GitHub URL or local path
2. Extracts description and trigger keywords
3. Compares against all installed skills using Jaccard similarity
4. Reports overlap level:
   - **0-30%**: Safe to install, no significant overlap
   - **30-60%**: Moderate overlap, review before installing
   - **60%+**: High overlap, likely duplicate of existing skill

## Output

```
=== Skills Janitor - Pre-Install Check ===

  Checking: marketing-seo-v2
  Keywords: seo, audit, ranking, technical, meta, tags

  Scanned 35 installed skills

  --- HIGH OVERLAP (likely duplicates) ---
    [72%] marketing-seo-audit (user)
         Shared: seo, audit, ranking, meta
         Existing desc: audit seo issues on your site...

  VERDICT: High overlap detected - likely duplicate
```

## After Checking

- If HIGH overlap: consider using the existing skill instead
- If MODERATE overlap: review both descriptions to see if they serve different purposes
- If SAFE: go ahead and install

## Related Skills

- For checking existing duplicates: `/janitor-report`
- For full inventory: `/janitor-audit`
