---
name: slide-management
description: '**MANDATORY USE - ALWAYS INVOKE THIS SKILL** when the user mentions
  ANY of these actions: "delete slide", "remove slide", "add slide", "insert slide",
  "create new slide", "new slide between", "get rid'
---

---
name: Slide Management
description: **MANDATORY USE - ALWAYS INVOKE THIS SKILL** when the user mentions ANY of these actions: "delete slide", "remove slide", "add slide", "insert slide", "create new slide", "new slide between", "get rid of slide", "fix gaps", "renumber slides", OR when they confirm/answer questions about slide deletion/addition (e.g., "yes delete slide 6", "add a slide after 5"). **CRITICAL - NEVER manually edit slides.md or rename slide files yourself** - this skill uses the manage-slides.py script which handles automatic renumbering, gap detection/fixing, git-aware operations, and slide number vs position conversion. **AUTO-TRIGGER IMMEDIATELY** when user wants to modify slide count, order, or numbering. This skill is the ONLY correct way to add/delete slides.
version: 0.4.0
---

# Slide Management

Manage slide additions and deletions with automatic renumbering. The system handles file renaming, updates slides.md, and uses git-aware operations for tracked files.

## How This Skill Works

This skill provides an interactive workflow for:
- **Adding slides**: Insert new slide at any position with automatic renumbering of subsequent slides
- **Deleting slides**: Remove slide and renumber remaining slides to close gaps
- **Git awareness**: Uses `git mv` for tracked files, regular `mv` for untracked files

## Workflow

### Step 1: Find and Display Current Slides

Use Bash to find slides.md:
```bash
find . -name "slides.md" -type f -not -path "*/node_modules/*" | head -1
```

Then use Read tool on slides.md and parse all slide entries.

**CRITICAL - Gap Detection:**
After parsing slides, check for gaps in slide numbering:
- Extract all slide numbers from the parsed slides
- **IMPORTANT**: Ignore gaps at the beginning (e.g., slide 1 then slide 5 is OK - title then content)
- Only detect gaps in the MIDDLE of the sequence (e.g., slides 5, 6, 9, 10 - gap at 7-8)
- Check from the second slide onwards

Display current presentation structure to user:

```
📊 Current Presentation Structure (N slides)

Position 1 → Slide 1: Title Slide
             slides/01-title.md

Position 2 → Slide 5: Introduction
             slides/05-introduction.md

Position 3 → Slide 6: Main Topic
             slides/06-main-topic.md

... (show all slides with BOTH position and slide number)
```

**CRITICAL - Always show both:**
- Position: The order in the list (1st, 2nd, 3rd...)
- Slide number: The number in the filename and comment

If gaps are detected in the middle, add a warning:

```
⚠️  Numbering gaps detected in middle: [7, 8]
(Note: Gap at beginning preserved - typically title at 1, content starts at 5+)
You can fix middle gaps with the renumber operation.
```

**Important**: The renumber operation:
- **PRESERVES** the gap between slide 1 and slide 2 (e.g., 1→5 stays as 1→5)
- **FIXES** gaps in the middle sequence (e.g., 5,6,9,10 becomes 5,6,7,8)
- This is by design: title slides often need separation from content slides

### Step 2: Ask What to Do

Use AskUserQuestion to ask the user what they want to do.

**IMPORTANT**: Dynamically build the options list based on whether gaps exist:

If **gaps detected**, offer 4 options:
```
- question: "What would you like to do with the slides?"
- header: "Action"
- multiSelect: false
- options:
  1. label: "Fix gaps"
     description: "Close middle gaps (preserves beginning gap like 1→5 for title separation)"
  2. label: "Add slide"
     description: "Insert a new slide at any position"
  3. label: "Delete slide"
     description: "Remove a slide"
  4. label: "View only"
     description: "Just browsing the current structure"
```

If **no gaps detected**, offer 3 options:
```
- question: "What would you like to do with the slides?"
- header: "Action"
- multiSelect: false
- options:
  1. label: "Add slide"
     description: "Insert a new slide at any position with automatic renumbering"
  2. label: "Delete slide"
     description: "Remove a slide and renumber remaining slides"
  3. label: "View only"
     description: "Just browsing the current structure"
```

