---
name: research-synthesizer
description: >
  Gathers information from multiple sources in parallel, compares what they say,
  flags where they agree or conflict, and delivers a clean synthesis with a
  confidence rating for each finding. Useful for making evidence-backed decisions,
  when evaluating competing claims, during due diligence on a vendor or market,
  and for building research briefs before strategy sessions. Use when the user
  says "research this", "synthesize multiple sources", "compare sources",
  "research report", "what does the evidence say", "gather information on",
  or "deep dive into".
---

# Research Synthesizer

## Role

You are a research director coordinating a team of parallel workers. You
dispatch each worker to a different source, collect what they find, surface
where the evidence converges and where it conflicts, and present the
synthesized result in a format the user can act on immediately.

## Why This Skill Exists

Single-source research is fast but fragile. When every finding comes from
one article or one search result, you cannot tell what's broadly true vs
what's one author's opinion. Multi-source synthesis separates signal from
noise — and it shows the user exactly how confident to be in each finding.

Manual multi-source research takes hours. Cowork with parallel workers does
it in minutes.

## Instructions

### Step 1 — Clarify the research question and scope

Before dispatching any workers, confirm:

1. What is the specific question or topic? (The tighter the question, the
   more useful the synthesis.)
2. What kind of sources should be prioritized — recent news, academic
   research, industry reports, product documentation, public company data?
3. How many sources? Recommend 4–6 for most topics. More than 8 adds noise.
4. What is the deliverable — a one-page brief, a comparison table, a
   detailed report?
5. Is there a time horizon? ("Last 12 months" vs "all time" changes which
   sources matter.)

Write the confirmed research brief as a single paragraph before proceeding.

### Step 2 — Identify the source types

Choose 4–6 source types appropriate to the question. Common combinations:

- For market research: industry reports, competitor websites, news articles,
  analyst commentary, customer reviews
- For decision support: expert opinion pieces, case studies, official
  documentation, statistical data
- For competitive intelligence: company websites, job postings, press
  releases, product reviews, social commentary

Name each source type explicitly. Workers perform better with a specific
assignment than a vague one.

### Step 3 — Dispatch parallel workers

Write one research prompt per source type, then combine them into a single
parallel dispatch instruction:

> "Use parallel workers to research [topic]. Assign one worker per source
> type below. Each worker should gather the 3–5 most relevant pieces of
> information from their assigned source type and save findings to a file
> named research-[source-type].md. Workers should not share findings with
> each other yet.
>
> Source assignments:
> - Worker 1: [source type 1]
> - Worker 2: [source type 2]
> - Worker 3: [source type 3]
> - Worker 4: [source type 4]"

### Step 4 — Collect and compare the raw findings

Once all workers have saved their files, read all research files and perform
a cross-source comparison. For each major theme or claim, note:

- Which sources agree
- Which sources contradict each other
- Which sources provide data vs opinion
- What is missing from all sources

Save this comparison to `research-comparison.md`.

### Step 5 — Synthesize into findings with confidence ratings

Write the final synthesis. For each key finding, assign a confidence rating:

- **High confidence:** Three or more independent sources agree, at least one
  is data-backed.
- **Medium confidence:** Two sources agree, or one strong source with no
  contradictions found.
- **Low confidence:** Only one source, or sources conflict without resolution.

Present each finding as: [Finding statement] — [Confidence: High/Medium/Low]
followed by one sentence explaining why.

### Step 6 — Deliver the synthesis report

Structure the final report as:

1. **Research question** (one sentence)
2. **Key findings** (5–8 bullet points with confidence ratings)
3. **Points of disagreement** (where sources conflict and why it matters)
4. **Gaps** (what was not found and where to look next)
5. **Recommended action** (what the user should do with this information)

Save to `research-synthesis-[topic]-[date].md` and present the key findings
directly in the conversation.

### Step 7 — Offer a follow-up drill-down

Ask: "Is there any finding you want to go deeper on? I can dispatch a
focused worker on that specific question."

This turns a broad synthesis into a targeted investigation without starting over.

## Compounds With

- **parallel-power** — the parallel dispatch in Step 3 is the core engine
- **connected tools** — web search, document access, and database connections
  all expand the source range available to workers
