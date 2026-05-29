# Epic Scoping Skill

Interactive question bank-driven scoping for epic workflows.

## Purpose

Systematically scope epics with structured AskUserQuestion calls, eliminating ambiguity before planning. Uses centralized question bank to ensure consistent, comprehensive scoping.

## When to Invoke

- Always for new epics (via `/epic` command)
- Skip if resuming with `/epic continue`

## Quick Start

```bash
# Load question bank
cat .claude/skills/epic/references/question-bank.md
```

## 5-Round Interactive Scoping

### Round 1: Initial Scoping (2 questions)

**Questions from bank**:
- `initial_scoping.business_goal`
- `initial_scoping.subsystem_selection`

```javascript
AskUserQuestion({
  questions: [
    questionBank.initial_scoping.business_goal,
    questionBank.initial_scoping.subsystem_selection,
  ],
});
```

**Apply answers to epic-spec.md**:
- business_goal → `## Objective` > `### Business Value`
- subsystem_selection → `## Subsystems` (update **Involved** field)

### Round 2: Scope Refinement (0-4 questions, conditional)

**Based on subsystem_selection**, ask relevant follow-ups:

```javascript
const refinementQuestions = [];

if (selectedSubsystems.includes("Backend API")) {
  refinementQuestions.push(questionBank.scope_refinement.backend_scope);
}
if (selectedSubsystems.includes("Frontend UI")) {
  refinementQuestions.push(questionBank.scope_refinement.frontend_scope);
}
if (selectedSubsystems.includes("Database")) {
  refinementQuestions.push(questionBank.scope_refinement.database_scope);
}
if (selectedSubsystems.includes("External integrations")) {
  refinementQuestions.push(questionBank.scope_refinement.integration_scope);
}

if (refinementQuestions.length > 0) {
  AskUserQuestion({ questions: refinementQuestions });
}
```

**Apply answers**:
- backend_scope → `### Backend` section
- frontend_scope → `### Frontend` section
- database_scope → `### Database` section
- integration_scope → `### Infrastructure` section

### Round 3: Success Metrics (2 questions)

```javascript
AskUserQuestion({
  questions: [
    questionBank.success_metrics.measurement_approach,
    questionBank.success_metrics.target_values,
  ],
});

// If "Specific targets" selected, follow-up:
if (answers["Targets"] === "Specific targets") {
  const customTargets = answers["Targets_custom"];
  // Parse and apply to epic-spec.md
}
```

**Apply answers**:
- measurement_approach → `### Success Metrics` section
- target_values → `### Success Metrics` (actual values)

### Round 4: Dependencies & Constraints (2 questions)

```javascript
AskUserQuestion({
  questions: [
    questionBank.dependencies_and_constraints.external_dependencies,
    questionBank.dependencies_and_constraints.constraints,
  ],
});
```

**Apply answers**:
- external_dependencies → `## Dependencies` section
- constraints → `### Constraints` section

### Round 5: Complexity Assessment (2 questions)

```javascript
AskUserQuestion({
  questions: [
    questionBank.complexity_assessment.technical_complexity,
    questionBank.complexity_assessment.sprint_estimate,
  ],
});

// Warn if 7+ sprints
if (answers["Sprint Estimate"] === "7+ sprints") {
  console.log("Warning: Consider breaking into smaller epics");
}
```

**Apply answers**:
- technical_complexity → YAML frontmatter `complexity` field
- sprint_estimate → `## Overview` section

## Progress Indicators

Show progress after each round:

```
🔍 Epic Scoping: Round 1/5 (Initial scoping)
📝 Applied: Business Goal → New capability
📝 Applied: Subsystems → Backend API, Frontend UI, Database
🔍 Epic Scoping: Round 2/5 (Scope refinement)
...
```

## Completion Summary

After 5 rounds:

```
✅ Epic Scoping Complete (9 questions answered)

📊 Epic Summary:
  Business Goal: New capability
  Subsystems: Backend API, Frontend UI, Database (3)
  Success Metrics: User adoption (target: 80% within 30 days)
  Dependencies: Third-party APIs (Stripe)
  Constraints: Time constraint (2-week deadline)
  Complexity: Medium
  Estimated Sprints: 3-4 sprints

📋 Next Steps:
  1. Review epic-spec.md for accuracy
  2. Run /plan to generate research → plan → sprint breakdown
  3. Run /epic continue to execute automated workflow
```

## Velocity Benefit

- **With skill**: 5-10 minute interactive scoping
- **Without skill**: 30+ minute unstructured discussion
- **Improvement**: 3-6x faster

## Question Bank Reference

Location: `.claude/skills/epic/references/question-bank.md`

Contains:
- Initial scoping (2 questions)
- Scope refinement (0-4 conditional)
- Success metrics (2 questions)
- Dependencies & constraints (2 questions)
- Complexity assessment (2 questions)

**Total**: 8-9 questions across 5 rounds
