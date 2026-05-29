---
name: competency-builder
description: Guide competency framework development and operation. Use when building training that produces capability, when existing training doesn't produce competence, when structuring knowledge for multiple audiences, or when setting up feedback loops to surface gaps.
license: MIT
metadata:
  author: jwynia
  version: "1.0"
---

# Competency Builder Skill

Build and operate competency frameworks that produce capability—not just completion. Diagnose where competency development is stuck and guide the next step.

## Core Principle

**Competencies are observable capabilities, not knowledge states. If you can't watch someone demonstrate it, it's not a competency.**

---

## Diagnostic States

### CF0: No Framework

**Symptoms:** Have training content but no competency structure. People complete training but can't apply it. Same questions keep getting asked.

**Test:**
- What decisions do people need to make with this knowledge?
- What mistakes indicate someone lacks competency?
- Can you describe what a competent person can DO?

**Intervention:** Start with failure modes. List mistakes you've seen, questions that shouldn't need asking, things that take too long. Each failure mode suggests a competency that would prevent it.

---

### CF1: Content-First Trap

**Symptoms:** Started by listing all the information people need to know. Training is comprehensive but competence is low. "We trained on that" but mistakes continue.

**Test:**
- Can you describe what someone with this competency can DO?
- What would you watch them do to verify competency?
- Does each content piece connect to a specific competency?

**Intervention:** Reframe each content chunk as "what decision/action does this enable?" Kill orphan content that doesn't support a competency. Work backward from actions to required knowledge.

---

### CF2: Vague Competencies

**Symptoms:** Competencies are knowledge states ("understands X") not capabilities ("can evaluate X against Y"). Can't tell if someone has the competency or not.

**Test:**
- Could two people disagree about whether someone has this competency?
- Can you observe it?
- Does it start with "Can" + action verb?

**Intervention:** Rewrite each competency as observable behavior. Transform:
- "Understands data policies" → "Can classify data according to policy categories"
- "Knows the approval process" → "Can determine required approval level for a given case"
- "Familiar with the tool" → "Can configure the tool to accomplish [specific task]"

---

### CF3: No Scenarios

**Symptoms:** Competencies defined but no way to test them. Assessment is knowledge recall (quizzes, multiple choice). People pass but fail in real situations.

**Test:**
- What realistic situation requires this competency?
- Does assessment require judgment, or can it be answered by searching documentation?
- What would a weak vs. strong response look like?

**Intervention:** For each core competency, create a scenario that:
1. Presents a realistic situation
2. Includes incomplete information
3. Requires judgment (not just recall)
4. Has better and worse responses (not binary right/wrong)

Create variants: interview (generic), assessment (org-specific), ongoing (real situations).

---

### CF4: Simple Scenarios

**Symptoms:** Scenarios exist but have artificial clarity. All information needed is provided. There's an obvious "right answer." People pass but fail in messy real situations.

**Test:**
- Do scenarios match the ambiguity of real situations?
- Can scenarios be answered by looking up documentation?
- Do scenarios require weighing trade-offs?

**Intervention:** Add ambiguity. Remove artificial clarity. Include information that might be relevant but isn't, and omit information that would make the answer obvious. Test with real people—if everyone gets the same answer immediately, it's too simple.

---

### CF5: Single Audience

**Symptoms:** Everyone gets the same training. Specialists are bored by basics. Generalists are overwhelmed by detail. One-size-fits-none.

**Test:**
- Who are your actual audiences?
- What depth does each audience need?
- Does a general employee need the same competencies as a specialist?

**Intervention:** Define audience layers (typically General / Practitioner / Specialist). Map competencies to audiences. Layer content by depth:
- L1: Rules without extensive justification (what to do)
- L2: Principles behind rules (how to handle edge cases)
- L3: Full technical detail (how to verify, audit, configure)

---

### CF6: No Progression

**Symptoms:** Competencies exist but no clear order. Prerequisites unclear. No skip logic. Everyone follows the same path regardless of prior knowledge.

**Test:**
- Which competencies require others as foundation?
- What's the minimum viable path for each role?
- Can someone with prior knowledge skip parts?

**Intervention:** Map dependencies. Build progression tree:
```
Foundation (everyone)
├── Prerequisite competencies
├─► Intermediate (builds on foundation)
└─► Role-specific branches (parallel tracks)
```

Define skip logic: what evidence allows skipping which modules?

---

### CF7: No Verification Stakes

**Symptoms:** Assessment exists but doesn't gate anything. People skip or game it. No consequence for demonstrating vs. not demonstrating competency.