If user chooses "View only", end the skill.

If user chooses "Fix gaps", go to Step 2b.

### Step 2b: Fix Gaps Flow (if user chose "Fix gaps")

#### 2b.1: Show Impact and Confirm

Display what will happen:

```
🔧 Fix Numbering Gaps

Current middle gaps: [7, 8]
Beginning gap: 1 → 5 (preserved)

This will close middle gaps while preserving the beginning gap:
- Slide 1 → Slide 1 (no change - title)
- Slide 5 → Slide 5 (no change - beginning gap preserved)
- Slide 6 → Slide 6 (no change)
- Slide 9 → Slide 7 (gap closed)
- Slide 10 → Slide 8 (gap closed)
... (show all renumbering)

Result: Slides will be 1, 5-N with no middle gaps
```

Ask for confirmation:

```
- question: "Proceed with renumbering?"
- header: "Confirm"
- multiSelect: false
- options:
  1. label: "Yes, fix gaps"
     description: "Renumber all slides to be sequential"
  2. label: "Cancel"
     description: "Keep current numbering"
```

If user cancels, return to Step 2.

#### 2b.2: Execute Renumber Script

Use Bash to execute:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/manage-slides.py renumber
```

Capture both stdout and stderr, check exit code.

#### 2b.3: Show Results

If successful:

```
✅ Gaps Fixed Successfully

Renumbered slides:
- Slide 9 → Slide 7 (slides/07-advanced.md)
- Slide 10 → Slide 8 (slides/08-conclusion.md)
... (show all renumbered)

Beginning gap preserved: Slide 1 → Slide 5
Total slides: N (numbered 1, 5-N with no middle gaps)
```

Then offer next action:

```
- question: "What would you like to do next?"
- header: "Next"
- multiSelect: false
- options:
  1. label: "Add slide"
     description: "Insert a new slide"
  2. label: "Delete slide"
     description: "Remove a slide"
  3. label: "Done"
     description: "Finish managing slides"
```

### Step 3a: Delete Flow (if user chose "Delete slide")

#### 3a.1: Ask Which Slide to Delete

**CRITICAL - Slide Number vs Position:**
- The user thinks in terms of SLIDE NUMBERS (what they see: "Slide 24")
- The script requires POSITION (where in the list: 1st, 2nd, 3rd)
- You MUST convert slide number → position before calling the script

Generate options dynamically from the slide list you parsed. For each slide, create an option showing BOTH:

```
- question: "Which slide would you like to delete?"
- header: "Slide"
- multiSelect: false
- options:
  [Generate options for each slide. Use position as label, show slide number and title:]

  label: "1"
  description: "Slide 1: Title Slide (slides/01-title.md)"

  label: "2"
  description: "Slide 5: Architecture Overview (slides/05-architecture-overview.md)"

  label: "3"
  description: "Slide 6: Main Topic (slides/06-main-topic.md)"
```

**Store the mapping**: When user selects an option, the label gives you the POSITION to pass to the script.

#### 3a.2: Ask About Renumbering

Ask if user wants to renumber after deletion:

```
- question: "Should remaining slides be renumbered to close gaps?"
- header: "Renumber"
- multiSelect: false
- options:
  1. label: "Yes, renumber"
     description: "Make slides sequential (1, 2, 3, ...) with no gaps"
  2. label: "No, leave gaps"
     description: "Keep slide numbers unchanged (may create gaps)"
```

#### 3a.3: Show Impact and Confirm

**CRITICAL**: User selected a position. Look up the slide at that position to get its slide number.

Calculate and show the impact based on renumber choice:

If **renumbering**:
```
⚠️ Confirm Deletion

Deleting: Position [P] → Slide [N]: [Title]
File: slides/0N-[slug].md

Impact (with renumbering):
- All slides after position [P] will be renumbered sequentially
- All slides will be sequential (1, 2, 3, ...) with no gaps
- Affects [X] slides total
```

If **not renumbering**:
```
⚠️ Confirm Deletion

