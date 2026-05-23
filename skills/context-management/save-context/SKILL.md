---
name: save-context
description: |
  Save important session context to MCP memory before compaction. This skill
  should be used when: (1) Claude detects the conversation is getting long,
  (2) Before starting a risky operation, (3) After completing significant work,
  (4) User requests context preservation. Triggers: "save context", "preserve
  session", "remember this", "before we lose context", "context getting long".
---

# Save Context

## Overview

This skill saves important session context to MCP memory, ensuring critical
information survives context compaction. Use proactively when conversations get
long or before significant work is lost.

## When to Use

- **Approaching compaction** - Conversation has been long with many tool calls
- **Completed milestone** - Just finished implementing a feature or fix
- **Complex decisions** - Made architectural choices that should persist
- **User request** - User explicitly asks to save/preserve context
- **Before risky operations** - About to make breaking changes

## Workflow

To save context to MCP memory:

### Step 1: Gather Context

Collect key information to preserve:

1. **Current task status** - What was being worked on
2. **Decisions made** - Key choices and their rationale
3. **Files modified** - Recent changes and their purpose
4. **Blockers/issues** - Unresolved problems
5. **Next steps** - What should happen next

### Step 2: Create Entities

Use `mcp__memory__create_entities()` to save structured data:

```javascript
// Example entities to create
entities = [
  {
    name: "Session_2026-01-28_TaskName",
    entityType: "session_context",
    observations: [
      "Working on: [task description]",
      "Completed: [what was done]",
      "Decision: [key choice made]",
      "Files: [files modified]",
      "Next: [pending work]",
    ],
  },
  {
    name: "Decision_FeatureName",
    entityType: "architectural_decision",
    observations: [
      "Context: [why this came up]",
      "Options considered: [list]",
      "Chosen: [option]",
      "Rationale: [why]",
    ],
  },
];
```

### Step 3: Create Relations

Link related entities:

```javascript
// Example relations
relations = [
  {
    from: "Session_2026-01-28_TaskName",
    relationType: "decided",
    to: "Decision_FeatureName",
  },
];
```

### Step 4: Confirm Save

After saving, confirm what was preserved:

```
Saved to MCP memory:
- Session context: [summary]
- Decisions: [count]
- Relations: [count]

To retrieve later: mcp__memory__read_graph()
```

## Entity Types

| Type                     | Use For                                    |
| ------------------------ | ------------------------------------------ |
| `session_context`        | Current work status, progress, next steps  |
| `architectural_decision` | Design choices with rationale              |
| `bug_investigation`      | Debugging context, findings, hypotheses    |
| `feature_implementation` | Feature details, approach, progress        |
| `user_preference`        | User's stated preferences and requirements |

## Naming Conventions

- **Sessions**: `Session_YYYY-MM-DD_BriefTaskName`
- **Decisions**: `Decision_FeatureName_Choice`
- **Bugs**: `Bug_ComponentName_Issue`
- **Features**: `Feature_FeatureName`

## Best Practices

1. **Save early, save often** - Don't wait until context is about to compact
2. **Be concise** - MCP memory has limits; focus on key information
3. **Use clear names** - Entity names should be searchable and meaningful
4. **Link entities** - Relations help reconstruct context later
5. **Include next steps** - Future sessions need to know what's pending

## Context Size Indicators

Watch for these signs that context is getting large:

- **Many tool calls** - 50+ tool uses in the session
- **Large file reads** - Multiple large files read
- **Long conversation** - Many back-and-forth exchanges
- **Complex task** - Multi-step implementation with decisions

When you see these, proactively suggest using `/save-context`.
