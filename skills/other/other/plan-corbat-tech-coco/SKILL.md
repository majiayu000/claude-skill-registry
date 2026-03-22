---
name: plan
description: Create a detailed, phased implementation plan before writing any code. Restate requirements, identify risks, and break the work into actionable steps. Waits for user confirmation before touching any code.
allowed-tools: Read, Grep, Glob
---

# Plan

Invoke the **planner** agent to create a comprehensive implementation plan.

## Rules

1. **DO NOT write any code** until the user explicitly confirms with "yes", "proceed", "go ahead", or similar
2. **DO NOT modify any files** during planning
3. Use only Read, Grep, and Glob tools to understand the codebase
4. Present the complete plan and wait for confirmation

## Process

### 1. Understand the Request
Restate the requirements in your own words to confirm understanding.
Ask clarifying questions if anything is ambiguous.

### 2. Explore the Codebase
- Read relevant source files in `src/`
- Find similar patterns already in the codebase
- Identify what files will need to change
- Check for existing tests to understand test patterns

### 3. Create the Plan
Follow this structure:

```markdown
# Plan: [Feature Name]

## Summary
[2-3 sentences: what, why, expected result]

## Affected Files
| File | Change |
|------|--------|
| `src/...` | [new / modify / extend] |

## Implementation Steps

### Phase 1: Types & Schema
1. **[action]** — `src/path/file.ts`
   - What: [specific change]
   - Deps: none
   - Risk: Low/Medium/High

### Phase 2: Core Logic
2. **[action]** — `src/path/file.ts`
   - What: [specific change]
   - Deps: Step 1
   - Risk: Low/Medium/High

### Phase 3: Integration
3. **[Register/Connect]** — `src/path/file.ts`

### Phase 4: Tests
4. **[Write tests]** — `src/path/file.test.ts`
   - Cover: happy path, errors, edge cases

## Testing Strategy
- Files: `pnpm test src/path/`
- Coverage target: 80%+
- `pnpm check` must pass

## Risks & Mitigations
- Risk: [description] → Mitigation: [approach]

## Success Criteria
- [ ] `pnpm check` passes
- [ ] Coverage ≥80%
- [ ] Works with all providers (Anthropic, OpenAI, Gemini)
```

### 4. Present and Wait

After presenting the plan, say:

> **Awaiting confirmation.** Reply "yes" to proceed, or request changes.

Do NOT start implementing until you receive explicit confirmation.

## Usage

```
/plan add a new tool that...
/plan refactor the quality analyzer to...
/plan implement feature X described in the issue
```
