---
name: diagnose
description: Routes a vague symptom or complaint to the most relevant Clairvoyance skill via a decision tree. Use when someone describes a problem but doesn't know which skill to reach for. Not for running a comprehensive review (use design-review) or scanning a checklist (use red-flags).
argument-hint: "[description of the symptom or problem]"
metadata:
  allowed-tools: Read, Grep
---

# Diagnose

When invoked with $ARGUMENTS, match the described symptom against the decision tree below and route to the appropriate skill. If code paths are referenced, read them first to confirm the match before routing. This skill routes to other skills from Clairvoyance (https://clairvoyance.fyi). It works best when the full collection is installed.

## Decision Tree

### 1. "Something feels wrong but I can't say what"

The symptom is a general sense of unease with no concrete complaint.

→ **complexity-recognition**: Apply the three-symptom framework to locate the source.

### 2. "Simple changes require edits in many files"

Change amplification. Branch by cause:

- Shared knowledge is scattered across modules → **information-hiding** (look for leaked implementation details)
- Old abstractions no longer fit the current shape of the system → **code-evolution** (check whether the design has kept pace with requirements)
- Module boundaries cut across concerns instead of encapsulating them → **module-boundaries** (re-evaluate decomposition)

### 3. "This interface is awkward / too many parameters"

The interface exposes too much or forces callers to assemble details they shouldn't need.

- Implementation burden leaks upward → **pull-complexity-down** (push details below the interface)
- The abstraction mixes general infrastructure with special-case logic → **general-vs-special** (separate the two)
- The module is shallow. Interface cost rivals implementation cost → **deep-modules** (deepen the module)

### 4. "I can't name this thing"

Naming difficulty signals a design problem, not a vocabulary problem.

→ **naming-obviousness**: If the name can't be made obvious, the entity's responsibility is likely unclear.
→ Then **design-it-twice**: Consider alternative decompositions that yield nameable pieces.

### 5. "Errors everywhere / too many exceptions"

Exception surfaces are large, catch blocks are boilerplate or error paths obscure the normal path.

→ **error-design**: Apply define-errors-out and exception aggregation.

### 6. "Layers feel redundant / wrappers add nothing"

Pass-through methods, thin adapter classes or layers that exist only for "architecture."

→ **abstraction-quality**: Evaluate whether each layer provides a meaningful abstraction or just adds indirection.

### 7. "Comments are useless / missing / stale"

Comments restate code, are absent where needed or have drifted from the implementation.

→ **comments-docs**: Apply the four-category framework and contamination checks.

### 8. "Code was written under pressure"

Technical debt from tactical shortcuts. The concern is process, not a specific structural flaw.

→ **strategic-mindset**: Assess the tactical-vs-strategic balance.
→ Then **code-evolution**: Plan incremental improvement alongside current work.

## Multiple Symptoms

When the description maps to more than one root symptom, prioritize in this order:

1. **Structural** (symptoms 1–6): These address the shape of the code and have the highest design leverage.
2. **Process** (symptom 8): This addresses how work is done. Important but downstream of structure.
3. **Surface** (symptom 7): Comment/doc issues are often symptoms of deeper structural problems. Fixing structure first may resolve them.

Route to the highest-priority match first. Mention the secondary matches so the user can follow up.

## Fallback

If the described symptom does not match any branch above, fall back to **red-flags**: a systematic scan will surface concrete signals to diagnose from.
