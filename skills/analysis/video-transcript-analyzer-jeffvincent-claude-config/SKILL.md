---
name: Video Transcript Analyzer
description: Analyze customer interview transcripts (SRT or plain text) to generate thematic breakdowns with summary, quotes, topics, timestamps, and full transcript. Use when given video transcripts or asked to create chapter markers.
version: 1.0.0
allowed-tools: [Read, Write]
---

# Video Transcript Analyzer

## Overview
This Skill analyzes video transcripts from customer interviews, user research sessions, or feedback calls and produces a comprehensive structured document with thematic analysis, key insights, chapter markers (if timestamps available), and the complete original transcript.

## When to Apply
Use this Skill when:
- User provides a video transcript file (.srt or .txt)
- User asks to "analyze this customer call/interview"
- User requests "chapter markers" or "topical breakdown" from a transcript
- User wants to extract insights from a recorded conversation
- User provides a transcript and asks for a summary or key themes

Do NOT use this Skill for:
- General text summarization (not conversation transcripts)
- Meeting notes that aren't transcripts
- Live conversations (only recorded/transcribed ones)

## Inputs
1. **Transcript file** - Either:
   - SRT format (with timestamps like `00:05:30,120 --> 00:05:33,450`)
   - Plain text format (dialogue without timestamps)
2. **Video URL** (optional) - Link to hosted video file if provided
3. **Context** (optional) - What the call/interview was about, participant names if not clear

## Outputs
A single comprehensive markdown document containing:
1. **Video Link** - If provided by user
2. **Call Summary** - 2-3 paragraph overview
3. **Key Quotes** - 5-8 verbatim customer quotes highlighting important points
4. **Topical Breakdown** - Thematic analysis with:
   - Timestamps (if SRT format)
   - Topic headers with brief descriptions
   - Detailed context bullets for each topic
5. **Full Transcript** - Complete original transcript at the end

## Instructions for Claude

### Step 1: Detect Format and Extract Information
- Read the provided transcript file
- Determine if it's SRT format (has timestamps) or plain text
- If SRT, parse timestamps and dialogue
- Check if video URL was provided in the user's message or context
- If NO video URL found, prompt the user: "Do you have a link to the video recording? If so, please share it and I'll include it in the analysis."
- Wait for user response before proceeding
- Identify participants (interviewer vs customer/interviewee)
- Extract customer and company information from context or prompt user:
  - "What is the customer's first name?" (e.g., Emma, Martin, Sarah)
  - "What is the customer's last name (or press Enter to skip)?" (e.g., McKenna, Jones)
  - "What is the company name?" (e.g., HubSpot, Acme, TechCorp)
- Generate output filename based on what's available:
  - If last name provided: `YYYY-MM-DD_FirstName_LastName_CompanyName.md`
  - If no last name: `YYYY-MM-DD_FirstName_CompanyName.md`
  - YYYY-MM-DD is today's date

### Step 2: Analyze Conversation Themes
- Read through the entire conversation
- Identify 5-10 major topics or themes discussed
- Look for:
  - Pain points and problems mentioned
  - Feature requests or desired functionality
  - Workflow impacts and efficiency issues
  - Perception or sentiment changes
  - Specific examples or demonstrations
  - Business impact statements
- Group related discussions thematically (not just chronologically)

### Step 3: Extract Verbatim Quotes
- Select 5-8 powerful, representative quotes from the customer/interviewee
- Keep quotes EXACTLY as spoken - do not paraphrase or clean up
- Choose quotes that:
  - Highlight key pain points
  - Show emotional impact or urgency
  - Provide specific examples
  - Reveal perception or sentiment
  - Demonstrate business impact
- Include brief context for each quote if needed

### Step 4: Write Call Summary
- Write 2-3 paragraphs summarizing:
  - Who was on the call and their role
  - What was discussed at high level
  - Main themes that emerged
  - Key outcomes or next steps
- Keep it concise but informative

### Step 5: Build Topical Breakdown
For **SRT transcripts** (with timestamps):
- Create chapter markers with timestamps for each major topic
- Use the timestamp where that topic begins
- Format: `**HH:MM:SS - Topic Title**`
- Under each topic, add:
  - One-line description of what's covered
  - 3-6 detailed bullet points with specific context
  - Include sub-issues, examples mentioned, impact described

For **Plain text transcripts** (no timestamps):
- Create topic sections without timestamps
- Format: `## Topic #: Topic Title`
- Same detailed structure as SRT version

### Step 6: Assemble Final Document
Create a single markdown document with this structure.

**Output filename format:**
- With last name: `YYYY-MM-DD_FirstName_LastName_CompanyName.md`
  - Example: `2025-11-15_Martin_McKenna_HubSpot.md`
- Without last name: `YYYY-MM-DD_FirstName_CompanyName.md`
  - Example: `2025-11-11_Emma_Ax.md`

Rules:
- Use today's date for YYYY-MM-DD
- Include last name only if provided (skip if not available)
- Use company name only (no legal entity suffix)
- Use underscores between all parts

