---
name: ralph-technique
description: The Ralph Wiggum technique for minimal, declarative prompts that enable loop-based autonomous execution.
agents: [rex, nova, blaze, grizz, tess]
triggers: [minimal, ralph, loop, autonomous, simple prompt, deterministic]
---

# Ralph Wiggum Technique

The Ralph technique is a minimal prompting approach that enables autonomous, loop-based agent execution. Named after the Simpsons character, it embraces simplicity and iterative refinement.

## Core Philosophy

> "Ralph is deterministically bad in an undeterministic world."

**Key insight:** Simpler prompts (~40-50 lines) often outperform verbose prompts (~200+ lines). Overly detailed prompts can make agents "slower and dumber."

## The Ralph Loop

In its purest form, Ralph is a bash loop:

```bash
while :; do cat PROMPT.md | claude-code ; done
```

The agent runs continuously, making incremental progress. Failures are expected and corrected through iteration.

## Signs on the Playground

When Ralph makes mistakes, don't blame the tools—add "signs":

```
Ralph builds playground → Falls off slide → Add sign: "SLIDE DOWN, DON'T JUMP"
                                         → Ralph sees sign next time
                                         → Behavior improves
```

**Translation:** When an agent fails, add a concise constraint to the prompt. Don't explain why—just state the rule.

## Minimal Prompt Pattern

```markdown
# {Agent} - {Role}

You are {Agent}. Your job is to {primary task} in `task/`.

## Constraints

- {Essential constraint 1}
- {Essential constraint 2}
- {Essential constraint 3}
- {Max 5-7 constraints}

## Definition of Done

- All acceptance criteria in `task/acceptance.md` satisfied
- {Required commands pass}
- PR created with Linear issue link

## Task Context

- Task ID: {{task_id}}
- Service: {{service}}
- Branch: feature/task-{{task_id}}-{job}

Read `task/` directory and implement.
```

**Total: ~40-50 lines**

## What to Include

| Include | Why |
|---------|-----|
| Role statement | One sentence, no fluff |
| Hard constraints | Non-negotiable rules (lint, types, etc.) |
| Definition of Done | Acceptance criteria reference |
| Task context | Variables for this run |
| Start instruction | "Read `task/` and implement" |

## What to Exclude

| Exclude | Why |
|---------|-----|
| Code examples | Trust model's training data |
| Tool usage guides | Model knows its tools |
| Detailed explanations | Adds noise, slows reasoning |
| Decision frameworks | Let model decide |
| Checklists | Keep it in acceptance.md |

## When to Use Ralph

| Scenario | Use Ralph? |
|----------|-----------|
| Greenfield implementation | ✅ Yes |
| Well-defined task with clear acceptance | ✅ Yes |
| Complex refactoring across many files | ⚠️ Maybe |
| Novel architecture decisions | ❌ No - use standard |
| Debugging obscure issues | ❌ No - use standard |
| First implementation of a pattern | ❌ No - use standard |

## Tuning Ralph

When Ralph fails repeatedly:

1. **Identify the pattern** - What mistake keeps happening?
2. **Add a sign** - One-line constraint, no explanation
3. **Test again** - Run the loop
4. **Iterate** - Repeat until stable

**Example signs (constraints):**
- "Never use `any` types"
- "Run `cargo clippy` before committing"
- "Test at 375px mobile viewport"
- "Use Effect.gen, not raw Promise chains"

## Ralph vs Standard Prompts

| Aspect | Ralph (Minimal) | Standard |
|--------|----------------|----------|
| Lines | 40-50 | 150-200+ |
| Code examples | None | Extensive |
| Tool guidance | None | Detailed |
| Trust in model | High | Lower |
| Iteration speed | Fast | Slower |
| Context overhead | Low | High |

## Activating Ralph Mode

### Via Linear Label
```
Labels: cto:prompt:minimal
```

### Via CodeRun Spec
```yaml
spec:
  promptStyle: "minimal"
```

## The Ralph Mindset

1. **Faith in eventual consistency** - Ralph will get there
2. **Deterministic failure** - Failures are predictable and fixable
3. **Tuning, not debugging** - Adjust prompts like tuning a guitar
4. **Less is more** - Every word costs attention

## References

- [Ralph Wiggum technique](https://ghuntley.com/ralph/) - Original concept by Geoff Huntley
- [YC Agents hackathon](https://github.com/repomirrorhq/repomirror/blob/main/repomirror.md) - Field report
- [Brief History of Ralph](https://www.humanlayer.dev/blog/brief-history-of-ralph) - HumanLayer's experience
