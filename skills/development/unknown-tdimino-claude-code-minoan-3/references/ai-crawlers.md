# AI Crawler Registry

Complete taxonomy of AI crawlers, classified by purpose. OpenAI now runs THREE separate crawlers — most robots.txt files predate this split.

---

## Search/Retrieval Crawlers

Blocking any of these removes the site from that engine's AI search results.

| Crawler | Operator | Product | User-Agent |
|---------|----------|---------|------------|
| OAI-SearchBot | OpenAI | ChatGPT Search index | `OAI-SearchBot` |
| PerplexityBot | Perplexity | Perplexity search | `PerplexityBot` |
| Claude-SearchBot | Anthropic | Claude search | `Claude-SearchBot` |
| Bingbot | Microsoft | Bing Copilot | `bingbot` |
| Googlebot | Google | Google AI Overviews | `Googlebot` |
| Bravebot | Brave | Brave Search / Leo AI | `Bravebot` |
| YouBot | You.com | You.com AI search | `YouBot` |

### User-Triggered Fetch Bots

These are triggered when a user pastes a URL into the AI product. Blocking them doesn't remove the site from search results—it only prevents live page reads during a conversation. Recommended to allow, but not search-critical.

| Crawler | Operator | Product | User-Agent |
|---------|----------|---------|------------|
| ChatGPT-User | OpenAI | Real-time user fetch | `ChatGPT-User` |
| Perplexity-User | Perplexity | Real-time user fetch | `Perplexity-User` |
| Claude-User | Anthropic | Real-time user fetch | `Claude-User` |

**Perplexity-User caveat:** Per Perplexity's own documentation, `Perplexity-User` "generally ignores robots.txt" directives. Adding `Disallow` rules for this bot may have no effect. The only reliable way to block Perplexity user-triggered fetches is server-side User-Agent filtering. Note this when auditing—a `Disallow` for `Perplexity-User` in robots.txt gives false confidence.

### Training Opt-Out Bots

These control whether your content is used for AI model training. Blocking them opts out of training but has no effect on search visibility.

| Crawler | Operator | What Blocking Does | User-Agent |
|---------|----------|--------------------|------------|
| Applebot-Extended | Apple | Opts out of Apple Intelligence training | `Applebot-Extended` |

**Note:** Applebot-Extended is NOT a search crawler. It is Apple's training data opt-out mechanism. Apple search visibility is controlled by `Applebot` (the base crawler, not `-Extended`). Blocking `Applebot-Extended` is equivalent to blocking `GPTBot` or `ClaudeBot`—it protects content from training use only.

### OpenAI's 3-Crawler Split

Most robots.txt files only reference `GPTBot`. OpenAI now uses three separate crawlers:

1. **GPTBot** — training data collection only. Blocking this does NOT affect ChatGPT Search.
2. **OAI-SearchBot** — builds the ChatGPT Search index. Blocking this removes the site from ChatGPT Search results. This is the only search-critical OpenAI crawler.
3. **ChatGPT-User** — user-triggered fetch when someone pastes a URL into ChatGPT. Blocking this prevents live page reads but does NOT remove the site from search results. Recommended to allow, but not search-critical.

**Common mistake:** Blocking `GPTBot` thinking it controls all OpenAI access. It only controls training. Search index visibility requires `OAI-SearchBot` to be allowed. `ChatGPT-User` is a convenience bot, not a search-index bot.

### OpenAI's Ad Crawler

| Crawler | Purpose | User-Agent |
|---------|---------|------------|
| OAI-AdsBot | Crawls product/service pages for ChatGPT ad placement | `OAI-AdsBot` |

**Ecommerce relevance:** Blocking `OAI-AdsBot` may prevent product listings from appearing in ChatGPT's sponsored/ad surfaces. For ecommerce sites, recommend allowing it alongside `OAI-SearchBot`.

---

## Training Crawlers

These index content for model training only. Blocking them has no effect on AI search visibility.

| Crawler | Operator | Purpose |
|---------|----------|---------|
| GPTBot | OpenAI | Model training |
| ClaudeBot | Anthropic | Model training |
| Google-Extended | Google | Gemini/AI training |
| CCBot | Common Crawl | Open training dataset |
| Bytespider | ByteDance | TikTok/Doubao training |
| Amazonbot | Amazon | Alexa/model training |
| Diffbot | Diffbot | Knowledge graph construction |
| FacebookBot | Meta | AI training |
| meta-externalagent | Meta | External agent training |
| Ai2Bot | Allen AI | Research training |
| img2dataset | LAION | Image training data |
| Timesbot | OpenAI | News training partnership |
| cohere-ai | Cohere | Model training |

---

## CDN Bot Blocking Detection

Silent blocking that site owners may not be aware of.

| Platform | Feature | How to detect |
|----------|---------|---------------|
| Cloudflare | Bot Fight Mode | Dashboard → Security → Bots; or `wrangler.toml` `bot_management` settings |
| Cloudflare | Super Bot Fight Mode | Enterprise feature; blocks "definitely automated" traffic by default |
| Akamai | Bot Manager | Property rules → Bot classification rules |
| Vercel | Firewall | `vercel.json` → firewall rules; or dashboard → Firewall |
| AWS | WAF Bot Control | WAF rules → Bot Control rule group |
| Netlify | n/a | No built-in bot blocking (safe by default) |

**Detection commands:**
```bash
grep -ri "bot.*fight\|bot.*manage\|firewall" wrangler.toml vercel.json netlify.toml _headers 2>/dev/null
```

---

## Recommended robots.txt Template

```
# ============================================
# AI Search Crawlers — ALLOW for visibility
# Blocking these removes the site from AI search results
# ============================================

# OpenAI ChatGPT Search
User-agent: OAI-SearchBot
Allow: /

# Perplexity
User-agent: PerplexityBot
Allow: /

# Anthropic Claude Search
User-agent: Claude-SearchBot
Allow: /

# Brave Search / Leo AI
User-agent: Bravebot
Allow: /

# You.com AI Search
User-agent: YouBot
Allow: /

# User-triggered fetch bots (recommended to allow)
User-agent: ChatGPT-User
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: Claude-User
Allow: /

# ============================================
# AI Training / Opt-Out Crawlers — BLOCK to protect content
# Blocking these has NO effect on AI search visibility
# ============================================

# Apple Intelligence training opt-out (NOT a search crawler)
User-agent: Applebot-Extended
Disallow: /

User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: CCBot
Disallow: /

User-agent: Bytespider
Disallow: /

User-agent: Amazonbot
Disallow: /

User-agent: Diffbot
Disallow: /

User-agent: FacebookBot
Disallow: /

User-agent: meta-externalagent
Disallow: /

# ============================================
# AI Discovery Directives
# ============================================
LLMs-Txt: /llms.txt
LLMs-Full-Txt: /llms-full.txt
```

---

## IndexNow Integration

IndexNow provides instant indexing notification to Bing and Yandex.

### Setup

1. Generate an API key (any UUID)
2. Place key file at site root: `/{key}.txt` containing the key value
3. POST to `https://api.indexnow.org/indexnow` with:
   ```json
   {
     "host": "example.com",
     "key": "your-key",
     "urlList": ["https://example.com/updated-page"]
   }
   ```

### Supported Engines

| Engine | IndexNow Support |
|--------|-----------------|
| Bing | Yes — primary supporter |
| Yandex | Yes |
| Google | No — uses its own Indexing API |
| Perplexity | No |
| ChatGPT | No |

### When to Use

- After publishing new content
- After significant content updates
- After URL structure changes
- Automated via CI/CD post-deploy hook
