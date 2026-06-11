---
name: professional-communication
description: "Draft interpersonal and meeting messages — emails, memos, status updates, and pushing back or disagreeing in a structured business format."
user-invocable: false
allowed-tools:
  - Read
  - Write
routing:
  triggers:
    - "business communication"
    - "structured format"
    - "clear writing"
    - "write email"
    - "draft memo"
    - "executive summary"
    - "summarize for management"
    - "status update"
  not_for: "critiquing or stress-testing a proposal's merits — that is multi-persona-critique. This drafts the message, it does not judge the idea."
  category: content-creation
  pairs_with:
    - voice-writer
    - pptx-generator
---

# Professional Communication Skill

## Overview

This skill transforms dense technical communication into clear, structured business formats using **proposition extraction** (identify all facts and relationships) and **deterministic templates** (apply consistent structure). It extracts every detail without loss, categorizes by business relevance, applies a standard template with professional tone, and verifies completeness before delivery.

**Core principle**: Transformation ≠ creation. Only restructure existing input; always extract from existing input and restructure it for executive clarity with preserved technical accuracy.

---

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| transforming raw engineer notes: stream-of-consciousness debugging, blockers, crisis updates | `examples.md` | Loads detailed guidance from `examples.md`. |
| drafting from section templates; phrase transformations | `templates.md` | Loads detailed guidance from `templates.md`. |

## Instructions

### Phase 1: PARSE

**Goal**: Extract every proposition from the input before structuring anything. This prevents information loss and ensures technical accuracy is preserved.

**Step 1: Classify input type**

Identify the communication type (this determines categorization strategy in Phase 2):
- Technical update (progress report with embedded facts)
- Debugging narrative (stream-of-consciousness problem-solving)
- Status report (project state with blockers/dependencies)
- Dependency discussion (constraints buried in defensive language)

**Step 2: Extract all propositions**

Parse each sentence systematically. Extract all propositions before summarizing — summarizing skips propositions and loses facts:

1. **Facts**: All distinct statements of truth
2. **Implications**: Cause-effect relationships
3. **Temporal markers**: Past/present/future actions
4. **System references**: All mentioned components
5. **Blockers**: Hidden dependencies and constraints
6. **Emotional context**: Frustration/satisfaction/urgency indicators (needed to transform defensive language)

**Step 3: Document implicit context**

Surface assumptions the author takes for granted but the audience needs stated. Non-technical audiences cannot act without this:
- Technical acronyms or project names the audience may not know
- Timeline context (when things happened relative to milestones)
- Organizational context (team relationships, reporting structures)

**Step 4: Count and validate propositions**

```markdown
## Parsing Result
Input type: [technical update | debugging narrative | status report | dependency discussion]
Proposition count: [N distinct facts/claims]
Emotional markers: [frustration | satisfaction | urgency | neutral]

Extracted Propositions:
1. [Fact/claim 1]
2. [Fact/claim 2]
... (ALL propositions - NO information loss)

Implicit Context:
- [Assumption 1]
- [Assumption 2]
```

**Gate**: ALL propositions extracted with zero information loss. Proceed only when gate passes.

### Phase 2: STRUCTURE

**Goal**: Categorize and prioritize all extracted propositions by business relevance. This prevents unsolicited sections and keeps output focused on what matters most.

**Step 1: Categorize propositions**

Organize by type (categorization determines template section placement):

```markdown
Status:   [items with current state]
Actions:  [completed, in-progress, planned]
Impacts:  [business and technical consequences]
Blockers: [dependencies, constraints]
Next:     [required actions]
```

**Step 2: Priority order**

Rank by impact to executive decision-making, not completeness:

1. Business Impact (revenue, customer, strategic)
2. Technical Functionality (core operation)
3. Project Timeline (schedule implications)
4. Resource Requirements (personnel, infrastructure)
5. Risk Management (potential issues)

Only the highest-priority categories go into the output. Lower-priority items are preserved in Technical Details but not emphasized.

**Step 3: Identify information gaps**

