---
name: ghm-sot-builder
description: >
  Creates new Source of Truth (SoT) files when existing templates don't fit your needs.
  Triggers on requests to create a new SoT file, add a new artifact type, or when user says
  "I need to track [X] but there's no SoT for it", "create SoT", "new source of truth".
  Outputs a properly structured SoT.*.md file with ID prefix, frontmatter, and update protocol.
---

# SoT Builder

Create new Source of Truth files that fit your product's unique needs while maintaining template purity.

## When to Use This Skill

This skill is for **rare occasions** (3-4 times per product lifecycle) when:
- You fork this repo and the existing SoT files don't cover your artifact types
- Your product needs to track a concept that doesn't fit existing ID prefixes
- You need to consolidate scattered documentation into a canonical SoT

**Do NOT use** when:
- An existing SoT file covers your need (just add entries there)
- You want to track temporary/session-specific data (use `temp/` instead)
- The artifact type is already covered by `ghm-id-register`

## Workflow Overview

1. **Identify Need** → Confirm no existing SoT fits
2. **Design Schema** → Define ID prefix, categories, required fields
3. **Draft Template** → Create pure structure (no methodology teaching)
4. **Validate Purity** → Apply the litmus test
5. **Register & Integrate** → Update SoT.README.md and ID system

## Core Output Template

See `assets/sot-template.md` for the copy-paste starter template.

| Element | Definition | Required |
|---------|------------|----------|
| **YAML Frontmatter** | version, purpose, id_prefix, authority | Yes |
| **Purpose Block** | Single paragraph explaining what this tracks | Yes |
| **Navigation Section** | Category links for quick access | Yes |
| **Entry Template** | Repeatable structure for each ID | Yes |
| **Cross-Reference Index** | Bidirectional links to other SoT files | Yes |
| **Update Protocol** | When/how to add new entries | Yes |

## Step 1: Identify the Need

Before creating a new SoT, verify:

### Checklist
- [ ] Searched existing SoT files for similar artifact types
- [ ] Confirmed the concept is **durable** (survives multiple sessions)
- [ ] Confirmed the concept needs **unique IDs** for cross-referencing
- [ ] Confirmed this isn't better served by a subsection in an existing SoT

### Questions to Answer

1. **What artifact type does this track?**
   - Bad: "Notes" (too generic)
   - Good: "Partner Integration Contracts" (specific, durable)

2. **Why can't existing SoT files handle this?**
   - Valid: "We need different fields than API contracts for partner integrations"
   - Invalid: "I just want a separate file" (preference, not need)

3. **What ID prefix will you use?**
   - Must be unique across the system
   - 2-4 uppercase letters
   - Check `SoT/SoT.UNIQUE_ID_SYSTEM.md` for existing prefixes

## Step 2: Design the Schema

Define the structure before writing:

### ID Prefix Selection

```
Format: [PREFIX]-[XXX]
Examples: PIC-001, INT-042, MIG-003
```

**Rules**:
- 2-4 uppercase letters
- Descriptive but short
- Unique across all SoT files
- Check existing prefixes in `SoT/SoT.UNIQUE_ID_SYSTEM.md`

### Category Ranges

Reserve ID ranges for logical groupings:

```markdown
**Category A** (XXX-001 to XXX-099):
**Category B** (XXX-101 to XXX-199):
**Category C** (XXX-201 to XXX-299):
```

### Required Fields per Entry

Define the minimum fields every entry needs:

| Field | Purpose | Example |
|-------|---------|---------|
| **ID** | Unique identifier | `PIC-001` |
| **Title** | Human-readable name | "Stripe Payment Integration" |
| **Status** | Current state | Active / Deprecated / Planned |
| **Created** | Origin date | 2025-01-10 |
| **Last Updated** | Last modification | 2025-01-15 |
| **Related IDs** | Cross-references | BR-101, API-045 |

### Optional Fields

Add domain-specific fields as needed, but keep them structural (not methodology):

- Good: "Partner Contact" (data field)
- Bad: "Best Practices for Partner Selection" (methodology teaching)

## Step 3: Draft the Template

Use `assets/sot-template.md` as your starting point.

