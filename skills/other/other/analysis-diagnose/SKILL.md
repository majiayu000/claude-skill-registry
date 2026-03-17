---
name: analysis-diagnose
agent: explore
context: fork
description: "Perform systematic root cause investigation through 4-phase process. Use when encountering bugs, test failures, or unexpected behavior. Includes evidence gathering, hypothesis formation, testing protocols, and solution justification. Not for trivial fixes, creative experimentation, learning new systems, or implementing solutions."
---

<mission_control>
<objective>Perform systematic root cause investigation through evidence gathering, hypothesis formation, testing, and solution justification.</objective>
<success_criteria>
- Symptom documented with exact error messages and reproduction steps
- Evidence gathered: logs, git history, environment data, diagnostics
- Single hypothesis formed based on evidence (not assumptions)
- Minimal reproduction test created to verify hypothesis
- Root cause identified with file:line evidence
- Fix strategy documented with verification approach
</success_criteria>
<semantic_anchors>
- **Single Hypothesis**: Test one theory at a time for clear verification
- **5 Whys**: Iterative "why" questioning to reach actionable root cause
- **Pattern Recognition**: 3+ failures indicate systemic vs isolated issue
- **Evidence-Based**: All claims require file reads or diagnostic output
</semantic_anchors>
</mission_control>

## Quick Start

Bug encountered → Document symptom → Gather evidence → Form single hypothesis → Test with minimal reproduction → Identify root cause → Implement fix

## Navigation

| If you need... | Read this section... |
| :--- | :--- |
| Run diagnosis | ## Quick Start |
| 4-phase process | ## Diagnostic Flow |
| Semantic anchors | ## Semantic Anchors |
| Troubleshooting | ## Troubleshooting |
| Validation | ## Validation Checklist |

## Semantic Anchors

### Single Hypothesis Protocol

Test one theory at a time for clear verification. Multiple simultaneous hypotheses create uncertainty about which fix worked.

**Process:**
1. Form hypothesis based on evidence (not assumptions)
2. Create minimal reproduction test
3. Confirm or reject
4. Only then move to next hypothesis

**Example:**
```
Hypothesis: "Request size exceeds limit"
Test: Send request with 151 items, expect 500 error
Result: Confirmed
Next: Implement maxItems validation
```

### 5 Whys Technique

Iterative questioning to reach actionable root cause. Each "why" drills deeper from symptom to cause.

**Process:**
```
Problem: [Observable symptom]

Why 1: [First-level cause]
→ Because [explanation]

Why 2: [Second-level cause]
→ Because [explanation]

Why 3: [Third-level cause]
→ Because [explanation]

Why 4: [Fourth-level cause]
→ Because [explanation]

Why 5: [Root cause]
→ Because [explanation]

Root Cause: [The fundamental issue]
Action: [What to fix to prevent recurrence]
```

**Guidelines:**
- Be specific — each answer factual and verifiable
- Avoid blame — focus on systems and processes
- Check logic — ensure each answer explains the previous level
- Stop at actionable — when you reach something you can fix

### Pattern Recognition

Distinguish isolated bugs from architectural problems.

**Isolated Issue:**
- Single component affected
- Reproducible with specific input
- No cascade effects
- Local fix sufficient

**Systemic Problem:**
- Multiple components affected
- Architecture-level issue
- State management problem
- Integration failure

**Decision rule:** 3+ similar failures = systemic problem requiring architectural review, not localized patches.

### Evidence-Based Investigation

Every claim requires verification:
- File reads for code analysis
- Diagnostic output for system state
- Git history for recent changes
- No assumptions about what's "obvious"

## Diagnostic Flow

### Phase 1: State the Problem

Document symptom before investigating:
- Exact error messages
- Stack traces
- Reproduction steps
- Frequency (Always/Sometimes/Once)

### Phase 2: Gather Evidence

Collect proof, don't assume:
- **Logs**: Error output, console logs
- **Recent changes**: `git log --oneline -10`
- **Environment**: OS, versions, dependencies
- **Diagnostics**: Test output, build status

**Temporal analysis:** When did this first occur? What changed between working and broken?

**Backward tracing:** Start from error, trace call stack to failure point, find root cause upstream.

### Phase 3: Form Hypothesis

Single hypothesis based on evidence.

**Good hypothesis:**
- Based on evidence from Phase 2
- Falsifiable (can be proven wrong)
- Specific (predicts exact behavior)
- Actionable (suggests concrete fix)

**Bad hypothesis:**
- Multiple competing theories
- Based on assumptions, not evidence
- Too vague to test

### Phase 4: Test & Conclude

