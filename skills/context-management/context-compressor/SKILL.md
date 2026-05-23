---
name: context-compressor
description: Context compression and summarization methodology. Techniques for reducing token usage while preserving decision-critical information.
version: 1.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write]
best_practices:
  - Preserve decision-critical information
  - Remove redundant content
  - Use structured formats
  - Maintain traceability
error_handling: graceful
streaming: supported
---

# Context Compressor Skill

<identity>
Context Compressor Skill - Techniques for reducing token usage while preserving decision-critical information. Helps agents work efficiently within context limits.
</identity>

<capabilities>
- Compressing conversation history
- Summarizing code and documentation
- Extracting key decisions and context
- Creating efficient memory snapshots
- Reducing redundancy in context
</capabilities>

<instructions>
<execution_process>

### Step 1: Identify Compressible Content

Content types that can be compressed:

| Type          | Compression Strategy                         |
| ------------- | -------------------------------------------- |
| Code          | Keep signatures, summarize implementations   |
| Conversations | Extract decisions, drop small talk           |
| Documentation | Keep headings and key points                 |
| Errors        | Keep message and location, drop stack frames |
| Logs          | Keep patterns, drop repetitions              |

### Step 2: Apply Compression Techniques

**Technique 1: Decision Extraction**

Before:

```
User: Should we use Redis or Memcached?
Assistant: Let me analyze both options...
[500 words of analysis]
Recommendation: Redis for pub/sub support.
User: Ok let's use Redis.
```

After:

```
Decision: Use Redis (chosen for pub/sub support)
```

**Technique 2: Code Summarization**

Before:

```javascript
// 100 lines of UserService implementation
```

After:

```
UserService: CRUD operations for users
- Methods: create, read, update, delete, findByEmail
- Dependencies: db, validator, logger
- Location: src/services/user.js
```

**Technique 3: Error Compression**

Before:

```
Error: Cannot read property 'id' of undefined
    at UserController.getUser (src/controllers/user.js:45:23)
    at Layer.handle [as handle_request] (node_modules/express/lib/router/layer.js:95:5)
    ... 20 more stack frames
```

After:

```
Error: Cannot read 'id' of undefined @ src/controllers/user.js:45
Cause: User object is null when accessing .id
```

### Step 3: Structure Compressed Output

Use consistent formats:

```markdown
## Session Summary

### Decisions Made

- [D1] Use Redis for caching
- [D2] JWT for authentication

### Files Modified

- src/auth/jwt.js (new)
- src/config/redis.js (updated)

### Open Items

- [ ] Add rate limiting
- [ ] Write tests for JWT
```

### Step 4: Validate Compression

Ensure critical info preserved:

- [ ] All decisions captured
- [ ] Key file locations retained
- [ ] Error causes documented
- [ ] Next steps clear

</execution_process>

<best_practices>

1. **Preserve Decisions**: Never lose decision rationale
2. **Keep Locations**: File paths and line numbers are critical
3. **Summarize, Don't Delete**: Transform verbose content
4. **Use References**: Point to files instead of including content
5. **Test Recovery**: Can you continue work from compressed context?

</best_practices>
</instructions>

<examples>
<usage_example>
**Compression Request**:

```
Compress the last 10 messages for context handoff
```

**Example Response**:

```markdown
## Context Summary (compressed from 10 messages)

### Task

Implementing user authentication with JWT

### Progress

1. Created JWT utility (src/auth/jwt.js)
2. Added login endpoint (src/routes/auth.js)
3. Tests failing - mock issue

### Key Decisions

- Using RS256 for JWT signing (security over performance)
- 1-hour token expiry with refresh tokens

### Current Issue

Jest mock for jwt.sign not working
Location: src/auth/**tests**/jwt.test.js:23

### Next Steps

1. Fix JWT mock
2. Add refresh token endpoint
```

</usage_example>
</examples>

## Rules

- Never lose decision rationale
- Always include file locations
- Test that work can continue from compressed context

## Workflow Integration

This skill supports multi-agent orchestration by enabling efficient context management:

**Router Decision:** `.claude/workflows/core/router-decision.md`

- Router spawns agents that use this skill for context-efficient handoffs
- Used in long-running sessions to maintain continuity

**Artifact Lifecycle:** `.claude/workflows/core/skill-lifecycle.md`

- Compression patterns evolve with framework changes
- Session summaries feed into memory protocol

**Related Workflows:**

- `session-handoff` skill for complete handoff protocol
- `swarm-coordination` skill for multi-agent context sharing

---

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
