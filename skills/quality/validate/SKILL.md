---
name: Validate Training Materials
description: Run comprehensive validation and review checks including heading numbering, TODO/FIXME comments, Nextflow script conventions, orphaned files, admonition syntax, lesson structure, formatting, content accuracy, and teaching effectiveness. Use when validating, reviewing, or checking training materials quality, lesson quality, or before committing changes.
---

# Validate Training Materials

Run comprehensive validation checks on training materials. Execute from repository root.

See [../shared/repo-conventions.md](../shared/repo-conventions.md) for directory mapping and file conventions.

## Skill Dependencies (MANDATORY)

This skill MUST invoke other skills during validation. **Do not skip these.**

| Task | Skill | When |
|------|-------|------|
| Check code block highlights | `/check-highlights` | Always |
| Check inline code formatting | `/check-inline-code` | Always |

## Scope

Ask user to specify what to validate if not clear:
- Specific side quest (e.g., "debugging")
- Specific module (e.g., "hello_nextflow")
- Entire repository (only if explicitly requested)

## Determining Scope

Based on the user's request, determine the scope:

1. **Specific side quest** (e.g., "debugging"):

   - Documentation file: `docs/side_quests/{name}.md`
   - Example scripts: `side-quests/{name}/**/*.nf`
   - Solution files: `side-quests/solutions/{name}/**/*.nf`

2. **Specific module** (e.g., "hello_nextflow"):

   - Documentation files: `docs/{module}/**/*.md`
   - Example scripts: `{module}/**/*.nf` or `hello-nextflow/**/*.nf`
   - Solution files: `{module}/solutions/**/*.nf`

3. **Entire repository** (only if explicitly requested):
   - All files: `docs/**/*.md`, `**/*.nf`

## Tasks to Perform

Perform the following checks **only on files within the determined scope**:

1. **Check Heading Numbering**

   - Run: `uv run .github/check_headings.py [scoped-path]/**/*.md`
   - Report any heading numbering issues found
   - If errors exist, ask if user wants to auto-fix with `--fix` flag

2. **Find TODO/FIXME Comments**

   - Search markdown files in scope
   - Search Nextflow scripts in scope
   - Categorize by priority (high, medium, low)
   - Report files with most TODOs

3. **Check Nextflow Script Conventions**

   - Find .nf files in scope
   - Verify they start with `#!/usr/bin/env nextflow`
   - Check for DSL2 syntax
   - Report any that don't follow conventions

4. **Find Orphaned Files**

   - Check if main documentation file is referenced in mkdocs.yml
   - Look for solution files without corresponding exercise documentation
   - Report any orphaned files within scope

5. **Verify Admonition Syntax**

   - Search for common admonition formatting errors in scoped files
   - Check for proper indentation (4 spaces)
   - Report any malformed admonitions

6. **Check Code Block Highlights**

   ```
   >>> STOP. INVOKE /check-highlights on the scoped files NOW.

   Record results before continuing.
   ```

7. **Check Inline Code Formatting**

   ```
   >>> STOP. INVOKE /check-inline-code on the scoped files NOW.

   Record results before continuing.
   ```

8. **Check Writing Style**

   - Search for LLM-style patterns that should be avoided:
     - `Let's` or `let's` at start of sentences
     - `Remember when` or `Remember that` callbacks
     - `Don't worry` reassurances
     - `worth mentioning` or `important to note` padding
     - Exclamation marks used for emphasis (not in code/output)
   - Check for em-dash elaborations (space-hyphen-space followed by lowercase) that could be periods
   - Flag any issues found for manual review

9. **Deep Lesson Review** (when reviewing a specific lesson file)

   If the user asks to review a specific lesson, perform this comprehensive checklist:

   a. **Structure Check**:

   - [ ] Proper heading numbering with trailing periods
   - [ ] Heading levels match numbering depth (## for 1., ### for 1.1.)
   - [ ] Each major section has "### Takeaway"
   - [ ] Each major section has "### What's next?"
   - [ ] Logical flow from simple to complex
   - [ ] Clear learning objectives stated or implied

   b. **Formatting Check**:

   - [ ] Code blocks have proper titles, line numbers, and highlighting
   - [ ] Console output properly formatted with `console title="Output"`
   - [ ] File paths use proper markdown formatting
   - [ ] Before/After comparisons use tabbed blocks
   - [ ] Admonitions properly formatted and indented
   - [ ] Each sentence on new line (for clean diffs)

   c. **Content Check**:

   - [ ] Technical accuracy of Nextflow code
   - [ ] Commands are correct and runnable
   - [ ] Parameter syntax correct (-- for pipeline, - for Nextflow)
   - [ ] Examples progress logically
   - [ ] Common pitfalls addressed
   - [ ] Edge cases explained

   d. **Teaching Effectiveness**:

   - [ ] Clear explanations for beginners
   - [ ] Concepts introduced before use
   - [ ] Examples are relevant and motivating
   - [ ] Exercises appropriate for skill level
   - [ ] Solutions available for exercises
   - [ ] Good use of tips and warnings

   e. **Cross-References**:

   - [ ] Links to related lessons work
   - [ ] References to files/scripts are correct
   - [ ] External links are valid
   - [ ] Prerequisites clearly stated

   f. **Examples & Code**:

   - [ ] All Nextflow examples are syntactically correct
   - [ ] Variable names are clear and consistent
   - [ ] Comments explain non-obvious code
   - [ ] Examples can be run as shown
   - [ ] Output examples match what code produces

   g. **Writing Style** (see CLAUDE.md for full guidelines):

   - [ ] No LLM-style interjections ("Let's", "Remember when...?", "Don't worry")
   - [ ] No exclamation-based emphasis ("Much faster!", "So powerful!")
   - [ ] Em-dash elaborations replaced with periods or semicolons
   - [ ] List explanations use colons, not hyphens
   - [ ] Single clear explanation per concept (not multiple phrasings)
   - [ ] Professional, direct tone throughout

## Output Format

Structure your report with these sections:

```
# Validation Report

## Heading Numbering
## TODO/FIXME Comments (count by priority, list top files)
## Nextflow Scripts (conventions check)
## Orphaned Files
## Admonitions
## Code Block Highlights (from /check-highlights)
## Inline Code Formatting (from /check-inline-code)
## Writing Style
## Summary
```

For deep lesson reviews, add sections for: Structure, Formatting, Content Accuracy, Teaching Effectiveness, Cross-References, Examples & Code, Writing Style, Overall Assessment, Positive Aspects.

**Important**: Always provide actionable next steps for any issues found. If no issues found, give clear confirmation.