Minimal reproduction test before full fix.

**Process:**
1. Create smallest test that confirms hypothesis
2. Verify expected vs actual result
3. If confirmed: implement fix
4. If rejected: return to Phase 3 with new hypothesis
5. After fix: verify no regressions

## Investigation Format

```xml
<investigation>
  <symptom>
    <description>[Observable problem]</description>
    <error_messages>[Complete error text]</error_messages>
    <reproduction_steps>[Exact steps]</reproduction_steps>
    <frequency>[Always/Sometimes/Once]</frequency>
  </symptom>

  <evidence>
    <logs>[Relevant log output]</logs>
    <recent_changes>[Git diff, commits]</recent_changes>
    <environment_data>[OS, versions]</environment_data>
    <diagnostic_output>[Diagnostic commands]</diagnostic_output>
  </evidence>

  <hypothesis>
    <root_cause>[Likely root cause]</root_cause>
    <reasoning>[Why this causes symptom]</reasoning>
    <confidence>[High/Medium/Low]</confidence>
  </hypothesis>

  <test>
    <minimal_reproduction>[Smallest test]</minimal_reproduction>
    <expected_result>[What should happen]</expected_result>
    <actual_result>[What actually happened]</actual_result>
    <conclusion>[Confirmed/Rejected]</conclusion>
  </test>
</investigation>
```

## Troubleshooting

| Symptom | Solution |
| :--- | :--- |
| Tests pass locally, fail in CI | Check environment differences, timeouts, race conditions |
| Flaky tests | Look for async timing issues, mock dependencies properly |
| Bug recurs after fix | Root cause wasn't truly fixed — re-run 5 Whys analysis |
| Multiple hypotheses conflicting | Test ONE at a time with minimal reproduction |
| Cannot determine isolated/systemic | Count affected components: 3+ = systemic |
| Investigation stalls after 3+ hypotheses | Question the pattern, not individual bugs |

## Pressure Resistance

Systematic investigation prevents shortcuts that create technical debt.

**Time pressure responses:**
- "Need to deploy soon" → Root cause prevents future issues
- "User waiting for fix" → Rushed fixes create more problems

**Sunk cost responses:**
- "Already spent 2 hours" → Wrong approach wastes more time
- "Almost there" → Return to root cause with fresh perspective

**Obvious fix responses:**
- "It's obviously just X" → Obvious ≠ Correct, verify with evidence

**Protocol:** Acknowledge pressure → Return to systematic approach → Brief justification → Continue investigation

## Best Practices

**DO:**
- Gather concrete evidence before forming conclusions
- Test one hypothesis at a time
- Use 5 Whys to reach root cause
- Document root cause for future reference
- Verify with minimal reproduction before full fix

**DON'T:**
- Apply fixes without root cause investigation
- Test multiple hypotheses simultaneously
- Assume obvious = correct
- Ignore patterns (3+ failures = systemic)
- Fall for sunk cost rationalization

## Validation Checklist

Before claiming diagnosis complete:

**Problem Statement:**
- [ ] Symptom documented with exact error messages
- [ ] Reproduction steps verified
- [ ] Frequency and conditions identified

**Evidence Gathering:**
- [ ] Logs and error output collected
- [ ] Recent changes reviewed (git history)
- [ ] Environment data documented

**Hypothesis Formation:**
- [ ] Single hypothesis based on evidence
- [ ] Hypothesis is falsifiable
- [ ] Confidence level assigned

**Test & Conclude:**
- [ ] Minimal reproduction test created
- [ ] Hypothesis confirmed or rejected
- [ ] Root cause identified with file:line evidence
- [ ] Fix strategy documented

**Pattern Recognition:**
- [ ] Isolated vs systemic determined
- [ ] 3+ failures = architectural flag raised

---

## Genetic Code

<critical_constraint>
**Portability Invariant: Zero External Dependencies**

This component must work in a project with ZERO external rules access (no CLAUDE.md, CLAUDE.local.md, or .claude/rules/ dependencies).
All necessary philosophy is embedded within this skill.

**Evidence Requirements**

Complete evidence gathering before proposing fixes.
Document symptoms, evidence, hypothesis before implementing.
Test hypothesis with minimal reproduction before full fix.

**Single Hypothesis Protocol**

Form single hypothesis based on evidence.
Test with minimal reproduction.
Confirm or reject before next hypothesis.

**Architecture Pattern Recognition**

Three or more similar failures indicate architectural problems requiring broader solutions than localized patches.

**Delta Standard**: Good Component = Expert Knowledge − What Claude Already Knows
</critical_constraint>
