---
name: geo-content-optimizer
version: "1.0"
description: Optimizes content for Generative Engine Optimization (GEO) to increase chances of being cited by AI systems like ChatGPT, Claude, Perplexity, and Google AI Overviews. Makes content AI-friendly while maintaining SEO value.
---

# GEO Content Optimizer

This skill optimizes content to appear in AI-generated responses. As AI systems increasingly answer user queries directly, getting cited by these systems becomes crucial for visibility.

## When to Use This Skill

- Optimizing existing content for AI citations
- Creating new content designed for both SEO and GEO
- Improving chances of appearing in AI Overviews
- Making content more quotable by AI systems
- Adding authority signals that AI systems trust
- Structuring content for AI comprehension
- Competing for visibility in the AI-first search era

## What This Skill Does

1. **Citation Optimization**: Makes content more likely to be quoted by AI
2. **Structure Enhancement**: Formats content for AI comprehension
3. **Authority Building**: Adds signals that AI systems trust
4. **Factual Enhancement**: Improves accuracy and verifiability
5. **Quote Creation**: Creates memorable, citeable statements
6. **Source Attribution**: Adds proper citations that AI can verify
7. **GEO Scoring**: Evaluates content's AI-friendliness

## How to Use

### Optimize Existing Content

```
Optimize this content for GEO/AI citations: [content or URL]
```

```
Make this article more likely to be cited by AI systems
```

### Create GEO-Optimized Content

```
Write content about [topic] optimized for both SEO and GEO
```

### GEO Audit

```
Audit this content for GEO readiness and suggest improvements
```

## Data Sources

> See [CONNECTORS.md](../../CONNECTORS.md) for tool category placeholders.

**With ~~AI monitor + ~~SEO tool connected:**
Automatically pull AI citation patterns (which content is being cited by ChatGPT, Claude, Perplexity), current AI visibility scores, competitor citation frequency, and AI Overview appearance tracking.

**With manual data only:**
Ask the user to provide:
1. Target queries where they want AI citations
2. Current content URL or full content text
3. Any known instances where competitors are being cited by AI

Proceed with the full workflow using provided data. Note in the output which metrics are from automated collection vs. user-provided data.

## Instructions

When a user requests GEO optimization:

1. **Load CORE-EEAT GEO-First Optimization Targets**

   Before optimizing, load GEO-critical items from the [CORE-EEAT Benchmark](../../references/core-eeat-benchmark.md):

   ```markdown
   ### CORE-EEAT GEO-First Targets

   These items have the highest impact on AI engine citation. Use as optimization checklist:

   **Top 6 Priority Items**:
   | Rank | ID | Standard | Why It Matters |
   |------|----|----------|---------------|
   | 1 | C02 | Direct Answer in first 150 words | All engines extract from first paragraph |
   | 2 | C09 | Structured FAQ with Schema | Directly matches AI follow-up queries |
   | 3 | O03 | Data in tables, not prose | Most extractable structured format |
   | 4 | O05 | JSON-LD Schema Markup | Helps AI understand content type |
   | 5 | E01 | Original first-party data | AI prefers exclusive, verifiable sources |
   | 6 | O02 | Key Takeaways / Summary Box | First choice for AI summary citations |

   **All GEO-First Items** (optimize for all when possible):
   C02, C04, C05, C07, C08, C09 | O02, O03, O04, O05, O06, O09
   R01, R02, R03, R04, R05, R07, R09 | E01, E02, E03, E04, E06, E08, E09, E10
   Exp10 | Ept05, Ept08 | A08

   **AI Engine Preferences**:
   | Engine | Priority Items |
   |--------|----------------|
   | Google AI Overview | C02, O03, O05, C09 |
   | ChatGPT Browse | C02, R01, R02, E01 |
   | Perplexity AI | E01, R03, R05, Ept05 |
   | Claude | R04, Ept08, Exp10, R03 |

   _Full benchmark: [references/core-eeat-benchmark.md](../../references/core-eeat-benchmark.md)_
   ```

2. **Understand GEO Fundamentals**

   ```markdown
   ### How AI Systems Select Content to Cite
   
   AI systems prioritize content that is:
   
   **Authoritative**
   - From recognized experts or trusted sources
   - Contains proper citations and references
   - Shows expertise signals (author credentials, original research)
   
   **Accurate**
   - Factually correct and verifiable
   - Up-to-date information
   - Consistent with consensus knowledge
   
   **Clear**
   - Well-structured and organized
   - Contains clear definitions and explanations
   - Uses unambiguous language
   
   **Quotable**
   - Has standalone statements that answer questions
   - Contains specific facts, statistics, and data
   - Includes memorable, concise explanations
   ```

