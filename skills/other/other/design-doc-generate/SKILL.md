---
name: design-doc-generate
description: Generate design documents for Validate mode work items (Checkpoint 1). Required for high-complexity items.
version: 1.0.0
---

<objective>
Generate design documents for Validate mode work items (Checkpoint 1).
</objective>

<triggers>
  - Work item has complexity: high
  - Work item has mode: validate
  - Design review required before implementation
</triggers>

<degrees_of_freedom>
  **LOW** — Follow the design doc structure precisely. Decisions must have rationale.
</degrees_of_freedom>

<llm critical="true">
  <mandate>Design doc MUST be approved before implementation</mandate>
  <mandate>Document DECISIONS with RATIONALE, not just choices</mandate>
  <mandate>Keep concise — enough detail to implement, no more</mandate>
  <mandate>Include risks upfront — don't hide complexity</mandate>
</llm>

<flow>
  <step n="1" title="Analyze Work Item">
    <action>Read work item from .specs-fire/intents/{intent-id}/work-items/{id}.md</action>
    <action>Identify key design decisions needed</action>
    <action>Assess domain modeling needs</action>
    <action>Identify integration points</action>
  </step>

  <step n="2" title="Gather Context">
    <action>Review project standards (.specs-fire/standards/)</action>
    <action>Check existing codebase patterns</action>
    <action>Identify similar implementations to reference</action>
  </step>

  <step n="3" title="Draft Key Decisions">
    <action>For each decision point:</action>
    <substep>Identify options considered</substep>
    <substep>Evaluate trade-offs</substep>
    <substep>Select recommended choice</substep>
    <substep>Document rationale</substep>

    <output_format>
      | Decision | Choice | Rationale |
      |----------|--------|-----------|
      | ... | ... | ... |
    </output_format>
  </step>

  <step n="4" title="Define Domain Model" if="has_domain_complexity">
    <action>Identify entities (things with identity)</action>
    <action>Identify value objects (immutable values)</action>
    <action>Identify domain events (if event-driven)</action>
    <action>Map relationships</action>
  </step>

  <step n="5" title="Design Technical Approach">
    <action>Create component diagram (ASCII)</action>
    <action>Define API contracts (if applicable)</action>
    <action>Specify database changes (if applicable)</action>
    <action>Document data flow</action>
  </step>

  <step n="6" title="Identify Risks">
    <action>List potential risks</action>
    <action>Assess impact (high/medium/low)</action>
    <action>Propose mitigations</action>

    <output_format>
      | Risk | Impact | Mitigation |
      |------|--------|------------|
      | ... | ... | ... |
    </output_format>
  </step>

  <step n="7" title="Create Implementation Checklist">
    <action>Break down into implementation steps</action>
    <action>Order by dependency</action>
    <action>Keep granular but not excessive</action>
  </step>

  <step n="8" title="Present Design Doc">
    <checkpoint message="Design document ready for review">
      <output>
        # Design: {work-item-title}

        ## Summary
        {brief description}

        ## Key Decisions
        {decisions table}

        ## Technical Approach
        {component diagram, API contracts}

        ## Risks
        {risks table}

        ## Implementation Checklist
        {ordered steps}

        ---
        This is Checkpoint 1 of Validate mode.

        Approve design? [Y/n/edit]
      </output>
    </checkpoint>
  </step>

  <step n="9" title="Handle Response">
    <check if="response == y">
      <action>Generate design doc using template: templates/design.md.hbs</action>
      <action>Save to: .specs-fire/intents/{intent-id}/work-items/{id}-design.md</action>
      <action>Mark checkpoint 1 as passed</action>
      <output>
        Design approved. Ready for implementation planning.

        Route to Builder for Checkpoint 2 (implementation plan)? [Y/n]
      </output>
    </check>
    <check if="response == edit">
      <ask>What changes are needed?</ask>
      <action>Incorporate feedback</action>
      <goto step="8"/>
    </check>
    <check if="response == n">
      <output>Design rejected. What concerns need to be addressed?</output>
      <action>Gather feedback, revise approach</action>
      <goto step="3"/>
    </check>
  </step>
</flow>

<output_artifacts>

  | Artifact | Location | Template |
  |----------|----------|----------|
  | Design Doc | `.specs-fire/intents/{intent-id}/work-items/{id}-design.md` | `./templates/design.md.hbs` |
</output_artifacts>

<success_criteria>
  <criterion>Work item analyzed for design decisions</criterion>
  <criterion>Key decisions documented with rationale</criterion>
  <criterion>Domain model defined (if applicable)</criterion>
  <criterion>Technical approach specified</criterion>
  <criterion>Risks identified with mitigations</criterion>
  <criterion>Implementation checklist created</criterion>
  <criterion>Design doc approved at checkpoint</criterion>
  <criterion>Design doc saved to correct location</criterion>
</success_criteria>
