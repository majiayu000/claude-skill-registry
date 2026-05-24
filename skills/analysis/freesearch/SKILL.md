---
name: freesearch
description: TRULY FREE research via Exa API - zero Claude tokens. Uses Exa directly, no Gemini CLI wrapper.
homepage: https://github.com/Khamel83/oneshot
allowed-tools: Read, Write, Edit, Bash
metadata: {"oneshot":{"emoji":"🆓","requires":{"bins":["curl"]}}}
---

# /freesearch - TRULY FREE Research

**Uses 0 Claude Code tokens.** Calls Exa API directly via curl.

## When To Use

User says:
- `/freesearch [topic]` - Slash command
- "Free research on [topic]"
- "Research without burning tokens"

---

## How It Works

**Direct API calls via curl:**

1. Ask 2-3 clarifying questions (goal, depth, audience)
2. Create `docs/research/{date}_{topic}_in_progress.md`
3. Search Exa API:
   - web search for overview
   - code search for technical details
   - company/person search if relevant
4. Update in-progress file with raw results
5. Create `docs/research/{date}_{topic}_final.md` with:
   - Executive summary
   - Key findings
   - Sources with links
   - Related topics
6. Return file path to Claude for reading

---

## Exa API Configuration

The EXA_API_KEY is loaded from encrypted secrets:

```bash
# Decrypt and load key (done via skill wrapper)
EXA_KEY=$(sops --decrypt --output-type json ~/github/oneshot/secrets/research_keys.json.encrypted | grep -o '"EXA_API_KEY": "[^"]*"' | cut -d'"' -f4)
```

API Endpoint: `https://api.exa.ai/search`

---

## Research Prompt Template

```bash
curl -s -X POST 'https://api.exa.ai/search' \
  -H "x-api-key: $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "[TOPIC]",
    "type": "auto",
    "numResults": 10,
    "contents": {
      "text": {
        "maxCharacters": 20000
      }
    }
  }'
```

---

## Output Locations

**Project research files:**
```
docs/research/{YYYY-MM-DD}_{topic_slug}_in_progress.md
docs/research/{YYYY-MM-DD}_{topic_slug}_final.md
```

**Historical research:**
```
research/{topic_slug}/research.md
```

---

## Quick Wins to Implement

Based on competitor research, these features should be added to ONE_SHOT:

1. **`/browse` command** - Visual skill discovery with fuzzy search
2. **`bd test` framework** - Skill testing framework
3. **Diff preview** - Show changes before applying
4. **Skill analytics** - Track most-used skills

---

## Example Usage

**User says:** `/freesearch AI coding tools with persistent memory`

**You do:**

1. Ask clarifying questions:
   - "What's your goal?"
   - "How deep should I go?"

2. Create in-progress file with initial query

3. Search Exa API:
   - `web_search_exa`: "AI coding tools persistent memory cross-session"
   - `get_code_context_exa`: "AI coding task orchestration memory"

4. Update in-progress file with findings

5. Create final report with executive summary

6. Return:
   ```
   Key findings:
   - MCP Task Orchestrator, Cipher, Pieces AI Memory, Cursor Rules
   - All use RAG + vector stores for persistent context

   📄 Full research: docs/research/2025-01-31_ai_persistent_memory_final.md
   ```

---

## File Format Template

### In-Progress Template
```markdown
# Research: {Topic}

**Started:** {timestamp}
**Status:** In Progress

## Search Queries Used
- {query1}
- {query2}

## Raw Results

### Source 1
- **URL:** {url}
- **Title:** {title}
- **Snippet:** {content}

### Source 2
- **URL:** {url}
- **Title:** {title}
- **Snippet:** {content}

## Initial Notes
{ongoing analysis}
```

### Final Template
```markdown
# Research: {Topic}

**Completed:** {timestamp}
**Duration:** {duration}

## Executive Summary
{2-3 sentence overview}

## Key Findings
1. {finding with citation}
2. {finding with citation}

## Sources
1. [{Title}]({url}) - {description}
2. [{Title}]({url}) - {description}

## Related Topics
- {topic for further research}

## Full Details
{detailed analysis}

---

📄 **In-progress research:** docs/research/{date}_{topic}_in_progress.md
```

---

## Why This Exists

The `deep-research` skill wraps Gemini CLI in a Claude sub-agent, which still burns tokens. This skill calls Exa API **directly** via curl:

- ✅ 0 Claude Code tokens for research
- ✅ Only main conversation tokens (clarifying questions, summary)
- ✅ Same quality research (Exa's neural search)
- ✅ Saves to project `docs/research/` (tracked in git)

---

## Tips

- Research takes 10-30 seconds (Exa is fast)
- Always save to `docs/research/` NOT `~/github/oneshot/research/`
- Include user's goal in the prompt for better results
- Link in-progress file in final report for drill-down

## Keywords

free research, exa api, zero tokens, web search, research save
