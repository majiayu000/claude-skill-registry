---
name: task-parsing
description: Parses natural language into structured tasks with priority, due date, project, and tags. Use when adding tasks, processing inbox, or when user describes work to be done.
---

# Task Parsing

Convert natural language into structured task format.

## Task Format

```
- [ ] Task description @project #tag !priority ~estimate
```

## Parsing Rules

### Priority Detection
| Input Pattern | Priority |
|--------------|----------|
| "urgent", "ASAP", "critical", "blocking" | `!high` |
| "important", "should", "need to" | `!medium` |
| "when possible", "eventually", "nice to have" | `!low` |

### Time Estimation
| Input Pattern | Estimate |
|--------------|----------|
| "quick", "small", "minor" | `~15m` |
| "short", "simple" | `~30m` |
| "medium", "regular" | `~1h` |
| "large", "significant" | `~2h` |
| "big", "complex", "deep work" | `~4h` |

### Due Date Extraction
| Input Pattern | Action |
|--------------|--------|
| "today", "EOD" | Add to today.md |
| "tomorrow" | Add to today.md with note |
| "this week", "by Friday" | Add to backlog, Do First |
| "next week", "soon" | Add to backlog, Schedule |
| "someday", "eventually" | Add to someday.md |

### Project Detection
- Look for explicit `@project-name` mentions
- Infer from context: "for the API project" → `@api`
- Work-related defaults to `@work`
- Personal items get `#personal` tag

### Tag Extraction
Common tags to apply:
- `#code` - Programming tasks
- `#docs` - Documentation
- `#meeting` - Meetings and calls
- `#research` - Research and learning
- `#bug` - Bug fixes
- `#feature` - New features
- `#review` - Code/document reviews

## Examples

**Input:** "Review John's PR for the auth feature, it's blocking the release"
**Output:** `- [ ] Review John's PR for auth feature @work #review #code !high ~30m`

**Input:** "Eventually learn Kubernetes"
**Output:** `- [ ] Learn Kubernetes #learning !low ~4h` → someday.md

**Input:** "Need to fix the login bug today"
**Output:** `- [ ] Fix login bug @work #bug !high ~1h` → today.md

## Processing Steps

1. Extract the core action (verb + object)
2. Detect priority from urgency words
3. Estimate time from complexity hints
4. Extract or infer project
5. Add relevant tags
6. Determine destination file
7. Format as markdown checkbox
