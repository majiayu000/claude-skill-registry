---
name: rough-draft-pseudocode
description: Phase 2 - Define the logic flow for each function
user-invocable: false
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
  - mcp__plugin_mermaid-collab_mermaid__*
---

## Step 0: Query Kodex

Query project knowledge for error handling and logic patterns.

### Topic Inference (Pseudocode Focus)

From work item context, build candidates:
- `{item-keyword}-error-handling`
- `{item-keyword}-logic`
- `error-patterns`
- `validation-patterns`

### Example

```
Tool: mcp__plugin_mermaid-collab_mermaid__kodex_query_topic
Args: { "project": "<cwd>", "name": "error-patterns" }
```

Display found topics as context before writing pseudocode.

# Phase 2: Pseudocode

Define the logic flow for each function.

## What to Produce

1. **Logic flow** - Step-by-step description of what each function does
2. **Error handling approach** - How errors are caught, propagated, reported
3. **Edge cases** - Boundary conditions and how they're handled
4. **Dependencies** - External services, databases, APIs called

## Process

For each function from the Interface phase:
1. Write plain-language pseudocode
2. Identify error conditions
3. List edge cases
4. Note any external calls

## Output Format

**Create per-item pseudocode documents** instead of adding to design.md:

For each work item N, create `pseudocode-item-N.md`:

```
Tool: mcp__plugin_mermaid-collab_mermaid__create_document
Args: {
  "project": "<cwd>",
  "session": "<session>",
  "name": "pseudocode-item-N",
  "content": "<pseudocode content for item N>"
}
```

**Document structure:**

```markdown
# Pseudocode: Item N - [Title]

### AuthService.authenticate(email, password)

```
1. Validate email format
   - If invalid: return { success: false, error: "Invalid email format" }

2. Look up user by email in database
   - If not found: return { success: false, error: "User not found" }

3. Verify password hash
   - If mismatch: return { success: false, error: "Invalid password" }
   - Rate limit: after 5 failures, lock account for 15 minutes

4. Generate JWT token
   - Include: user.id, user.role, expiry (1 hour)

5. Store token in Redis with TTL
   - Key: "token:{tokenId}", Value: user.id

6. Return { success: true, user, token }
```

**Error Handling:**
- Database errors: Log and return generic "Authentication failed"
- Redis errors: Fall back to stateless JWT (no revocation support)

**Edge Cases:**
- Empty password: Reject before hashing
- Expired account: Check `user.expiresAt` before authenticating
- Concurrent logins: Allow (no session limit)
```

## Verification Gate

Before moving to Phase 3, run verification:

```bash
./hooks/verify-phase.sh pseudocode <collab-name>
```

**Checklist:**
- [ ] Every function from Interface has pseudocode
- [ ] Error handling is explicit for each function
- [ ] Edge cases are identified
- [ ] External dependencies are noted

**GATE: Do NOT proceed until this checklist passes.**

**If Pseudocode phase doesn't apply** (e.g., no logic to describe, pure data changes):
1. Document explicitly: "N/A - [reason why pseudocode phase doesn't apply]"
2. Add this to the design doc Pseudocode section
3. You still MUST proceed through skeleton and executing-plans
4. Skipping to implementation is NEVER allowed

**Update state on success:**

```
Tool: mcp__plugin_mermaid-collab_mermaid__update_session_state
Args: { "project": "<cwd>", "session": "<name>", "phase": "rough-draft/skeleton" }
```
Note: `lastActivity` is automatically updated by the MCP tool.

## Completion

At the end of this skill's work, call complete_skill:

```
Tool: mcp__plugin_mermaid-collab_mermaid__complete_skill
Args: { "project": "<cwd>", "session": "<session>", "skill": "rough-draft-pseudocode" }
```

**Handle response:**
- If `action == "clear"`: Invoke skill: collab-clear
- If `next_skill` is not null: Invoke that skill
- If `next_skill` is null: Workflow complete
