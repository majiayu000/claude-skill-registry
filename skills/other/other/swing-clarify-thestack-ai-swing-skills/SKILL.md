---
name: swing-clarify
description: Prevents premature execution on ambiguous requests. Analyzes request clarity using 5W1H decomposition, surfaces hidden assumptions, and generates structured clarifying questions before work begins. Use at the start of any non-trivial task, or when a request could be interpreted multiple ways. Triggers on "뭘 원하는건지", "요구사항 정리", "clarify", "what exactly", "scope", "requirements", "정확히 뭘", "before we start".
argument-hint: "[request or task description to clarify]"
allowed-tools: Read, Grep, Glob, Bash
---

# Scope Clarifier

Prevents the most common AI failure: rushing to execute before understanding what's actually needed.

> Addresses the cognitive failure of **Premature Closure** — AI interprets ambiguous requests using defaults and assumptions instead of asking, producing confident output that answers the wrong question.


## Rules (Absolute)

1. **Never execute before clarifying.** If ambiguity score is above threshold, generate questions FIRST. Do not start implementation, research, or analysis until scope is confirmed.
2. **Maximum 3 questions.** Respect the user's time. If more than 3 questions are needed, the request needs decomposition, not interrogation. Ask the 3 highest-impact questions.
3. **Questions must be actionable.** Every question must change what you build. "What's your timeline?" is only valid if it affects scope. "Should this handle authentication?" is always valid if auth wasn't mentioned.
4. **Prefer multiple choice over open-ended.** "Should auth use (a) session cookies, (b) JWT, or (c) OAuth2 with a provider?" beats "How should auth work?"
5. **State your default assumption.** For each question, state what you WOULD assume if the user doesn't answer. This lets them skip questions where the default is fine.
6. **Clear requests get a green light, not questions.** If the request is unambiguous, say so and proceed. Do not ask questions for the sake of asking.
7. **Never block on style preferences.** Naming conventions, formatting, folder structure — these are not scope questions. Use project conventions or sensible defaults.


## Process

### Stage 1: 5W1H Decomposition

Break the request into six dimensions:

| Dimension | Question | Example Gap |
|:----------|:---------|:------------|
| **What** | What exactly is being built/changed? | "Build auth" — login? signup? password reset? SSO? |
| **Who** | Who uses this? What roles/permissions? | "Users can edit" — all users? admins only? owners? |
| **Where** | Where does this live? What system/service? | "Add to the API" — which API? new endpoint? existing? |
| **When** | What triggers this? What's the lifecycle? | "Send notifications" — real-time? batched? on what event? |
| **Why** | What problem does this solve? What's the success criteria? | "Improve performance" — latency? throughput? cost? |
| **How** | Are there constraints on implementation? | "Use the existing stack" — which parts? any exceptions? |

### Stage 2: Ambiguity Scoring

For each dimension, rate clarity:

- **Clear** — explicitly stated or unambiguously implied by context
- **Assumable** — not stated, but a reasonable default exists (state the default)
- **Ambiguous** — multiple valid interpretations, wrong guess = wasted work

Count the **Ambiguous** dimensions:
- 0 Ambiguous → **Green light.** Proceed immediately. State: "Scope is clear. Proceeding."
- 1-2 Ambiguous → **Quick clarify.** Ask 1-2 targeted questions with defaults.
- 3+ Ambiguous → **Must clarify.** Ask up to 3 highest-impact questions. Do not proceed until answered.

### Stage 3: Generate Clarifying Questions

For each Ambiguous dimension (up to 3, prioritized by impact):

```
**Q[N]: [Specific question]**
Options: (a) [option] (b) [option] (c) [option]
My default: (b) — [why this is the reasonable default]
Impact: [what changes depending on the answer]
```

### Stage 4: Confirm and Proceed

After receiving answers (or user says "go with defaults"):
1. Restate the clarified scope in 3-5 bullet points
2. Note any remaining assumptions (rated as Assumable, not Ambiguous)
3. Proceed with execution


## Output Format

```markdown
## Scope Analysis: [Request Summary]

### 5W1H Decomposition
| Dimension | Status | Detail |
|:----------|:-------|:-------|
| What | Clear / Assumable / Ambiguous | [extracted or missing info] |
| Who | Clear / Assumable / Ambiguous | [extracted or missing info] |
| Where | Clear / Assumable / Ambiguous | [extracted or missing info] |
| When | Clear / Assumable / Ambiguous | [extracted or missing info] |
| Why | Clear / Assumable / Ambiguous | [extracted or missing info] |
| How | Clear / Assumable / Ambiguous | [extracted or missing info] |

### Ambiguity Score: [N]/6 → [Green light / Quick clarify / Must clarify]

### Questions (if any)

**Q1: [Question]**
Options: (a) ... (b) ... (c) ...
My default: (b) — [reason]
Impact: [what changes]

**Q2: ...**

### Clarified Scope (after answers)
- [bullet 1]
- [bullet 2]
- [bullet 3]

### Remaining Assumptions
- [assumption 1] — rated Assumable because [reason]
```


