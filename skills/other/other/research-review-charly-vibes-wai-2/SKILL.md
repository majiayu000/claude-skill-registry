---
name: research-review
description: Iterative review of research documents using Rule of 5
disable-model-invocation: true
---

# Iterative Research Review (Rule of 5)

Perform thorough research document review using the Rule of 5 - iterative refinement until convergence.

## Setup

**If research document path provided:** Read the document completely

**If no path:** Ask for the research document path or list available research documents

## Process

Perform 5 passes, each focusing on different aspects. After each pass (starting with pass 2), check for convergence.

### PASS 1 - Accuracy & Sources

**Focus on:**
- Claims backed by evidence
- Source credibility and recency
- Correct interpretation of sources
- Factual accuracy of technical details
- Version/date relevance (is information outdated?)
- Code references are correct (file:line exist and match claim)

**Output format:**
```
PASS 1: Accuracy & Sources

Issues Found:

[ACC-001] [CRITICAL|HIGH|MEDIUM|LOW] - Section/Paragraph
Description: [What's inaccurate or unsourced]
Evidence: [Why this is problematic]
Recommendation: [How to fix with specific guidance]

[ACC-002] ...
```

**What to look for:**
- "This works by..." without code reference
- Claims about codebase without verification
- Outdated information (library versions, deprecated APIs)
- Misinterpretation of source code
- Assumptions presented as facts

### PASS 2 - Completeness & Scope

**Focus on:**
- Missing important topics or considerations
- Unanswered questions that should be addressed
- Gaps in the analysis
- Scope creep (irrelevant tangents)
- Depth appropriate for the topic
- All research questions answered

**Prefix:** COMP-001, COMP-002, etc.

**What to look for:**
- Research question asked but not answered
- Obvious related topics not explored
- Shallow treatment of complex topics
- Too much detail on tangential topics
- "Further research needed" without followthrough

### PASS 3 - Clarity & Structure

**Focus on:**
- Logical flow and organization
- Clear definitions of terms
- Appropriate headings and sections
- Readability for target audience
- Jargon explained or avoided
- Consistent terminology

**Prefix:** CLAR-001, CLAR-002, etc.

**What to look for:**
- Jumping between topics without transitions
- Technical terms used without definition
- Conclusions before supporting evidence
- Redundant sections
- Confusing or ambiguous language

### PASS 4 - Actionability & Conclusions

**Focus on:**
- Clear takeaways and recommendations
- Conclusions supported by the research
- Practical applicability to the project
- Trade-offs clearly articulated
- Next steps identified
- Decision-making guidance provided

**Prefix:** ACT-001, ACT-002, etc.

**What to look for:**
- Research without recommendations
- Conclusions that don't follow from findings
- "Interesting but..." without actionable insight
- Missing implementation guidance
- No clear "what should we do?"

### PASS 5 - Integration & Context

**Focus on:**
- Alignment with existing research
- Connections to specs and requirements
- Relevance to current project goals
- Contradictions with established decisions
- Impact on existing plans
- References to related work

**Prefix:** INT-001, INT-002, etc.

**What to look for:**
- Contradicts previous research without acknowledgment
- Ignores existing patterns in codebase
- Doesn't reference related specs or docs
- Recommendations conflict with project direction
- Missing cross-references

## Convergence Check

After each pass (starting with pass 2), report:

```
Convergence Check After Pass [N]:

1. New CRITICAL issues: [count]
2. Total new issues this pass: [count]
3. Total new issues previous pass: [count]
4. Estimated false positive rate: [percentage]

Status: [CONVERGED | ITERATE | NEEDS_HUMAN]
```

**Convergence criteria:**
- **CONVERGED**: No new CRITICAL, <10% new issues vs previous pass, <20% false positives
- **ITERATE**: Continue to next pass
- **NEEDS_HUMAN**: Found blocking issues requiring human judgment

**If CONVERGED before Pass 5:** Stop and report final findings.

## Final Report

After convergence or completing all passes:

```
## Research Review Final Report

**Research:** [path/to/research.md]

### Summary

Total Issues by Severity:
- CRITICAL: [count] - Must fix before using research
- HIGH: [count] - Should fix before using research
- MEDIUM: [count] - Consider addressing
- LOW: [count] - Nice to have

Convergence: Pass [N]

### Top 3 Most Critical Findings

1. [ACC-001] [Description] - Section [N]
   Impact: [Why this matters]
   Fix: [What to do]

2. [COMP-003] [Description] - Section [N]
   Impact: [Why this matters]
   Fix: [What to do]

3. [ACT-002] [Description] - Conclusions
   Impact: [Why this matters]
   Fix: [What to do]

### Recommended Revisions

1. [Action 1 - specific and actionable]
2. [Action 2 - specific and actionable]
3. [Action 3 - specific and actionable]

### Verdict

[READY | NEEDS_REVISION | NEEDS_MORE_RESEARCH]

**Rationale:** [1-2 sentences explaining the verdict]

### Research Quality Assessment

- **Accuracy**: [Excellent|Good|Fair|Poor] - [brief comment]
- **Completeness**: [Excellent|Good|Fair|Poor] - [brief comment]
- **Actionability**: [Excellent|Good|Fair|Poor] - [brief comment]
- **Clarity**: [Excellent|Good|Fair|Poor] - [brief comment]
```

## Rules

1. **Be specific** - Reference sections/paragraphs, provide file:line for code claims
2. **Verify claims** - Actually check code references and factual statements
3. **Validate actionability** - Research should drive decisions, not just inform
4. **Prioritize correctly**:
   - CRITICAL: Factually wrong or misleading
   - HIGH: Significant gaps or unclear conclusions
   - MEDIUM: Could be clearer or more complete
   - LOW: Minor improvements
5. **If converged before pass 5** - Stop and report, don't continue needlessly