Flag any propositions that need clarification before transformation. Ask for specifics only when severity classification is ambiguous:
- Ambiguous severity (could be GREEN or YELLOW — default to YELLOW if unclear)
- Missing ownership for action items (block on clarity, ask for clarity)
- Undefined technical terms critical to business impact (ask for definition)

**Gate**: All propositions categorized and prioritized. Proceed only when gate passes.

### Phase 3: TRANSFORM

**Goal**: Apply standard template with professional tone. This ensures consistent, executive-ready formatting without speculative sections.

**Step 1: Apply standard template**

Include only the sections in the standard template (Risk Assessment, Historical Context, Mitigation Strategies). Use ONLY this structure:

```markdown
**STATUS**: [GREEN|YELLOW|RED]
**KEY POINT**: [Single most important business takeaway]

**Summary**:
- [Primary accomplishment/issue]: [Business impact]
- [Current focus/blocker]: [Expected outcome/resolution need]
- [Secondary consideration]: [Implications]

**Technical Details**:
[2-3 sentences maximum preserving technical accuracy]

**Next Steps**:
1. [Specific action with timeline if available]
2. [Secondary action with ownership implications]
3. [Follow-up considerations]
```

**Step 2: Tone adjustment**

The transformation rules are deterministic (apply all):
- Strip hedging language: "I think we might need to..." → "Deploy X to address Y"
- Transform defensive tone: "We had to rollback because..." → "Rolled back to [previous version] due to [root cause]"
- Preserve urgency markers and severity indicators (needed for status classification)
- Keep technical terms intact (oversimplification loses information; non-technical audiences still need accuracy)
- Maintain causal chains and specific metrics (specific > generic)

**Step 3: Status classification**

Apply criteria consistently (inconsistency confuses stakeholders and erodes trust):

- **GREEN**: Fully complete with no follow-up, all verification done
- **YELLOW**: Resolved with follow-up needed, blocked on dependencies, partial completion
- **RED**: Active critical issues, production impact, urgent intervention needed

Always document reasoning: "Status: YELLOW (deployment successful but monitoring pending)" not just "Status: YELLOW"

**Step 4: Action item specificity**

Vague action items cannot be executed. Every next step MUST include:
- Specific action verb (investigate, deploy, coordinate, document) — "fix" is too vague
- Clear scope (what exactly needs doing) — define the boundary
- Ownership implication (who or which team) — someone must be accountable
- Timeline marker when available (IMMEDIATE, by EOW, this sprint) — explicit > implied

**Gate**: Output follows template structure with professional tone and all specificity rules applied. Proceed only when gate passes.

### Phase 4: VERIFY

**Goal**: Confirm transformation quality before delivery. All gates must pass; proceed only when complete.

**Step 1**: Compare output against extracted propositions — NO information loss allowed. If a fact from Phase 1 doesn't appear in output, it belongs in Technical Details.

**Step 2**: Verify technical accuracy — terms, metrics, causal chains preserved exactly. Preserve exact technical terms ("database issues" for "Redis cluster failover") — specificity is required.

**Step 3**: Confirm status indicator matches actual severity. Check reasoning against actual criteria (GREEN ≠ YELLOW vs YELLOW ≠ RED boundaries).

**Step 4**: Validate action items are specific — check each next step for (verb, scope, owner, timeline). "Fix the issue" fails; "Complete Redis failover testing in staging (DevOps, by EOW)" passes.

**Step 5**: Check appropriate detail level for target audience. If audience is non-technical, Technical Details should bridge jargon with plain explanations without losing precision.

**Step 6**: Document transformation summary to prove gate passage:

```markdown
## Transformation Summary
Input type: [type]
Propositions extracted: [N]
Status assigned: [GREEN|YELLOW|RED] ([reasoning])
Information loss: None
Template applied: standard
```

**Gate**: All verification checks pass. Transformation is complete. Complete all 6 steps before delivering.

---

## Examples

