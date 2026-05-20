---
name: podcast-personalization-research
description: >
  Research a prospect's podcast appearances and generate deep personalization angles with specific quotes, topics, and draft openers for outreach.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Outreach & Personalization"
compatibility: Requires Amplemarket MCP server
---

# Podcast Personalization Research

Research a prospect's podcast appearances and generate deep personalization angles with specific quotes, topics, and draft openers for outreach.

## Instructions

When a user wants to personalize outreach based on a prospect's podcast appearances, search for episodes, extract key insights, and synthesize them into actionable personalization fields and openers.

### Steps

1. **Identify the prospect.** Extract any available identifiers from the user's request:
    - LinkedIn URL
    - Email address
    - Name + company
    If the user provides minimal info (e.g., first name only), ask for at least a full name and company or a LinkedIn URL before proceeding.
2. **Enrich the person** by calling `mcp__claude_ai_Amplemarket__enrich_person` with all available identifiers. Key data points to extract:
    - Full name
    - Current title and role
    - Company name and domain
    - Career history and previous companies
    - Industry and areas of expertise
    These details are essential for constructing accurate podcast search queries in the next step.
3. **Search for podcast appearances** using `WebSearch` with multiple query patterns to maximize coverage. Run all of these queries:
    - `"[full name]" podcast`
    - `"[full name]" episode guest`
    - `"[full name]" interview [industry topic]`
    - `"[full name]" "[company name]" podcast`
    - `"[full name]" webinar OR panel OR fireside`
    Scan the results for podcast directories (Apple Podcasts, Spotify, YouTube), show notes pages, and episode listings. Deduplicate results across queries and rank by relevance and recency.
4. **Extract podcast content** by calling `WebFetch` on the top 3-5 most promising results. For each episode page, extract:
    - Podcast name and host
    - Episode title and date
    - Key topics discussed
    - Direct quotes or paraphrased insights from the prospect
    - The prospect's stated opinions, predictions, or challenges
    - Whether the prospect was the host, a guest, or merely mentioned
    If a page is behind a paywall or lacks useful content, move to the next result.
5. **Enrich the company** by calling `mcp__claude_ai_Amplemarket__enrich_company` with the prospect's company `domain` or `linkedin_url`. Key data points to extract:
    - Industry and sub-industry
    - Company size and growth trajectory
    - Description and value proposition
    - Recent funding or milestones
    - Tech stack
    Use this context to connect podcast insights back to the prospect's current business reality.
6. **Synthesize findings.** Analyze all extracted podcast content and identify the strongest personalization angles based on:
    - **Specific quotes or opinions** they stated on the podcast. These are the most powerful hooks
    - **Topics they are passionate about.** Recurring themes across multiple appearances signal genuine interest
    - **Predictions they made,** especially ones you can validate, reference, or ask about
    - **Challenges they described.** Pain points they openly discussed are ideal outreach entry points
    - **Contrarian or unique takes.** Bold stances that set them apart from conventional thinking
    Rank angles by specificity and relevance to the outreach goal.
7. **Generate dynamic fields** for each podcast appearance found. Populate the `{{podcast_*}}` fields listed in the Dynamic Fields Generated section below. If multiple appearances are found, generate a set of fields for each episode, numbered sequentially (e.g., `{{podcast_name_1}}`, `{{podcast_name_2}}`).
8. **Draft 3-5 outreach openers** that naturally reference podcast content. Each opener should:
    - Reference a specific episode, quote, or topic, not generic podcast mentions
    - Connect the podcast insight to a relevant business challenge or opportunity
    - Feel conversational and authentic, not like a templated mail merge
    - Be 1-3 sentences long
    - Vary in angle: one quote-based, one topic-based, one prediction-based, one challenge-based, one shared-interest-based (where applicable)

### Important Notes

- **Never fabricate quotes.** Only use direct quotes that were actually extracted from podcast content via WebFetch. If you cannot verify a quote, paraphrase and note it as paraphrased.
- **Distinguish between host, guest, and mention.** The prospect's role in the podcast matters. Being a regular host signals thought leadership differently than a one-time guest appearance.
- **Quality over quantity.** One deeply researched episode with real quotes beats five shallow mentions. Prioritize depth of extraction over breadth of appearances.
- **Recency matters.** Prioritize recent appearances (last 12-18 months) over older ones, as the prospect's views and role may have evolved.
- **Respect content boundaries.** If podcast content is behind a paywall or requires authentication, note the episode metadata and skip content extraction rather than attempting to bypass access controls.

