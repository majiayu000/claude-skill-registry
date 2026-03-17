---
name: seo-content-writer
description: 'Use when the user asks to "write SEO content", "create a blog post", "write an article", "content writing", "draft optimized content", "write me an article", "create a blog post about", "help me write SEO content", or "draft content for". Creates high-quality, SEO-optimized content that ranks in search engines. Applies on-page SEO best practices, keyword optimization, and content structure for maximum visibility and engagement. For AI citation optimization, see geo-content-optimizer. For updating existing content, see content-refresher.'
license: Apache-2.0
metadata:
  author: aaron-he-zhu
  version: "2.0.0"
  geo-relevance: "medium"
  tags:
    - seo
    - content writing
    - blog post
    - article
    - copywriting
    - content creation
    - on-page seo
  triggers:
    - "write SEO content"
    - "create blog post"
    - "write an article"
    - "content writing"
    - "draft optimized content"
    - "write for SEO"
    - "blog writing"
    - "write me an article"
    - "create a blog post about"
    - "help me write SEO content"
    - "draft content for"
---

# SEO Content Writer

This skill creates search-engine-optimized content that ranks well while providing genuine value to readers. It applies proven SEO copywriting techniques, proper keyword integration, and optimal content structure.

## When to Use This Skill

- Writing blog posts targeting specific keywords
- Creating landing pages optimized for search
- Developing pillar content for topic clusters
- Writing product descriptions for e-commerce
- Creating service pages for local SEO
- Producing how-to guides and tutorials
- Writing comparison and review articles

## What This Skill Does

1. **Keyword Integration**: Naturally incorporates target and related keywords
2. **Structure Optimization**: Creates scannable, well-organized content
3. **Title & Meta Creation**: Writes compelling, click-worthy titles
4. **Header Optimization**: Uses strategic H1-H6 hierarchy
5. **Internal Linking**: Suggests relevant internal link opportunities
6. **Readability Enhancement**: Ensures content is accessible and engaging
7. **Featured Snippet Optimization**: Formats for SERP feature opportunities

## How to Use

### Basic Content Creation

```
Write an SEO-optimized article about [topic] targeting the keyword [keyword]
```

```
Create a blog post for [topic] with these keywords: [keyword list]
```

### With Specific Requirements

```
Write a 2,000-word guide about [topic] targeting [keyword],
include FAQ section for featured snippets
```

### Content Briefs

```
Here's my content brief: [brief]. Write SEO-optimized content following this outline.
```

## Data Sources

> See [CONNECTORS.md](../../CONNECTORS.md) for tool category placeholders.

**With ~~SEO tool + ~~search console connected:**
Automatically pull keyword metrics (search volume, difficulty, CPC), competitor content analysis (top-ranking pages, content length, common topics), SERP features (featured snippets, PAA questions), and keyword opportunities (related keywords, question-based queries).

**With manual data only:**
Ask the user to provide:
1. Target primary keyword and 3-5 secondary keywords
2. Target audience and search intent (informational/commercial/transactional)
3. Target word count and desired tone
4. Any competitor URLs or content examples to reference

Proceed with the full workflow using provided data. Note in the output which metrics are from automated collection vs. user-provided data.

## Instructions

When a user requests SEO content:

1. **Gather Requirements**

   Confirm or ask for:
   
   ```markdown
   ### Content Requirements
   
   **Primary Keyword**: [main keyword]
   **Secondary Keywords**: [2-5 related keywords]
   **Target Word Count**: [length]
   **Content Type**: [blog/guide/landing page/etc.]
   **Target Audience**: [who is this for]
   **Search Intent**: [informational/commercial/transactional]
   **Tone**: [professional/casual/technical/friendly]
   **CTA Goal**: [what action should readers take]
   **Competitor URLs**: [top ranking content to beat]
   ```

