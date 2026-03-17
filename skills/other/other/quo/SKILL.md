---
name: quo
version: 0.2.0
description:
  Query and interact with Quo business phone - calls, texts, contacts, transcripts, send
  SMS
triggers:
  - quo
  - openphone
  - business phone
  - work calls
  - call transcript
  - call summary
metadata:
  openclaw:
    emoji: "📞"
    apiKey:
      env: QUO_API_KEY
      getFrom: https://my.quo.com → Settings → API
---

# Quo 📞

Query your Quo (formerly OpenPhone) business phone — calls, texts, contacts,
transcripts.

## Setup

API key from my.quo.com → Settings → API. Configure via gateway.

## What Users Ask

- "What's my Quo number?"
- "Show recent conversations"
- "Get the transcript from that call"
- "What was the summary of my call with [person]?"
- "List my business contacts"
- "Send a text to [number]"
- "Show my recent calls with [number]"

## Capabilities

- List phone numbers
- Recent conversations (calls + texts)
- Contacts and workspace users
- Call summaries and transcripts
- Recording URLs
- Send SMS messages
- List messages/calls with specific participants

## Response Data

**Conversations:**

- `id` — Conversation ID
- `name` — Contact name if known
- `participants` — Phone numbers
- `lastActivityAt` — Most recent activity

**Transcripts/Summaries:**

- AI-generated summary
- Full transcript with timestamps
- Speaker attribution when available

## Notes

- Transcripts require call recording enabled in Quo settings
- Phone numbers in E.164 format (+1XXXXXXXXXX)