### Example 1: Multi-Propositional Sentence
User says: "I fixed the database issue but then the API started failing so I had to rollback and now we're investigating the connection pool settings which might be related to the recent Kubernetes upgrade."
Actions:
1. Extract 5 propositions: DB fix, API failure, rollback, pool investigation, K8s link (PARSE)
2. Categorize: Status=rollback done, Blockers=pool+K8s, Actions=investigating (STRUCTURE)
3. Apply template with YELLOW status, specific next steps (TRANSFORM)
4. Verify no facts lost, technical terms preserved (VERIFY)
Result: Structured update with clear status and actionable next steps

### Example 2: Defensive Blocker Communication
User says: "I can't make progress because the API team hasn't responded in 3 days and my sprint is at risk"
Actions:
1. Extract urgency, duration, dependency, impact propositions (PARSE)
2. Categorize: Blocker=API spec, Impact=sprint risk, Timeline=3 days (STRUCTURE)
3. Apply template with YELLOW status, escalation-focused next steps (TRANSFORM)
4. Verify urgency preserved, defensive tone neutralized (VERIFY)
Result: Neutral status report with clear escalation path

### Example 3: Crisis Communication
User says: "The latest deploy broke checkout completely, users are getting 500 errors, we rolled back but some orders might be lost"
Actions:
1. Extract severity, system affected, user impact, rollback status, data risk (PARSE)
2. Categorize: Status=rolled back, Impact=orders lost, Blocker=data recovery (STRUCTURE)
3. Apply template with RED status, IMMEDIATE/URGENT tiered next steps (TRANSFORM)
4. Verify crisis severity reflected, no false reassurance in tone (VERIFY)
Result: RED status report with tiered emergency response actions

---

## Error Handling

### Error: "Missing Context in Input"
**Cause**: Technical terms or acronyms critical to business impact are undefined.

**Solution**:
1. Ask user for clarification on terms critical to status classification — speculation causes wrong status assignments
2. Make reasonable inferences only for minor details; flag all assumptions explicitly in Technical Details section
3. Complete transformation while waiting — provide output with a note: "Status classification assumed X because Y was undefined"

### Error: "Ambiguous Status Classification"
**Cause**: Input contains mixed signals (e.g., issue resolved but monitoring incomplete).

**Solution**:
1. Default to YELLOW when unclear between GREEN/YELLOW — YELLOW preserves urgency for follow-up without false reassurance
2. Default to RED only with clear critical indicators: production impact (users affected), data loss (unrecoverable), or ongoing crisis (not yet mitigated)
3. Document reasoning in parenthetical: "Status: YELLOW (deployment successful but monitoring pending)" — transparency prevents misinterpretation

### Error: "Multi-Thread Update Contamination"
**Cause**: Input contains multiple unrelated topics that could cross-contaminate status classifications.

**Solution**:
1. Process each thread as separate proposition set (Phase 1 extraction per thread)
2. Apply template independently to each thread (Phase 2-3 per thread)
3. Combine with clear thread identification in final output (use headers: "Thread A: Deployment", "Thread B: Data Recovery")
4. Ensure status indicators are thread-specific (Thread A may be GREEN while Thread B is RED) — separate outcomes, separate classifications

---

## Error Handling Principles

**Constraint distribution in error handling**:
- **Summarizing before extracting** = loses facts. Complete Phase 1 fully before proceeding.
- **Status is "obvious"** = assumption. Apply classification criteria consistently, document reasoning.
- **Technical details not needed for non-technical audience** = false. Always include Technical Details; bridge jargon with explanation.
- **Action items are implied** = stakeholders cannot execute implied work. Write explicit (verb, scope, owner, timeline) for every next step.
- **Professional tone is "close enough"** = defensive language still embedded. Apply ALL transformation rules: hedging → direct, emotional → neutral, vague → specific.

---

## References

### Reference Files
- `${CLAUDE_SKILL_DIR}/references/templates.md`: Status-specific templates, section formats, phrase transformations
- `${CLAUDE_SKILL_DIR}/references/examples.md`: Complete transformation examples with proposition extraction
