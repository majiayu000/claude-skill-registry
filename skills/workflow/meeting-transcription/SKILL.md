---
name: meeting-transcription
description: Transcribe meeting audio with speaker diarization, generate structured summaries with action items, decisions, and follow-ups, and support multiple audio formats and languages. Use when the user requests meeting transcription or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# Meeting Transcription

This skill enables an AI agent to process meeting audio recordings into structured, actionable documents. The agent handles the full pipeline from raw audio input through speaker diarization, transcription, and intelligent summarization. The output includes a timestamped transcript with speaker labels, a concise summary of key discussion points, a list of decisions made, and clearly assigned action items with owners and deadlines.

## Workflow

1. **Ingest and validate the audio input.** Accept the meeting audio file and verify it is in a supported format: MP3, WAV, M4A, FLAC, OGG, or WebM. Check the file size, duration, and channel count (mono vs. stereo). If the audio is in a non-standard format, convert it to WAV 16kHz mono using FFmpeg or a similar preprocessing tool. Log the file metadata (duration, sample rate, codec) for downstream reference.

2. **Preprocess the audio for quality.** Apply noise reduction to suppress background hum, keyboard clicks, and room echo. Normalize audio levels across the recording so that quiet speakers are boosted and loud segments are attenuated. If the recording has multiple channels (e.g., a stereo podcast), split channels where each maps to a known speaker. Flag sections with very low signal-to-noise ratio as potentially unreliable.

3. **Perform speaker diarization.** Identify and label distinct speakers throughout the recording. Use voiceprint clustering to distinguish speakers even when they interrupt each other or speak in quick succession. Assign temporary labels (Speaker 1, Speaker 2, etc.) by default, and allow the user to provide a name mapping either before or after processing. Handle overlapping speech by attributing the segment to the dominant speaker and noting the overlap.

4. **Transcribe the audio to text.** Run the preprocessed, diarized audio through a speech-to-text engine (e.g., Whisper, Deepgram, Google Speech-to-Text). Produce a word-level or segment-level transcript with timestamps. Apply punctuation restoration and capitalization correction. For multi-language meetings, detect language switches and transcribe each segment in its original language, optionally providing inline translations.

5. **Generate the structured summary.** Analyze the full transcript to extract key discussion topics, decisions made, open questions, and action items. Group related discussion segments into thematic sections. For each action item, identify the owner (by speaker label or name), the task description, and any mentioned deadline. Produce a summary document with clearly delineated sections: Overview, Key Discussion Points, Decisions, Action Items, and Follow-ups.

6. **Format and deliver the output.** Produce the final output in the requested format: Markdown, JSON, or plain text. Include both the full timestamped transcript and the structured summary as separate sections or files. If calendar integration is enabled, cross-reference the meeting with calendar event data to auto-populate the meeting title, attendee list, and agenda in the output header.

## Usage

Provide the agent with the path to an audio file and optionally a speaker name mapping, output format preference, and language hint. The agent returns a full transcript and a structured summary.

**Prompt format:**

~~~
Transcribe and summarize the meeting recording.
Audio file: [path or URL to audio file]
Speakers: [optional name mapping, e.g., "Speaker 1 = Priya, Speaker 2 = James"]
Language: [primary language, e.g., English]
Output format: [markdown / json / text]
~~~

## Examples

### Example 1: Timestamped Transcript with Speaker Labels

**Input:**

~~~
Transcribe the meeting at /recordings/sprint-planning-2026-02-10.m4a
Speakers: Speaker 1 = Priya, Speaker 2 = James, Speaker 3 = Dana
Output format: markdown
~~~

**Output (transcript excerpt):**

~~~markdown
# Sprint Planning — February 10, 2026

Attendees: Priya (Engineering Lead), James (Product Manager), Dana (Designer)
Duration: 34 minutes

---

[00:00:12] Priya: Alright, let's kick off sprint planning. James, can you
walk us through the priorities for this sprint?

[00:00:18] James: Sure. The top item is the checkout flow redesign. We got
feedback from the beta group that the three-step process is causing drop-off
at step two. Dana, you had some mockups ready?

[00:00:31] Dana: Yes, I've simplified it to a single-page layout. The address
and payment fields are on the same screen now with a collapsible order summary
on the right. I'll share the Figma link after this call.

