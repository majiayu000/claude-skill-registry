---
name: compile
description: Compile a course module into the Andamio import format for publishing.
license: MIT
compatibility: Designed for Andamio platform import format. Adapt output format for other learning platforms.
metadata:
  author: Andamio
  version: 1.0.0
---

# Skill: Compile Module for Import

## Description

Takes a completed course module and packages it into the clean directory structure required by Andamio's module import system. Creates a `compiled/` directory with `outline.md`, numbered lesson files, and optional `introduction.md` and `assignment.md`.

## Import Format Quick Reference

```
module-folder/
├── outline.md          # Required
├── introduction.md     # Optional
├── assignment.md       # Optional
├── lesson-1.md         # Optional (maps to SLT 1)
├── lesson-2.md         # Optional (maps to SLT 2)
└── ...
```

**outline.md critical requirements:**
| Element | Format | Notes |
|---------|--------|-------|
| Title (YAML) | `title:` in frontmatter | Module display name |
| Code | YAML `code:` | Unique module identifier — can be a number (`101`) or slug (`intro-cardano`) |
| SLT heading | `## SLTs` | Must be exactly this (H2, case-insensitive) — first element after frontmatter |
| SLT list | Numbered or bulleted | Each item becomes one SLT |

**Common mistakes:**
- Adding `# Title` heading in outline.md → not needed, title comes from YAML frontmatter
- Using `# Student Learning Targets` instead of `## SLTs` → parser ignores SLTs

**Upsert behavior:** If `code` matches an existing module, content will be updated.

## Instructions

### 1. Select Course and Module

First, list courses in `courses-in-progress/`:

```markdown
## Available Courses

| # | Course | Modules |
|---|--------|---------|
| 1 | andamio-for-contributors | 4 |
| 2 | andamio-for-api-developers | 4 |

Which course? (number or slug)
```

After course selection, list modules:

```markdown
## Modules in [Course Name]

| # | Module | SLTs | Lessons Written |
|---|--------|------|-----------------|
| 1 | Your On-Chain Identity | 3 | 3/3 |
| 2 | Browsing Courses and Projects | 3 | 3/3 |
| 3 | Earning a Credential | 2 | 2/2 |
| 4 | The Contribution Loop | 4 | 1/4 |

Which module to compile? (number)
```

Warn if lessons are incomplete:
- If `lessons/module-N/` doesn't have files for all SLTs, show warning
- Ask if user wants to continue anyway (partial compile)

### 2. Parse Source Materials

From `00-course.md`, extract for the selected module:
- Module title (e.g., "Your On-Chain Identity")
- Module number (1, 2, 3...)
- All SLTs for that module (the "I can..." statements)
- Assignment section content

From `lessons/module-N/`:
- All lesson markdown files (e.g., `1.1-compare-access-token.md`)
- Map by SLT index (first number before hyphen)

### 3. Generate Module Code

Create a unique `code` for the module. This can be a numeric code or a slug string:

**Numeric convention** (when course uses numbered modules):
- Module 1 of course → `101`
- Module 2 of course → `102`
- Module 3 of course → `103`
- Intermediate course modules → `201`, `202`, `203`

**Slug convention** (when course uses descriptive identifiers):
- `intro-cardano`
- `wallet-setup`
- `first-transaction`

The code must be unique within the course. If it matches an existing module, the import will upsert (update) rather than create.

### 4. Create Output Directory

Create `compiled/[course-slug]/[module-code]/`:

```
compiled/
  andamio-for-contributors/
    101/
      outline.md
      lesson-1.md
      lesson-2.md
      lesson-3.md
      assignment.md
```

### 5. Generate outline.md

```markdown
---
title: [Module Title]
code: [module-code]
---

## SLTs

1. [First SLT text, exactly as it appears on-chain]
2. [Second SLT text, exactly as it appears on-chain]
3. [Third SLT text, exactly as it appears on-chain]
```

**Critical format requirements:**
- **No H1 heading** in outline.md — the module title comes from YAML `title:` field only
- SLT heading **must** be exactly `## SLTs` (H2 level, case-insensitive) — first element after frontmatter
- Common mistake: Adding `# Title` after frontmatter or using `# Student Learning Targets`
- SLT list can be numbered (1.) or bulleted (-, *)
- Each list item becomes one SLT

**SLT text formatting:**
- Preserve the SLT text exactly as written — do NOT strip "I can" or other prefixes
- The importer uses the text as-is for the learning target
- Number them 1, 2, 3... matching lesson file numbers

### 6. Generate lesson-N.md Files

For each SLT, copy the corresponding lesson file:
- `1.1-compare-access-token.md` → `lesson-1.md`
- `1.2-connect-wallet.md` → `lesson-2.md`
- `1.3-mint-access-token.md` → `lesson-3.md`

**Lesson file transformations:**
- Remove frontmatter-style header (SLT, Type lines at top, `---` divider)
- **Add an `# H1` title** — this becomes the lesson title in the import system. Use a short, descriptive title (e.g., `# Connect a Cardano Wallet`, `# Mint Your Access Token`)
- Keep all lesson content below the H1 title

### 7. Generate assignment.md

Extract assignment content from `00-course.md`:

```markdown
# Module Assignment

## Task

[Description of what the learner will do]

## Deliverables

1. [First deliverable]
2. [Second deliverable]
3. [Third deliverable]
```

