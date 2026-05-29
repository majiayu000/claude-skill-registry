---
name: intent-capture
description: Capture user intent through guided conversation. Exploratory phase with high degrees of freedom.
version: 1.0.0
---

<objective>
Capture user intent through guided conversation.
</objective>

<triggers>
  - No active intent exists
  - User wants to start something new
</triggers>

<degrees_of_freedom>
  **HIGH** — This is a creative, exploratory phase. Ask open-ended questions. Don't constrain prematurely.
</degrees_of_freedom>

<llm critical="true">
  <mandate>NEVER assume requirements — ALWAYS ask clarifying questions</mandate>
  <mandate>Capture the "what" and "why" — leave the "how" for decomposition</mandate>
  <mandate>Let user describe freely — don't interrupt</mandate>
</llm>

<flow>
  <step n="1" title="Initial Question">
    <ask>What do you want to build?</ask>
    <listen>Let user describe freely. Don't interrupt.</listen>
  </step>

  <step n="2" title="Elicit Context">
    <action>Based on response, ask follow-up questions:</action>

    <question if="unclear who benefits">
      Who is this for? Who will use this feature?
    </question>

    <question if="unclear problem">
      What problem does this solve? What's painful today?
    </question>

    <question if="unclear scope">
      What's the minimum that would be valuable? What can wait?
    </question>

    <question if="unclear constraints">
      Any technical constraints? Existing systems to integrate with?
    </question>

    <question if="unclear success">
      How will you know this is working? What does success look like?
    </question>
  </step>

  <step n="3" title="Summarize Understanding">
    <output>
      Let me make sure I understand:

      **Goal**: {summarized goal}

      **Users**: {who benefits}

      **Problem**: {what pain this solves}

      **Success Criteria**:
      - {criterion 1}
      - {criterion 2}
      - {criterion 3}

      **Constraints**:
      - {constraint 1}
      - {constraint 2}

      Is this accurate? [Y/n/edit]
    </output>
    <check if="response == n or edit">
      <action>Ask specific clarifying questions</action>
      <goto step="3"/>
    </check>
  </step>

  <step n="4" title="Generate Intent Brief">
    <action>Create intent ID from title (kebab-case)</action>
    <action>Generate intent brief using template: templates/brief.md.hbs</action>
    <action>Create directory: .specs-fire/intents/{intent-id}/</action>
    <action>Save: .specs-fire/intents/{intent-id}/brief.md</action>
  </step>

  <step n="5" title="Update State">
    <action>Add intent to state.yaml</action>
    <action>Set intent status to "in_progress"</action>
  </step>

  <step n="6" title="Transition">
    <output>
      **Intent captured**: "{intent-title}"

      Saved to: .specs-fire/intents/{intent-id}/brief.md

      ---

      Ready to break this into work items? [Y/n]
    </output>
    <check if="response == y">
      <invoke_skill>work-item-decompose</invoke_skill>
    </check>
  </step>
</flow>

<output_artifacts>

  | Artifact | Location | Template |
  |----------|----------|----------|
  | Intent Brief | `.specs-fire/intents/{id}/brief.md` | `./templates/brief.md.hbs` |
</output_artifacts>

<success_criteria>
  <criterion>User intent fully understood through dialogue</criterion>
  <criterion>Goal, users, problem clearly captured</criterion>
  <criterion>Success criteria defined</criterion>
  <criterion>Constraints identified</criterion>
  <criterion>Intent brief saved to correct location</criterion>
  <criterion>State.yaml updated with new intent</criterion>
</success_criteria>
