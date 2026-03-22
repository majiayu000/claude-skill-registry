---
name: managing-finances
description: Guides entrepreneurs through financial planning including pricing strategy selection and financial modeling
tools: Read, Write, Edit, Bash
model: inherit
---

# Managing Finances Skill

## Purpose

This skill helps entrepreneurs develop financial plans for their business, including pricing models, revenue projections, and cost analysis.

## When to Use

- When an entrepreneur needs to set pricing for their product or service
- When financial modeling or revenue planning is required
- When cost structure analysis is needed

## Workflow

### Phase 1: Financial Context Discovery

Gather business context: product/service type, target market, cost structure, and competitive landscape.

### Phase 2: Pricing Strategy

Guide the user through selecting and executing a pricing strategy.

This phase uses the pricing-strategy-framework reference to walk the user through three pricing approaches (cost-plus, value-based, competitive) and produce a documented pricing model.

For full details, see: [pricing-strategy-framework.md](references/pricing-strategy-framework.md) (Pricing Strategy Framework)

### Phase 3: Revenue Projection

Invoke the financial-modeler subagent to build revenue projections based on the selected pricing model and market assumptions:

```
Agent(subagent_type="financial-modeler",
      prompt="Generate revenue projections based on the pricing model and market assumptions gathered in Phases 1-2")
```

### Phase 4: Financial Summary

Compile all financial artifacts into a cohesive financial plan.

### Phase 5: Break-Even Analysis

Calculate break-even point in units and revenue, generate an ASCII chart visualization, and append results to the financial projections file.

This phase guides the user through providing fixed costs, variable cost per unit, and selling price per unit, then computes break-even metrics with full formula transparency.

For full details, see: [break-even-analysis.md](references/break-even-analysis.md) (Break-Even Analysis)

## Adaptive Pacing (EPIC-072 User Profile Integration)

This skill supports profile-based adaptation via EPIC-072 adaptive user profile integration. Before starting the workflow, read the user profile to determine the entrepreneur's experience level.

### Profile Read Mechanism

At the start of Phase 1, load the user profile from the project context:

```
Read(file_path="devforgeai/specs/business/user-profile.md")
```

Extract the `experience` field to determine adaptive pacing behavior.

### Experience-Based Pacing Levels

- **Beginner**: Provide detailed explanatory context for every financial concept. Use guided sub-questions to walk through inputs step by step. Explain terminology (e.g., "gross margin", "burn rate") inline. Include worked examples with each calculation.

- **Intermediate**: Provide standard explanations with moderate detail. Assume familiarity with basic financial terms. Offer optional deep-dives on complex topics.

- **Advanced**: Use concise, direct prompts without unnecessary explanation. Present results in streamlined tabular format. Skip introductory context and proceed to data collection immediately. Assume full fluency with financial modeling concepts.

### Missing Experience Field (EC-001)

When the experience field is missing from the user profile, default to intermediate pacing. This fallback to intermediate ensures a balanced experience without overwhelming or under-serving the user. Log this as a non-blocking note but do not halt the workflow.

## Graceful Degradation (Profile Unavailable - AC#4)

When the user profile is unavailable or the profile file does not exist, the skill applies graceful degradation with the following rules:

- **Default to intermediate** pacing for all interactions
- **Fallback behavior**: When the profile is absent, continue with intermediate defaults rather than blocking
- Issue a **non-blocking warning** that the profile was not found, without halting or blocking the workflow
- **Do not halt** on a missing profile. The skill must continue without the profile and never halt due to profile unavailability
- The **complete workflow must execute without error** even when the profile is absent or missing. The full financial projection workflow completes without requiring the profile

### Incomplete Projection Data (EC-002)

When incomplete or truncated projection data is encountered (e.g., the financial-modeler subagent returns partial results), the skill must surface a structured error message rather than presenting partial data as if it were complete. Never emit partial data without clearly labeling it as incomplete.

### Input Validation (EC-005)

All financial input values must be validated before use. Reject negative input values for revenue, cost, and pricing fields. When a zero or negative value is detected, reject it as invalid and use AskUserQuestion to prompt the user for a corrected value.

## Project-Anchored Mode (AC#5)

The skill operates in two modes depending on project context:

### Detecting Project Context

At startup, detect whether an active project context exists by checking for project configuration files. Identify the active project and its name from the project metadata.

### Project-Anchored Mode

When an active project is detected, the skill operates in project-anchored mode. In this mode:

- All projections are scoped to the active project specifically
- Scoping projections to the project ensures relevance and consistency
- All output files are labeled with the project name via a title or tag referencing the project name
- Financial artifacts are written to the project-specific directory

### Standalone Mode

When no project context is detected (or when explicitly requested), the skill operates in standalone mode. In standalone mode, projections are generic and unscoped, suitable for general financial exploration without project-specific assumptions.

### The --standalone Flag (EC-003)

The `--standalone` flag (standalone flag) allows the user to explicitly request standalone mode even when a project context exists. The --standalone flag takes precedence and overrides any auto-detected project context. This ensures the user always has control over the operating mode.

## References

| Reference | Path | When to Load |
|-----------|------|--------------|
| Pricing Strategy Framework | `references/pricing-strategy-framework.md` | Phase 2: Pricing strategy selection and calculation |
| Break-Even Analysis | `references/break-even-analysis.md` | Phase 5: Break-even calculation, chart, and projections output |

## Success Criteria

- [ ] Pricing strategy selected and documented
- [ ] Pricing model output written to `devforgeai/specs/business/financial/pricing-model.md`
- [ ] All outputs include "not financial advice" disclaimer
