---
name: blackbelt-meeting-summary
description: Processes BlackBelt coaching call transcripts and generates Basecamp-ready summaries. Use when "process meeting transcripts", "summarize BlackBelt meetings", "check for new transcripts".
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion
---

# BlackBelt Meeting Summary

## What This Does

Processes transcripts from BlackBelt coaching calls (Game Plan, Velocity, Red) and generates
summaries ready to paste into Basecamp. Follows the capture-triage pattern: scan → preview →
confirm → process → output.

## Watch Folder

```
/Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/Transcripts/
```

Processed transcripts move to `Transcripts/Processed/`.

## Instructions

### Step 1: Scan for Unprocessed Transcripts

1. Read all `.md` and `.txt` files in the Transcripts folder (not Processed subfolder)
2. For each file, try to detect:
   - Client name (from filename or speaker names in transcript)
   - Session type (Game Plan, Velocity, Red) from filename or content
3. Skip files that are empty or don't look like transcripts

### Step 2: Dry-Run Preview

Use AskUserQuestion to show what was found:

```
Found transcripts to process:

| # | File | Detected Client | Type |
|---|------|-----------------|------|
| 1 | GamePlan-Bren-Jan5.md | Bren | Game Plan |
| 2 | Velocity-Jan5.md | ? | Velocity |

Please confirm or correct the client name and session type for each.
```

Options for each:
- Confirm as detected
- Enter correct client name
- Select session type (Game Plan / Velocity / Red)
- Skip this transcript

### Step 3: Process Each Confirmed Transcript

For each approved transcript:

1. **Read the full transcript**

2. **Generate summary** using the template below (250-400 words)

3. **Run through ai-slop-detector skill** to clean up AI patterns

4. **Save to Zettelkasten:**
   - Filename: `Meeting Summary - [Client] - [Type] - YYYY-MM-DD.md`
   - Location: `/Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/`

5. **Add to daily note Captures section:**
   ```
   - [[Meeting Summary - [Client] - [Type] - YYYY-MM-DD]] - [Type] with [Client]
   ```

6. **Move transcript** to `Transcripts/Processed/`

### Step 4: Display Copyable Output

For each processed meeting, display the Basecamp-ready summary in a code block:

```
✓ Processed: [Client] — [Type] Summary

Copy for Basecamp:
```

Then show the summary in a fenced code block for easy copy/paste.

---

## Summary Template

### Voice Guidelines

- Ed Dale's voice: clear, direct, practical. Bond Halbert tight edits. No fluff. Short sentences.
- Australian English.
- Compassionate amusement. Celebrate real wins. Call out what's cool.
- Plain language. Avoid jargon unless transcript uses it.
- **Highlight areas of concern** - reality makes these valuable.

### Output Structure (250-400 words)

```
**[Client Name] — [Call Type] Summary**
Coach: Ed Dale

**Summary:**
- 2-3 short paragraphs
- Include 1-3 direct quotes from client (attribute with name + role)
- State core outcome(s), main shift/decision, any milestone
- Highlight areas of concern if present

**Key Focus Areas:**
- Bulleted list of main topics/systems discussed

**Trainings Highlighted / Assigned:**
- Label-only (no links)

**Requests / Follow-Ups for the Blackbelt Team:**
- Explicit requests made on the call (ops team visibility)

**Momentum & Culture - Call Vibes:**
- 1-2 bullets on rhythm, energy, confidence, systemisation
- Potential issues in energy, language, emotion

**Next Steps / Action Items:**
- Bulleted, concrete, time-bound where possible
- One line each
```

---

## Saved Document Format

```markdown
---
type: meeting-summary
client: [Client Name]
session-type: game-plan | velocity | red
date: YYYY-MM-DD
coach: Ed Dale
---

# [Client Name] — [Call Type] Summary

## Basecamp Update

\`\`\`
[Full formatted summary - ready to copy]
\`\`\`

## Transcript Reference

Source: [[Original Transcript Filename]]
```

---

## Session Types

| Type | Duration | Focus |
|------|----------|-------|
| **Game Plan** | 45min-2hr | Onboarding strategy, foundations |
| **Velocity** | 20min | Progress check, adjustments, next steps |
| **Red** | 20min | Emergency/issue resolution |

---

## Requirements

- Be faithful to the transcript. Do not invent facts.
- Keep total length tight (target 250-400 words).
- No hyperlinks in the Trainings section.
- If a role isn't stated, add a brief clarifier only when obvious from transcript.
- Always run through ai-slop-detector before saving.

---

## Examples

### Good Summary

```
**Bren & Christy — Velocity Summary**
Coach: Ed Dale

**Summary:**
Record month just wrapped. "Christy's confidence has gone through the roof." — Bren.
The triage call system is now running smoothly with Christy handling initial conversations.
Main focus this session was locking in the Six-Week Campaign rhythm and content repurposing.

One concern: Bren mentioned feeling stretched with LinkedIn output. Worth monitoring.

**Key Focus Areas:**
- Triage call handoff to Christy
- Six-Week Campaign planning
- Content repurposing from podcast
- LinkedIn posting rhythm

**Trainings Highlighted / Assigned:**
- Strategy Call Framework
- Six-Week Campaign overview
- Content Alchemy

**Requests / Follow-Ups for the Blackbelt Team:**
- Send today's recording
- Add Strategy Call training to their portal

**Momentum & Culture - Call Vibes:**
- High energy, clear direction. Team operating as unit now.
- Christy stepping up has freed Bren for strategy work.

**Next Steps / Action Items:**
- Christy to run next three triage calls solo
- Bren to draft Six-Week Campaign theme by Friday
- Review LinkedIn content batch next Velocity
```
