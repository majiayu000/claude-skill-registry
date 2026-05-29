---
name: walkthrough-generate
description: Generate implementation walkthrough for human review after run completion. Documents decisions, changes, and verification steps.
version: 1.0.0
---

<objective>
Generate implementation walkthrough for human review after run completion.
</objective>

<triggers>
  - Run completed successfully
  - Invoked by run-execute skill
</triggers>

<degrees_of_freedom>
  **LOW** — Follow walkthrough structure precisely. Be thorough but concise.
</degrees_of_freedom>

<llm critical="true">
  <mandate>ALWAYS generate walkthrough after run completion</mandate>
  <mandate>Document DECISIONS, not just changes</mandate>
  <mandate>Include verification steps — how to test this works</mandate>
  <mandate>Track DEVIATIONS from plan — compare to original work item</mandate>
  <mandate>List ALL new dependencies added during implementation</mandate>
  <mandate>Capture developer notes — gotchas save future debugging time</mandate>
</llm>

<flow>
  <step n="1" title="Gather Implementation Data">
    <action>Read run log from .specs-fire/runs/{run-id}/run.md</action>
    <action>Read work item plan from .specs-fire/intents/{intent}/work-items/{work-item}/</action>
    <action>Collect:</action>
    <substep>Work item details (id, title, intent)</substep>
    <substep>Files created during implementation</substep>
    <substep>Files modified during implementation</substep>
    <substep>Decisions made during execution</substep>
    <substep>Tests added and coverage</substep>
    <substep>Dependencies added (new packages in package.json, requirements.txt, etc.)</substep>
    <substep>Deviations from the original work item plan</substep>
  </step>

  <step n="2" title="Analyze Implementation">
    <action>For each file created/modified:</action>
    <substep>Identify purpose of the file</substep>
    <substep>Summarize key changes</substep>
    <substep>Note patterns or approaches used</substep>
    <action>Document structure overview:</action>
    <substep>How the pieces fit together architecturally</substep>
    <substep>Data flow or component relationships</substep>
    <substep>Keep high-level, NO CODE</substep>
    <action>Identify architecture pattern (if multi-component):</action>
    <substep>Pattern used (Repository, Service Layer, MVC, Clean Architecture, etc.)</substep>
    <substep>Layer structure diagram (ASCII) if applicable</substep>
    <action>Document domain model (if entities/models created):</action>
    <substep>Entities with properties and business rules</substep>
    <substep>Value objects with constraints</substep>
  </step>

  <step n="3" title="Document Key Details">
    <action>Extract implementation highlights:</action>
    <substep>Main flow/algorithm implemented</substep>
    <substep>Integration points with existing code</substep>
    <action>Document security considerations (if applicable):</action>
    <substep>Authentication/authorization approach</substep>
    <substep>Input validation strategy</substep>
    <substep>Data protection measures</substep>
    <substep>Format as table: Concern | Approach</substep>
    <action>Document performance considerations (if applicable):</action>
    <substep>Optimization strategies used</substep>
    <substep>Caching, indexing, or query optimization</substep>
    <substep>Scalability approach</substep>
    <substep>Format as table: Requirement | Implementation</substep>
    <action>Document deviations from plan:</action>
    <substep>Compare implementation to original work item plan</substep>
    <substep>Note any changes and explain WHY they were made</substep>
    <substep>If no deviations, state "None"</substep>
    <action>Capture developer notes:</action>
    <substep>Gotchas or non-obvious behaviors</substep>
    <substep>Tips for future developers</substep>
    <substep>Context that would save debugging time</substep>
  </step>

  <step n="4" title="Create Verification Steps">
    <action>Generate how-to-verify section:</action>
    <substep>Commands to run the feature</substep>
    <substep>Expected behavior/output</substep>
    <substep>Manual test scenarios</substep>
  </step>

  <step n="5" title="Assess Ready for Review">
    <action>Evaluate implementation completeness:</action>
    <substep>All acceptance criteria met?</substep>
    <substep>Tests passing?</substep>
    <substep>No critical issues remaining?</substep>
    <substep>Documentation updated (if applicable)?</substep>
    <substep>Developer notes captured?</substep>
    <action>Generate checklist with [x] for met, [ ] for unmet</action>
  </step>

  <step n="6" title="Generate Walkthrough">
    <action>Generate walkthrough using template: templates/walkthrough.md.hbs</action>
    <action>Include all sections (conditional sections only if data exists):</action>
    <substep>Architecture — only if multi-component with clear pattern</substep>
    <substep>Domain Model — only if entities/value objects created</substep>
    <substep>Security Considerations — only if security-relevant changes</substep>
    <substep>Performance Considerations — only if performance-relevant changes</substep>
    <action>Save to: .specs-fire/runs/{run-id}/walkthrough.md</action>
    <output>
      Walkthrough generated: .specs-fire/runs/{run-id}/walkthrough.md
    </output>
  </step>
