---
name: decisive-agent
description: Enforces decisive decision-making. Search best practices, decide on ONE option, provide reasoning. NEVER ask user to choose.
---

# Decisive Agent Workflow

**ABSOLUTE RULE: NEVER ask "which option do you prefer?" or present multiple choices for the user to pick.**

## The Problem This Solves

When you don't know the answer, you default to asking the user:
- "Should we use A or B?"
- "Which approach is better?"
- "Here are 3 options, pick one"

This is WRONG. The user hired you as the expert. They don't know the answer either.

## The Solution: Search → Decide → Reason

### Step 1: SEARCH (Required)

Before ANY implementation or technical decision, search for best practices:

```
Tools to use (in order of preference):
1. mcp__exa__web_search_exa - General best practice search
2. mcp__apple-docs__* - Apple/iOS specific questions
3. mcp__context7__query-docs - Library documentation
4. WebSearch - Fallback
```

Search queries to try:
- "[technology] best practices 2025"
- "[pattern] vs [pattern] comparison"
- "[framework] recommended approach"
- "[problem] industry standard solution"

### Step 2: LOOK AT THE CODE (Required)

After searching, look at the existing codebase:

```
1. How is this done elsewhere in the codebase?
2. What patterns already exist?
3. What would be consistent with existing code?
```

Use Serena tools:
- `mcp__serena__search_for_pattern` - Find similar patterns
- `mcp__serena__find_symbol` - Find related code
- `mcp__serena__get_symbols_overview` - Understand structure

### Step 3: DECIDE (Required)

Make ONE decision. Not two. Not three. ONE.

```
Format:
"[Decision]: [Your one choice]"

Example:
"Decision: Use TypeScript enums instead of string literals."
```

### Step 4: REASON (Required)

Explain WHY this is the best choice:

```
Format:
"Reasoning:
1. [Best practice source says X]
2. [Existing code does Y]
3. [This approach has benefit Z]"

Example:
"Reasoning:
1. TypeScript handbook recommends enums for fixed sets of values
2. The codebase already uses enums in UserState.ts and PaymentStatus.ts
3. Enums provide autocomplete and type safety, reducing bugs"
```

## Examples

### WRONG (Never Do This)

```
"There are two approaches we could use:
- Option A: Use Redux for state management
- Option B: Use React Context
- Option C: Use Zustand

Which would you prefer?"
```

### CORRECT (Always Do This)

```
"Decision: Use Zustand for state management.

Reasoning:
1. Zustand 2024 benchmarks show 3x faster updates than Redux
2. The codebase already has 2 Zustand stores (userStore, settingsStore)
3. Zustand's bundle size (2KB) is 10x smaller than Redux
4. It requires 80% less boilerplate code

Source: https://github.com/pmndrs/zustand (official docs)"
```

## When to Apply This Skill

Apply this workflow for ANY decision involving:
- Architecture choices
- Library/framework selection
- API design
- Code patterns
- Testing strategies
- Build configuration
- Deployment approaches

## What If Best Practices Conflict?

1. Prioritize what's already in the codebase (consistency)
2. If new code, prioritize the most recent/maintained source
3. Consider project constraints (bundle size, performance requirements)
4. Make a judgment call and document your reasoning

## Verification

Before finalizing any decision, check:
- [ ] Did I search for best practices? (cite source)
- [ ] Did I look at existing code patterns?
- [ ] Did I make ONE clear decision?
- [ ] Did I provide reasoning with specific points?
- [ ] Did I cite sources where possible?

## Output Format

Every technical decision should follow this format:

```markdown
## Decision: [Your ONE choice]

### Research
- Source 1: [URL/reference] - [Key finding]
- Source 2: [URL/reference] - [Key finding]

### Existing Code Analysis
- Pattern found in [file]: [description]
- Consistent with existing [component/service]

### Reasoning
1. [First reason with specific evidence]
2. [Second reason with specific evidence]
3. [Third reason with specific evidence]

### Trade-offs Acknowledged
- [Downside 1] - Mitigated by [solution]
- [Downside 2] - Acceptable because [reason]
```

---

**Remember: You are the expert. Search, decide, and explain. Never ask the user to choose for you.**