3. **Analyze Current Content**

   ```markdown
   ## GEO Analysis: [Content Title]
   
   ### Current State Assessment
   
   | GEO Factor | Current Score (1-10) | Notes |
   |------------|---------------------|-------|
   | Clear definitions | [X] | [notes] |
   | Quotable statements | [X] | [notes] |
   | Factual density | [X] | [notes] |
   | Source citations | [X] | [notes] |
   | Q&A format | [X] | [notes] |
   | Authority signals | [X] | [notes] |
   | Content freshness | [X] | [notes] |
   | Structure clarity | [X] | [notes] |
   | **GEO Readiness** | **[avg]/10** | **Average across factors** |
   
   **Primary Weaknesses**:
   1. [Weakness 1]
   2. [Weakness 2]
   3. [Weakness 3]
   
   **Quick Wins**:
   1. [Quick improvement 1]
   2. [Quick improvement 2]
   ```

4. **Optimize for Clear Definitions**

   AI systems love clear, quotable definitions.

   ```markdown
   ### Definition Optimization
   
   **Before** (Weak for GEO):
   > SEO is really important for businesses and involves various 
   > techniques to improve visibility online through search engines.
   
   **After** (Strong for GEO):
   > **Search Engine Optimization (SEO)** is the practice of optimizing 
   > websites and content to rank higher in search engine results pages 
   > (SERPs), increasing organic traffic and visibility.
   
   **Definition Template**:
   "[Term] is [clear category/classification] that [primary function/purpose], 
   [key characteristic or benefit]."
   
   **Checklist for GEO-Optimized Definitions**:
   - [ ] Starts with the term being defined
   - [ ] Provides clear category (what type of thing it is)
   - [ ] Explains primary function or purpose
   - [ ] Uses precise, unambiguous language
   - [ ] Can stand alone as a complete answer
   - [ ] Is 25-50 words for optimal citation length
   ```

5. **Create Quotable Statements**

   ```markdown
   ### Quotable Statement Optimization
   
   AI systems cite specific, standalone statements. Transform vague 
   content into quotable facts.
   
   **Weak (Not quotable)**:
   > Email marketing is pretty effective and lots of companies use it.
   
   **Strong (Quotable)**:
   > Email marketing delivers an average ROI of $42 for every $1 spent, 
   > making it one of the highest-performing digital marketing channels.
   
   **Types of Quotable Statements**:
   
   1. **Statistics**
      - Include specific numbers
      - Cite the source
      - Add context (timeframe, comparison)
      
      Example: "According to [Source], [specific statistic] as of [date]."
   
   2. **Facts**
      - Verifiable information
      - Unambiguous language
      - Authoritative source
      
      Example: "[Subject] was [fact], according to [authoritative source]."
   
   3. **Definitions** (covered above)
   
   4. **Comparisons**
      - Clear comparison structure
      - Specific differentiators
      
      Example: "Unlike [A], [B] [specific difference], which means [implication]."
   
   5. **How-to Steps**
      - Numbered, clear steps
      - Action-oriented language
      
      Example: "To [achieve goal], [step 1], then [step 2], and finally [step 3]."
   ```

6. **Add Authority Signals**

   ```markdown
   ### Authority Signal Enhancement
   
   **Expert Attribution**
   
   Add expert quotes and credentials:
   
   > "AI will transform how we search for information," says Dr. Jane Smith, 
   > AI Research Director at Stanford University.
   
   **Source Citations**
   
   Properly cite sources that AI can verify:
   
   Before:
   > Studies show that most people prefer video content.
   
   After:
   > According to Wyzowl's 2024 Video Marketing Statistics report, 
   > 91% of consumers want to see more online video content from brands.
   
   **Authority Elements to Add**:
   - [ ] Author byline with credentials
   - [ ] Expert quotes with attribution
   - [ ] Citations to peer-reviewed research
   - [ ] References to recognized authorities
   - [ ] Original data or research
   - [ ] Case studies with named companies
   - [ ] Industry statistics with sources
   ```

7. **Optimize Content Structure**

   ```markdown
   ### Structure Optimization for GEO
   
   AI systems parse structured content more effectively.
   
   **Q&A Format**
   
   Transform content into question-answer pairs:
   
   ```html
   <h2>What is [Topic]?</h2>
   <p>[Direct answer in 40-60 words]</p>
   
   <h2>How does [Topic] work?</h2>
   <p>[Clear explanation with steps if applicable]</p>
   
   <h2>Why is [Topic] important?</h2>
   <p>[Specific reasons with evidence]</p>
   ```
   
   **Comparison Tables**
   
   For comparison queries, use clear tables:
   
   | Feature | Option A | Option B |
   |---------|----------|----------|
   | [Feature 1] | [Specific value] | [Specific value] |
   | [Feature 2] | [Specific value] | [Specific value] |
   | **Best for** | [Use case] | [Use case] |
   
   **Numbered Lists**
   
   For process or list queries:
   
   1. **Step 1: [Action]** - [Brief explanation]
   2. **Step 2: [Action]** - [Brief explanation]
   3. **Step 3: [Action]** - [Brief explanation]
   
   **Definition Boxes**
   
   Highlight key definitions:
   
   > **Key Definition**: [Term] refers to [clear definition].
   ```

