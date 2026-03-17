---
description: Claim and work on feedback items
argument-hint: "[feedback-id]"
allowed-tools: Bash(node:*)
---

# Feedback Workflow

Work on a feedback item from the queue.

## Usage

- `/fb` - Auto-select and claim the best feedback item
- `/fb <id>` - Claim and work on a specific feedback item

## Arguments

$ARGUMENTS - Optional feedback ID (first 8+ characters)

## Instructions

### If no argument provided:

**STEP 1: Check for in-progress items**

Run this command to check if there are any in-progress items:
```bash
node F:/_CODE/shared-scripts/feedback/fetch-feedback.js mine
```

**If items are found:**

1. **Fetch full details for EACH in-progress item** - the `mine` list is truncated, so you MUST run:
   ```bash
   node F:/_CODE/shared-scripts/feedback/fetch-feedback.js <id>
   ```
   for each item to show the user the complete title, description, page/area, and any images.

2. **Display the full details** so the user can actually understand what each item is.

3. **Then ask:** "This item is in-progress from another session (claim token `[xxxxxxxx]`). Want me to continue working on it, or skip to unclaimed items?"

**If user says continue:**
1. First try: `node F:/_CODE/shared-scripts/feedback/fetch-feedback.js claim <id>`
2. If claim succeeds -> proceed with work
3. If claim fails with "active work in progress" -> the claim is still fresh (<45 min activity)
   - **DO NOT bypass the protection** - this would steal another agent's active work
   - Tell the user the options:
     a. "Wait for the claim to become stale (45 min inactivity)"
     b. "Submit a claim request: `request-claim <id> 'reason'` (starts 15-min countdown)"
     c. "Emergency takeover: `unclaim <id> --emergency 'reason'` (audited, requires justification)"
   - **Only the USER can decide to force or use emergency** - never do it automatically

**If user says skip:** Proceed to STEP 2 and pick from unclaimed items only.

**If no in-progress items found:** Proceed directly to STEP 2.

---

**STEP 2: Auto-select a new item**

Run `node F:/_CODE/shared-scripts/feedback/fetch-feedback.js list` to show the feedback queue.

**Auto-delete obvious test submissions:** Before selecting, scan the unclaimed list for items that are clearly just testing the feedback system (e.g., "This is a test", "Testing again", "asdfgh", single words like "test"). Delete these immediately without asking:
```bash
node F:/_CODE/shared-scripts/feedback/fetch-feedback.js delete <id>
```
Do NOT delete items that might be real feedback with poor titles - only delete when 99%+ confident it's just a test.

**Auto-select the best item using this priority:**

1. **ONLY select from "new" (unclaimed) items** - never select in-progress items for auto-selection
2. **Bugs first** - bugs affect current users, features can wait
3. **Higher priority** - high > medium > low > unset
4. **Skip incomplete metadata** - avoid items with `--title` or `--description` placeholders

**STOP OVERTHINKING. JUST PICK ONE.**

- Look at the list ONCE
- Pick the FIRST item that isn't obviously broken metadata
- If there are no bugs, pick the first feature
- "Too complex for one session" is NOT a reason to skip - you have plenty of tokens
- Large features are fine - break them into subtasks and make progress
- Do NOT check 2+ items before deciding
- Do NOT reject items for being "ambitious"

The goal is PROGRESS, not finding the "perfect" item.

After selecting, announce your choice with a 1-sentence rationale, then immediately claim it:
```bash
node F:/_CODE/shared-scripts/feedback/fetch-feedback.js claim <id>
```
This atomically claims the item with a unique token, preventing race conditions with other agents.

### If argument provided (feedback ID):

1. **Claim the feedback:**
   ```bash
   node F:/_CODE/shared-scripts/feedback/fetch-feedback.js claim $ARGUMENTS
   ```
   This atomically claims the item with a unique token, preventing other agents from picking it up.

2. **Display the feedback** with all details:
   - Title and ID
   - Type (bug/feature/enhancement) and Priority
   - Who submitted it and when
   - Page/Area it affects
   - The full description - word for word
   - Any existing notes or subtasks

3. **If feedback has images attached:**
   - Read each image with the Read tool (so Claude can analyze it)
   - **ALSO open each image for the user** so they see what you see:
     ```bash
     powershell -Command "Invoke-Item '<absolute-path-to-image>'"
     ```
   - This ensures both Claude and the user are looking at the same thing

4. **Assess complexity** using model triage:
   - **TRIVIAL** (Haiku): Literal string swaps, single-line changes where solution is already known
   - **MEDIUM** (Sonnet): CSS fixes, single-file changes, clear bugs with repro steps
   - **COMPLEX** (Opus): Multi-file coordination, ambiguous requirements, extension integration

5. **Announce triage decision:**
   ```
   **Complexity Assessment:** [TRIVIAL / MEDIUM / COMPLEX]
   **Model Routing:** [Delegating to Haiku / Delegating to Sonnet / Handling as Opus]
   **Reasoning:** [Brief explanation]
   ```

6. **Ask for confirmation** before proceeding with implementation.

7. **After user approves**, rename the conversation to reflect the feedback item:
   ```
   /rename FB: [short descriptive title]
   ```
   Use the feedback title if it's concise, or write a 2-4 word summary of what you're fixing/implementing.

### After implementing:

1. Move to review: `node F:/_CODE/shared-scripts/feedback/fetch-feedback.js <id> in-review "Brief admin notes"`
2. Summarize what changed
3. Give clear testing steps
4. Describe expected behavior
