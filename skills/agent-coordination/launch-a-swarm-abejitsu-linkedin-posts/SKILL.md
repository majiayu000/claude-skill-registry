---
name: launch-a-swarm
description: Spawn 5 parallel agents applying quality principles across planning, building, and validating code. Use when designing features, making decisions, or checking work. Triggers on "launch a swarm" or when ensuring solid, maintainable, secure software.
---

# Launch A Swarm

## TL;DR

Say "launch a swarm" to spawn 5 parallel agents that review your work through Structure, Protection, Correctness, Evolution, and Value lenses. Use during planning, building, or validation phases.

## What This Does

Spawns 5 specialized agents working in parallel to ensure your software is well-built across all critical dimensions. Think of it as having 5 experienced colleagues each examining your work from a different essential angle.

**Why 5 domains?** They cover the complete lifecycle of quality software without overlap:
- **Structure** catches organizational issues
- **Protection** prevents security/safety problems
- **Correctness** ensures things work right
- **Evolution** enables future changes
- **Value** keeps focus on what matters

## When To Use

Say "launch a swarm" for comprehensive quality checks:
- **Planning**: Designing features, choosing technologies, making architectural decisions
- **Building**: Writing code and want real-time quality guidance
- **Validating**: Checking work before merge or deploy

**When NOT to use:**
- Simple, single-file changes with clear requirements
- Emergencies requiring immediate fixes (use after the fix)
- When you just need one perspective (call that specific agent directly)

## The 5 Fundamental Domains

### 1. STRUCTURE (How It's Built)
**Single source of truth. Independent parts. Clear organization.**

Checks:
- Is knowledge in exactly one place? (DRY)
- Are components independent? (can change one without breaking others)
- Do parts know only what they must? (minimal coupling)
- Are names clear and meaningful?
- Is code organized logically?

### 2. PROTECTION (Keeping Bad Things Out)
**Isolated. Validated. Defended.**

Checks:
- Are services isolated in containers? (database, app, cache, web server separated)
- Is input validated before use? (never trust outside data)
- Does each part have minimum access needed? (least privilege)
- Are assumptions checked with assertions?
- Is attack surface minimized?
- Are secrets properly protected? (API keys, passwords)
- Are authentication and authorization enforced?
- Are resources cleaned up? (connections, files, memory)

### 3. CORRECTNESS (Does It Work Right?)
**Tested. Validated. Reliable.**

Checks:
- Is everything tested? (unit, integration, E2E, edge cases)
- Does data flow cleanly? (input → transform → output)
- Is state managed properly? (passed around, not shared globally)
- Do errors fail loudly? (crash early vs. limping along)
- Are edge cases handled?
- Is both happy path AND failure path tested?

### 4. EVOLUTION (Can It Change?)
**Flexible. Configurable. Adaptable.**

Checks:
- Will changes be localized or ripple everywhere?
- Is configuration external to code? (environment variables, not hardcoded)
- Can we swap implementations easily?
- Are decisions reversible?
- Is code rigid or flexible?
- Can we refactor without fear?

### 5. VALUE (Does It Matter?)
**Solves problems. Ships fast. Documented.**

Checks:
- Does this solve actual user need?
- Is build/test/deploy automated?
- Is documentation current and useful?
- Are we shipping or just coding?
- Is it simple or over-engineered?
- Can we deliver when users need it?

## How It Works

### Step 1: Understand Context

Before spawning agents, determine:
- What the user is working on
- The phase (planning, building, or validating)
- What files/areas are relevant

**Phase Detection & Focus:**

| Phase | Triggers | Agent Focus |
|-------|----------|-------------|
| Planning | "should I...", "how should I...", "design", "architecture" | "Will this design lead to problems?" (prevention) |
| Building | "I'm adding", "working on", "implementing" | "Is this code introducing issues?" (real-time guidance) |
| Validating | "done", "finished", "review", "check", "ready" | "What problems exist right now?" (comprehensive review) |

### Step 2: Spawn 5 Agents in Parallel

Launch all 5 agents simultaneously using the Task tool:

```
Task(
  description: "[Domain] Agent: Review [feature]",
  prompt: "[Agent prompt with context]",
  subagent_type: "general-purpose",
  run_in_background: true
)
```

### Step 3: Synthesize Results

After all agents complete, combine findings using the output template below.

## Agent Prompts

Each agent receives a self-contained prompt with embedded checks. Copy the full prompt—agents can't access other sections.

### Base Template
```
You are the [DOMAIN] Agent.

[EMBED CHECKS FROM DOMAIN SECTION ABOVE]

Phase: [PLANNING/BUILDING/VALIDATING]
Context: [What user is working on]
Files: [Relevant file paths]

Report findings as:
1. **Issues** (with file:line references)
2. **Recommendations** (specific actions)
3. **Positives** (what's done well)
```

