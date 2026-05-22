---
name: doc-architect
description: Generate comprehensive documentation checklist for feature implementation
---

# Doc-Architect Skill

Analyzes feature requirements and generates a structured documentation checklist identifying all documentation impacts.

## Invocation

```
/doc-architect
```

## Inputs

From conversation context:
- Feature description or requirements
- Affected modules/components
- New functionality being added

## Outputs

A **Documentation Planning** section in markdown format:

```markdown
## Documentation Planning

### High-level design docs (docs/)
- `docs/workflows/feature-name.md` — create/update workflow documentation
- `docs/tutorial/XX-feature-name.md` — create/update tutorial

### Folder READMEs
- `path/to/module/README.md` — update purpose and organization

### Interface docs
- `src/module/component.md` — update interface documentation
```

## Analysis Steps

### 1. Identify Documentation Categories

Analyze the feature to determine which documentation types need updates:

**High-level design docs (docs/):**
- New workflows → `docs/workflows/*.md`
- Tutorials → `docs/tutorial/*.md`
- Architecture changes → `docs/architecture/*.md`

**Folder READMEs:**
- New directories → create `README.md`
- Module changes → update existing `README.md`

**Interface docs:**
- API changes → update endpoint documentation
- Component interfaces → add/update `.md` companion files
- Configuration → update config documentation

### 2. Generate Checklist

For each identified documentation impact:
- List the specific file path
- Indicate create vs. update action
- Provide brief rationale (1 line)

### 3. Output Format

Structure output as markdown section ready to paste into implementation plans:

```markdown
## Documentation Planning

### High-level design docs (docs/)
- `docs/path/to/doc.md` — create/update [brief description]

### Folder READMEs
- `path/to/README.md` — update [what aspect]

### Interface docs
- `src/module/interface.md` — update [which interfaces]
```

## Integration

This skill is invoked during planning workflows to ensure documentation impacts are identified early. The output is consumed by:

- `/ultra-planner` — includes checklist in consensus plan
- `/make-a-plan` — includes checklist in implementation plan
- `/issue-to-impl` Step 5 — uses checklist to update documentation

## Examples

**Feature: Add JWT authentication**

Output:
```markdown
## Documentation Planning

### High-level design docs (docs/)
- `docs/api/authentication.md` — create JWT auth API documentation
- `docs/tutorial/05-authentication.md` — create tutorial for auth setup

### Folder READMEs
- `src/auth/README.md` — create module overview and architecture

### Interface docs
- `src/middleware/auth.ts` — add interface documentation for auth middleware
```

**Feature: Refactor build system**

Output:
```markdown
## Documentation Planning

### High-level design docs (docs/)
- `docs/development/build.md` — update build system documentation with new structure

### Folder READMEs
- `build/README.md` — update build directory organization

### Interface docs
- N/A — internal refactor, no interface changes
```
