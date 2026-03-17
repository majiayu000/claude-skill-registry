---
name: spec
description: Refine product specs through parallel adversarial agents - multiple perspectives catch what any single review would miss
---

# Spec Refinement

Multi-agent adversarial review for product specs. Parallel agents with different personas critique your spec until consensus.

**Why this matters:** A single reviewer will miss things. Multiple perspectives - skeptic, implementer, user advocate, security engineer - will catch gaps, challenge assumptions, and surface edge cases. The result is a document that has survived rigorous review before you write a single line of code.

**Dogfooding:** This skill uses JFL's own multi-agent infrastructure. No external API keys needed. Parallel Task agents debate using the same Claude that powers everything else.

## Usage

```
/spec                           # Start from scratch - describe what to build
/spec ./docs/my-spec.md         # Refine an existing spec
/spec --interview               # Deep requirements gathering first
/spec --focus security          # Focus critique on security concerns
```

## On Skill Invoke

### Step 1: Determine Input

**If user provided a file path:**
- Read the file
- Use as starting spec

**If user said --interview:**
- Start interview mode (see Interview section below)

**If user just described what to build:**
- Ask 2-4 clarifying questions first
- Draft initial spec based on answers
- Show draft for approval before debate

### Step 2: Select Document Type

```
What type of document?

1. PRD - Product requirements (for stakeholders, PMs)
2. Tech Spec - Technical architecture (for engineers)
```

### Step 3: Select Personas

```
Which perspectives should review this spec?
(More = more rigorous review)

[x] Skeptic - challenges assumptions, asks "why not X?"
[x] Implementer - cares about buildability, edge cases
[x] User Advocate - focuses on UX, accessibility, real usage
[ ] Security Engineer - thinks like an attacker
[ ] Oncall Engineer - cares about debugging at 3am
[ ] Junior Developer - flags ambiguity, missing context
[ ] Product Manager - user value, success metrics
[ ] QA Engineer - missing test scenarios, failure modes
```

Default: Skeptic + Implementer + User Advocate (3 perspectives)

### Step 4: Run Parallel Critique

**Spawn Task agents in parallel, each with their persona:**

```
Launching 3 agents in parallel:

[Skeptic]      Challenging assumptions...
[Implementer]  Checking buildability...
[User Advocate] Evaluating UX...
```

Each agent receives:
- The spec content
- Their persona description
- Instructions to critique independently
- Focus area if specified (--focus security, etc.)

**Example agent prompts:**

**Skeptic Agent:**
```
You are a skeptical technical reviewer. Your job is to challenge assumptions and ask "why not X?"

Read this spec and identify:
1. Assumptions that aren't justified
2. Alternative approaches not considered
3. Potential failure modes
4. Questions that should be answered before building
5. Scope that could be cut

Be constructively critical. Don't just criticize - suggest alternatives.

SPEC:
<spec content>
```

**Implementer Agent:**
```
You are a senior engineer who will build this. Your job is to evaluate buildability.

Read this spec and identify:
1. Missing technical details needed to implement
2. Edge cases not covered
3. Integration points that are underspecified
4. Performance concerns
5. Dependencies and ordering constraints
6. Ambiguous requirements

Be specific about what's missing. Give examples of edge cases.

SPEC:
<spec content>
```

**User Advocate Agent:**
```
You are a UX-focused product person. Your job is to advocate for real users.

Read this spec and identify:
1. User journeys that are incomplete
2. Error states not handled
3. Accessibility concerns
4. Mobile vs desktop gaps
5. Onboarding friction
6. Confusing terminology

Think about actual humans using this. What will frustrate them?

SPEC:
<spec content>
```

### Step 5: Synthesize Critiques

After all agents complete, synthesize their feedback:

```
## Critique Summary

### Skeptic raised:
- [concern 1]
- [concern 2]

### Implementer raised:
- [concern 1]
- [concern 2]

### User Advocate raised:
- [concern 1]
- [concern 2]

## Overlapping concerns (multiple agents flagged):
- [high priority issue]

## Questions that need answers:
- [question 1]
- [question 2]
```

### Step 6: Get User Input on Questions

If agents raised questions that need user input:

```
The reviewers raised some questions:

1. What are your expected traffic patterns for rate limiting?
2. Should offline mode be supported?
3. What happens if the WebSocket disconnects mid-huddle?

Your answers:
```

### Step 7: Revise Spec

Based on critiques and user input:
1. Address each concern raised
2. Add missing details
3. Clarify ambiguities
4. Document decisions made

