---
name: rough-draft-interface
description: Phase 1 - Define the structural contracts of the system
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

Query project knowledge for type conventions and patterns.

### Topic Inference (Interface Focus)

From work item context, build candidates:
- `{item-keyword}-types`
- `{item-keyword}-patterns`
- `type-conventions`
- `coding-standards`

### Example

```
Tool: mcp__plugin_mermaid-collab_mermaid__kodex_query_topic
Args: { "project": "<cwd>", "name": "type-conventions" }
```

Display found topics as context before defining interfaces.

# Phase 1: Interface

Define the structural contracts of the system.

## What to Produce

1. **File paths** - List all files that will be created or modified
2. **Class and function signatures** - Names, parameters, return types
3. **Public API contracts** - How components interact with each other
4. **Type definitions** - Custom types, interfaces, enums

## Process

```bash
# Read design doc
cat .collab/<name>/documents/design.md
```

**For each component identified in design:**
1. Define the file path where it will live
2. List all public functions/methods with signatures
3. Define input/output types
4. Document how it connects to other components

## Output Format

**Create per-item interface documents** instead of adding to design.md:

For each work item N, create `interface-item-N.md`:

```
Tool: mcp__plugin_mermaid-collab_mermaid__create_document
Args: {
  "project": "<cwd>",
  "session": "<session>",
  "name": "interface-item-N",
  "content": "<interface content for item N>"
}
```

**Document structure:**

```markdown
## Interface Definition

### File Structure
- `src/auth/types.ts` - Core type definitions
- `src/auth/service.ts` - Authentication service
- `src/auth/middleware.ts` - Express middleware

### Type Definitions

```typescript
// src/auth/types.ts
interface User {
  id: string;
  email: string;
  role: 'admin' | 'user';
}

interface AuthResult {
  success: boolean;
  user?: User;
  error?: string;
}
```

### Function Signatures

```typescript
// src/auth/service.ts
class AuthService {
  authenticate(email: string, password: string): Promise<AuthResult>
  validateToken(token: string): Promise<User | null>
  revokeToken(token: string): Promise<void>
}

// src/auth/middleware.ts
function requireAuth(req: Request, res: Response, next: NextFunction): void
function requireRole(role: string): Middleware
```

### Component Interactions
- `middleware.requireAuth` calls `service.validateToken`
- `service.authenticate` returns tokens stored in Redis
```

## Verification Gate

Before moving to Phase 2, run verification:

```bash
# Trigger verify-phase hook
./hooks/verify-phase.sh interface <collab-name>
```

**Checklist:**
- [ ] All files from design are listed
- [ ] All public interfaces have signatures
- [ ] Parameter types are explicit (no `any`)
- [ ] Return types are explicit
- [ ] Component interactions are documented

**GATE: Do NOT proceed until this checklist passes.**

**If Interface phase doesn't apply** (e.g., pure config changes, docker setup):
1. Document explicitly: "N/A - [reason why interface phase doesn't apply]"
2. Add this to the design doc Interface Definition section
3. You still MUST proceed through pseudocode, skeleton, and executing-plans
4. Skipping to implementation is NEVER allowed

**Update state on success:**

```
Tool: mcp__plugin_mermaid-collab_mermaid__update_session_state
Args: { "project": "<cwd>", "session": "<name>", "phase": "rough-draft/pseudocode" }
```
Note: `lastActivity` is automatically updated by the MCP tool.

## Completion

At the end of this skill's work, call complete_skill:

```
Tool: mcp__plugin_mermaid-collab_mermaid__complete_skill
Args: { "project": "<cwd>", "session": "<session>", "skill": "rough-draft-interface" }
```

**Handle response:**
- If `action == "clear"`: Invoke skill: collab-clear
- If `next_skill` is not null: Invoke that skill
- If `next_skill` is null: Workflow complete
