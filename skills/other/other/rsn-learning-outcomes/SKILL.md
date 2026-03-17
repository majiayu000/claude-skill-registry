---
name: rsn-learning-outcomes
description: Extracts insights and improves performance from experience. Applies single-loop (fix action), double-loop (fix frame), reflection (extract insight), experimentation (test belief), and calibration (adjust confidence) modes. Use when correcting mistakes, learning from outcomes, testing hypotheses, or improving predictions. Triggers on "why did this fail", "what can we learn", "test this", "how accurate are we", "pattern of failures".
license: Complete terms in LICENSE.txt
---

# Learning

Systematic improvement from experience. Convert outcomes into better future performance.

## Core Principle

Learning is not automatic. Experience without reflection is just repetition. Learning requires deliberate extraction of insight and updating of beliefs and behaviors.

```
Experience → Extract → Update → Apply → Better Outcomes
```

## Mode Selection

| Mode | Question | Output | Trigger |
|------|----------|--------|---------|
| **Single-loop** | Did action work? | Corrected action | Gap between expected/actual |
| **Double-loop** | Is frame right? | Updated frame | Pattern of single-loop failures |
| **Reflection** | What can we learn? | Transferable insights | Experience completed |
| **Experimentation** | Should we test this? | Validated/invalidated belief | Belief needs validation |
| **Calibration** | How accurate are we? | Adjusted confidence rules | Predictions need tuning |

## Decision Tree

```
Is there a gap between expected and actual?
  YES → Is this a pattern (3+ similar failures)?
    YES → Double-loop (question the frame)
    NO  → Single-loop (fix the action)
  NO  ↓
Has an experience completed?
  YES → Reflection (extract insights)
  NO  ↓
Do you have a belief that needs validation before commitment?
  YES → Experimentation (test the belief)
  NO  ↓
Have predictions been consistently off?
  YES → Calibration (adjust confidence)
  NO  → No learning mode needed
```

---

## Mode Summaries

### Single-Loop

**Purpose:** Correct action within existing frame.

**Mental model:** Thermostat — detect deviation, adjust action, return to target. The goal is not questioned.

**Process:** Gap detected → Diagnose cause → Identify correction → Verify fix → Prevent recurrence

**Key rules:**
- Fix the proximate cause
- Don't question the goal (yet)
- Add prevention to avoid repeat
- Check: is this a pattern? If yes → double-loop

**Output:** Corrected action with prevention

→ [references/single-loop.md](references/single-loop.md)

---

### Double-Loop

**Purpose:** Question and update the frame itself.

**Mental model:** Not just adjusting thermostat, but asking: "Is heating the right goal?"

**Process:** Pattern detected → Examine current frame → Challenge assumptions → Construct new frame → Validate change

**Key rules:**
- Requires 3+ single-loop failures (pattern)
- Articulate current frame (goals, assumptions, constraints)
- Challenge each element with evidence
- Test new frame before full commitment

**Output:** Updated frame with validation plan

→ [references/double-loop.md](references/double-loop.md)

---

### Reflection

**Purpose:** Extract transferable insight from experience.

**Mental model:** Mine the experience for reusable gold.

**Process:** Capture experience → Analyze what worked/didn't → Extract insights → Update beliefs → Create artifacts → Disseminate

**Key rules:**
- Reflection is scheduled, not accidental
- Analyze both successes and failures
- Specify conditions when insight applies
- Create persistent artifacts (heuristics, playbooks, checklists)

**Output:** Insights and artifacts for future use

→ [references/reflection.md](references/reflection.md)

---

### Experimentation

**Purpose:** Test belief through deliberate action before commitment.

**Mental model:** Scientific method applied to operational decisions.

**Process:** Formulate hypothesis → Design experiment → Execute → Analyze results → Conclude → Act

**Key rules:**
- Hypothesis must be falsifiable
- Define success criteria before testing
- Control variables where possible
- Don't peek at results early

**Output:** Validated or invalidated belief with next steps

→ [references/experimentation.md](references/experimentation.md)

---

### Calibration

**Purpose:** Adjust prediction confidence based on track record.

**Mental model:** Weather forecaster — when I say 80% confident, it should be right 80% of the time.

**Process:** Assemble track record → Stratify by confidence level → Calculate calibration error → Identify patterns → Define adjustment rules

**Key rules:**
- Need 30+ predictions for meaningful calibration
- Stratify by domain (calibration varies)
- Adjust gradually, not dramatically
- Monitor ongoing calibration

**Output:** Calibration adjustment rules

→ [references/calibration.md](references/calibration.md)

---

## Output Format

Every learning output includes:

```markdown
## [Mode]: [Topic]

**Trigger:** [What triggered this learning mode]

**Analysis:**
[Mode-specific analysis]

**Conclusion:**
[What was learned/changed]

**Artifacts:**
- [Any persistent outputs: rules, checklists, playbooks]

**Next:**
- [Actions to take]
- [What to monitor]
```

---

## Mode Transitions

| From | To | Trigger |
|------|----|---------|
| Single-loop | Double-loop | Pattern detected (3+ similar failures) |
| Double-loop | Experimentation | New frame needs validation |
| Experimentation | Reflection | Experiment completed |
| Reflection | Calibration | Predictions were off |
| Any | Single-loop | New gap detected |

## Learning → Other Skills Handoff

| Learning Output | Next Skill |
|-----------------|------------|
| Corrected action | Causal (execute) |
| New frame | Thinking (reason with new assumptions) |
| Insight about perception | Perceiving (adjust attention) |
| Validated hypothesis | Causal (plan rollout) |
| Calibration rule | All thinking modes (adjust confidence) |

---

## Anti-Patterns

| Avoid | Do Instead |
|-------|------------|
| No reflection time | Schedule deliberate reflection |
| Blame focus | Focus on system/process |
| Premature double-loop | Require pattern of failures |
| Peeking at experiment results | Wait for full duration |
| Over-adjusting calibration | Gradual adjustments |
| Insight hoarding | Plan dissemination |

---

## References

| File | Content |
|------|---------|
| [single-loop.md](references/single-loop.md) | Action correction within frame |
| [double-loop.md](references/double-loop.md) | Frame examination and update |
| [reflection.md](references/reflection.md) | Insight extraction process |
| [experimentation.md](references/experimentation.md) | Hypothesis testing methods |
| [calibration.md](references/calibration.md) | Confidence adjustment |
