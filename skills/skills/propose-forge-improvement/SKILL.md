---
name: propose-forge-improvement
description: Propose improvements or new components for Product Forge
argument-hint: "[--save]"
---

# Propose Forge Improvement

Retrospect on the current session and propose improvements to Product Forge - either enhancing existing components or suggesting new ones.

## Purpose

After working with Product Forge skills, commands, or agents, identify opportunities to improve the ecosystem based on real usage patterns.

## Usage

```bash
/propose-forge-improvement        # Analyze and propose improvements
/propose-forge-improvement --save # Save proposal to ~/.claude/learnings/
```

## Decision Flow

```
Analyze session for Product Forge opportunities
                    ↓
┌─────────────────────────────────────────────┐
│ Could an existing component be improved?    │
│                                             │
│ Check:                                      │
│ - Skills used → Missing guidance?           │
│ - Commands run → Missing options?           │
│ - Agents spawned → Missing capabilities?    │
│ - Docs referenced → Outdated/incomplete?    │
└─────────────────────────────────────────────┘
                    ↓
         ┌─────────┴─────────┐
         ↓                   ↓
   Improvement          New Component
   to existing          proposal
```

## Execution Instructions

When the user runs this command:

### 1. Identify Product Forge Usage

Scan the session for:

- **Skills referenced** - Which skills were applied or mentioned?
- **Commands executed** - Which /commands were run?
- **Agents spawned** - Which Task agents were used?
- **Patterns observed** - Reusable workflows or code structures?
- **Friction points** - Where did existing tools fall short?

### 2. Check for Improvement Opportunities

For each identified component, ask:

| Question | If Yes → |
|----------|----------|
| Missing guidance in a skill? | Skill improvement |
| Missing option in a command? | Command improvement |
| Missing capability in an agent? | Agent improvement |
| Outdated information in docs? | Doc improvement |
| Workflow that could be automated? | New command |
| Knowledge that should be applied automatically? | New skill |
| Complex task needing specialized agent? | New agent |

### 3. Locate Existing Components

If proposing an improvement, find the target:

```bash
# Search Product Forge for existing components
find ~/.claude/plugins/cache -name "*.md" | xargs grep -l "{component-name}" 2>/dev/null
```

Or reference known locations:
- Skills: `plugins/{plugin}/skills/{skill-name}/SKILL.md`
- Commands: `plugins/{plugin}/commands/{command-name}.md`
- Agents: `plugins/{plugin}/agents/{agent-name}.md`

### 4. Generate Proposal

#### For Improvements to Existing Components

```markdown
# Proposed Improvement to Product Forge

## Target Component

**Type**: skill | command | agent | doc
**Location**: plugins/python-experts/skills/django-api/SKILL.md
**Component**: django-api skill

## Current Gap

The django-api skill covers endpoint creation but lacks guidance on:
- Pagination patterns for large datasets
- Cursor-based vs offset pagination trade-offs
- Integration with Django REST Framework pagination classes

## Observed Need

During this session, we implemented pagination for a user listing endpoint.
Had to research DRF pagination classes manually - this knowledge should be
in the skill.

## Suggested Addition

Add a "Pagination Patterns" section:

```python
# Cursor-based pagination (preferred for large datasets)
class UserPagination(CursorPagination):
    page_size = 50
    ordering = '-created_at'

# Offset pagination (simpler, but slower for deep pages)
class UserPagination(PageNumberPagination):
    page_size = 50
    max_page_size = 100
```

## Impact

- Reduces research time for common pagination needs
- Ensures consistent pagination patterns across projects
- Covers both DRF approaches with trade-off guidance
```

#### For New Components

```markdown
# Proposed New Component for Product Forge

## Component Type

**Type**: skill | command | agent
**Suggested Name**: migration-safety
**Target Plugin**: python-experts

## Problem Statement

When modifying Django models, there's risk of creating migrations that:
- Lock tables for extended periods
- Cause data loss
- Break backwards compatibility

No current skill covers migration safety patterns.

## Proposed Solution

### If Skill

Create `migration-safety` skill that Claude applies when:
- Modifying Django models
- Creating or reviewing migrations
- Planning database schema changes

Key guidance:
- Additive-only changes for zero-downtime
- Separate deploy for column removal
- Index creation with CONCURRENTLY

### If Command

Create `/check-migration` command that:
- Analyzes pending migrations for safety issues
- Flags risky operations (column drops, type changes)
- Suggests safer alternatives

### If Agent

Create `migration-reviewer` agent that:
- Reviews migration files
- Checks for backwards compatibility
- Suggests deployment order

## Evidence from Session

[What happened in the session that prompted this suggestion]
```

### 5. Handle --save Flag

If `--save` is provided:

1. **Determine type**:
   - `improvement` → existing component enhancement
   - `skill-idea` / `command-idea` / `agent-idea` → new component

2. **Save to appropriate location**:
   ```bash
   mkdir -p ~/.claude/learnings/projects/{project-slug}/feedback/{type}/
   # Save as: {type}-{timestamp}.md
   ```

3. **Confirm**:
   ```
   Proposal saved to ~/.claude/learnings/projects/{project-slug}/feedback/improvement/

   Review with: /sync-feedback --review
   ```

### 6. Offer Next Steps

```
Next steps:
  [1] Create/modify the component now (I'll help implement)
  [2] Save for later review (/propose-forge-improvement --save)
  [3] Open GitHub issue (if Product Forge repo accessible)
  [4] Dismiss

Select option:
```

## Quality Criteria

Only propose improvements that are:

| Criterion | Description |
|-----------|-------------|
| **Evidence-based** | Rooted in actual session experience |
| **Generalizable** | Useful beyond this specific project |
| **Non-trivial** | Meaningful improvement, not minor tweaks |
| **Actionable** | Clear enough to implement |
| **Scoped** | One focused improvement per proposal |

## Priority Order

When multiple opportunities exist, prioritize:

1. **Improvements to existing** - Lower friction, higher impact
2. **New skills** - Knowledge that applies automatically
3. **New commands** - User-invoked workflows
4. **New agents** - Complex specialized tasks

## Notes

- Complements `/propose-project-learning` which targets project CLAUDE.md
- Works with `/sync-feedback` for batch review and export
- Integrates with feedback hooks system for automatic capture
- Product Forge maintainers review submitted proposals
