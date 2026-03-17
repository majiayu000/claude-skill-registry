---
id: memory-context-recall
name: Memory Context Recall
description: Recall past conversations and facts from agent memory
role: other
requiredTools:
  - type: builtin
    tool: search_memory
---

## Memory Context Recall

When the user asks to remember past conversations or facts:

- Use **search_memory** with a suitable grain (working, daily, weekly, monthly, quarterly, yearly) and optional **queryText** for semantic search.
- Use **minimumDaysAgo** and **maximumDaysAgo** to bound the time window (e.g. "last week" = maximumDaysAgo 7, minimumDaysAgo 0).
- Synthesize recalled events into context before answering; cite that the answer is based on prior context when relevant.
- Prefer **working** grain for "our last conversation" or recent context; use **daily** or **weekly** for broader recall.
- When no **queryText** is provided, the tool returns most recent events for the grain and time range.

## Step-by-step instructions

1. Interpret the user's time intent: "last conversation" -> working, 0-1 days; "last week" -> daily or weekly, maximumDaysAgo 7; "last month" -> weekly or monthly, maximumDaysAgo 30.
2. Call **search_memory** with grain, minimumDaysAgo, maximumDaysAgo, and optionally queryText (for semantic match) and maxResults (default 10, max 100).
3. Read the returned events (prefixed by date when available) and extract relevant facts or prior decisions.
4. Answer the user's question using the recalled context; say "Based on our previous conversation..." or "From what we discussed..." when appropriate.
5. If nothing relevant is found, say so and suggest rephrasing the time range or query.

## Examples of inputs and outputs

- **Input**: "What did we decide about the API design last time?"  
  **Output**: Short summary of the relevant prior decision from **search_memory** (grain=working or daily, queryText="API design" or no queryText with recent range); cite that it's from a prior conversation.

- **Input**: "Do you remember the budget number we discussed?"  
  **Output**: The budget value if found in **search_memory** (e.g. grain=working, queryText="budget"); if not found, "I don't have that in memory for that period."

## Common edge cases

- **No results**: Say "I couldn't find anything in memory for that period/topic" and suggest widening the time range or trying a different query.
- **Ambiguous time range**: If the user says "a while ago", use a broad range (e.g. maximumDaysAgo 90) and optionally queryText; summarize what you find.
- **Too many results**: Use maxResults (e.g. 10-20) and summarize the most relevant; mention that more may exist.
- **queryText vs no queryText**: Use queryText for topic-specific recall; omit it for "what happened in the last N days" style requests.

## Tool usage for specific purposes

- **search_memory (grain=working)**: Use for "last conversation", "recently", or most recent events.
- **search_memory (grain=daily/weekly/monthly)**: Use for "last week", "this month", or summarized recall over longer periods.
- **search_memory (queryText)**: Use when the user asks about a specific topic or fact to search semantically.
- **minimumDaysAgo / maximumDaysAgo**: Use to narrow the window (e.g. last 7 days: maximumDaysAgo 7, minimumDaysAgo 0).