## Dynamic Fields Generated

| Field | Description |
| --- | --- |
| `{{podcast_name}}` | Name of the podcast show |
| `{{podcast_host}}` | Host of the podcast |
| `{{podcast_episode_title}}` | Title of the specific episode |
| `{{podcast_episode_date}}` | Air date of the episode |
| `{{podcast_episode_url}}` | URL to the episode page |
| `{{podcast_topic}}` | Primary topic or theme discussed |
| `{{podcast_person_quote}}` | Direct quote from the prospect on the podcast |
| `{{podcast_person_stance}}` | The prospect's position or opinion on a key topic |
| `{{podcast_key_insight}}` | Most notable insight or takeaway from the appearance |
| `{{podcast_prediction}}` | A prediction or forward-looking statement the prospect made |
| `{{podcast_shared_interest}}` | Topic overlap between the prospect's podcast discussion and your product or solution |
| `{{podcast_suggested_opener}}` | Ready-to-use outreach opener referencing the podcast |
| `{{podcast_challenge_mentioned}}` | A business challenge or pain point the prospect discussed |

## Examples

### Example 1: Prospect Who Was a Podcast Guest

**User prompt:** "Find podcast appearances for linkedin.com/in/maria-torres-cro"

**What the skill does:**
1. Calls `mcp__claude_ai_Amplemarket__enrich_person` with `linkedin_url`: "https://linkedin.com/in/maria-torres-cro".
2. Gets back: Maria Torres, CRO at ScaleFlow (scaleflow.io), former VP Sales at Gong.
3. Runs `WebSearch` with:
- `"Maria Torres" podcast`
- `"Maria Torres" episode guest`
- `"Maria Torres" interview sales leadership`
- `"Maria Torres" "ScaleFlow" podcast`
- `"Maria Torres" webinar OR panel OR fireside`
4. Calls `WebFetch` on the top 4 results.
5. Calls `mcp__claude_ai_Amplemarket__enrich_company` with `domain`: "scaleflow.io".
6. Synthesizes findings and generates output.

**Example output:**

---

**PODCAST PERSONALIZATION BRIEF: Maria Torres**

**Prospect Summary**
Maria Torres is the CRO at ScaleFlow, a Series C revenue operations platform with 320 employees. She joined 14 months ago from Gong where she was VP of Sales. She has appeared on at least 3 podcasts in the past year.

**Podcast Appearances Found**

**1. Revenue Architects Podcast - "Scaling Revenue Without Scaling Headcount"**
- Host: David Kim
- Date: 2026-01-18
- Role: Guest
- Key topics: Revenue efficiency, automation in sales workflows, the myth of "more reps = more revenue"
- Quote: "We cut our SDR team by 30% and actually increased pipeline by 40%. The secret was not hiring more people. It was giving the right people the right signals at the right time."
- Stance: Strongly believes that AI-driven signal routing will replace traditional SDR qualification within 3 years
- Prediction: "By 2028, the SDR role as we know it will be unrecognizable. The companies that figure out signal-based selling first will have a 2-year head start."

**2. SaaStr Sessions - "The CRO Playbook for PLG Companies"**
- Host: Jason Lemkin
- Date: 2025-11-04
- Role: Guest
- Key topics: Product-led growth, sales-assist models, when to hire a CRO
- Quote: "The biggest mistake PLG companies make is waiting too long to layer in sales. By the time they realize they need it, they have left 18 months of enterprise revenue on the table."
- Challenge mentioned: Bridging the gap between self-serve users and enterprise sales motion at ScaleFlow

**3. Women in Revenue - "Breaking Through the CRO Ceiling"**
- Host: Rachel Greenfield
- Date: 2025-08-22
- Role: Guest
- Key topics: Career progression for women in revenue, building executive presence, negotiating CRO roles
- Insight: Shared that she almost turned down the ScaleFlow CRO role because the company had never had a CRO before, so she had to define the role from scratch

**Dynamic Fields**

