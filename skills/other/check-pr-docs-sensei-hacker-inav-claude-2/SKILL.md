---
description: Check pull requests for documentation updates and compliance
triggers:
  - check pr docs
  - check pr documentation
  - verify pr docs
  - check documentation
  - pr documentation check
  - docs compliance
  - documentation compliance
---

# Check PR Documentation Compliance

Analyzes pull requests from the last week to verify they include appropriate documentation updates. Identifies PRs that may need documentation but don't have it.

## Overview

This skill helps ensure PRs include proper documentation by:
1. Listing recent PRs (last 7 days) for each repository
2. Checking if PRs have documentation updates
3. **Independently checking wiki commits** (may not be mentioned in PR)
4. Assessing whether documentation is needed
5. Flagging PRs that may need docs tagged

## Quick Check

```bash
# List PRs from last week for inav firmware
cd inav
gh pr list --state all --search "created:>=$(date -d '7 days ago' +%Y-%m-%d)"

# List PRs from last week for configurator
cd inav-configurator
gh pr list --state all --search "created:>=$(date -d '7 days ago' +%Y-%m-%d)"
```

## Documentation Check Workflow

### Step 1: Get Recent PRs

For each repository (inav, inav-configurator), get PRs from the last week:

```bash
# Navigate to repo
cd inav  # or inav-configurator

# List PRs created in last 7 days
gh pr list --state all --search "created:>=$(date -d '7 days ago' +%Y-%m-%d)" --json number,title,url,state,author

# Get count
gh pr list --state all --search "created:>=$(date -d '7 days ago' +%Y-%m-%d)" | wc -l
```

### Step 2: Fetch Recent Wiki Commits

**CRITICAL:** Check wiki commits independently - authors may update the wiki but not mention it in the PR.

#### Clone/Update Wiki Repository

```bash
# For inav wiki
cd /path/to/workspace

# Clone wiki if not already present
if [ ! -d "inav.wiki" ]; then
    git clone https://github.com/iNavFlight/inav.wiki.git
fi

cd inav.wiki
git pull origin master

# Get recent commits (last 7 days)
git log --since="7 days ago" --pretty=format:"%H|%an|%ae|%ai|%s" --all
```

#### Parse Wiki Commits

```bash
# Get wiki commits with details
git log --since="7 days ago" \
    --pretty=format:"%H|%an|%ae|%ai|%s" \
    --all > /tmp/wiki_commits.txt

# Example output format:
# abc123|John Doe|john@example.com|2025-12-21 14:30:00|Updated Navigation docs for PR #1234
```

#### Extract PR References from Wiki Commits

```bash
# Look for PR numbers in wiki commit messages
grep -oE "#[0-9]+" /tmp/wiki_commits.txt

# Or more detailed:
while IFS='|' read -r hash author email date message; do
    pr_refs=$(echo "$message" | grep -oE "#[0-9]+")
    if [ -n "$pr_refs" ]; then
        echo "Wiki commit $hash references: $pr_refs"
        echo "  Author: $author"
        echo "  Date: $date"
        echo "  Message: $message"
    fi
done < /tmp/wiki_commits.txt
```

### Step 3: Check Each PR for Documentation

For each PR, check the following indicators of documentation:

#### A. Check Files Modified in PR

```bash
# Get list of files changed in PR
gh pr view <PR_NUMBER> --json files --jq '.files[].path'

# Check if any docs/ files were modified
gh pr view <PR_NUMBER> --json files --jq '.files[].path' | grep -i "docs/"

# Check for README updates
gh pr view <PR_NUMBER> --json files --jq '.files[].path' | grep -i "README"

# Check for wiki-related files
gh pr view <PR_NUMBER> --json files --jq '.files[].path' | grep -i "\.md$"
```

**Documentation indicators (GOOD):**
- Files in `docs/` directory modified
- README files updated
- Markdown files added/updated (may indicate docs)

#### B. Check PR Description for Links

