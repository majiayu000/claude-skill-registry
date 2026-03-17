---
name: financial-deep-research
description: Conduct enterprise-grade financial research with multi-source synthesis, regulatory compliance tracking, and verified market analysis. Use when user needs comprehensive financial analysis requiring 10+ sources, verified claims, market comparisons, or investment research. Triggers include "financial research", "market analysis", "investment analysis", "due diligence", "financial deep dive", "compare stocks/funds", or "analyze [company/sector]". Do NOT use for simple stock quotes, basic company lookups, or questions answerable with 1-2 searches.
---

# Financial Deep Research

<!-- STATIC CONTEXT BLOCK START - Optimized for prompt caching -->
<!-- All static instructions, methodology, and templates below this line -->
<!-- Dynamic content (user queries, results) added after this block -->

## Core System Instructions

**Purpose:** Deliver citation-backed, verified financial research reports through 8-phase pipeline (Scope > Plan > Retrieve > Triangulate > Synthesize > Critique > Refine > Package) with financial source credibility scoring, regulatory compliance tracking, and progressive context management.

**Financial Focus:** This skill specializes in:
- Market analysis and investment research
- Due diligence and competitive benchmarking
- Regulatory compliance and risk assessment
- Financial modeling support and valuation analysis
- Earnings analysis and financial statement review
- Sector/industry deep dives

**Context Strategy:** This skill uses 2025 context engineering best practices:
- Static instructions cached (this section)
- Progressive disclosure (load references only when needed)
- Avoid "loss in the middle" (critical info at start/end, not buried)
- Explicit section markers for context navigation

---

## Decision Tree (Execute First)

```
Request Analysis
|-- Simple stock quote? -> STOP: Use WebSearch, not this skill
|-- Basic company lookup? -> STOP: Use WebSearch, not this skill
|-- Debugging code? -> STOP: Use standard tools, not this skill
+-- Complex financial analysis needed? -> CONTINUE

Mode Selection
|-- Quick market check? -> quick (3 phases, 2-5 min)
|-- Standard analysis? -> standard (6 phases, 5-10 min) [DEFAULT]
|-- Investment decision? -> deep (8 phases, 10-20 min)
|-- Due diligence/M&A? -> ultradeep (8+ phases, 20-45 min)

Execution Loop (per phase)
|-- Load phase instructions from [methodology](./reference/methodology.md#phase-N)
|-- Execute phase tasks
|-- Spawn parallel agents if applicable
+-- Update progress

Validation Gate
|-- Run `python scripts/validate_report.py --report [path]`
|-- Pass? -> Deliver
+-- Fail? -> Fix (max 2 attempts) -> Still fails? -> Escalate
```

---

## Workflow (Clarify > Plan > Act > Verify > Report)

**AUTONOMY PRINCIPLE:** This skill operates independently. Infer assumptions from query context. Only stop for critical errors or incomprehensible queries.

### 1. Clarify (Rarely Needed - Prefer Autonomy)

**DEFAULT: Proceed autonomously. Derive assumptions from query signals.**

**ONLY ask if CRITICALLY ambiguous:**
- Query is incomprehensible (e.g., "analyze the thing")
- Contradictory requirements (e.g., "quick 50-source ultradeep analysis")
- Critical compliance/regulatory scope unclear

**When in doubt: PROCEED with standard mode. User will redirect if incorrect.**

**Default assumptions:**
- Company analysis -> Assume investor/analyst audience
- Sector query -> Assume comprehensive market view needed
- Valuation query -> Assume institutional-quality analysis
- Regulatory query -> Assume US jurisdiction unless specified
- Standard mode is default for most queries

---

### 2. Plan

**Mode selection criteria:**
- **Quick** (2-5 min): Market snapshot, earnings preview, quick check
- **Standard** (5-10 min): Most analysis, balanced depth/speed [DEFAULT]
- **Deep** (10-20 min): Investment decisions, detailed due diligence
- **UltraDeep** (20-45 min): M&A due diligence, comprehensive sector analysis

**Announce plan and execute:**
- Briefly state: selected mode, estimated time, number of sources
- Example: "Starting standard mode financial research (5-10 min, 15-30 sources)"
- Proceed without waiting for approval

---

### 3. Act (Phase Execution)

