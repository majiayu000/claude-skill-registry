---
skill: document-feature
description: Generate technical and user documentation for a feature
location: project
---

# Document Feature: $ARGUMENTS

Generate comprehensive documentation for a feature in both developer and user-friendly formats.

## Process

### Phase 1: Feature Analysis

1. **Identify feature type**: Frontend, Backend, or Full-stack
2. **Gather technical context**: Files, types, dependencies, data flow
3. **Analyze user interaction**: UI elements, step-by-step journey

Search in: `/components/`, `/app/`, `/lib/`, `/types/`, `/contexts/`

### Phase 2: Developer Documentation

Create: `docs/dev/$ARGUMENTS-implementation.md`

**Required sections:**
1. Overview and quick reference
2. Architecture (component structure, data flow, types)
3. Implementation details (core logic, state, events)
4. Code examples (basic and advanced)
5. Testing (coverage, manual checklist)
6. Integration guide (config, dependencies)
7. API reference (if applicable)
8. Maintenance (known issues, future work)

### Phase 3: User Documentation

Create: `docs/user/how-to-$ARGUMENTS.md`

**Required sections:**
1. Overview (what it does, benefits)
2. Getting started (prerequisites, access)
3. Step-by-step instructions with screenshot placeholders
4. Common use cases/scenarios
5. Tips and best practices (do's, don'ts, pro tips)
6. Troubleshooting (common problems + solutions)
7. FAQ
8. Related features

### Phase 4: Screenshot List

Create: `docs/screenshots/$ARGUMENTS-screenshots-needed.txt`

List all screenshots needed with:
- Filename
- What to show
- What to highlight

### Phase 5: Cross-References

- Update main documentation index
- Add links to related docs
- Update CLAUDE.md if new patterns introduced

## Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Dev docs | `[feature]-implementation.md` | `dark-mode-implementation.md` |
| User docs | `how-to-[feature].md` | `how-to-dark-mode.md` |
| Screenshots | `[feature]-[context].png` | `dark-mode-toggle.png` |

## Quality Standards

**Developer docs**: Technically accurate, includes file paths and line numbers, proper terminology

**User docs**: Non-technical language, visual aids, clear actionable steps, scannable formatting

## Output Checklist

- [ ] Dev doc at correct path with all sections
- [ ] User doc at correct path with all sections
- [ ] Screenshot placeholder list generated
- [ ] Code examples syntactically correct
- [ ] Cross-references added
- [ ] Technical accuracy verified against code
