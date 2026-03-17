---
name: quick-topic-researcher
description: "Rapid topic mastery for video/content prep. Takes a topic → generates 5 research questions → parallel PubMed + web search → outputs McKinsey-style brief in 5 minutes. Use BEFORE recording videos or writing content."
---

# Quick Topic Researcher

**5 minutes to topic mastery.** This skill generates a focused research brief you can use immediately before recording a video or writing content.

**Different from `deep-researcher`:** That skill is comprehensive (5+ sources, file-based, 30+ minutes). This skill is FAST (5 questions, parallel search, 5 minutes).

---

## When to Use

| Use Case | This Skill |
|----------|------------|
| Prepping for a YouTube video | Yes |
| Writing a quick tweet thread | Yes |
| Refreshing knowledge on a topic | Yes |
| Before a podcast discussion | Yes |
| Comprehensive literature review | No → Use `deep-researcher` |
| Writing a formal editorial | No → Use `deep-researcher` first |

---

## How It Works

```
TOPIC: "GLP-1 agonists in heart failure"
DOMAIN: "Cardiology"

    │
    ▼
┌─────────────────────────────────────────────────────┐
│ STEP 1: Generate 5 Research Questions               │
│                                                      │
│ 1. Do GLP-1 agonists reduce heart failure           │
│    hospitalization in diabetic patients?            │
│ 2. Is there evidence of direct cardiac benefit?     │
│ 3. What are the key trials showing CV outcomes?     │
│ 4. Are there safety concerns in existing HF?        │
│ 5. What do current guidelines recommend?            │
└─────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────┐
│ STEP 2: Parallel Research (5 searches at once)      │
│                                                      │
│ [PubMed Q1] [PubMed Q2] [PubMed Q3] [Perplexity Q4] │
│ [Perplexity Q5]                                      │
│                                                      │
│ ~30 seconds total                                    │
└─────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────┐
│ STEP 3: McKinsey-Style Brief                         │
│                                                      │
│ EXECUTIVE SUMMARY                                    │
│ • Key finding with strongest PMID                   │
│                                                      │
│ ANALYSIS                                             │
│ • Theme 1: Trial evidence (PMIDs)                   │
│ • Theme 2: Mechanisms (PMIDs)                       │
│ • Theme 3: Guidelines                               │
│                                                      │
│ CLINICAL IMPLICATIONS                                │
│ • What this means for your content                  │
│                                                      │
│ KEY PMIDS TO CITE                                    │
│ • List of 5-7 citation-ready references             │
└─────────────────────────────────────────────────────┘
```

---

## Usage

### Interactive Mode (Recommended)

Ask Claude:

```
Use quick-topic-researcher for [TOPIC] in [DOMAIN]
```

Example:
```
Use quick-topic-researcher for "SGLT2 inhibitors in CKD" in "Cardiology/Nephrology"
```

### CLI Mode (Coming Soon)

```bash
python skills/cardiology/quick-topic-researcher/scripts/quick_research.py \
    --topic "GLP-1 agonists in heart failure" \
    --domain "Cardiology"
```

---

## Research Sources

### Primary (Citable)
| Source | Tool | Purpose |
|--------|------|---------|
| **PubMed MCP** | `pubmed_search_articles`, `pubmed_fetch_contents` | All medical evidence |
| **Guidelines** | Direct URL fetch to ACC/ESC/ADA | Recommendations |

### Discovery (Not Citable)
| Source | Tool | Purpose |
|--------|------|---------|
| **Perplexity** | `perplexity_ask` via MCP | Quick context, trend discovery |
| **Web Search** | `WebSearch` | Background, non-medical context |

**Rule:** You can USE Perplexity to understand context, but you CITE only PubMed.

---

## Output Format

The skill outputs a structured brief:

```markdown
# Quick Research Brief: [TOPIC]

**Domain:** [DOMAIN]
**Generated:** [DATE]
**Time to Read:** 3 minutes

---

## Executive Summary

[2-3 sentences: What you need to know before recording/writing]

Key takeaway: [ONE sentence with strongest PMID]

---

## Research Questions & Findings

### Q1: [Question]
**Answer:** [Concise answer]
**Evidence:** [Study name, PMID, key stat (HR, CI, p-value)]

### Q2: [Question]
**Answer:** [Concise answer]
**Evidence:** [Study name, PMID, key stat]

[... Q3-Q5 ...]

---

## Clinical Context

### What Guidelines Say
[ACC/ESC/ADA recommendations with class/level]

### Practice Implications
[What this means for real patients]

---

## Content Hooks

For your video/content, consider these angles:
1. [Hook 1 based on findings]
2. [Hook 2 based on findings]
3. [Hook 3 based on findings]

---

## Citation-Ready References

1. Author A, et al. TRIAL-NAME. Journal. Year. PMID: XXXXXXXX
2. Author B, et al. Study Name. Journal. Year. PMID: XXXXXXXX
3. [5-7 total references]

---

## Gaps & Caveats

- [What the evidence doesn't cover]
- [Patient populations with limited data]
```

---

## Integration with Content Pipeline

### Before YouTube Script
```
1. Run quick-topic-researcher on your video topic
2. Review the brief (3 min read)
3. Open youtube-script-master with the brief in context
4. Script now has verified facts and PMIDs
```

### Before Tweet Thread
```
1. Run quick-topic-researcher
2. Pick 1-2 key findings from the brief
3. Use x-post-creator-skill with specific PMIDs
```

