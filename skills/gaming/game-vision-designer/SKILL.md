---
name: Game Vision Designer
description: Evolve and maintain game vision through Q&A interviews and decision tracking. Use when exploring game concepts, validating feature alignment, or making design decisions.
---

# Game Vision Designer

The "north star" skill for Stapledon's Voyage. Maintains game vision docs, interviews the designer to evolve concepts, and validates that features align with core pillars.

## Quick Start

**Most common usage:**
```bash
# User says: "interview me about the game"
# This skill will:
# 1. Load current vision from docs/vision/
# 2. Ask probing questions to deepen understanding
# 3. Update vision docs based on answers
# 4. Log any design decisions made

# User says: "does this feature fit the vision?"
# This skill will:
# 1. Load core-pillars.md
# 2. Check alignment with each pillar
# 3. Report: ALIGNED / NEEDS DISCUSSION / CONFLICTS
```

## When to Use This Skill

Invoke this skill when:
- User says "interview me" about game concepts
- User asks "does [feature] fit the vision?"
- User wants to make or record a design decision
- User asks about core pillars or game direction
- Other skills need vision context for their work
- Starting a new major feature direction

## Available Scripts

### `scripts/init_vision_docs.sh`
Initialize the vision docs directory structure.

### `scripts/log_decision.sh <title> <decision> <rationale>`
Log a design decision to design-decisions.md.

### `scripts/check_pillars.sh`
Display current core pillars for quick reference.

## Workflow

### 1. Vision Interview Mode

When user wants to explore/evolve concepts:

1. **Load context** - Read existing `docs/vision/` docs
2. **Ask questions** - Pick 2-3 from the interview bank (see resources)
3. **Dig deeper** - Follow up with "why?" and "give an example"
4. **Update docs** - Revise core-pillars.md, log decisions, note open questions

### 2. Feature Validation Mode

When validating a feature against vision:

1. **Load pillars** - Read `docs/vision/core-pillars.md`
2. **Check each pillar**:
   - Does feature serve this pillar? How?
   - Does it conflict? How?
3. **Check decisions** - Any prior decisions relevant?
4. **Report** - ALIGNED / NEEDS DISCUSSION / CONFLICTS

### 3. Decision Logging Mode

When recording a design decision:

1. **Capture context** - Why did this come up?
2. **Document decision** - What was decided?
3. **Record rationale** - How does this serve the pillars?
4. **Note alternatives** - What was rejected and why?
5. **Update docs** - Append to design-decisions.md

## Vision Doc Structure

All vision docs go to `docs/vision/`:

| File | Purpose |
|------|---------|
| `core-pillars.md` | 3-5 non-negotiable design constraints |
| `design-decisions.md` | Log of decisions with rationale |
| `open-questions.md` | Unresolved design questions |
| `interview-log.md` | Q&A session history |

## Resources

### Interview Questions Bank
See [`resources/interview_questions.md`](resources/interview_questions.md) for full question bank organized by topic.

### Vision Doc Templates
See [`resources/vision_templates.md`](resources/vision_templates.md) for doc templates.

## Integration with Other Skills

- **sprint-planner**: Reads core-pillars.md before planning
- **design-doc-creator**: References pillars when designing features
- **sprint-executor**: Checks design-decisions.md for constraints

## Notes

- Pillars rarely change; if they do, document why
- Every feature must serve at least one pillar
- Be specific - vague pillars are useless
- This is collaborative - thought partner, not gatekeeper
