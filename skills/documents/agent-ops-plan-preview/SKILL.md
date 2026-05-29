---
name: agent-ops-plan-preview
description: "Transform implementation plans into concise stakeholder-friendly summaries with file change overviews, component listings, and optional flow diagrams."
license: MIT
compatibility: [opencode, claude, cursor]

metadata:
  category: core
  related: [agent-ops-planning]

---

# Plan Preview Workflow

## Purpose

Generate concise, stakeholder-ready summaries from detailed implementation plans. Enables developers, tech leads, and project owners to understand and approve planned changes without reviewing full technical details.

## Input Sources

Accept plan from one of:

| Source | Format | Example |
|--------|--------|---------|
| Issue ID | `{TYPE}-{NUMBER}@{HASH}` | `PLAN-0295@a1b2c3` |
| File path | Absolute or relative path | `.agent/issues/references/PLAN-0295@a1b2c3-plan.md` |
| Current context | Plan in conversation | (no argument needed) |

**Resolution order**:
1. If issue ID provided → resolve to `.agent/issues/references/{id}-plan.md`
2. If path provided → read directly
3. If neither → check if plan exists in current conversation context

## Procedure

### Step 1: Resolve Input

```
IF issue_id provided:
    path = .agent/issues/references/{issue_id}-plan.md
    IF NOT exists(path):
        ERROR "Plan file not found for issue {issue_id}"
ELSE IF file_path provided:
    path = file_path
ELSE:
    Scan conversation context for plan content
```

### Step 2: Language Selection

**Ask user** (one question):

> "What language should the summary be in? (default: English)"

Common choices:
- English (default)
- Norwegian (Norsk)
- Other (specify)

**Wait for response before proceeding.**

### Step 3: Confidence Level Selection

**Ask user** (one question):

> "What confidence level is this plan? This affects detail level in the summary:
> - **LOW** — More details, explicit changes, method signatures
> - **NORMAL** — Balanced overview (default)
> - **HIGH** — Sparse, broad outlines only"

**Wait for response before proceeding.**

### Step 4: Extract Plan Elements

Parse the implementation plan and extract elements **based on confidence level**:

#### Detail Level by Confidence

| Element | LOW Confidence | NORMAL Confidence | HIGH Confidence |
|---------|----------------|-------------------|-----------------|
| **Objective** | 2-3 sentences with context | 1-2 sentences | 1 sentence |
| **Approach** | 5-7 sentences, edge cases noted | 2-3 sentences | 1 sentence max |
| **Files** | Full paths + line estimates + change description | Paths + change type + brief purpose | Count only ("3 files modified") |
| **Components** | Name + signature + params + return type | Name + one-line purpose | Category counts ("2 endpoints, 1 validator") |
| **Dependencies** | Package names + versions + why needed | Package names | "New dependencies: Yes/No" |
| **Risks** | Detailed risk analysis with mitigations | Bullet list of risks | Omit unless critical |
| **Diagram** | Always if any flow exists | Only if branching logic | Never |

### Step 5: Flow Diagram Decision

**Confidence-aware diagram rules:**

| Confidence | Diagram Rule |
|------------|--------------|
| LOW | Include diagram if plan has ANY sequential flow |
| NORMAL | Include only if branching logic or state transitions |
| HIGH | Never include diagrams |

**Standard criteria (NORMAL confidence):**
- Plan has branching logic (if/else paths)
- Plan has multi-step sequences with dependencies
- Plan involves state transitions
- Plan has complex component interactions

### Step 6: Generate Summary

Structure varies by confidence level:

#### LOW Confidence Template

```markdown
# Plan Summary: {objective_short}

**Issue**: {issue_id}
**Generated**: {date}
**Language**: {language}
**Confidence**: LOW (detailed preview)

## Objective

{2-3 sentences with full context and background}

## Approach

{5-7 sentences explaining the implementation strategy}

**Edge Cases Considered:**
- {edge case 1}
- {edge case 2}

## Files Changed

| File | Change Type | Lines (est.) | Details |
|------|-------------|--------------|---------|
| `path/to/file.ts` | New | ~150 | {detailed description of what file contains} |
| `path/to/existing.ts` | Modify | +30/-10 | {specific changes being made} |

## New Components

### {Category}

| Name | Signature | Purpose |
|------|-----------|---------|
| `methodName` | `(param: Type) → ReturnType` | {detailed description} |

## Dependencies

| Package | Version | Reason |
|---------|---------|--------|
| `package-name` | ^1.2.3 | {why this dependency is needed} |

## Flow Overview

{Mermaid diagram - always included for LOW confidence}

## Risks & Considerations

| Risk | Impact | Mitigation |
|------|--------|------------|
| {risk description} | {HIGH/MEDIUM/LOW} | {how to address} |

---
*Detailed preview for LOW confidence plan — verify assumptions before implementation.*
```

#### NORMAL Confidence Template

(Use existing Step 5 template from original skill)

#### HIGH Confidence Template