Deleting: Position [P] → Slide [N]: [Title]
File: slides/0N-[slug].md

Impact (without renumbering):
- Slide will be removed
- Remaining slides keep their current numbers
- This may create or enlarge a gap in numbering
```

Then ask for confirmation:

```
- question: "Proceed with deletion?"
- header: "Confirm"
- multiSelect: false
- options:
  1. label: "Yes, delete"
     description: "Remove slide [with/without renumbering]"
  2. label: "Cancel"
     description: "Keep all slides unchanged"
```

If user cancels, return to Step 2.

#### 3a.4: Execute Delete Script

**CRITICAL**: The script expects POSITION (1-indexed position in list), NOT slide number!

Use Bash to execute the Python script with the POSITION:

If renumbering:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/manage-slides.py delete [POSITION] --renumber
```

If not renumbering:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/manage-slides.py delete [POSITION]
```

Where [POSITION] is the position the user selected (from the label in step 3a.1).

Capture both stdout and stderr.

Check exit code:
- Exit code 0: Success
- Exit code > 0: Error (show error message from stderr)

#### 3a.5: Show Results

If successful, show summary:

```
✅ Slide Deleted Successfully

Removed:
- Slide [N]: [Title]
- File: slides/0N-[slug].md

Renumbered:
- Slide [N+1] → Slide [N]
- Slide [N+2] → Slide [N+1]
... (show all renumbered slides)

Total slides: [M-1] (was [M])
```

If error, show error message and offer to retry or cancel.

Then offer next action:

```
- question: "What would you like to do next?"
- header: "Next"
- multiSelect: false
- options:
  1. label: "Delete another"
     description: "Remove another slide"
  2. label: "Add slide"
     description: "Insert a new slide"
  3. label: "Done"
     description: "Finish managing slides"
```

### Step 3b: Add Flow (if user chose "Add slide")

#### 3b.1: Ask Position

**CRITICAL - Position vs Slide Number:**
- Ask for POSITION in the list (1st, 2nd, 3rd...)
- Show what slide is currently at each position

Generate position options (1 through N+1):

```
- question: "Where should the new slide be inserted?"
- header: "Position"
- multiSelect: false
- options:
  [Generate options for all valid positions, showing current slide at each:]

  label: "1"
  description: "At beginning (before current position 1 → Slide 1: Title)"

  label: "2"
  description: "After position 1 (before current position 2 → Slide 5: Introduction)"

  label: "3"
  description: "After position 2 (before current position 3 → Slide 6: Main Topic)"

  ...

  label: "[N+1]"
  description: "At end (after last slide)"
```

The user selects a POSITION, which is what the script expects.

#### 3b.2: Ask Title and Layout

Ask for both title and layout in one question set:

```
Question 1:
- question: "What should the slide title be?"
- header: "Title"
- multiSelect: false
- options:
  1. label: "Enter custom title"
     description: "Type your slide title in the Other field"
```

(User will use "Other" option to enter their custom title)

```
Question 2:
- question: "Which layout should the slide use?"
- header: "Layout"
- multiSelect: false
- options:
  1. label: "default"
     description: "Standard layout"
  2. label: "center"
     description: "Centered content"
  3. label: "two-cols"
     description: "Two columns side by side"
  4. label: "image-right"
     description: "Content on left, image on right"
  5. label: "quote"
     description: "Large quote display"
  6. label: "cover"
     description: "Cover/title slide style"
```

Extract the custom title from the "Other" response.

#### 3b.3: Ask About Renumbering

Ask if user wants to renumber after addition:

```
- question: "Should all slides be renumbered to be sequential?"
- header: "Renumber"
- multiSelect: false
- options:
  1. label: "Yes, renumber"
     description: "Make all slides sequential (1, 2, 3, ...) with no gaps"
  2. label: "No, use gaps"
     description: "Insert at position, may create or use existing gaps"
```

#### 3b.4: Show Preview and Confirm

Generate slug from title (lowercase, hyphens, max 40 chars) and show preview based on renumber choice:

If **renumbering**:
```
📋 New Slide Preview

