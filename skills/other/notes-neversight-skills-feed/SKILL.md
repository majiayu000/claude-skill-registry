---
name: notes
description: Collect and process inline editing notes from chapters. Finds %%NOTE:%%, %%EDIT:%%, %%CHECK:%%, and %%CUT:%% markers.
argument-hint: "[chapter] [--process] [--clear]"
disable-model-invocation: true
---

Scan chapters for inline editing notes and present them for processing.

## Note Format

While reading your manuscript, add inline notes using Obsidian's comment syntax:

```markdown
%%NOTE: observation or question%%
%%EDIT: specific change needed%%
%%CUT: text that should be removed%%
%%CHECK: continuity or fact to verify%%
```

These are invisible in Obsidian's reading view but visible when editing.

## What This Does

1. Greps all chapter files for `%%.*%%` patterns
2. Extracts notes with chapter name and line number
3. Groups by type (EDIT, NOTE, CHECK, CUT)
4. Presents them for review or processing

## Usage

```
/fiction:notes              # List all notes across chapters
/fiction:notes 5            # List notes in chapter 5 only
/fiction:notes --process    # Work through notes one by one
/fiction:notes --clear      # Remove all processed notes
```

If arguments provided: $ARGUMENTS

## Output Format

```markdown
## Editing Notes

### EDIT (4 items)
- **Chapter 2, line 3:** damp wool repeated
- **Chapter 7, line 45:** awkward transition
- **Chapter 12, line 88:** unclear antecedent
- **Chapter 12, line 92:** word echo "silent/silence"

### CHECK (2 items)
- **Chapter 2, line 21:** was this asked in ch1?
- **Chapter 9, line 156:** timeline - is this before or after the party?

### NOTE (1 item)
- **Chapter 15, line 200:** consider expanding this moment

### CUT (1 item)
- **Chapter 3, line 67:** this paragraph feels redundant
```

## Processing Modes

### List Mode (default)
Shows all notes grouped by type. Good for getting an overview.

### Process Mode (`--process`)
Works through notes one at a time:
1. Shows the note with surrounding context (5 lines before/after)
2. Offers options: Fix it, Skip, Delete note
3. For EDIT/CUT: suggests specific changes
4. For CHECK: investigates and reports findings
5. Removes the `%%marker%%` after processing

### Clear Mode (`--clear`)
Removes all `%%.*%%` markers from chapters. Use after you've addressed everything.

## When to Use

- During read-throughs: add notes as you spot issues
- Before revision: collect all notes to plan your editing session
- After revision: clear processed notes

## Workflow

1. Read chapters, adding `%%EDIT:%%`, `%%NOTE:%%`, etc. as you go
2. Run `/fiction:notes` to see everything collected
3. Run `/fiction:notes --process` to work through them systematically
4. Run `/fiction:notes --clear` when done

## Implementation

When executing this command:

1. **Find all notes:**
```bash
grep -rn '%%[A-Z]*:' chapters/*.md
```

2. **Parse each match:** Extract type, content, file, line number

3. **Group by type:** EDIT, NOTE, CHECK, CUT (and any others)

4. **For --process mode:**
   - Read context around each note
   - Present with options
   - Apply changes if requested
   - Remove the marker after processing

## Related Commands

- `/fiction:edit` — Automated line-level editing
- `/fiction:review` — Story and craft feedback
- `/fiction:continuity` — Cross-chapter consistency checks
