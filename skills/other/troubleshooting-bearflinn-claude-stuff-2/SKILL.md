---
name: troubleshooting
description: A robust troubleshooting framework. Use this skill anytime the user reports something isn't working, is buggy, or is throwing errors.
---

# Troubleshooting

This skill helps identify when you're applying a bandaid fix versus addressing root causes, and when to escalate to deeper investigation.

## Core Principles

### 1. Bandaid Detection

Before implementing any fix, check if it's treating symptoms vs. root cause:

**Red flags indicating bandaid fixes:**
- Adding try/catch blocks that hide errors without understanding why they occur
- Implementing timeouts or retries without investigating why failures happen
- Duplicating logic to work around a broken component
- Increasing resource limits without understanding why resources are exhausted
- Caching to hide performance issues without addressing underlying inefficiency
- Adding null checks without understanding why nulls appear
- Hard-coding values that should be dynamic (IDs, paths, credentials, configuration values)

**When you detect a bandaid:**
"I could [quick fix], but that just masks the real issue: [root cause]. To fix properly, I need to [proper solution / missing information]. Should I implement the workaround for now or investigate the root cause?"

### 2. Systemic Issue Detection

Watch for signs that a bug indicates larger problems:

**Indicators of systemic issues:**
- Same type of error occurring in multiple places
- Issue requires workarounds in multiple locations
- Root cause points to architectural decisions
- Fix would require changing fundamental assumptions
- Similar issues have been "fixed" before with workarounds

**When you detect systemic issues:**
"This appears to be a symptom of a larger issue: [systemic problem]. The immediate fix is [X], but this suggests we should also consider [architectural change]."

### 3. Escalation to Deep Investigation

For most issues, attempt a straightforward fix. If any of these occur, **you MUST read `references/collaborative-workflow.md` and follow that process:**

**Escalation triggers:**
- Simple fix attempt fails or reveals complexity
- Multiple possible root causes exist
- Issue is more complex than it initially appeared
- You're uncertain whether a solution is proper or a bandaid
- Investigation requires information you don't have access to

**When triggered, immediately use the view tool:**
```
view references/collaborative-workflow.md
```
Then follow the detailed investigation process described in that file.

## Quick Troubleshooting

For straightforward issues, proceed autonomously:

1. **Identify the issue** - Read error messages, examine code, check logs
2. **Verify it's not a bandaid** - Check against red flags above
3. **Implement the fix** - Address the root cause
4. **Verify** - Confirm the specific symptom is resolved

If at any point this becomes unclear or the fix would be a bandaid, escalate to the collaborative workflow.

## Anti-Patterns

**Assumption-driven debugging:**
- Don't assume you understand the architecture
- Don't guess at configuration or environment details
- Don't implement solutions based on incomplete information

**Premature solutions:**
- Don't propose fixes before understanding the root cause
- Don't implement the first solution that comes to mind without evaluation
- Don't skip verification that the fix actually addresses the root cause