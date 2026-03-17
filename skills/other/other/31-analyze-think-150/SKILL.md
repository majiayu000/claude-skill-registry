---
name: 31-analyze-think-150
description: "[31] ANALYZE. Universal deep thinking methodology for any situation requiring quality reasoning. Use when solving problems, debugging, making decisions, analyzing code, planning, reviewing, or anytime you need thorough thinking instead of surface-level responses. Triggers on \"think deeply\", \"analyze thoroughly\", \"reason carefully\", \"deep thinking\", \"understand completely\", or any task requiring careful thought."
---

# Analyze-Think 150 Protocol

**Core Principle:** Think deeply, reason thoroughly, understand completely. Quality thinking for any situation.

## When This Skill Activates

**Universal trigger:** Any situation requiring quality thinking over quick responses.

**Specific triggers:**
- Problem solving and debugging
- Decision making at any scale
- Code review and analysis
- Planning and strategy
- Understanding complex systems
- Evaluating options and trade-offs
- When user says "think deeply", "analyze", "reason carefully"

**Key insight:** This skill applies at ANY point in work, not just at the beginning.

## The 150% Rule

- **100% Core:** Complete internal analysis to coherent conclusion
- **50% Enhancement:** Identify hidden assumptions, risks, and alternative interpretations

## Execution Protocol

### Step 1: IMMEDIATE PAUSE
Before any response, stop and prepare for systematic analysis.

### Step 2: MODEL FORMATION
Build understanding: **Goal → Context → Constraints → Dependencies**
- What is the real objective?
- What is the full context?
- What are the constraints?
- What depends on this?

### Step 3: ASSUMPTION AUDIT
List and test every assumption:
- What am I assuming without proof?
- Which assumptions are verified vs unverified?
- What evidence supports each assumption?

### Step 4: ALTERNATIVE ANALYSIS
Generate 3+ different interpretations:
- How else could this problem be viewed?
- What's the opposite perspective?
- What if my initial assumption is wrong?

### Step 5: RISK & FAILURE ANALYSIS
Identify potential failures:
- What could go wrong?
- What's the impact of wrong assumptions?
- How can I mitigate risks?

### Step 6: SYNTHESIS & VALIDATION
Combine insights into coherent model:
- Can I explain this simply?
- Is anything missing?
- Does the logic hold together?

## Mandatory Analysis Questions

Ask yourself before responding:
1. "What do I actually understand about this problem?"
2. "What am I assuming without verification?"
3. "What could disprove my current conclusion?"
4. "How would this look from another perspective?"
5. "What am I missing?"
6. "Can I explain this in simple words?"

## Output Format

When using Deep-Think 150, structure response as:

```
🧠 **Deep-Think 150 Analysis**

**Understanding:**
[Core problem/goal identified]

**Assumptions Checked:**
- ✅ Verified: [assumption with evidence]
- ⚠️ Unverified: [assumption needing validation]

**Alternative Perspectives:**
- [Alternative 1]
- [Alternative 2]

**Risks Identified:**
- [Risk and mitigation]

**Conclusion:**
[Well-reasoned conclusion with confidence level]
```

## Operational Rules

1. **NO SURFACE SOLUTIONS:** Never respond without full internal analysis
2. **COMPLETE BEFORE PROCEEDING:** Finish analysis before any action
3. **QUESTION EVERYTHING:** Challenge every assumption
4. **MULTIPLE PERSPECTIVES:** Consider problem from different angles
5. **SIMPLE EXPLANATION TEST:** If you can't explain simply, analysis is incomplete
6. **CONTINUOUS VALIDATION:** Keep validating throughout work

## Examples

### ❌ BAD (Surface Response)
```
User: "Fix the login bug"
AI: "I'll add a null check to the login function."
```
Problem: No analysis, jumped to solution based on assumption.

### ✅ GOOD (Deep-Think Response)
```
User: "Fix the login bug"
AI: "🧠 Deep-Think 150 Analysis

Understanding: Login fails for some users. Need to identify root cause.

Assumptions Checked:
- ⚠️ Unverified: Bug is in login function (need to trace full flow)
- ⚠️ Unverified: It's a null pointer issue (no evidence yet)

Alternative Perspectives:
1. Could be authentication API timeout
2. Could be session management issue
3. Could be database connection problem

Risks: Fixing symptom without finding root cause = bug returns

Conclusion: First, I'll trace the full authentication flow and check 
error logs before proposing a fix. Let me investigate..."
```

## Failure Modes & Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| **Premature Action** | Responding without analysis | Stop, return to Step 1 |
| **Hidden Assumptions** | Unverified beliefs in reasoning | Explicit assumption testing |
| **Single Perspective** | Only one interpretation considered | Generate 3+ alternatives |
| **Complex Explanation** | Can't explain simply | Simplify model, extract core |

## When to Use

This Skill is **universal** and applies to any situation requiring quality thinking:
- **At the start:** Understanding new problems or requests
- **In the middle:** When stuck or facing complexity
- **At decision points:** Before making important choices
- **During review:** Analyzing code, plans, or solutions
- **Anytime:** When you need to think, not just react

## Session Log Entry (MANDATORY)

After completing this skill, write to `.sessions/SESSION_[date]-[name].md`:

```
### [date - HH"MM] Analyze-Think 150 Complete
**Topic:** <what was analyzed>
**Conclusion:** <key insight/decision>
**Risks:** <identified risks>
```

---

**Remember:** Deep-Think 150 is not about slowing down — it's about thinking better. Apply the depth appropriate to the complexity. Simple questions get simple analysis; complex problems get full Deep-Think treatment.

