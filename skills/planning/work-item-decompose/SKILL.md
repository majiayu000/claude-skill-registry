---
name: work-item-decompose
description: Break an intent into discrete, executable work items with complexity assessment and dependency validation.
version: 1.0.0
---

<objective>
Break an intent into discrete, executable work items.
</objective>

<triggers>
  - Intent exists without work items
  - User wants to plan execution
</triggers>

<degrees_of_freedom>
  **MEDIUM** — Follow decomposition patterns but adapt to the specific intent.
</degrees_of_freedom>

<llm critical="true">
  <mandate>Each work item MUST be completable in a single run</mandate>
  <mandate>Each work item MUST have clear acceptance criteria</mandate>
  <mandate>Dependencies MUST be explicit and validated</mandate>
</llm>

<flow>
  <step n="1" title="Load Intent">
    <action>Read intent brief from .specs-fire/intents/{intent-id}/brief.md</action>
    <action>Understand goal, users, success criteria</action>
  </step>

  <step n="2" title="Identify Deliverables">
    <action>Break intent into discrete deliverables</action>
    <action>Each deliverable should be independently valuable</action>

    <guidelines>
      - Prefer vertical slices over horizontal layers
      - Start with foundation pieces (models, schemas)
      - End with integration pieces (API, UI)
      - Keep each item focused on ONE concern
    </guidelines>
  </step>

  <step n="3" title="Assess Complexity">
    <action>For each work item, assess RAW complexity:</action>

    <complexity level="low">
      - Single file or few files
      - Well-understood pattern
      - No external dependencies
      - Examples: bug fix, config change, simple utility
    </complexity>

    <complexity level="medium">
      - Multiple files
      - Standard patterns with some decisions
      - May touch existing code
      - Examples: new endpoint, new component, feature addition
    </complexity>

    <complexity level="high">
      - Architectural decisions required
      - Security or data implications
      - Core system changes
      - Examples: auth system, payment flow, database migration
    </complexity>
  </step>

  <step n="3b" title="Apply Autonomy Bias">
    <action>Read workspace.autonomy_bias from state.yaml</action>
    <action>Apply bias to determine final execution mode:</action>

    <bias_table>
      | Raw Complexity | autonomous | balanced | controlled |
      |----------------|------------|----------|------------|
      | low            | autopilot  | autopilot| confirm    |
      | medium         | autopilot  | confirm  | validate   |
      | high           | confirm    | validate | validate   |
    </bias_table>

    <note>
      This allows user preference to shift thresholds:
      - autonomous: trusts AI more, fewer checkpoints
      - balanced: standard behavior (default)
      - controlled: more human oversight
    </note>
  </step>

  <step n="4" title="Define Acceptance Criteria">
    <action>For each work item, define:</action>
    <substep>What must be true when complete</substep>
    <substep>How to verify it works</substep>
    <substep>Any edge cases to handle</substep>
  </step>

  <step n="5" title="Validate Dependencies">
    <action>Check for circular dependencies</action>
    <action>Ensure dependencies exist or will be created first</action>
    <action>Order work items by dependency</action>

    <check if="circular dependency detected">
      <output>
        Warning: Circular dependency detected between {item-a} and {item-b}.
        Suggest splitting into smaller items or reordering.
      </output>
    </check>
  </step>

  <step n="6" title="Present Plan">
    <output>
      ## Work Items for "{intent-title}"

      **Total**: {count} work items
      **Estimated**: {low} autopilot, {medium} confirm, {high} validate

      **Work Item Details**:

      {for each item}
      {n}. **{title}** ({mode}) — {description}
      {/for}

      ---

      Approve this plan? [Y/n/edit]
    </output>
  </step>

  <step n="7" title="Save Work Items">
    <check if="approved">
      <action>Create .specs-fire/intents/{intent-id}/work-items/</action>
      <action>For each work item, generate using template: templates/work-item.md.hbs</action>
      <action>Save each to: .specs-fire/intents/{intent-id}/work-items/{work-item-id}.md</action>
      <action>Update state.yaml with work items list</action>
    </check>
  </step>

  <step n="8" title="Transition">
    <output>
      **{count} work items created** for "{intent-title}".

      ---

      Ready to plan execution scope? [Y/n]
    </output>
    <check if="response == y">
      <route_to>builder-agent (run-plan)</route_to>
    </check>
  </step>
</flow>

<output_artifacts>

  | Artifact | Location | Template |
  |----------|----------|----------|
  | Work Item | `.specs-fire/intents/{intent-id}/work-items/{id}.md` | `./templates/work-item.md.hbs` |
</output_artifacts>

<success_criteria>
  <criterion>Intent decomposed into discrete work items</criterion>
  <criterion>Each work item has clear acceptance criteria</criterion>
  <criterion>Complexity assessed for each item</criterion>
  <criterion>Autonomy bias applied to determine modes</criterion>
  <criterion>Dependencies validated (no circular dependencies)</criterion>
  <criterion>Work items saved to correct locations</criterion>
  <criterion>State.yaml updated with work items list</criterion>
</success_criteria>
