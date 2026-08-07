---
name: meeting-copilot
description: Use when preparing for, running, or closing a live meeting with an AI assistant dashboard. Triggers on "meeting copilot", "live copilot", "prepare for a call", "update copilot", "close the session", or requests to turn transcript chunks into meeting questions, topic maps, decisions, and follow-ups.
---

# Meeting Copilot

Create and maintain a local HTML dashboard for a live meeting. The dashboard gives the user a second-screen view of context, questions, topic progress, decisions, risks, and follow-ups while the call is happening.

This skill is designed for private workspaces. Do not publish raw transcripts, client names, personal notes, or generated meeting artifacts unless the user explicitly asks for a sanitized export.

## Modes

Use one of three modes:

| Mode | When | Output |
| --- | --- | --- |
| CREATE | Before the meeting | A local dashboard app with prepared context and questions |
| UPDATE | During the meeting | Updated questions, topics, decisions, risks, and follow-ups from transcript chunks |
| CLOSE | After the meeting | Final summary, action items, CRM or notes updates, and optional sanitized export |

## CREATE

Inputs:
- meeting title or contact name
- meeting type, for example discovery, sales, mentoring, support, hiring, partnership
- date
- available context files, if any
- output directory

Create this structure:

```text
YYYY-MM-DD-meeting-copilot/
  app/
    index.html
    app.js
    components.js
    styles.css
    tabs/
      briefing.js
      questions.js
      topics.js
      decisions.js
      followups.js
  state/
    transcript.txt
    diff.py
```

Dashboard tabs:
- `briefing.js`: meeting goal, known context, participants, constraints
- `questions.js`: grouped live questions
- `topics.js`: planned and discussed topics
- `decisions.js`: decisions, risks, blockers, open loops
- `followups.js`: action items, owners, due dates, next message draft

If the app uses ES modules, serve it over HTTP:

```bash
cd YYYY-MM-DD-meeting-copilot/app
python3 -m http.server 8080
```

Then open `http://127.0.0.1:8080`.

## UPDATE

Input is usually a full transcript copied from a transcription tool. Treat it as sensitive.

Use suffix diffing so the agent processes only the new part:

```python
#!/usr/bin/env python3
import pathlib
import sys

baseline = pathlib.Path(__file__).parent / "transcript.txt"
old = baseline.read_text() if baseline.exists() else ""
new = sys.stdin.read()
old_s = old.strip()
new_s = new.strip()

if not old_s:
    sys.stdout.write(new)
elif new_s.startswith(old_s):
    sys.stdout.write(new_s[len(old_s):].lstrip())
else:
    sys.stderr.write("[diff] baseline mismatch; using full transcript\n")
    sys.stdout.write(new)
```

Recommended update flow:

1. Save incoming transcript to `state/transcript-new.txt`.
2. Run `python3 state/diff.py < state/transcript-new.txt > state/delta.txt`.
3. Read `state/delta.txt`.
4. Update only live tabs: `questions.js`, `topics.js`, `decisions.js`, `followups.js`.
5. Move `state/transcript-new.txt` to `state/transcript.txt`.
6. Tell the user what changed and ask them to refresh the dashboard.

Do not update long-term profile or history files during UPDATE unless the user asks. Keep the live loop fast.

## Question Design

Group questions by topic. Avoid one long list.

Use 3 to 6 groups, with 3 to 6 questions per group:

```js
function questionGroup(title, items) {
  if (!items.length) return "";
  return card(title, `<ul>${items.map((item) => `<li>${item}</li>`).join("")}</ul>`);
}
```

Good groups:
- Check-in and goal
- Business context
- Budget, timeline, and constraints
- Decision criteria
- Risks and blockers
- Next steps

Mark critical questions clearly, especially around money, deadlines, authority, legal constraints, and irreversible decisions.

## Topic Map

Track meeting flow as planned, discussed, skipped, or unresolved.

Use a compact visual language:
- filled marker: discussed
- hollow marker: planned but not reached
- warning marker: blocked or risky
- check marker: decided

If using a graph, include only topics, projects, concepts, decisions, and risks. Do not put private participant names into public exports.

## CLOSE

At the end of the meeting:

1. Process the final transcript chunk.
2. Write a concise meeting summary.
3. Extract decisions, action items, owners, deadlines, and open questions.
4. Update the user's chosen system of record, for example CRM, project issue, notes folder, or ticket.
5. Create a follow-up message draft.
6. If requested, create a sanitized export with names, company data, private links, and raw transcript removed.

Close output template:

```markdown
# Meeting Summary

## Outcome

## Decisions

## Action Items

| Item | Owner | Due | Status |
| --- | --- | --- | --- |

## Open Questions

## Follow-up Draft
```

## Privacy Rules

Never put these in public artifacts:
- raw transcript
- private names, emails, handles, phone numbers
- company secrets, pricing, revenue, pipeline data
- private repository paths or URLs
- authentication tokens, meeting links, calendar links
- internal prompts, model names, or routing rules that expose private operations

For public examples, use placeholders:
- `Participant A`
- `Company X`
- `~/workspace/crm`
- `https://example.com/private-doc`

## Quality Bar

Before calling the work done:
- dashboard opens locally
- tabs render without console-breaking syntax errors
- sensitive data is not present in public docs
- close summary has decisions and action items separated
- generated public export is clearly marked as sanitized
