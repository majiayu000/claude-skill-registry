---
context: fork
---

# ADR Report Skill

## Purpose

Generate comprehensive Architecture Decision Record (ADR) activity reports for a specified time period.

## Usage

- `/adr-report` - All ADR activity (default: last 30 days)
- `/adr-report week` - ADR activity this week
- `/adr-report month` - ADR activity this month
- `/adr-report all` - Complete ADR inventory

## Instructions

When this skill is invoked:

1. **Find all ADRs** in the vault using Glob:

   ```
   ADR*.md
   ```

2. **Read all ADR files** to extract:
   - Title and status (proposed, accepted, deprecated)
   - Created date and modified date
   - Related project(s)
   - Decision summary
   - Key consequences
   - Deciders/stakeholders

3. **Categorize ADRs by status:**
   - Recently Created (within time period)
   - Recently Updated (modified within time period)
   - Proposed (awaiting approval)
   - Accepted (approved and implemented)
   - Deprecated (superseded or no longer valid)

4. **Generate formatted report** with:

### Report Structure

```markdown
# ADR Activity Report

**Period**: [time period]
**Generated**: [current date]

## Summary Statistics

- Total ADRs: [count]
- Accepted: [count]
- Proposed: [count]
- Deprecated: [count]
- Created in period: [count]
- Updated in period: [count]

## Recent ADR Activity

### Created This Period

| ADR             | Status   | Project          | Created    | Deciders |
| --------------- | -------- | ---------------- | ---------- | -------- |
| [[ADR - Title]] | accepted | [[Project Name]] | YYYY-MM-DD | Team     |

### Updated This Period

| ADR             | Status   | Project          | Modified   | Changes        |
| --------------- | -------- | ---------------- | ---------- | -------------- |
| [[ADR - Title]] | accepted | [[Project Name]] | YYYY-MM-DD | Status changed |

## ADRs by Project

### [Project Name]

- [[ADR - Decision 1]] (accepted)
- [[ADR - Decision 2]] (proposed)

## Pending Decisions (Proposed ADRs)

| ADR             | Project     | Created    | Deciders | Next Action       |
| --------------- | ----------- | ---------- | -------- | ----------------- |
| [[ADR - Title]] | [[Project]] | YYYY-MM-DD | Team     | Awaiting approval |

## Recent Key Decisions

### [ADR Title]

**Status**: Accepted
**Project**: [[Project Name]]
**Decision**: Brief summary of what was decided
**Impact**: Key consequences and implications
**Date**: YYYY-MM-DD

## ADRs by Technology Area

- **Cloud/AWS**: 5 ADRs
- **Data Integration**: 3 ADRs
- **Security**: 2 ADRs
- **AI/ML**: 4 ADRs

## Recommendations

- [Any ADRs that need review or updates]
- [ADRs that have been proposed for >30 days without decision]
- [ADRs that may need deprecation]
```

5. **Output the report** as formatted markdown

6. **Optionally save report** by asking user:
   - "Would you like me to save this report as a Page?"
   - If yes, create `Page - ADR Activity Report [date].md`

## Notes

- Focus on architectural significance and business impact
- Highlight decisions that affect multiple projects
- Flag any stale proposed ADRs (>30 days without decision)
- Cross-reference with related projects and meetings
- Use UK English spelling throughout

## Examples

**Example 1:**
User: `/adr-report week`
Assistant: [Generates report for past 7 days showing 3 new ADRs created for NewProductLine and AIIncidentProcessor projects]

**Example 2:**
User: `/adr-report`
Assistant: [Generates default 30-day report showing all ADR activity including VendorTooling ADR completion]

**Example 3:**
User: `/adr-report all`
Assistant: [Generates complete inventory of all ADRs grouped by project and status]
