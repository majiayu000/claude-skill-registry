---
context: current
model: sonnet
description: Record meetings with voice transcription and create meeting notes
---

# /voice-meeting

Record a meeting using voice capture and automatically create a meeting note with transcript.

## Usage

```
/voice-meeting start <title>
/voice-meeting start <title> for <project>
/voice-meeting stop
/voice-meeting status
```

## Examples

```
/voice-meeting start Weekly Team Sync
/voice-meeting start Architecture Review for Project - Alpha
/voice-meeting stop
/voice-meeting status
```

## Prerequisites

Before using this skill, ensure:

1. The Inworld voice-agent server is running at `ws://localhost:4000`
2. Start it with: `cd ~/Documents/GitHub/claude-voice && npm run start:server`
3. Microphone permissions are granted

## Instructions

### For `start` action:

1. Parse the command for:
   - **title**: Meeting name (required)
   - **project**: Project mentioned after "for" (optional)

2. Use the `voice_listen_continuous` MCP tool with action "start":

   ```
   mcp__voice-mcp__voice_listen_continuous({
     action: "start",
     title: "<meeting title>"
   })
   ```

3. Store the session_id returned for later use

4. Inform the user:
   - Recording has started
   - Remind them to say `/voice-meeting stop` when finished
   - Mention they can check status with `/voice-meeting status`

### For `stop` action:

1. Use the `voice_listen_continuous` MCP tool with action "stop":

   ```
   mcp__voice-mcp__voice_listen_continuous({
     action: "stop"
   })
   ```

2. Retrieve the full transcript and segments from the response

3. Generate filename: `Meeting - YYYY-MM-DD {{title}}.md`

4. Create the meeting note in **Meetings/** folder:

```markdown
---
type: Meeting
title: { { title } }
created: { { DATE } }
modified: { { DATE } }
tags: [voice-recorded]
date: "{{DATE}}"
project: { { project_link or null } }
attendees: []
summary: { { AI-generated summary of transcript } }
collections: null
recordingSession: { { session_id } }
duration: { { duration_ms formatted as HH:MM:SS } }
wordCount: { { word_count } }
---

# {{title}}

## Recording Info

- **Session ID**: {{session_id}}
- **Duration**: {{duration formatted}}
- **Word Count**: {{word_count}}

## Attendees

(To be filled in)

## Transcript

{{full_transcript}}

## AI Summary

{{Generate 3-5 bullet point summary of the meeting}}

## Action Items

{{Extract any action items mentioned in transcript, or leave template:}}

- [ ]

## Decisions Made

## {{Extract any decisions mentioned, or leave template:}}

## Follow-up

-
```

5. After creating, confirm and show:
   - File path
   - Meeting duration
   - Word count
   - Brief transcript preview

### For `status` action:

1. Use the `voice_listen_continuous` MCP tool with action "status":

   ```
   mcp__voice-mcp__voice_listen_continuous({
     action: "status"
   })
   ```

2. Report:
   - Whether recording is active
   - Session ID
   - Current duration
   - Word count so far
   - Transcript preview (last 500 chars)

## Error Handling

- If no Inworld server connection: Remind user to start the voice-agent server
- If stop called with no active session: Inform user no recording is active
- If recording fails: Provide helpful error message and suggest checking microphone

## Notes

- Recording automatically includes VAD (Voice Activity Detection)
- Maximum recording duration is 1 hour (configurable)
- Transcripts are stored in the session until `stop` is called
