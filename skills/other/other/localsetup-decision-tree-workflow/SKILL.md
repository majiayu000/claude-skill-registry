---
name: localsetup-decision-tree-workflow
description: "Decision tree / reverse prompt workflow  - AI prompts user one question at a time with 4 options (A-D), preferred choice + rationale; build context for maximum impact. Use when user says 'decision tree', 'run the decision tree', 'reverse prompt', or 'reverse prompt workflow'; or when editing .agent/queue/**, PRD.md, *.prd.md."
metadata:
  version: "1.1"
---

# Decision tree workflow (reverse prompt)

When the user says **decision tree**, **decision tree questions**, **decision tree workflow**, **run the decision tree**, **reverse prompt**, **reverse prompt workflow**, or any synonymous phrase, **read this rule** and then run the process in [_localsetup/docs/DECISION_TREE_WORKFLOW.md](../../docs/DECISION_TREE_WORKFLOW.md). This is a **reverse prompt**: the AI prompts the user to gather context and decisions before implementing.

## Summary (full procedure in framework-docs)

- **One question per turn.** Four options (A, B, C, D); state preferred option and rationale. Questions relevant to the topic; most important first. Default 7-9 questions per topic; user may override. Accept A/B/C/D, different choice, or free-form; use all feedback as context.
- **When to use:** User explicitly invokes "decision tree" / "reverse prompt" (or "reverse prompt workflow") or when clarifying a draft PRD/spec with structured Q&A.
- **Do not run** unless user has clearly requested the workflow (e.g. "run the decision tree", "reverse prompt workflow", "use the decision tree process").

See [_localsetup/docs/DECISION_TREE_WORKFLOW.md](../../docs/DECISION_TREE_WORKFLOW.md) for full format, flow, and checklist.