Show the revised spec sections.

### Step 8: Validate (Optional Second Round)

```
Run another round of review?

[Yes - full review]  [Yes - quick check]  [No - spec is ready]
```

If yes, spawn agents again on revised spec. Repeat until consensus or user is satisfied.

### Step 9: Output Final Spec

When done:
- Write to `product/SPEC.md` or user-specified location
- Show summary of rounds and refinements
- Offer to continue to tech spec if PRD was just completed

---

## Interview Mode

Deep requirements gathering before drafting. Covers:

1. **Problem & Context** - What are we solving? Who has this pain?
2. **Users & Stakeholders** - All user types, technical levels, concerns
3. **Functional Requirements** - Core user journey, decision points, edge cases
4. **Technical Constraints** - Integrations, performance, scale, compliance
5. **UI/UX** - Desired experience, critical flows, mobile vs desktop
6. **Tradeoffs** - What gets cut first? Build vs buy?
7. **Risks** - What could cause failure? What assumptions might be wrong?
8. **Success Criteria** - How do we know it worked? What metrics?

After interview, synthesize into complete spec, then run through adversarial review.

---

## Focus Modes

Direct critique toward specific concerns:

```
/spec --focus security      # Auth, validation, encryption, vulnerabilities
/spec --focus scalability   # Horizontal scaling, sharding, caching
/spec --focus performance   # Latency, throughput, optimization
/spec --focus ux            # User journeys, error states, accessibility
/spec --focus reliability   # Failure modes, circuit breakers, recovery
/spec --focus cost          # Infrastructure costs, resource efficiency
```

When focus is specified, agents weight that area more heavily in their critique.

---

## Persona Definitions

### Skeptic
- Challenges every assumption
- Asks "why not just use X?"
- Identifies scope creep
- Questions necessity of features
- Suggests simpler alternatives

### Implementer
- Focuses on buildability
- Catches edge cases
- Identifies missing technical specs
- Thinks about testing
- Flags integration complexity

### User Advocate
- Thinks about real usage
- Catches UX friction
- Advocates for accessibility
- Identifies confusing flows
- Focuses on error states

### Security Engineer
- Thinks like an attacker
- Reviews auth/authz
- Identifies injection points
- Checks data handling
- Reviews trust boundaries

### Oncall Engineer
- Cares about observability
- Wants clear error messages
- Thinks about debugging at 3am
- Asks about runbooks
- Flags monitoring gaps

### Junior Developer
- Flags unclear context
- Identifies assumed knowledge
- Asks "dumb" questions
- Catches jargon
- Wants more examples

### Product Manager
- Focuses on user value
- Asks about success metrics
- Prioritizes features
- Thinks about launch
- Identifies missing stakeholders

### QA Engineer
- Thinks about test scenarios
- Identifies failure modes
- Asks about data states
- Catches race conditions
- Wants acceptance criteria

---

## The Flow

```
You describe what to build
        ↓
(Optional) Interview mode for deep requirements
        ↓
Claude drafts initial spec
        ↓
Parallel agents critique (3+ perspectives)
        ↓
Synthesize feedback + get user input on questions
        ↓
Revise spec
        ↓
(Optional) Another round until consensus
        ↓
Final spec output
        ↓
Ready to build
```

---

## Why Before Building

This is agents working together to catch what a single review misses.

Before writing code:
- Edge cases surfaced
- Assumptions challenged
- Gaps identified
- Clarifying questions asked

The spec that survives adversarial review is the spec worth building.

---

## Integration with JFL

After spec is finalized:
- Save to `product/SPEC.md` or appropriate location
- Reference during build for decisions already made
- Update as implementation reveals new questions

The spec becomes part of the context layer - persistent knowledge that survives sessions.

---

## Example Output

```
## Spec Review Complete

Rounds: 2
Personas: Skeptic, Implementer, User Advocate

### Key refinements made:
1. Added WebSocket reconnection handling (Implementer)
2. Clarified mobile-first approach (User Advocate)
3. Removed over-engineered participant limit system (Skeptic)
4. Added error states for all async operations (Implementer)
5. Defined success metrics (User Advocate)

### Concerns addressed:
- 8 edge cases documented
- 3 security considerations added
- 2 features descoped to v2

### Remaining open questions (for implementation):
- Exact voice transcription service TBD
- Rate limiting thresholds need load testing

Spec saved to: product/HUDDLE_SPEC.md
```
