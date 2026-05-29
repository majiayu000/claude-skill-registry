---
name: ghm-harvest
description: >
  Extracts durable insights from temp/ files to SoT during EPIC Phase E.
  Triggers at EPIC completion or explicit `/ghm-harvest` invocation.
  Outputs new SoT entries and archive manifest.
---

# Harvest

Extract durable insights from temporary files to Source of Truth during EPIC Phase E (Finish).

## Workflow Overview

1. **Enumerate Temps** → List all temp/ files from current EPIC
2. **Identify SoT-worthy** → Determine what should persist
3. **Format Entries** → Convert to proper SoT templates
4. **Archive** → Move temps to archive, update manifest

## Core Output Template

| Element | Definition | Evidence |
|---------|------------|----------|
| **Temp Files** | Files processed | List with paths |
| **New SoT Entries** | IDs created | BR-XXX, UJ-XXX, etc. |
| **Archive Manifest** | What was archived | Paths and dates |
| **Discarded** | What was not kept | Reason for each |

## Harvest Decision Matrix

| Content Type | Action | Destination |
|--------------|--------|-------------|
| Business rule discovered | Extract | `SoT/SoT.BUSINESS_RULES.md` |
| User flow documented | Extract | `SoT/SoT.USER_JOURNEYS.md` |
| API design finalized | Extract | `SoT/SoT.API_CONTRACTS.md` |
| Customer feedback captured | Extract | `SoT/SoT.CUSTOMER_FEEDBACK.md` |
| Session notes | Archive only | `archive/YYYY-MM/` |
| Scratch work | Discard | Delete after review |

## Step 1: Enumerate Temp Files

1. Read EPIC Section 3A for temp file references
2. List all files in `temp/` directory
3. Match temps to EPIC (by date or naming)

### Checklist
- [ ] All EPIC-referenced temps identified
- [ ] Temp directory scanned
- [ ] Files categorized by content type

## Step 2: Identify SoT-Worthy Content

For each temp file, evaluate:

| Question | If Yes | If No |
|----------|--------|-------|
| Is this a business rule? | Extract as BR-XXX | Continue |
| Is this a user flow? | Extract as UJ-XXX | Continue |
| Is this an API design? | Extract as API-XXX | Continue |
| Is this customer evidence? | Extract as CFD-XXX | Continue |
| Is this useful context? | Archive | Continue |
| Is this scratch work? | Discard | - |

### Checklist
- [ ] Each temp file evaluated
- [ ] Extract/Archive/Discard decision made
- [ ] Decisions documented

## Step 3: Format SoT Entries

For each extracted item:

1. Generate appropriate ID using `ghm-id-register`
2. Format per SoT template
3. Add cross-references
4. Insert into correct SoT file

### Entry Template

```markdown
### [ID]: [Title]

**Status**: Active
**Created**: YYYY-MM-DD
**Source**: temp/[filename].md (EPIC-XX)
**Cross-References**: [Related IDs]

[Extracted content, properly formatted]
```

### Checklist
- [ ] All extracts have valid IDs
- [ ] Formatting matches SoT templates
- [ ] Cross-references verified

## Step 4: Archive and Cleanup

1. Create archive directory: `archive/YYYY-MM/`
2. Move processed temps to archive
3. Generate manifest
4. Update EPIC Phase E checklist

### Archive Manifest Template

```markdown
## Archive Manifest: EPIC-XX

**Date**: YYYY-MM-DD
**Archived To**: archive/YYYY-MM/

### Extracted to SoT
| Temp File | New ID | SoT File |
|-----------|--------|----------|
| temp/file.md | BR-XXX | SoT.BUSINESS_RULES.md |

### Archived Only
| Temp File | Reason |
|-----------|--------|
| temp/notes.md | Session context |

### Discarded
| Temp File | Reason |
|-----------|--------|
| temp/scratch.md | No durable value |
```

## Quality Gates

### Pass Checklist
- [ ] All temps processed (none orphaned)
- [ ] Extracted content has valid IDs
- [ ] Archive manifest is complete
- [ ] EPIC Phase E checklist updated

### Testability Check
- [ ] SoT entries are findable by ID
- [ ] Archive manifest matches actual files
- [ ] Temp directory is clean

## Anti-Patterns

| Pattern | Example | Fix |
|---------|---------|-----|
| Orphan temps | Temps not in manifest | → Process all files |
| Lost context | Archive without manifest | → Always create manifest |
| Over-extraction | Everything becomes SoT | → Apply decision matrix |
| Under-extraction | Valuable insights lost | → Review before discard |

## Boundaries

**DO**:
- Extract durable insights
- Format per templates
- Create complete manifests
- Clean up temps

**DON'T**:
- Create new analysis
- Modify conclusions
- Skip the manifest
- Delete without review

## Handoff

After harvest completes:
- SoT files updated with new entries
- Temps archived with manifest
- EPIC Phase E marked complete
- Ready to close EPIC
