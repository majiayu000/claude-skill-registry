---
name: 022-root-cause-analysis
description: Use when a framed problem needs root-cause investigation rather than a symptom-level fix, applying Five Whys, Fishbone (Ishikawa), Current Reality Tree, and constraint identification. This should trigger when an issue's Root Cause Analysis point of view needs evaluation, or when a maintainer directly asks to find the root cause of a problem before proposing a fix. Part of Plinth Toolkit
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.18.0
---
# Root Cause Analysis

Guide the identification of root causes, not symptoms, for a framed problem, using Five Whys, Fishbone (Ishikawa), Current Reality Tree, and constraint identification. **This is an interactive SKILL**.

**What is covered in this Skill?**

- Five Whys for a linear causal chain from a symptom to a root cause
- Fishbone (Ishikawa) for categorized candidate causes across multiple dimensions
- Current Reality Tree for interconnected causes and effects with a small number of core problems
- Constraint identification for the limiting factor holding the current state in place
- Choosing the technique(s) proportionate to the problem's complexity
- Feeding root-cause findings into `023-assumption-analysis` and the remaining Functional Specification lenses

## Constraints

Distinguish root causes from symptoms before recommending a fix. When this technique is orchestrated by another workflow, the orchestrator owns clarifying-question sequencing; when applied standalone, ask directly.

- **MUST** read `references/022-root-cause-analysis.md` before applying Root Cause Analysis guidance
- **MUST** distinguish a symptom (an observed effect) from a root cause (the condition that produces it)
- **MUST** apply Five Whys as a chain of "why" questions grounded in evidence from the problem frame, not assumption
- **MUST** apply Fishbone to organize candidate causes into categories (for example people, process, technology, environment) when more than one causal dimension is plausible
- **MUST** apply Current Reality Tree when multiple symptoms may share one or a small number of core problems connected by cause-effect relationships
- **MUST** identify the constraint limiting the current state, not only the most visible cause
- **MUST NOT** invent a root cause when the available evidence is vague or ambiguous; flag the gap for a clarifying question instead

## When to use this skill

- Find the root cause of this problem
- Apply Five Whys to this issue
- Build a Fishbone diagram for this problem
- Use Current Reality Tree to connect these symptoms
- Identify the constraint limiting the current state
- Draft the Root Cause Analysis section of a Functional Specification

## Workflow

1. **Read the Reference**

Read `references/022-root-cause-analysis.md`, then identify the symptom(s) evidenced by the problem frame.

2. **Apply Five Whys**

Chain "why" questions from the symptom toward an evidenced root cause, stopping when further "why" steps would require guessing.

3. **Apply Fishbone When Multiple Dimensions Are Plausible**

Organize candidate causes into categories when more than one causal dimension (people, process, technology, environment) is plausible.

4. **Apply Current Reality Tree When Symptoms Interconnect**

Connect multiple symptoms to a small number of shared core problems through cause-effect relationships when the symptoms appear related.

5. **Identify the Constraint**

Name the constraint limiting the current state, distinct from the most visible or most recently reported cause.

6. **Report the Root Cause Findings**

Report findings using Five Whys, Fishbone, Current Reality Tree, and the identified constraint, and flag any finding left open pending a clarifying answer.

## Reference

For detailed guidance, examples, and constraints, see [references/022-root-cause-analysis.md](references/022-root-cause-analysis.md).
