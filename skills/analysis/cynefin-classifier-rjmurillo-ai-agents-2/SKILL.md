---
name: cynefin-classifier
version: 1.0.0
model: claude-sonnet-4-5
description: Classify problems into Cynefin Framework domains (Clear, Complicated, Complex, Chaotic, Confusion) and recommend appropriate response strategies. Use when unsure how to approach a problem, facing analysis paralysis, or needing to choose between expert analysis and experimentation.
license: MIT
metadata:
  framework: Cynefin (Dave Snowden)
---

# Cynefin Classifier

Classify problems into the correct Cynefin domain and recommend the appropriate response strategy. This prevents applying the wrong cognitive approach to problems.

## Triggers

Activate when the user:

- `classify this problem`
- `cynefin analysis`
- `what approach should we take`
- `should we analyze or experiment`
- `is this complex or complicated`

## When to Use

Use this skill when:

- Unsure how to approach a new problem (analyze vs experiment vs act)
- Facing analysis paralysis on a decision
- Team disagrees on whether to research more or start building
- Need to justify an experimental approach to stakeholders

Use [decision-critic](../decision-critic/SKILL.md) instead when:

- Problem is already classified as Complicated and you need to validate a specific decision
- You have a concrete proposal to challenge, not a general problem to classify

## The Cynefin Framework

```text
                    UNORDERED                          ORDERED
              ┌─────────────────────────────────┬─────────────────────────────────┐
              │         COMPLEX                 │        COMPLICATED              │
              │                                 │                                 │
              │  Cause-effect visible only      │  Cause-effect discoverable      │
              │  in retrospect                  │  through expert analysis        │
              │                                 │                                 │
              │  Response: PROBE-SENSE-RESPOND  │  Response: SENSE-ANALYZE-RESPOND│
              │  • Safe-to-fail experiments     │  • Expert consultation          │
 NOVEL        │  • Emergent practice            │  • Root cause analysis          │   KNOWN
              │  • Amplify what works           │  • Good practice                │
              ├─────────────────────────────────┼─────────────────────────────────┤
              │         CHAOTIC                 │          CLEAR                  │
              │                                 │                                 │
              │  No discernible cause-effect    │  Cause-effect obvious to all    │
              │  No time for analysis           │                                 │
              │                                 │  Response: SENSE-CATEGORIZE-    │
              │  Response: ACT-SENSE-RESPOND    │           RESPOND               │
              │  • Stabilize first              │  • Apply best practice          │
              │  • Novel practice               │  • Follow procedures            │
              │  • Then move to complex         │  • Standardize                  │
              └─────────────────────────────────┴─────────────────────────────────┘

                                    CONFUSION (center)
                              Domain unknown - gather information
```

## Process

### Step 1: Identify Cause-Effect Relationship

Ask: "Can we predict the outcome of an action?"

| If... | Then Domain is Likely... |
|-------|--------------------------|
| Anyone can predict outcome | Clear |
| Experts can predict outcome | Complicated |
| Outcome only knowable after action | Complex |
| No one can predict, crisis mode | Chaotic |
| Insufficient information to determine | Confusion |

### Step 2: Check Temporal State

Problems can move between domains:

- **Crisis → Stabilization**: Chaotic → Complex (after immediate action)
- **Learning → Optimization**: Complex → Complicated (after patterns emerge)
- **Maturity → Commoditization**: Complicated → Clear (after expertise codified)
- **Disruption → Uncertainty**: Clear → Complex/Chaotic (black swan event)

### Step 3: Validate with Diagnostic Questions

**Clear Domain Indicators:**

- Is there a documented procedure?
- Would a junior developer handle this the same way?
- Is this a "solved problem"?

**Complicated Domain Indicators:**

- Do we need an expert to analyze this?
- Are there multiple valid approaches requiring evaluation?
- Can we predict the outcome with sufficient analysis?

**Complex Domain Indicators:**

- Are multiple independent variables interacting?
- Has similar analysis failed to predict outcomes before?
- Do we need to "try and see"?

