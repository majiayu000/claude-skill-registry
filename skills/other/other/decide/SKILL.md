---
name: decide
description: Present viable paths, detect decision type, and guide commitment with a user checkpoint. Use after synthesize to move from analysis to action.
allowed-tools: [Read]
---

# Decide

Analysis is done. Time to move from understanding to action.

Based on the synthesis above, guide the user through a decision. The goal is to stop analyzing and start acting, but with the right framing for the type of decision at hand.

## Step 1: Decision Landscape

Before committing to a direction, present two to four viable paths that emerged from the synthesis. For each path:

- **Path name**: A short descriptive label
- **What it looks like**: One sentence describing the approach
- **Primary strength**: The single biggest reason to choose this path
- **Primary risk**: The single biggest concern with this path

This gives the user something concrete to react to before locking in a direction.

## Step 2: Decision Type Detection

Assess which type of decision this is and adapt the output format accordingly:

### Clear Choice
Use when: The evidence points strongly in one direction, tradeoffs are well understood, and the decision is relatively binary or technical.

Format:
- **Decision**: State what you will do. One sentence, direct, unhedged.
- **Confidence**: High / Medium / Low, with brief rationale
- **Reversal triggers**: Specific conditions that would reopen this decision
- **Next action**: The single next step to execute, something achievable today or tomorrow

### Phased Approach
Use when: Significant uncertainty remains, the decision involves multiple stages, or a full commitment is premature.

Format:
- **Initial move**: What to do first and what it will reveal
- **Evaluation milestone**: A specific point where you will assess progress and decide whether to continue, pivot, or stop
- **Conditional next phase**: What happens if the initial move succeeds? What if it does not?
- **Confidence**: High / Medium / Low, with brief rationale
- **Reversal triggers**: Specific conditions that would reopen this decision
- **Next action**: The single next step to begin the initial move

### Navigational
Use when: People, relationships, coaching, or interpersonal dynamics are central. The "decision" is more about an approach and principles than a single action.

Format:
- **Approach**: The overall strategy, framed as principles rather than rigid steps. "Lead with X, watch for Y, adjust based on Z."
- **Opening move**: The first conversation or action, with guidance on tone and framing
- **Signals to watch for**: What responses or reactions indicate the approach is working? What indicates it needs adjustment?
- **Adjustment guidance**: If the initial approach meets resistance, what is the fallback? How do you adapt without abandoning the core intent?
- **Confidence**: High / Medium / Low, with brief rationale
- **Next action**: The single next step to begin

## Step 3: Synthesis Confidence Connection

If the synthesis confidence was Medium or Low, the recommended path must explicitly acknowledge this. Do not present a Medium confidence recommendation with the same certainty as a High confidence one. Options:
- Recommend a phased approach that builds confidence before full commitment
- Identify what specific information would move confidence higher
- Frame the decision as provisional, with a clear review point

## Step 4: User Checkpoint

After presenting the landscape and recommended path, ask:

**Does this direction match what you need, or should I reconsider from a different angle?**

This is critical. The decide step should be a conversation, not a declaration. Wait for the user to confirm before treating the decision as final.

## Decision Record

After the user confirms, provide a structured record for future reference:

```
## Decision Record
**Date**: [current date]
**Decision**: [one sentence]
**Type**: Clear Choice / Phased / Navigational
**Confidence**: High / Medium / Low
**Time horizon**: When this decision should be fully evaluated
**Review cadence**: How often to check whether reversal triggers have been hit
**Reversal triggers**: [list]
**Next action**: [specific step]
```

---

If you are not ready to decide, say so directly and identify what is blocking commitment. Then either:
- Run additional analysis on the blocking issue
- Accept that you are deciding under uncertainty, as most real decisions are

Do not use this as another round of analysis. Decide or explicitly defer.