2. **Load CORE-EEAT Quality Constraints**

   Before writing, load content quality standards from the [CORE-EEAT Benchmark](../../references/core-eeat-benchmark.md):

   ```markdown
   ### CORE-EEAT Pre-Write Checklist

   **Content Type**: [identified from requirements above]
   **Loaded Constraints** (high-weight items for this content type):

   Apply these standards while writing:

   | ID | Standard | How to Apply |
   |----|----------|-------------|
   | C01 | Intent Alignment | Title promise must match content delivery |
   | C02 | Direct Answer | Core answer in first 150 words |
   | C06 | Audience Targeting | State "this article is for..." |
   | C10 | Semantic Closure | Conclusion answers opening question + next steps |
   | O01 | Heading Hierarchy | H1→H2→H3, no level skipping |
   | O02 | Summary Box | Include TL;DR or Key Takeaways |
   | O06 | Section Chunking | Each section single topic; paragraphs 3–5 sentences |
   | O09 | Information Density | No filler; consistent terminology |
   | R01 | Data Precision | ≥5 precise numbers with units |
   | R02 | Citation Density | ≥1 external citation per 500 words |
   | R04 | Evidence-Claim Mapping | Every claim backed by evidence |
   | R07 | Entity Precision | Full names for people/orgs/products |
   | C03 | Query Coverage | Cover ≥3 query variants (synonyms, long-tail) |
   | O08 | Anchor Navigation | Table of contents with jump links |
   | O10 | Multimedia Structure | Images/videos have captions and carry information |
   | E07 | Practical Tools | Include downloadable templates, checklists, or calculators |

   _These 16 items apply across all content types. For content-type-specific dimension weights, see the Content-Type Weight Table in [core-eeat-benchmark.md](../../references/core-eeat-benchmark.md)._
   _Full 80-item benchmark: [references/core-eeat-benchmark.md](../../references/core-eeat-benchmark.md)_
   _For complete content quality audit: use [content-quality-auditor](../../cross-cutting/content-quality-auditor/)_
   ```

3. **Research and Plan**

   Before writing:
   
   ```markdown
   ### Content Research
   
   **SERP Analysis**:
   - Top results format: [what's ranking]
   - Average word count: [X] words
   - Common sections: [list]
   - SERP features: [snippets, PAA, etc.]
   
   **Keyword Map**:
   - Primary: [keyword] - use in title, H1, intro, conclusion
   - Secondary: [keywords] - use in H2s, body paragraphs
   - LSI/Related: [terms] - sprinkle naturally throughout
   - Questions: [PAA questions] - use as H2/H3s or FAQ
   
   **Content Angle**:
   [What unique perspective or value will this content provide?]
   ```

4. **Create Optimized Title**

   ```markdown
   ### Title Optimization
   
   **Requirements**:
   - Include primary keyword (preferably at start)
   - Under 60 characters for full SERP display
   - Compelling and click-worthy
   - Match search intent
   
   **Title Options**:
   
   1. [Title option 1] ([X] chars)
      - Keyword position: [front/middle]
      - Power words: [list]
   
   2. [Title option 2] ([X] chars)
      - Keyword position: [front/middle]
      - Power words: [list]
   
   **Recommended**: [Best option with reasoning]
   ```

5. **Write Meta Description**

   ```markdown
   ### Meta Description
   
   **Requirements**:
   - 150-160 characters
   - Include primary keyword naturally
   - Include call-to-action
   - Compelling and specific
   
   **Meta Description**:
   "[Description text]" ([X] characters)
   
   **Elements included**:
   - ✅ Primary keyword
   - ✅ Value proposition
   - ✅ CTA or curiosity hook
   ```

6. **Structure Content with SEO Headers**

   ```markdown
   ### Content Structure
   
   **H1**: [Primary keyword in H1 - only one per page]
   
   **Introduction** (100-150 words)
   - Hook reader in first sentence
   - State what they'll learn
   - Include primary keyword in first 100 words
   
   **H2**: [Secondary keyword or question]
   [Content section]
   
   **H2**: [Secondary keyword or question]
   
   **H3**: [Sub-topic]
   [Content]
   
   **H3**: [Sub-topic]
   [Content]
   
   **H2**: [Secondary keyword or question]
   [Content]
   
   **H2**: Frequently Asked Questions
   [FAQ section for PAA optimization]
   
   **Conclusion**
   - Summarize key points
   - Include primary keyword
   - Clear call-to-action
   ```