```markdown
# Plan Summary: {objective_short}

**Issue**: {issue_id}
**Generated**: {date}
**Confidence**: HIGH (executive summary)

## Objective

{1 sentence}

## Approach

{1 sentence}

## Scope

- **Files**: {count} files ({new_count} new, {modify_count} modified)
- **Components**: {component_summary, e.g., "2 endpoints, 1 service, 3 tests"}
- **Dependencies**: {Yes/No new dependencies}

## Key Risks

{Only if critical risks exist, otherwise omit section}

---
*High-confidence plan — minimal review needed.*
```

### Step 7: Present & Offer Options

Display the generated summary, then ask:

> "Summary generated. What would you like to do?
> 
> 1. **Open in editor** — Opens as new file in VS Code
> 2. **Save to .agent/docs/** — Saves as `{issue_id}-preview.md`
> 3. **Done** — Keep in chat only"

## Output Templates by Language

### English (default)

Use templates from Step 6 based on confidence level.

### Norwegian (Norsk)

#### NORMAL Confidence (Norsk)

```markdown
# Plansammendrag: {objective_short}

**Sak**: {issue_id}
**Generert**: {date}
**Språk**: Norsk
**Konfidensnivå**: NORMAL

## Mål

{1-2 setninger om hovedmålet}

## Tilnærming

{2-3 setninger om hvordan planen oppnår målet}

## Endrede filer

| Fil | Endringstype | Formål |
|-----|--------------|--------|

## Nye komponenter

### {Kategori: Metoder/Endepunkter/Validatorer/Kommandoer}

| Navn | Formål |
|------|--------|

## Avhengigheter

## Flyt

## Risiko og vurderinger

---

*Dette sammendraget ble generert fra implementeringsplanen for interessentgjennomgang.*
```

#### HIGH Confidence (Norsk)

```markdown
# Plansammendrag: {objective_short}

**Sak**: {issue_id}
**Generert**: {date}
**Konfidensnivå**: HØY (sammendrag)

## Mål

{1 setning}

## Tilnærming

{1 setning}

## Omfang

- **Filer**: {antall} filer ({nye} nye, {endrede} endrede)
- **Komponenter**: {komponentsammendrag}
- **Avhengigheter**: {Ja/Nei nye avhengigheter}

---
*Høy-konfidensplan — minimal gjennomgang nødvendig.*
```

## Completion Criteria

- [ ] Plan source resolved (issue ID, path, or context)
- [ ] Language confirmed with user
- [ ] Confidence level confirmed with user
- [ ] Summary generated with appropriate detail level
- [ ] Mermaid diagram included according to confidence rules
- [ ] Output presented to user
- [ ] User chose action (editor/save/done)

## Anti-patterns (avoid)

- ❌ Generating output before asking for language preference
- ❌ Generating output before asking for confidence level
- ❌ Including Mermaid diagrams for HIGH confidence plans
- ❌ Providing sparse details for LOW confidence plans
- ❌ Copying implementation details verbatim (defeats purpose)
- ❌ Assuming English without asking
- ❌ Assuming NORMAL confidence without asking
- ❌ Saving file without user consent

## Examples

### Example 1: HIGH Confidence (Brief Overview)

**User**: "Preview plan for FEAT-0042@abc123"

**Agent**:
1. Resolves `.agent/issues/references/FEAT-0042@abc123-plan.md`
2. Asks: "What language?" → User: "English"
3. Asks: "What confidence level?" → User: "High"
4. Generates brief summary (no diagram):

```markdown
# Plan Summary: Add User Settings API

**Issue**: FEAT-0042@abc123
**Confidence**: HIGH (overview)

## Objective
Add CRUD endpoints for user settings.

## Approach
RESTful API with validation middleware.

## Scope
- **Files**: 4 files (2 new, 2 modified)
- **Components**: 1 service, 4 endpoints
- **Dependencies**: None new
```

### Example 2: NORMAL Confidence (Standard)

**User**: (plan in context) "Create preview in Norwegian"

**Agent**:
1. Detects plan in context
2. Language already specified: Norwegian
3. Asks: "What confidence level?" → User: "Normal"
4. Generates standard summary with optional diagram (if workflow has branches)

### Example 3: LOW Confidence (Detailed Review)

**User**: "Preview this complex migration plan, I need detailed review"

**Agent**:
1. Detects "detailed review" signals LOW confidence
2. Asks: "What language?" → User: "English"  
3. Confirms: "LOW confidence for detailed review. Correct?"
4. Generates comprehensive summary with detailed tables, diagrams, and risk matrix

### Example 4: Diagram Decision by Confidence

| Confidence | Plan Type | Diagram Decision |
|------------|-----------|------------------|
| HIGH | Any | ❌ Skip — keep brief |
| NORMAL | Simple CRUD | ❌ Skip — linear operations |
| NORMAL | Workflow with branches | ✅ Include — decision points |
| LOW | Any | ✅ Include — detailed review |
