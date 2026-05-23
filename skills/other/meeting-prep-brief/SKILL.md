---
name: meeting-prep-brief
description: "Use when preparing for a sales meeting, discovery call, demo, or customer check-in. Triggers: 'prep me for a meeting with [company]', 'meeting brief for [company]', 'pre-call prep', 'I have a call with [contact] at [company]', 'meeting prep', 'call prep'."
version: 1.0.0
---

# Meeting Prep Brief

Generate a concise pre-call intelligence brief in 2-3 minutes. Everything you need before walking into a meeting: company context, stakeholder profile, competitive landmines, talking points, and a proposed agenda. Uses WebSearch for real-time intelligence and builds on existing account research when available.

## Steps

### 1. Collect Input

Ask the user for the following:

- **Company name** (required)
- **Contact name and title** (required) — who you are meeting with
- **Meeting type** (required) — one of: discovery call, demo, follow-up, QBR, negotiation
- **Your product/service** (optional) — if provided, talking points and agenda will be tailored to the user's offering
- **Deal context** (optional) — past conversations, where they are in the funnel, previous meetings, known objections
- **Specific questions** (optional) — anything the user wants answered or addressed during the meeting

Do NOT proceed until you have the company name, contact name/title, and meeting type.

### 2. Check Existing Intelligence

Use Glob to check for existing files that can accelerate the brief:

- `docs/accounts/{company}.md` — account research brief (from the Account Research Brief skill)
- `docs/signals/{company}.md` — signal data (from the Signal Scanner skill)
- `docs/pipeline/scored-leads.md` — qualification score
- `docs/icp.md` — ICP match assessment

**If any of these exist:** Read them. Summarize what you loaded. Skip redundant research in subsequent steps and build on the existing intelligence instead.

**If none exist:** Proceed with full research from Step 3 onward.

### 3. Company Context

Skip this step if a recent account brief already exists at `docs/accounts/{company}.md`.

Run 2-3 WebSearch queries (e.g., `"{company} what does it do"`, `"{company} news 2026"`, `"{company} funding"` ).

Gather:

- What they do (one paragraph, plain language)
- Recent news from the last 30 days (1-3 headlines with source URLs)
- Key metrics: funding stage, total raised, headcount, revenue range (if public)
- Current challenges or priorities — inferred from press releases, job postings, executive interviews, or earnings calls

If any data point is not findable, write "Not found." NEVER fabricate company data.

### 4. Stakeholder Profile

Run 2-3 WebSearch queries focused on the specific contact (e.g., `"{contact name}" "{company}"`, `"{contact name}" LinkedIn`, `"{contact name}" podcast OR conference OR interview`).

Gather:

- **Current role and tenure** — title, how long they have been in this position
- **Career history** — where they worked before, what they did (1-2 sentences)
- **Public content** — LinkedIn articles, podcast appearances, conference talks, blog posts, tweets. Include URLs where found.
- **Communication style clues** — are they technical or business-oriented? Data-driven or narrative-driven? Formal or casual? Infer from their content and background.
- **What they likely care about** — based on their role and company context, what metrics, outcomes, and problems occupy their day
- **Potential common ground** — shared background, interests, mutual connections, or overlapping communities

**Rules for this step:**
- If WebSearch returns nothing about the contact, say "No public profile found for {contact name}. Recommend checking LinkedIn directly before the call." Do NOT fabricate biographical details.
- Do not guess at personality traits without evidence. Only note communication style clues when backed by observed content.

### 5. Competitive Landmines

Run 2-3 WebSearch queries (e.g., `"{company}" uses "{competitor tool}"`, `"{company}" tech stack job postings`, `"{company}" case study "{competitor}"`).

Gather:

- **Current tools/solutions** in the user's product category — detected from job postings, integrations pages, case studies, G2 reviews, or tech stack analysis tools
- **Competitor relationships** — are they an existing customer of a competitor? Have they published a case study or testimonial with them? Are they listed on a competitor's customer page?
- **Potential objections** based on the competitive situation (e.g., switching costs, existing contract, "good enough" inertia)
- **Positioning recommendations** — 1-2 sentences on how to position against the incumbent (if one is identified) or how to frame the conversation if no competitor is in place

