---
name: skill-chain-prompts
description: Orchestrate multi-skill workflows with prompt-based skill chaining. Define sequential or parallel skill invocations using YAML chain definitions, track progress through chains, and use pre-built chains for development, documentation, and career workflows. Use when coordinating multiple skills for complex tasks.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags: [orchestration, workflow, chaining, multi-skill, automation, meta]
---

# Skill Chain Prompts

Orchestrate complex workflows by chaining multiple skills together. Define sequences, track progress, and use pre-built chains for common development patterns.

## Concept

A **chain** is a sequence of skills that work together to accomplish a larger goal. Each step invokes a skill, passes context forward, and tracks completion. Chains work through Claude's sequential processing—no external engine required.

## Quick Reference

### Chain Format

```yaml
chain:
  name: "my-workflow"
  description: "What this chain accomplishes"

steps:
  - id: first
    skill: skill-name
    description: "What this step does"
    outputs: [artifact1, artifact2]

  - id: second
    skill: another-skill
    depends_on: [first]
    checkpoint: true  # Pause for review

  - id: third
    skill: final-skill
    depends_on: [second]
    optional: true  # Can be skipped
```

### Commands

| Command | Purpose |
|---------|---------|
| `/skill-chain-prompts run <chain>` | Execute a named chain |
| `/skill-chain-prompts list` | Show available chains |
| `/skill-chain-prompts status` | Display current progress |
| `/skill-chain-prompts resume` | Continue from checkpoint |
| `/skill-chain-prompts skip` | Skip current optional step |

## Pre-Built Chains

### Development Workflows

**api-development** — Full API from design to deployment
```
api-design-patterns → tdd-workflow → backend-implementation-patterns → verification-loop → deployment-cicd
```

**fullstack-feature** — Complete feature implementation
```
product-requirements-designer → api-design-patterns → backend-implementation-patterns → frontend-design-systems → testing-patterns → verification-loop
```

**mcp-development** — MCP server creation
```
mcp-builder → testing-patterns → verification-loop → mcp-server-orchestrator
```

### Professional Workflows

**career-preparation** — Job search readiness
```
cv-resume-builder → portfolio-presentation → interview-preparation → networking-outreach
```

**documentation** — Project documentation
```
doc-coauthoring → github-repository-standards → github-profile-architect
```

## Usage Examples

### Run a Pre-Built Chain

```
User: /skill-chain-prompts run api-development

Claude: Starting chain: api-development
        "Full API development from design to deployment"

        Step 1/5: design (api-design-patterns)
        Invoking /api-design-patterns...
```

### Check Progress

```
User: /skill-chain-prompts status

Claude: ## Chain Progress: api-development

        | Step | Skill | Status | Notes |
        |------|-------|--------|-------|
        | design | api-design-patterns | ● Done | OpenAPI spec created |
        | test-first | tdd-workflow | ◐ Active | Writing endpoint tests |
        | implement | backend-implementation-patterns | ○ Pending | |
        | verify | verification-loop | ○ Pending | |
        | deploy | deployment-cicd | ⊖ Optional | |

        **Progress**: 2/5 steps (40%)
        **Current**: test-first
```

### Create Custom Chain

```
User: I need a chain for building a CLI tool

Claude: Creating custom chain...

        chain:
          name: "cli-tool"
          description: "Build a CLI application"

        steps:
          - id: design
            skill: api-design-patterns
            description: "Design CLI interface and commands"

          - id: implement
            skill: backend-implementation-patterns
            depends_on: [design]

          - id: test
            skill: testing-patterns
            depends_on: [implement]

          - id: docs
            skill: doc-coauthoring
            depends_on: [implement]
            optional: true

        Ready to execute?
```

## State Tracking

Progress is tracked in the conversation using markdown tables:

```markdown
## Chain Progress: fullstack-feature

| Step | Skill | Status | Notes |
|------|-------|--------|-------|
| requirements | product-requirements-designer | ● Done | PRD complete |
| api | api-design-patterns | ● Done | 12 endpoints |
| backend | backend-implementation-patterns | ◐ Active | 8/12 endpoints |
| frontend | frontend-design-systems | ○ Pending | |
| testing | testing-patterns | ○ Pending | |
| verify | verification-loop | ○ Pending | |

**Progress**: 2.5/6 steps (42%)
**Checkpoint**: After verify
```

### Status Icons

| Icon | Meaning |
|------|---------|
| ○ | Pending |
| ◐ | In Progress |
| ● | Complete |
| ⊖ | Optional/Skipped |
| ✕ | Failed |

## Checkpoints

Checkpoints pause the chain for review:

```yaml
- id: verify
  skill: verification-loop
  depends_on: [implement]
  checkpoint: true  # Chain pauses here
```

At a checkpoint:
1. Chain pauses and shows summary
2. User reviews artifacts and progress
3. `/skill-chain-prompts resume` continues
4. Or user can modify, redo, or abort

## Best Practices

1. **Start with pre-built chains** — Customize as needed
2. **Use checkpoints** — Add after critical steps for review
3. **Mark optional steps** — Deployment, documentation often optional
4. **Keep chains focused** — 3-7 steps is ideal
5. **Pass context forward** — Reference outputs from prior steps

## References

- `references/chain-format.md` — Complete YAML specification
- `references/execution-model.md` — How chains are processed
- `references/state-tracking.md` — Progress visualization formats
- `references/built-in-chains.md` — All pre-built chains documented

## Chain Templates

Pre-built chain files in `assets/chains/`:
- `api-development.yaml`
- `fullstack-feature.yaml`
- `career-preparation.yaml`
- `mcp-development.yaml`
- `custom-chain.yaml` — Blank template