```bash
# Get PR body/description
gh pr view <PR_NUMBER> --json body --jq '.body'

# Look for PR references in description
gh pr view <PR_NUMBER> --json body --jq '.body' | grep -E "#[0-9]+"

# Look for wiki links
gh pr view <PR_NUMBER> --json body --jq '.body' | grep -iE "wiki|documentation"
```

**Documentation indicators (GOOD):**
- Links to other PRs (e.g., "Docs in #1234")
- Links to wiki pages or commits
- Mentions of "documentation", "wiki", "docs updated"
- References like "See inavflight/inav-configurator#5678"

#### C. Check PR Comments

```bash
# Get PR comments
gh api repos/inavflight/inav/pulls/<PR_NUMBER>/comments --jq '.[].body'

# Or for configurator
gh api repos/inavflight/inav-configurator/pulls/<PR_NUMBER>/comments --jq '.[].body'

# Search for documentation mentions
gh api repos/inavflight/inav/pulls/<PR_NUMBER>/comments --jq '.[].body' | grep -iE "wiki|docs|documentation"
```

**Documentation indicators (GOOD):**
- Comments linking to wiki updates
- Comments linking to documentation PRs
- Maintainer confirmation of docs

#### D. **NEW: Cross-Reference with Wiki Commits**

Check if wiki was updated by same author around the same time:

```bash
# Get PR details
PR_NUM=1234
pr_author=$(gh pr view $PR_NUM --json author --jq '.author.login')
pr_merged=$(gh pr view $PR_NUM --json mergedAt --jq '.mergedAt')
pr_created=$(gh pr view $PR_NUM --json createdAt --jq '.createdAt')

# Search wiki commits by author
cd inav.wiki
git log --since="7 days ago" --author="$pr_author" --pretty=format:"%ai|%s"

# Search wiki commits mentioning this PR number
git log --since="7 days ago" --grep="#$PR_NUM" --pretty=format:"%H|%an|%ai|%s"

# Search wiki commits in time window (±2 days of PR merge)
# This catches wiki updates made around the same time as the PR
git log --since="$(date -d "$pr_merged - 2 days" +%Y-%m-%d)" \
        --until="$(date -d "$pr_merged + 2 days" +%Y-%m-%d)" \
        --author="$pr_author" \
        --pretty=format:"%ai|%s"
```

**Wiki matching strategies:**

1. **Direct PR reference:** Wiki commit message mentions "#1234"
2. **Author + time match:** Same author committed to wiki within ±2 days of PR
3. **Topic match:** Wiki commit message mentions related keywords from PR title

```bash
# Example: Check if wiki commit topics match PR
pr_title=$(gh pr view $PR_NUM --json title --jq '.title')

# Extract key terms from PR title (e.g., "GPS", "navigation", "OSD")
key_terms=$(echo "$pr_title" | grep -oE "[A-Z]{2,}|navigation|telemetry|OSD|CLI" | tr '\n' '|' | sed 's/|$//')

# Search wiki for those terms
cd inav.wiki
git log --since="7 days ago" --grep="$key_terms" -i --pretty=format:"%H|%an|%ai|%s"
```

### Step 4: Assess If Documentation Is Needed

If no documentation indicators found, evaluate whether docs are likely needed based on:

#### Changes Likely Needing Documentation:

**Firmware (inav):**
- New features or modes
- New CLI commands or settings
- New MSP messages
- Changes to flight behavior
- New sensor support
- Navigation changes
- Changes affecting users (not just internal refactoring)

**Configurator:**
- New UI features or tabs
- New settings/configuration options
- Changes to user workflows
- New tooltips or help text
- Feature additions visible to users

#### Changes NOT Needing Documentation:

- Internal refactoring (no user-visible changes)
- Code cleanup or formatting
- Dependency updates (unless user-facing)
- Build system changes (unless affecting developers)
- Test additions/fixes
- Bug fixes (minor, no behavior change)
- CI/workflow updates

### Step 5: Check File Contents for Clues

```bash
# View the actual diff to understand changes
gh pr diff <PR_NUMBER>

# Check specific files
gh pr diff <PR_NUMBER> | grep "^+" | head -20
```

