---
name: claude-codex-guardrail-loop
description: Use after planning or implementing non-trivial tasks - runs Codex MCP background verification/review for quality gates (plan validation + implementation review)
---

# Codex-Claude Engineering Loop Skill

## When to use

**Recommended after the following (plan validation runs only on request/approval):**
- After building a non-trivial plan (3+ steps, architecture impact, multi-file changes) -> run plan validation only if user requests/approves
- After implementation completes (new feature, refactor, API change)
- Final validation before build/deploy
- Quality gate check after major work

**Do not use for:**
- Simple config changes (env vars, formatter settings)
- Documentation-only updates
- 1-2 line trivial edits (typos, minor styling)

## Role
- Base role follows `CLAUDE.md`. Codex is a reviewer for plan/implementation.
- The last agent that summarized continues the work.

## Constraint-based guardrails (Gemini prompt strategy)
- **Specify context scope**: do not guess/assume/edit beyond target files/folders. Cite evidence by file/line.
- **Fix output format**: keep requested output format (Plan/Implementation/Review) and length constraints.
- **Declare allowed/forbidden actions**: no external resources, no new deps, no large refactors without approval.
- **Handle uncertainty**: ask briefly when info is missing; mark as "needs confirmation" instead of guessing.
- **Checklist self-check**: before sending, verify key constraints (file scope, format, forbidden items, risks).

## Response template
### User context
- Target files/folders:
- Current behavior:
- Additional context:
- (If needed) constraints/priorities: allowed/forbidden actions, output length/format, whether questions needed

#### Example
- Target files/folders:
  - `src/app/page.tsx`
  - `src/store/dashboardStore.ts`
- Current behavior: fetch data from server and store in local state
- Additional context: can use Suspense / useOptimistic for React 19 support

### Task
- Summarize the user request as bullets.
- Example:
  - Split dashboard state management into Zustand + Immer
  - Minimize potential breakage in existing code
  - Consider type safety (narrowing, ReturnType, etc.)
- Re-summarize constraints (allowed/forbidden actions, format, length, confirm needs).

### Output format
1. Plan: summarize key steps, assumptions, risks.
2. Implementation: summarize file-by-file changes and evidence.
3. Review: summarize edge cases, test approach, remaining risks.

### Final instruction
- Always respond in Plan -> Implementation -> Review order.

## Codex-Claude Loop Procedure
1. **Plan (Claude)**: build a detailed plan and record it in `{tasksRoot}/context.md`.
2. **Plan validation (Codex)** *(optional)*: when requested/approved, ask MCP to validate in background.
   - Use `mcp__codex__spawn_agent`
   - Prompt example:
   ```
   Review this implementation plan and find issues:
   [Claude's plan]

   Focus on:
   - Logic errors and missing edge cases
   - Data/flow consistency and API contract violations
   - Type safety (narrowing, null/undefined) and error handling
   - Performance/resource waste
   - Security/auth/input validation
   - Framework/language best practices
   - Project code conventions and repo rules (CLAUDE.md, etc.)

   Constraints:
   - Keep Plan/Implementation/Review format, summary only
   - Do not mention files/deps not in context; mark "needs confirmation" if unknown
   - Cite evidence near file/line
   ```
   - **Summarize results**: extract only key issues from Codex response for the user (full logs only if needed)
3. **Feedback loop**: summarize Codex issues, update the plan, and ask the user whether to re-validate or proceed.
4. **Implementation (Claude)**: implement step-by-step following the validated plan and record errors/changes explicitly.
5. **Cross review (Codex)**: request background review after implementation.
   - Use `mcp__codex__spawn_agent`
   - Prompt example:
   ```
   Review the implementation and check:

   - Logic/flow errors, missing edge cases
   - Type safety and null/undefined guards, error/exception handling
   - API contract and data model consistency
   - Performance/resource waste
   - Security/auth/input validation
   - Framework/language best practices
   - Project code conventions and repo rules (CLAUDE.md, etc.)
   - Code complexity and maintainability

   Constraints:
   - Summarize response in Plan/Implementation/Review format
   - Do not suggest deps/files outside context; mark "needs confirmation" if required
   - Cite file/line evidence for each issue
   ```
   - **Summarize results**: classify as critical issues, warnings, suggestions
6. **Re-validate and continue**: fix critical issues immediately; confirm large changes with the user; re-validate if needed.
7. **Error handling**: on Codex or implementation errors, analyze cause -> adjust strategy -> confirm before large-impact changes.

## Codex Result Summary Guide

### Summary principles
- **Only the essentials**: critical issues > warnings > suggestions
- **Brevity**: deliver only 3-5 key points
- **Context savings**: do not dump full Codex logs
- **Action-oriented**: include a fix approach for each issue

### Summary template

```
Codex validation complete:

Critical issues (fix immediately):
- [Issue 1]: [short description] -> [action]

Warnings (improve if possible):
- [Issue 2]: [short description] -> [action]

Suggestions:
- [Issue 3]: [short description]
```

### Example
```
Codex validation complete:

Critical issues:
- Type safety: PagingResponse<T> missing -> apply PagingResponse type to API response

Warnings:
- Error handling: Either Left case missing -> add fold handling

Suggestions:
- Performance: consider useMemo for list filtering
```

## Notes
- **Plan validation**: run plan validation via `mcp__codex__spawn_agent`
- **Implementation**: use Claude Edit/Write/Read tools
- **Review**: run review prompt via `mcp__codex__spawn_agent`
- **Parallel validation**: use `mcp__codex__spawn_agents_parallel` for multi-angle checks