If the user did not provide their product/service, keep this section general: focus on what solutions the company uses in their operations, and flag any vendor relationships that could be relevant.

### 6. Meeting-Type Specific Prep

Generate questions and preparation items based on the meeting type the user specified.

#### For Discovery Calls

- **5 open-ended questions** to understand their current state (process, tools, team structure, priorities)
- **3 pain-probing questions** based on likely challenges inferred from the company context and stakeholder profile
- **2 vision questions** ("Where do you want to be in 12 months?" style)
- **Red flags to watch for** — 3-4 signals during the call that indicate this prospect is not a fit (e.g., no budget allocated, evaluating in 12+ months, no pain acknowledged)

#### For Demos

- **3 most relevant features/capabilities to show** — based on the contact's likely pain points and company context
- **Potential "wow moment"** — one thing to lead with that will immediately resonate
- **3 objections to prepare for** — based on competitive landscape and company situation
- **1-2 success stories** — describe the type of similar company/use case to reference (e.g., "a Series B fintech that cut onboarding time by 40%"). Do not fabricate specific customer names.

#### For Follow-ups

- **Previous context summary** — restate what the user provided about past conversations
- **3 questions that should have been asked** — gaps to fill based on what a thorough discovery would cover
- **New information since last meeting** — any recent signals (funding, hires, news) discovered during research
- **2-3 proposed next steps** to discuss on the call

#### For QBRs (Quarterly Business Reviews)

- **3 value-delivered themes** to highlight (ask user for specific wins if not provided)
- **Expansion opportunities** — based on company signals, where could the engagement grow
- **3 strategic questions** to deepen the relationship and uncover new needs
- **Renewal risk signals** — anything from research that suggests dissatisfaction or competing priorities

#### For Negotiations

- **Their likely concerns and priorities** — inferred from company stage, funding situation, and role
- **Walk-away point** — ask the user: "What is the minimum you would accept?"
- **Value framing for pricing discussions** — 2-3 ways to anchor the conversation on value, not cost
- **Terms they will likely push back on** — common objections for their company profile (payment terms, commitment length, scope)

### 7. Talking Points

Generate **5-7 talking points**, each tied to a specific finding from the research.

Structure each talking point as:

> **Because** [specific finding from research], **mention** [what to say] **to** [achieve what goal].

Rules:
- Every talking point must reference a concrete finding, not a generic observation. "Because they just raised a $15M Series B" is good. "Because they are growing" is too vague.
- Include one **"wild card" insight** — something unexpected that shows deep preparation (an obscure interview quote, a niche community they participate in, a pattern in their hiring, a regulatory change affecting their industry). Label this one as the wild card.
- If the user provided their product/service, talking points should connect findings to the user's value proposition. If not, keep them conversational and insight-driven.

### 8. Proposed Agenda

Generate a meeting agenda with time allocations. Default to a 30-minute meeting unless the user specifies otherwise.

Structure:

| Time | Section | Details |
|------|---------|---------|
| 0-3 min | **Opening & Rapport** | {Specific rapport-building topic based on common ground found in Step 4} |
| 3-X min | **Core Discussion** | {Varies by meeting type — discovery questions, demo flow, review items} |
| X-Y min | **Questions** | {Top 3 questions to ask, drawn from Step 6} |
| Y-end min | **Next Steps & Close** | {Specific next step to propose based on meeting type} |

Note at the bottom: _"This agenda is a starting point. Adapt based on the conversation flow. Follow the prospect's energy — if they light up on a topic, go deeper there."_

### 9. Write the Brief

Write the output file to `docs/meeting-prep/{company-name-slug}-{YYYY-MM-DD}.md`.

The slug is the company name lowercased with spaces replaced by hyphens and special characters removed (e.g., "HubSpot" becomes `hubspot`, "Scale AI" becomes `scale-ai`).

Create the `docs/meeting-prep/` directory if it does not exist.

Use this structure for the output file:

```markdown
# Meeting Prep Brief: {Company Name}

| | |
|---|---|
| **Company** | {Company Name} |
| **Contact** | {Contact Name}, {Title} |
| **Meeting Type** | {Type} |
| **Date** | {YYYY-MM-DD} |
| **Prepared** | {YYYY-MM-DD} |

---

## Company Context

{One paragraph on what they do}

- **Founded:** {year}
- **HQ:** {location}
- **Employees:** {count or range}
- **Funding:** {stage, total raised}

### Recent News
- {headline} — [{source}]({url}) ({date})
- ...

---

## Stakeholder Profile: {Contact Name}

**Role:** {title} at {company} ({tenure if known})

**Background:** {career history, 2-3 sentences}

**Public Content:**
- {content item with URL}
- ...

**Communication Style:** {observations based on evidence}

**Likely Priorities:** {what they care about based on role and context}

**Common Ground:** {shared interests, background, connections}

---

## Competitive Landscape

**Current Stack:** {tools/solutions they use in your category}

**Competitor Relationships:** {known vendor relationships}

**Potential Objections:**
- {objection 1}
- {objection 2}
- {objection 3}

**Positioning Recommendation:** {how to frame against incumbents}

---

## Talking Points

1. **Because** {finding}, **mention** {point} **to** {goal}.
2. **Because** {finding}, **mention** {point} **to** {goal}.
3. **Because** {finding}, **mention** {point} **to** {goal}.
4. **Because** {finding}, **mention** {point} **to** {goal}.
5. **Because** {finding}, **mention** {point} **to** {goal}.
6. *Wild Card:* **Because** {unexpected finding}, **mention** {point} **to** {goal}.

---

## Questions to Ask

### {Category based on meeting type}
- {question 1}
- {question 2}
- {question 3}

### {Category 2}
- {question 4}
- {question 5}

### {Category 3}
- {question 6}
- {question 7}

---

## Proposed Agenda ({duration} minutes)

| Time | Section | Details |
|------|---------|---------|
| 0-3 min | Opening & Rapport | {specific topic} |
| ... | ... | ... |

_This agenda is a starting point. Adapt based on the conversation flow. Follow the prospect's energy — if they light up on a topic, go deeper there._

---

## Sources

- [{description}]({url})
- ...
```

After writing the file, tell the user the file path and offer to adjust any section before the meeting.

## Tools

- **WebSearch** — primary tool. Run 8-12 searches to cover company context, stakeholder profile, and competitive landscape. Batch independent searches into the same message to run them in parallel.
- **Read** — load existing account briefs, signal reports, ICP definition, and pipeline scores when available.
- **Write** — output the final brief to `docs/meeting-prep/{company-name-slug}-{date}.md`.
- **Glob** — check for existing intelligence files before starting research.

## Rules

1. **Speed is the value.** The entire brief should take 2-3 minutes. Do not over-research. Run searches in parallel when possible. If an account brief already exists, skip redundant research and build on it.
2. **One page, scannable.** The brief should be concise enough to review in 3 minutes before walking into the meeting. Use bullets, tables, and short sentences. No filler paragraphs.
3. **Talking points must be specific.** "Mention their recent Series B" is good. "Build rapport" is useless. Every talking point must reference a concrete finding.
4. **Never fabricate.** If WebSearch returns nothing about the contact, say so. If you cannot find their tech stack, say "Not found." Never guess at names, titles, career history, or company data.
5. **Always cite sources.** Every factual claim must trace back to a URL in the Sources section. Include URLs inline where relevant.
6. **Build on existing intelligence.** If account briefs, signal reports, or ICP docs already exist in the project, use them. Do not duplicate work that has already been done.
7. **Meeting type drives the prep.** The questions, agenda, and talking points should be shaped by whether this is a discovery call, demo, follow-up, QBR, or negotiation. Do not give discovery questions for a demo.
8. **The agenda is a suggestion.** Always note that the agenda should be adapted to the conversation flow. Never present it as rigid.
9. **No internal references.** This skill is part of a public playbook. Never reference proprietary tools, databases, internal agents, or vendor accounts.
10. **Works universally.** This skill works for any B2B seller preparing for any meeting. Do not assume a specific industry, company size, or GTM motion.
11. **Create directories as needed.** If `docs/meeting-prep/` does not exist, create it before writing the file.
