---
name: extract-my-action-items
description: Extract action items from a Fireflies call transcript. Default extracts for ALL attendees; specify a target person to extract only theirs. Use when the user wants to find commitments, assignments, and follow-ups from a recorded meeting.
user-invocable: true
---

# Extract Action Items

Extract action items from a Fireflies transcript using parallel subagents. Catches items automated summaries miss.

**Two modes:**
- **All attendees (default):** No target specified — extract action items for every participant
- **Single person:** Target specified — extract action items for that person only

## Phase 1: Determine Mode

Parse the user's invocation:
- If a target person is specified → **single-person mode**
- Otherwise → **all-attendees mode**

Extract the search criteria (date, keyword, or transcript ID) from the invocation.

## Phase 2: Fetch & Preprocess (Subagent)

The transcript API returns a JSON array (or an MCP wrapper containing one). Extract to plain text before chunking.

You should inspect the user's local hooks config and avoid running commands that are blocked by the hooks.

### MCP based extraction
```bash
mkdir -p .claude/scratchpad
node -e "
  const fs = require('fs');
  let data = JSON.parse(fs.readFileSync(process.argv[1], 'utf8'));
  // Handle MCP wrapper: if top-level array has a .text field containing the real transcript, parse that
  if (data.length === 1 && typeof data[0]?.text === 'string') {
    // Extract speaker lines from the text content
    const lines = data[0].text.split('\n').filter(l => l.match(/^[A-Za-z].*?:/));
    fs.writeFileSync('.claude/scratchpad/transcript.txt', lines.join('\n'));
    const speakers = [...new Set(lines.map(l => l.split(':')[0].trim()))].sort();
    console.log('Speakers:', JSON.stringify(speakers));
    console.log('Total lines:', lines.length);
  } else {
    // Standard array of {speaker_name, text} objects
    const lines = data.map(e => (e.speaker_name || 'Unknown') + ': ' + (e.text || ''));
    fs.writeFileSync('.claude/scratchpad/transcript.txt', lines.join('\n'));
    const speakers = [...new Set(data.map(e => e.speaker_name).filter(Boolean))].sort();
    console.log('Speakers:', JSON.stringify(speakers));
    console.log('Total lines:', lines.length);
  }
" [TRANSCRIPT_JSON_FILE]
```

If the transcript JSON was saved to a tool-results file by the MCP client, pass that file path as the argument.

### API based extraction

**CRITICAL: The orchestrator MUST NOT call any Fireflies MCP tools directly. ALL Fireflies interaction happens inside this subagent.**

Launch a single `general-purpose` subagent with this prompt:

```
Search Fireflies for a transcript matching: [SEARCH_CRITERIA]

1. Call `mcp__fireflies__fireflies_get_transcripts` to find the transcript (by date, keyword, or ID).
2. Call `mcp__fireflies__fireflies_get_summary` and `mcp__fireflies__fireflies_get_transcript` in parallel for the matched transcript.
3. The transcript API returns a JSON array. Extract to plain text:
   - With jq: jq -r '.[].text' < raw_transcript.json > .claude/scratchpad/transcript.txt
   - Fallback: python3 -c "import json,sys; print('\n'.join(e['text'] for e in json.load(sys.stdin)))" < raw_transcript.json > .claude/scratchpad/transcript.txt
4. Count lines: wc -l < .claude/scratchpad/transcript.txt
5. Extract the distinct speaker list from the transcript JSON:
   python3 -c "import json,sys; data=json.load(sys.stdin); print('\n'.join(sorted(set(e.get('speaker_name','') for e in data if e.get('speaker_name')))))" < raw_transcript.json

Return EXACTLY this (no other text):
- meeting_title: <title>
- meeting_date: <date>
- transcript_id: <id>
- transcript_path: .claude/scratchpad/transcript.txt
- line_count: <number>
- speakers: <comma-separated list>
- summary: <the Fireflies summary text>
```

Wait for the subagent to finish. Parse its returned values — these are the inputs for the remaining phases.


## Phase 3: Parallel Subagent Extraction

**Chunk sizing:** `ceil(total_lines / 5)` lines per chunk, minimum 200. Adjust chunk count so no chunk is under 200 lines.

Launch one `general-purpose` subagent per chunk.

### Single-Person Prompt

```
Read lines [START] to [END] of [FILE_PATH].

Find ALL action items for [TARGET_PERSON]. Return each as:
- **Item**: what they committed to
- **Quote**: exact words from transcript
- **Context**: who else involved, any deadline

Beyond obvious commitments ("I'll do X"), catch these non-obvious patterns:
- Self-notes: "I'll make a note to...", "let me jot down..."
- Admissions implying catch-up: "I dropped the ball on X", "I still haven't read X"
- Conditional offers that became commitments: "If we have time, I'm happy to..."
- Volunteering: "I guess I'll volunteer to..."
- Exploration tasks: "Let me spend a few hours with it"
- Questions/topics for external parties: "I need to ask [person/firm] about X", "thing to discuss with [party]"
```

