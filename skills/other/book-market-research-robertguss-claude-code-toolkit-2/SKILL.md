---
name: book-market-research
description: Assess commercial viability of book concepts for Amazon KDP self-publishing. Use when the user has a Book Concept Document and wants to understand market demand, competition, pricing, and positioning before committing to write. Produces a Market Research Report with viability scorecard and Go/No-Go recommendation. Works standalone (commercial analysis only) or after idea-validator (integrated assessment). Nonfiction only.
---

# Market Research

Determine if a book is worth writing from a business perspective, specifically for Amazon KDP self-publishing.

## Core Philosophy

**Commercial viability is separate from intellectual merit.** A brilliant idea can fail commercially. A mediocre idea can succeed. This skill assesses the market, not the idea itself.

**Better to know the odds now.** Authors deserve realistic expectations before investing months in writing.

**Author intent shapes interpretation.** A 5/10 viability score means different things to someone seeking income versus someone writing for legacy. Same data, different recommendations.

**Claude does the analysis; human gathers the data Claude can't access.** Claude performs qualitative research via web search. For quantitative data (BSR, prices, review counts), Claude provides a pre-filled spreadsheet and field guide—human gathers the numbers and brings them back.

## Dependency Model

**Standalone Mode:** Book Concept Document only → pure commercial analysis. Claude flags that intellectual validation hasn't been done and recommends `idea-validator` if concerns arise.

**Post-Validation Mode:** Book Concept Document + Validation Report → integrated assessment. Combines intellectual merit with commercial viability for definitive pipeline gate.

## Author Intent

**Ask before researching.** Author intent determines how to interpret the viability score.

| Intent               | Description                              | Score Interpretation                               |
| -------------------- | ---------------------------------------- | -------------------------------------------------- |
| **Income**           | Book must generate meaningful revenue    | Score is decisive—low score means revise or kill   |
| **Authority**        | Position as expert, book is a credential | Moderate score acceptable if positioning is strong |
| **Passion/Legacy**   | "This book needs to exist"               | Low score = proceed with eyes open, not a blocker  |
| **Lead Generation**  | Funnel for services/consulting           | Score less critical if book serves the funnel      |
| **Audience Service** | Serving existing followers               | Platform strength matters more than market size    |

## Session Modes

**Quick Assessment (single session):**

- Claude-only qualitative analysis via web search
- Identifies competitors, positioning gaps, review themes
- Produces preliminary viability assessment
- No manual data gathering required
- Best for: early-stage filtering, passion/legacy authors, authors with KDP experience

**Deep Dive (multi-session):**

- Full qualitative analysis PLUS quantitative data
- Claude provides pre-filled CSV with competitor URLs
- Human gathers BSR, prices, review counts from Amazon
- Claude analyzes completed data for full scorecard
- Best for: income-focused authors, competitive categories, first-time KDP authors

**Claude recommends mode** based on author intent, validation status, category competitiveness, and KDP experience.

## Session Flow

### Starting Research

1. Ask for Book Concept Document (and Validation Report if available)
2. Read carefully, note the core thesis and target reader
3. Ask about author intent (Income/Authority/Passion/Lead Gen/Audience Service)
4. Recommend session mode with reasoning
5. User confirms mode
6. Proceed to research

### Quick Assessment Flow

1. Search for competing books in the category
2. Analyze search results for:
   - Competitor titles, authors, positioning
   - Bestseller badges (indicator of demand)
   - Publisher patterns (traditional vs. self-pub)
   - Review themes from Goodreads/snippets
3. Identify market gaps from complaint patterns
4. Assess author credibility fit
5. Produce preliminary Market Research Report

### Deep Dive Flow

**Phase 1: Qualitative Research**

1. Perform Quick Assessment steps
2. Identify 5-8 key competitors for quantitative analysis
3. Generate pre-filled `competitor-analysis.csv` with:
   - Title, Author, Amazon URL (filled by Claude)
   - BSR, prices, reviews, rating, pages, KU status (for human to fill)
4. Provide Amazon Field Guide (see `references/amazon-field-guide.md`)
5. Output CSV file for user

**Phase 2: Human Data Gathering**

- User opens CSV in Excel/Sheets
- User visits each Amazon URL (~10 min for 5-8 books)
- User fills in the quantitative fields
- User uploads completed CSV

