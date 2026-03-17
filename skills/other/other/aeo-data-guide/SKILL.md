---
name: aeo-data-guide
description: How to think about AirOps AEO data — interpreting metrics, handling ambiguous asks, routing to the right agent.
auto-apply: true
disable-model-invocation: false
---

## The Data Model (Conceptual)

AirOps tracks how AI search engines talk about a brand. The core idea:

1. A brand has **prompts** — questions people ask AI (e.g. "What are the best AEO tools?")
2. Each prompt gets passed into multiple **AI providers** (ChatGPT, Gemini, Perplexity, etc.)
3. Each provider returns an **answer**
4. Each answer is checked: did it **mention** the brand? Did it **cite** (link to) the brand?
5. From this, we get metrics: mention rate, citation rate, share of voice, etc.

There's also a **page** side — how each URL on the brand's site performs across
AEO (AI citations), GSC (Google search), and GA4 (site analytics).

Everything hangs off a **Brand Kit**, which lives in a **Workspace**. You always
need to find the right brand kit first.

---

## Two Domains of Data

| Domain | What it covers | Agent |
|--------|---------------|-------|
| **AI search visibility** | Prompts, answers, mentions, citations, competitors, share of voice | **ai-search-analyst** |
| **Page performance** | Page-level AEO + GSC + GA4 metrics, smart filters, optimization opportunities | **page-analyst** |

Delegate to the right agent. If a question spans both (e.g. "which pages are losing
AI citations and also losing Google rankings?"), start with the page-analyst (it
has the combined view) and escalate to ai-search-analyst for deeper prompt/answer
drill-downs.

---

## Branded vs Non-Branded (Critical Guardrail)

Prompts have a `brand_mentioned` field. When the brand is in the question
("What is AirOps?"), AI will almost always mention it — inflating metrics.

**Default to non-branded (`brand_mentioned: false`) for all analysis.**

Only include branded when:
- User explicitly asks for branded vs non-branded comparison
- Analyzing brand-name recognition specifically

If metrics look suspiciously high, check whether branded prompts are included.

---

## Handling Ambiguous Requests

Users often ask vague things. Here's how to route them:

### "How are we doing?"
- Start with overall health: mention_rate, citation_rate, share_of_voice
- Break down by provider and topic to find the story
- Compare to benchmarks (5-15% mention rate for non-branded is good)
- Delegate to **ai-search-analyst**

### "What should we work on?"
- Check pages with smart filters: losing_ai_visibility, citation_rate_decline, almost_page_one
- Check prompts where brand is NOT mentioned but volume is high (opportunities)
- Delegate to **page-analyst** for page opportunities, **ai-search-analyst** for prompt gaps
- For each opportunity, check if a page exists (see Refresh vs Create) and suggest
  a specific skill the user can run (e.g. `/airops:refresh-content "url"` or `/airops:create-blog "keyword"`)

### "How do we compare to competitors?"
- share_of_voice and citation_share by competitor dimension
- Drill into which topics competitors dominate
- Delegate to **ai-search-analyst**

### "Show me our best/worst performing content"
- Pages sorted by citation_rate or citations_count (best) or using smart filters (worst)
- Delegate to **page-analyst**

### "What's happening with [specific provider]?"
- Filter analytics to that provider
- Compare mention_rate and citation_rate vs other providers
- Delegate to **ai-search-analyst**

### When you don't have enough context — ASK:

- **No time period specified** → "What time range? Last 30 days, 90 days, or a specific period?"
- **No brand kit clarity** → List brand kits and ask which one
- **"Report" is vague** → "Do you want a summary in chat, a saved markdown file, or a dashboard in AirOps?"
- **Topic unclear** → List topics and ask which to focus on
- **"Performance" is broad** → "Are you asking about AI search visibility (mentions/citations) or page performance (traffic/rankings)?"

Don't guess. A quick clarifying question saves a wrong analysis.

---

## Reading AI Search Numbers

### Mentions first, citations second

**Mention rate is the primary metric for AI search visibility.** It tells you
whether AI is actually talking about the brand. If you're not mentioned, nothing
else matters — citations, sentiment, and position are all downstream of being
mentioned in the first place.