8. **Enhance Factual Density**

   ```markdown
   ### Factual Density Improvement
   
   AI systems prefer fact-rich content over opinion-heavy content.
   
   **Content Transformation**:
   
   **Low factual density**:
   > Social media marketing is very popular nowadays. Many businesses 
   > use it and find it helpful for reaching customers.
   
   **High factual density**:
   > Social media marketing reaches 4.9 billion users globally (Statista, 2024). 
   > Businesses using social media marketing report 66% higher lead generation 
   > rates compared to non-users (HubSpot State of Marketing Report, 2024). 
   > The most effective platforms for B2B marketing are LinkedIn (96% usage), 
   > Twitter (82%), and Facebook (80%).
   
   **Factual Enhancement Checklist**:
   - [ ] Add specific statistics with sources
   - [ ] Include exact dates, numbers, percentages
   - [ ] Replace vague claims with verified facts
   - [ ] Add recent data (within last 2 years)
   - [ ] Include multiple data points per section
   - [ ] Cross-reference with authoritative sources
   ```

9. **Implement FAQ Schema**

   ```markdown
   ### FAQ Optimization for GEO
   
   FAQ sections are highly effective for GEO because:
   - They match question-based AI queries
   - They provide concise, structured answers
   - FAQ schema helps AI understand Q&A pairs
   
   **FAQ Structure**:
   
   ## Frequently Asked Questions
   
   ### [Question matching common query]?
   
   [Direct answer: 40-60 words]
   [Supporting detail or example]
   
   ### [Question matching common query]?
   
   [Direct answer: 40-60 words]
   [Supporting detail or example]
   
   **FAQ Schema (JSON-LD)**:
   
   ```json
   {
     "@context": "https://schema.org",
     "@type": "FAQPage",
     "mainEntity": [{
       "@type": "Question",
       "name": "[Question text]",
       "acceptedAnswer": {
         "@type": "Answer",
         "text": "[Answer text]"
       }
     }]
   }
   ```
   ```

10. **Generate GEO-Optimized Output**

   ```markdown
   ## GEO Optimization Report

   ### Changes Made

   **Definitions Added/Improved**:
   1. [Definition 1] - [location in content]
   2. [Definition 2] - [location in content]

   **Quotable Statements Created**:
   1. "[Statement 1]"
   2. "[Statement 2]"

   **Authority Signals Added**:
   1. [Expert quote/citation]
   2. [Source attribution]

   **Structural Improvements**:
   1. [Change 1]
   2. [Change 2]

   ### Before/After GEO Score

   | GEO Factor | Before (1-10) | After (1-10) | Change |
   |------------|---------------|--------------|--------|
   | Clear definitions | [X] | [X] | +[X] |
   | Quotable statements | [X] | [X] | +[X] |
   | Factual density | [X] | [X] | +[X] |
   | Source citations | [X] | [X] | +[X] |
   | Q&A format | [X] | [X] | +[X] |
   | Authority signals | [X] | [X] | +[X] |
   | **Overall GEO Score** | **[avg]/10** | **[avg]/10** | **+[X]** |

   ### AI Query Coverage

   This content is now optimized to answer:
   - "What is [topic]?" ✅
   - "How does [topic] work?" ✅
   - "Why is [topic] important?" ✅
   - "[Topic] vs [alternative]" ✅
   - "Best [topic] for [use case]" ✅
   ```

11. **CORE-EEAT GEO Self-Check**

    After optimization, verify GEO-First items:

    ```markdown
    ### CORE-EEAT GEO Post-Optimization Check

    | ID | Standard | Status | Notes |
    |----|----------|--------|-------|
    | C02 | Direct Answer in first 150 words | ✅/⚠️/❌ | [notes] |
    | C04 | Key terms defined on first use | ✅/⚠️/❌ | [notes] |
    | C09 | Structured FAQ with Schema | ✅/⚠️/❌ | [notes] |
    | O02 | Summary Box / Key Takeaways | ✅/⚠️/❌ | [notes] |
    | O03 | Comparisons in tables | ✅/⚠️/❌ | [notes] |
    | O05 | JSON-LD Schema Markup | ✅/⚠️/❌ | [notes] |
    | O06 | Section chunking (3–5 sentences) | ✅/⚠️/❌ | [notes] |
    | R01 | ≥5 precise data points with units | ✅/⚠️/❌ | [notes] |
    | R02 | ≥1 citation per 500 words | ✅/⚠️/❌ | [notes] |
    | R04 | Claims backed by evidence | ✅/⚠️/❌ | [notes] |
    | R07 | Full entity names | ✅/⚠️/❌ | [notes] |
    | E01 | Original first-party data | ✅/⚠️/❌ | [notes] |
    | Exp10 | Limitations acknowledged | ✅/⚠️/❌ | [notes] |
    | Ept08 | Reasoning transparency | ✅/⚠️/❌ | [notes] |

    **Items Needing Attention**: [list any ⚠️/❌ items]

    _For full 80-item audit, use [content-quality-auditor](../../cross-cutting/content-quality-auditor/)_
    ```

