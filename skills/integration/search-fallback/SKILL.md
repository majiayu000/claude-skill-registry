---
name: search-fallback
description: Fallback to free search APIs (Tavily, Brave, Bing) when WebSearch fails or rate-limits.
homepage: https://github.com/Khamel83/oneshot
allowed-tools: Read, Write, Edit, Bash
metadata: {"oneshot":{"emoji":"🔍","requires":{"bins":["curl"]}}}
---

# Search Fallback Skill

Free search APIs as fallback when built-in WebSearch fails or hits rate limits.

## When To Use

**Auto-triggered via AGENTS.md when:**
- WebSearch returns rate limit (429 error)
- User says "web search failed", "search not working"
- Explicit request: "use search api", "fallback search"

**Also available manually:**
- User can invoke with `/search-fallback` or "use search fallback"

## How It Works

### Step 1: Check Available API Keys

First, check which search API keys are available:

```bash
# Decrypt and check available keys
cd ~/github/oneshot/secrets

# Check Tavily
sops -d --output-type dotenv ~/github/oneshot/secrets/research_keys.env.encrypted | grep TAVILY_API_KEY | cut -d= -f2 2>/dev/null && echo "Tavily: available" || echo "Tavily: not configured"

# Check Brave
sops -d --output-type dotenv ~/github/oneshot/secrets/research_keys.env.encrypted | grep BRAVE_API_KEY | cut -d= -f2 2>/dev/null && echo "Brave: available" || echo "Brave: not configured"

# Check Bing
sops -d --output-type dotenv ~/github/oneshot/secrets/research_keys.env.encrypted | grep BING_API_KEY | cut -d= -f2 2>/dev/null && echo "Bing: available" || echo "Bing: not configured"
```

### Step 2: Try Each API in Order

**1. Perplexity** (Best - AI answers with web search + citations):
```bash
OUTPUT=$(sops -d --output-type dotenv ~/github/oneshot/secrets/research_keys.env.encrypted 2>/dev/null)
OUTPUT=${OUTPUT#data=}
PERPLEXITY_KEY=$(echo "$OUTPUT" | grep -oP 'PERPLEXITY_API_KEY=\K[^\\]+')

curl -s -X POST "https://api.perplexity.ai/chat/completions" \
  -H "Authorization: Bearer $PERPLEXITY_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"sonar\",
    \"messages\": [{\"role\": \"user\", \"content\": \"$QUERY\"}],
    \"max_tokens\": 500
  }" | jq -r '.choices[0].message.content, "\n\nCitations:", (.citations // [] | .[] | "- \(.)")'
```

**2. Context7** (Code documentation search - perfect for finding code examples):
```bash
OUTPUT=$(sops -d --output-type dotenv ~/github/oneshot/secrets/research_keys.env.encrypted 2>/dev/null)
OUTPUT=${OUTPUT#data=}
CONTEXT7_KEY=$(echo "$OUTPUT" | grep -oP 'CONTEXT7_API_KEY=\K[^\\]+')

curl -s "https://context7.com/api/v1/search?query=$QUERY&numResults=5" \
  -H "Authorization: Bearer $CONTEXT7_KEY" | jq -r '.results[] | "- \(.title): \(.id)\n  \(.description)"'
```

**3. Tavily** (AI answers + sources - if keys are valid):
```bash
OUTPUT=$(sops -d --output-type dotenv ~/github/oneshot/secrets/research_keys.env.encrypted 2>/dev/null)
OUTPUT=${OUTPUT#data=}
TAVILY_KEY=$(echo "$OUTPUT" | grep -oP 'TAVILY_API_KEY=\K[^\\]+')

curl -s https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -d "{
    \"api_key\": \"$TAVILY_KEY\",
    \"query\": \"$QUERY\",
    \"search_depth\": \"advanced\",
    \"include_answer\": true,
    \"include_raw_content\": false,
    \"max_results\": 10
  }" | jq -r '.answer // "No answer", (.results[] | "- \(.title): \(.url)")'
```

**4. Brave** (Clean, privacy-focused results - not configured):
```bash
# Add BRAVE_API_KEY to research_keys.env.encrypted first
BRAVE_KEY=$(sops -d --output-type dotenv ~/github/oneshot/secrets/research_keys.env.encrypted | grep BRAVE_API_KEY | cut -d= -f2)

curl -s "https://api.search.brave.com/res/v1/web/search?q=$QUERY&count=10" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: $BRAVE_KEY" | jq -r '.web.results[] | "- \(.title): \(.url)\n  \(.description)"'
```

