---
name: decision-logging
description: Capture architectural and implementation decisions with rationale to prevent re-debating. Creates and maintains DECISIONS.md.
---

# Decision Logging Skill

// Project Autopilot - Decision Documentation
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

**Purpose:** Record decisions with full context so future sessions don't re-debate settled issues, rationale is preserved, and decision impact is trackable.

---

## Why Decision Logging?

Without decision logging:
- Same questions asked repeatedly across sessions
- Rationale lost, leading to reversals without understanding
- Time wasted re-debating settled issues
- Context lost when decisions need to be revisited

With decision logging:
- Decisions preserved with full context
- Alternatives considered are documented
- Future sessions can read and understand past decisions
- Easy to revisit decisions when requirements change

---

## DECISIONS.md Location

```
.autopilot/DECISIONS.md
```

This file is automatically created and updated by the decision logging system.

---

## DECISIONS.md Template

```markdown
# Project Decisions

// Project Autopilot - Decision Log
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

**Project:** {project_name}
**Last Updated:** {timestamp}

---

## Decision Index

| ID | Title | Date | Status | Phase |
|----|-------|------|--------|-------|
| D001 | Auth Provider Selection | 2026-01-29 | Final | 1 |
| D002 | State Management Approach | 2026-01-29 | Final | 1 |
| D003 | Database Schema Design | 2026-01-29 | Final | 2 |

---

## D001: Auth Provider Selection

**Date:** 2026-01-29
**Status:** Final
**Owner:** {user}
**Phase:** 1

### Context
We need to implement user authentication for the application. Multiple providers
are available, each with different trade-offs in terms of features, cost, and
development complexity.

### Options Considered
| Option | Pros | Cons |
|--------|------|------|
| Supabase Auth | Built-in with DB, free tier, easy setup | Less customizable |
| Clerk | Best DX, beautiful pre-built UI | Paid after 10k MAU |
| Auth.js | Full control, free | More implementation work |
| Custom JWT | Complete flexibility | Security responsibility |

### Decision
**Selected:** Supabase Auth

### Rationale
1. Already using Supabase for database - natural fit
2. Free tier sufficient for MVP and initial growth
3. Built-in security best practices
4. Minimal implementation time

### Consequences
**Positive:**
- Fast implementation (hours vs days)
- Security handled by Supabase team
- Integration with row-level security

**Trade-offs:**
- Vendor lock-in to Supabase ecosystem
- Less customizable than Auth.js
- May need migration if exceeding free tier

### Related Decisions
- D003: Database schema (influenced by this)
- D007: API authentication (builds on this)

---

## D002: State Management Approach

**Date:** 2026-01-29
**Status:** Final
**Owner:** {user}
**Phase:** 1

### Context
The application needs client-side state management for UI state, caching,
and server state synchronization.

### Options Considered
| Option | Pros | Cons |
|--------|------|------|
| Redux | Battle-tested, dev tools | Boilerplate, complexity |
| Zustand | Simple, minimal boilerplate | Less ecosystem |
| Jotai | Atomic, React-native feel | Learning curve |
| React Query only | Server state handled | No client state |

### Decision
**Selected:** Zustand + React Query

### Rationale
1. Zustand for simple client state (UI, preferences)
2. React Query for server state (API caching, sync)
3. Minimal boilerplate, familiar patterns
4. Excellent TypeScript support

### Consequences
**Positive:**
- Clean separation of client vs server state
- Minimal bundle size
- Easy to understand and maintain

**Trade-offs:**
- Two libraries to learn
- Less unified than Redux

### Related Decisions
- D005: Component architecture (influenced by this)

---
```

---

## Decision Capture Protocol

### When to Capture Decisions

Capture a decision when:
- Multiple valid approaches exist
- The choice has lasting implications
- Future sessions might question the choice
- The decision affects architecture or patterns

### Decision Capture Function

```
FUNCTION captureDecision(context, options, selected, rationale):
    """
    Capture a decision with full context.
    """
    # Generate decision ID
    decisions = loadDecisions()
    id = "D" + String(decisions.length + 1).padStart(3, "0")

    # Build decision object
    decision = {
        id: id,
        title: context.title,
        date: now().format("YYYY-MM-DD"),
        status: "Final",
        owner: getCurrentUser() OR "Claude",
        phase: context.phase OR null,
        context: context.description,
        options: options,
        selected: selected,
        rationale: rationale,
        consequences: {
            positive: inferPositiveConsequences(selected, options),
            tradeoffs: inferTradeoffs(selected, options)
        },
        related: context.related_decisions OR []
    }

    # Append to DECISIONS.md
    appendToDecisionsFile(decision)
    updateDecisionIndex(decision)

    LOG "✅ Decision captured: {id} - {decision.title}"

    RETURN id
```

### Auto-Capture During Discussion

```
FUNCTION captureFromDiscussion(gray_area, user_selection):
    """
    Automatically capture decisions during /autopilot:discuss.
    """
    IF user_selection.is_significant:
        context = {
            title: gray_area.label,
            description: gray_area.question,
            phase: current_phase
        }

        options = gray_area.options.map(opt => ({
            name: opt.label,
            pros: opt.pros OR ["N/A"],
            cons: opt.cons OR ["N/A"]
        }))

        selected = user_selection.option.label
        rationale = user_selection.explanation OR "User preference"

        captureDecision(context, options, selected, rationale)
```

---

## Re-Debate Prevention