7. **Apply On-Page SEO Best Practices**

   ```markdown
   ### On-Page SEO Checklist
   
   **Keyword Placement**:
   - [ ] Primary keyword in title
   - [ ] Primary keyword in H1
   - [ ] Primary keyword in first 100 words
   - [ ] Primary keyword in at least one H2
   - [ ] Primary keyword in conclusion
   - [ ] Primary keyword in meta description
   - [ ] Secondary keywords in H2s/H3s
   - [ ] Related terms throughout body
   
   **Content Quality**:
   - [ ] Comprehensive coverage of topic
   - [ ] Original insights or data
   - [ ] Actionable takeaways
   - [ ] Examples and illustrations
   - [ ] Expert quotes or citations (for E-E-A-T)
   
   **Readability**:
   - [ ] Paragraphs of 3-5 sentences (per CORE-EEAT O06 Section Chunking standard)
   - [ ] Varied sentence length
   - [ ] Bullet points and lists
   - [ ] Bold key phrases
   - [ ] Table of contents for long content
   
   **Technical**:
   - [ ] Internal links to relevant pages (2-5)
   - [ ] External links to authoritative sources (2-3)
   - [ ] Image alt text with keywords
   - [ ] URL slug includes keyword
   ```

8. **Write the Content**

   Follow this structure:

   ```markdown
   # [H1 with Primary Keyword]
   
   [Hook sentence that grabs attention]
   
   [Problem statement or context - why this matters]
   
   [Promise - what the reader will learn/gain] [Include primary keyword naturally]
   
   [Brief overview of what's covered - can be bullet points for scanability]
   
   ## [H2 - First Main Section with Secondary Keyword]
   
   [Introduction to section - 1-2 sentences]
   
   [Main content with valuable information]
   
   [Examples, data, or evidence to support points]
   
   [Transition to next section]
   
   ### [H3 - Sub-section if needed]
   
   [Detailed content]
   
   [Key points in bullet format]:
   - Point 1
   - Point 2
   - Point 3
   
   ## [H2 - Second Main Section]
   
   [Continue with valuable content...]
   
   > **Pro Tip**: [Highlighted tip or key insight]
   
   | Column 1 | Column 2 | Column 3 |
   |----------|----------|----------|
   | Data | Data | Data |
   
   ## [H2 - Additional Sections as Needed]
   
   [Content...]
   
   ## Frequently Asked Questions
   
   ### [Question from PAA or common query]?
   
   [Direct, concise answer in 40-60 words for featured snippet opportunity]
   
   ### [Question 2]?
   
   [Answer]
   
   ### [Question 3]?
   
   [Answer]
   
   ## Conclusion
   
   [Summary of key points - include primary keyword]
   
   [Final thought or insight]
   
   [Clear call-to-action: what should reader do next?]
   ```

9. **Optimize for Featured Snippets**

   ```markdown
   ### Featured Snippet Optimization
   
   **For Definition Snippets**:
   "[Term] is [clear, concise definition in 40-60 words]"
   
   **For List Snippets**:
   Create clear, numbered or bulleted lists under H2s
   
   **For Table Snippets**:
   Use comparison tables with clear headers
   
   **For How-To Snippets**:
   Number each step clearly: "Step 1:", "Step 2:", etc.
   ```

10. **Add Internal/External Links**

   ```markdown
   ### Link Recommendations
   
   **Internal Links** (include 2-5):
   1. "[anchor text]" → [/your-page-url] (relevant because: [reason])
   2. "[anchor text]" → [/your-page-url] (relevant because: [reason])
   
   **External Links** (include 2-3 authoritative sources):
   1. "[anchor text]" → [authoritative-source.com] (supports: [claim])
   2. "[anchor text]" → [authoritative-source.com] (supports: [claim])
   ```

11. **Final SEO Review**

    ```markdown
    ### Content SEO Score

    | Factor | Status | Notes |
    |--------|--------|-------|
    | Title optimized | ✅/⚠️/❌ | [notes] |
    | Meta description | ✅/⚠️/❌ | [notes] |
    | H1 with keyword | ✅/⚠️/❌ | [notes] |
    | Keyword in first 100 words | ✅/⚠️/❌ | [notes] |
    | H2s optimized | ✅/⚠️/❌ | [notes] |
    | Internal links | ✅/⚠️/❌ | [notes] |
    | External links | ✅/⚠️/❌ | [notes] |
    | FAQ section | ✅/⚠️/❌ | [notes] |
    | Readability | ✅/⚠️/❌ | [notes] |
    | Word count | ✅/⚠️/❌ | [X] words |

    **Overall SEO Score**: [X]/10

    **Improvements to Consider**:
    1. [Suggestion]
    2. [Suggestion]
    ```