**Test:**
- What decision does verification inform?
- What happens if someone fails assessment?
- Is there a real consequence for "not demonstrated"?

**Intervention:** Connect each verification to a decision:
- Hiring: Does candidate advance?
- Onboarding: Ready to work independently?
- Access: Qualified for elevated permissions?
- Promotion: Has developed required competency?

If verification doesn't connect to a decision, question whether it's worth doing.

---

### CF8: No Feedback Loop

**Symptoms:** Framework built once and never updated. Questions keep arising that weren't anticipated. No visibility into what's not working.

**Test:**
- How do you know what's not working?
- What mechanism surfaces gaps in training, framework, or process?
- When did this framework last change based on feedback?

**Intervention:** Implement feedback loop:
1. Agent/support system logs questions with context
2. Tag questions by competency/content area (or "unmapped")
3. Regular review for patterns
4. Route fixes to owners (training team, policy owners, tooling)
5. Track when patterns lead to changes

---

### CF9: Static Framework

**Symptoms:** Framework was built months/years ago. Reality has changed but framework hasn't. Questions reveal framework doesn't match current state.

**Test:**
- When was this last reviewed?
- What triggers an update?
- Who owns maintenance?

**Intervention:** Define:
- Review triggers (policy changes, incidents, new tools, feedback patterns)
- Ownership (who updates what)
- Version tracking (people trained on V1 vs. V2)
- Cadence (minimum review frequency even without triggers)

---

### CF10: Framework Operational

**Symptoms:** Competencies observable, scenarios tested, progression mapped, verification meaningful, feedback loop active, maintenance owned.

**Indicators:**
- Can answer all previous state questions affirmatively
- New hires reach competence faster
- Repeat questions decrease
- Framework has evolved based on feedback data
- Skip logic personalizes paths based on demonstrated competency

---

## Diagnostic Process

When someone presents a competency development need:

1. **Identify current state** — What exists? Training content? Competency list? Scenarios? Assessment?
2. **Apply state diagnosis** — Match symptoms to states above
3. **Ask clarifying questions** — What decisions do people make? What failures have you seen?
4. **Explain the diagnosis** — Name the state and what's missing
5. **Recommend next step** — Point to specific template or intervention
6. **Validate progress** — Check if intervention resolved the state

---

## Key Questions by Phase

### For Competency Identification
- What decisions do people need to make with this knowledge?
- What mistakes indicate someone lacks this competency?
- What would you watch someone do to verify competency?
- What's the failure mode this competency would prevent?

### For Scenario Design
- What realistic situation requires this judgment?
- What information would be incomplete or ambiguous?
- What would a weak response miss?
- What distinguishes competent from exceptional?

### For Audience Mapping
- Who needs full depth? Who needs rules only?
- Can the same content serve multiple audiences at different depths?
- What's minimum viable competency for each role?

### For Verification Design
- What decision does this verification inform?
- What evidence types are appropriate (scenario response, artifact, observed behavior)?
- What distinguishes "partial" from "competent" from "strong"?

### For Feedback Loops
- What questions do people ask after training?
- Which questions indicate training gaps vs. framework gaps vs. process gaps?
- Who receives the signal? Who decides on fixes?

---

## Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| **Document Dump** | Converting existing documentation into "training" without restructuring | Identify decisions documentation supports. Build backward from decisions to content. |
| **Quiz Fallacy** | Assessing competency with knowledge recall questions | Replace with scenarios requiring judgment. Can't answer by ctrl+F. |
| **Universal Training** | One training for all audiences | Layer content. Define minimum viable competency per role. |
| **Orphan Scenario** | Scenario doesn't map to any defined competency | Either add the competency it tests, or cut the scenario. |
| **Orphan Content** | Content doesn't support any competency | Either identify the competency it serves, or cut the content. |
| **Checkbox Completion** | "Completed training" without demonstrated competency | Tie completion to demonstrated competency, not time spent. |
| **Perfect on Paper** | Framework exists but isn't used; training continues as before | Pilot with real people. Get feedback. Iterate. |
| **Build-Once** | Framework created, never updated | Define triggers, owners, cadence for maintenance. |

---

## Templates

### Competency Definition Template

```markdown
## [Cluster Name] Competencies

| ID | Competency | Description |
|----|------------|-------------|
| [PREFIX]-1 | [Action verb phrase] | [Observable capability starting with "Can..."] |
```

### Scenario Template