Look for:
- New CLI commands (`cliXXX`, `pgRegistry`)
- New MSP messages (`MSP_`, `MSP2_`)
- New settings structures
- UI component additions
- Feature flag additions

### Step 6: Generate Report

Create a summary report with:

```markdown
## PR Documentation Check - YYYY-MM-DD

### Repository: inav

#### PRs with Documentation ✅

- #1234 - "Add new flight mode" - docs/ files modified
- #1235 - "Update GPS settings" - links to wiki PR
- #1236 - "Add telemetry feature" - wiki commit found (abc123, same author, ±1 day)
- #1237 - "Fix OSD layout" - wiki commit references #1237

#### PRs Needing Documentation Review ⚠️

- #1238 - "Add new CLI command 'set gps_mode'"
  - Reason: New user-facing CLI command, no docs found
  - Wiki check: No commits by author in time window
  - Action needed: Tag as "documentation needed"?

- #1239 - "Add RTH altitude preset"
  - Reason: New user-visible feature, no docs found
  - Wiki check: No related wiki commits found
  - Action needed: Tag as "documentation needed"?

#### PRs Not Needing Documentation ℹ️

- #1240 - "Refactor PID controller code" - Internal refactoring only
- #1241 - "Update GitHub Actions workflow" - CI changes only
- #1242 - "Fix typo in comment" - Code comment fix

### Repository: inav-configurator

(Similar structure)

### Wiki Commits Summary

**Total wiki commits (last 7 days):** 12

**Commits with PR references:**
- abc123 - "Updated Navigation.md for #1234" (matched to PR #1234 ✅)
- def456 - "OSD documentation #1237" (matched to PR #1237 ✅)

**Commits without PR references (by author/time):**
- ghi789 - "Updated telemetry docs" by user123, 2025-12-22 (matched to PR #1236 by author/time ✅)

**Unmatched wiki commits:**
- jkl012 - "Fix typo in GPS.md" (minor fix, no PR needed)
```

## Complete Workflow Script

Here's a complete workflow you can follow:

```bash
#!/bin/bash

# Check PR documentation for last week

echo "=== PR Documentation Check ==="
echo "Date: $(date)"
echo ""

# Step 1: Update wiki repositories
echo "=== Updating Wiki Repositories ==="
for wiki_repo in inav.wiki inav-configurator.wiki; do
    if [ -d "$wiki_repo" ]; then
        cd "$wiki_repo"
        git pull origin master
        cd ..
    else
        if [ "$wiki_repo" = "inav.wiki" ]; then
            git clone https://github.com/iNavFlight/inav.wiki.git
        elif [ "$wiki_repo" = "inav-configurator.wiki" ]; then
            git clone https://github.com/iNavFlight/inav-configurator.wiki.git
        fi
    fi
done
echo ""

# Step 2: Get wiki commits
echo "=== Recent Wiki Commits ==="
cd inav.wiki
echo "## inav.wiki commits (last 7 days):"
git log --since="7 days ago" --pretty=format:"%H|%an|%ai|%s" --all > /tmp/inav_wiki_commits.txt
cat /tmp/inav_wiki_commits.txt
echo ""
cd ..

cd inav-configurator.wiki
echo "## inav-configurator.wiki commits (last 7 days):"
git log --since="7 days ago" --pretty=format:"%H|%an|%ai|%s" --all > /tmp/configurator_wiki_commits.txt
cat /tmp/configurator_wiki_commits.txt
echo ""
cd ..

# Step 3: Check PRs in each repo
for repo in inav inav-configurator; do
    echo "### Repository: $repo"
    echo ""

    cd "$repo"

    # Determine wiki file
    if [ "$repo" = "inav" ]; then
        wiki_commits="/tmp/inav_wiki_commits.txt"
    else
        wiki_commits="/tmp/configurator_wiki_commits.txt"
    fi

    # Get PRs from last week
    prs=$(gh pr list --state all --search "created:>=$(date -d '7 days ago' +%Y-%m-%d)" --json number --jq '.[].number')

    if [ -z "$prs" ]; then
        echo "No PRs in last 7 days"
        echo ""
        cd ..
        continue
    fi

    for pr in $prs; do
        echo "#### PR #$pr"

        # Get PR details
        pr_data=$(gh pr view $pr --json title,author,mergedAt,createdAt,state)
        title=$(echo "$pr_data" | jq -r '.title')
        author=$(echo "$pr_data" | jq -r '.author.login')
        merged=$(echo "$pr_data" | jq -r '.mergedAt')
        created=$(echo "$pr_data" | jq -r '.createdAt')
        state=$(echo "$pr_data" | jq -r '.state')

        echo "Title: $title"
        echo "Author: $author"
        echo "State: $state"

        has_docs=false

        # Check for docs files in PR
        docs_files=$(gh pr view $pr --json files --jq '.files[].path' | grep -iE "docs/|README|\.md$" || true)
        if [ -n "$docs_files" ]; then
            echo "✅ Has documentation files in PR"
            echo "$docs_files"
            has_docs=true
        fi

        # Check PR body for references
        body=$(gh pr view $pr --json body --jq '.body')
        wiki_refs=$(echo "$body" | grep -iE "wiki|#[0-9]+|documentation" || true)
        if [ -n "$wiki_refs" ]; then
            echo "✅ Has documentation references in PR description"
            has_docs=true
        fi

        # Check wiki commits for PR reference
        wiki_pr_refs=$(grep "#$pr" "$wiki_commits" || true)
        if [ -n "$wiki_pr_refs" ]; then
            echo "✅ Wiki commit references this PR:"
            echo "$wiki_pr_refs"
            has_docs=true
        fi

        # Check wiki commits by same author in time window
        if [ "$state" = "MERGED" ] && [ "$merged" != "null" ]; then
            # Check ±2 days from merge
            wiki_author_commits=$(grep "$author" "$wiki_commits" || true)
            if [ -n "$wiki_author_commits" ]; then
                echo "✅ Wiki commits by same author (check time proximity):"
                echo "$wiki_author_commits"
                has_docs=true
            fi
        fi

        if [ "$has_docs" = false ]; then
            echo "⚠️ No documentation found - needs review"
        fi

        echo ""
    done

    cd ..
done

echo "=== Check Complete ==="
```

## Wiki Commit Matching Logic

### Priority 1: Direct PR Reference

```bash
# Wiki commit message contains "#1234"
grep "#$PR_NUM" /tmp/wiki_commits.txt
```

**Confidence:** HIGH - Explicit link

### Priority 2: Author + Time Window

```bash
# Same author, within ±2 days of PR merge
pr_merge_date="2025-12-22"
author="john_doe"

# Check if any commits match
git log --since="$(date -d "$pr_merge_date - 2 days" +%Y-%m-%d)" \
        --until="$(date -d "$pr_merge_date + 2 days" +%Y-%m-%d)" \
        --author="$author" \
        --pretty=format:"%ai|%s"
```

**Confidence:** MEDIUM - Likely related if timing matches

### Priority 3: Topic/Keyword Match

```bash
# PR title: "Add GPS altitude hold feature"
# Look for wiki commits mentioning "GPS" or "altitude"

pr_title="Add GPS altitude hold feature"
keywords=$(echo "$pr_title" | grep -oE "[A-Za-z]{3,}" | sort -u | tr '\n' '|' | sed 's/|$//')

git log --since="7 days ago" \
        --grep="$keywords" -i \
        --pretty=format:"%H|%an|%ai|%s"
```

**Confidence:** LOW - May be coincidental, needs human review

## Implementation Notes

### Wiki Repository Locations

```bash
# Clone wiki repos if not present
git clone https://github.com/iNavFlight/inav.wiki.git
git clone https://github.com/iNavFlight/inav-configurator.wiki.git

# Standard locations in workspace
~/Documents/planes/inavflight/inav.wiki/
~/Documents/planes/inavflight/inav-configurator.wiki/
```

