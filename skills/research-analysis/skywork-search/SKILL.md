---
name: Skywork Search
description: Search the web for real-time information using the Skywork web search API. Use this skill whenever the user needs up-to-date information from the internet — for example, researching a topic, looking up recent events, finding facts or statistics, gathering material for a document or presentation, or answering questions that require current data. Also trigger when the user says things like "search for", "look up", "find information about", "what's the latest on", or any request that implies needing information beyond your training data.
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# Web Search Skill

Search the web for real-time information via the Skywork search API. This skill lets you run up to 3 queries in a single invocation and returns structured results with source URLs and content snippets.

## When to use

- The user asks you to research a topic or find current information
- You need up-to-date facts, statistics, or news to answer a question
- Another task (writing a report, creating a PPT, drafting a document) needs web research as a preliminary step
- The user explicitly asks to search or look something up

## Authentication (Required First)

Before using this skill, authentication must be completed. Run the auth script first:

```bash
# Authenticate: checks env token / cached token / browser login
python3 <skill-dir>/scripts/skywork_auth.py || exit 1
```

**Token priority**:
1. Environment variable `SKYBOT_TOKEN` → if set, use directly
2. Cached token file `~/.skywork_token` → validate via API, if valid, use it
3. No valid token → opens browser for login, polls until complete, saves token

**IMPORTANT - Login URL handling**: If script output contains a line starting with `[LOGIN_URL]`, you **MUST** immediately send that URL to the user in a clickable message (e.g. "Please open this link to log in: <url>"). The user may be in an environment where the browser cannot open automatically, so always surface the login URL.

## How to use

Run the bundled script from this skill's `scripts/` directory:

```bash
python3 <skill-path>/scripts/web_search.py "query1" ["query2"] ["query3"]
```

- Pass 1–3 search queries as positional arguments
- Results are saved to individual text files in a temporary directory
- The script prints the file paths to stdout so you can read them

## Crafting good queries

Search quality depends heavily on query phrasing. A few tips:

- **Be specific**: "Tesla Q4 2025 revenue" works better than "Tesla financials"
- **Use natural language**: The API handles full questions well — "What is the current population of Tokyo?" is fine
- **Split broad topics**: If the user wants a comprehensive overview, break it into 2–3 focused queries rather than one vague one
- **Include time context** when relevant: "best Python web frameworks 2026" rather than just "best Python web frameworks"

## Reading results

After running the script, read the output files. Each file contains:

```
query: <the original query>

[result-1] <source URL>
<content snippet>

[result-2] <source URL>
<content snippet>
...
```

Synthesize the results into a clear answer for the user. Always cite sources when presenting factual information — include the URLs from the results so the user can verify.

## Example workflow

User asks: "What are the latest developments in quantum computing?"

1. Run the search with focused queries:
   ```bash
   python3 <skill-path>/scripts/web_search.py \
     "quantum computing breakthroughs 2026" \
     "quantum computing industry news latest"
   ```
2. Read the result files
3. Synthesize findings into a clear, sourced summary for the user

## Limitations

- Maximum 3 queries per invocation (the script caps it)
- Each query has a 30-second timeout
- Results depend on the Skywork search API availability
