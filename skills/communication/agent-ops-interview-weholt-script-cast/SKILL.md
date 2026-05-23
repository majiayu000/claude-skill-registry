---
name: agent-ops-interview
description: "Conduct structured interviews with the user. Use when multiple decisions need user input: ask ONE question at a time, wait for response, record answer, then proceed to next question."
category: utility
invokes: [agent-ops-state]
invoked_by: [agent-ops-constitution, agent-ops-planning, agent-ops-task-creation, agent-ops-task-refinement]
state_files:
  read: [focus.md]
  write: [focus.md]
---

# Interview workflow

## Purpose

Gather user decisions, preferences, or clarifications through a structured one-question-at-a-time process. This prevents overwhelming the user and ensures each answer is properly understood before moving on.

## Rules (strict)

1. **One question per message.** Never batch multiple questions.
2. **Present clear options.** Each question should have labeled options (A, B, C) or a clear format for the expected answer.
3. **Explain briefly.** Give just enough context for the user to decide—not a wall of text.
4. **Record immediately.** After each answer, note it in `.agent/focus.md` or a working document before asking the next question.
5. **Allow escape.** User can say "skip", "defer", "use your recommendation", or "stop interview".
6. **Summarize at end.** When all questions are answered, present a summary for confirmation.

## Interview state tracking

Track in `.agent/focus.md` under "Doing now":

```markdown
## Doing now

Interview: [topic]
- Q1: [question summary] → [answer or pending]
- Q2: [question summary] → [answer or pending]
- ...
```

## Procedure

1. **Setup**: List all questions internally (do not show to user yet).
2. **Ask Q1**: Present one question with options.
3. **Wait**: Do not proceed until user responds.
4. **Record**: Update focus.md with the answer.
5. **Ask Q2**: Repeat until all questions answered or user stops.
6. **Summarize**: Present all answers for confirmation.
7. **Proceed**: Use confirmed answers to continue the workflow.

## Handling special responses

| User says | Action |
|-----------|--------|
| "skip" | Mark as SKIPPED, move to next question |
| "defer" | Mark as DEFERRED, move to next question |
| "use your recommendation" | Apply the agent's recommended default, note it |
| "stop" / "pause" | End interview, save progress, can resume later |
| "go back" | Re-ask the previous question |
| unclear answer | Ask a brief clarifying follow-up (still counts as same question) |

## Question Quality Standards

### Good Questions

- **Specific to context** — Reference project details, not generic templates
- **Reveal non-obvious decisions** — Probe tradeoffs and implications
- **Uncover edge cases** — "What happens when X fails?"
- **Challenge assumptions gently** — "You mentioned X; does that mean Y?"
- **Build on previous answers** — Show you listened

### Bad Questions (avoid)

- ❌ Too obvious: "What programming language will you use?"
- ❌ Too generic: "Do you need a database?"
- ❌ Trivial: "What color should the button be?"
- ❌ Already answered: Re-asking what user just said
- ❌ Assumptive: Leading questions that presume an answer

### Multi-Option Format

When presenting choices, use **label + description**:

```markdown
**Q3: How should the system handle conflicting edits?**

A) **Last-write-wins** — Simple, but may lose data. Best for low-conflict scenarios.
B) **Optimistic locking** — Detect conflicts, prompt user to resolve. More complex.
C) **CRDT-based merge** — Automatic conflict resolution. Best for real-time collab.
D) **Manual review queue** — Flag conflicts for human review. Best for critical data.
```

This format helps users make informed decisions without lengthy explanations.

---

## Completion Criteria

Interview is complete when:

- [ ] All planned questions answered (or explicitly skipped/deferred)
- [ ] No obvious gaps in the information gathered
- [ ] User confirms summary is accurate
- [ ] Answers are recorded in appropriate state file

---

## Anti-patterns (never do)

- ❌ Asking multiple questions in one message
- ❌ Presenting all questions upfront as a "form"
- ❌ Proceeding without waiting for an answer
- ❌ Long explanations that bury the actual question
- ❌ Forgetting to record answers
- ❌ Asking generic template questions regardless of context
- ❌ Ignoring previous answers when forming next question