**Assignment transformations:**
- Convert "Artifact:" to the Task section
- Convert "Assessment criteria:" bullets to numbered Deliverables
- Optionally add a Notes section for on-chain cost, timing, common mistakes

### 8. Generate introduction.md (Optional)

Module introduction shown before lessons. Great for context, prerequisites, or learning objectives.

If the module section in `00-course.md` has introductory text, extract it:

```markdown
# Welcome to [Module Topic]

[Module-level introduction - context, what learners will accomplish]

## Prerequisites

- [Prerequisite 1]
- [Prerequisite 2]
```

If there's no intro text in the source, skip this file.

### 9. Validation

Before writing files, validate:
- [ ] All SLTs have corresponding lesson files
- [ ] Lesson files aren't empty
- [ ] Assignment content exists in `00-course.md`
- [ ] Module code is unique (no collision with existing compiled modules)

Report any issues:

```markdown
## Validation

- [x] 3 SLTs found in module
- [x] 3 lesson files found
- [x] Assignment content found
- [ ] Missing: lesson-2.md (SLT 1.2)

Fix missing lessons before compiling, or proceed with partial?
```

### 10. Write and Confirm

Write all files to `compiled/[course-slug]/[module-code]/`.

Show summary:

```markdown
## Compiled: Module [N] - [Title]

**Output:** `compiled/[course-slug]/[module-code]/`

### Files Created

| File | Size | Status |
|------|------|--------|
| outline.md | 245 bytes | Created |
| lesson-1.md | 3.2 KB | Created |
| lesson-2.md | 2.8 KB | Created |
| lesson-3.md | 4.1 KB | Created |
| assignment.md | 890 bytes | Created |

### Ready for Import

This module is ready to upload to Andamio Studio.

**Next steps:**
1. Review files in `compiled/[course-slug]/[module-code]/`
2. Upload folder via Studio import
3. Verify SLTs and content in preview
```

## Image Handling

Images in lessons are automatically processed during import. Place them correctly and they'll be uploaded to cloud storage with local paths replaced by hosted URLs.

### Folder Structure

Place images in an `assets/` subdirectory within your module folder:

```
compiled/
  andamio-for-contributors/
    101/
      outline.md
      lesson-1.md
      lesson-2.md
      assignment.md
      assets/
        diagram-1.png
        screenshot-wallet.png
        screenshots/
          step-by-step.png
```

### Referencing Images in Markdown

Use relative paths from the markdown file:

```markdown
![Wallet Setup](assets/screenshot-wallet.png)

![Diagram](./assets/diagram-1.png)

![Step by Step](assets/screenshots/step-by-step.png)
```

All three path formats work:
- `assets/image.png`
- `./assets/image.png`
- Just `image.png` (matched by filename as fallback)

### Supported Formats

`.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.svg`

### What Happens on Import

1. Images are automatically uploaded to cloud storage
2. Local paths are replaced with hosted URLs
3. Default size is Medium (600px)
4. Use S/M/L toggle in editor to resize (300/600/900px)

### Best Practices

- Use lowercase filenames without spaces: `wallet-setup.png` not `Wallet Setup.png`
- Keep filenames unique across subdirectories
- Organize by type: `assets/diagrams/`, `assets/screenshots/`
- Name screenshots to match lesson flow: `1.1-connect-wallet-01.png`, `1.1-connect-wallet-02.png`

## Lesson File Cleaning Rules

When copying lesson content, apply these transformations:

1. **Top metadata block** — strip the SLT/Type/divider metadata:
```markdown
# Lesson X.Y: Title        ← STRIP this specific format

**SLT:** I can...           ← STRIP
**Type:** Product Demo      ← STRIP
---                         ← STRIP
```

2. **Add an `# H1` title** — this becomes the lesson title in the app:
```markdown
# Connect a Cardano Wallet  ← ADD a short, descriptive title

## Before You Start          ← Lesson content starts here
...
```
The H1 title should be descriptive but concise (not "Lesson 1.2: Connect a Cardano Wallet", just "Connect a Cardano Wallet").

3. **Key Terms sections:** Keep (useful for learners)

4. **What's Next sections:** Remove or keep based on context
   - Remove if it references "the next lesson" specifically
   - Keep if it references other courses or resources

5. **"Want to know how this works?" links:** Keep (cross-course references are good)

## Error Handling

**Missing lesson file:**
```
Warning: No lesson file found for SLT 1.2
- Expected: lessons/module-1/1.2-*.md
- Action: Creating empty lesson-2.md placeholder
```

**Missing assignment:**
```
Warning: No assignment found for Module 1
- Expected: "### Module 1 Assignment" in 00-course.md
- Action: Skipping assignment.md
```

**Module code collision:**
```
Error: Module code "101" already exists
- Existing: compiled/andamio-for-contributors/101/
- Action: Choose different code or delete existing
```

## Guidelines

- **Don't modify source files.** This skill only reads and outputs to `compiled/`.
- **Keep lesson content intact.** Only strip metadata headers, not pedagogical content.
- **SLT text is sacred.** Once on-chain, SLTs cannot change. Double-check the outline.md output.
- **Prefer completeness.** Warn about missing pieces but allow partial compiles for preview.
- **Clean output.** The `compiled/` directory should be uploadable as-is.
