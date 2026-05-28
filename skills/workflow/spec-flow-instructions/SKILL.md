---
name: spec-flow-instructions
description: MUST use when working with spec files in `specs/` directories, or when commands reference this skill for conventions.
---

# Spec Flow Instructions Skill

A 5-step workflow for specification-driven development.

## Workflow

1. **initialize_spec** — Create spec from description with requirements and resource placeholders
2. **create_resource** — Analyze external resources, create detailed analysis files (repeatable)
3. **refine_spec** — Refine requirements, prompt user to resolve ambiguities, loop back if more resources needed
4. **create_tasks** — Generate concrete implementation tasks (code changes, tool calls, actions)
5. **execute_task** — Implement one task at a time (repeatable)

## File Structure

```
specs/<SPEC_SLUG>/
├── spec.md                    # Main specification file
└── resources/
    └── <resource-slug>.md     # Resource analysis files
```

## Templates

### Spec Template (spec.md)

```markdown
---
spec:
  title: "<Title Case>"
  slug: "<kebab-case>"
---

## Overview

<Brief description of what this specification accomplishes>

## Requirements

- (R-001) <Requirement description>

## Resources

<Resource entries will be added here as RS-XXX>

## Open Questions

<Questions identified during refine_spec that need user input>

## Tasks

<Tasks will be generated during create_tasks>
```

### Resource Template (for resources)

```markdown
---
resource:
  id: "RS-XXX"
  title: "<Resource Name>"
  source: "<URL or path>"
  spec_slug: "<SPEC_SLUG>"
  supports_requirements: [R-XXX]
---

# <Resource Name>

## Source

<URL or path to the resource>

## Summary

<2-3 sentences: what this resource is and why it matters for this spec>

## Key Insights

<Core concepts, patterns, and mental models relevant to spec requirements>

## Spec Alignment

<How this resource supports specific requirements, cite R-XXX IDs>

## Implementation Blueprint

<Practical entry points, code patterns, and setup requirements>

## Risks & Considerations

<Limitations, pitfalls, and alternatives to consider>
```

## ID Allocation

| Type         | Format | Example                |
| ------------ | ------ | ---------------------- |
| Requirements | R-XXX  | R-001, R-002, R-003    |
| Resources    | RS-XXX | RS-001, RS-002, RS-003 |
| Tasks        | T-XXX  | T-001, T-002, T-003    |

Rules:

- Sequential numbering starting from 001
- Never backfill gaps (if R-001, R-003 exist → next is R-004)
- Preserve existing IDs when updating, show traceability for merged items: `(R-002) [merged into R-003]`
- Mark obsolete requirements with `[obsolete]` tag, preserving their content: `(R-002) [obsolete] Original requirement text here`

## Slug Generation

Convert Title Case to kebab-case:

- "AI Agent Chat" → `ai-agent-chat`
- "React Native Gifted Chat" → `react-native-gifted-chat`

## Traceability

- Tasks reference requirements: "Addresses R-001 and R-002"
- Resources align with requirements: "Supports R-003"
- Every active requirement must map to at least one task

## Resource Entry Format

```markdown
- (RS-XXX) **<Name>** — Source: <url/path> — Analysis: `resources/<slug>.md` — Summary: <2-3 sentences>
```

## Resource Analysis

Use the **Resource Template** above. Section guidance:

- **Summary**: What this resource is and why it matters for this spec (2-3 sentences)
- **Key Insights**: Problem it solves, core abstractions, usage patterns, integration points
- **Spec Alignment**: How it supports requirements (cite R-XXX), relevant vs irrelevant parts, gaps filled or created
- **Implementation Blueprint**: Entry points (APIs, CLIs, SDKs), code patterns, proof-of-concept approach, dependencies
- **Risks & Considerations**: Limitations, performance concerns, maintenance considerations, alternatives

## Task Format

```markdown
### <Task Title> (T-XXX) [pending]

#### Overview

Addresses R-XXX by... [explanation and approach]

#### Acceptance Criteria

- [verifiable outcome]
- [demo-able result]

#### Implementation Details

- **Files to modify**: `path/to/file.ts`
- **Functions to change**: `functionName()`
- **Patterns to follow**: Similar to existing implementation
- **Integration**: Use specific hooks, context, APIs
- **Testing**: How to verify
```

Status tags: `[pending]`, `[in-progress]`, `[done]`, `[blocked <reason>]`

## Execution Summary Format

Append to task after execution:

```markdown
Execution Summary (T-XXX):
Files Changed (N):

- path/to/file.ts
  Acceptance Criteria:
- Criterion 1: PASS
- Criterion 2: PASS
  Tests: [results]
  Notes: [any observations]
```

## Definition of Done Patterns

### initialize_spec

- [ ] `specs/<slug>/` directory created
- [ ] `spec.md` created using the **Spec Template** above
- [ ] `resources/` subdirectory created
- [ ] Requirements derived from description
- [ ] Resource placeholders for mentioned URIs/paths only

### create_resource

- [ ] Analysis file at `specs/<slug>/resources/<resource-slug>.md`
- [ ] All analysis sections completed
- [ ] `supports_requirements` field populated in frontmatter
- [ ] Parent spec Resources section updated with summary
- [ ] Resource ID assigned (sequential, no backfill)

### refine_spec

- [ ] Spec and all resource analyses reviewed
- [ ] Problems and inconsistencies identified
- [ ] Ambiguities recorded in Open Questions section
- [ ] User prompted for each open question (use AskUserQuestion tool)
- [ ] Questions section updated with answers or cleared when resolved
- [ ] Overview refined for clarity
- [ ] Requirements refined to be concrete and testable

### create_tasks

- [ ] Codebase inspected for patterns and file structure
- [ ] Every requirement (R-XXX) covered by at least one task
- [ ] Tasks include specific file paths, function names, patterns
- [ ] Acceptance criteria are verifiable
- [ ] Task dependencies marked when present

### execute_task

- [ ] Task analyzed and current codebase understood
- [ ] Code changes implemented per task spec
- [ ] Follows existing code patterns
- [ ] All acceptance criteria verified
- [ ] Testing completed as specified
- [ ] No breaking changes to unrelated functionality
- [ ] Execution summary appended to task
