---
name: codex-invocation
description: Invoke OpenAI Codex CLI with the correct configuration for autonomous code generation. Use when you need Codex to generate or regenerate code files, implement features, or execute multi-step coding tasks.
---

# Codex Invocation Skill

Invoke OpenAI Codex CLI (gpt-5.1-codex) with proper configuration for autonomous code generation and file creation.

## When to Use This Skill

- Generating complete code files from specifications
- Implementing complex features autonomously
- Regenerating code with specific requirements
- Executing multi-step coding tasks that require deep reasoning
- When the user explicitly requests Codex to implement something

## Core Concepts

### Codex CLI Configuration

**Model Selection:**
- `gpt-5.1-codex`: Latest Codex model with extended reasoning capabilities
- Use with `model_reasoning_effort="high"` for production-quality code

**Sandbox Modes:**
- `read-only`: Codex can read files but not modify them
- `workspace-write`: Codex can write files within the workspace
- `danger-full-access`: Full system access (required for most code generation)

**Approval Policy:**
- `untrusted`: Codex must ask before running commands
- `on-failure`: Ask only if commands fail
- `on-request`: Codex decides when to ask
- `never`: Fully autonomous (use with caution)

### Essential Flags

```bash
codex exec \
  -m gpt-5.1-codex \
  --dangerously-bypass-approvals-and-sandbox \
  -c model_reasoning_effort="high" \
  "Your prompt here"
```

**Flag Breakdown:**
- `-m gpt-5.1-codex`: Use the GPT-5.1 Codex model
- `--dangerously-bypass-approvals-and-sandbox`: Enable `danger-full-access` sandbox and `never` approval policy
- `-c model_reasoning_effort="high"`: Enable extended reasoning for better code quality
- Final argument: The prompt/instruction for Codex

## Pattern 1: Basic Codex Invocation

```bash
# Simple task with high reasoning
codex exec \
  -m gpt-5.1-codex \
  --dangerously-bypass-approvals-and-sandbox \
  -c model_reasoning_effort="high" \
  "Implement the login form component in src/components/LoginForm.tsx with email and password validation."
```

## Pattern 2: Multi-File Implementation from Specification

```bash
# Complex implementation from a prompt file
codex exec \
  -m gpt-5.1-codex \
  --dangerously-bypass-approvals-and-sandbox \
  -c model_reasoning_effort="high" \
  "Implement Phase 2 as specified in CODEX_PHASE_2_PROMPT.md. Create all required files: errors.ts, cache.ts, and all query files (servers.ts, parts.ts, compatibility.ts, builds.ts). Follow all specifications exactly."
```

## Pattern 3: Background Execution with Monitoring

```bash
# Run Codex in background and monitor output
codex exec \
  -m gpt-5.1-codex \
  --dangerously-bypass-approvals-and-sandbox \
  -c model_reasoning_effort="high" \
  "Your prompt here" &

# Monitor using Claude's BashOutput tool
# Use the process ID returned to check progress
```

## Pattern 4: Referencing Skills in Prompts

When creating prompts for Codex, reference relevant Claude skills for guidance:

```markdown
**Relevant Skills to Reference:**
- `.claude/skills/api-design-principles/` - REST API design patterns
- `.claude/skills/database-migration/` - Migration best practices
- `.claude/skills/sql-optimization-patterns/` - Query optimization
- `.claude/skills/modern-javascript-patterns/` - TypeScript patterns
```

This tells Codex to follow the patterns and best practices from these skill files.

## Common Use Cases

### 1. Implementing Database Query Layer

```bash
codex exec \
  -m gpt-5.1-codex \
  --dangerously-bypass-approvals-and-sandbox \
  -c model_reasoning_effort="high" \
  "Create TypeScript database query functions in src/lib/queries/ following the specification in SPEC.md. Include:
  - Type-safe Supabase queries
  - React cache wrapping
  - Error handling
  - JSDoc documentation"
```

### 2. Adding Bonus Features to Existing Code

```bash
codex exec \
  -m gpt-5.1-codex \
  --dangerously-bypass-approvals-and-sandbox \
  -c model_reasoning_effort="high" \
  "Enhance the query files in src/lib/queries/ with these features:
  1. Add comprehensive JSDoc documentation
  2. Add pagination support
  3. Add query logging
  4. Add performance monitoring
  Follow the bonus features section in CODEX_PHASE_2_PROMPT.md"
```

### 3. Generating API Routes