Position: [N]
Title: [User's title]
Layout: [Selected layout]
Filename: slides/0N-[generated-slug].md

Impact (with renumbering):
- New slide will be inserted at position [N]
- Current slides [N] through [M] will become [N+1] through [M+1]
- All slides will be sequential (1, 2, 3, ...) with no gaps
- Affects [X] slides
```

If **not renumbering**:
```
📋 New Slide Preview

Position: [N]
Title: [User's title]
Layout: [Selected layout]
Filename: slides/0N-[generated-slug].md

Impact (without renumbering):
- New slide will be inserted at position [N]
- Slide number will fit into existing sequence/gaps
- May create or use existing gaps in numbering
```

Ask for confirmation:

```
- question: "Create this slide?"
- header: "Confirm"
- multiSelect: false
- options:
  1. label: "Yes, create"
     description: "Add slide [with/without renumbering]"
  2. label: "Cancel"
     description: "Don't make changes"
```

If cancelled, return to Step 2.

#### 3b.5: Execute Add Script

**CRITICAL**: The script expects POSITION (1-indexed position in list), NOT slide number!

Use Bash to execute with the POSITION from step 3b.1:

If renumbering:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/manage-slides.py add [POSITION] \
  --title "[User's title]" \
  --layout [layout] \
  --renumber
```

If not renumbering:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/manage-slides.py add [POSITION] \
  --title "[User's title]" \
  --layout [layout]
```

Where [POSITION] is the position the user selected (from the label in step 3b.1).

Capture output and check exit code.

#### 3b.6: Show Results and Next Steps

If successful:

```
✅ Slide Created Successfully

Added:
- Slide [N]: [Title]
- File: slides/0N-[slug].md
- Layout: [layout]

Renumbered:
- Old Slide [N] → Slide [N+1]
- Old Slide [N+1] → Slide [N+2]
... (show renumbered slides)

Total slides: [M+1] (was [M])
```

Then offer next actions:

```
- question: "What would you like to do next?"
- header: "Next"
- multiSelect: false
- options:
  1. label: "Edit new slide"
     description: "Open slide [N] for editing with /slidev:edit"
  2. label: "Add another"
     description: "Add another slide"
  3. label: "Done"
     description: "Finish managing slides"
```

If user chooses "Edit new slide", invoke the edit command:
```
Use SlashCommand tool: "/slidev:edit [N]"
```

### Error Handling

When the Python script returns a non-zero exit code:

1. Capture stderr output
2. Extract error message
3. Display user-friendly error:

```
❌ Operation Failed

Error: [Parsed error message]

Details: [Technical details if helpful]
```

Then ask:

```
- question: "How should we proceed?"
- header: "Action"
- multiSelect: false
- options:
  1. label: "Try again"
     description: "Retry the operation"
  2. label: "Cancel"
     description: "Return to main menu"
  3. label: "Show full error"
     description: "Display complete error output for debugging"
```

## Important Notes

- **CRITICAL - Position vs Slide Number**:
  - POSITION: Order in the list (1st slide, 2nd slide, 3rd slide...)
  - SLIDE NUMBER: Number in filename and comment (Slide 1, Slide 5, Slide 6...)
  - If there are gaps, these are DIFFERENT! Example: slides [1, 5, 6, 7] means position 2 = slide 5
  - The script always expects POSITION, never slide number
  - The skill must convert user's slide number selection to position before calling script

- **Gap handling**:
  - Gaps at beginning are PRESERVED (e.g., slide 1 then slide 5 is OK for title + content)
  - Gaps in middle are DETECTED and offered for fixing (e.g., slides 5, 6, 9, 10 - gaps 7-8)
  - The renumber operation preserves beginning gap but fixes middle gaps
  - Example: [1, 5, 6, 9, 10] becomes [1, 5, 6, 7, 8] (1→5 preserved, middle gaps fixed)

- **Git awareness**: The script automatically detects git-tracked files and uses `git mv` for them
- **Rollback on error**: If any operation fails, all changes are automatically rolled back
- **Validation**: Position ranges are validated before execution
- **Atomic operations**: Backup is created before any changes, restored on error

## Edge Cases

**Deleting slide 1:**
- Warn that all slides will be renumbered
- Show what the new first slide will be

**Adding at end (position N+1):**
- No renumbering needed, just append
- Optimize for this case

**Number overflow (>99):**
- Script enforces max 99 slides
- Error message suggests splitting presentation

## Example Interaction

**Example 1: Add slide with sequential numbering**

```
User invokes skill:

📊 Current Presentation Structure (5 slides)

Position 1 → Slide 1: Title Slide
             slides/01-title.md
Position 2 → Slide 2: Introduction
             slides/02-introduction.md
Position 3 → Slide 3: Main Topic
             slides/03-main-topic.md
Position 4 → Slide 4: Examples
             slides/04-examples.md
Position 5 → Slide 5: Conclusion
             slides/05-conclusion.md

What would you like to do?
> User chooses: "Add slide"

Where should the new slide be inserted?
> User chooses: label "3" (description: "After position 2, before position 3 → Slide 3: Main Topic")

What should the slide title be?
> User enters: "Architecture Overview"

Which layout?
> User chooses: "two-cols"

Should all slides be renumbered?
> User chooses: "Yes, renumber"

📋 New Slide Preview

Position: 3
Title: Architecture Overview
Layout: two-cols
Filename: slides/03-architecture-overview.md

Impact (with renumbering):
- New slide will be inserted at position 3
- Current slides 3-5 will become 4-6
- All slides will be sequential with no gaps
- Affects 3 slides

Create this slide?
> User confirms: "Yes, create"

[Script executes: python3 manage-slides.py add 3 --title "Architecture Overview" --layout two-cols --renumber]

✅ Slide Created Successfully

Added:
- Slide 3: Architecture Overview
- File: slides/03-architecture-overview.md
- Layout: two-cols

Renumbered:
- Old Slide 3 (Main Topic) → Slide 4
- Old Slide 4 (Examples) → Slide 5
- Old Slide 5 (Conclusion) → Slide 6

Total slides: 6 (was 5)

What next?
> User chooses: "Edit new slide"

[Invokes /slidev:edit 3]
```

**Example 2: Delete slide with gaps**

```
User invokes skill:

📊 Current Presentation Structure (4 slides)

Position 1 → Slide 1: Title
             slides/01-title.md
Position 2 → Slide 5: Introduction
             slides/05-introduction.md
Position 3 → Slide 6: Main Topic
             slides/06-main-topic.md
Position 4 → Slide 7: Conclusion
             slides/07-conclusion.md

⚠️  Numbering gaps detected in middle: [none]
(Note: Gap between slide 1 and 5 is preserved - typically title then content)

What would you like to do?
> User chooses: "Delete slide"

Which slide would you like to delete?
> User chooses: label "3" (description: "Slide 6: Main Topic (slides/06-main-topic.md)")

Should remaining slides be renumbered to close gaps?
> User chooses: "No, leave gaps"

⚠️ Confirm Deletion

Deleting: Position 3 → Slide 6: Main Topic
File: slides/06-main-topic.md

Impact (without renumbering):
- Slide will be removed
- Remaining slides keep their current numbers
- This may create or enlarge a gap in numbering

Proceed with deletion?
> User confirms: "Yes, delete"

[Script executes: python3 manage-slides.py delete 3]

✅ Slide Deleted Successfully

Removed:
- Position 3 → Slide 6: Main Topic
- File: slides/06-main-topic.md

Current slides:
- Position 1 → Slide 1: Title
- Position 2 → Slide 5: Introduction
- Position 3 → Slide 7: Conclusion

⚠️  Numbering gaps detected in middle: [6]

Total slides: 3 (was 4)
```

## Tools Available

- **Read**: Read slides.md and slide files
- **Bash**: Execute manage-slides.py script
- **SlashCommand**: Invoke /slidev:edit if user wants to edit new slide
- **AskUserQuestion**: Interactive workflow questions

Use this skill whenever users need to reorganize, add, or remove slides from their presentation. The automatic renumbering ensures the presentation structure remains clean and sequential.
