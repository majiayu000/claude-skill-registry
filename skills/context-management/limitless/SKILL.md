---
name: limitless
# prettier-ignore
description: "Use when recalling conversations from Limitless Pendant, finding what was discussed in meetings, searching lifelogs, or answering 'what did I say about' questions"
version: 1.0.0
category: research
triggers:
  - "limitless"
  - "pendant"
  - "lifelogs"
  - "what did I say"
  - "what was discussed"
  - "conversation history"
  - "ambient recording"
---

<objective>
Query your Limitless Pendant's lifelogs - conversations, meetings, and ambient recordings captured by the wearable AI device. Transform "what did I talk about?" into searchable, citable transcripts.
</objective>

<when-to-use>
Use when answering questions about past conversations, finding meeting context, recalling what someone said, searching for topics discussed, or building context from real-world interactions.

Clear triggers:
- "What did I talk about with [person]?"
- "What happened in my meeting yesterday?"
- "Find when I mentioned [topic]"
- "What was that restaurant recommendation?"
</when-to-use>

<prerequisites>
Set `LIMITLESS_API_KEY` environment variable. Get your key from [app.limitless.ai](https://app.limitless.ai) → Settings → Developer.

Optional: Set `LIMITLESS_TIMEZONE` (defaults to America/Chicago).
</prerequisites>

<commands>
```bash
# Recent lifelogs (default: 5)
limitless recent
limitless recent 10

# Today's conversations
limitless today

# Specific date
limitless date 2026-01-28

# Semantic search
limitless search "meeting with john"
limitless search "restaurant recommendation"

# Raw API with custom params
limitless raw "limit=5&isStarred=true"
```
</commands>

<response-format>
Lifelogs include:
- **title** - AI-generated summary
- **markdown** - Full transcript with timestamps
- **startTime/endTime** - When recorded
- **contents** - Structured segments with speaker attribution

Speaker names show as "Unknown" unless voice profiles are trained in the Limitless app.
</response-format>

<api-notes>
- Rate limit: 180 requests/minute
- Requires Limitless Pendant hardware
- Developer portal: [limitless.ai/developers](https://www.limitless.ai/developers)
- API examples: [github.com/limitless-ai-inc/limitless-api-examples](https://github.com/limitless-ai-inc/limitless-api-examples)
</api-notes>

<llm-api-reference>
If you need to look up API details beyond this skill's commands, use Context7:
```
resolve-library-id: limitless → /websites/help_limitless_ai_en
query-docs: /websites/help_limitless_ai_en with "lifelogs API" query
```

Or fetch current docs directly from https://www.limitless.ai/developers
</llm-api-reference>
