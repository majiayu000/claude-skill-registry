---
name: doc-create-adr-gamma
description: "{{ ƔƔƔ }} Create an Architecture Decision Record (ADR) for a significant technical decision"
model: sonnet
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Write"]
argument-hint: [brief decision title]
---

<overview>
  Guide user through creating an ADR via focused questions, then generate using ~/.claude/doc-templates/ADR.md
</overview>
<template-location>
  ~/.claude/doc-templates/ADR.md
</template-location>
<steps>
  1. Read ADR template
  2. Ask focused questions conversationally (not all at once):
     - Context: What problem/decision? What factors? Constraints?
     - Decision: What did you choose? Be specific.
     - Alternatives: What else considered? Pros/cons? Why rejected?
     - Consequences: What improves? What trade-offs? What gets harder?
  3. Generate ADR with proper numbering (check existing in docs/dev/architecture/)
  4. Suggest location: docs/dev/architecture/[decision-slug]-adr.md
  5. Show for approval; revise if needed
</steps>
<notes>
  - Keep questions conversational
  - Probe for details if answers incomplete
  - ADR should be understandable 6 months later
</notes>