```bash
codex exec \
  -m gpt-5.1-codex \
  --dangerously-bypass-approvals-and-sandbox \
  -c model_reasoning_effort="high" \
  "Create Next.js 14 App Router API routes in src/app/api/ for:
  - GET /api/servers - List servers with filtering
  - GET /api/servers/[id] - Get server by ID
  - POST /api/builds - Create new build
  Follow REST API best practices from .claude/skills/api-design-principles/"
```

## Best Practices

### 1. Clear, Specific Prompts
- Specify exact file paths
- Include expected behavior
- Reference specification files
- List all required features

### 2. Reference Specifications
- Create detailed prompt files (e.g., CODEX_PHASE_2_PROMPT.md)
- Reference existing Claude skills for patterns
- Include code examples when needed

### 3. Monitor Long-Running Tasks
```typescript
// Use Claude's Bash tool to run Codex
await bash({
  command: 'codex exec -m gpt-5.1-codex --dangerously-bypass-approvals-and-sandbox -c model_reasoning_effort="high" "prompt"',
  run_in_background: true
});

// Monitor progress
await bashOutput({ bash_id: "process-id" });
```

### 4. Verify Output
After Codex completes:
- Check all files were created
- Verify TypeScript compilation
- Run tests
- Review for bonus features
- Check for proper error handling

## Troubleshooting

### Windows Shell Issues

If you encounter DLL initialization errors (0xC0000142):

```bash
# Kill hung processes
taskkill /F /IM node.exe /T
taskkill /F /IM powershell.exe /T
taskkill /F /IM cmd.exe /T

# Test shell works
powershell -Command "echo ok"

# Then retry Codex
```

### Codex Not Creating Files

Ensure you're using the correct sandbox mode:
- `--dangerously-bypass-approvals-and-sandbox` for full write access
- Or explicitly set: `--sandbox danger-full-access`

### Low Quality Output

Increase reasoning effort:
- Use `-c model_reasoning_effort="high"` for production code
- Default is "medium" which may skip important details

## Skills Referenced in Prompts

When creating Codex prompts, these skills provide excellent guidance:

1. **api-design-principles** - REST and GraphQL API design patterns
2. **database-migration** - Database migration best practices
3. **sql-optimization-patterns** - Query optimization and indexing
4. **modern-javascript-patterns** - ES6+ and TypeScript patterns
5. **react-modernization** - React hooks and modern patterns
6. **frontend-design** - UI component design principles

## Example: Complete Codex Workflow

```bash
# 1. Create specification file
cat > CODEX_TASK.md << 'EOF'
## Task: Implement User Authentication

Create a complete authentication system:

**Files to Create:**
- src/lib/auth.ts - Auth utilities
- src/app/api/auth/login/route.ts - Login endpoint
- src/app/api/auth/logout/route.ts - Logout endpoint
- src/components/LoginForm.tsx - Login UI

**Requirements:**
- Use JWT tokens
- Hash passwords with bcrypt
- Implement CSRF protection
- Add rate limiting
- Follow .claude/skills/api-design-principles/

**Bonus Features:**
- Add JSDoc documentation
- Add error handling
- Add input validation
- Add unit tests
EOF

# 2. Invoke Codex
codex exec \
  -m gpt-5.1-codex \
  --dangerously-bypass-approvals-and-sandbox \
  -c model_reasoning_effort="high" \
  "Implement the authentication system as specified in CODEX_TASK.md. Include all bonus features."

# 3. Verify output
npm run type-check
npm test
```

## Advanced: Iterative Refinement

```bash
# First pass - basic implementation
codex exec -m gpt-5.1-codex --dangerously-bypass-approvals-and-sandbox \
  -c model_reasoning_effort="high" \
  "Create basic query functions in src/lib/queries/"

# Second pass - add enhancements
codex exec -m gpt-5.1-codex --dangerously-bypass-approvals-and-sandbox \
  -c model_reasoning_effort="high" \
  "Enhance src/lib/queries/*.ts with:
  - Comprehensive JSDoc
  - Pagination
  - Error handling
  - Performance monitoring"

# Third pass - add tests
codex exec -m gpt-5.1-codex --dangerously-bypass-approvals-and-sandbox \
  -c model_reasoning_effort="high" \
  "Create unit tests for all query functions in src/lib/__tests__/"
```

## Summary

Use this skill to invoke Codex with the correct configuration for autonomous code generation. Always:
- Use `gpt-5.1-codex` model
- Use `--dangerously-bypass-approvals-and-sandbox` for write access
- Use `-c model_reasoning_effort="high"` for quality output
- Create detailed specification files
- Reference relevant Claude skills in prompts
- Monitor long-running tasks
- Verify output after completion
