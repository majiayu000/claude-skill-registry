---
name: icp-architect
description: "Use when building or refining an Ideal Customer Profile (ICP), defining target personas, mapping buyer psychographics, or discovering where prospects gather online. Triggers: 'build my ICP', 'define target customer', 'who should I sell to', 'refine ICP', 'persona mapping'."
version: 1.0.0
---

# ICP Architect

Build a comprehensive Ideal Customer Profile through an interactive discovery process. This skill asks questions, pressure-tests assumptions, and produces a reference-ready `docs/icp.md` that other skills in the playbook can consume.

---

## Activation

When the user triggers this skill, follow the steps below **in order**. Do NOT skip the discovery interview. Do NOT produce output before gathering all answers.

---

## Step 0 — Check for Existing ICP

Use `Read` to check if `docs/icp.md` already exists in the current working directory.

- **If it exists:** Read the file, present a summary to the user, and ask: _"You already have an ICP on file. Do you want to (A) refine it, (B) start fresh, or (C) add a new segment?"_
  - If **refine**: Load the existing content as context. During the discovery interview, pre-fill answers from the existing file and only ask about gaps or changes.
  - If **start fresh**: Proceed with the full interview from scratch. The old file will be overwritten at the end.
  - If **add segment**: Skip to Step 2 (ICP Segmentation) and ask only the questions needed to define the new segment and its personas. Append to the existing file.
- **If it does not exist:** Proceed to Step 1.

---

## Step 1 — Discovery Interview (Interactive)

Present these questions to the user **all at once** in a numbered list. Tell the user they can answer inline (numbered) or paste a block of text and you will extract the answers.

Ask exactly these questions:

```
I need to understand your business before building your ICP. Answer these 10 questions — be as specific as possible. One-word answers are fine where they fit; paragraphs are fine where they don't.

1. What does your product do? (one sentence)
2. Who is your current best customer? Why are they your best?
3. What's your ACV or typical deal size range?
4. How long is your typical sales cycle? (days/weeks/months)
5. Who signs the check? (job title, not a person's name)
6. What's the trigger event that makes someone start looking for your solution?
7. What were they doing before your product? (the "old way" — spreadsheets, manual process, a competitor, nothing?)
8. What happens if they do nothing? (cost of inaction — lost revenue, compliance risk, wasted time?)
9. What's your unfair advantage vs. the next best alternative?
10. (Optional) Paste 3-5 LinkedIn profile URLs of your best customers. I'll extract patterns from their titles, industries, and company sizes.
```

**Rules for this step:**
- Wait for the user to respond before proceeding. Do NOT generate placeholder answers.
- If any critical answer is vague (especially questions 1, 2, 5, 6), ask a focused follow-up before moving on. At most 2 follow-up rounds.
- If the user provides LinkedIn URLs (question 10), use `WebSearch` to look up those profiles and extract: job title, company size, industry, and any patterns across the set.

---

## Step 2 — ICP Segmentation

From the user's answers, define **2-3 ICP segments**. Present them to the user in a table for validation before going deeper.

For each segment, define:

| Field | Description |
|---|---|
| **Segment name** | Short label (e.g., "Mid-Market SaaS", "Enterprise Financial Services") |
| **Company stage** | Seed / Series A / Series B / Growth / Enterprise |
| **Company size** | Employee count range and/or revenue range |
| **Industries** | 2-5 specific verticals |
| **Budget range** | What they typically spend on solutions like this |
| **Sales cycle** | Expected length for this segment |
| **Decision maker(s)** | Title(s) of the person who signs or champions |
| **Core problem** | One sentence describing why they buy |
| **Pain points** | 3-5 specific, concrete pains (not generic fluff) |

**Rules for this step:**
- Ground every segment in the user's actual answers. Do not invent segments that contradict what the user told you.
- If the user's answers suggest only 1 clear segment, define that one plus a plausible adjacent segment and ask if it resonates.
- After presenting the segments, ask: _"Do these segments look right? Should I adjust, merge, or add any?"_
- Wait for confirmation before proceeding to Step 3.