### All-Attendees Prompt

```
Read lines [START] to [END] of [FILE_PATH].

The meeting attendees are: [SPEAKER_LIST]

Find ALL action items for EVERY attendee. Group by person. For each item return:
- **Person**: who owns the action item
- **Item**: what they committed to
- **Quote**: exact words from transcript
- **Context**: who else involved, any deadline

Beyond obvious commitments ("I'll do X"), catch these non-obvious patterns:
- Self-notes: "I'll make a note to...", "let me jot down..."
- Admissions implying catch-up: "I dropped the ball on X", "I still haven't read X"
- Conditional offers that became commitments: "If we have time, I'm happy to..."
- Volunteering: "I guess I'll volunteer to..."
- Exploration tasks: "Let me spend a few hours with it"
- Questions/topics for external parties: "I need to ask [person/firm] about X", "thing to discuss with [party]"
- Delegations: "[Person], can you handle X?", "I'll leave that to [person]"
```

## Phase 4: Consolidate

Merge subagent results, deduplicate, and categorize. **Only include categories that have items.**

### Categories

1. **High Priority / Technical** — Code changes, bug fixes, PR reviews, investigations
2. **Pairing / Collaboration** — Scheduled syncs, joint work sessions
3. **Content / Research** — Reading, writing, experiments, documentation
4. **Questions for External Parties** — Topics to raise with specific people/firms outside the immediate team
5. **Exploration / Tooling** — Tool evaluations, setup, environment tasks
6. **Catch-up** — Things explicitly acknowledged as dropped or missed

### Output

**Single-person mode** — Write to `.claude/scratchpad/[name]-action-items-YYYY-MM-DD.md`:

```markdown
# [Name] Action Items — [Meeting Title]

**Date:** [Date]
**Fireflies Link:** https://app.fireflies.ai/view/[TRANSCRIPT_ID]

## [Category Name]

- [ ] **Item title**
  - Context and details
  - > "Exact quote"

## Quick Reference — Time-Sensitive

1. [Item with deadline or scheduled time]
```

**All-attendees mode** — Write to `.claude/scratchpad/action-items-YYYY-MM-DD.md`:

```markdown
# Action Items — [Meeting Title]

**Date:** [Date]
**Fireflies Link:** https://app.fireflies.ai/view/[TRANSCRIPT_ID]

## [Person Name]

### [Category Name]

- [ ] **Item title**
  - Context and details
  - > "Exact quote"

## Quick Reference — Time-Sensitive

1. [Person] — [Item with deadline or scheduled time]
```

## Phase 5: Review & DM to Slack

1. Use `AskUserQuestion`: **"DM action items to each person on Slack?"** — options: "Send DMs", "Skip — just keep the file"
2. If approved, ensure `.claude/slack-users.local.json` exists in the project root:
   - If **missing**, run `node [SKILL_DIR]/scripts/fetch-slack-users.mjs` (requires `SLACK_BOT_TOKEN` with `users:read` scope), present the output to the user for review, then save to `.claude/slack-users.local.json` (gitignored by `**/.claude/**/*.local.json`)
   - If **present**, proceed directly
3. Run the bundled script with the output file path:

```bash
node [SKILL_DIR]/scripts/slack-post.mjs [OUTPUT_FILE_PATH]
```

The script sends Block Kit–formatted DMs to each person via `conversations.open` + `chat.postMessage`. Requires env var `SLACK_BOT_TOKEN` (with `chat:write` and `im:write` scopes).

**Behavior by mode:**
- **All-attendees:** Each person matched in `slack-users.local.json` receives a DM with only their action items. Unresolvable names are skipped with a warning.
- **Single-person:** One DM to the target person.

Name resolution supports exact match and fuzzy first-name match (e.g., "Jelvin" resolves to "Jelvin Base"). After the script runs, report any skipped names to the user.

4. After posting (or skipping), delete all artifacts created during the run: `transcript.txt`, the action items markdown file, and any other temp files written to `.claude/scratchpad/` during this workflow.

## Example Invocations

- `/extract-my-action-items` — all attendees, most recent meeting
- `/extract-my-action-items standup` — all attendees, search for "standup"
- `/extract-my-action-items for Basti from yesterday` — single person
- `/extract-my-action-items 01KFY1RSEVVQW7MB1TKG4N2D20` — all attendees, specific transcript
