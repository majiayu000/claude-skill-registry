---
name: deep-researcher
description: Performs comprehensive, multi-layered research on any topic with structured analysis and synthesis of information from multiple sources. Uses file-based research tracking, parallel investigation threads, and context-efficient patterns for deep investigations. ALL MEDICAL CITATIONS FROM PUBMED MCP ONLY.
---

# Deep Researcher v2.0

Comprehensive research methodology with file-based tracking, parallel execution, and context management for investigations requiring 5+ sources.

**CRITICAL: All medical evidence and citations must come from PubMed MCP. No exceptions.**

---

## Research Modes

**Quick Research** (1-4 sources): Work in-context, no file structure needed.

**Deep Research** (5+ sources): Use file-based tracking below.

---

## Research Sources (STRICT POLICY)

### ALLOWED for Medical Citations

| Source | Tool | Use Case |
|--------|------|----------|
| **PubMed MCP** | `pubmed_search_articles`, `pubmed_fetch_contents`, `pubmed_article_connections` | ALL medical evidence, trials, mechanisms |
| **Official Guidelines** | `web_fetch` to ACC/ESC/ADA/AHA URLs only | Guideline recommendations |
| **AstraDB RAG** | Knowledge pipeline | Textbook references, pre-loaded guidelines |

### NOT ALLOWED for Medical Citations

| Source | Why Excluded | Allowed Use |
|--------|--------------|-------------|
| ~~OpenAlex~~ | Quality variable | **REMOVED** |
| ~~Perplexity~~ | Not peer-reviewed | Trend discovery only, NEVER cite |
| ~~General web search~~ | Unreliable | Topic discovery only, NEVER cite |
| ~~News articles~~ | Not primary evidence | Background context only |

### PubMed Quality Filters

**Prefer (Tier 1):**
- Randomized Controlled Trials (RCTs)
- Meta-analyses and Systematic Reviews
- Guidelines from ACC/ESC/ADA/AHA

**Accept (Tier 2):**
- Large observational studies from Q1 journals
- Cohort studies with >1000 patients
- Registry data from established registries

**Use Cautiously (Tier 3):**
- Case series (only if no better evidence)
- Expert consensus statements
- Narrative reviews (as background, not primary evidence)

**Reject:**
- Case reports (except for rare conditions)
- Letters to editor
- Preprints without peer review
- Animal studies (unless specifically about mechanisms)

---

## Deep Research Workflow

### Progress Tracking

Create this checklist and update after each step:

```
Deep Research Progress:
- [ ] Step 1: Initialize research project
- [ ] Step 2: Define scope and plan
- [ ] Step 3: Execute research threads (parallel when possible)
- [ ] Step 4: Validate and cross-reference
- [ ] Step 5: Synthesize from files
- [ ] Step 6: Generate final report
```

---

## Step 1: Initialize Research Project

For research requiring 5+ sources, create a project structure:

```bash
mkdir -p ~/research_{topic}/sources
mkdir -p ~/research_{topic}/threads
```

**Project Structure:**
```
~/research_{topic}/
├── plan.md              # Research questions, scope, thread assignments
├── progress.md          # Living checklist, updated throughout
├── sources/
│   └── pubmed.md        # PubMed search results and abstracts
├── threads/
│   ├── thread_1.md      # Independent research thread
│   ├── thread_2.md      # Another thread
│   └── ...
├── validation.md        # Cross-reference and credibility check
├── synthesis.md         # Cross-thread analysis
└── report.md            # Final deliverable
```

**Why file-based?** Context windows fill up. Writing findings to files lets you:
- Continue researching without context pressure
- Synthesize from persistent storage, not memory
- Produce larger, more comprehensive reports
- Resume if interrupted

---

## Step 2: Define Scope and Research Plan

Write `plan.md` with:

```markdown
# Research Plan: {Topic}

## Primary Question
[The main thing we're trying to answer]

## Scope
- Include: [what's in scope]
- Exclude: [what's explicitly out]
- Depth: [overview | detailed | exhaustive]
- Deliverable: [report type and length]

## Research Threads

### Thread 1: {Subtopic A}
- Questions to answer: ...
- PubMed search strategy: [MeSH terms, filters]
- Expected study types: RCTs, meta-analyses, etc.
- Can run parallel? Yes/No

### Thread 2: {Subtopic B}
- Questions to answer: ...
- PubMed search strategy: ...
- Can run parallel? Yes/No

[Continue for 2-5 threads]

## Thread Dependencies
- Thread 3 depends on Thread 1 findings
- Threads 1, 2, 4 can run in parallel

## Synthesis Strategy
How will threads combine into final answer?
```

