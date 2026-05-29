---
name: nav-diagnose
description: Detect quality drops in AI output and prompt re-anchoring. Auto-triggers after repeated corrections, context confusion, or when user says "something seems off", "you're not getting this".
allowed-tools: Read, Write, Bash
version: 1.0.0
---

# Navigator Diagnose Skill

Detect when human-AI collaboration quality drops and prompt re-anchoring to restore effective communication.

## Why This Exists (Theory of Mind)

Based on Riedl & Weidmann 2025 research on Human-AI Synergy:
- Theory of Mind varies dynamically within users (moment-to-moment)
- Quality drops occur when ToM alignment degrades
- Early detection and re-anchoring restores collaboration effectiveness
- Both user ToM (understanding Claude) and Claude's model of user can drift

This skill detects when collaboration is degrading and prompts corrective action.

## When to Invoke

**Auto-invoke when**:
- 2+ corrections on the same topic detected
- User says "something seems off", "you're not getting this"
- User says "wrong again", "still not right"
- Context usage exceeds 75% and quality signals degrade
- User expresses frustration ("ugh", "sigh", explicit frustration)
- Loop mode stagnation detected (3+ same-state iterations)

**DO NOT invoke if**:
- Single correction (normal collaboration)
- User is providing new requirements (not correcting)
- Fresh session (insufficient data to diagnose)
- User explicitly says "it's fine" or "close enough"

## Quality Drop Indicators

### 1. Repeated Corrections (High Severity)
```
Trigger: Same correction given 2+ times
Signal: "No, I said users plural, not user" (2nd time)
Issue: Not incorporating user feedback
```

### 2. Hallucination Signals (High Severity)
```
Trigger: References to non-existent files, functions, or packages
Signal: "That file doesn't exist", "There's no such function"
Issue: Generating from incorrect mental model
```

### 3. Context Confusion (Medium Severity)
```
Trigger: Mixing details from unrelated tasks
Signal: "That's from the other project", "Wrong feature"
Issue: Context window pollution or misattribution
```

### 4. Unaddressed Feedback (Medium Severity)
```
Trigger: User correction not reflected in next output
Signal: Generates same pattern after being told not to
Issue: Not properly updating internal model
```

### 5. Goal Drift (Low Severity)
```
Trigger: Output increasingly diverges from original goal
Signal: "We're getting off track", "Not what I asked for"
Issue: Lost sight of user's actual objective
```

### 6. Loop Stagnation (High Severity)
```
Trigger: 3+ consecutive iterations with same state hash (loop mode only)
Signal: nav-loop detects stagnation, triggers nav-diagnose
Issue: Stuck on same step, unable to progress
```

## Execution Steps

### Step 1: Assess Quality State

**Analyze recent exchanges** (last 10-15 messages):

```
Quality Indicators:
- [ ] Corrections given: {count}
- [ ] Same-topic corrections: {count}
- [ ] User frustration signals: {count}
- [ ] Hallucination reports: {count}
- [ ] "Not what I meant" phrases: {count}
```

**Calculate severity**:
```python
severity = "critical" if same_topic_corrections >= 2 or hallucinations >= 1
severity = "high" if corrections >= 3 or frustration_signals >= 2
severity = "medium" if corrections >= 2 or goal_drift_detected
severity = "low" if corrections == 1  # Normal, don't trigger
```

### Step 2: Identify Root Cause

**Analyze correction patterns**:

| Pattern | Likely Cause | Re-anchoring Focus |
|---------|--------------|-------------------|
| Same correction repeated | Not incorporating feedback | Explicitly acknowledge and confirm understanding |
| Increasing corrections | Drifting from user intent | Re-establish goals |
| Technical mismatches | Wrong assumptions | Clarify technical context |
| Frustration without specifics | Communication mismatch | Ask what's wrong |

### Step 3: Display Diagnostic

**Show quality check alert**:
```
⚠️  QUALITY CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Detected Issue: {ISSUE_TYPE}
Severity: {SEVERITY}

What I noticed:
- {OBSERVATION_1}
- {OBSERVATION_2}

Possible causes:
- {CAUSE_1}
- {CAUSE_2}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Let me re-anchor our collaboration:

1. Your goal: {RECONSTRUCTED_GOAL}
2. Current state: {STATE_SUMMARY}
3. What you want: {CORRECTED_UNDERSTANDING}

Is this understanding correct? [Y/n]
```

### Step 4: Re-anchor Collaboration

**Based on user confirmation**:

**If correct** (Y):
```
✅ Re-anchored!

I'll proceed with this understanding:
- {KEY_POINT_1}
- {KEY_POINT_2}

Continuing with: {NEXT_ACTION}
```

**If incorrect** (n):
```
Help me understand better:

1. What is your actual goal?
2. What am I getting wrong?
3. What constraints should I know?

[Open-ended response welcome]
```

### Step 5: Log Diagnostic (Optional)