### Date Calculation

Different systems may need different date commands:

```bash
# Linux
date -d '7 days ago' +%Y-%m-%d
date -d "$some_date - 2 days" +%Y-%m-%d

# macOS
date -v-7d +%Y-%m-%d
date -j -f "%Y-%m-%d" "$some_date" -v-2d +%Y-%m-%d
```

### Handling Email vs. GitHub Username

Wiki commits may use email addresses while GitHub PRs use usernames:

```bash
# Get both from PR
gh pr view $PR_NUM --json author --jq '.author.login'  # GitHub username
gh pr view $PR_NUM --json commits --jq '.commits[0].commit.author.email'  # Email from commit

# Search wiki by either
git log --author="username_or_email"
```

## Common Scenarios

### Scenario 1: PR with docs/ files

```
PR #1234 - "Add GPS altitude hold"
Files changed:
  - src/main/navigation/navigation_pos_estimator.c
  - docs/Navigation.md ✅

Result: ✅ Documentation included
Action: None needed
```

### Scenario 2: PR with Wiki commit reference

```
PR #1235 - "Add new telemetry fields"
Files changed:
  - src/main/telemetry/crsf.c
Wiki commits:
  - abc123: "Updated Telemetry.md for #1235" ✅

Result: ✅ Wiki updated and linked
Action: None needed
```

### Scenario 3: PR with Wiki commit by author (no reference)

```
PR #1236 - "Add OSD element" by user_alice
Merged: 2025-12-22
Files changed:
  - src/main/io/osd.c
Wiki commits:
  - def456: "Updated OSD.md" by user_alice, 2025-12-22 ✅

Result: ✅ Wiki likely updated (author/time match)
Action: Verify this is the related update
```

### Scenario 4: Feature PR without any docs

```
PR #1237 - "Add new CLI command"
Files changed:
  - src/main/cli/settings.c
No docs/ changes, no wiki references
Wiki commits: None by author in time window ⚠️

Result: ⚠️ Likely needs documentation
Action: Ask user to tag as "documentation needed"
```

### Scenario 5: Refactoring PR

```
PR #1238 - "Refactor PID loop structure"
Files changed:
  - src/main/flight/pid.c (internal refactoring)
No user-visible changes ℹ️

Result: ℹ️ No documentation needed
Action: Note as internal change only
```

## Tips for Effective Checking

1. **Always check wiki independently** - Don't rely on PR mentions
2. **Match by author + time** - Often more reliable than PR references
3. **Read PR titles carefully** - Often indicate if user-facing
4. **Check PR labels** - May already be tagged
5. **Look at file paths** - `src/main/` often user-facing, `lib/` usually not
6. **Search for keywords** - "CLI", "MSP", "OSD", "setting" indicate user features
7. **Check wiki commit dates** - May be before OR after PR merge

## Output Format

Generate a structured report for the user:

```markdown
# PR Documentation Check Report
**Date:** 2025-12-28
**Period:** Last 7 days

## Summary
- Total PRs checked: 15
- PRs with documentation: 8 ✅
  - With docs/ files: 3
  - With PR-referenced wiki commits: 2
  - With author-matched wiki commits: 3
- PRs needing doc review: 4 ⚠️
- PRs not needing docs: 3 ℹ️

## Wiki Activity Summary
- Total wiki commits: 12
- Wiki commits with PR refs: 5 (matched to PRs)
- Wiki commits matched by author/time: 3
- Unmatched wiki commits: 4 (typo fixes, minor updates)

## Detailed Findings

[Details for each PR category]

## Recommended Actions

[List of PRs to tag, with reasons]
```

## Related Skills

- **pr-review** - Review PR code and comments
- **git-workflow** - Manage git operations for PRs
- **wiki-search** - Search wiki for related documentation
- **check-builds** - Verify PR builds pass

---

**Note:** This is a manager skill for tracking documentation compliance. The manager should run this periodically to ensure PRs include appropriate documentation.