**Phase 3: Quantitative Analysis**

1. Parse completed CSV
2. Calculate market indicators:
   - Average BSR (demand signal)
   - Price range and median
   - Review velocity patterns
   - KU saturation
3. Score each criterion
4. Produce full Market Research Report with viability scorecard

### Ending Any Session

1. Summarize what was accomplished
2. Output all documents as files
3. State clearly what comes next
4. If mid-Deep-Dive: remind about CSV and field guide

## Viability Scorecard

| Criterion              | Weight | What It Measures                                                        |
| ---------------------- | ------ | ----------------------------------------------------------------------- |
| Market Demand          | 25%    | Are people buying books in this space? BSR patterns, bestseller signals |
| Review Landscape       | 15%    | Review counts/ratings, gap signals from complaints                      |
| Competition Gap        | 15%    | Differentiation opportunity, positioning white space                    |
| Author Credibility     | 15%    | Does author's background match the claims?                              |
| Pricing Viability      | 10%    | Can price competitively and maintain margin?                            |
| Author Platform        | 10%    | Existing audience for launch velocity                                   |
| Timing                 | 5%     | Trend momentum vs. evergreen stability                                  |
| Production Feasibility | 5%     | Can this realistically be written?                                      |

**Scoring:** Each criterion rated 1-10. Weighted average produces overall score.

## Score Interpretation

| Score   | Label              | Meaning                                       |
| ------- | ------------------ | --------------------------------------------- |
| 7.0+    | **Strong Go**      | Market conditions favor success               |
| 5.5–6.9 | **Conditional Go** | Viable with strategic adjustments             |
| 4.0–5.4 | **Revise**         | Significant concerns—reposition or reconsider |
| <4.0    | **Kill**           | Market conditions unfavorable                 |

**Intent Overlay:**

- Income authors: Follow score literally
- Authority authors: Conditional Go sufficient if positioning is strong
- Passion authors: Even Kill score = "proceed with eyes open"
- Lead Gen authors: Platform fit matters more than raw score

## Research Methods

Claude performs qualitative research via web search. See `references/research-methods.md` for detailed methodology.

**What Claude CAN assess via search:**

- Competitor titles, authors, positioning
- Bestseller badges (demand indicator)
- Publisher patterns
- Review themes and complaints
- Market gaps and opportunities
- Author credibility signals

**What requires human data gathering:**

- Best Sellers Rank (BSR)
- Exact prices (Kindle, paperback, hardcover)
- Review counts and star ratings
- Page counts
- Kindle Unlimited status
- Category rankings

For human data gathering, Claude provides a pre-filled CSV and the Amazon Field Guide from `references/amazon-field-guide.md`.

## Market Research Report Structure

Use template from `assets/templates/market-research-report.md`.

1. **Executive Summary** — 2-3 sentences, overall assessment, recommendation
2. **Author Intent & Interpretation** — how intent shapes the recommendation
3. **Viability Scorecard** — weighted scores with reasoning
4. **Competitive Landscape** — top competitors, their positioning, gaps
5. **Target Reader Analysis** — refined reader persona, underserved needs
6. **Positioning Recommendation** — how to differentiate
7. **Pricing Recommendation** — based on market analysis
8. **Title/Subtitle Direction** — market-informed suggestions
9. **Platform Fit Assessment** — author's existing audience leverage
10. **Timing Assessment** — trend vs. evergreen
11. **Key Risks** — what could derail commercial success
12. **Recommendation** — Go / Conditional Go / Revise / Kill with reasoning

## Handoff

**To book-architect (if Go):**

- Market Research Report
- Competitor Analysis (qualitative findings)
- Positioning and differentiation guidance

**Back to idea-validator (if concerns):**

- Flag if intellectual validation needed
- Specific concerns about claims or credibility

**Back to book-ideation (if Revise):**

- Specific repositioning suggestions
- Reader persona refinements

## Scope Boundaries

This skill assesses **commercial viability**, not:

- Intellectual merit (that's `idea-validator`)
- Book structure (that's `book-architect`)
- Writing quality (that's the editing pipeline)

Commercial viability is necessary but not sufficient. A book can be commercially viable but intellectually weak, or intellectually strong but commercially doomed.