12. **CORE-EEAT Self-Check**

    After writing, verify content against loaded CORE-EEAT constraints:

    ```markdown
    ### CORE-EEAT Post-Write Check

    | ID | Standard | Status | Notes |
    |----|----------|--------|-------|
    | C01 | Intent Alignment: title = content | ✅/⚠️/❌ | [notes] |
    | C02 | Direct Answer in first 150 words | ✅/⚠️/❌ | [notes] |
    | C06 | Audience explicitly stated | ✅/⚠️/❌ | [notes] |
    | C10 | Conclusion answers opening question | ✅/⚠️/❌ | [notes] |
    | O01 | Heading hierarchy correct | ✅/⚠️/❌ | [notes] |
    | O02 | Summary/Key Takeaways present | ✅/⚠️/❌ | [notes] |
    | O06 | Paragraphs 3–5 sentences | ✅/⚠️/❌ | [notes] |
    | O09 | No filler; consistent terms | ✅/⚠️/❌ | [notes] |
    | R01 | ≥5 precise data points with units | ✅/⚠️/❌ | [notes] |
    | R02 | ≥1 citation per 500 words | ✅/⚠️/❌ | [notes] |
    | R04 | Claims backed by evidence | ✅/⚠️/❌ | [notes] |
    | R07 | Full entity names used | ✅/⚠️/❌ | [notes] |
    | C03 | ≥3 query variants covered | ✅/⚠️/❌ | [notes] |
    | O08 | Table of contents with jump links | ✅/⚠️/❌ | [notes] |
    | O10 | Images/videos captioned and informative | ✅/⚠️/❌ | [notes] |
    | E07 | Downloadable template/checklist included | ✅/⚠️/❌ | [notes] |

    **Items Needing Attention**: [list any ⚠️/❌ items]

    _For full 80-item audit, use [content-quality-auditor](../../cross-cutting/content-quality-auditor/)_
    ```

## Validation Checkpoints

### Input Validation
- [ ] Primary keyword confirmed and matches search intent
- [ ] Target word count specified (minimum 800 words for substantive content)
- [ ] Content type and audience clearly defined
- [ ] Competitor URLs reviewed or target SERP features identified

### Output Validation
- [ ] Keyword density within 1-2% for primary keyword (Note: Keyword density is a guideline, not a hard rule. Modern search engines prioritize semantic relevance and natural language over exact density targets. Focus on covering the topic comprehensively with semantic variants rather than hitting a specific percentage.)
- [ ] All sections from outline covered completely
- [ ] Internal links included (2-5 relevant links)
- [ ] FAQ section present with at least 3 questions
- [ ] Readability score appropriate for target audience
- [ ] Source of each data point clearly stated (~~SEO tool data, user-provided, or estimated)

## Example

**User**: "Write an SEO-optimized article about 'email marketing best practices' targeting small businesses"

**Output**:

