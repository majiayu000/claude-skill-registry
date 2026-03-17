---
name: project-brainstorming
description: "Guide project ideation through Socratic questioning and constraint analysis for actionable project briefs. Use for starting projects, exploring problems, comparing approaches, feasibility. Skip if requirements are clear."
# Custom metadata (not used by Claude for matching):
model_preference: claude-sonnet-4
category: workflow
tags: [brainstorming, ideation, planning, requirements, socratic-method]
complexity: intermediate
estimated_tokens: 2800
---
## Table of Contents

- [When to Use](#when-to-use)
- [Integration](#integration)
- [Brainstorming Framework](#brainstorming-framework)
- [Phase 1: Problem Definition](#phase-1:-problem-definition)
- [Problem Statement](#problem-statement)
- [Phase 2: Constraint Discovery](#phase-2:-constraint-discovery)
- [Constraints](#constraints)
- [Technical](#technical)
- [Resources](#resources)
- [Integration](#integration)
- [Compliance](#compliance)
- [Success Criteria](#success-criteria)
- [Phase 3: Approach Generation](#phase-3:-approach-generation)
- [Approach [N]: [Name]](#approach-[n]:-[name])
- [Phase 3.5: War Room Deliberation (REQUIRED)](#phase-3.5:-war-room-deliberation-(required))
- [Phase 4: Approach Comparison](#phase-4:-approach-comparison)
- [Phase 5: Decision & Rationale](#phase-5:-decision-&-rationale)
- [Selected Approach: [Approach Name] ⭐](#selected-approach:-[approach-name]-⭐)
- [Rationale](#rationale)
- [Trade-offs Accepted](#trade-offs-accepted)
- [Rejected Approaches](#rejected-approaches)
- [Output: Project Brief](#output:-project-brief)
- [Problem Statement](#problem-statement)
- [Goals](#goals)
- [Constraints](#constraints)
- [Approach Comparison](#approach-comparison)
- [Selected Approach](#selected-approach)
- [Next Steps](#next-steps)
- [Questioning Patterns](#questioning-patterns)
- [Socratic Method](#socratic-method)
- [Constraint-Based Thinking](#constraint-based-thinking)
- [Red Flags to Surface](#red-flags-to-surface)
- [Session State Management](#session-state-management)
- [Related Skills](#related-skills)
- [Related Commands](#related-commands)
- [Examples](#examples)


# Project Brainstorming Skill

Guide project ideation through Socratic questioning, constraint analysis, and structured exploration.

## When To Use

- Starting a new project without clear requirements
- Exploring problem space before specification
- Need to compare multiple approaches systematically
- Validating project feasibility and scope
- Documenting decision rationale for stakeholders
- Need to clarify the core problem being solved

## When NOT To Use

- Requirements and specification already exist (use `Skill(attune:project-planning)` instead)
- Refining existing specs (use `Skill(attune:project-specification)` instead)
- Project scope is well-defined (jump to `/attune:project-init`)
- Mid-project pivots (use `Skill(attune:war-room)` for strategic decisions)

## Integration

**With superpowers**:
- Delegates to `Skill(superpowers:brainstorming)` for Socratic method
- Augments with project-specific patterns
- Uses project brainstorm templates

**Without superpowers**:
- Standalone questioning framework
- Project-focused ideation patterns
- Structured output templates

**War Room Integration (REQUIRED)**:
- After Phase 3 (Approach Generation), automatically invokes `Skill(attune:war-room)`
- All brainstorming context passed to War Room for expert deliberation
- War Room provides multi-LLM pressure testing and synthesis
- Only bypassed for Type 2 decisions (RS ≤ 0.40) with explicit user confirmation

## Brainstorming Framework

### Phase 1: Problem Definition

**Socratic Questions**:
1. What problem are you solving?
2. Who experiences this problem?
3. What makes this problem worth solving now?
4. What happens if this problem isn't solved?
5. What existing solutions have been tried?

**Output**: Problem statement in docs/project-brief.md

**Template**:
```markdown
## Problem Statement

**Who**: [Target users/stakeholders]
**What**: [The problem they face]
**Where**: [Context where problem occurs]
**When**: [Frequency/timing of problem]
**Why**: [Impact of the problem]
**Current State**: [Existing solutions and limitations]
```
**Verification:** Run the command with `--help` flag to verify availability.

### Phase 2: Constraint Discovery

**Questions**:
1. What are non-negotiable technical constraints?
2. What are resource constraints (time, budget, team)?
3. What integration points are required?
4. What compliance/regulatory requirements apply?
5. What are success criteria and failure modes?

**Output**: Constraints matrix

**Template**:
```markdown
## Constraints

### Technical
- [Constraint 1 with rationale]
- [Constraint 2 with rationale]

### Resources
- **Timeline**: [Duration with milestones]
- **Team**: [Size and skills]
- **Budget**: [If applicable]

### Integration
- [Required system 1]
- [Required system 2]

### Compliance
- [Requirement 1]
- [Requirement 2]

### Success Criteria
- [ ] [Measurable criterion 1]
- [ ] [Measurable criterion 2]
```
**Verification:** Run the command with `--help` flag to verify availability.

### Phase 3: Approach Generation

**Technique**: Generate 3-5 distinct approaches

**For each approach**:
- Clear description (1-2 sentences)
- Technology stack
- Pros (3-5 points)
- Cons (3-5 points)
- Risks (2-3 points)
- Estimated effort
- Trade-offs

**Template**:
```markdown
## Approach [N]: [Name]

**Description**: [Clear 1-2 sentence description]

**Stack**: [Technologies and tools]

**Pros**:
- [Advantage 1]
- [Advantage 2]
- [Advantage 3]

**Cons**:
- [Disadvantage 1]
- [Disadvantage 2]
- [Disadvantage 3]

**Risks**:
- [Risk 1 with likelihood]
- [Risk 2 with likelihood]

**Effort**: [S/M/L/XL or time estimate]

**Trade-offs**:
- [Trade-off 1 with mitigation]
- [Trade-off 2 with mitigation]
```
**Verification:** Run the command with `--help` flag to verify availability.

### Phase 3.5: War Room Deliberation (REQUIRED)

**Automatic Trigger**: After generating approaches, MUST invoke `Skill(attune:war-room)` for expert deliberation

**When War Room is invoked**:
- All brainstorming context (problem, constraints, approaches) automatically passed to War Room
- Expert panel reviews, challenges, and pressures each approach
- Reversibility assessment conducted
- Multi-LLM deliberation identifies blind spots
- Supreme Commander provides synthesis with rationale

**Command**:
```bash
# Automatically invoked from brainstorm - DO NOT SKIP
/attune:war-room --from-brainstorm
```

**War Room Output**:
- Reversibility Score (RS) and decision type
- Red Team challenges for each approach
- Premortem analysis on selected approach
- Supreme Commander Decision document
- Implementation orders and watch points

**Bypass Conditions** (ONLY skip war room if ALL true):
- [ ] RS ≤ 0.40 (Type 2 decision - clearly reversible)
- [ ] Single obvious approach with no meaningful trade-offs
- [ ] Low complexity with well-documented pattern
- [ ] User explicitly declines after being shown RS assessment

**Proceed to Phase 4 only after War Room completes**

### Phase 4: Approach Comparison

**Comparison Matrix**:

| Criterion | Approach 1 | Approach 2 | Approach 3 | Approach 4 |
|-----------|------------|------------|------------|------------|
| Technical Fit | 🟢 High | 🟡 Medium | 🟡 Medium | 🔴 Low |
| Resource Efficiency | 🟡 Medium | 🟢 High | 🔴 Low | 🟡 Medium |
| Time to Value | 🟢 Fast | 🟡 Medium | 🔴 Slow | 🟢 Fast |
| Risk Level | 🟡 Medium | 🟢 Low | 🔴 High | 🟡 Medium |
| Maintainability | 🟢 High | 🟡 Medium | 🟢 High | 🔴 Low |

**Scoring**: 🟢 = Good, 🟡 = Acceptable, 🔴 = Concern

### Phase 5: Decision & Rationale

**Selection Criteria**:
1. Alignment with constraints (must satisfy all)
2. Risk vs. reward balance
3. Team capability and experience
4. Time to value
5. Long-term maintainability

**Template**:
```markdown
## Selected Approach: [Approach Name] ⭐

### Rationale
[2-3 paragraphs explaining why this approach was selected]

Key decision factors:
- [Factor 1]
- [Factor 2]
- [Factor 3]

### Trade-offs Accepted
- **Trade-off 1**: [Description] → Mitigation: [Strategy]
- **Trade-off 2**: [Description] → Mitigation: [Strategy]

### Rejected Approaches
- **Approach X**: Rejected because [reason]
- **Approach Y**: Rejected because [reason]
```
**Verification:** Run the command with `--help` flag to verify availability.

## Output: Project Brief

Final output saved to `docs/project-brief.md`:

```markdown
# [Project Name] - Project Brief

**Date**: [YYYY-MM-DD]
**Author**: [Name]
**Status**: Draft | Approved

## Problem Statement
[From Phase 1]

## Goals
1. [Primary goal]
2. [Secondary goal]
3. [Tertiary goal]

## Constraints
[From Phase 2]

## Approach Comparison
[From Phase 3 & 4]

## War Room Decision
[From Phase 3.5 - includes RS assessment, Red Team challenges, premortem]

## Selected Approach
[From Phase 5, informed by War Room synthesis]

## Next Steps
1. `/attune:specify` - Create detailed specification
2. `/attune:blueprint` - Plan architecture and tasks
3. `/attune:project-init` - Initialize project structure
```
**Verification:** Run the command with `--help` flag to verify availability.

## Questioning Patterns

### Socratic Method

**Clarification**:
- "What do you mean by [term]?"
- "Can you give an example?"
- "What is the difference between X and Y?"

**Probing Assumptions**:
- "What are you assuming about [aspect]?"
- "Why do you think that assumption is valid?"
- "What if that assumption is wrong?"

**Probing Reasoning**:
- "Why do you think this approach is best?"
- "What evidence supports this?"
- "Are there alternative explanations?"

**Questioning Viewpoints**:
- "What would [stakeholder] think about this?"
- "What are the counterarguments?"
- "How might this fail?"

**Probing Implications**:
- "What happens if we choose this approach?"
- "What are the long-term consequences?"
- "What does this commit us to?"

### Constraint-Based Thinking

**Must Have** (Non-negotiable):
- What absolutely must be true for success?
- What constraints cannot be changed?

**Should Have** (Important):
- What would significantly increase success?
- What preferences matter most?

**Could Have** (Nice to have):
- What would be beneficial but not critical?
- What can we defer or drop if needed?

**Won't Have** (Explicit exclusions):
- What are we explicitly NOT doing?
- What scope boundaries prevent creep?

## Red Flags to Surface

During brainstorming, watch for:
- ⚠️ Vague problem statements ("make it better")
- ⚠️ Unclear success criteria
- ⚠️ Hidden assumptions about users or technology
- ⚠️ Single approach bias (not exploring alternatives)
- ⚠️ Scope creep in requirements
- ⚠️ Unrealistic constraints or timelines
- ⚠️ Missing stakeholder perspectives

## Session State Management

Save session to `.attune/brainstorm-session.json`:

```json
{
  "session_id": "20260102-143022",
  "started_at": "2026-01-02T14:30:22Z",
  "current_phase": "approach-selection",
  "problem": {
    "statement": "...",
    "stakeholders": ["..."]
  },
  "constraints": {
    "technical": ["..."],
    "resources": {"timeline": "...", "team": "..."}
  },
  "approaches": [
    {
      "name": "...",
      "pros": ["..."],
      "cons": ["..."]
    }
  ],
  "selected_approach": null,
  "decisions": {}
}
```
**Verification:** Run the command with `--help` flag to verify availability.

## Related Skills

- `Skill(superpowers:brainstorming)` - Socratic method (if available)
- `Skill(attune:war-room)` - **REQUIRED AUTOMATIC INTEGRATION** - Invoked after Phase 3 for multi-LLM deliberation
- `Skill(imbue:scope-guard)` - Scope creep prevention
- `Skill(attune:project-specification)` - Next phase after brainstorming

## Related Commands

- `/attune:brainstorm` - Invoke this skill
- `/attune:specify` - Next step in workflow
- `/imbue:feature-review` - Worthiness assessment

## Examples

See `/attune:brainstorm` command documentation for complete examples.
## Troubleshooting

### Common Issues

**Command not found**
Ensure all dependencies are installed and in PATH

**Permission errors**
Check file permissions and run with appropriate privileges

**Unexpected behavior**
Enable verbose logging with `--verbose` flag