## Validation Checkpoints

### Input Validation
- [ ] Content source identified (URL, full text, or content draft)
- [ ] Target AI queries or topics clearly defined
- [ ] Current GEO baseline assessed (if optimizing existing content)

### Output Validation
- [ ] At least 3 clear, quotable definitions added
- [ ] Factual density improved with at least 5 verifiable statistics
- [ ] All claims have source citations from authoritative sources
- [ ] Q&A format sections cover top 5 user queries
- [ ] GEO score improvement of at least 50% from baseline
- [ ] Source of each data point clearly stated (~~AI monitor data, user-provided, or estimated)

## Example

**User**: "Optimize this paragraph for GEO: 'Email marketing is a good way to reach customers. It's been around for a while and many businesses use it. You can send newsletters, promotions, and other messages.'"

**Output**:

```markdown
## GEO-Optimized Version

**Email marketing** is a digital marketing strategy that uses email to promote 
products, build customer relationships, and drive conversions. According to 
the Data & Marketing Association, email marketing delivers an average ROI 
of $42 for every $1 invested, making it the highest-performing digital 
marketing channel.

### Key email marketing formats include:

1. **Newsletters**: Regular updates sharing company news, industry insights, 
   and valuable content to maintain subscriber engagement
2. **Promotional emails**: Time-sensitive offers, discounts, and product 
   announcements designed to drive immediate sales
3. **Transactional emails**: Order confirmations, shipping updates, and 
   account notifications with 8x higher open rates than marketing emails
4. **Automated sequences**: Pre-scheduled email series triggered by user 
   actions, such as welcome series or abandoned cart reminders

> **Key statistic**: 81% of small businesses rely on email as their primary 
> customer acquisition channel (Emarsys, 2024).

---

### Changes Made:

| Element | Before | After |
|---------|--------|-------|
| Definition | None | Clear definition with category |
| Statistics | None | 2 specific stats with sources |
| Structure | Single paragraph | Structured list with headers |
| Authority | None | DMA and Emarsys citations |
| Quotable statements | 0 | 3 standalone facts |

**GEO Score**: Improved from 1/10 to 8/10
```

## GEO Optimization Checklist

Use this checklist for any content:

```markdown
### GEO Readiness Checklist

**Definitions & Clarity**
- [ ] Key terms are clearly defined
- [ ] Definitions can stand alone as answers
- [ ] Language is precise and unambiguous

**Quotable Content**
- [ ] Specific statistics included
- [ ] Facts have source citations
- [ ] Memorable statements created

**Authority**
- [ ] Expert quotes or credentials present
- [ ] Authoritative sources cited
- [ ] Original data or research included

**Structure**
- [ ] Q&A format sections included
- [ ] Clear headings match common queries
- [ ] Comparison tables where relevant
- [ ] Numbered lists for processes

**Technical**
- [ ] FAQ schema markup added
- [ ] Content freshness indicated
- [ ] Sources are verifiable
```

## Tips for Success

1. **Answer the question first** - Put the answer in the first sentence
2. **Be specific** - Vague content doesn't get cited
3. **Cite sources** - AI systems trust verifiable information
4. **Stay current** - Update statistics and facts regularly
5. **Match query format** - Questions deserve direct answers
6. **Build authority** - Expert credentials increase citation likelihood

## Reference Materials

- [AI Citation Patterns](./references/ai-citation-patterns.md) - How Google AI Overviews, ChatGPT, Perplexity, and Claude select and cite sources
- [Quotable Content Examples](./references/quotable-content-examples.md) - Before/after examples of content optimized for AI citation

## Related Skills

- [seo-content-writer](../seo-content-writer/) - Create SEO content to optimize
- [schema-markup-generator](../schema-markup-generator/) - Add structured data
- [keyword-research](../../research/keyword-research/) - Identify keyword targets for GEO optimization
- [content-refresher](../../optimize/content-refresher/) - Update content for freshness
- [serp-analysis](../../research/serp-analysis/) - Analyze AI Overview patterns
- [content-quality-auditor](../../cross-cutting/content-quality-auditor/) - Full 80-item CORE-EEAT audit
- [domain-authority-auditor](../../cross-cutting/domain-authority-auditor/) — Domain-level AI citation signals (CITE C05-C08) complement page-level GEO optimization

