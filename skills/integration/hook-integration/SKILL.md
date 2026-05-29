---
name: hook-integration
description: Comprehensive guide to integrating skills with Claude Code's 12 hook events. Use when creating hook-aware skills for harnesses like Clausitron, or when needing hook response schemas and patterns.
---

# Hook Integration for Skills

Skills can be designed to work with Claude Code's 12 hook events, enabling deep integration with harnesses like Clausitron.

## Available Hook Events

| Hook Event | When It Fires | Skill Integration Opportunity |
|------------|---------------|-------------------------------|
| `PreToolUse` | Before any tool executes | Validation skills, policy enforcement |
| `PostToolUse` | After tool execution | Logging skills, result enrichment |
| `PostToolUseFailure` | When a tool fails | Error analysis skills, recovery suggestions |
| `UserPromptSubmit` | When user sends prompt | Context injection, prompt enhancement |
| `SessionStart` | Session begins | Environment setup, context loading |
| `SessionEnd` | Session ends | Summary generation, cleanup |
| `SubagentStart` | Subagent spawns | Budget allocation, tracking |
| `SubagentStop` | Subagent completes | Result aggregation, cost tracking |
| `Stop` | Agent stops | State persistence, handoff notes |
| `PreCompact` | Before context compaction | Archive important context |
| `PermissionRequest` | Permission dialog triggered | Policy-based auto-decisions |
| `Notification` | Agent status messages | External notifications (Slack, etc.) |

## Hook-Aware Skill Patterns

### Pattern 1: Validation Skill (PreToolUse)

Skills that validate operations before they execute:

```markdown
---
name: security-validator
description: Validates file operations for security compliance. Use with PreToolUse hook.
---

# Security Validator

## Hook Integration
This skill provides validation logic for PreToolUse hooks.

## Validation Rules

### File Write Validation
When `tool_name` is `Write` or `Edit`:
1. Check `file_path` against blocked patterns:
   - `*.env*` - Environment files with secrets
   - `*credentials*` - Credential files
   - `**/config/production/**` - Production configs
2. Return `permissionDecision: 'deny'` if blocked

### Bash Command Validation
When `tool_name` is `Bash`:
1. Parse `command` for dangerous patterns:
   - `rm -rf /` or `rm -rf ~`
   - `curl | bash` or `wget | sh`
   - Commands with `--force` on production paths
2. Return `permissionDecision: 'ask'` for review
```

### Pattern 2: Context Injection Skill (SessionStart/UserPromptSubmit)

Skills that enrich context at key moments:

```markdown
---
name: project-context
description: Injects project-specific context at session start. Use with SessionStart hook.
---

# Project Context Injector

## Hook Integration
Responds to SessionStart and UserPromptSubmit hooks.

## Context Injection

### On SessionStart
Read and inject:
- Active sprint goals from `docs/SPRINT.md`
- Recent changes from `git log --oneline -10`
- Known issues from `docs/KNOWN_ISSUES.md`

### On UserPromptSubmit
Analyze prompt for keywords and inject relevant:
- API documentation for mentioned endpoints
- Schema definitions for mentioned models
- Test patterns for mentioned components
```

### Pattern 3: Summary Skill (SessionEnd/Stop)

Skills that generate summaries when sessions end:

```markdown
---
name: session-summarizer
description: Generates session summaries on completion. Use with SessionEnd hook.
---

# Session Summarizer

## Hook Integration
Responds to SessionEnd and Stop hooks.

## Summary Generation

### Session Summary Format
```json
{
  "session_id": "{from hook input}",
  "duration_minutes": "{calculated}",
  "files_modified": ["{list from git status}"],
  "key_accomplishments": ["{extracted from conversation}"],
  "open_questions": ["{unresolved items}"],
  "next_steps": ["{suggested follow-ups}"]
}
```

### Storage
Write summaries to:
- `.claude/session-summaries/{session_id}.json`
- Update `.claude/HANDOFF.md` with latest summary
```

### Pattern 4: Cost Tracking Skill (SubagentStart/SubagentStop)

Skills that monitor resource usage:

```markdown
---
name: cost-tracker
description: Tracks token usage and costs across subagents. Use with Subagent hooks.
---

# Cost Tracker

## Hook Integration
Responds to SubagentStart and SubagentStop hooks.

## Tracking Logic

### On SubagentStart
Record:
- `agent_id` from hook input
- `agent_type` for categorization
- Start timestamp
- Allocated budget (if applicable)

### On SubagentStop
Calculate:
- Token usage from result message
- Cost based on model pricing
- Duration
- Update running totals

### Budget Enforcement
If cumulative cost exceeds threshold:
- Log warning
- Can trigger `permissionDecision: 'deny'` on next PreToolUse
```

## Hook Response Schemas

Skills that integrate with hooks should understand the response format:

```typescript
// PreToolUse can return permission decisions
{
  hookSpecificOutput: {
    hookEventName: 'PreToolUse',
    permissionDecision: 'allow' | 'deny' | 'ask',
    permissionDecisionReason: 'Explanation shown to Claude',
    updatedInput: { /* modified tool input */ }
  }
}

// UserPromptSubmit can add context
{
  hookSpecificOutput: {
    hookEventName: 'UserPromptSubmit',
    additionalContext: 'Context injected into conversation'
  }
}

// SessionStart can add context
{
  hookSpecificOutput: {
    hookEventName: 'SessionStart',
    additionalContext: 'Startup context for Claude'
  }
}

// PostToolUse can add context
{
  hookSpecificOutput: {
    hookEventName: 'PostToolUse',
    additionalContext: 'Context after tool execution'
  }
}

// Any hook can inject system messages
{
  systemMessage: 'Message visible to Claude in conversation'
}

// Any hook can stop execution
{
  continue: false,
  stopReason: 'Why execution stopped'
}
```

## Hook Input Schemas

Each hook receives specific input data:

### PreToolUse Input
```typescript
{
  hook_event_name: 'PreToolUse',
  session_id: string,
  tool_name: string,        // 'Bash', 'Write', 'Edit', etc.
  tool_input: {             // Tool-specific parameters
    command?: string,       // For Bash
    file_path?: string,     // For Write/Edit/Read
    content?: string,       // For Write
    // ... other tool params
  },
  cwd: string,
  transcript_path: string
}
```

### SessionStart Input
```typescript
{
  hook_event_name: 'SessionStart',
  session_id: string,
  source: 'startup' | 'resume' | 'clear' | 'compact',
  cwd: string,
  transcript_path: string
}
```

### SessionEnd Input
```typescript
{
  hook_event_name: 'SessionEnd',
  session_id: string,
  reason: string,  // 'clear', 'logout', 'prompt_input_exit', etc.
  cwd: string,
  transcript_path: string
}
```

### SubagentStart Input
```typescript
{
  hook_event_name: 'SubagentStart',
  session_id: string,
  agent_id: string,
  agent_type: string,
  cwd: string,
  transcript_path: string
}
```

### SubagentStop Input
```typescript
{
  hook_event_name: 'SubagentStop',
  session_id: string,
  stop_hook_active: boolean,
  cwd: string,
  transcript_path: string
}
```

## Hook Integration Checklist

When creating hook-aware skills:
- [ ] Identify which hook event(s) the skill responds to
- [ ] Document the expected input schema from the hook
- [ ] Define the response format the skill generates
- [ ] Consider error cases and graceful degradation
- [ ] Test with actual hook invocations if possible
- [ ] Handle missing or malformed input gracefully
- [ ] Return empty `{}` to allow operations by default
