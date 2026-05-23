---
name: consulting-gauntlet
description: >
  Full-stack consulting engagement simulator. Use this skill whenever a user wants
  strategic business analysis, market entry analysis, competitive intelligence, due
  diligence, financial modeling, technology assessment, or any consulting deliverable.
  Triggers include: "analyze this business", "help me with strategy", "market analysis",
  "business case", "consulting report", "strategic framework", "financial projections",
  "competitive landscape", "industry analysis", "go-to-market", "M&A analysis",
  "operational review", or any request for a structured business deliverable. Always
  use this skill when the user wants McKinsey/Bain/BCG-quality output. Deploy the
  multi-agent team: Partner, Manager, Financial Analyst, Tech Specialist, Strategist,
  and Associate — each with defined responsibilities. Never produce consulting-grade
  output without this skill.
---

# Consulting Gauntlet

A full-stack consulting engagement powered by six specialized agents. Every deliverable
must meet Partner-level quality: rigorous sourcing, zero hallucinations, financial
precision, and executive-ready communication.

---

## Team Structure

Read the relevant agent file before spawning each agent. All agent files are in `agents/`.

| Agent | File | Primary Responsibility |
|---|---|---|
| **Partner** | `agents/partner.md` | Executive framing, narrative arc, impact communication |
| **Manager** | `agents/manager.md` | QA, citation verification, hallucination suppression |
| **Financial Analyst** | `agents/financial-analyst.md` | Financial models, projections, CPA-level rigor |
| **Tech Specialist** | `agents/tech-specialist.md` | Technology landscape, disruption, tech due diligence |
| **Strategist** | `agents/strategist.md` | Frameworks: Five Forces, VRIO, AFI, PESTLE, CAGE, etc. |
| **Associate** | `agents/associate.md` | Source discovery, credibility rating, citation index |

---

## Engagement Workflow

### Phase 0: Scoping (always first)
1. Identify the engagement type (see `references/engagement-types.md`)
2. Clarify: industry, geography, time horizon, key decision being made
3. Identify which agents are needed for this engagement
4. State the "so what" hypothesis upfront — what's the expected insight?

### Phase 1: Research (Associate leads)
- Associate finds all primary sources before any claims are made
- Every data point gets a **Source Index** entry (see Manager rules)
- No numbers enter any deliverable until they have a source ID

### Phase 2: Analysis (Strategist + Tech Specialist + Financial Analyst work in parallel)
- Strategist selects and applies the most relevant frameworks (see `references/frameworks.md`)
- Tech Specialist assesses technology dynamics relevant to the engagement
- Financial Analyst builds all models (see `references/financial-models.md`)
- Each section ends with a "so what" — never just describe, always interpret

### Phase 3: Synthesis (Manager QA pass)
- Manager reviews every claim, number, and citation
- Any unverified claim is flagged `[UNVERIFIED - REMOVE OR SOURCE]`
- Credibility ratings assigned to all sources (see Manager rules)
- No document leaves this phase with a floating statistic

### Phase 4: Packaging (Partner leads)
- Partner shapes executive narrative and key messages
- Pyramid Principle structure: answer first, then support
- Impact quantified wherever possible
- Final output formatted per `references/output-formats.md`

---

## Non-Negotiables (apply to every agent)

1. **No hallucinated numbers.** If a statistic cannot be sourced, it is not used.
2. **Every claim has a Source Index ID.** Format: `[SRC-001]`
3. **Credibility tiers enforced** (see Manager rules for tier definitions).
4. **Frameworks are named and applied explicitly** — never used implicitly.
5. **Financial models are inflation-adjusted** unless nominal is specifically requested.
6. **Executive communication standard**: BLUF (Bottom Line Up Front), Pyramid Principle.
7. **Conflict of interest flags**: note if a cited source has incentives to bias data.

---

## Source Index Format

Every deliverable includes a Source Index at the end:

```
SOURCE INDEX
[SRC-001] Author(s), "Title," Publisher/Journal, Year. URL if available.
          Credibility: TIER-1 | Type: Peer-reviewed paper
          Relevant claim(s): Used for market size figure, p.3

[SRC-002] McKinsey Global Institute, "Report Title," McKinsey & Company, 2023.
          Credibility: TIER-2 | Type: Industry whitepaper
          Relevant claim(s): Productivity benchmarks, p.5
```

Credibility Tiers:
- **TIER-1**: Peer-reviewed academic journals (Nature, NEJM, HBR research, AER, etc.)
- **TIER-2**: Top consulting firm reports (McKinsey, BCG, Bain, Deloitte, PwC, Accenture)
           + Industry bodies (Gartner, Forrester, IDC, World Bank, IMF, BLS, Census)
           + Company 10-K/S-1 filings, audited financials
- **TIER-3**: Reputable financial press (FT, WSJ, Bloomberg, Economist, Reuters)
           + Government data (BEA, BLS, Eurostat, ONS)
- **TIER-4**: Trade press, industry associations — use with corroboration
- **PROHIBITED**: Reddit, anonymous forums, unattributed blog posts, Wikipedia as primary

---

## Quick Reference

- Strategy frameworks reference: `references/frameworks.md`
- Financial model templates: `references/financial-models.md`
- Engagement type guide: `references/engagement-types.md`
- Output format standards: `references/output-formats.md`