**All modes execute:**
- Phase 1: SCOPE - Define financial analysis boundaries ([method](./reference/methodology.md#phase-1-scope))
- Phase 3: RETRIEVE - Parallel financial data gathering (5-10 concurrent searches + agents) ([method](./reference/methodology.md#phase-3-retrieve---parallel-information-gathering))
- Phase 8: PACKAGE - Generate report using [template](./templates/report_template.md)

**Standard/Deep/UltraDeep execute:**
- Phase 2: PLAN - Financial research strategy formulation
- Phase 4: TRIANGULATE - Verify 3+ sources per financial claim
- Phase 4.5: OUTLINE REFINEMENT - Adapt structure based on evidence (WebWeaver 2025) ([method](./reference/methodology.md#phase-45-outline-refinement---dynamic-evolution-webweaver-2025))
- Phase 5: SYNTHESIZE - Generate investment insights

**Deep/UltraDeep execute:**
- Phase 6: CRITIQUE - Risk analysis and bear case
- Phase 7: REFINE - Address gaps, strengthen thesis

**Critical: Avoid "Loss in the Middle"**
- Place key findings at START and END of sections, not buried
- Use explicit headers and markers
- Structure: Summary > Details > Conclusion (not Details sandwiched)

**Progressive Context Loading:**
- Load [methodology](./reference/methodology.md) sections on-demand
- Load [template](./templates/report_template.md) only for Phase 8
- Do not inline everything - reference external files

**Anti-Hallucination Protocol (CRITICAL for Financial Data):**
- **Source grounding**: Every financial claim MUST cite a specific source immediately [N]
- **Clear boundaries**: Distinguish between FACTS (from filings/data) and ANALYSIS (your interpretation)
- **Explicit markers**: Use "According to [1]..." or "[1] reports..." for source-grounded statements
- **No speculation without labeling**: Mark inferences as "This suggests..." not "Data shows..."
- **Verify before citing**: If unsure whether source actually says X, do NOT fabricate citation
- **When uncertain**: Say "No sources found for X" rather than inventing references
- **Financial precision**: Always include specific numbers, dates, and currency when available

**Parallel Execution Requirements (CRITICAL for Speed):**

**Phase 3 RETRIEVE - Mandatory Parallel Financial Search:**
1. **Decompose query** into 5-10 independent search angles before ANY searches
2. **Launch ALL searches in single message** with multiple tool calls (NOT sequential)
3. **Quality threshold monitoring** for FFS pattern:
   - Track source count and avg credibility score
   - Proceed when threshold reached (mode-specific, see methodology)
   - Continue background searches for additional depth
4. **Spawn 3-5 parallel agents** using Task tool for deep-dive investigations

**Financial Search Decomposition Strategy:**
```
[Single message with 8+ parallel tool calls]
WebSearch #1: Company fundamentals + recent filings
WebSearch #2: Earnings/financial performance
WebSearch #3: Industry/sector analysis
WebSearch #4: Competitive landscape
WebSearch #5: Regulatory/compliance news
WebSearch #6: Analyst ratings/price targets
WebSearch #7: Risk factors/bear case
WebSearch #8: Recent news + catalysts
Task agent #1: SEC filing deep dive (10-K, 10-Q analysis)
Task agent #2: Financial statement analysis
Task agent #3: Industry comparison/benchmarking
```

---

### 4. Verify (Always Execute)

**Step 1: Citation Verification (Catches Fabricated Sources)**

```bash
python scripts/verify_citations.py --report [path]
```

**Financial-Specific Checks:**
- SEC filing references (verify EDGAR links)
- Financial data accuracy (cross-check key metrics)
- Date accuracy (earnings dates, filing dates)
- Flags suspicious entries (future financials, impossible metrics)

**If suspicious citations found:**
- Review flagged entries manually
- Remove or replace fabricated sources
- Re-run until clean

**Step 2: Structure & Quality Validation**

```bash
python scripts/validate_report.py --report [path]
```

**9 automated checks (financial-enhanced):**
1. Executive summary length (50-250 words)
2. Required sections present (+ recommended: Risk Factors, Valuation)
3. Citations formatted [1], [2], [3]
4. Bibliography matches citations
5. No placeholder text (TBD, TODO)
6. Word count reasonable (500-10000)
7. Minimum 10 sources
8. No broken internal links
9. Financial data consistency (dates, currencies, units)

**If fails:**
- Attempt 1: Auto-fix formatting/links
- Attempt 2: Manual review + correction
- After 2 failures: **STOP** > Report issues > Ask user

---

### 5. Report

**CRITICAL: Generate COMPREHENSIVE, DETAILED financial markdown reports**

**File Organization (CRITICAL - Clean Accessibility):**

**1. Create Organized Folder in /code:**
- ALWAYS create dedicated folder: `/code/[TickerOrTopic]_Financial_Research_[YYYYMMDD]/`
- Extract clean topic name from research question
- Examples:
  - "AAPL investment analysis" -> `/code/AAPL_Financial_Research_20251104/`
  - "compare cloud providers" -> `/code/Cloud_Sector_Analysis_20251104/`
  - "fintech due diligence" -> `/code/Fintech_Due_Diligence_20251104/`
- If folder exists, use it; if not, create it
- This ensures clean organization and easy accessibility

**2. Save All Formats to Same Folder:**

**Markdown (Primary Source):**
- Save to: `[Documents folder]/financial_report_[YYYYMMDD]_[topic_slug].md`
- Also save copy to: `/code/research_output/` (internal tracking)
- Full detailed report with all findings

**HTML (McKinsey Style - ALWAYS GENERATE):**
- Save to: `[Documents folder]/financial_report_[YYYYMMDD]_[topic_slug].html`
- Use McKinsey template: [mckinsey_template](./templates/mckinsey_report_template.html)
- Design principles: Sharp corners (NO border-radius), muted corporate colors (navy #003d5c, gray #f8f9fa), ultra-compact layout, info-first structure
- Place critical financial metrics dashboard at top (extract 3-4 key metrics: market cap, P/E, revenue growth, etc.)
- Use data tables for dense financial information
- 14px base font, compact spacing, no decorative gradients or colors
- OPEN in browser automatically after generation

**PDF (Professional Print - ALWAYS GENERATE):**
- Save to: `[Documents folder]/financial_report_[YYYYMMDD]_[topic_slug].pdf`
- Use generating-pdf skill (via Task tool with general-purpose agent)
- Professional formatting with headers, page numbers
- OPEN in default PDF viewer after generation

**3. File Naming Convention:**
All files use same base name for easy matching:
- `financial_report_20251104_aapl_analysis.md`
- `financial_report_20251104_aapl_analysis.html`
- `financial_report_20251104_aapl_analysis.pdf`

**Length Requirements (UNLIMITED with Progressive Assembly):**
- Quick mode: 2,000+ words (baseline quality threshold)
- Standard mode: 4,000+ words (comprehensive analysis)
- Deep mode: 6,000+ words (thorough investigation)
- UltraDeep mode: 10,000-50,000+ words (NO UPPER LIMIT)

**How Unlimited Length Works:**
Progressive file assembly allows ANY report length by generating section-by-section.
Each section is written to file immediately (avoiding output token limits).
Complex analyses with many findings? Generate 20, 30, 50+ findings - no constraint!

**Content Requirements:**
- Use [template](./templates/report_template.md) as exact structure
- Generate each section to APPROPRIATE depth (determined by evidence, not word targets)
- Include specific financial data, statistics, dates, numbers
- Multiple paragraphs per finding with evidence
- Each section gets focused generation attention
- DO NOT write summaries - write FULL analysis

**Writing Standards (Financial Precision):**
- **Data-driven**: Every claim backed by specific numbers from sources
- **Precision**: Exact figures with currency, dates, and units
- **Economy**: No fluff, eliminate unnecessary modifiers
- **Clarity**: Financial terminology used correctly and consistently
- **Directness**: State findings without embellishment
- **High signal-to-noise**: Dense information, respect reader's time
- **Examples**:
  - Bad: "revenue increased significantly" -> Good: "revenue grew 23% YoY to $94.8B in FY2024 [1]"
  - Bad: "strong margins" -> Good: "gross margin of 43.2%, up 180bps YoY [2]"
  - Bad: "expensive valuation" -> Good: "trades at 28x forward P/E vs sector median 22x [3]"

**Source Attribution Standards (Critical for Financial Research):**
- **Immediate citation**: Every financial claim followed by [N] citation in same sentence
- **Quote sources directly**: Use "According to [1]..." or "[1] reports..." for factual statements
- **Distinguish fact from analysis**:
  - GOOD: "Q3 revenue was $24.9B, up 8% YoY [1]."
  - BAD: "Revenue grew strongly last quarter."
- **No vague attributions**:
  - NEVER: "Analysts believe...", "Market expects...", "Sources indicate..."
  - ALWAYS: "Goldman Sachs estimates..." [1], "Per SEC 10-K filing..." [2]
- **Label speculation explicitly**:
  - GOOD: "This suggests potential margin expansion..." (analysis, not fact)
  - BAD: "Margins will expand..." (presented as fact without citation)

**Deliver to user:**
1. Executive summary with key investment thesis (inline in chat)
2. Organized folder path (e.g., "All files saved to: /code/AAPL_Financial_Research_20251104/")
3. Confirmation of all three formats generated:
   - Markdown (source)
   - HTML (McKinsey-style, opened in browser)
   - PDF (professional print, opened in viewer)
4. Source quality assessment summary (source count, regulatory vs news mix)
5. Key financial metrics summary
6. Risk factors summary
7. Next steps (if relevant)

**Generation Workflow: Progressive File Assembly (Unlimited Length)**

[Same progressive assembly workflow as base skill - see deep-research SKILL.md]

---

## Financial Data Sources (Priority Order)

### Tier 1: Primary/Regulatory Sources (Highest Credibility)
- **SEC EDGAR**: 10-K, 10-Q, 8-K, proxy statements, insider filings
- **Federal Reserve**: FRED data, monetary policy, banking data
- **FDIC/OCC**: Banking regulation, call reports
- **Treasury**: Economic data, fiscal policy
- **Company IR**: Investor relations, earnings calls, presentations
- **Exchange Filings**: NYSE, NASDAQ company disclosures

### Tier 2: Financial Data Providers (High Credibility)
- **Bloomberg**: Real-time data, analysis, news
- **Reuters**: News, data, analysis
- **S&P Global**: Ratings, research, Capital IQ data
- **Moody's/Fitch**: Credit ratings, research
- **FactSet**: Financial data, analytics
- **Morningstar**: Fund data, equity research
- **PitchBook**: Private market data, VC/PE

### Tier 3: Financial News & Research (Moderate-High Credibility)
- **Wall Street Journal**: Business news, analysis
- **Financial Times**: Global finance news
- **Barron's**: Investment analysis
- **Institutional research**: Goldman, Morgan Stanley, JPM research
- **Industry publications**: American Banker, Insurance Journal

### Tier 4: General Business Sources (Moderate Credibility)
- **CNBC, Yahoo Finance**: Market news (verify with primary sources)
- **Seeking Alpha**: Analysis (note: user-generated, verify claims)
- **Industry blogs**: Supplement only, not primary citation

**Source Verification Requirements:**
- Tier 1 sources: Can cite directly, highest trust
- Tier 2 sources: Reliable, cross-check major claims
- Tier 3 sources: Good for analysis, verify data with Tier 1-2
- Tier 4 sources: Use sparingly, always verify with higher tiers

---

## Output Contract

**Format:** Comprehensive financial markdown report following [template](./templates/report_template.md) EXACTLY

**Required sections (all must be detailed):**
- Executive Summary with Investment Thesis (50-250 words)
- Company/Topic Overview (background, business model)
- Financial Analysis (revenue, margins, cash flow, balance sheet)
- Valuation Analysis (multiples, DCF if applicable, peer comparison)
- Competitive Position (market share, moat, competitive dynamics)
- Risk Factors (business, financial, regulatory, market risks)
- Investment Thesis / Recommendations
- **Bibliography (CRITICAL - see rules below)**
- Methodology Appendix

**Financial-Specific Sections (include when relevant):**
- Earnings Analysis (quarterly trends, guidance vs actual)
- Management Assessment (track record, insider activity)
- Regulatory Environment (compliance, pending regulation)
- ESG Considerations (if material to thesis)
- Catalyst Timeline (upcoming events, catalysts)

**Bibliography Requirements (ZERO TOLERANCE):**
- MUST include EVERY citation [N] used in report body
- Format: [N] Source (Date). "Title". Publication/Filing. URL (Retrieved: Date)
- Each entry on its own line, complete with all metadata
- NO placeholders, NO ranges, NO truncation
- Validation WILL FAIL if bibliography is incomplete

**Strictly Prohibited:**
- Placeholder text (TBD, TODO, [citation needed])
- Uncited financial claims
- Forward-looking statements presented as facts
- Broken links
- Missing required sections
- **Short summaries instead of detailed analysis**
- **Vague statements without specific data**

**Quality gates (enforced by validator):**
- Minimum 2,000 words (standard mode)
- Average credibility score >70/100 (higher bar for financial)
- 3+ sources per major financial claim
- Clear facts vs. analysis distinction
- All sections present and detailed
- Key financial metrics included with sources

---

## Error Handling & Stop Rules

**Stop immediately if:**
- 2 validation failures on same error > Pause, report, ask user
- <5 sources after exhaustive search > Report limitation, request direction
- Critical financial data unavailable > Note gap, proceed with caveats
- User interrupts/changes scope > Confirm new direction

**Graceful degradation:**
- 5-10 sources > Note in limitations, proceed with extra verification
- Missing recent filing > Note, use most recent available
- Private company (limited data) > Acknowledge, use available sources
- Time constraint reached > Package partial results, document gaps

**Error format:**
```
Issue: [Description]
Context: [What was attempted]
Tried: [Resolution attempts]
Options:
   1. [Option 1]
   2. [Option 2]
   3. [Option 3]
```

---

## Quality Standards (Always Enforce)

Every financial report must:
- 10+ sources (document if fewer)
- 3+ sources per major financial claim
- Executive summary <250 words with clear thesis
- Full citations with URLs to filings/sources
- Credibility assessment (source tier breakdown)
- Risk factors section
- Methodology documented
- Key metrics with sources
- No placeholders

**Priority:** Accuracy over speed. Financial data must be verified.

---

## Inputs & Assumptions

**Required:**
- Financial research question (string)

**Optional:**
- Mode (quick/standard/deep/ultradeep)
- Time constraints
- Specific data requirements (valuation focus, risk focus, etc.)
- Output format preferences
- Jurisdiction (default: US)

**Assumptions:**
- User requires verified, citation-backed financial information
- Institutional-quality analysis expected
- 10-50 sources available on topic
- Time investment: 5-45 minutes
- USD unless otherwise specified
- US regulatory framework unless specified

---

## When to Use / NOT Use

**Use when:**
- Investment analysis (buy/sell/hold thesis)
- Company due diligence
- Sector/industry deep dives
- M&A analysis
- Competitive benchmarking
- Earnings analysis
- Regulatory impact assessment
- Financial modeling research

**Do NOT use:**
- Simple stock quotes (use WebSearch)
- Basic company lookups (use WebSearch)
- Real-time trading decisions (need live data)
- Personal financial advice (not qualified)
- Tax/legal advice (not qualified)

---

## Scripts (Offline, Python stdlib only)

**Location:** `./scripts/`

- **research_engine.py** - Orchestration engine
- **validate_report.py** - Quality validation (9 checks, financial-enhanced)
- **citation_manager.py** - Citation tracking
- **source_evaluator.py** - Financial source credibility scoring (0-100)
- **verify_citations.py** - Citation verification with SEC filing checks

**No external dependencies required.**

---

## Progressive References (Load On-Demand)

**Do not inline these - reference only:**
- [Complete Methodology](./reference/methodology.md) - 8-phase details with financial focus
- [Report Template](./templates/report_template.md) - Financial output structure
- [README](./README.md) - Usage docs
- [QUICK_START](./QUICK_START.md) - Fast reference

**Context Management:** Load files on-demand for current phase only. Do not preload all content.

---

<!-- STATIC CONTEXT BLOCK END -->
<!-- Above content is cacheable (>1024 tokens, static) -->
<!-- Below: Dynamic content (user queries, retrieved data, generated reports) -->
<!-- This structure enables 85% latency reduction via prompt caching -->

---

## Dynamic Execution Zone

**User Query Processing:**
[User financial research question will be inserted here during execution]

**Retrieved Information:**
[Search results and sources will be accumulated here]

**Generated Analysis:**
[Findings, synthesis, and report content generated here]

**Note:** This section remains empty in the skill definition. Content populated during runtime only.
