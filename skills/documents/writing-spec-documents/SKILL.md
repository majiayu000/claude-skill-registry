---
name: writing-spec-documents
description: Use when creating implementation specification documents - ALWAYS required in Phase 2 regardless of bridge weight, prescribes exactly what to build with traceability to whiteboard decisions
---

# Writing Spec Documents

Create implementation specification documents that prescribe exactly what to build. The spec is a living document that evolves during sequencing and implementation.

**Announce at start:** "I'm using the writing-spec-documents skill to create the implementation spec."

## When to Use

**ALWAYS use this skill in Phase 2.** Spec documents are required regardless of bridge weight.

| Bridge Weight | Design Doc | Spec Doc | This Skill |
|---------------|------------|----------|------------|
| Heavy | Required | Required | **Required** |
| Medium | Optional | Required | **Required** |
| Light | Skip | Required | **Required** |
| Thin | Skip | Required | **Required** |

**Key difference from design doc:**
- Design doc = WHY (rationale, exploration, stable)
- Spec doc = HOW (prescription, living, evolves)

## Inputs

| Bridge Weight | Required Inputs |
|---------------|-----------------|
| Heavy/Medium | PRD, Whiteboard, Design Doc |
| Light/Thin | PRD, Whiteboard |

Before starting, ensure you have:

1. **PRD with FRs** — requirements document with block-anchored FRs
2. **Phase 2 Whiteboard** — decisions with `^decision-N` anchors
3. **Design Doc** (Heavy/Medium only) — formal design rationale

## Traceability Model

Spec references whiteboard decisions. When spec changes, add new decision to whiteboard FIRST.

```text
Whiteboard (append-only)        Spec (living)
├── ^decision-D1 ──────────►   <satisfies>D1</satisfies>
├── ^decision-D2 ──────────►   <component references="D2">
└── ^decision-D3 ──────────►   <changes references="D3">
```

**Rule:** Every significant spec element should trace to a whiteboard decision or PRD FR/NFR.

## Spec Document Structure

Save to: `{{feature-dir}}/{{feature-name}}-spec.md`

The spec uses XML format in a codeblock for structured, machine-parseable content.

```markdown
# {{Feature Name}} — Specification

**Feature**: {{feature name}}
**Phase**: 2 (Design)
**Status**: Draft

> **Context:**
> - [PRD]({{feature-name}}-prd.md)
> - [Phase 2 Whiteboard](2-design-phase/phase2-design-whiteboard.md)
> - [Design Doc]({{feature-name}}-design.md) _(if Heavy/Medium bridge)_

---

\`\`\`xml
<project_specification>
  <project_name>{{Feature Name}}</project_name>

  <overview>
    {{Brief description of what's being built}}
  </overview>

  <components>
    {{See Component Template below}}
  </components>

  <data_schemas>
    {{See Data Schema Template below}}
  </data_schemas>

  <integration>
    {{See Integration Template below}}
  </integration>

  <acceptance_criteria>
    {{See AC Template below}}
  </acceptance_criteria>

  <risks>
    {{See Risk Template below}}
  </risks>
</project_specification>
\`\`\`
```

## Component Template

```xml
<component name="{{component-name}}" port_type="{{type}}">
  <source>{{source file path if porting}}</source>
  <target>{{target file path}}</target>
  <lines>{{estimated lines}}</lines>
  <language>{{language}}</language>
  <changes>
    - {{Change 1}}
    - {{Change 2}}
  </changes>
  <satisfies>{{FR1, FR2, D1}}</satisfies>
</component>
```

**Port types:**
- `new` — New file, not in source
- `copy_modify` — Copy from source with path/config changes only
- `rewrite` — Significant structural rewrite (language change, tool change)
- `translation` — Language translation, same logic

## Data Schema Template

```xml
<schema name="{{schema-name}}">
  <format>{{JSON, YAML, JSONL, etc.}}</format>
  <location>{{file path}}</location>
  <fields>
    - {{field1}}: {{type and description}}
    - {{field2}}: {{type and description}}
  </fields>
</schema>
```

## Integration Template