**Planning Guidelines:**
| Research Type | Threads | Pattern |
|--------------|---------|---------|
| Simple fact-finding | 1-2 | Sequential |
| Drug comparison | 1 per drug (max 5) | Parallel |
| Complex investigation | 3-5 thematic | Mixed |
| Literature review | By time period or theme | Sequential |

---

## Step 3: Execute Research Threads

### PubMed Search Strategy

For each thread, use structured PubMed queries:

```python
# Example search for SGLT2 CV outcomes
pubmed_search_articles(
    queryTerm="SGLT2 inhibitor cardiovascular outcomes randomized controlled trial",
    maxResults=20,
    sortBy="relevance"
)

# Then fetch full details for top results
pubmed_fetch_contents(pmids=["PMID1", "PMID2", ...])

# Find related articles for key papers
pubmed_article_connections(
    sourcePmid="key_paper_pmid",
    relationshipType="pubmed_similar_articles"
)
```

### Parallel Execution Pattern

For independent threads, execute PubMed searches in parallel (multiple tool calls in one turn), then write each to its thread file.

**Example: Comparing SGLT2 Inhibitors**
```
Thread 1: Empagliflozin → pubmed_search "empagliflozin cardiovascular RCT" → threads/empagliflozin.md
Thread 2: Dapagliflozin → pubmed_search "dapagliflozin cardiovascular RCT" → threads/dapagliflozin.md
Thread 3: Canagliflozin → pubmed_search "canagliflozin cardiovascular RCT" → threads/canagliflozin.md
```

Execute all three searches, then write findings to respective files.

### Sequential Execution Pattern

For dependent threads, complete each fully before starting the next.

### Thread File Format

Each `threads/thread_N.md` should contain:

```markdown
# Thread: {Subtopic}

## PubMed Searches Executed
1. Query: [exact query] → [N results] → Top PMIDs: [list]
2. Query: [exact query] → [N results] → Top PMIDs: [list]

## Key Findings

### Finding 1: [Title]
- PMID: [number]
- Citation: [Authors, Journal, Year]
- Study type: RCT / Meta-analysis / Cohort / etc.
- Population: [N patients, characteristics]
- Key result: [HR/OR with 95% CI, p-value]
- Quality: High / Medium / Low [+ brief justification]

### Finding 2: [Title]
- PMID: [number]
...

## Contradictions Found
- PMID X says [claim], PMID Y says [different claim]
- Potential explanation: [patient population, endpoints, timing, etc.]

## Gaps Identified
- No RCT data on [specific question]
- Limited evidence in [patient subgroup]

## Thread Summary
[2-3 sentence synthesis of this thread's findings with key PMIDs cited]
```

### Context Offloading

**After every 5-7 tool calls:**
1. Write current findings to appropriate file
2. Update `progress.md` with status
3. Continue with fresh context

**Trigger for offload:**
- Context feeling "full" (responses slowing, losing track)
- Switching between threads
- Before any synthesis step

---

## Step 4: Validate and Cross-Reference

Read all thread files, then create `validation.md`:

```markdown
# Validation Report

## Facts Requiring Cross-Reference
| Claim | Thread Source | PMID | Verification Status | Confidence |
|-------|--------------|------|---------------------|------------|
| SGLT2i reduces HF hospitalization | Thread 1 | 12345678 | Confirmed by PMIDs 23456789, 34567890 | High |
| Benefit extends to HFpEF | Thread 2 | 45678901 | Conflicting: PMID 56789012 shows null | Investigate |

## Contradictions Analysis
### Contradiction 1: [Description]
- Position A: PMID [X], [study name], found [result]
- Position B: PMID [Y], [study name], found [result]
- Resolution: [Population difference / endpoint difference / timing / unresolved]

## Source Quality Assessment
| PMID | Study | Type | N | Quality | Notes |
|------|-------|------|---|---------|-------|
| 12345678 | EMPA-REG | RCT | 7,020 | High | Industry-funded but well-designed |
| 23456789 | Meta-analysis | MA | 45,000 | High | Published in Lancet |

## Validated Knowledge Base
[List of facts we're confident in, with PMIDs]

1. **SGLT2 inhibitors reduce CV death in T2DM with established CVD** (PMID: 12345678, 23456789)
2. **Benefit on HF hospitalization is consistent across the class** (PMID: 34567890, 45678901)
3. ...
```

