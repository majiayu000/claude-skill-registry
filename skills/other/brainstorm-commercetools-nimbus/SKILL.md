---
name: brainstorming
description:
  "You MUST use this before any creative work - creating features, building
  components, adding functionality, or modifying behavior. Explores user intent,
  requirements and design before implementation."
---

# Brainstorming Ideas Into Designs

## Overview

Help turn ideas into fully formed designs and specs through natural
collaborative dialogue.

Start by understanding the current project context, then ask questions one at a
time to refine the idea. Once you understand what you're building, present the
design in small sections (200-300 words), checking after each section whether it
looks right so far.

## The Process

**Understanding the idea:**

**Note**: This skill is typically invoked by agents like nimbus-researcher when
requirements are unclear. You can also invoke it directly when:

- Starting a new component and need to explore design options
- Facing architectural decisions with multiple valid approaches
- Requirements are ambiguous and need clarification

For complete component creation with OpenSpec integration, use
`/propose-component` command instead.

- You SHOULD begin by reviewing the current project state (files, docs, recent
  commits). This ensures the design fits existing patterns and doesn't duplicate
  work.
- You SHOULD ask questions one at a time to refine the idea. This creates a
  focused conversation and helps clarify requirements incrementally.
- You MAY prefer multiple choice questions when they clarify options quickly,
  but open-ended questions are fine too—choose based on conversation flow.
- You SHOULD structure exploration into separate messages if multiple topics
  need investigation. This prevents overwhelming both parties.
- You MUST focus on understanding: purpose, constraints, and success criteria.

**Exploring approaches:**

- You SHOULD propose 2-3 different approaches with trade-offs. This explores the
  design space and prevents premature convergence on the first idea.
- You SHOULD present options conversationally with your recommendation and
  reasoning. Explain why you're recommending one approach over others.
- You MUST lead with your RECOMMENDED option and explain the trade-offs. Help
  the user understand your reasoning before they decide.

**Presenting the design:**

- You SHOULD verify you understand the full scope before presenting (not just
  your initial interpretation). Ask clarifying questions until you can describe
  what's being built with confidence.
- You MUST present design in reviewable sections (200-300 words each). This lets
  the user verify direction incrementally rather than discovering misalignment
  at the end.
- You MUST ask after each section whether it looks right so far. If it doesn't,
  correct the misalignment before moving forward.
- You MUST cover: architecture, components, data flow, error handling, and
  testing. Missing any of these creates gaps later.
- You SHOULD be ready to go back and clarify if something doesn't make sense.
  This is normal and expected.

## After the Design

**Next Steps:**

- You have a validated design/plan document
- User can choose their next step:
  - Create an OpenSpec proposal via `/openspec:proposal` for formal
    specification
  - Use the plan for implementation planning
  - Continue refining the design if needed
  - Save the plan for later reference
- Ask the user what they'd like to do next

## Key Principles

- **YAGNI ruthlessly**: You MUST remove unnecessary features from all designs.
  Scope creep at design time is easier to fix than during implementation.

- **Explore alternatives**: You SHOULD propose 2-3 approaches with trade-offs
  before settling on the recommended approach. This prevents the "first idea"
  bias and helps users understand the design space.

- **Incremental validation**: You MUST present design in sections and ask after
  each one. Discovering fundamental misalignment after 30 minutes of work is
  wasteful.

- **Be flexible with clarification**: You SHOULD be ready to go back and ask
  clarifying questions when something doesn't make sense. This is normal and
  expected, not a failure.

- **Focus on patterns**: You MUST ensure designs align with established Nimbus
  patterns and standards (see ./openspec/AGENTS.md for project architecture).
  Consistency reduces learning curve for implementers.