```xml
<integration>
  <hook_registration>
    <file>{{config file path}}</file>
    <additions>
      {{What's being added to the config}}
    </additions>
  </hook_registration>

  <directory_structure>
    <path>{{base path}}</path>
    <contents>
      - {{file/dir 1}} — {{purpose}}
      - {{file/dir 2}} — {{purpose}}
    </contents>
  </directory_structure>

  <path_mapping>
    <entry>
      <source>{{source path}}</source>
      <target>{{target path}}</target>
    </entry>
  </path_mapping>
</integration>
```

## Acceptance Criteria Template

```xml
<acceptance_criteria>
  <section name="{{Section Name}}" fr="{{FR1}}">
    - AC1: {{Testable acceptance criterion}}
    - AC2: {{Testable acceptance criterion}}
  </section>
</acceptance_criteria>
```

**Traceability:** Each AC section traces to an FR. Individual ACs inherit that traceability.

## Risk Template

```xml
<risks>
  <risk severity="{{High|Medium|Low}}">
    <description>{{What could go wrong}}</description>
    <mitigation>{{How to prevent or handle it}}</mitigation>
  </risk>
</risks>
```

## Bridge-Specific Content

### Heavy Bridge (Greenfield, Integration, API)

Full spec with all sections:
- Detailed component specs with behavior descriptions
- Complete data schemas
- Interface contracts
- All integration points
- Comprehensive ACs

### Medium Bridge (Brownfield, Migration)

Moderate spec:
- Component specs focused on changes
- Schemas for new/modified data
- Integration changes only
- ACs for new functionality

### Light Bridge (Port, Refactor)

Focused spec:
- Components with port_type and source/target mapping
- Path mappings (source → target)
- Minimal schemas (only if format changes)
- ACs focused on parity validation

### Thin Bridge (Bug Fix, Deprecation)

Minimal spec:
- Affected components only
- Change description
- Verification criteria

## Spec Evolution

The spec is a **living document**. It changes during:

1. **Sequencing (Phase 3)** — ACs refined, risks reassessed
2. **Implementation (Phase 4)** — Details adjusted based on reality

**When changing the spec:**

1. Add new decision to whiteboard with rationale: `^decision-DN`
2. Update spec component/section with reference: `<satisfies>DN</satisfies>`
3. Commit both files together

**Never:** Change spec without whiteboard decision anchor.

## Output Location

| Artifact | Location |
|----------|----------|
| Spec Document | `{{feature-dir}}/{{feature-name}}-spec.md` |

## Validation Checklist

After writing spec, verify:

1. [ ] Every component has `<satisfies>` tracing to FR or decision
2. [ ] All port_types are correct (new, copy_modify, rewrite, translation)
3. [ ] Path mappings are complete (source → target)
4. [ ] ACs trace to FRs
5. [ ] Risks have mitigations
6. [ ] Run `citation-manager validate <spec-path>`

## Common Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|----------------|-----|
| Spec without decision traceability | Can't understand why changes were made | Add `<satisfies>` to every component |
| Changing spec without whiteboard update | Breaks traceability, loses rationale | Add decision to whiteboard first |
| Over-specifying for Light bridge | Wastes effort on unnecessary detail | Match spec depth to bridge weight |
| Under-specifying for Heavy bridge | Insufficient guidance for implementation | Include all sections for Heavy bridge |
| Hardcoded paths in spec | Breaks portability | Use variables like `$PROJECT` |

## Red Flags

- Components without `<satisfies>` traceability
- Spec changes with no corresponding whiteboard decision
- Heavy bridge with minimal spec content
- Light bridge with excessive spec content
- Missing path mappings for ports
- ACs that don't trace to FRs

## Integration with Other Skills

**Inputs from:**
- `writing-requirements-documents` — PRD with FRs
- `writing-design-documents` — Design doc (Heavy/Medium bridge)
- Phase 2 whiteboard — Decision anchors

**Outputs to:**
- Sequencing phase — Spec informs work decomposition
- `writing-plans` — Spec feeds implementation planning

**Referenced by:**
- `enforcing-development-workflow` — Phase 2 REQUIRED skill (all bridge weights)

---

**Remember:** The spec prescribes exactly what to build. It's a living document that evolves, but every change must trace back to a whiteboard decision. Spec depth should match bridge weight — don't over-engineer for ports, don't under-specify for greenfield.
