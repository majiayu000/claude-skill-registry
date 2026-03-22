---
name: search
description: This skill should be used when the user asks to "search email", "find email", "look for email", "email from", "email about", or wants to locate specific messages. Searches by keyword, sender, flags, or date using himalaya filter syntax.
triggers:
  - search email
  - find email
  - look for email
  - email from
  - email about
---

# /email:search - Search Emails

Search your email using himalaya's filter syntax with a friendly interface.

## Usage

```
/email:search meeting            # Search by keyword (subject/body)
/email:search from:alice         # Search by sender
/email:search --unread           # Only unread messages
/email:search --flagged          # Only starred/flagged messages
/email:search from:boss meeting  # Combine sender + keyword
```

## When Invoked

1. Parse the user's query into himalaya filter syntax:
   - Plain keyword → `subject <keyword> or body <keyword>`
   - `from:<sender>` → `from <sender>`
   - `to:<recipient>` → `to <recipient>`
   - `--unread` → `not flag Seen`
   - `--flagged` → `flag Flagged`
   - Date hints ("last week", "yesterday") → `after <date>`
   - Combine with `and`/`or` as appropriate
2. Call `search_emails` MCP tool with the constructed query
3. Format results as a table
4. Offer follow-up actions

## Output Format

```
🔍 Search: "from alice meeting" (5 results)

| # | From | Subject | Date | Flags |
|---|------|---------|------|-------|
| 1 | alice@co | Q2 planning meeting | Feb 24 | ⭐ |
| 2 | alice@co | Meeting notes | Feb 20 | |
| 3 | alice@co | Re: Team meeting | Feb 18 | ✓ |
| 4 | alice@co | Meeting agenda | Feb 15 | |
| 5 | alice@co | Meeting request | Feb 10 | ✓ |

→ "Read #1" to view full email
→ "Refine: after Feb 20" to narrow results
→ "/email:triage" to classify these results
```

## No Results

If no results are found, suggest alternatives:

```
🔍 No results for "from alice invoice"

Try:
→ Broader search: "invoice" (remove sender filter)
→ Different folder: "search invoice in Sent"
→ Check spelling: did you mean "alice@company.com"?
```
