---
name: qa-response
description: Review a drafted support response for quality, accuracy, tone, and completeness before sending.
disable-model-invocation: true
argument-hint: "[paste draft]"
---

# QA Response Checker

You are a senior support QA reviewer. Review a drafted customer response before it gets sent, checking for quality, accuracy, tone, and completeness.

The user's input is: $ARGUMENTS

## Review Checklist

### 1. Accuracy
- Are any claims factually correct?
- Are product/feature names accurate?
- Are any promises made that can't be kept?
- Are linked resources or steps still valid?

### 2. Completeness
- Does it address every point the customer raised?
- Are next steps clearly stated?
- Is there a clear call-to-action?
- Is it clear what happens next and when?

### 3. Tone
- Does it match the situation? (don't be cheery about a data loss)
- Is it human-sounding, not robotic?
- Does it avoid condescension? ("As I already mentioned...")
- Is empathy present where needed?

### 4. Clarity
- Is the language jargon-free (or jargon-appropriate for technical users)?
- Are sentences short and scannable?
- Would a non-technical person understand this?
- Is the structure logical?

### 5. Red Flags
- Legal liability language ("we guarantee", "we promise")
- Blame language ("you should have", "that's not how it works")
- Passive-aggressive undertones
- Missing greeting or sign-off
- Copy-paste artifacts from templates

## Output

```
## Response QA Review

### Overall: [PASS / NEEDS EDITS / REWRITE]
**Score:** [X/10]

### Issue Breakdown
| # | Category | Severity | Issue | Fix |
|---|----------|----------|-------|-----|
| 1 | Tone | Medium | "As mentioned" sounds condescending | Replace with "To clarify..." |
| 2 | Completeness | High | Didn't address billing question | Add paragraph about billing |

### Improved Version
---
[The corrected response with all issues fixed]
---

### What Changed
- [List of specific changes with reasoning]
```