### Before Newsletter
```
1. Run quick-topic-researcher for quick take
2. If topic is complex, follow up with deep-researcher
3. Write with cardiology-newsletter-writer
```

---

## Example Session

**User:** Use quick-topic-researcher for "colchicine in cardiovascular prevention" in "Cardiology"

**Claude:**

I'll research this topic rapidly using PubMed and generate a brief.

**Step 1: Generating 5 research questions...**

1. Does colchicine reduce major cardiovascular events in CAD patients?
2. What are the key RCTs (COLCOT, LoDoCo2, CLEAR SYNERGY)?
3. What is the proposed anti-inflammatory mechanism?
4. What are the safety concerns and contraindications?
5. What do current guidelines recommend?

**Step 2: Parallel research...**

[Executes 5 PubMed searches in parallel]
[Fetches key article abstracts]
[Searches Perplexity for context]

**Step 3: Generating McKinsey-style brief...**

---

# Quick Research Brief: Colchicine in CV Prevention

**Domain:** Cardiology
**Generated:** 2026-01-01
**Time to Read:** 3 minutes

## Executive Summary

Low-dose colchicine (0.5mg daily) reduces cardiovascular events in patients with established coronary artery disease through anti-inflammatory mechanisms. COLCOT and LoDoCo2 showed consistent benefit; CLEAR SYNERGY was neutral but in a different population.

Key takeaway: **In stable CAD patients, colchicine 0.5mg daily reduces CV events by ~25% (HR 0.69-0.77)** (PMID: 31733140, 32865377)

## Research Questions & Findings

### Q1: Does colchicine reduce major CV events?
**Answer:** Yes, in stable CAD
**Evidence:** LoDoCo2: HR 0.69 (0.57-0.83), p<0.001 for CV death/MI/stroke (PMID: 32865377)

### Q2: What are the key trials?
**Answer:** COLCOT (post-MI), LoDoCo2 (chronic CAD), CLEAR SYNERGY (post-PCI)
**Evidence:**
- COLCOT: 0.5mg, HR 0.77 for composite (PMID: 31733140)
- LoDoCo2: 0.5mg, HR 0.69 for composite (PMID: 32865377)
- CLEAR SYNERGY: Neutral for primary endpoint (PMID: 37634428)

### Q3: What is the mechanism?
**Answer:** NLRP3 inflammasome inhibition, IL-1β reduction
**Evidence:** Reduces hsCRP; targets residual inflammatory risk (PMID: 29724838)

### Q4: Safety concerns?
**Answer:** GI side effects, myopathy with statins, CKD dose adjustment
**Evidence:** NNH for GI: ~50; avoid with strong CYP3A4 inhibitors (PMID: 31733140)

### Q5: Guidelines?
**Answer:** Class IIb in ESC 2024 for chronic CAD
**Evidence:** ESC 2024 CCS Guidelines, consider in patients with elevated hsCRP

## Clinical Context

### What Guidelines Say
ESC 2024: Class IIb, Level A - "Colchicine 0.5mg may be considered to reduce CV risk in chronic coronary syndrome"

### Practice Implications
- Best candidates: Stable CAD with elevated hsCRP despite optimal therapy
- Less certain: Immediately post-MI (COLCOT positive, but smaller effect)
- Probably not: Post-PCI without other CAD (CLEAR SYNERGY neutral)

## Content Hooks

1. "The inflammation hypothesis finally has a drug - and it's ancient"
2. "0.5mg for 50 cents - the cheapest CV prevention we've ignored"
3. "Why the cardiologist's gout drug became a heart drug"

## Citation-Ready References

1. Tardif JC, et al. COLCOT. NEJM. 2019. PMID: 31733140
2. Nidorf SM, et al. LoDoCo2. NEJM. 2020. PMID: 32865377
3. Jolly SS, et al. CLEAR SYNERGY. NEJM. 2024. PMID: 37634428
4. Ridker PM. Residual inflammatory risk. JACC. 2018. PMID: 29724838
5. ESC CCS Guidelines 2024

## Gaps & Caveats

- No RCT in primary prevention (only secondary prevention studied)
- Unclear benefit in patients with normal hsCRP
- Long-term safety (>3 years) data limited
- CLEAR SYNERGY challenges universal applicability

---

**Ready for your video!** You now have verified facts, PMIDs, and content hooks.

---

## Comparison with Other Skills

| Skill | Time | Depth | Use Case |
|-------|------|-------|----------|
| **quick-topic-researcher** | 5 min | Surface + key trials | Video prep, quick refresh |
| `deep-researcher` | 30-60 min | Comprehensive | Editorials, literature review |
| `pubmed-database` | 2 min | Single search | Specific question |
| `perplexity-search` | 1 min | Trend only | Discovery, non-citable |

---

## Technical Implementation

### Dependencies
- PubMed MCP (existing)
- Perplexity MCP (existing)
- Claude (default model)

### Parallel Execution
The skill uses Claude's ability to make multiple tool calls simultaneously:
```python
# These run in parallel (single message, multiple tool calls)
pubmed_search_articles(queryTerm="colchicine cardiovascular RCT", maxResults=10)
pubmed_search_articles(queryTerm="colchicine mechanism inflammation", maxResults=5)
perplexity_ask(messages=[{"role": "user", "content": "colchicine cardiology guidelines 2024"}])
```

### Output
- Markdown brief (displayed in terminal)
- Optional: Save to `~/research_briefs/{topic}_{date}.md`

---

*This skill gets you from "I need to know about X" to "I can confidently speak about X" in 5 minutes.*