### Domain-Specific Prompts

**Structure Agent** - copy checks from "1. STRUCTURE" section above

**Protection Agent** - copy checks from "2. PROTECTION" section above, plus:
- Add severity (CRITICAL/HIGH/MEDIUM/LOW) to all issues
- Include XSS/CSRF/Injection vulnerability checks

**Correctness Agent** - copy checks from "3. CORRECTNESS" section above, plus:
- Verify test types: E2E (Playwright), Unit (Vitest), Integration, Accessibility (WCAG AA)

**Evolution Agent** - copy checks from "4. EVOLUTION" section above

**Value Agent** - copy checks from "5. VALUE" section above, plus:
- Flag outdated documentation in README.md

**Important:** The orchestrator must embed the full checks in each prompt. Agents cannot access this skill file—they only receive their prompt text.

## Output Template

After all agents complete, synthesize results:

```markdown
# Swarm Review Results

## Summary
Phase: [PLANNING/BUILDING/VALIDATING]
Scope: [What was reviewed]
Overall: [1-sentence assessment]

## Critical Issues (Must Fix Before Ship)
| Issue | Domain | Location | Fix |
|-------|--------|----------|-----|
| [issue] | Protection | file.ts:42 | [specific action] |

## Important Issues (Should Fix)
| Issue | Domain | Location | Fix |
|-------|--------|----------|-----|
| [issue] | Structure | file.ts:78 | [specific action] |

## Improvements (Nice To Have)
- [improvement] - [domain] - [location]

## Positive Patterns
- [what's working well] - [domain]

## Next Steps
1. [prioritized action]
2. [prioritized action]
3. [prioritized action]

## Domain Scores
- Structure: [Good/Needs Work/Critical Issues]
- Protection: [Good/Needs Work/Critical Issues]
- Correctness: [Good/Needs Work/Critical Issues]
- Evolution: [Good/Needs Work/Critical Issues]
- Value: [Good/Needs Work/Critical Issues]
```

## Error Handling

**If an agent fails to respond:**
- Skip that domain in synthesis
- Note which domains completed
- Recommend re-running failed domain separately

**If synthesis exceeds token limits:**
- Prioritize Critical issues first
- Summarize Important issues
- Link to individual agent outputs

**If agents conflict:**
- Protection Agent > all others (security is non-negotiable)
- Correctness Agent > Evolution Agent (working code > flexible code)
- Value Agent provides tiebreaker for non-security issues

## Examples

**Planning a feature:**
```
User: "Need to add user notifications. Launch a swarm."

Result:
- Structure: Component boundaries for notification service
- Protection: Input validation, rate limiting, auth checks needed
- Correctness: How to test notification delivery
- Evolution: Config for different notification channels
- Value: Does this solve user's actual communication need?
```

**Validating code:**
```
User: "Just built the payment flow. Launch a swarm."

Result:
- Structure: Payment logic is DRY, well-organized (✓)
- Protection: CRITICAL - API keys hardcoded in payment.ts:47
- Correctness: Missing tests for refund edge cases
- Evolution: Payment gateway is swappable (✓)
- Value: Meets user requirements, ready after fixes

Next Steps:
1. Fix hardcoded API keys in payment.ts:47 (Critical)
2. Add refund edge case tests
3. Update README.md with payment flow docs
```

## Glossary

**Container/Sandbox**: Each service runs in isolation - if one is compromised, others stay protected
**Input Validation**: Checking that data from users or APIs is safe before using it
**Attack Surface**: The parts of your system exposed to potential attackers
**Secrets Management**: Protecting API keys, passwords, and tokens from exposure
**DRY**: Don't Repeat Yourself - knowledge in exactly one place
**Coupling**: How much components depend on each other's internals
**Least Privilege**: Giving each part only the minimum access it needs

## Success Looks Like

**Good Planning**: Clear boundaries, isolated services, testable design, flexible architecture, solves real user need

**Good Building**: Principles applied as you write, no shortcuts accumulating, tests growing with code, input validated, configuration external

**Good Validation**: No critical issues, components decoupled and sandboxed, changes localized, tests passing, automated deployment, documentation current, you're proud to ship it

## Remember

- Swarm adapts to what you're doing - planning gets different checks than validation
- Focus is improvement and partnership, not criticism
- Concrete guidance beats abstract principles
- Catching issues in planning is 10x easier than fixing in production
- Quality compounds - small good decisions add up to great software
- You build better when you know someone's checking your work
