# Plan Review Reference

## Review Instructions

Read project context (AGENTS.md and files mentioned in the plan) to understand the codebase.

## What to Review

- **Completeness** — Missing steps, undefined behavior, unaddressed requirements or edge cases
- **Feasibility** — Technically unsound approaches, ignored constraints, missing dependencies
- **Scope** — Requirements addressed without creep. No missing requirements from the original ask
- **Ordering** — Step dependency issues, missing prerequisites, circular dependencies
- **Buildability** — Steps specific enough to execute without getting stuck. No logical gaps between steps
- **Concreteness** — Every step references a concrete anchor (file/line, function, symbol, or file to create), and named symbols/types are verifiable in the codebase. Flag vague directives or placeholder language
- **Consistency** — Internal contradictions between sections (e.g., Implementation Steps disagree with Verification, two steps describe the same call differently)
- **Verification** — The plan has a verification section that describes how to confirm the change works. Flag if missing, or if it is vague ("run tests" without naming which tests or what to look for)
- **Pattern Alignment** — Proposed approach follows existing codebase patterns where applicable. Deviations from established patterns are justified
- **Side effects** — Other consumers, callers, or co-firing components affected by changes to shared surfaces (helpers, lifecycle hooks, globals)
- **Design Direction** — Whether the chosen approach is the simplest safe option. Challenge assumptions the plan depends on and flag when a different approach would be safer or simpler
- **Failure Modes** — How the design handles partial failure, race conditions, stale state, rollback, data loss, and degraded dependencies

## Determination Criteria

Flag an issue only when ALL of these hold:

1. It would cause an implementer to build the wrong thing or get stuck
2. The issue is discrete and actionable (not a vague concern or general suggestion)
3. The author would likely fix the issue if made aware of it
4. The issue is clearly not an intentional design choice, OR it challenges a design choice with evidence of concrete failure modes or a simpler alternative

## Priority Levels

- **P0** — Plan is fundamentally flawed. Wrong approach or missing core requirement
- **P1** — Significant gap that will likely cause implementation problems
- **P2** — Moderate issue that should be addressed before implementation
- **P3** — Minor improvement

## What to Ignore

- Wording, stylistic, or cosmetic preferences that don't affect buildability
- Alternative approaches without evidence of concrete advantages over the chosen one
- Suggestions that add complexity without clear implementation value
