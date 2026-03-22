---
name: assessing-entrepreneur
description: "Use when a solo developer or aspiring entrepreneur needs a cognitive work-style assessment to personalize business coaching. Guides users through a 6-dimension self-assessment questionnaire and generates a structured profile."
---

# Assessing Entrepreneur

Guide users through a self-assessment questionnaire covering 6 cognitive work-style dimensions to adapt business coaching to their individual preferences.

---

## EXECUTION MODEL: This Skill Expands Inline

After invocation, YOU (Claude) execute these instructions phase by phase.

---

## Purpose

This skill collects self-reported preferences from solo developers and aspiring entrepreneurs across 6 dimensions of cognitive work style. The resulting profile helps calibrate business plans, task granularity, and coaching style.

**Important: This skill NEVER diagnoses any mental health conditions. It does not provide clinical assessment. All questions capture self-reported preferences and behavioral patterns only. This is not a diagnosis tool.**

---

## When to Use

- User wants to understand their work style for business planning
- Before creating a personalized business plan
- When adapting coaching approach to individual preferences
- When a user self-reports challenges with focus, motivation, or task completion

---

## Generated Artifacts

- **User profile**: Structured self-reported preferences across 6 dimensions
- **Calibration data**: Input for plan-calibration-engine.md

---

## Assessment Dimensions

The questionnaire covers 6 self-reported dimensions:

1. **Work Style** - How the user prefers to structure their work
2. **Task Completion** - Patterns in how the user finishes tasks
3. **Motivation** - What drives and sustains the user's effort
4. **Energy Management** - How the user manages energy and focus throughout the day
5. **Previous Attempts** - Past entrepreneurial or project attempts and lessons learned
6. **Self-Reported Challenges** - Areas where the user feels they struggle most

---

## Workflow Phases

### Phase 1: Disclaimer and Consent

**Purpose:** Ensure the user understands this is a self-reported preferences questionnaire.

Display the following disclaimer:

> **Important: This is a self-reported work-style preferences questionnaire.**
> It does not diagnose any condition. The questions collect your personal
> preferences and behavioral patterns to help tailor business coaching.
> Your responses are used only to personalize your experience.

Use AskUserQuestion to confirm consent:

```
AskUserQuestion(
  question="Do you understand that this is a self-reported preferences questionnaire and wish to proceed?",
  header="Consent",
  options=["Yes, I understand and want to proceed", "No, I have questions first"]
)
```

If user declines, answer questions before proceeding. Never proceed without consent.

---

### Phase 2: Work Style Preferences

**Purpose:** Understand how the user prefers to organize and approach work.

Ask the primary Work Style question and follow up as needed. For all questions and detailed instructions, see: [work-style-questionnaire.md](references/work-style-questionnaire.md)

---

### Phase 3: Task Completion Patterns

**Purpose:** Understand how the user approaches finishing tasks and projects.

For all Task Completion questions, see: [work-style-questionnaire.md](references/work-style-questionnaire.md)

---

### Phase 4: Motivation Drivers

**Purpose:** Identify what drives and sustains the user's effort.

For all Motivation questions, see: [work-style-questionnaire.md](references/work-style-questionnaire.md)

---

### Phase 5: Energy Management

**Purpose:** Understand how the user manages energy and focus.

For all Energy Management questions, see: [work-style-questionnaire.md](references/work-style-questionnaire.md)

---

### Phase 6: Previous Attempts

**Purpose:** Learn from the user's past entrepreneurial or project experiences.

For all Previous Attempts questions, see: [work-style-questionnaire.md](references/work-style-questionnaire.md)

---

### Phase 7: Self-Reported Challenges

**Purpose:** Identify areas where the user feels they struggle most.

For all Self-Reported Challenges questions, see: [work-style-questionnaire.md](references/work-style-questionnaire.md)

---

### Phase 8: Profile Generation

**Purpose:** Normalize responses into a structured profile using the entrepreneur-assessor subagent.

Invoke the entrepreneur-assessor subagent:

```
Task(
  subagent_type="entrepreneur-assessor",
  description="Normalize assessment responses into structured user profile",
  prompt="Process the following self-reported assessment responses and generate a structured user-profile. Responses: [collected responses from Phases 2-7]. Dimensions: Work Style, Task Completion, Motivation, Energy Management, Previous Attempts, Self-Reported Challenges."
)
```

The subagent produces a structured profile covering all 6 dimensions.

For adaptation strategies based on profile results, see:
- [adhd-adaptation-framework.md](references/adhd-adaptation-framework.md) - Neurodivergent-friendly adaptations
- [confidence-assessment-workflow.md](references/confidence-assessment-workflow.md) - Confidence calibration
- [plan-calibration-engine.md](references/plan-calibration-engine.md) - Plan complexity adjustment

---

### Profile Synthesis Output

**Purpose:** Document the 7-dimension adaptive profile written to `devforgeai/specs/business/user-profile.yaml`.

The profile synthesis maps assessment responses to 7 calibration dimensions:

| Dimension | Range | Notes |
|-----------|-------|-------|
| task_chunk_size | 5-60 min per task | micro / standard / extended |
| session_length | 15-60 min per session | short / medium / long |
| check_in_frequency | every 1-5 tasks | frequent / moderate / minimal |
| progress_visualization | per-task to weekly | per_task / daily / weekly |
| celebration_intensity | every-completion to milestone-only | high / medium / low |
| reminder_style | specific-next-action to gentle-nudge | specific / balanced / gentle |
| overwhelm_prevention | next-3-tasks-only to full-roadmap | strict / moderate / open |

**Output schema** written to `devforgeai/specs/business/user-profile.yaml`:

```yaml
schema_version: "1.0"
created: "YYYY-MM-DD"
last_calibrated: "YYYY-MM-DD"

adaptive_profile:
  task_chunk_size: micro        # micro | standard | extended
  session_length: short         # short | medium | long
  check_in_frequency: frequent  # frequent | moderate | minimal
  progress_visualization: per_task  # per_task | daily | weekly
  celebration_intensity: high   # high | medium | low
  reminder_style: specific      # specific | balanced | gentle
  overwhelm_prevention: strict  # strict | moderate | open
```

---

### Phase 9: Results Summary

**Purpose:** Present the assessment results to the user.

Display a summary covering:

1. **Work Style Profile** - Summary of self-reported preferences across all 6 dimensions
2. **Recommended Adaptations** - Coaching style adjustments based on self-reported preferences
3. **Plan Calibration** - Suggested task granularity, timeline expectations, and support level
4. **Next Steps** - How this profile will be used in business planning

**Note: All results reflect self-reported preferences only. This summary does not diagnose or imply any condition.**

---

## Reference Files

Load on demand for detailed workflows:

| Reference | Purpose | When to Load |
|-----------|---------|--------------|
| [adhd-adaptation-framework.md](references/adhd-adaptation-framework.md) | Neurodivergent-friendly coaching adaptations | Phase 8-9, when profile suggests focus challenges |
| [confidence-assessment-workflow.md](references/confidence-assessment-workflow.md) | Confidence and imposter syndrome patterns | Phase 8-9, when self-reported challenges include confidence |
| [work-style-questionnaire.md](references/work-style-questionnaire.md) | Detailed question sets for all 6 dimensions | Phases 2-7, for follow-up questions |
| [plan-calibration-engine.md](references/plan-calibration-engine.md) | Calibrate plan complexity from profile | Phase 8-9, when generating recommendations |

---

## Integration

**Invoked by:** Business coaching workflows, `/ideate` command (optional)
**Produces:** Structured user profile for plan calibration
**Consumed by:** Plan calibration engine, coaching adaptation workflows

---

## Success Criteria

- [ ] User consented to self-reported preferences questionnaire
- [ ] All 6 dimensions assessed via AskUserQuestion
- [ ] Responses normalized into structured profile via entrepreneur-assessor subagent
- [ ] Results presented with appropriate context (self-reported, not clinical)
- [ ] No affirmative use of clinical or diagnostic language