[00:00:48] Priya: That sounds good. How much engineering effort are we looking
at? I'm thinking this is a two-sprint task if we include the backend changes
for the new validation logic.

[00:01:02] James: Can we scope it so the frontend ships this sprint and the
backend validation follows in the next one?

[00:01:10] Priya: That works. We can use client-side validation as a stopgap.
I'll create the tickets after this meeting.

[00:01:22] James: Great. Second priority is the analytics event tracking.
We're missing conversion events on the pricing page.

[00:01:35] Dana: No design implications there. It's purely instrumentation.
No UI changes needed.
~~~

### Example 2: Structured Summary with Action Items

**Output (summary for the same meeting):**

~~~markdown
## Meeting Summary

### Overview
The sprint planning session covered three topics: the checkout flow redesign,
analytics event tracking for the pricing page, and an update on the mobile
onboarding experiment. The team agreed to split the checkout work across two
sprints and prioritize the analytics instrumentation for immediate deployment.

### Key Discussion Points
- **Checkout flow redesign:** Beta feedback indicates 35% drop-off at step 2.
  Dana presented a single-page layout. The team agreed on a phased rollout:
  frontend this sprint, backend validation next sprint.
- **Analytics event tracking:** Conversion events are missing on the pricing
  page. No design changes required. Estimated at 3 story points.
- **Mobile onboarding experiment:** A/B test results not yet significant.
  The team will extend the experiment by one week.

### Decisions
1. Checkout redesign split: frontend in Sprint 14, backend in Sprint 15.
2. Client-side validation will serve as a temporary stopgap.
3. Analytics instrumentation ships this sprint with no design dependency.
4. Mobile onboarding experiment extended by one week.

### Action Items
| Owner | Task                                              | Deadline  |
|-------|---------------------------------------------------|-----------|
| Priya | Create Jira tickets for checkout frontend work    | Feb 10    |
| Dana  | Share Figma link for single-page checkout mockup  | Feb 10    |
| Priya | Estimate backend validation effort for Sprint 15  | Feb 12    |
| James | Write analytics event spec for pricing page       | Feb 11    |
| James | Schedule decision review for mobile onboarding    | Feb 17    |

### Follow-ups
- Priya to sync with the backend team on API contract changes.
- Dana to run a usability test on the single-page layout with 3 users.
- James to share the A/B test dashboard link in Slack for monitoring.
~~~

## Best Practices

- **Use stereo or multi-channel recording when possible.** Separate audio channels per speaker dramatically improve diarization accuracy. Encourage teams to use meeting platforms that support per-participant audio tracks.
- **Provide speaker name mappings upfront.** Pre-mapping speaker identities avoids manual relabeling after transcription and enables richer summaries with named action item owners.
- **Review low-confidence segments.** Flag transcript segments where the speech-to-text confidence score is below 0.7 for human review. These often correspond to crosstalk, mumbling, or heavy accents.
- **Keep summaries to one page.** A good summary is shorter than the transcript, not a restatement of it. Focus on decisions and action items — the transcript exists for anyone who needs full detail.
- **Separate transcript from summary in the output.** Users have different needs: some want the full record, others just want action items. Deliver both as distinct sections or files.
- **Integrate with calendar metadata.** When the agent has access to calendar events, auto-populate the meeting title, attendee list, and agenda to reduce manual input and enrich the output header.

## Edge Cases

- **Overlapping speech and crosstalk.** When multiple people speak simultaneously, attribute the segment to the loudest speaker and add an annotation like `[crosstalk]`. Avoid silently dropping content.
- **Non-English or mixed-language meetings.** Detect language switches mid-conversation using language identification models. Transcribe each segment in its source language and optionally provide an inline English translation in brackets.
- **Poor audio quality.** If signal-to-noise ratio is very low (e.g., phone recordings in noisy environments), warn the user that transcript accuracy may be degraded and highlight uncertain passages with `[inaudible]` markers.
- **Very long meetings (2+ hours).** For extended recordings, process in chunks to avoid memory issues. Generate section-level summaries as well as an overall summary to help users navigate the content.
- **Confidential or sensitive content.** If the transcript contains personally identifiable information, financial data, or legal discussions, flag the output for restricted access and apply redaction rules if configured.
