---
name: composable-primitives
description: Design composable agentic primitives for flexible workflows. Use when creating reusable workflow building blocks, designing SDLC primitives, or building agent operations that can be combined in different ways.
allowed-tools: Read, Grep, Glob
---

# Composable Primitives Skill

Guide design of composable agentic primitives for flexible workflow creation.

## When to Use

- Designing new agentic workflows
- Customizing SDLC for specific needs
- Mapping problem classes to primitives
- Building organization-specific compositions

## The Secret

> "The secret of tactical agentic coding is that it's not about the software developer lifecycle at all. It's about composable agentic primitives you can use to solve any engineering problem class."

## Core Primitives

| Primitive | Purpose | Input | Output |
| --- | --- | --- | --- |
| **Classify** | Categorize input | Issue/task | Classification |
| **Plan** | Create implementation spec | Issue | Plan file |
| **Build** | Implement the plan | Plan file | Code changes |
| **Test** | Validate functionality | Code changes | Pass/fail |
| **Review** | Validate alignment | Spec + code | Issue list |
| **Patch** | Fix specific issues | Issue description | Targeted fix |
| **Document** | Generate documentation | Code changes | Doc files |
| **Ship** | Deploy to production | Validated code | Deployed state |
| **Branch** | Create isolated context | Classification | Branch name |
| **Commit** | Save checkpoint | Changes | Commit hash |

## Composition Workflow

### Step 1: Identify Problem Class

What type of work?

- Chore (simple, low risk)
- Bug (medium complexity, clear criteria)
- Feature (complex, full SDLC)
- Hotfix (urgent, minimal process)
- Documentation (content only)

### Step 2: Select Primitives

Based on problem class, choose primitives:

| Problem Class | Primitives |
| --- | --- |
| Chore | Classify -> Build -> Test -> Ship |
| Bug | Classify -> Plan -> Build -> Test -> Review -> Ship |
| Feature | Full SDLC |
| Hotfix | Patch -> Test -> Ship |
| Documentation | Document -> Review -> Ship |

### Step 3: Order by Dependencies

Ensure correct sequencing:

- Plan before Build (Build needs plan)
- Build before Test (Test needs code)
- Test before Ship (Ship needs validation)

### Step 4: Add Validation Points

Where should failures stop the pipeline?

```text
Plan -> Build -> [Test GATE] -> Review -> [Review GATE] -> Ship
```

### Step 5: Define Entry/Exit

- Entry: What triggers this workflow?
- Exit: What signals completion?

## Standard Compositions

### Full SDLC

```text
Classify -> Plan -> Build -> Test -> Review -> Document -> Ship
```

### ZTE (Zero-Touch)

```text
Classify -> Plan -> Build -> Test -> Review -> Document -> Ship
                              | |
                          [GATE]         [GATE]
```

### Quick Fix

```text
Classify -> Patch -> Test -> Ship
```

### Review-Driven

```text
Review -> Patch -> Test -> Ship
```

## Custom Composition Design

### Organization Factors

Consider:

- Testing requirements (mandatory E2E?)
- Review processes (who reviews?)
- Documentation standards (auto-generated?)
- Deployment pipelines (manual approval?)
- Compliance needs (audit trails?)

### Example: Compliance-Heavy

```text
Classify -> Plan -> [Compliance Review] -> Build -> Test ->
[Security Scan] -> Review -> Document -> [Approval] -> Ship
```

### Example: Rapid Iteration

```text
Build -> Test -> Ship (no planning for small changes)
```

## Key Memory References

- @composable-primitives.md - Detailed primitives documentation
- @template-engineering.md - Templates as primitive definitions
- @adw-anatomy.md - ADW as composition framework

## Output Format

Provide composition design:

```markdown
## Workflow Composition

**Problem Class:** {type}
**Entry Trigger:** {trigger}
**Exit Criteria:** {criteria}

### Primitives Selected
1. Classify - Categorize the task
2. Plan - Create implementation spec
3. Build - Implement changes
4. Test - Validate functionality
5. Ship - Deploy to production

### Composition Flow
```

Classify -> Plan -> Build -> Test -> Ship
                              |
                          [GATE: Must pass]

```markdown

### Validation Gates

- After Test: Abort if tests fail
- After Review: Optional based on confidence

### Customizations

- [Organization-specific additions]

```

## Anti-Patterns

- Rigid SDLC thinking (must do all steps)
- Over-composition (too many primitives)
- Under-composition (missing critical steps)
- Ignoring failure paths (no gates)
- One-size-fits-all (same for all problem classes)

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