---

## Step 5: Synthesize from Files

**Critical: Read from files, not memory.**

```bash
# Read all thread files
cat ~/research_{topic}/threads/*.md

# Read validation
cat ~/research_{topic}/validation.md
```

Write `synthesis.md`:

```markdown
# Synthesis: {Topic}

## Cross-Thread Patterns
[What themes emerge across multiple threads?]

## Key Insights
1. [Insight that required combining multiple threads]
2. [Insight that wasn't obvious in any single thread]
3. ...

## The Answer
[Direct response to the primary research question, with PMID citations]

## Evidence Strength Assessment
- **Strong evidence (multiple RCTs):** [claims]
- **Moderate evidence (single RCT or consistent observational):** [claims]
- **Limited evidence (observational only):** [claims]
- **Expert opinion / guideline extrapolation:** [claims]

## Remaining Gaps
[What we still don't know and would need to investigate further]
```

---

## Step 6: Generate Final Report

Write `report.md` using the synthesis:

```markdown
# {Title}

## Executive Summary
[3-5 sentences: question, key finding, main conclusion with strongest PMID]

## Research Question and Scope
[From plan.md]

## Methodology
- Database: PubMed via NCBI MCP
- Search date: [date]
- Total articles screened: [N]
- Articles included: [N]
- Study types: [breakdown]

## Findings

### {Theme 1}
[Narrative synthesis with inline PMID citations]

### {Theme 2}
...

## Analysis
[Patterns, implications, connections]

## Conclusions
1. [Primary conclusion with evidence level]
2. [Secondary conclusions]

## Clinical Implications
[If applicable: what this means for practice]

## Limitations
- [Search limitations]
- [Evidence gaps]
- [Potential biases]

## References
[Full reference list with PMIDs and DOIs]

1. Author A, Author B, et al. Title. Journal. Year;Vol:Pages. PMID: XXXXXXXX. DOI: XX.XXXX/XXXXX
2. ...
```

---

## Parallel Research Patterns

### Pattern A: Drug/Entity Comparison
**Use when:** Comparing 2-5 similar entities (drugs, devices, techniques)
```
User: "Compare CV outcomes of GLP-1 agonists"
→ Thread per drug (semaglutide, tirzepatide, liraglutide)
→ All threads parallel (same PubMed structure)
→ Comparison matrix synthesis
```

### Pattern B: Pro/Con Analysis
**Use when:** Topic has debate or controversy
```
User: "Analyze the evidence on aggressive LDL lowering"
→ Thread 1: Evidence FOR aggressive targets (PubMed: LDL <55 outcomes)
→ Thread 2: Evidence AGAINST/concerns (PubMed: LDL lowering adverse effects)
→ Thread 3: Current guidelines (fetch ACC/ESC guideline URLs)
→ Threads 1-2 parallel, Thread 3 after
```

### Pattern C: Evidence + Guidelines
**Use when:** Need both primary evidence and clinical guidance
```
User: "What's the evidence on TAVR durability?"
→ Thread 1: Trial data (PubMed: TAVR long-term outcomes RCT)
→ Thread 2: Registry data (PubMed: TAVR registry durability)
→ Thread 3: Guidelines (fetch ACC/ESC valve guidelines)
→ All parallel
```

### Pattern D: Historical Evolution
**Use when:** Understanding how evidence has evolved
```
User: "How has heart failure treatment evolved?"
→ Thread 1: Pre-neurohormonal era (PubMed: heart failure treatment 1980-1990)
→ Thread 2: ACE/ARB/BB era (PubMed: heart failure ACE inhibitor landmark)
→ Thread 3: Modern era ARNI/SGLT2 (PubMed: heart failure SGLT2 ARNI)
→ Sequential (each builds context for next)
```

---

## Quality Checkpoints

### After Step 2 (Planning)
- [ ] Research question is specific and answerable
- [ ] PubMed search strategies are defined for each thread
- [ ] Threads are independent where marked parallel
- [ ] Expected study types are specified

### After Step 3 (Execution)
- [ ] Each thread has 3+ credible PubMed sources
- [ ] Key claims have specific data (HR, CI, p-value)
- [ ] All citations have PMIDs
- [ ] Gaps and contradictions are documented
- [ ] Thread summaries are written