## Quality Calibration

### BAD Scope Clarification (Don't Do This)

```
User: "Build me an auth system"

AI: I have a few questions before we start:
1. What programming language would you like to use?
2. What database do you prefer?
3. Do you want tests?
4. What's your timeline?
5. How many users do you expect?
6. Should it be containerized?
7. What CI/CD platform do you use?
```

Problems:
- 7 questions — overwhelming, most don't affect auth scope
- "What language?" — look at the project, it's obvious
- "Do you want tests?" — always yes, not a scope question
- "What's your timeline?" — doesn't change what you build
- No multiple choice, no defaults stated
- No 5W1H structure, just a brain dump

### GOOD Scope Clarification (Do This)

```
User: "Build me an auth system"

## Scope Analysis: Auth System

### 5W1H Decomposition
| Dimension | Status | Detail |
|:----------|:-------|:-------|
| What | Ambiguous | "Auth system" — login only? signup? password reset? SSO? |
| Who | Ambiguous | User roles not specified — single role or RBAC? |
| Where | Clear | Next.js app (inferred from project structure) |
| When | Clear | Standard request-response auth flow |
| Why | Assumable | Secure user access (standard) |
| How | Assumable | Project uses TypeScript + Prisma (from codebase) |

### Ambiguity Score: 2/6 → Quick clarify

**Q1: What auth flows are needed?**
Options: (a) Email/password login only (b) Login + signup + password reset (c) Full OAuth2 with Google/GitHub providers
My default: (b) — most apps need the complete basic flow
Impact: (a) = 2 hours, (b) = 4 hours, (c) = 8 hours + provider setup

**Q2: User roles?**
Options: (a) Single role — all users equal (b) Admin + User (c) Custom RBAC with permissions
My default: (a) — add roles later when needed (YAGNI)
Impact: (c) requires permission tables, middleware, and role management UI
```

Why this is better:
- Only 2 questions, both high-impact
- Multiple choice with clear options
- Defaults stated with reasoning
- Impact quantified (hours, complexity)
- 4 dimensions already resolved from context (no wasted questions)
- 5W1H structure makes the analysis transparent


## When to Use

- Start of any non-trivial task or feature request
- When a request contains words like "system", "module", "feature", "improve", "fix" without specifics
- When you catch yourself making assumptions about what the user wants
- When a task could take 2 hours or 2 weeks depending on interpretation
- Before invoking any other Stack Skill (clarify scope first, then research/review/plan)

## When NOT to Use

- Bug reports with reproduction steps (scope is the bug)
- Explicit, detailed specifications ("Add a GET /users endpoint returning id and name")
- Follow-up tasks in an ongoing conversation where context is established
- Quick questions ("What does this function do?")
- When the user explicitly says "just do it" or "use your judgment"

## Gotchas

1. **Don't ask what you can read.** If the project has a `package.json`, `tsconfig.json`, or existing code — check it before asking "what language/framework?" That's not clarification, it's laziness.
2. **3 questions max is a hard ceiling.** If you need more, the request needs decomposition into sub-tasks, not more interrogation.
3. **Style preferences are not scope questions.** Naming conventions, folder structure, formatting — use project conventions or sensible defaults. Never block on these.
4. **State your default for every question.** The user should be able to say "go with defaults" and skip all questions. If your defaults aren't stated, you've failed.
5. **Green light means GO.** If the request is clear, say so and proceed immediately. Do not ask questions for the sake of appearing thorough.

## Integration Notes

- **Before everything:** swing-clarify is designed to run FIRST. Clarified scope feeds into all other skills.
- **With swing-research:** Clarified scope → focused research questions (prevents researching the wrong thing)
- **With swing-review:** Clarified scope → review against actual requirements (prevents reviewing against assumed requirements)
- **With swing-options:** Clarified constraints → better option generation (constraints define what's conventional vs unconventional)
- **With swing-mortem:** Clarified assumptions → more specific failure scenarios
- **With swing-trace:** Clarified scope → clearer claim isolation in Stage 1 (fewer ambiguous assumptions to trace)