| Field | Value |
| --- | --- |
| `{{podcast_name}}` | Revenue Architects Podcast |
| `{{podcast_host}}` | David Kim |
| `{{podcast_episode_title}}` | Scaling Revenue Without Scaling Headcount |
| `{{podcast_episode_date}}` | 2026-01-18 |
| `{{podcast_topic}}` | Revenue efficiency and AI-driven signal routing |
| `{{podcast_person_quote}}` | "We cut our SDR team by 30% and actually increased pipeline by 40%." |
| `{{podcast_person_stance}}` | AI-driven signal routing will replace traditional SDR qualification |
| `{{podcast_key_insight}}` | Reduced headcount while increasing pipeline through better signal routing |
| `{{podcast_prediction}}` | SDR role will be unrecognizable by 2028 |
| `{{podcast_shared_interest}}` | Sales automation and revenue efficiency |
| `{{podcast_challenge_mentioned}}` | Bridging PLG self-serve and enterprise sales motion |
| `{{podcast_suggested_opener}}` | See openers below |

**Draft Openers**

1. **Quote-based:** "Maria, I caught your episode on Revenue Architects. The stat about cutting SDRs by 30% while growing pipeline 40% stopped me in my tracks. We are seeing similar patterns with our customers and I would love to share what is working."
2. **Prediction-based:** "Your prediction on the SaaStr podcast about the SDR role being unrecognizable by 2028 really resonated. We are building exactly the kind of signal-based selling layer you described. Would love your take on our approach."
3. **Challenge-based:** "On the SaaStr episode, you mentioned the challenge of bridging PLG self-serve with enterprise sales at ScaleFlow. That is a problem we have helped 3 other Series C companies solve. Happy to share what worked."
4. **Topic-based:** "Loved your take on revenue efficiency over headcount growth on the Revenue Architects pod. Most CROs I talk to are still defaulting to 'hire more reps'. Your signal-based approach is ahead of the curve."
5. **Personal-based:** "Your story on Women in Revenue about defining the CRO role from scratch at ScaleFlow was impressive. Building a revenue org without a blueprint takes a different kind of leadership. Curious how the first year has gone."

---

### Example 2: Prospect Who Hosts Their Own Podcast

**User prompt:** "Research their podcast - Jake Randall, CEO of DataForge"

**What the skill does:**
1. Calls `mcp__claude_ai_Amplemarket__enrich_person` with `name`: "Jake Randall", `company_name`: "DataForge".
2. Runs `WebSearch` queries and discovers Jake is the host of "The Data Stack Show," a podcast with 80+ episodes.
3. Calls `WebFetch` on the podcast landing page and 3 recent episodes to understand his interviewing focus and recurring themes.
4. Calls `mcp__claude_ai_Amplemarket__enrich_company` with `domain`: "dataforge.io".
5. Synthesizes findings.

**Example output (abbreviated):**

---

**PODCAST PERSONALIZATION BRIEF: Jake Randall**

**Prospect Summary**
Jake Randall is the CEO and co-founder of DataForge (dataforge.io), a 150-person Series B data infrastructure company. He hosts "The Data Stack Show," a weekly podcast with 80+ episodes focused on data engineering, modern data stack architecture, and interviews with data leaders.

**Key Finding:** Jake is a podcast HOST, not just a guest. This signals strong thought leadership investment and means he is deeply familiar with the podcast format. Referencing his show directly is more personal than referencing a guest appearance.

**Recurring Themes Across Episodes:**
- Data mesh vs. data warehouse architecture debates
- The "unbundling of Snowflake" thesis
- Real-time data pipelines as competitive advantage
- Hiring and retaining data engineers

**Draft Openers**

1. "Jake, I have been following The Data Stack Show. Your conversation with [recent guest] on real-time pipelines was exactly the debate we are seeing play out with our customers."
2. "As someone who has interviewed 80+ data leaders on your podcast, you have probably heard every take on the modern data stack. Curious if you have seen anyone solving [specific problem] the way we are approaching it."
3. "Your 'unbundling of Snowflake' thesis from The Data Stack Show keeps coming up in conversations I am having with data leaders. Would love to share what we are building in that space. Might make for an interesting episode too."

---

### Example 3: Sparse Results - Only One Appearance Found

**User prompt:** "What podcasts has this person been on - Priya Sharma, VP Eng at NovaTech?"

**What the skill does:**
1. Calls `mcp__claude_ai_Amplemarket__enrich_person` with `name`: "Priya Sharma", `company_name`: "NovaTech".
2. Runs all 5 `WebSearch` query patterns.
3. Only finds 1 relevant result, a webinar panel from 6 months ago.
4. Calls `WebFetch` on that result.
5. Calls `mcp__claude_ai_Amplemarket__enrich_company` with NovaTech's domain.
6. Delivers findings with a transparency note about limited results.