**Chaotic Domain Indicators:**

- Is there immediate harm occurring?
- Do we lack time for any analysis?
- Is the situation unprecedented?

## Output Format

```markdown
## Cynefin Classification

**Problem**: [Restate the problem concisely]

### Domain: [CLEAR | COMPLICATED | COMPLEX | CHAOTIC | CONFUSION]

**Confidence**: [HIGH | MEDIUM | LOW]

### Rationale

[2-3 sentences explaining why this domain based on cause-effect relationship]

### Response Strategy

**Approach**: [Sense-Categorize-Respond | Sense-Analyze-Respond | Probe-Sense-Respond | Act-Sense-Respond | Gather Information]

### Recommended Actions

1. [First specific action]
2. [Second specific action]
3. [Third specific action]

### Pitfall Warning

[Domain-specific anti-pattern to avoid]

### Related Considerations

- **Temporal**: [Will domain likely shift? When?]
- **Boundary**: [Is this near a domain boundary?]
- **Compound**: [Are sub-problems in different domains?]
```

## Domain-Specific Guidance

### Clear Domain

**When you see it**: Bug with known fix, style violation, typo, standard CRUD operation.

**Response**: Apply best practice immediately. Don't over-engineer.

**Pitfall**: Over-complicating simple problems. Creating abstractions where none needed.

**Software Examples**:

- Fixing a null reference with documented pattern
- Adding a missing import
- Correcting a typo in documentation
- Following established coding standards

### Complicated Domain

**When you see it**: Performance issue, security vulnerability assessment, architecture evaluation.

**Response**: Gather experts, analyze thoroughly, then act decisively.

**Pitfall**: Analysis paralysis OR acting without sufficient expertise.

**Software Examples**:

- Debugging a memory leak
- Evaluating database schema design
- Security audit of authentication flow
- Choosing between well-documented frameworks with clear trade-offs

### Complex Domain

**When you see it**: User behavior prediction, team dynamics, new technology adoption, architectural decisions with uncertainty.

**Response**: Run safe-to-fail experiments. Probe, sense patterns, respond. Amplify what works.

**Pitfall**: Trying to fully analyze before acting. Expecting predictable outcomes.

**Software Examples**:

- Deciding microservices vs monolith for new product
- Predicting which features users will adopt
- Evaluating emerging frameworks with limited production data
- Team restructuring impacts on productivity
- A/B testing user experience changes

### Chaotic Domain

**When you see it**: Production outage, data breach, critical security incident.

**Response**: Act immediately to stabilize. Restore order first. Analyze later.

**Pitfall**: Forming committees. Waiting for consensus. Deep analysis during crisis.

**Software Examples**:

- Database corruption with active users
- Active security breach
- Complete service outage
- Cascading infrastructure failure

### Confusion Domain

**When you see it**: Insufficient information to classify. Contradictory signals. Unknown unknowns.

**Response**: Gather information. Break problem into smaller pieces. Reclassify components.

**Pitfall**: Assuming a domain without evidence. Paralysis from uncertainty.

**Software Examples**:

- Vague requirement that could be simple or complex
- Bug report without reproduction steps
- Performance issue without metrics
- "System is slow" without specifics

## Integration with Other Skills

| Skill | Integration Point |
|-------|-------------------|
| decision-critic | After classifying as Complicated, use decision-critic to validate analysis |
| milestone-planner | After classifying as Complex, use milestone-planner to design experiments |
| architect | Complicated architectural decisions benefit from ADR process |
| analyst | Confusion domain benefits from analyst investigation |

## Compound Problems

When a problem spans multiple domains:

1. **Decompose** the problem into sub-problems
2. **Classify** each sub-problem independently
3. **Sequence** work by domain priority:
   - Chaotic first (stabilize)
   - Clear next (quick wins)
   - Complicated then (expert analysis)
   - Complex last (experiments need stable foundation)

## Scripts

### classify.py

Structured classification with validation.

```bash
python3 .claude/skills/cynefin-classifier/scripts/classify.py \
  --problem "Description of the problem" \
  --context "Additional context about constraints, environment"
```

