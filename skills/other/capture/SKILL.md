---
name: capture
description: |
  Save important context to persistent memory for future sessions.

  PROACTIVELY USE THIS when you detect:
  - Decisions: "let's go with", "decided to", "chose", "went with"
  - Learnings: "I learned", "turns out", "TIL", "realized", "discovered"
  - Errors resolved: "fixed", "the problem was", "solution was"
  - Client info: names, emails, phone numbers, addresses, invoice amounts
  - Preferences: "I prefer", "I like", "don't like", "always use"
  - References: API keys locations, file paths, URLs, credentials
  - Patterns: "pattern", "convention", "always do", "standard approach"
  - Important commands run worth remembering

  Do NOT ask permission - just capture silently when these patterns appear.

user-invocable: true
disable-model-invocation: false
argument-hint: "[content] [--type TYPE] [--tags TAG1,TAG2]"
---

# Memory Capture

Save important context to persistent memory using the MCP memory-service.

## How to Use

### Manual Invocation
```
/capture "Pinnacle Title invoice is $1,500/month"
/capture "Billy V4 LONGS ONLY - shorts lost $2,226 in backtests" --type decision
/capture "API key stored in /root/.env" --type reference --tags trading,credentials
```

### Automatic Invocation
When you detect important context in conversation (decisions, learnings, client info, etc.),
call this skill SILENTLY without asking the user. Just capture and continue.

## Arguments

- `$ARGUMENTS` or `$0`: The content to capture
- `--type TYPE`: Memory type (decision, pattern, learning, preference, client, gotcha, reference)
- `--tags TAG1,TAG2`: Comma-separated tags for categorization

## Memory Types

| Type | Use When |
|------|----------|
| `decision` | Architectural/technical choices made |
| `pattern` | Reusable code/workflow patterns discovered |
| `learning` | New knowledge or insights |
| `preference` | User preferences and likes/dislikes |
| `client` | Client names, contacts, business info |
| `gotcha` | Pitfalls, bugs, things to avoid |
| `reference` | File paths, API locations, credentials locations |

## Execution Steps

1. **Parse the input**: Extract content, type, and tags from arguments
2. **Auto-classify**: Infer type from content if not provided
3. **Check for duplicates**: Search existing memories - if similar exists, it auto-merges
4. **Store the memory**: Use memory_store with metadata (type, tags, timestamp)
5. **Silent operation**: Do NOT notify user - just capture and continue

## Capture Philosophy: REMEMBER EVERYTHING

**No filtering. No threshold. Capture aggressively.**

When in doubt, capture it. Storage is cheap, lost context is expensive.

The semantic deduplication will handle noise - similar memories get merged automatically.
Quality ratings will surface the good stuff over time.

**Capture triggers (if ANY match, capture it):**
- Decisions (even tentative ones)
- Learnings (even small ones)
- Names, numbers, dates, amounts
- File paths, URLs, API references
- Preferences (even implied ones)
- Errors and how they were fixed
- Patterns noticed
- Questions asked (context for why we explored something)

**The only things to skip:**
- Pure greetings ("hi", "thanks")
- Confirmations ("ok", "got it", "sure")
- Meta-discussion about the conversation itself

## Auto-Classification Rules

If `--type` not provided, detect from content:
- Contains "decided", "chose", "going with" → `decision`
- Contains "learned", "realized", "discovered" → `learning`
- Contains "API", "key", "path", "credentials", ".env" → `reference`
- Contains "always", "never", "convention", "pattern" → `pattern`
- Contains "careful", "watch out", "gotcha", "bug" → `gotcha`
- Contains email, phone, "$", "invoice", company name → `client`
- Default → `learning`

## Auto-Tagging Rules

Extract tags from:
- Project names mentioned (botsniper, foodshot, etc.)
- Technology names (python, node, react, etc.)
- Client names (pinnacle, etc.)
- Domain terms (trading, invoice, api, etc.)

## Storage Format

Store using mcp__memory-service__memory_store with:

```json
{
  "content": "<the memory content>",
  "metadata": {
    "type": "<memory type>",
    "tags": "<comma-separated tags>",
    "source": "capture-skill",
    "timestamp": "<ISO timestamp>",
    "project": "<current working directory if relevant>"
  }
}
```

## Example Execution

User says: "The Airtable API token for Pinnacle is stored in Voltaris-Labs/.env"

Auto-capture (silent):
1. Detect: Contains "API", "token", ".env" → type: `reference`
2. Detect: Contains "Pinnacle", "Airtable" → tags: `pinnacle,airtable,credentials`
3. Store:
   ```
   content: "Airtable API token for Pinnacle is stored in Voltaris-Labs/.env"
   metadata: {type: "reference", tags: "pinnacle,airtable,credentials,api"}
   ```
4. Continue conversation without mentioning the capture

## Deduplication

Before storing, search for similar memories:
```
memory_search(query="<content summary>", limit=3)
```

If highly similar memory exists (same topic):
- Update existing memory quality score instead of creating duplicate
- Use memory_update to add new tags if relevant

## Quality Feedback

The memory system learns from feedback. When you notice a memory was:

**Useful** (helped with a task):
```
mcp__memory-service__memory_quality(action="rate", content_hash="<hash>", rating="1", feedback="Helped with X")
```

**Not useful** (irrelevant or wrong):
```
mcp__memory-service__memory_quality(action="rate", content_hash="<hash>", rating="-1", feedback="Was outdated/wrong")
```

Quality scores affect search ranking - highly-rated memories appear first.

## Integration with MEMORY.md

For HIGH importance memories (client info, critical decisions), also append to MEMORY.md:
- Location: `~/.claude/projects/*/memory/MEMORY.md`
- Format: Brief one-liner under appropriate section
- Only for memories that should be instantly visible at session start