### Checking for Prior Decisions

```
FUNCTION checkForPriorDecision(topic):
    """
    Check if a decision has already been made on this topic.
    Prevents re-debating settled issues.
    """
    decisions = loadDecisions()

    FOR each decision IN decisions:
        # Semantic similarity check
        similarity = semanticSimilarity(topic, decision.title)

        IF similarity > 0.8:
            RETURN {
                found: true,
                decision: decision,
                message: formatPriorDecisionMessage(decision)
            }

        # Check for keyword matches
        IF containsKeywords(topic, decision.title) OR
           containsKeywords(topic, decision.context):
            RETURN {
                found: true,
                decision: decision,
                message: formatPriorDecisionMessage(decision)
            }

    RETURN {found: false}

FUNCTION formatPriorDecisionMessage(decision):
    """
    Format a message about a prior decision.
    """
    message = """
This was decided in {decision.id}: {decision.title}

**Decision:** {decision.selected}
**Rationale:** {decision.rationale}

To revisit this decision, use:
/autopilot:decision revisit {decision.id}
"""
    RETURN message
```

### Re-Debate Response

When a topic matches a prior decision:

```
User: "Should we use Redux for state management?"

Claude: "This was decided in D002: State Management Approach.

**Decision:** Zustand + React Query
**Rationale:** Clean separation of client vs server state, minimal boilerplate

To revisit this decision, use:
/autopilot:decision revisit D002"
```

---

## Decision Revisit Protocol

### When to Revisit

Decisions can be revisited when:
- Requirements have fundamentally changed
- New information invalidates assumptions
- Significant time has passed and landscape changed
- Implementation revealed unforeseen issues

### Revisit Function

```
FUNCTION revisitDecision(decision_id, reason):
    """
    Mark a decision for revisit and document why.
    """
    decisions = loadDecisions()
    decision = decisions.find(d => d.id == decision_id)

    IF NOT decision:
        ERROR "Decision not found: {decision_id}"

    # Add revisit note
    decision.status = "Under Review"
    decision.revisit = {
        date: now(),
        reason: reason,
        original_decision: decision.selected,
        original_rationale: decision.rationale
    }

    updateDecision(decision)

    LOG "Decision {decision_id} marked for revisit"
    LOG "Original: {decision.selected}"
    LOG "Reason for revisit: {reason}"

    # Start new discussion
    RETURN startDecisionDiscussion(decision)
```

---

## Integration Points

### With /autopilot:discuss

```
discuss.md integrates:
    - Check for prior decisions before asking questions
    - Auto-capture significant decisions
    - Link decisions to phases
```

### With /autopilot:takeoff

```
build.md integrates:
    - Check decisions before making architectural choices
    - Reference decisions in code comments where relevant
    - Update decisions if implementation reveals issues
```

### With /autopilot:cockpit

```
resume.md loads:
    - All decisions for context
    - Pending decisions needing resolution
    - Recent decisions for reference
```

### With /autopilot:plan

```
plan.md reads:
    - Architectural decisions for planning
    - Technology decisions for task estimation
    - Prior decisions to avoid re-deciding
```

---

## Commands

### View Decisions

```bash
/autopilot:decisions list
/autopilot:decisions list --phase=3
/autopilot:decisions show D001
```

### Search Decisions

```bash
/autopilot:decisions search "authentication"
/autopilot:decisions search --keyword=database
```

### Revisit Decision

```bash
/autopilot:decisions revisit D001 --reason="New requirements"
```

### Add Decision

```bash
/autopilot:decisions add
# Interactive prompt for decision details
```

---

## Decision Categories

### Architectural Decisions
- Framework selection
- Database choice
- API design patterns
- Deployment architecture

### Implementation Decisions
- Library selection
- Code organization
- Error handling approach
- Testing strategy

### Process Decisions
- Workflow choices
- Review process
- Deployment frequency
- Documentation approach

### Trade-off Decisions
- Build vs buy
- Performance vs simplicity
- Flexibility vs speed
- Cost vs features

---

## Output Formats

### Compact (for conversation)

```
📋 Decision D001: Auth Provider
├─ Selected: Supabase Auth
├─ Rationale: Built-in with DB, minimal setup
└─ Status: Final (2026-01-29)
```

### Detailed (for review)

```markdown
## D001: Auth Provider Selection

**Status:** Final
**Date:** 2026-01-29
**Phase:** 1

### Decision
Supabase Auth

### Why
1. Already using Supabase for database
2. Free tier sufficient for MVP
3. Built-in security best practices

### Trade-offs Accepted
- Vendor lock-in to Supabase
- Less customizable than custom solution

### Affects
- D003: Database schema
- D007: API authentication
```

---

## Best Practices

### Writing Good Decisions

**DO:**
- Capture context: Why was this decision needed?
- List all options considered, not just the chosen one
- Document rationale with specific reasons
- Note consequences (both positive and negative)
- Link related decisions

**DON'T:**
- Skip the "why" - future you will wonder
- Omit rejected options - understanding why they were rejected is valuable
- Make decisions without documenting
- Leave decisions as "pending" indefinitely

### Decision Quality Checklist

- [ ] Title clearly describes the decision
- [ ] Context explains why decision was needed
- [ ] At least 2 options were considered
- [ ] Each option has pros and cons
- [ ] Rationale explains why selected option was chosen
- [ ] Consequences (positive and trade-offs) documented
- [ ] Related decisions linked