**Exit Codes**:

- 0: Classification complete
- 1: Invalid arguments
- 2: Insufficient information (Confusion domain)

## Escalation Criteria

Escalate to human or senior decision-maker when:

- Confidence is LOW
- Problem is on domain boundary
- Stakes are high (production, security, data)
- Classification contradicts team consensus
- Chaotic domain with no runbook

## Examples

### Example 1: CI Test Failures

**Input**: "Tests pass locally but fail randomly in CI"

**Classification**: COMPLEX

**Rationale**: Multiple interacting factors (timing, environment, dependencies, parallelism) make cause-effect unclear. Analysis alone won't solve this.

**Strategy**: Probe-Sense-Respond

1. Add instrumentation to failing tests
2. Run experiments with different configurations
3. Look for patterns, amplify what works

**Pitfall**: Don't spend weeks trying to "root cause" before experimenting.

### Example 2: Production Database Down

**Input**: "Production database is unresponsive, customers cannot access the site"

**Classification**: CHAOTIC

**Rationale**: Active harm occurring. No time for analysis. Stabilization required.

**Strategy**: Act-Sense-Respond

1. Execute failover runbook immediately
2. Restore service using backup/replica
3. Only after stable: investigate root cause

**Pitfall**: Don't form a committee. Don't start analyzing before acting.

### Example 3: Framework Choice

**Input**: "Should we use React or Vue for our new frontend?"

**Classification**: COMPLEX

**Rationale**: Team dynamics, learning curves, ecosystem fit, and long-term maintainability only emerge through experience. Trade-off analysis alone is insufficient.

**Strategy**: Probe-Sense-Respond

1. Build small prototype with each (timeboxed)
2. Measure team velocity and satisfaction
3. Let experience inform decision

**Pitfall**: Don't try to "perfectly analyze" all trade-offs in spreadsheet.

### Example 4: Memory Leak

**Input**: "Application memory grows steadily over 24 hours"

**Classification**: COMPLICATED

**Rationale**: Cause-effect is discoverable through expert analysis. Heap dumps, profiling, and code review will reveal the source.

**Strategy**: Sense-Analyze-Respond

1. Collect heap dumps at intervals
2. Analyze object retention with profiler
3. Expert review of suspected areas

**Pitfall**: Don't guess and patch. Systematic analysis will find root cause.

### Example 5: Vague Bug Report

**Input**: "The app feels slow sometimes"

**Classification**: CONFUSION

**Rationale**: Insufficient information to determine domain. Could be Clear (known fix), Complicated (needs profiling), or Complex (user perception).

**Strategy**: Gather Information

1. What operations feel slow?
2. What device/network conditions?
3. Can it be reproduced?
4. What does "slow" mean (seconds? milliseconds?)

**Next Step**: Reclassify once information gathered.

## References

- [Cynefin Framework](references/cynefin-deep-dive.md) - Dave Snowden's original framework
- [Domain Transitions](references/domain-transitions.md) - How problems move between domains
- [Software Engineering Applications](references/software-applications.md) - Domain patterns in software

## Verification

After classification:

- [ ] Domain identified with confidence level (HIGH/MEDIUM/LOW)
- [ ] Rationale explains cause-effect relationship
- [ ] Response strategy matches the domain (not borrowed from another)
- [ ] Recommended actions are specific, not generic
- [ ] Compound problems decomposed into sub-problems with individual classifications

## Anti-Patterns

| Anti-Pattern | Description | Consequence |
|--------------|-------------|-------------|
| **Complicated-izing Complexity** | Applying analysis to emergent problems | Analysis paralysis, wasted effort |
| **Simplifying Complicated** | Skipping expert analysis for nuanced problems | Rework, technical debt |
| **Analyzing Chaos** | Forming committees during crisis | Prolonged outage, increased damage |
| **Experimenting on Clear** | Running A/B tests on solved problems | Wasted time, unnecessary risk |
| **Guessing Confusion** | Assuming domain without evidence | Wrong approach, compounded problems |
