---
name: repo-defining-workflows
description: Workflow pattern standards for creating multi-agent orchestrations including YAML frontmatter (name, description, tags, status, agents, parameters), execution phases (sequential/parallel/conditional), agent coordination patterns, and Gherkin success criteria. Essential for defining reusable, validated workflow processes.
---

# Defining Workflows

## Purpose

This Skill provides comprehensive guidance for **defining workflows** - multi-agent orchestrations that coordinate multiple agents in sequence, parallel, or conditionally to accomplish complex tasks. Workflows enable reusable, validated processes.

**When to use this Skill:**

- Creating new workflow documents
- Defining multi-agent coordination patterns
- Structuring sequential or parallel agent execution
- Writing workflow acceptance criteria
- Documenting workflow parameters and inputs

## Workflow Structure

### YAML Frontmatter (Required)

```yaml
---
name: workflow-name
description: Clear description of workflow purpose and outcomes
tags:
  - workflow-category
  - domain-area
status: active | draft | deprecated
agents:
  - agent-name-1
  - agent-name-2
parameters:
  - name: param-name
    type: string | number | boolean
    required: true | false
    default: value
    description: Parameter purpose
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Critical YAML Syntax**: Values containing colons (`:`) must be quoted.

✅ **Good**:

```yaml
description: "Workflow name: detailed description here"
parameter: "key: value pairs"
```

❌ **Bad** (breaks YAML parsing):

```yaml
description: Workflow name: detailed description
```

### Workflow Content

````markdown
# Workflow Name

## Purpose

What this workflow accomplishes and when to use it.

## Agents Involved

- **agent-name-1**: Role and responsibility
- **agent-name-2**: Role and responsibility

## Input Parameters

| Parameter | Type   | Required | Default | Description |
| --------- | ------ | -------- | ------- | ----------- |
| param1    | string | Yes      | -       | Purpose     |
| param2    | number | No       | 5       | Purpose     |

## Execution Phases

### Phase 1: Name (Sequential)

1. Run agent-name-1 with parameters
2. Wait for completion
3. Run agent-name-2 with results from agent-name-1

### Phase 2: Name (Parallel)

Run in parallel:

- agent-name-3
- agent-name-4

Wait for all to complete before proceeding.

### Phase 3: Name (Conditional)

If condition A:

- Run agent-name-5
  Else:
- Run agent-name-6

## Success Criteria

```gherkin
Given [precondition]
When [workflow executed]
Then [expected outcome]
And [additional verification]
```
````

## Example Usage

Concrete example showing how to invoke workflow.

## Related Workflows

- workflow-name-1 - When to use together
- workflow-name-2 - Alternative approach

````

## Execution Patterns

### Sequential Execution

**When**: Steps depend on previous results.

```markdown
1. maker creates content
2. checker validates content (uses maker output)
3. fixer applies fixes (uses checker findings)
````

### Parallel Execution

**When**: Steps are independent and can run simultaneously.

```markdown
Run in parallel:

- checker-1 validates docs
- checker-2 validates code
- checker-3 validates configs

Combine results after all complete.
```

### Conditional Execution

**When**: Different paths based on conditions.

```markdown
If validation passes:

- Deploy to production
  Else:
- Create issue with findings
- Notify team
```

### Mixed Patterns

Combine sequential, parallel, and conditional:

```markdown
1. Run maker (sequential)
2. Run checkers in parallel:
   - checker-1
   - checker-2
3. Wait for all checkers
4. Conditional:
   If critical issues found:
   - STOP
   - Report to user
     Else:
   - Run fixer (sequential)
   - Deploy
```

## Standard Input Parameters

Most workflows support:

- **max-concurrency** (number, default: 2): Maximum parallel agents
- **dry-run** (boolean, default: false): Preview without executing
- **verbose** (boolean, default: false): Detailed logging

## Common Mistakes

### ❌ Mistake 1: Unquoted colons in YAML

**Wrong**:

```yaml
description: Workflow name: detailed description
```

**Right**:

```yaml
description: "Workflow name: detailed description"
```

### ❌ Mistake 2: Missing agent dependencies

**Wrong**: Parallel execution when agent-2 needs agent-1 output
**Right**: Sequential execution with explicit dependency

### ❌ Mistake 3: No success criteria

**Wrong**: Workflow without Gherkin validation criteria
**Right**: Clear Gherkin scenarios for success validation

### ❌ Mistake 4: Missing parameters documentation

**Wrong**: Undocumented parameters that users must guess
**Right**: Table with all parameters, types, defaults, descriptions

## Workflow File Naming

**Convention**: `[workflow-name].md`

**Examples**:

- `quality-gate.md` - Plan quality gate workflow
- `quality-gate.md` - Docs quality gate workflow
- `repository-rules-validation.md` - Repo rules quality gate workflow

## Quality Checklist

Before publishing workflow:

- [ ] Valid YAML frontmatter (all colons quoted)
- [ ] name field matches filename
- [ ] description is clear and concise
- [ ] All agents listed in frontmatter
- [ ] All parameters documented (type, required, default)
- [ ] Execution phases clearly defined
- [ ] Dependencies explicit (sequential vs parallel)
- [ ] Success criteria in Gherkin format
- [ ] Example usage provided
- [ ] Related workflows linked

## References

**Primary Convention**: [Workflow Pattern Convention](../../../governance/workflows/meta/workflow-identifier.md)

**Related Conventions**:

- [Maker-Checker-Fixer Pattern](../../../governance/development/pattern/maker-checker-fixer.md) - Three-stage workflow pattern
- [Acceptance Criteria Convention](../../../governance/development/infra/acceptance-criteria.md) - Gherkin format

**Related Skills**:

- `wow__applying-maker-checker-fixer` - MCF workflow pattern
- `plan__writing-gherkin-criteria` - Success criteria format

---

This Skill packages workflow definition standards for creating reusable multi-agent orchestrations with clear coordination patterns. For comprehensive details, consult the primary convention document.
