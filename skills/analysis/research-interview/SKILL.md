---
name: research-interview
description: >
  Quick entry point for structured knowledge elicitation with epistemic tracking.
  PROACTIVELY activate for: (1) interviews and requirements gathering, (2) problem definition,
  (3) domain knowledge capture, (4) stakeholder elicitation, (5) assumptions surfacing.
  Triggers: "research interview", "elicit knowledge", "gather requirements", "define problem",
  "interview stakeholder", "capture domain knowledge"
argument-hint: [topic]
---

# Research Interview

Structured knowledge elicitation with epistemic tracking for problem definition and requirements gathering.

## When to Use

Use this skill when you need to:
- Elicit knowledge from stakeholders or domain experts
- Define a problem space systematically
- Gather requirements with confidence tracking
- Surface hidden assumptions and constraints
- Capture domain knowledge for later research

## Workflow

Invoke the `research-interviewer` skill for: "$ARGUMENTS"

### Default Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `output_format` | PROBLEM-STATEMENT | Default; produces actionable problem definition |
| `confidence_threshold` | 0.85 | High confidence required for conclusions |
| `validation_mode` | balanced | Mix of challenging and supportive questioning |
| `epistemic_tracking` | enabled | Track certainty levels throughout |

### Output Formats

Select based on your goal:
- **PROBLEM-STATEMENT** - Clear problem definition with constraints and success criteria
- **REQUIREMENTS** - Structured requirements with priority and confidence levels
- **KNOWLEDGE-CORPUS** - Domain knowledge capture for research continuation

### Interview Techniques Applied

1. **Open-ended exploration** - Surface the problem space
2. **Assumption challenging** - Identify hidden constraints
3. **Edge case probing** - Find boundary conditions
4. **Confidence calibration** - Assess certainty levels
5. **Gap identification** - Find missing information

### Epistemic Labels

All findings are tagged with confidence:
- **VERIFIED** - Confirmed by multiple sources or evidence
- **STATED** - Reported but not independently verified
- **INFERRED** - Derived from other information
- **SPECULATIVE** - Hypothesis requiring validation
- **UNKNOWN** - Explicit knowledge gap

## Output Format

The research interview produces structured output:

```xml
<interview-output>
  <header>
    <id>[unique identifier]</id>
    <topic>$ARGUMENTS</topic>
    <format>[PROBLEM-STATEMENT|REQUIREMENTS|KNOWLEDGE-CORPUS]</format>
  </header>

  <findings>
    <finding confidence="[0.0-1.0]" epistemic="[VERIFIED|STATED|INFERRED|SPECULATIVE]">
      [Key finding or requirement]
    </finding>
    <!-- ... more findings ... -->
  </findings>

  <assumptions>
    <assumption status="[confirmed|challenged|unknown]">
      [Assumption that was surfaced]
    </assumption>
  </assumptions>

  <gaps>
    <gap priority="[high|medium|low]">
      [Information still needed]
    </gap>
  </gaps>

  <next-steps>
    1. [Recommended follow-up action]
    2. [Additional research needed]
  </next-steps>
</interview-output>
```

## Quality Gates

- [ ] Topic is clearly defined and scoped
- [ ] Key assumptions have been surfaced and examined
- [ ] Confidence levels assigned to all findings
- [ ] Information gaps explicitly identified
- [ ] Next steps actionable and specific
- [ ] Output ready for research-brief input

## Workflow Integration

This skill is the first step in the research pipeline:

```
/research-interview → /research-brief → /consolidate-research
     (elicit)            (design)           (synthesize)
```

After completing a research interview, consider:
- Run `/research-brief` with the problem statement to design multi-LLM research
- Run `/evaluate-schema` if the topic involves data modeling
- Run `/compare-options` if multiple solutions were identified
