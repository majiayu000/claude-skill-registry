---
name: 62-validate-integrity-150
description: "[62] VALIDATE. Final self-check before delivery. Verify goal alignment, completeness, correctness, and identify residual risks. Produces quality score (0-100) and delivery status. Use when completing any significant work, before handoff, or when you need confidence that work is ready."
---

# Validate-Integrity 150 Protocol

**Core Principle:** Check yourself before delivery. Verify goal alignment, completeness, correctness. Identify what could still go wrong. Score the quality honestly.

## What This Skill Does

When you invoke this skill, you're asking AI to:
- **Verify alignment** — Does result match original goal?
- **Check completeness** — Are all requirements satisfied?
- **Validate correctness** — Is it technically accurate?
- **Assess risks** — What residual issues remain?
- **Score quality** — Honest 0-100 rating with reasoning

## The 150% Check Rule

| Dimension | 100% Core | +50% Enhancement |
|-----------|-----------|------------------|
| **Goal** | Meets objectives | + Exceeds expectations |
| **Complete** | Requirements done | + Edge cases covered |
| **Correct** | Technically valid | + Best practices followed |
| **Risks** | Known issues noted | + Mitigation strategies ready |

## Quality Assessment Framework

```
CORE INTEGRITY (100% Required)
├── Goal Alignment: Meets original objectives
├── Completeness: All requirements satisfied
├── Correctness: Technically accurate and valid
└── Consistency: Internal logic coherent

EXTENDED VALIDATION (50% Enhancement)
├── Context Fit: Works in broader environment
├── Side Effects: No unintended consequences
├── Edge Cases: Handles unusual scenarios
└── Future-Proofing: Adaptable to changes
```

## Quality Score Framework

| Score | Rating | Description | Action |
|-------|--------|-------------|--------|
| **95-100** | Excellent | Exceeds expectations | Deliver with confidence |
| **85-94** | Good | Meets all requirements | Deliver, note improvements |
| **75-84** | Acceptable | Minor issues exist | Deliver with caveats |
| **60-74** | Needs Work | Significant issues | Fix before delivery |
| **<60** | Unacceptable | Major problems | Return to development |

## When to Use This Skill

- **Before delivery** — Any significant work output
- **After implementation** — Code, features, documents
- **Before handoff** — To another person or system
- **When uncertain** — Need confidence check
- **After major changes** — Verify nothing broke

## Execution Protocol

### Step 1: GOAL ALIGNMENT
```
🎯 **GOAL VERIFICATION**

**Original Objective:** [What was requested]
**Delivered Result:** [What was produced]
**Alignment:** ✅ Match | ⚠️ Partial | ❌ Mismatch

**Gaps:** [Any differences from original goal]
```

### Step 2: COMPLETENESS ASSESSMENT
```
📋 **COMPLETENESS CHECK**

Requirements:
- [ ] Requirement 1: [Status]
- [ ] Requirement 2: [Status]
- [ ] Requirement 3: [Status]

**Coverage:** [X]% of requirements met
**Missing:** [What's not done]
```

### Step 3: CORRECTNESS VALIDATION
```
✓ **CORRECTNESS CHECK**

**Technical Accuracy:** [Assessment]
**Logic Coherence:** [Assessment]
**Best Practices:** [Assessment]
**Issues Found:** [List any problems]
```

### Step 4: CONTEXT INTEGRATION
```
🔗 **CONTEXT FIT**

**Environment:** Works in target environment?
**Integration:** Properly connected to dependencies?
**Side Effects:** Any unintended consequences?
**Performance:** Meets performance requirements?
```

### Step 5: RISK EVALUATION
```
⚠️ **RISK ASSESSMENT**

**Known Issues:**
- [Issue 1]: [Severity] - [Mitigation]
- [Issue 2]: [Severity] - [Mitigation]

**Edge Cases:** [Unusual scenarios covered?]
**Security:** [Any vulnerabilities?]
**Scalability:** [Can handle expected load?]
```

### Step 6: SELF-CRITIQUE
```
🔮 **SELF-CRITIQUE**

**What could be better?**
- [Improvement 1]
- [Improvement 2]

**Alternative approaches considered?**
- [Alternative and why not chosen]

**Lessons for future:**
- [Learning 1]
```

