---
name: pipeline
description: Manage the content pipeline and idea backlog. Use when checking pipeline status, evaluating pillar distribution, reviewing idea statuses, or planning content calendar. Includes idea template, pillar definitions, and frontmatter schemas.
---

# Pipeline Skill

Manage the content pipeline from idea to publication.

## When to Use

- Checking overall pipeline status (`/pipeline` command)
- Reviewing idea backlog and priorities
- Ensuring pillar distribution is on target
- Planning which ideas to draft next
- Creating new ideas with proper structure

## Quick Reference

**Idea statuses:** `idea` → `drafting` → `ready_for_projection` → `published` → `archived`

**Pillar targets:**
- Technology Strategy: 30%
- Leadership & Management: 25%
- Execution & Delivery: 20%
- Founder Lessons: 15%
- Market & AI Trends: 10%

## Context Files

- `context/pillars.md` - Content pillar definitions and targets
- `context/frontmatter.md` - Frontmatter schemas for all file types
- `context/workflow.md` - Status flow and weekly rhythm
- `context/memory.md` - MCP Memory usage for author profile and voice queries

## Templates

- `templates/idea.md` - Idea file template with full frontmatter

## Commands

### /pipeline

Run the pipeline status script to see the current state of all content.

**Usage:**
```bash
npm run pipeline
```

**Output includes:**

1. **Pipeline Status** - Counts of ideas by status (idea, drafting, ready_for_projection, published, archived) plus totals for drafts, posts, LinkedIn posts, and newsletter issues.

2. **Pillar Distribution** - Active ideas by pillar with percentage vs target:
   - ✓ = On target (within 10%)
   - ⚠ = Under target (needs more ideas)
   - ▲ = Over target (pause new ideas)

3. **Stale Items** - Ideas in "drafting" status for 30+ days (based on YYYY-MM in the id)

4. **Suggested Next Actions**:
   - Ideas ready for drafting (have pillar and target_audience)
   - Pillars needing more ideas (>10% under target)
   - Drafts to review for publishing