### Structure Sections

1. **YAML Frontmatter** - Metadata for the file
2. **Title & Purpose Block** - What this SoT tracks
3. **Navigation by Category** - Quick links to entries
4. **Entry Template** - Repeatable structure (copy for each new entry)
5. **Deprecated Section** - Where old entries go
6. **Cross-Reference Index** - Bidirectional links
7. **Update Protocol** - When/how to maintain

### Template Purity Rules

**KEEP in the template** (self-documentation):
- When to add new entries
- Required fields checklist
- Cross-reference integrity checks
- File-specific maintenance procedures

**MOVE to skill references** (methodology teaching):
- "Best practices" for this domain
- "What makes a good entry"
- Example workflows beyond format
- Evaluation criteria

### Litmus Test

For each section, ask:

> "Is this teaching me how to maintain the FILE STRUCTURE, or teaching me DOMAIN KNOWLEDGE about what makes good content?"

- File structure maintenance → Keep in template
- Domain knowledge → Move to skill references

## Step 4: Validate Purity

Before finalizing, run this checklist:

### Purity Checklist
- [ ] No "how to analyze" or "how to evaluate" content
- [ ] No "best practices" or "key learnings" sections
- [ ] No cross-file workflows (multi-file coordination)
- [ ] No "what makes a good entry" evaluation criteria
- [ ] Examples show FORMAT only, not instructional CONTENT
- [ ] Self-documentation is under 20% of total file size

### Self-Documentation Checklist
- [ ] Has "Update Protocol" section
- [ ] Documents when to add new IDs
- [ ] Includes cross-reference integrity checks
- [ ] Specifies required fields for new entries
- [ ] Self-documentation is file-specific (not generic)

### Context Efficiency Checklist
- [ ] Template can be read without loading other files
- [ ] Methodology examples are in skill references, not template
- [ ] General governance references SoT.README.md

## Step 5: Register and Integrate

After creating the SoT file:

### Update SoT.README.md

Add entry to the structure table:

```markdown
| `SoT.{YOUR_FILE}.md` | {PREFIX}-### | {Purpose description} |
```

### Update SoT.UNIQUE_ID_SYSTEM.md

Add new prefix to Section 1.2 Standard Prefixes:

```markdown
| **{PREFIX}** | {Meaning} | `SoT.{YOUR_FILE}.md` |
```

### Create Index Tables

Add empty index table in Part 2 of SoT.UNIQUE_ID_SYSTEM.md:

```markdown
#### {Your Type} ({PREFIX}-XXX)

| ID | Title | Status | Used By |
|----|-------|--------|---------|
| {PREFIX}-001 | {Title} | Active | {IDs} |
```

## Quality Gates

### Pass Checklist
- [ ] ID prefix is unique across all SoT files
- [ ] Template follows purity standard
- [ ] Update protocol included
- [ ] Cross-reference index structure defined
- [ ] SoT.README.md updated
- [ ] SoT.UNIQUE_ID_SYSTEM.md updated

### Testability Check
- [ ] Can create a new entry using only the template instructions
- [ ] Cross-references can be validated programmatically
- [ ] Entries can be found by ID search

## Anti-Patterns

| Pattern | Example | Fix |
|---------|---------|-----|
| Methodology in template | "Best practices for partner selection" | Move to skill references |
| Duplicate prefix | Using BR- for a new file | Choose unique prefix |
| Too generic | "Notes.md" | Be specific: "Partner_Integrations.md" |
| No update protocol | Template with no maintenance section | Add "Update Protocol" section |
| Orphan SoT | Not registered in SoT.README.md | Always register new files |

## Bundled Resources

- **`references/sot-patterns.md`** — Common patterns across existing SoT files
- **`references/examples.md`** — Before/after examples of SoT creation
- **`assets/sot-template.md`** — Copy-paste starter template

## Handoff

After creating a new SoT:
1. SoT file exists at `SoT/SoT.{NAME}.md`
2. SoT.README.md lists the new file
3. SoT.UNIQUE_ID_SYSTEM.md has the new prefix
4. Ready to use `ghm-id-register` for adding entries
