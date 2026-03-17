---
id: posthog-marketing-analytics
name: PostHog Marketing Analytics
description: Funnel analysis, campaign attribution, conversion tracking
role: marketing
requiredTools:
  - type: mcpService
    serviceType: posthog
---

## PostHog Marketing Analytics

When analyzing marketing data:

- Use **posthog_list_events** and **posthog_list_persons** (tool names may have a suffix if multiple PostHog servers exist) to trace user journeys and conversion funnels.
- Prefer **posthog_list_insights** / **posthog_get_insight** over raw events when answering funnel or retention questions.
- When comparing campaigns, use distinctId and event filters in **posthog_list_events** for attribution.
- Always specify projectId; call **posthog_list_projects** first if unknown.
- For conversion funnels, list events with relevant filters (event names, time range) then summarize steps and drop-off.
- When asked about retention, use persons and events to identify returning users and cohort behavior.

## Step-by-step instructions

1. If projectId is unknown, call **posthog_list_projects** and pick the relevant one.
2. For funnel questions: identify the event sequence (e.g. signup → trial_start → paid), call **posthog_list_events** with projectId, event filter, and after/before; summarize steps and drop-off rates.
3. For attribution or campaigns: use **posthog_list_events** with distinctId and event filters to relate events to campaigns; summarize by campaign or source.
4. For retention: use **posthog_list_persons** and **posthog_list_events** to count returning users and cohort behavior over time.
5. Prefer **posthog_list_insights** / **posthog_get_insight** when available; otherwise cite filters and time range used.

## Examples of inputs and outputs

- **Input**: “What’s our signup-to-paid funnel look like this month?”  
  **Output**: Short summary: event names per step, counts or rates, main drop-off step; mention projectId and date range used.

- **Input**: “Which campaign drove the most signups?”  
  **Output**: Ranked list or table (campaign/source, signup count or share) with attribution from event properties; cite query filters.

## Common edge cases

- **No projectId**: Call **posthog_list_projects** first and ask the user which one, or use the default if only one.
- **No events in range**: Report “No events in this period” and suggest a wider range or different events.
- **Ambiguous event names**: List available events or ask the user to confirm event names before building the funnel.
- **Rate limits or errors**: Tell the user the request hit a limit or failed and suggest narrowing the range or retrying later.

## Tool usage for specific purposes

- **posthog_list_events**: Use to query events with projectId, event name, after/before, distinctId, personId for funnels, counts, and attribution. Always include a sensible time range.
- **posthog_list_persons** / **posthog_get_person**: Use for retention and cohort-style questions; relate to events via distinct_id.
- **posthog_list_insights** / **posthog_get_insight**: Use when they support funnel or retention answers.