### Step 7: FINAL SCORE
Calculate and declare:
```
📊 **QUALITY SCORE:** [X]/100 ([Rating])

**Reasoning:** [Why this score]
```

## Output Format

```
🔍 **INTEGRITY-CHECK 150 COMPLETE**

**Quality Score:** [X]/100 ([Rating])

**✅ STRENGTHS:**
- [Key positive finding 1]
- [Key positive finding 2]
- [Quality achievement]

**⚠️ AREAS FOR ATTENTION:**
- [Minor issue 1]
- [Recommendation 1]
- [Residual risk 1]

**🚫 CRITICAL ISSUES:** [None / List blockers]

**📋 DELIVERY STATUS:** 
[✅ Ready | ⚠️ Conditional | ❌ Not Ready]

**🎯 CONFIDENCE LEVEL:** [High/Medium/Low]
**Reasoning:** [Why this confidence]

**RECOMMENDATIONS:**
- [What to do next]
- [What to monitor]
```

## Integrity Checklist

**🎯 CORE QUALITY**
- [ ] Goal Achievement: Original objectives fully met?
- [ ] Requirement Coverage: All specified requirements?
- [ ] Technical Accuracy: Solution correct?
- [ ] Consistency: Internal logic coherent?

**🔍 CONTEXT**
- [ ] Environment Fit: Works in target environment?
- [ ] Integration: Properly connected?
- [ ] Side Effects: None unintended?
- [ ] Performance: Meets requirements?

**⚠️ RISKS**
- [ ] Known Issues: Documented and acceptable?
- [ ] Edge Cases: Unusual scenarios handled?
- [ ] Security: No vulnerabilities?
- [ ] Scalability: Handles expected load?

**🔮 FUTURE**
- [ ] Maintainability: Easy to maintain?
- [ ] Documentation: Well-documented?
- [ ] Knowledge Transfer: Others can understand?

## Operational Rules

1. **MANDATORY CHECK:** Every significant work needs integrity check
2. **OBJECTIVE CRITIQUE:** Self-assess without bias
3. **COMPLETE COVERAGE:** Check all quality dimensions
4. **RISK TRANSPARENCY:** Document residual risks honestly
5. **IMPROVEMENT FOCUS:** Identify what could be better
6. **HONEST SCORING:** Don't inflate quality score

## Failure Modes & Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| **Overconfidence** | Score too high | Get external review |
| **Incomplete Check** | Missed aspects | Use full checklist |
| **Bias Blindness** | Ignoring own errors | Delayed assessment |
| **Risk Denial** | Ignoring issues | Explicit risk documentation |

## Examples

### ❌ Without Integrity-Check
```
AI: "Done! Feature implemented."
[Deploys to production]
Result: Critical security vulnerability discovered by users
```

### ✅ With Integrity-Check 150
```
🔍 INTEGRITY-CHECK 150 COMPLETE

Quality Score: 88/100 (Good)

✅ STRENGTHS:
- User registration fully functional
- Mobile/desktop compatibility verified
- All 5 requirements implemented
- Unit tests passing (94% coverage)

⚠️ AREAS FOR ATTENTION:
- Loading states could be smoother
- Error messages need localization
- Consider rate limiting for production

🚫 CRITICAL ISSUES: None

📋 DELIVERY STATUS: ✅ Ready

🎯 CONFIDENCE: High
Reasoning: All core requirements met, tested on multiple 
devices, no blocking issues found.

RECOMMENDATIONS:
- Add loading animation polish in next sprint
- Set up error message translation pipeline
- Implement rate limiting before high traffic events
```

## Relationship to Other Skills

- **gated-exec-150** → Executes the plan
- **integrity-check-150** → Validates the result
- **74-mid-session-save-150** → Documents continuity via checkpoints

## Session Log Entry (MANDATORY)

After completing this skill, write to `.sessions/SESSION_[date]-[name].md`:

```
### [date - HH"MM] Validate-Integrity 150 Complete
**Target:** <what was validated>
**Score:** <X/100>
**Issues:** <found issues/none>
**Recommendation:** <Deliver/Fix>
```

---

**Remember:** Integrity-check isn't criticism — it's quality assurance. An honest 85 score with documented issues is more valuable than a false 100. The check protects you and the user from preventable problems.