```markdown
# Email Marketing Best Practices: A Complete Guide for Small Businesses

**Meta Description**: Discover proven email marketing best practices that help small businesses increase open rates, boost engagement, and drive sales. Start improving your campaigns today. (158 chars)

---

Want to know the secret behind small businesses that consistently turn subscribers into loyal customers? It's not luck—it's strategic email marketing.

Email marketing remains one of the most effective channels for small businesses, delivering an average ROI of $42 for every $1 spent. But with inboxes more crowded than ever, following email marketing best practices isn't optional—it's essential for survival.

In this guide, you'll learn:
- How to build a quality email list that converts
- Proven strategies to increase open and click rates
- Advanced personalization techniques that drive results
- Common mistakes that kill email performance

Let's dive into the strategies that will transform your email marketing.

## Why Email Marketing Matters for Small Businesses

Before we explore the best practices, let's understand why email deserves your attention.

Unlike social media where algorithms control who sees your content, email gives you direct access to your audience. You own your email list—no platform can take it away.

**Key email marketing statistics for small businesses**:
- 81% of SMBs rely on email as their primary customer acquisition channel
- Email subscribers are 3x more likely to share content on social media
- Personalized emails generate 6x higher transaction rates

## Building a High-Quality Email List

### Use Strategic Opt-in Incentives

The foundation of effective email marketing is a quality list. Here's how to grow yours:

**Lead magnets that convert**:
- Industry-specific templates
- Exclusive discounts or early access
- Free tools or calculators
- Educational email courses

> **Pro Tip**: The best lead magnets solve a specific, immediate problem for your target audience.

### Implement Double Opt-in

Double opt-in confirms subscriber intent and improves deliverability. Yes, you'll have fewer subscribers, but they'll be more engaged.

| Single Opt-in | Double Opt-in |
|---------------|---------------|
| More subscribers | Fewer subscribers |
| Higher bounce rates | Lower bounce rates |
| Lower engagement | Higher engagement |
| Spam risk | Better deliverability |

## Crafting Emails That Get Opened

### Write Compelling Subject Lines

Your subject line determines whether emails get opened or ignored.

**Subject line best practices**:
1. Keep it under 50 characters
2. Create urgency without being spammy
3. Use numbers and specifics
4. Personalize when possible
5. A/B test consistently

### Optimize Preview Text

The preview text (preheader) is your second chance to convince someone to open. Use it to expand on your subject line, not repeat it.

## Personalization Strategies That Work

Generic emails perform poorly. Here's how to personalize effectively:

### Segment Your Email List

Divide your list based on:
- Purchase history
- Engagement level
- Demographics
- Interests or preferences
- Customer lifecycle stage

### Use Dynamic Content

Send the same email but show different content blocks based on subscriber data.

## Frequently Asked Questions

### How often should small businesses send marketing emails?

For most small businesses, sending 1-2 emails per week strikes the right balance. This keeps you top-of-mind without overwhelming subscribers. Monitor your unsubscribe rates—if they spike after increasing frequency, scale back.

### What is a good email open rate for small businesses?

A good email open rate for small businesses is 20-25%. However, this varies by industry. E-commerce averages 15-20%, while B2B services often see 25-30%. Focus on improving your own benchmarks rather than industry averages.

### Should I buy email lists to grow faster?

Never buy email lists. Purchased lists violate GDPR and CAN-SPAM regulations, damage your sender reputation, and result in poor engagement. Organic list growth, while slower, produces much better results.

## Conclusion

Implementing these email marketing best practices will help your small business build stronger customer relationships and drive consistent revenue. Remember: quality always beats quantity in email marketing.

Start with one improvement today. Whether it's segmenting your list, testing subject lines, or cleaning inactive subscribers, small changes compound into significant results.

**Ready to level up your email marketing?** Download our free Email Marketing Checklist to ensure every campaign you send follows these best practices.

---

*Further reading: [Internal link: "How to Write Email Copy That Converts"]*

*Sources: [Litmus Email Marketing Statistics](https://litmus.com), [Campaign Monitor Email Benchmarks](https://campaignmonitor.com)*
```

## Content Type Templates

### How-To Guide

```
Write a how-to guide for [task] targeting [keyword]
```

### Comparison Article

```
Write a comparison article: [Option A] vs [Option B] for [keyword]
```

### Listicle

```
Write a list post: "X Best [Items] for [Audience/Purpose]" targeting [keyword]
```

### Ultimate Guide

```
Write an ultimate guide about [topic] (3,000+ words) targeting [keyword]
```

## Tips for Success

1. **Match search intent** - Informational queries need guides, not sales pages
2. **Front-load value** - Put key information early for readers and snippets
3. **Use data and examples** - Specific beats generic every time
4. **Write for humans first** - SEO optimization should feel natural
5. **Include visual elements** - Break up text with images, tables, lists
6. **Update regularly** - Fresh content signals to search engines

## Reference Materials

- [Title Formulas](./references/title-formulas.md) - Proven headline formulas, power words, CTR patterns
- [Content Structure Templates](./references/content-structure-templates.md) - Templates for blog posts, comparisons, listicles, how-tos, pillar pages

## Related Skills

- [keyword-research](../../research/keyword-research/) — Find keywords to target
- [geo-content-optimizer](../geo-content-optimizer/) — Optimize for AI citations
- [meta-tags-optimizer](../meta-tags-optimizer/) — Create compelling meta tags
- [on-page-seo-auditor](../../optimize/on-page-seo-auditor/) — Audit SEO elements
- [internal-linking-optimizer](../../optimize/internal-linking-optimizer/) — Place internal links during content writing
- [content-refresher](../../optimize/content-refresher/) — Refresh and update existing content
- [content-quality-auditor](../../cross-cutting/content-quality-auditor/) — Full 80-item CORE-EEAT audit
- [memory-management](../../cross-cutting/memory-management/) — Track content performance over time
- [content-gap-analysis](../../research/content-gap-analysis/) — Identify content opportunities to write about
- [schema-markup-generator](../schema-markup-generator/) — Add structured data to published content