---

## Step 3 — Persona Deep-Dive

For each confirmed ICP segment, build **1-2 personas**. Each persona is a fictional archetype representing a real buyer.

For each persona, define:

| Field | Description |
|---|---|
| **Archetype name** | A memorable label (e.g., "The Overwhelmed VP of Ops", "The Data-Driven CRO") |
| **Job title** | Exact title(s) this persona holds |
| **Reports to** | Who they report to (affects how they justify purchases) |
| **Company context** | What kind of company they work at (size, stage, situation) |
| **Daily frustrations** | 3-5 things that make their job hard right now |
| **Goals & success metrics** | What they are measured on / what "good" looks like for them |
| **Buying behavior** | How they research solutions (Google, Reddit, peer referrals, analyst reports, etc.) |
| **Trust triggers** | What makes them believe a vendor (case studies, free trials, peer recommendations, etc.) |
| **Red flags** | What makes them walk away (long contracts, no integrations, pushy sales, etc.) |
| **Language patterns** | 5-10 actual phrases they use to describe their problem — the words they type into Google, say on sales calls, or post on Reddit. These should sound like real speech, not marketing copy. |

**Rules for this step:**
- Language patterns are the most important field. Get these right. They drive content, ads, and outreach messaging downstream.
- Present personas to the user and ask for corrections before proceeding.

---

## Step 4 — Community & Channel Discovery

For each persona, identify where they spend time online and offline. **Use `WebSearch` to validate every community you suggest.** Do not guess subreddit names or Slack community names -- verify they exist.

For each persona, produce:

### Online Communities
| Channel Type | Specific Communities |
|---|---|
| **Subreddits** | 5-8 subreddits (use WebSearch: search `reddit.com {topic} {persona role}` to find active, relevant subs). Include subscriber count if available. |
| **LinkedIn groups & hashtags** | 3-5 groups, 5-8 hashtags |
| **Slack / Discord communities** | 2-4 (use WebSearch to find open communities in the persona's space) |
| **Newsletters** | 3-5 newsletters they likely subscribe to |
| **Podcasts** | 3-5 podcasts relevant to their role and problems |
| **Events / Conferences** | 2-4 industry events (in-person or virtual) |
| **Thought leaders** | 5-8 people this persona follows or respects (with LinkedIn or Twitter handles where findable) |

**Rules for this step:**
- Every subreddit must be verified via WebSearch. If a search returns no evidence the subreddit exists and is active, drop it and find one that does.
- Prefer communities with actual activity (posts in the last 30 days, >1K members for subreddits) over theoretical matches.
- Include at least 1-2 non-obvious or "hidden gem" communities per persona -- places competitors are unlikely to be watching.

---

## Step 5 — Buying Signals Mapping

Define **8-12 signals** that indicate a company or person matching the ICP is in a buying window.

For each signal:

| Field | Options / Description |
|---|---|
| **Signal** | What happened (e.g., "Posted a job listing for their first RevOps hire") |
| **Where to find it** | LinkedIn, job boards, press releases, G2 reviews, Reddit, SEC filings, tech stack tools, etc. |
| **Signal strength** | **Strong** (high intent, act now) / **Moderate** (worth monitoring) / **Weak** (early awareness) |
| **Recommended action** | What to do when you spot this signal (e.g., "Send a personalized cold email referencing the hire", "Add to nurture sequence", "Flag for SDR review") |

**Rules for this step:**
- At least 3 signals must be "Strong."
- Signals should be observable and actionable -- not vague ("they seem interested"). Every signal must answer: where exactly would I see this?
- Include a mix of digital signals (job posts, tech installs, content engagement) and real-world signals (funding rounds, leadership changes, regulatory shifts).

---

## Step 6 — Disqualification Criteria

Define **3-5 hard disqualifiers** -- characteristics that mean a prospect is NOT a fit, no matter how interested they seem.

For each disqualifier:

| Field | Description |
|---|---|
| **Criterion** | What makes them a non-fit (e.g., "Company has fewer than 10 employees") |
| **Why** | Why this is a dealbreaker (e.g., "ACV too small to justify sales cycle length") |
| **How to detect early** | Where / when in the process you can spot this before wasting time |

**Rules for this step:**
- These should be based on the user's actual experience (from the discovery interview) plus logical inference from the ICP segments.
- Ask the user: _"Are there any other dealbreakers I'm missing from your experience?"_ before finalizing.

---

## Step 7 — Output

After all steps are confirmed, write the complete ICP to `docs/icp.md` using `Write`.

### File Structure

```markdown
# Ideal Customer Profile
> Generated by ICP Architect | Last updated: {YYYY-MM-DD}

## Company Overview
- **Product:** {one-sentence description from Q1}
- **ACV Range:** {from Q3}
- **Sales Cycle:** {from Q4}
- **Key Decision Maker(s):** {from Q5}

---

## ICP Segments

### Segment 1: {Name}
{Full segment table from Step 2}

### Segment 2: {Name}
{Full segment table from Step 2}

---

## Personas

### {Archetype Name} ({Segment Name})
{Full persona details from Step 3}

#### Where They Hang Out
{Community & channel table from Step 4}

---
{Repeat for each persona}

## Buying Signals

| # | Signal | Source | Strength | Action |
|---|--------|--------|----------|--------|
| 1 | ... | ... | Strong | ... |
{Full table from Step 5}

---

## Disqualification Criteria

| # | Criterion | Why | Early Detection |
|---|-----------|-----|-----------------|
| 1 | ... | ... | ... |
{Full table from Step 6}

---

## Language Bank
> Phrases your personas actually use. Reference these in outreach, content, and ad copy.

### {Persona 1 Name}
- "{phrase 1}"
- "{phrase 2}"
...

### {Persona 2 Name}
- "{phrase 1}"
- "{phrase 2}"
...

---

## Quick Reference — Who to Target

| Segment | Decision Maker | Trigger Event | Best Channel |
|---------|---------------|---------------|--------------|
| {Segment 1} | {Title} | {Trigger from Q6} | {Top channel from Step 4} |
| {Segment 2} | {Title} | {Trigger from Q6} | {Top channel from Step 4} |

---
*This file is a living document. Rerun the ICP Architect skill to refine as you learn more from customers and deals.*
```

### Post-Output Actions

After writing the file:
1. Confirm to the user: _"Your ICP has been written to `docs/icp.md`."_
2. Provide a brief summary: number of segments, number of personas, number of buying signals, and the top 3 communities discovered.
3. Suggest next steps: _"Now that your ICP is defined, you can use it as input for outreach sequences, content strategy, or competitive research."_

---

## Tools Used

| Tool | Purpose |
|---|---|
| `Read` | Check if `docs/icp.md` already exists |
| `Write` | Output the final ICP document |
| `WebSearch` | Validate subreddit names, find Slack/Discord communities, discover newsletters, podcasts, and thought leaders |

---

## Rules (Non-Negotiable)

1. **Interactive first, output second.** Never skip the discovery interview. Never generate the ICP from assumptions alone.
2. **Ask all questions before producing output.** Do not drip-feed one question at a time (unless following up on a vague answer). Present the full question set, let the user answer, then build.
3. **Validate communities with WebSearch.** Do not hallucinate subreddit names, Slack groups, or newsletters. If you cannot verify it exists, do not include it.
4. **Get user confirmation at each milestone.** Confirm segments (Step 2) and personas (Step 3) before going deeper. The user is the expert on their own business.
5. **Language patterns must sound human.** They should read like something typed into a search bar or said on a sales call -- not like marketing copy.
6. **The output file must be self-contained.** Anyone reading `docs/icp.md` should understand the full ICP without needing additional context.
7. **No proprietary references.** This skill is public. Do not reference internal tools, databases, client names, or private infrastructure.
8. **Prefer depth over breadth.** Two deeply-researched segments beat five shallow ones. Three real buying signals beat twelve generic ones.