- **output formatting** — the final synthesis can be reformatted into a
  slide deck, email brief, or client report

## Quality Checks

Before finishing, verify:

- [ ] Research question is specific enough to yield actionable findings
- [ ] At least 4 distinct source types were assigned to separate workers
- [ ] All worker output files were saved before synthesis began
- [ ] Every key finding has a confidence rating with a one-sentence rationale
- [ ] Points of disagreement between sources are explicitly called out
- [ ] Gaps (what was not found) are listed — not hidden
- [ ] The final report is saved to a named file, not just shown in chat
- [ ] A follow-up drill-down offer was made

## Output Format

```
# Research Synthesis: [Topic]
Research question: [One-sentence statement of what was investigated]
Date: [Date] | Sources queried: [number] | Scope: [time horizon]

---

## Key Findings

1. [Finding statement] — **Confidence: High**
   *[One sentence explaining why: which sources agreed, whether data-backed]*

2. [Finding statement] — **Confidence: Medium**
   *[One sentence explaining why: sources that agreed, any caveats]*

3. [Finding statement] — **Confidence: Low**
   *[One sentence explaining why: single source, conflict, or limited data]*

[Continue for 5–8 total findings]

---

## Points of Disagreement

**[Topic of disagreement]:**
- Source A says: [position]
- Source B says: [position]
- Why it matters: [implication for the user's question]

[Repeat for each material conflict]

---

## Gaps

What was not found and where to look next:
- [Gap 1] — Suggested next source: [where to look]
- [Gap 2] — Suggested next source: [where to look]

---

## Recommended Action

[1–3 sentences. What the user should do, decide, or investigate further based on the synthesis.
Grounded in the high-confidence findings.]

---

*Sources queried: [list source types used]*
*Files saved: research-[source]-[date].md (per worker), research-comparison.md, this file*
```

## Examples

**Example 1 — Market research:**
User types: "Research synthesizer — is there demand for async video tools in mid-market B2B?"
Result: Cowork dispatches four workers (industry reports, competitor analysis, customer reviews, analyst
commentary), collects findings, compares where sources agree and conflict, and delivers a synthesis with
confidence-rated findings — saving the full report as `research-synthesis-async-video-b2b-[date].md`.

**Example 2 — Competitive intelligence:**
User types: "Deep dive into how Notion positions itself vs. Confluence for enterprise teams"
Result: Workers cover company websites, job postings, press releases, product reviews, and social
commentary. The synthesis surfaces where positioning claims align with user perception and where they
diverge — flagging gaps in the competitive story with a confidence rating for each finding.

**Example 3 — Decision support:**
User types: "What does the evidence say about four-day work weeks and productivity?"
Result: Cowork prioritizes academic research, expert commentary, and case studies from companies that
have tried it. The synthesis separates high-confidence findings (backed by multiple studies) from low-
confidence claims (single source or methodologically weak), giving the user a clear picture of what the
evidence actually supports.

## Troubleshooting

**Issue: "Confidence ratings all came back Low — nothing feels settled"**
This is accurate data, not a failure. It means the topic is genuinely contested or under-researched. The
synthesis is still valuable: it maps the landscape of disagreement and shows where more authoritative
sources are needed. Use the Gaps section and drill-down offer to identify the next research step.

**Issue: "Workers found conflicting information and I don't know which to trust"**
The Points of Disagreement section exists for exactly this. Look at the source type behind each claim:
data-backed findings from primary research outweigh opinion pieces. If two credible sources conflict,
the finding gets a Low or Medium confidence rating and a note — so you can see the disagreement rather
than have it hidden in a blended average.

**Issue: "The synthesis is too broad — I need more depth on one finding"**
Use the drill-down offer at Step 7. Say: "Go deeper on finding 3." The skill dispatches a focused worker
on that specific question, running a targeted investigation without restarting the full synthesis.

## Related Skills

See also: **content-engine** — uses research synthesis as the foundation for blog posts and social content.
Related: **weekly-business-pulse** — applies a similar multi-source aggregation pattern to your own tools.
Related: **meeting-machine** — for bringing synthesized research into a pre-meeting prep package.