### After Step 4 (Validation)
- [ ] Key facts cross-referenced across threads
- [ ] Contradictions analyzed with potential explanations
- [ ] Source quality assessed for each major citation
- [ ] Validated knowledge base compiled

### After Step 5 (Synthesis)
- [ ] Cross-thread patterns identified
- [ ] Primary question directly answered
- [ ] Evidence strength honestly assessed
- [ ] Insights go beyond any single thread

### Before Delivery
- [ ] Report structure matches user's requested format
- [ ] All claims have PMID citations
- [ ] Executive summary is truly executive (skimmable)
- [ ] Reference list is complete with DOIs

---

## Common Research Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Context overflow | Losing track of earlier findings | Write to files every 5-7 tool calls |
| Confirmation bias | All sources agree suspiciously | Search for contradicting evidence explicitly |
| Recency bias | Only 2023-2024 sources | Include landmark trials regardless of date |
| Source homogeneity | All RCTs, no guidelines | Add guideline thread for clinical context |
| Scope creep | Research expanding endlessly | Return to plan.md, enforce boundaries |
| Premature synthesis | Concluding before validation | Complete Step 4 before Step 5 |
| Memory-based synthesis | Citing from recall | Read files explicitly during Step 5 |
| Non-PubMed citations | Citing Perplexity/web | Delete and replace with PubMed source |

---

## Example: Full Research Session

**User:** "Research the current evidence on colchicine for cardiovascular prevention"

**Step 1: Initialize**
```bash
mkdir -p ~/research_colchicine_cv/sources
mkdir -p ~/research_colchicine_cv/threads
```

**Step 2: Plan** (write to plan.md)
- Primary question: What's the evidence for colchicine in CV prevention?
- Thread 1: Major RCTs (COLCOT, LoDoCo2, CLEAR SYNERGY)
  - PubMed: "colchicine cardiovascular randomized controlled trial"
- Thread 2: Mechanisms and anti-inflammatory hypothesis
  - PubMed: "colchicine inflammation atherosclerosis mechanism"
- Thread 3: Guidelines and clinical adoption
  - Fetch: ACC/ESC guideline URLs for stable CAD
- Thread 4: Safety and practical considerations
  - PubMed: "colchicine adverse effects cardiovascular"
- Threads 1, 2, 4 parallel; Thread 3 after 1 completes

**Step 3: Execute**
```python
# Parallel searches
pubmed_search_articles(queryTerm="colchicine cardiovascular randomized controlled trial", maxResults=15)
pubmed_search_articles(queryTerm="colchicine inflammation atherosclerosis mechanism", maxResults=10)
pubmed_search_articles(queryTerm="colchicine adverse effects cardiovascular", maxResults=10)

# Fetch top results
pubmed_fetch_contents(pmids=["31733140", "32865377", "37634428"])  # COLCOT, LoDoCo2, CLEAR

# Write to thread files
```

**Step 4: Validate**
- Read all thread files
- Cross-reference mortality data across trials
- Note: CLEAR SYNERGY neutral vs positive COLCOT/LoDoCo2
- Analyze: Patient population differences (post-ACS vs chronic CAD)
- Write validation.md

**Step 5: Synthesize**
- Read from files
- Pattern: Inflammation hypothesis supported, but patient selection matters
- Insight: Post-ACS (COLCOT) benefit clear; chronic stable CAD (CLEAR) less certain
- Write synthesis.md

**Step 6: Report**
- Structured report with evidence summary
- Clear recommendation by patient type
- All PMIDs cited
- Complete reference list

---

## Integration with Other Skills

This skill provides research foundation for:
- `cardiology-editorial` → Use research output for trial analysis
- `cardiology-newsletter-writer` → Research before writing
- `youtube-script-master` → Research for script evidence base
- `x-post-creator-skill` → Research before tweet generation

**Workflow:**
1. User requests content on topic
2. Run `deep-researcher` first (this skill)
3. Pass validated findings to writing skill
4. Writing skill cites PMIDs from research output

---

## When NOT to Use This Skill

- Simple factual questions (use PubMed MCP directly)
- Trend discovery (use Perplexity, but don't cite)
- Non-medical topics (this skill is optimized for PubMed)
- Quick content needs (use writing skill directly with inline research)

Use this skill when you need:
- 5+ sources synthesized
- Complex multi-faceted questions
- Rigorous evidence assessment
- Comprehensive literature coverage
