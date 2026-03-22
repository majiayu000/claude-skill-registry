---
name: ado-repo-analysis
description: Analyze sibling repos to find best match for a work item
model: sonnet
---

# Repo Analysis Skill

Analyze local repositories to find the best match for a work item based on context.

## Process

1. **List sibling repos**: Find all directories with `.git` in REPOS_BASE_DIR
2. **For each repo**:
   - Pull latest from origin master/main
   - Read README.md and CLAUDE.md if they exist
   - Extract keywords and project descriptions
3. **Score against context**: Compare repo descriptions against:
   - Work item title
   - Work item description/body
   - PR URL hints (if any)
   - Project name from ADO
4. **Output ranked list**: Show repos sorted by confidence score

## Usage

```
/repo-analysis <work-item-context>
```

Example:
```
/repo-analysis "Fix video player buffering issue - relates to player SDK"
```

## Output Format

```
Repo Analysis Results:
1. video-player-sdk (95% match)
   - Keywords: video, player, SDK, streaming
   - Reason: Title mentions "player SDK"

2. media-services (60% match)
   - Keywords: media, transcoding, delivery
   - Reason: Related to video infrastructure

3. web-frontend (30% match)
   - Keywords: React, UI, components
   - Reason: May embed player
```

## Implementation Steps

When invoked:

1. Read REPOS_BASE_DIR from environment or use default `../`
2. List all directories, check for `.git` subdirectory
3. For each git repo:
   - `git fetch origin` (update refs)
   - Read `README.md` first 500 lines
   - Read `CLAUDE.md` if exists
   - Extract: project name, description, key technologies
4. Build keyword index per repo
5. Parse work item context for keywords
6. Score each repo (keyword overlap + description similarity)
7. Return top 5 matches with confidence scores