**5. Bing** (Familiar Google-style results - not configured):
```bash
# Add BING_API_KEY to research_keys.env.encrypted first
BING_KEY=$(sops -d --output-type dotenv ~/github/oneshot/secrets/research_keys.env.encrypted | grep BING_API_KEY | cut -d= -f2)

curl -s "https://api.bing.microsoft.com/v7.0/search?q=$QUERY&count=10" \
  -H "Ocp-Apim-Subscription-Key: $BING_KEY" | jq -r '.webPages.value[] | "- \(.name): \(.url)\n  \(.snippet)"'
```

### Step 3: Return Results to User

Format the search results clearly with:
- Title and URL for each result
- Brief description/snippet
- Link to full results if relevant

---

## Quick One-Liner Usage

When you need to run a quick search fallback:

```bash
# Helper to extract keys (sops outputs "data=" prefix)
OUTPUT=$(sops -d --output-type dotenv ~/github/oneshot/secrets/research_keys.env.encrypted 2>/dev/null)
OUTPUT=${OUTPUT#data=}

# Tavily (working - AI answers + sources)
TAVILY_KEY=$(echo "$OUTPUT" | grep -oP 'TAVILY_API_KEY=\K[^\\]+')
curl -s https://api.tavily.com/search -H "Content-Type: application/json" \
  -d "{\"api_key\":\"$TAVILY_KEY\",\"query\":\"YOUR_QUERY\",\"include_answer\":true}" | jq -r '.answer'

# Context7 (code/documentation search)
CONTEXT7_KEY=$(echo "$OUTPUT" | grep -oP 'CONTEXT7_API_KEY=\K[^\\]+')
curl -s "https://api.context7.io/v1/search?query=YOUR_QUERY&numResults=5" \
  -H "Authorization: Bearer $CONTEXT7_KEY" | jq -r '.results[] | "- \(.title): \(.id)"'
```

---

## Setup (One-Time)

### 1. Get Free API Keys

**Tavily** (1000 searches/month, best for AI answers):
- Sign up: https://tavily.com
- Get API key from dashboard

**Brave** (2000 requests/month, clean results):
- Sign up: https://brave.com/search/api/
- Get API key from dashboard

**Bing** (1000 queries/month):
- Sign up: https://www.microsoft.com/cognitive-services
- Get Bing Web Search API key

### 2. Store Keys Securely

```bash
cd ~/github/oneshot/secrets

# Create or edit the secrets file
sops ~/github/oneshot/secrets/research_keys.env.encrypted
```

Add:
```
TAVILY_API_KEY=tvly-your-key-here
BRAVE_API_KEY=BS-your-key-here
BING_API_KEY=your-key-here
```

### 3. Test Setup

```bash
# Test Tavily
sops -d --output-type dotenv ~/github/oneshot/secrets/research_keys.env.encrypted | grep TAVILY_API_KEY | cut -d= -f2 | xargs -I {} curl -s https://api.tavily.com/search -H "Content-Type: application/json" -d '{"api_key":"{}","query":"test","include_answer":true}' | jq '.answer'

# If you get an answer, it's working!
```

---

## API Comparison

| API | Free Tier | Best For | AI Answer | Status |
|-----|-----------|----------|-----------|--------|
| **Tavily** | varies | Research, learning | ✅ Yes | ✅ Working |
| **Perplexity** | varies | Research with citations | ✅ Yes | ⚠️ 401 errors |
| **Context7** | varies | Code/docs search | ✅ Yes | ⚠️ API uncertain |
| **Firecrawl** | varies | Web scraping | ❌ No | ⚠️ Out of credits |
| **Brave** | 2000/month | Quick facts | ❌ No | Not configured |
| **Bing** | 1000/month | Familiar format | ❌ No | Not configured |

**Recommended**: Use Tavily as primary fallback - confirmed working with current key.

---

## Integration Pattern

When WebSearch fails, the workflow is:

1. **Detect failure** - WebSearch returns 429 or error
2. **Auto-invoke this skill** - Via AGENTS.md pattern matching
3. **Run searches** - Try Perplexity → Context7 → Tavily → Brave → Bing
4. **Return results** - Format for user
5. **Continue work** - User gets what they need without interruption

---

## Notes

- **Perplexity** - AI-generated answer + web citations, best for general research
- **Context7** - Code/documentation search, perfect for finding code examples
- **Tavily** - AI-generated answer + sources, working with current key
- **Firecrawl** - Out of credits, recharge at https://firecrawl.dev/pricing
- All APIs have generous free tiers suitable for personal use
- Rate limits are per-month, not per-day
- Keys are encrypted with SOPS, stored in `~/github/oneshot/secrets/research_keys.env.encrypted`

## Keywords

search fallback, tavily, brave, bing, perplexity, websearch rate limit
