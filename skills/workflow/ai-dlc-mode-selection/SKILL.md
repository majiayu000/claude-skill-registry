---
name: ai-dlc-mode-selection
description: Use when deciding between HITL, OHOTL, and AHOTL modes in AI-DLC workflows. Covers decision frameworks for human involvement levels and mode transitions.
allowed-tools:
  - Read
  - Grep
  - Glob
---

# AI-DLC Mode Selection

AI-DLC supports three modes of human-AI collaboration. Choosing the right mode for each phase of work is critical for balancing productivity, quality, and control.

## The Three Modes

### HITL - Human In The Loop

Human actively participates in every decision.

**Characteristics:**
- Every action reviewed by human
- Synchronous collaboration
- Human makes final decisions
- AI proposes, human disposes

**When to Use:**
- Defining requirements (elaboration)
- Making architectural decisions
- Reviewing security-sensitive changes
- Course corrections when AI is off track

**Examples:**
```
User: "Add user authentication"
AI: "What authentication method? OAuth, email/password, or both?"
User: "Start with email/password, we'll add OAuth later"
AI: "Should we support 'remember me'?"
User: "Yes, 30-day sessions"
```

### OHOTL - Occasional Human Over The Loop

Human sets direction, AI operates with periodic checkpoints.

**Characteristics:**
- AI works autonomously on defined tasks
- Human reviews at milestones
- Human intervenes when stuck or for approval
- Balance of autonomy and oversight

**When to Use:**
- Building well-defined features
- Tasks with clear completion criteria
- When backpressure provides quality gates
- Medium-complexity work

**Examples:**
```
User: "Implement the login form based on these criteria"
AI: [Works autonomously]
AI: "Login form complete. Tests passing. Ready for review."
User: "Looks good, continue to the API integration"
```

### AHOTL - Autonomous Human Over The Loop

AI operates with minimal human involvement.

**Characteristics:**
- AI makes most decisions independently
- Human reviews only at completion or on exception
- Requires very clear criteria and robust backpressure
- Maximum autonomy

**When to Use:**
- Well-defined, routine tasks
- Tasks with comprehensive test coverage
- When all edge cases are known
- Low-risk changes

**Examples:**
```
User: "Implement all the CRUD endpoints for the User model"
AI: [Completes multiple iterations autonomously]
AI: "All endpoints implemented. 47 tests passing. PR ready."
User: "Merged."
```

## Mode Selection Framework

### Decision Matrix

| Factor | HITL | OHOTL | AHOTL |
|--------|------|-------|-------|
| Requirements clarity | Low | Medium | High |
| Risk level | High | Medium | Low |
| Test coverage | Low | Medium | High |
| Domain familiarity | Low | Medium | High |
| Reversibility | Difficult | Moderate | Easy |

### Questions to Ask

1. **How clear are the requirements?**
   - Vague → HITL
   - Mostly clear → OHOTL
   - Crystal clear → AHOTL

2. **What's the risk of mistakes?**
   - Security/data loss → HITL
   - User-facing bugs → OHOTL
   - Internal tooling → AHOTL

3. **How good is test coverage?**
   - No tests → HITL
   - Some tests → OHOTL
   - Comprehensive tests → AHOTL

4. **How familiar is the domain?**
   - New/complex domain → HITL
   - Familiar patterns → OHOTL
   - Routine work → AHOTL

5. **How reversible are changes?**
   - Database migrations → HITL
   - API changes → OHOTL
   - Internal refactoring → AHOTL

## Mode by Phase

### Default Workflow Modes

| Phase | Default Mode | Rationale |
|-------|--------------|-----------|
| Elaboration | HITL | Requires human input for requirements |
| Planning | HITL | Human should validate approach |
| Building | OHOTL | Autonomous with backpressure |
| Review | HITL | Human verification before completion |

### Mode Overrides

You can override defaults in `.ai-dlc/hats.yml`:

```yaml
hats:
  builder:
    mode: AHOTL  # Override to full autonomy
    instructions: |
      Work autonomously. Only stop if blocked.
```

## Transitioning Between Modes

### Upgrading Autonomy (HITL → OHOTL → AHOTL)

When to upgrade:
- Requirements have stabilized
- Test coverage is comprehensive
- Pattern is established
- Human has built trust

Example:
```
Session 1 (HITL): Define auth requirements together
Session 2 (HITL): Review initial implementation
Session 3 (OHOTL): AI implements remaining endpoints
Session 4 (AHOTL): AI handles routine CRUD operations
```

### Downgrading Autonomy (AHOTL → OHOTL → HITL)

When to downgrade:
- Unexpected complexity discovered
- AI making repeated mistakes
- Security concerns arise
- Requirements changed

Example:
```
AI operating in AHOTL...
AI: "I'm stuck on edge case X. Need clarification."
→ Downgrade to HITL for this issue
→ Resume OHOTL once resolved
```

## Mode Indicators

### Signs You're in the Wrong Mode

**Too much autonomy (should downgrade):**
- Repeated mistakes on similar issues
- Misunderstanding requirements
- Missing edge cases
- User frequently correcting course

**Too little autonomy (should upgrade):**
- User rubber-stamping every decision
- Routine, repetitive work
- Comprehensive test coverage exists
- AI consistently making good decisions

### Calibration Questions

Ask periodically:
- "Am I making decisions the human should make?"
- "Am I asking for approval on routine choices?"
- "Are my autonomous decisions causing rework?"
- "Is the human adding value at this checkpoint?"

## Mode-Specific Behaviors

### In HITL Mode

```markdown
- Ask before every significant decision
- Present options with trade-offs
- Wait for explicit approval
- Document decisions with rationale
```

### In OHOTL Mode

```markdown
- Make routine decisions autonomously
- Check in at milestones
- Ask when genuinely uncertain
- Save progress frequently (han keep)
```

### In AHOTL Mode

```markdown
- Make all decisions within criteria bounds
- Only interrupt for true blockers
- Log decisions for later review
- Complete full task before seeking feedback
```

## Backpressure by Mode

### HITL Backpressure

Human IS the backpressure:
- Every change reviewed
- Human catches issues immediately
- No automated gates needed

### OHOTL Backpressure

Mix of automated and human:
- Automated: tests, lint, types
- Human: milestone reviews, PR approval
- AI operates freely within automated bounds

### AHOTL Backpressure

Fully automated:
- Comprehensive test suite
- Strict type checking
- Automated code review tools
- CI/CD pipeline as final gate

## Examples

### Example 1: Security Feature

```yaml
phase: authentication
mode: HITL  # Security-sensitive
reason: |
  Authentication has security implications.
  Every decision needs human review.
```

### Example 2: UI Component

```yaml
phase: component_library
mode: OHOTL  # Balanced
reason: |
  Design system is established.
  AI implements, human reviews at milestones.
```

### Example 3: Data Migration Script

```yaml
phase: migration
mode: HITL  # High risk
reason: |
  Database changes are difficult to reverse.
  Human must verify each step.
```

### Example 4: Unit Tests

```yaml
phase: test_writing
mode: AHOTL  # Low risk
reason: |
  Tests are additive and easily reversible.
  Existing tests validate correctness.
```

## Summary

| Mode | Human Involvement | Use When |
|------|-------------------|----------|
| HITL | Every decision | High risk, unclear requirements |
| OHOTL | At milestones | Medium risk, clear criteria |
| AHOTL | At completion | Low risk, comprehensive tests |

**Default rule:** Start with HITL for new work, upgrade autonomy as trust builds and tests accumulate.
