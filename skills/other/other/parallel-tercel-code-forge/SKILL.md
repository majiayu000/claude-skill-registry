---
name: parallel
description: >
  Use when facing 2+ independent problems that can be solved concurrently —
  dispatches one sub-agent per problem domain for parallel investigation and fixing.
  For parallel task execution within a feature, use code-forge:impl instead.
---

# Code Forge — Parallel

Dispatch independent sub-agents to solve multiple unrelated problems concurrently.

## When to Use

- 3+ test files failing with different root causes
- Multiple independent subsystems broken simultaneously
- Several unrelated bugs reported at once
- Any situation with 2+ problems that share no state

## When NOT to Use

- Failures are related (fix one, others may resolve)
- Problems share state or dependencies
- Need full system state to diagnose (single-threaded investigation needed)
- Only 1 problem exists

**For task execution within a feature:** Use `/code-forge:impl` which has built-in parallel task support.

## Core Principle

**One agent per independent problem domain. Let them work concurrently.**

## Workflow

### Step 1: Identify Problems

List all problems. For each, note:
- What is failing (test file, error message, component)
- Which files/modules are involved
- Whether it shares state with other problems

### Step 2: Assess Independence

Build a dependency matrix:

```
Problem A ←→ Problem B: independent? (yes/no, why)
Problem A ←→ Problem C: independent? (yes/no, why)
Problem B ←→ Problem C: independent? (yes/no, why)
```

Group dependent problems together. Each independent group gets its own agent.

### Step 3: Dispatch Agents

For each independent problem group, launch a `Agent(subagent_type="general-purpose")`:

**Agent prompt structure:**
```
You are investigating and fixing: {problem description}

## Scope
- Files involved: {list}
- Error messages: {paste}
- Expected behavior: {description}

## Constraints
- Only modify files in your scope
- Use code-forge:tdd methodology (write failing test first)
- Use code-forge:debug methodology (root cause before fix)

## Output Required
- Root cause (1-2 sentences)
- Files changed (list)
- Test results (pass/fail counts)
- Summary of fix (1-2 sentences)
```

**CRITICAL:** Launch all agents in a single message using multiple `Agent` tool calls. This enables true parallel execution.

### Step 4: Review and Integrate

After all agents complete:

1. **Check for conflicts** — did any agents modify the same file?
   - No conflicts: proceed
   - Conflicts: resolve manually, prefer the more targeted change
2. **Run full test suite** — verify all fixes work together
3. **Report results:**

```
Parallel dispatch complete: {N} agents, {M} problems resolved

Agent 1: {problem} → {root cause} → {status}
Agent 2: {problem} → {root cause} → {status}
Agent 3: {problem} → {root cause} → {status}

Full test suite: {pass}/{total} passing
```

## Example

```
3 test files failing: auth.test.ts, payment.test.ts, email.test.ts

Independence check:
  auth ←→ payment: independent (different modules, no shared state)
  auth ←→ email:   independent (different modules)
  payment ←→ email: independent

Dispatch 3 agents in a single message:
  Agent 1: "Fix auth.test.ts — files: src/auth/, error: missing token validation"
  Agent 2: "Fix payment.test.ts — files: src/payment/, error: decimal precision"
  Agent 3: "Fix email.test.ts — files: src/email/, error: template not found"

Results: 3/3 resolved, full suite 128/128 passing
```

## Common Mistakes

- Dispatching agents for related problems (they'll step on each other's changes)
- Not providing enough context in agent prompts (agent wastes time re-discovering)
- Launching agents sequentially instead of in a single parallel message
- Skipping the full test suite after integration
- Dispatching too many agents (>5) — diminishing returns, harder to integrate
