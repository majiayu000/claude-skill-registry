---
name: codex
description: AI peer review via OpenAI Codex CLI. Use when reviewing code changes, validating technical decisions, comparing implementation approaches, or getting a second opinion on architecture choices. Triggers on /codex, /codex-review, or auto-triggers when presenting significant alternatives to user.
allowed-tools:
  - Bash(codex exec:*)
  - Read
  - Glob
  - Grep
  - Bash(git status:*)
  - Bash(git diff:*)
  - Bash(git log:*)
user-invocable: true
---

# Codex Peer Review

Consult OpenAI's Codex CLI for peer review before presenting significant decisions or completed work to user.

## When to Auto-Trigger (Without Explicit /codex)

Auto-consult Codex when about to:
- Present 2+ alternative approaches to solve a problem
- Complete a significant feature implementation
- Propose architectural decisions
- Suggest refactoring strategies
- Present trade-off analysis

**Skip auto-consultation for:**
- Trivial fixes (typos, formatting, simple one-liners)
- Direct user instructions with no ambiguity
- Information lookups / explanations
- When user explicitly said "just do X"

## Codex CLI Reference

### Code Review (Scoped)
```bash
# Review uncommitted changes (staged + unstaged + untracked)
codex exec review --uncommitted "Focus on: <specific concerns>"

# Review against base branch
codex exec review --base main "Focus on: <specific concerns>"

# Review specific commit
codex exec review --commit <SHA> "Focus on: <specific concerns>"
```

### Freeform Consultation
```bash
# Tech decisions, architecture questions, approach validation
codex exec "Given context X, should we use approach A or B? Consider: <factors>"
```

### Prompt Crafting
Claude decides how to prompt Codex. Guidelines:
- Be specific about what feedback you want
- Provide relevant context (file names, constraints, goals)
- For code review: mention what changed and why
- For decisions: frame the trade-offs clearly

## Review Loop Protocol

### Max Iterations: 3

Execute up to 3 rounds of Claude ↔ Codex exchange:

1. **Round 1**: Initial consultation
   - Send context + question/code to Codex
   - Receive Codex's feedback

2. **Round 2** (if disagreement): Counter-argument
   - If Claude disagrees with Codex's assessment, argue back
   - Provide reasoning for disagreement
   - Ask Codex to reconsider or clarify

3. **Round 3** (if still unresolved): Final exchange
   - Last attempt at consensus
   - If still disagreeing, note the impasse

### Disagreement Handling

**Do NOT blindly accept Codex feedback.** Evaluate critically:
- Does the suggestion align with project conventions?
- Is the concern valid given the specific context?
- Would the change actually improve the code/decision?

If Claude disagrees:
```bash
codex exec "You suggested X, but I disagree because Y. The context you may have missed: Z. Please reconsider or explain why X is still better."
```

### Iteration Limit Reached

If 3 rounds pass without consensus, notify user:
```
⚠️ Codex review: Reached iteration limit without consensus

**Point of contention**: [what we disagreed on]
**Claude's position**: [your stance + reasoning]
**Codex's position**: [their stance + reasoning]

Proceeding with: [which approach and why]
```

## Output Format

After consultation completes, summarize for user:

```markdown
## Codex Review Summary

**Consulted on**: [code changes | tech decision | architecture]

**Consensus reached**: Yes/No (N rounds)

### Key Points
- [Agreement 1]
- [Agreement 2]

### Disagreements (if any)
| Topic | Claude | Codex | Resolution |
|-------|--------|-------|------------|
| ... | ... | ... | ... |

### Final Decision
[What was decided and brief rationale]
```

## Invocation Modes

### Explicit: `/codex` or `/codex-review`
User explicitly requests peer review. Always execute full loop.

### Auto-trigger
When about to present alternatives or complete significant work:
1. Pause before responding to user
2. Run Codex consultation
3. Incorporate feedback (or note disagreement)
4. Then present to user with review summary

## Examples

### Code Review (Uncommitted Changes)
```bash
codex exec review --uncommitted "Review this authentication refactor. Key changes: moved from session-based to JWT. Check for security issues and edge cases."
```

### Architecture Decision
```bash
codex exec "Building a real-time notification system. Options: A) WebSockets with Redis pub/sub, B) Server-Sent Events with PostgreSQL NOTIFY, C) Polling with caching. Constraints: <1000 concurrent users, existing PostgreSQL infra, team familiar with Redis. Which approach and why?"
```

### Validating Trade-offs
```bash
codex exec "User asked for feature X. I'm proposing to implement it via Y because of Z. Are there approaches I'm missing? Any concerns with Y?"
```