```markdown
### Scenario: [Name]

**Core decision structure:** [What judgment is being tested]

**Interview variant:**
> [Generic situation]

**Assessment variant:**
> [Organization-specific situation]

**Competencies assessed:** [IDs]

**What good looks like:**
- [Consideration]

**Red flags:**
- [Weak response indicator]
```

### Progression Template

```
Foundation (Role: Everyone)
├── [COMP-1]: [Name]
└── [COMP-2]: [Name]

├─► Intermediate (Role: [Role])
│   ├── [COMP-3]: [Name] (requires: COMP-1)
│   └── [COMP-4]: [Name] (requires: COMP-2)

└─► Specialist (Role: [Role])
    └── [COMP-5]: [Name] (requires: COMP-3, COMP-4)
```

### Feedback Loop Template

```markdown
## Feedback Loop Design

**Observation mechanism:**
- How questions are logged
- What context is captured
- How they're tagged to competencies

**Analysis cadence:** [frequency]

**Pattern categories:**
- Training gap: [who handles]
- Framework gap: [who handles]
- Process gap: [who handles]
- Tooling gap: [who handles]

**Change tracking:**
- How changes are documented
- How effectiveness is measured
```

---

## Minimum Viable Framework

If starting small:

1. **3-5 core competencies** — the ones that matter most
2. **2-3 scenarios** — interview + assessment variants covering core competencies
3. **One layer of content** — probably L2 (practitioner depth)
4. **Basic rubric** — not demonstrated / partial / competent / strong
5. **One feedback signal** — what questions do people ask after training?

Expand based on what you learn from using it.

---

## Output Persistence

This skill writes primary output to files so work persists across sessions.

### Output Discovery

**Before doing any other work:**

1. Check for `context/output-config.md` in the project
2. If found, look for this skill's entry
3. If not found or no entry for this skill, **ask the user first**:
   - "Where should I save output from this competency-builder session?"
   - Suggest: `explorations/competency/` or a sensible location for this project
4. Store the user's preference:
   - In `context/output-config.md` if context network exists
   - In `.competency-builder-output.md` at project root otherwise

### Primary Output

For this skill, persist:
- **Diagnosed state** - which competency framework state applies
- **Competency definitions** - derived from failure modes
- **Scenario designs** - test scenarios for each competency
- **Framework structure** - progression model and dependencies
- **Feedback loop design** - how gaps will be identified

### Conversation vs. File

| Goes to File | Stays in Conversation |
|--------------|----------------------|
| State diagnosis | Clarifying questions |
| Competency definitions | Discussion of failure modes |
| Scenario templates | Iteration on structure |
| Framework architecture | Real-time feedback |

### File Naming

Pattern: `{domain}-competency-{date}.md`
Example: `ai-literacy-competency-2025-01-15.md`

## What This Skill Does NOT Do

- **Write training content** — You help structure, they write content
- **Prescribe specific competencies** — You help them discover theirs from failure modes
- **Assess whether existing training is "good"** — You diagnose what's missing
- **Replace subject matter expertise** — You provide methodology, they provide domain knowledge

---

## Health Check Questions

During competency framework development, ask:

1. Do all competencies describe observable capabilities (not knowledge states)?
2. Does each scenario require judgment that can't be looked up?
3. Is content layered appropriately for different audiences?
4. Does verification connect to real decisions?
5. Is there a mechanism to learn what's not working?
6. Has the framework changed based on feedback?
7. Can someone with prior knowledge skip parts?
8. Does everyone follow the same path, or is it personalized?

---

## Integration Points

| Skill | Connection |
|-------|------------|
| **research** | Use when building L3 content that requires domain expertise |
| **framework-development** | Related but distinct: frameworks capture knowledge; competency frameworks build capability |
| **framework-to-mastra** | Competency framework + feedback loop = deployable agent |

---

## Example Interaction

**User:** "We have a 40-page security policy. Everyone 'completes' the training but keeps making mistakes."

**Diagnosis:** CF1 (Content-First Trap)

**Questions to ask:**
- What are the 3 most common mistakes people make after "completing" training?
- What decisions do people make that require this knowledge?
- When someone makes a mistake, what did they fail to recognize or do?

**Guidance:**
"Each mistake suggests a competency gap. Let's work backward: if someone incorrectly handles sensitive data, the missing competency might be 'Can classify data according to organizational categories.' Once we have 3-5 competencies from failure modes, we'll design scenarios that test whether someone can actually apply the knowledge—not just recall it."

---

## Source Framework

Derived from: `frameworks/competency/competency-framework-development.md`
