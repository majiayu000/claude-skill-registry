---
name: plan-generation
description: Assist in generating comprehensive plans from templates using extended thinking. Use when generating plans from meta-prompt templates, reviewing plan quality, or ensuring plans meet team standards.
allowed-tools: Read, Grep, Glob
---

# Plan Generation

Guide for generating high-quality plans from meta-prompt templates.

## When to Use

- Generating plans from `/chore`, `/bug`, `/feature` templates
- Reviewing generated plans for completeness
- Ensuring plans follow team standards
- Improving plan quality and specificity

## Plan Generation Process

### Step 1: Understand the Request

Parse the high-level description:

```text
Input: "Add user authentication with OAuth"

Extract:
- Domain: Authentication
- Scope: User-facing, OAuth protocol
- Complexity: Medium-high (external integration)
```

### Step 2: Activate Reasoning

Use extended thinking for complex planning:

```markdown
THINK HARD about:
- What files need to change?
- What are the dependencies?
- What could go wrong?
- How will we verify success?
```

### Step 3: Explore the Codebase

Gather context before planning:

- Read README for project structure
- Identify relevant existing patterns
- Find test examples to follow
- Locate configuration files

### Step 4: Fill the Template

Complete every section with specifics:

```markdown
## Relevant Files
- src/auth/OAuthProvider.ts (create)
- src/auth/index.ts (modify - add export)
- src/config/oauth.ts (create)
- tests/auth/oauth.test.ts (create)
```

### Step 5: Validate Plan Quality

Check against quality criteria before finalizing.

## Quality Criteria

Every plan should meet these standards:

### Specificity

**Bad**: "Update the component"
**Good**: "Update UserProfile.tsx to add loading state on line 45"

### Actionability

**Bad**: "Handle errors appropriately"
**Good**: "Add try/catch in fetchUser(), log errors with console.error, show ErrorBoundary"

### Completeness

All template sections filled:

- [ ] Description explains what and why
- [ ] Relevant Files lists all files to touch
- [ ] Tasks are numbered and specific
- [ ] Validation Commands are executable
- [ ] Notes capture edge cases

### Testability

Every plan must include validation:

```markdown
## Validation Commands

- Run `npm test -- auth` to verify unit tests pass
- Run `npm run e2e -- oauth` to verify integration
- Manual: Complete OAuth flow in browser
```

## Plan Types and Focus Areas

### Chore Plans

Focus on:

- Clear scope boundaries
- Idempotent operations
- Low-risk execution
- Quick validation

### Bug Plans

Focus on:

- Root cause analysis
- Reproduction steps
- Regression prevention
- Before/after verification

### Feature Plans

Focus on:

- User story alignment
- Implementation phases
- Testing strategy
- Acceptance criteria

## Common Issues and Fixes

### Vague Tasks

**Problem**: "Implement the feature"
**Fix**: Break into specific sub-tasks with file references

```markdown
## Step by Step Tasks
1. Create AuthContext in src/contexts/AuthContext.tsx
2. Add useAuth hook in src/hooks/useAuth.ts
3. Wrap App component with AuthProvider in src/App.tsx
4. Add login route in src/routes/index.tsx
```

### Missing Files

**Problem**: Plan doesn't mention test files
**Fix**: Always include test file creation/modification

```markdown
## Relevant Files
- src/components/Login.tsx (create)
- src/components/Login.test.tsx (create) # Tests!
```

### Unclear Validation

**Problem**: "Make sure it works"
**Fix**: Specific commands with expected outcomes

```markdown
## Validation Commands
- Run `npm test` - expect 0 failures
- Run `npm run build` - expect successful build
- Run `npm run lint` - expect 0 errors
```

### Scope Creep

**Problem**: Plan addresses more than requested
**Fix**: Stay focused on original request, note related work in Notes

```markdown
## Notes
- Related: Login form could use accessibility improvements (separate chore)
- Related: Password reset flow needs similar OAuth option (separate feature)
```

## Extended Thinking Triggers

**Note:** Extended thinking is enabled by default in Claude Code (31,999 tokens). Phrases like "think", "think hard", "ultrathink" are prompt instructions that signal your expectations but don't control token allocation. Use `Alt+T` to toggle thinking or `MAX_THINKING_TOKENS` to adjust budget.

Use "THINK HARD" in meta-prompts as a prompt instruction to signal the need for careful reasoning:

| Phrase | When to Use |
| --- | --- |
| "THINK HARD" | Medium-to-high complexity, encourage careful reasoning |

## Output Guidelines

### Naming Convention

```text
specs/[type]-[descriptive-name].md

Examples:
- specs/chore-update-dependencies.md
- specs/bug-fix-login-race-condition.md
- specs/feature-oauth-authentication.md
```

### File Location

Always write plans to `specs/` directory (or project-specific equivalent).

### Format Consistency

Match the template's Plan Format exactly - don't add or remove sections.

## Related Memory Files

- @template-engineering.md - How templates work
- @meta-prompt-patterns.md - Prompt hierarchy
- @plan-format-guide.md - Standard plan structures
- @fresh-agent-rationale.md - Why plan then implement separately

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
