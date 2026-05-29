---
name: mini-spec
description: use **whenever designing, updating, or implementing the design, code, or docs** or **whenever reverse engineering a design from code**
---

# Mini-spec

3-level architecture: specs → design → code.

```
specs/    # Human specs (language, environment required)
design/   # SOURCE OF TRUTH: crc-*, seq-*, ui-*, test-*, manifest-ui.md
docs/     # user-manual.md, developer-guide.md
src/      # Code with traceability comments
```

## Core Principles
- SOLID principles, comprehensive unit tests
- Code and specs as MINIMAL as possible

## Traceability

`design.md` Artifacts section: design files with code file checkboxes.

**Code changes:** Uncheck `[x]`→`[ ]`, ask user: "Update design, specs, or defer?"
**Update design:** Read code, update design file, re-check box.

## Gap Analysis

`design.md` Gaps section tracks: Spec→Design, Design→Code, Code→Design, Oversights.

## Workflow

**Read specs first.** Specs must indicate language/environment.

### Phase Separation
- **"Design"** = design only, no code
- **"Implement"** = code only, update Artifacts checkboxes
- **"Code changes"** = uncheck Artifacts, ask user

### Design Phase
Create in `design/`:
- `design.md`: Intent + Artifacts (design files → code file checkboxes)
- `crc-*`: CRC cards (see format below)
- `seq-*`: sequence diagrams (≤150 chars wide)
- `ui-*`: ASCII layouts, reference CRC cards
- `test-*`: test designs (see format below)
- `manifest-ui.md`: routes, theme, global components

### Implementation Phase
Add traceability comments:
```
// CRC: crc-Store.md | Seq: seq-crud.md
add(data): Item {
```
Mark implemented: `[ ]`→`[x]` in Artifacts.

### Documentation Phase
Create `docs/user-manual.md` and `docs/developer-guide.md` with traceability links.

## CRC Card Format
```markdown
# ClassName
**Source Spec:** feature.md
## Knows
- attribute: description
## Does
- behavior: description
## Collaborators
- OtherClass: why
## Sequences
- seq-scenario.md
```
Principles: Single Responsibility, minimal collaborations, PascalCase.

## Test Case Format
```markdown
# Test Design: ComponentName
**Source:** crc-ComponentName.md
## Test: name
**Purpose:** what this validates
**Input:** setup and data
**Expected:** verifiable outcome
**Refs:** crc-*.md, seq-*.md
```
Cover: happy path, errors, edge cases.

## Quality Checklist
- [ ] CRC Cards: nouns/verbs covered, no god classes, Source Spec linked
- [ ] Sequences: participants from CRCs, ≤150 chars wide
- [ ] UI Specs: ASCII layouts, refs to CRCs and manifest-ui.md
- [ ] Traceability: design files in Artifacts, code files have checkboxes
- [ ] Tests: test-*.md for key behaviors