**If nav-profile exists**, save diagnostic:
```json
{
  "date": "{YYYY-MM-DD}",
  "issue_type": "{ISSUE_TYPE}",
  "severity": "{SEVERITY}",
  "resolution": "re-anchored|user-corrected|escalated",
  "learnings": ["{WHAT_TO_AVOID}"]
}
```

### Step 6: Suggest Preventive Actions

**Based on severity and pattern**:

**For context overload**:
```
💡 Suggestion: Consider running nav-compact to clear context.
Current context usage is high, which can cause confusion.
```

**For repeated corrections**:
```
💡 Suggestion: Let me save your preference to avoid this in future.
"Remember I always want {X}" - This will persist across sessions.
```

**For communication mismatch**:
```
💡 Suggestion: Consider adjusting your profile preferences.
- Current verbosity: {VERBOSITY}
- Current confirmation: {CONFIRMATION}

Update with: "Remember I prefer {SUGGESTED_STYLE}"
```

---

## Re-anchoring Templates

### Template 1: Goal Re-alignment
```
Let me verify I understand your goal:

You want to: {GOAL_STATEMENT}

Not: {COMMON_MISUNDERSTANDING}

Key constraints:
- {CONSTRAINT_1}
- {CONSTRAINT_2}

Is this right?
```

### Template 2: Technical Re-alignment
```
Let me verify the technical context:

Framework: {FRAMEWORK}
Patterns: {PATTERNS}
Conventions: {CONVENTIONS}

What I should be using:
- {TOOL_1}: for {PURPOSE_1}
- {TOOL_2}: for {PURPOSE_2}

Corrections to my assumptions?
```

### Template 3: Communication Re-alignment
```
I may be mismatching your communication style:

You seem to prefer:
- {INFERRED_STYLE_1}
- {INFERRED_STYLE_2}

I've been:
- {MY_STYLE_1}
- {MY_STYLE_2}

Should I adjust my approach?
```

---

## Integration with Other Skills

### With nav-profile
- Log diagnostics for pattern analysis
- Suggest preference updates after repeated issues
- Load profile preferences for baseline comparison

### With nav-marker
- Suggest marker before major re-anchoring
- Include diagnostic state in marker

### With nav-compact
- Recommend compact if context overload detected
- Track if compaction resolves issues

---

## Quality Signals Reference

### Positive Signals (Good Collaboration)
```
- "Perfect, exactly what I needed"
- "Yes, continue"
- "Good, now..."
- No corrections for 5+ exchanges
- User providing new requirements (not corrections)
```

### Negative Signals (Quality Drop)
```
- "No", "Wrong", "Not that"
- "I already said..."
- "Again, please..."
- "Sigh", "Ugh", explicit frustration
- "You're not understanding"
- Same correction twice
```

### Neutral Signals (Normal Iteration)
```
- "Actually, let's try..."
- "Can we also..."
- "What about..."
- Single correction with explanation
```

---

## Example Scenarios

### Scenario 1: Repeated REST Convention Correction
```
Exchange 1:
User: "Create endpoint for users"
Claude: Creates /user endpoint
User: "Should be /users (plural)"

Exchange 2:
User: "Now create endpoint for posts"
Claude: Creates /post endpoint
User: "Again, plural! /posts"

→ Trigger: Same correction (plural naming) given twice
→ Action: Re-anchor on REST conventions
→ Outcome: "I understand now - always use plural nouns for REST resources"
```

### Scenario 2: Context Confusion
```
User working on: OAuth feature (Feature A)
Claude references: Stripe integration (Feature B from earlier)

User: "That's from the payment feature, not auth"

→ Trigger: Context confusion detected
→ Action: Re-anchor on current feature
→ Suggestion: Consider nav-compact to clear old context
```

### Scenario 3: User Frustration
```
User: "Ugh, still not right"
User: "This is frustrating"

→ Trigger: Frustration signals detected
→ Action: Pause and diagnose
→ Response: Open-ended question about what's wrong
```

---

## Success Criteria

Diagnostic is successful when:
- [ ] Quality drops detected before user escalates
- [ ] Root cause correctly identified
- [ ] Re-anchoring restores collaboration quality
- [ ] Preventive suggestions are actionable
- [ ] User confirms understanding after re-anchor
- [ ] Same issue doesn't recur immediately

---

## Limitations

**Cannot detect**:
- Silent user frustration (no signals in text)
- Issues outside conversation context
- Problems with external systems
- User preferences not yet expressed

**Should not**:
- Over-trigger on normal corrections
- Interrupt productive flow
- Make user feel blamed
- Require lengthy re-explanation

---

## Best Practices

**When diagnosing**:
- Be humble about AI limitations
- Don't blame user for miscommunication
- Offer concrete next steps
- Keep re-anchoring brief

**When re-anchoring**:
- Focus on understanding, not apologizing
- Confirm specific points, not general "I understand"
- Let user correct if wrong
- Thank user for patience

---

**This skill catches collaboration quality drops early, enabling quick recovery through Theory of Mind re-alignment** 🔍
