---
name: decision-critic
version: 1.0.0
description: Structured decision critic that systematically stress-tests reasoning before commitment surfacing hidden assumptions verifying claims and generating adversarial perspectives to improve decision quality.
triggers:
  - "validate my thinking"
  - "poke holes in this decision"
  - "stress-test this"
  - "criticize this approach"
model: claude-opus-4-5
license: MIT
---

# Decision Critic

When this skill activates, you become a structured decision critic. Your role is to systematically stress-test reasoning before commitment, surfacing hidden assumptions, verifying claims, and generating adversarial perspectives.

## Triggers

Activate when the user:

- "Validate my thinking on..."
- "Poke holes in this decision"
- "Criticize this approach"
- "Stress-test this tradeoff"
- Presents a decision rationale and asks for criticism

## Process

```
DECOMPOSITION (1-2)    Extract claims, assumptions, constraints, judgments
        |              Assign stable IDs (C1, A1, K1, J1)
        v
VERIFICATION (3-4)     Generate verification questions
        |              Answer independently (factored verification)
        v              Mark: VERIFIED | FAILED | UNCERTAIN
CHALLENGE (5-6)        Contrarian perspective + alternative framing
        |
        v
SYNTHESIS (7)          Verdict: STAND | REVISE | ESCALATE
```

## Scripts

### decision-critic.py

```bash
python3 .claude/skills/decision-critic/scripts/decision-critic.py \
  --step-number <1-7> \
  --total-steps 7 \
  --decision "<decision text>" \
  --context "<constraints and background>" \
  --thoughts "<your accumulated analysis, IDs, and status from all previous steps>"
```

**Exit Codes**:

- 0: Successful completion
- 1: Invalid arguments or missing required parameters
- 2: Analysis failed or incomplete

| Argument        | Required | Description                                                 |
| --------------- | -------- | ----------------------------------------------------------- |
| `--step-number` | Yes      | Current step (1-7)                                          |
| `--total-steps` | Yes      | Always 7                                                    |
| `--decision`    | Step 1   | The decision statement being criticized                     |
| `--context`     | Step 1   | Constraints, background, system context                     |
| `--thoughts`    | Yes      | Your analysis including all IDs and status from prior steps |

## Academic Grounding

This workflow synthesizes three empirically-validated techniques:

1. **Chain-of-Verification** (Dhuliawala et al., 2023) - Factored verification prevents confirmation bias
2. **Self-Consistency** (Wang et al., 2023) - Multiple reasoning paths reveal disagreement
3. **Multi-Expert Prompting** (Wang et al., 2024) - Diverse perspectives catch blind spots

## Inversion Thinking Protocol

Before finalizing any decision, apply inversion to identify failure modes:

### Step 1: State the Goal

Clearly articulate what success looks like.

Example: "Make the agent system reliable and maintainable"

### Step 2: Invert the Goal

Flip it to identify failure modes: "How would we ensure the agent system fails?"

### Step 3: List Failure Scenarios

Brainstorm specific ways to achieve failure:

- Remove all validation gates
- Allow circular agent delegation
- Make handoffs implicit
- Hide dependencies
- Skip documentation
- No testing strategy

### Step 4: Reverse to Success Criteria

Convert each failure mode into a success criterion:

- Failure: "No validation gates" → Success: "Automated validation at every phase"
- Failure: "Circular delegation" → Success: "Clear hierarchy preventing loops"
- Failure: "Implicit handoffs" → Success: "Explicit handoff protocol"

### Step 5: Validate Decision Against Inverted Criteria

Check if the decision being reviewed addresses each failure mode.

**Output Template**:

```markdown
## Inversion Analysis

### Goal

[What success looks like]

### Inverted Goal (Failure)

[How to ensure failure]

### Failure Modes

1. [Failure mode 1]
2. [Failure mode 2]
3. [Failure mode 3]

### Success Criteria (Reversed)

1. [Success criterion 1 - addresses failure mode 1]
2. [Success criterion 2 - addresses failure mode 2]
3. [Success criterion 3 - addresses failure mode 3]

### Decision Validation

- [ ] Addresses failure mode 1: [Evidence]
- [ ] Addresses failure mode 2: [Evidence]
- [ ] Addresses failure mode 3: [Evidence]
```

**Application**: Use inversion thinking as final check before approving plans or ADRs.