**Example output (abbreviated):**

---

**PODCAST PERSONALIZATION BRIEF: Priya Sharma**

**Prospect Summary**
Priya Sharma is the VP of Engineering at NovaTech (novatech.dev), a 90-person Series A developer tools company. Limited podcast presence found. 1 appearance identified.

**Note:** Only one podcast or media appearance was found. Personalization angles from this single source can still be effective but should be used carefully to avoid appearing overly fixated on a single data point.

**1. DevOps Dialogues Webinar Panel - "Scaling Engineering Teams in a Remote-First World"**
- Date: 2025-09-10
- Role: Panelist (1 of 4)
- Key topics: Remote hiring, async communication, engineering culture at scale
- Paraphrased insight: Discussed NovaTech's approach of hiring senior engineers in non-traditional tech hubs and investing heavily in documentation culture instead of synchronous meetings
- Challenge mentioned: Maintaining engineering velocity while scaling from 20 to 60 engineers

**Draft Openers**

1. "Priya, your point on the DevOps Dialogues panel about documentation culture over sync meetings really stood out. We have seen similar results with our engineering customers who made that shift."
2. "Scaling from 20 to 60 engineers while maintaining velocity is no small feat. You mentioned that challenge at the DevOps Dialogues panel. Curious how that journey has gone since then."

**Dynamic Fields**

| Field | Value |
| --- | --- |
| `{{podcast_name}}` | DevOps Dialogues (webinar panel) |
| `{{podcast_episode_title}}` | Scaling Engineering Teams in a Remote-First World |
| `{{podcast_episode_date}}` | 2025-09-10 |
| `{{podcast_topic}}` | Remote hiring, async communication, engineering culture |
| `{{podcast_key_insight}}` | Investing in documentation culture over synchronous meetings |
| `{{podcast_challenge_mentioned}}` | Maintaining engineering velocity while scaling from 20 to 60 engineers |

**Recommendation:** Given the sparse podcast results, consider supplementing with other personalization approaches. The prospect may be more active on LinkedIn, conference speaking circuits, or in written content (blog posts, technical articles).

---

## Troubleshooting

| Problem | Solution |
| --- | --- |
| No podcast appearances found | Fallback chain: 1) Broaden search to include webinars, panels, fireside chats, YouTube interviews, and conference talks. 2) Search for the prospect's company name + "podcast" to find appearances by colleagues. 3) Be transparent: "No podcast appearances found for [name]. Would you like me to try other personalization approaches (career history, company news, LinkedIn activity)?" |
| Paywall or login blocking content extraction | Note the episode metadata (title, date, podcast name) from the search result snippet and skip full content extraction. Use the metadata for lighter personalization: "I saw you were on [podcast name] discussing [topic from snippet]. Would love to hear more about your perspective." |
| Wrong person returned in search results | Common with common names. Cross-reference podcast results against the enriched person data (title, company, industry). Discard any results that do not match the prospect's profile. If uncertain, ask: "I found a podcast appearance for a [name] but cannot confirm it is the same person. Can you verify?" |
| Podcast content is a transcript with no clear quotes | Scan the transcript for first-person statements by the prospect. Look for patterns like "[prospect name]:" or "Guest:" to isolate their contributions. Paraphrase key points and label them as paraphrased, not direct quotes. |
| Results are outdated (2+ years old) | Flag the age: "Note: This appearance is from [date]. The prospect's views and role may have changed since then." Still usable, but frame openers with temporal awareness: "A couple years back, you mentioned on [podcast] that..." |
| Too many results to process | Prioritize by: 1) Recency (last 12 months first). 2) Relevance to outreach goal. 3) Quality of source (dedicated podcast episode over brief panel mention). Focus on the top 3-5 most valuable appearances. |
| Prospect appeared on a podcast in a different language | Note the language and extract what you can from the episode title and metadata. If show notes are available in English or if the search snippet provides useful context, use that. Flag: "This episode appears to be in [language]. Personalization is based on available metadata only." |
| Search returns podcast appearances for a namesake at a different company | Cross-reference every result against the enriched person's current company, previous companies, and industry. Only include appearances where the company name, title, or topic aligns with the verified prospect profile. When in doubt, exclude the result and note: "Found a possible match but could not confirm identity." |