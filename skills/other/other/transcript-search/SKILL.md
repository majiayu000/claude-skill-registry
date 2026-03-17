---
name: transcript-search
description: Meeting transcript search from Fireflies.ai and Google Drive. Use this skill when searching for meeting transcripts, finding past client calls, retrieving conversation history, or exporting meeting notes. Triggers on transcript search, meeting history, call recordings, or Fireflies queries.
---

# Transcript Search

## Overview

Search and retrieve meeting transcripts from Fireflies.ai and Google Drive with full text and speaker attribution.

## Quick Decision Tree

```
Where are your transcripts?
│
├── Fireflies.ai (API)
│   └── references/fireflies.md
│   └── Script: scripts/fireflies_transcript_search.py
│
└── Google Drive (uploaded files)
    └── references/drive-transcripts.md
    └── Script: scripts/gdrive_transcript_search.py
```

## Environment Setup

```bash
# For Fireflies
FIREFLIES_API_KEY=your_api_key

# For Google Drive
# OAuth credentials (mycreds.txt) - see google-workspace skill
```

Get Fireflies API key: https://app.fireflies.ai/integrations (Custom Integrations)

## Common Usage

### Search Fireflies by Company
```bash
python scripts/fireflies_transcript_search.py "Microsoft" --days-back 30
```

### Get Full Transcript
```bash
python scripts/fireflies_transcript_search.py --id 01KCM2G0YX1GMPWYQ8GPAABBCK --content
```

### Save Formatted Transcript
```bash
python scripts/fireflies_transcript_search.py --id abc123 --content --save transcript.md
```

### Search Drive Transcripts
```bash
python scripts/gdrive_transcript_search.py "Acme Corp" --days 30
```

## Output Formats

### Search Results
- Transcript ID, title, date, duration
- AI-generated summary, keywords, action items
- Speaker list with names

### Full Transcript
- Complete text with speaker labels
- Timestamps for each sentence
- Formatted markdown output

## Cost

| Service | Cost |
|---------|------|
| Fireflies API | Free (with subscription) |
| Google Drive | Free |

## Security Notes

### Credential Handling
- Store `FIREFLIES_API_KEY` in `.env` file (never commit to git)
- Google OAuth credentials for Drive (see google-workspace skill)
- Regenerate Fireflies API key via Custom Integrations if compromised
- Never log or print API keys in script output

### Data Privacy
- Transcripts contain verbatim meeting conversations
- Speaker names and voices are identifiable
- Business discussions may include confidential information
- Action items and summaries capture sensitive decisions
- Avoid sharing full transcripts without authorization

### Access Scopes
- Fireflies API: Full access to transcripts user has access to
- Google Drive: Access to uploaded transcript files
- Transcripts inherit meeting participants' access permissions

### Compliance Considerations
- **Recording Consent**: Ensure all meeting participants consent to recording
- **Speaker Privacy**: Transcripts identify speakers by name
- **Confidential Meetings**: Some meetings should not be transcribed
- **GDPR**: Meeting recordings containing EU participants require consent
- **Data Retention**: Follow policies for transcript retention/deletion
- **Legal Holds**: Transcripts may be subject to legal discovery
- **Client Confidentiality**: Client meeting content is sensitive
- **Internal Use Only**: Mark transcripts as confidential where appropriate

## Troubleshooting

### Common Issues

#### Issue: Transcript not found
**Symptoms:** "Transcript not found" error with known meeting
**Cause:** Invalid transcript ID, no access, or not yet processed
**Solution:**
- Verify transcript ID from Fireflies dashboard
- Check if recording is still processing (wait and retry)
- Ensure API key has access to the transcript
- Confirm meeting was actually recorded and transcribed

#### Issue: API unauthorized
**Symptoms:** 401 error or "invalid API key"
**Cause:** API key expired, invalid, or not set
**Solution:**
- Regenerate API key at https://app.fireflies.ai/integrations
- Verify `FIREFLIES_API_KEY` is set correctly in `.env`
- Check for leading/trailing whitespace in key
- Ensure Custom Integration is enabled in Fireflies

#### Issue: Empty search results
**Symptoms:** Search returns no transcripts despite existing meetings
**Cause:** Search query too narrow, date range issue, or access restrictions
**Solution:**
- Broaden search query (fewer keywords)
- Expand date range with `--days-back` parameter
- Check if transcripts are shared with your account
- Verify search is using correct field (title, participants, content)

#### Issue: Missing transcript content
**Symptoms:** Metadata returned but full content is empty
**Cause:** Transcript still processing or content access restricted
**Solution:**
- Wait for transcript processing to complete (check Fireflies dashboard)
- Use `--content` flag explicitly to request full transcript
- Verify subscription tier includes API content access
- Check if transcript has processing errors

#### Issue: Speaker attribution missing
**Symptoms:** Transcript text present but speakers not identified
**Cause:** Low audio quality or speakers not enrolled
**Solution:**
- Speaker identification depends on audio quality
- Enroll frequent speakers in Fireflies for better recognition
- This is a Fireflies processing issue, not API issue
- Re-upload recording if possible with better audio

#### Issue: Google Drive transcript search fails
**Symptoms:** Can't find transcripts stored in Drive
**Cause:** OAuth issue, folder structure, or file format
**Solution:**
- Verify Google OAuth is working (see google-workspace skill)
- Check transcripts are in searchable folder
- Ensure transcripts are in readable format (txt, md, docx)
- Search by exact filename if full-text search fails

## Resources

- **references/fireflies.md** - Fireflies.ai API guide
- **references/drive-transcripts.md** - Drive transcript search

## Integration Patterns

### Transcript to Summary
**Skills:** transcript-search → content-generation
**Use case:** Create meeting summaries and action item docs
**Flow:**
1. Retrieve full transcript from Fireflies
2. Extract key discussion points and decisions
3. Generate formatted summary document via content-generation

### Transcript to Voice Agent
**Skills:** transcript-search → voice-agents
**Use case:** Build context-aware voice agents
**Flow:**
1. Search for past meetings with client
2. Extract relationship history and previous discussions
3. Include context in voice agent prompt for personalized calls

### Transcript to CRM
**Skills:** transcript-search → attio-crm
**Use case:** Add meeting notes to CRM records
**Flow:**
1. Search transcripts for client meetings
2. Extract summary, action items, and key quotes
3. Create note on Attio company record with meeting details
