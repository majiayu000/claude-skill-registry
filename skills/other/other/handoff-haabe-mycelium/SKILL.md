---
name: handoff
description: "Generate structured handoff materials for offline human tasks (interviews, observations, outreach). Creates actionable briefs with phone-friendly capture templates."
instruction_budget: 47
---

# Handoff Skill

Generate structured materials for tasks the human does offline. Bridges the gap between "we need external evidence" and "here's exactly what to do and bring back."

## When to Use

- When the Evidence Gate source ratio nudge fires (all evidence is desk-derived)
- When `/diamond-progress` identifies a need for external validation
- When the agent identifies an assumption that requires human contact to validate
- When the user asks "what should I do next offline?"
- **Proactively**: whenever a human-executable task is identified, offer to run `/handoff` before the user asks

## Workflow

1. **Identify the evidence gap**:
   - Read active diamond state from `diamonds/active.yml`
   - Check canvas provenance for `source_classes` distribution
   - Identify which canvas sections lack `external_human` or `external_data` evidence
   - State the gap plainly: "We have [N] evidence sources but none from real conversations."

2. **Determine task type**:
   - `interview` -- structured conversation with a target user/stakeholder
   - `observation` -- watch someone use a competitor product or perform a task
   - `survey` -- collect structured responses from multiple people
   - `usability_test` -- test a prototype or concept with a real user
   - `stakeholder_meeting` -- align with a decision-maker or domain expert
   - `experiential_research` -- try a competitor product yourself with structured observation

3. **Generate Task Brief**:

   ```
   ## Task Brief: [Objective in one sentence]

   **Type**: [interview/observation/survey/usability_test/stakeholder_meeting/experiential_research]
   **Diamond**: [diamond ID and name]
   **Evidence gap**: [which canvas section needs external evidence]
   **Priority**: [high/medium/low]

   ### Who to Talk To
   [Specific persona description or named contact if known.
   Include: role, context, why this person's perspective matters.]

   ### Key Questions (3-5, Torres-style)
   1. [Story-based, open-ended question -- "Tell me about the last time you..."]
   2. [Follow the energy -- "What was the hardest part of that?"]
   3. [Probe for JTBD -- "What were you trying to accomplish?"]
   4. [Uncover workarounds -- "How do you handle that today?"]
   5. [Emotional/social dimension -- "How did that make you feel?"]

   ### What NOT to Ask
   - [Leading question to avoid, e.g., "Don't you think X would be useful?"]
   - [Confirmation-seeking framing to avoid]
   - [Hypothetical future questions -- ask about past behavior instead]

   ### What to Observe (if applicable)
   - [Specific behaviors to watch for]
   - [Workarounds, friction points, emotional reactions]

   ### Success Criteria
   [What constitutes a useful conversation, e.g.,
   "Learned at least one unexpected JTBD" or
   "Found a workaround we hadn't considered"]
   ```

4. **Generate Capture Template** (phone-friendly, plain text):

   ```
   ---
   CAPTURE: [task objective]
   ---
   Date:
   Person (role, not name):
   Context (how do they relate to the problem):

   Key quotes (verbatim if possible):
   -
   -

   Surprising finding (anything you didn't expect):

   JTBD signals:
     Functional (what they're trying to do):
     Emotional (how they feel about it):
     Social (how others perceive them):

   Workarounds they use today:

   Contradicts our assumptions? (yes/no, which one):

   Follow-up needed? (yes/no, what):
   ---
   ```

5. **Write to `canvas/human-tasks.yml`**:
   - Add a `pending_tasks` entry with all fields populated
   - Set `status: pending`
   - Link to the relevant canvas section via `canvas_refs`

6. **Tell the user what to bring back**:
   "When you've completed this, run `/log-evidence` to record your findings. I'll update the canvas and recalculate confidence. Bring back:
   - Your filled capture template(s)
   - Any screenshots or artifacts
   - Your overall impression in a sentence or two"

## Canvas Output

- Writes to: `canvas/human-tasks.yml` (pending_tasks section)
- References: whatever canvas section has the evidence gap

## Theory Citations

- Torres (Continuous Discovery Habits): Story-based interview questions, weekly touchpoints
- Christensen (JTBD): Functional, emotional, social dimensions in capture template
- Shotton/Kahneman: Bias-aware question design (avoid leading, confirmation-seeking)
- Meza: Systemic bias diagnosis -- structured handoff addresses the motivation gap for external evidence
