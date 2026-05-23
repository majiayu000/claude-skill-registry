---
name: agent-ops-context-map
description: "Analyze the codebase to create a concise, LLM-optimized structured overview in .agent/map.md."
category: analysis
invokes: [agent-ops-state]
invoked_by: [agent-ops-constitution, agent-ops-planning]
state_files:
  read: [focus.md, constitution.md]
  write: [map.md, focus.md]
---

# Context Map Generation

## Purpose
Create a high-level, token-efficient overview of the system (`.agent/map.md`) to allow reasoning about the whole project without reading every file.

## Confidence-Based Staleness Thresholds

**Map freshness requirements scale with confidence level:**

| Confidence | Max Age | Refresh Requirement |
|------------|---------|---------------------|
| LOW | 24 hours | MANDATORY before implementation |
| NORMAL | 7 days | RECOMMENDED if significant changes |
| HIGH | 30 days | OPTIONAL |

### Staleness Check

When invoked (or before low confidence work):

```
📍 CONTEXT MAP STALENESS CHECK

Map file: .agent/map.md
Last updated: {date} ({N} days ago)
Confidence level: {confidence}
Max age for confidence: {threshold}

{If stale:}
⚠️ Context map is STALE for {confidence} confidence work.

For LOW confidence, understanding the codebase is critical.
Refreshing map before proceeding...

{If fresh:}
✅ Context map is current ({N} days old, threshold: {threshold} days)
```

### Low Confidence Refresh Requirements

For LOW confidence work:
1. **Check map age** — if > 24 hours, refresh is MANDATORY
2. **Check for recent changes** — git diff since last map update
3. **Partial refresh option** — focus on affected areas if full refresh is expensive

```
🔄 LOW CONFIDENCE CONTEXT MAP REFRESH

Affected areas for {ISSUE-ID}:
- src/services/ (target of changes)
- src/models/ (dependencies)
- tests/services/ (test coverage)

Refresh options:
1. Full refresh (entire codebase)
2. Partial refresh (affected areas only)
3. Skip (NOT RECOMMENDED for low confidence)

Proceeding with partial refresh...
```

## Procedure
1. **Scan** the file structure (limit to 2-3 levels of depth).
2. **Identify** key architectural elements:
   - Critical configuration files (package.json, pyproject.toml, docker-compose, etc.)
   - Entry points (main.py, index.js, App.tsx)
   - Core modules and their responsibilities.
3. **Summarize** architecture patterns and data flow.
4. **Write/Update** `.agent/map.md` with the following structure:
   - **System Overview**: One paragraph summary of purpose and stack.
   - **Key Components**: List of major modules/folders and what they do.
   - **Patterns**: Architectural decisions (e.g., MVC, Repository pattern, Event-driven).
   - **Key Files**: Table of critical files and their specific role.
   - **Last Updated**: Timestamp for staleness tracking.
5. **Constraint**: Keep the file concise (target < 150 lines). It is a map, not a territory.

## Map Header Template

Include this header in map.md for staleness tracking:

```markdown
# Context Map

**Generated**: {YYYY-MM-DD HH:MM}
**Scope**: {full | partial: areas}
**Confidence**: {confidence level that triggered refresh}

---
```