Citation rate is important but secondary — it measures whether AI links back to
your content. You can be mentioned without being cited (brand is known but content
isn't linked), but you generally won't be cited without being mentioned.

When reporting or analyzing:
- Lead with mention rate and share of voice
- Follow with citation rate as supporting context
- Don't fixate on citations alone — a brand that's mentioned everywhere but cited
  rarely has a different problem than one that's not mentioned at all

### Metric combinations that tell a story

| Pattern | What it means | Action |
|---------|--------------|--------|
| High mention, low citation | Brand is known but not linked to | Create more authoritative, linkable content so AI has something to cite |
| Low sentiment | AI talks about you negatively | Flag for messaging/PR review |
| Declining mention + stable citation | Losing mindshare but content still works | Brand awareness campaign needed |
| Declining citation + stable mention | Losing authority but still known | Content refresh — update outdated pages so AI trusts them again |

### Volume matters

`relative_volume_score` (0-1) tells you how popular a prompt is. A prompt with
0.9 volume where you're not mentioned is a much bigger opportunity than one with
0.1 volume. Always factor in volume when prioritizing.

---

## Reading Page Numbers

Page data combines three sources: AEO (AI citations), GSC (Google Search), and
GA4 (site analytics). The power is in reading them together — one source shows
what's happening, the others show why.

### Single-signal patterns

| Pattern | What it means | Action |
|---------|--------------|--------|
| Losing AI citations (`losing_ai_visibility`) | AI is dropping references to this page | Content is going stale for AI. Refresh with current data, stats, examples. Check what AI is citing instead. |
| Losing clicks, stable position (`losing_clicks`) | Ranking hasn't changed but fewer people click | Something else is eating clicks — likely AI overviews or featured snippets. Review meta title/description. Consider if AI is answering the query directly. |
| Rankings slipping (`rankings_slipping`) | Position declining over time | Classic SEO issue — competitors may have fresher/better content. Audit and refresh. |
| Almost page one (`almost_page_one`) | Ranking #11-20 | Quick win — small improvements could push to page 1. Strengthen content, add internal links, improve on-page SEO. |
| Citation rate decline, stable SEO (`citation_rate_decline`) | AI losing faith in this page while Google still ranks it | Early warning. AI updates faster than Google. If AI drops you, Google may follow. Refresh content now before both decline. |

### Multi-signal patterns (the real insights)

| AEO signal | GSC signal | GA4 signal | What's happening | What to do |
|------------|-----------|------------|-----------------|------------|
| Citations dropping | Clicks dropping | Traffic dropping | Everything is declining. This page is losing relevance across the board. | Major content refresh or rewrite. Check what competitors/citations are winning instead. |
| Citations dropping | Clicks stable | Traffic stable | AI is moving away from this page but Google still sends traffic. | The page works for traditional search but isn't structured for AI citation. Update to be more authoritative/quotable. |
| Citations stable | Clicks dropping | Traffic dropping | AI still cites you but Google traffic is falling. | Traditional SEO issue — position may be slipping, or AI overviews are taking clicks. Check position trend. |
| Citations rising | Clicks stable | Traffic rising | AI is sending you more traffic via citations. | This page is winning in AI search. Study what makes it work and replicate the pattern. |
| Citations stable | Clicks rising | Traffic rising | Google is sending more traffic, AI unchanged. | Traditional SEO win. Don't change what's working — focus AI optimization effort elsewhere. |
| No citations | High clicks | High traffic | Google loves this page but AI doesn't cite it. | Opportunity — optimize this high-traffic page to be more citable by AI (structured data, clear answers, authoritative framing). |

### How to navigate page analysis

1. **Start broad** — use smart filters to find pages that need attention
2. **Check the combination** — don't act on one signal alone. A page losing clicks but gaining citations is a different situation than one losing both.
3. **Drill into why** — use `get_page_prompts` to see which AI prompts cite the page. Are those prompts losing volume? Are competitors getting cited instead?
4. **Cross-reference** — if a page is losing AI citations, delegate to ai-search-analyst to check if it's a page-specific issue or a broader trend (maybe all pages on that topic are declining).
5. **Prioritize by impact** — pages with high traffic + declining signals need attention first. A page with 10 monthly visits losing citations is less urgent than one with 10,000.

---

## Refresh vs Create (Hard Gate — Not Optional)

**You MUST check if a page already exists before suggesting ANY content action.**
This is a hard gate, not a suggestion. If you skip this step, you will recommend
creating content that already exists — which is worse than recommending nothing.

### The rule (follow this EVERY TIME)

For **every** keyword, topic, or content gap you identify:

1. Identify the keyword or topic from the opportunity
2. **Run `list_pages`** — search by `primary_keyword` AND by `url` containing
   relevant terms. Do both searches. Cast a wide net.
3. If you're suggesting pillar pages, category pages, or hub content — also search
   by `folder_name` to see if an entire section already exists
4. **If a page exists** → recommend refreshing/optimizing that page. Don't create
   a competing page. Ever.
5. **If no page exists** (you searched and confirmed) → recommend creating new content.
6. **If you're not sure** → search more broadly. Don't default to "create."

### What counts as "checking"

A real check means you actually called `list_pages` with relevant filters and
reviewed the results. It does NOT mean:
- Assuming no page exists because you haven't seen one
- Skipping the check because you're making multiple recommendations
- Checking for one keyword but not the others in a batch of suggestions

**Every recommendation needs its own check.** If you're suggesting 5 pieces of
content, that's 5 checks. No exceptions.

### Why this matters

Suggesting "create a pillar page about X" when the brand already has one is
embarrassing and erodes trust. The existing page might just need a refresh —
updated stats, better structure for AI citation, stronger authority signals.
Duplicate content also competes with itself in search rankings.

### How to check (multiple searches)

For each opportunity, run at least two of these:

- `list_pages` filtered by `primary_keyword` matching the prompt's keyword
- `list_pages` filtered by `url` containing relevant terms (e.g. URL contains "pricing" or "comparison")
- `list_pages` filtered by `folder_name` to scan an entire section (e.g. `/blog/`, `/resources/`, `/guides/`)
- If the suggestion is a pillar/hub page, check for any existing pages in that topic area — not just exact keyword matches

### What to recommend

When suggesting actions, **point the user to a specific skill they can run.** The
user can invoke these directly — you can't run them yourself, but you can tell the
user exactly what to type with the right inputs pre-filled.

| Situation | Recommendation | Suggest to user |
|-----------|---------------|-----------------|
| Page exists, performing well | Leave it alone — focus effort elsewhere | (no action needed) |
| Page exists, losing citations or traffic | Refresh with current data, optimize for AI | `/airops:refresh-content "<page-url>"` |
| Page exists, no AI citations at all | Restructure for AI citability | `/airops:refresh-content "<page-url>"` |
| No page exists, high volume keyword (confirmed via search) | Create new content targeting this keyword | `/airops:create-blog "<keyword>"` |
| No page exists, low volume keyword | Deprioritize unless strategically important | (no action needed) |
| Comparing two competitors/products | Create comparison content | `/airops:create-comparison "<brand-a>" "<brand-b>"` |
| Multiple keywords in a category | Create a roundup or list | `/airops:create-listicle "<topic>"` |

**Format your suggestions as ready-to-run commands** with the actual keyword, URL,
or topic filled in. The user should be able to copy and paste directly.

**In your output, show your work.** When recommending content creation, explicitly
state that you checked for existing pages and what you searched for. Example:
> "Searched `list_pages` for keyword 'aeo tools' and URL containing 'aeo' — no
> existing page found. Recommend creating: `/airops:create-blog "aeo tools"`"

---

## Skip Root / Home Pages in Recommendations

**Never recommend changes to root-level or home pages** (e.g. `example.com/`,
`example.com`, `www.example.com/`). Even if their citation rate or traffic is
declining, suggesting edits to a homepage is not actionable advice — home pages
serve a different purpose than content pages, and their AI citation behavior is
driven by brand recognition, not content optimization.

When scanning `list_pages` results:
- **Filter out** any URL that is just the domain root (path is `/` or empty)
- **Don't surface** root pages in "pages that need attention" lists
- **Don't suggest** refreshing or rewriting the homepage
- If a root page shows up in a smart filter result (e.g. `losing_ai_visibility`),
  skip it silently — it's noise, not signal

This applies to all recommendations: page-analyst findings, action grids,
"what should we work on" answers, and any suggested `/airops:refresh-content` commands.

---

## What NOT to Do

- **Don't include branded prompts by default** — inflates everything
- **Don't report raw numbers without context** — "12% mention rate" means nothing without the benchmark and trend
- **Don't analyze a single time snapshot** — always check the trend
- **Don't mix up mention and citation** — mention = named in the response, citation = linked to. Very different signals.
- **Don't compare across providers without noting the difference** — each AI has different behavior patterns
- **Don't act on one signal alone for pages** — always cross-reference AEO + GSC + GA4 before recommending action
- **Don't guess at metric definitions** — check the AirOps concepts resource if unsure
- **Don't suggest creating content without checking if it already exists** — see "Refresh vs Create" above. This is a hard requirement, not a suggestion.