</flow>

<output_template>
  **Walkthrough** (`.specs-fire/runs/{run-id}/walkthrough.md`):

  ````markdown
  ---
  run: {run-id}
  work_item: {work-item-id}
  intent: {intent-id}
  generated: {timestamp}
  mode: {mode}
  ---

  # Implementation Walkthrough: {title}

  ## Summary

  {2-3 sentences describing what was implemented}

  ## Structure Overview

  {High-level description of how pieces fit together - NO CODE}

  ## Architecture (if multi-component)

  ### Pattern Used
  {Pattern and rationale - e.g., Repository pattern for data access abstraction}

  ### Layer Structure
  ```text
  ┌─────────────────────────────┐
  │      Presentation           │
  ├─────────────────────────────┤
  │      Application            │
  ├─────────────────────────────┤
  │        Domain               │
  ├─────────────────────────────┤
  │     Infrastructure          │
  └─────────────────────────────┘
  ```

## Files Changed

### Created

  | File | Purpose |
  |------|---------|
  | `{path}` | {purpose} |

### Modified

  | File | Changes |
  |------|---------|
  | `{path}` | {changes} |

## Domain Model (if entities created)

### Entities

  | Entity | Properties | Business Rules |
  |--------|------------|----------------|
  | {name} | {props} | {rules} |

### Value Objects

  | Value Object | Properties | Constraints |
  |--------------|------------|-------------|
  | {name} | {props} | {constraints} |

## Key Implementation Details

### 1. {Detail Title}

  {description of implementation approach}

## Security Considerations (if applicable)

  | Concern | Approach |
  |---------|----------|
  | {concern} | {approach} |

## Performance Considerations (if applicable)

  | Requirement | Implementation |
  |-------------|----------------|
  | {requirement} | {implementation} |

## Decisions Made

  | Decision | Choice | Rationale |
  |----------|--------|-----------|
  | {decision} | {choice} | {rationale} |

## Deviations from Plan

  {Changes from work item plan and why, or "None"}

## Dependencies Added

  | Package | Why Needed |
  |---------|------------|
  | `{package}` | {reason} |

## How to Verify

  1. **{Step Title}**

     ```bash
     {command}
     ```

     Expected: {expected output}

## Test Coverage

- Tests added: {count}
- Coverage: {percentage}%
- Status: {passing/failing}

## Ready for Review

- [x] All acceptance criteria met
- [x] Tests passing
- [x] No critical issues
- [ ] Documentation updated (if applicable)
- [x] Developer notes captured

## Developer Notes

  {Gotchas, tips, or context for future work - keep brief}

  ---
  *Generated by specs.md - fabriqa.ai FIRE Flow Run {run-id}*

  ````

</output_template>

<success_criteria>
  <criterion>Walkthrough generated with all applicable sections</criterion>
  <criterion>Structure overview explains architecture (NO CODE)</criterion>
  <criterion>Architecture pattern documented (if multi-component)</criterion>
  <criterion>Domain model documented (if entities created)</criterion>
  <criterion>Files changed documented with purposes</criterion>
  <criterion>Security considerations documented (if security-relevant)</criterion>
  <criterion>Performance considerations documented (if performance-relevant)</criterion>
  <criterion>Decisions recorded with rationale</criterion>
  <criterion>Deviations from plan documented (or "None")</criterion>
  <criterion>Dependencies added listed with reasons</criterion>
  <criterion>Verification steps included</criterion>
  <criterion>Ready for Review checklist completed</criterion>
  <criterion>Developer notes capture gotchas and tips</criterion>
  <criterion>Saved to run folder</criterion>
</success_criteria>
