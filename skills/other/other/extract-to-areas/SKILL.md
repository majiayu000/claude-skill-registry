---
name: extract-to-areas
description: Extract synthesized content to semantic Area notes (People, Projects, Insights). Prepares structured updates for review rituals to apply via update-semantic.
disable-model-invocation: true
allowed-tools: Read, Bash(ls)
---

# Extract to Areas Sub-Skill

Analyzes review synthesis data and prepares semantic note updates for People, Projects, and Insights files.

## Input Arguments

Arguments are passed as key-value pairs:
- `vault`: Path to the vault
- `scope`: "day" or "week" (affects summary depth)
- `people`: Array of `[[PersonName]]` references to process
- `projects`: Array of `[[project-name]]` references to process
- `insights`: Synthesized insights from the review
- `context`: Full context data (daily or weekly aggregates)

## Instructions

### 1. Process People

For each person in `people` array:

#### 1.1 Find Person File
```bash
ls "$VAULT/02_Areas/People/"*.md | grep -i "{person_name}"
```

If not found:
- Log: "Person file not found for {person}"
- Add to `skipped` with suggestion to create

#### 1.2 Gather Interactions

From context, compile all interactions with this person:
- Meeting dates and topics (from meetings sections)
- Notable moments from wins/insights mentioning them
- Follow-up items if any

#### 1.3 Prepare Update

Format for `update-semantic`:
```json
{
  "type": "person",
  "path": "02_Areas/People/{Name}.md",
  "section": "Interactions",
  "content": "{date_range}: {summary of interactions}"
}
```

**For weekly scope:**
```
2026-W07 (Feb 9-13): 3 conversations about career growth. Key moment: discussed tech lead path. She's energized about Q2 opportunities.
```

**For daily scope:**
```
2026-02-14: 1:1 focused on career growth. Discussed tech lead path interest.
```

### 2. Process Projects

For each project in `projects` array:

#### 2.1 Find Project File
```bash
ls "$VAULT/01_Projects/"*{project_name}*.md
```

If not found:
- Log: "Project file not found for {project}"
- Add to `skipped`

#### 2.2 Gather Progress

From context, compile all mentions:
- Strategic wins related to project
- Priority completions mentioning project
- Blockers resolved or discovered

#### 2.3 Prepare Update

```json
{
  "type": "project",
  "path": "01_Projects/{project-file}.md",
  "section": "Progress",
  "content": "{date_range}: {summary of progress}"
}
```

**For weekly scope:**
```
2026-W07: API design completed (Mon). Integration tests passing (Wed). Ready for staging deployment next week.
```

**For daily scope:**
```
2026-02-14: API design finalized, tests written for core endpoints.
```

### 3. Process Insights

For each insight in `insights`:

#### 3.1 Categorize Insight

Determine if it connects to an existing Insight note by:
- Keyword matching against Insight filenames in `02_Areas/Insights/`
- Theme analysis (leadership, delegation, productivity, focus, boundaries, etc.)

```bash
ls "$VAULT/02_Areas/Insights/"*.md
```

#### 3.2 Find or Flag

**If matches existing Insight file:**
```json
{
  "type": "insight",
  "path": "02_Areas/Insights/{topic}.md",
  "section": "Evidence",
  "content": "{date}: {insight content}"
}
```

**If new insight theme (no match):**
```json
{
  "type": "insight",
  "path": null,
  "action": "suggest_new",
  "suggested_name": "{kebab-case-topic}.md",
  "content": "{insight content}",
  "reason": "No existing Insight note matches this theme"
}
```

### 4. Return Structured Result

**Success:**
```json
{
  "success": true,
  "scope": "week",
  "date_range": "2026-W07",
  "updates": [
    {
      "type": "person",
      "path": "02_Areas/People/SarahK.md",
      "section": "Interactions",
      "content": "2026-W07 (Feb 9-13): 3 conversations about career growth. Key moment: discussed tech lead path. She's energized about Q2 opportunities."
    },
    {
      "type": "person",
      "path": "02_Areas/People/MarcusT.md",
      "section": "Interactions",
      "content": "2026-W07 (Feb 9-13): 2 syncs on platform migration. Great collaboration on API design—he's ramping up well."
    },
    {
      "type": "project",
      "path": "01_Projects/2026-03-15-platform-migration.md",
      "section": "Progress",
      "content": "2026-W07: API design completed (Mon). Integration tests passing (Wed). Ready for staging next week."
    },
    {
      "type": "insight",
      "path": "02_Areas/Insights/delegation.md",
      "section": "Evidence",
      "content": "2026-W07: Multiple successful delegation instances this week. Key learning: 'Delegation creates capacity'—when I hand off clearly, I get focused time back."
    }
  ],
  "skipped": [
    {
      "type": "person",
      "name": "[[NewHire]]",
      "reason": "file_not_found",
      "suggestion": "Create People file: 02_Areas/People/NewHire.md"
    }
  ],
  "new_insights": [
    {
      "suggested_name": "sustainable-pace.md",
      "content": "Realized that consistent energy matters more than sprints. The week was productive because I maintained boundaries, not despite them.",
      "reason": "No existing Insight note about pace/sustainability"
    }
  ],
  "summary": {
    "people_updates": 2,
    "project_updates": 1,
    "insight_updates": 1,
    "skipped": 1,
    "new_suggestions": 1
  }
}
```

**No Updates Needed:**
```json
{
  "success": true,
  "scope": "week",
  "date_range": "2026-W07",
  "updates": [],
  "skipped": [],
  "new_insights": [],
  "message": "No semantic updates to generate—no entities found in context.",
  "summary": {
    "people_updates": 0,
    "project_updates": 0,
    "insight_updates": 0,
    "skipped": 0,
    "new_suggestions": 0
  }
}
```

For backwards compatibility, also output human-readable summary:
```
Semantic Updates Prepared for 2026-W07

People (2):
- SarahK.md → Interactions: 3 conversations about career growth
- MarcusT.md → Interactions: 2 syncs on platform migration

Projects (1):
- platform-migration.md → Progress: API complete, tests passing

Insights (1):
- delegation.md → Evidence: "Delegation creates capacity"

Skipped (1):
- NewHire: file not found (suggest creating)

New Insight Suggestions (1):
- sustainable-pace.md: "Consistent energy > sprints"
```

## Design for Reuse

This sub-skill is designed to be called by:
- **daily-review**: Extract daily learnings to semantic notes (scope=day)
- **weekly-review**: Extract weekly synthesis to semantic notes (scope=week)
- **monthly-review**: Extract monthly patterns to semantic notes (scope=month)

The `scope` parameter controls the granularity of generated summaries:
- `day`: Specific dated entry
- `week`: Summarized with date range
- `month`: High-level themes and patterns

## Section Targeting

Updates target specific sections in semantic notes:

| Note Type | Target Section | Expected Format |
|-----------|----------------|-----------------|
| People | `## Interactions` | Dated entries with context |
| Projects | `## Progress` | Dated milestone/status entries |
| Insights | `## Evidence` | Dated observations supporting the insight |

If the target section doesn't exist, the update will be flagged for manual review.