```markdown
# [Call/Interview Title]

## Video
[Video URL if provided, or "Not provided"]

## Call Summary
[2-3 paragraph summary]

## Key Quotes
> "[Quote 1]"
>
> — [Speaker, context if needed]

> "[Quote 2]"
>
> — [Speaker, context if needed]

[Continue for 5-8 quotes]

## Topical Breakdown

**00:05:30 - Topic Title** [if SRT]
OR
## Topic #1: Topic Title [if plain text]

Brief description of what this section covers.

- Detailed bullet point about specific issue mentioned
- Another bullet with context and examples
- Impact or consequence described
- Related sub-issues or concerns
[3-6 bullets per topic]

[Repeat for all major topics]

## Full Transcript

[Complete original transcript - preserve exact formatting]
- If SRT: include timestamps and dialogue exactly as provided
- If plain text: include exactly as provided
```

### Step 7: Quality Checks
- Verify all quotes are verbatim (no paraphrasing)
- Ensure timestamps are accurate (if SRT)
- Check that topics are thematically organized
- Confirm full transcript is included at the end
- Validate video link is included (if provided)

## Examples

### Example 1: SRT Input (with last name)
**User provides:** `customer-feedback-call.srt` file and says "Here's the recording: https://vimeo.com/example123"

**Claude prompts for:**
- First name: Martin
- Last name: McKenna
- Company name: HubSpot

**Output filename:** `2025-11-15_Martin_McKenna_HubSpot.md`

**Output includes:**
```markdown
# Customer Feedback Call - Martin McKenna (Product Manager at HubSpot)

## Video
https://vimeo.com/example123

## Call Summary
Emma, the main HubSpot admin at AX for 4 years, discussed several critical pain points...
[2-3 paragraphs]

## Key Quotes
> "I had it was a proper panic moment for me, because we had our biggest dealer group about to resend. We were on a timeline for their campaign. And there was nothing like, I was completely powerless."
>
> — Emma, on being blocked by support limitations

[4-7 more quotes]

## Topical Breakdown

**00:02:57 - Memberships & Registration Management**
Cannot bulk manage registration emails for large membership lists.

- Must manually resend registration emails one by one to 2,000+ members
- Search functionality constantly refreshes while typing, making it difficult to use
- Requires HubSpot support intervention for "hard resets" of properties
- No ability to filter membership lists or create segments from membership data

**00:09:41 - Lists vs Views Disconnect**
[Continue...]

## Full Transcript
1
00:00:00,000 --> 00:00:03,300
Hi, Emma. Hi, how are you, Hannah?
[Complete transcript...]
```

### Example 1b: SRT Input (no last name)
**User provides:** `emma-interview.srt` file

**Claude prompts for:**
- First name: Emma
- Last name: [user presses Enter to skip]
- Company name: Ax

**Output filename:** `2025-11-11_Emma_Ax.md`

**Output includes:**
```markdown
# Customer Feedback Call - Emma (HubSpot Admin at Ax)

## Video
Not provided

## Call Summary
Emma is the main HubSpot admin at Ax, where she's worked for 4 years...
[2-3 paragraphs]

## Key Quotes
> "I had it was a proper panic moment for me..."
>
> — Emma, on being blocked by support limitations

[4-7 more quotes]

## Topical Breakdown
[Topics with timestamps and details]

## Full Transcript
[Complete transcript...]
```

### Example 2: Plain Text Input
**User provides:** Plain text transcript, no video link

**Output includes:**
```markdown
# Product Feedback Interview

## Video
Not provided

## Call Summary
[Summary content]

## Key Quotes
[Quotes content]

## Topical Breakdown

## Topic #1: Onboarding Complexity
New users struggle with initial setup and configuration.

- Users report spending 2-3 hours on first-time setup
- Lack of guided workflow causes confusion about next steps
[Continue...]

## Full Transcript
Interviewer: Thanks for joining today. Can you tell me about...
[Complete transcript...]
```

## Testing Checklist
- [ ] Correctly detects SRT vs plain text format
- [ ] Extracts and formats timestamps accurately (if SRT)
- [ ] Includes video link in output (if provided)
- [ ] Call summary is 2-3 paragraphs and informative
- [ ] 5-8 key quotes included, all verbatim (not paraphrased)
- [ ] Topics are thematically organized, not just chronological
- [ ] Each topic has descriptive title and 3-6 context bullets
- [ ] Full original transcript included at end
- [ ] Output is single, well-formatted markdown document
- [ ] No customer information redacted unless requested

## Security and Privacy
- Handle customer names and company information with care
- If transcript contains sensitive data (credentials, PII beyond names), warn user before processing
- Do not modify or sanitize quotes unless explicitly requested
- Preserve all content from original transcript in the full transcript section

## Related Skills (Workflow Chain)

This skill is part of the **video processing workflow**:

```
┌─────────────────────┐
│   wistia-uploader   │  → Upload video, get transcript
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────┐
│  video-transcript-analyzer  │  ← YOU ARE HERE
│  (analyze transcript)       │
└──────────┬──────────────────┘
           │
     ┌─────┴─────┐
     ▼           ▼
┌──────────┐ ┌───────────────────────────┐
│  video-  │ │ interview-synthesis-      │
│  clipper │ │ updater                   │
│ (clips)  │ │ (update synthesis docs)   │
└──────────┘ └───────────────────────────┘
```

**Preceding skill:** `wistia-uploader` - If user has a video file, upload to Wistia first to get automatic transcription

**Following skills:**
- `video-clipper` - Create video clips from the chapter timestamps in the Topical Breakdown
- `interview-synthesis-updater` - Automatically updates synthesis documents after this analysis completes
