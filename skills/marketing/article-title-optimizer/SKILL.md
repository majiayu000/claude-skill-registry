---
name: article-title-optimizer
description: 'This skill analyzes article content in-depth and generates optimized,
  marketable titles in the format ''Title: Subtitle'' (10-12 words maximum). The skill
  should be used when users request title optimiz'
---

---
name: article-title-optimizer
description: This skill analyzes article content in-depth and generates optimized, marketable titles in the format 'Title: Subtitle' (10-12 words maximum). The skill should be used when users request title optimization, title generation, or title improvement for articles, blog posts, or written content. It generates 5 title candidates using proven formulas, evaluates them against success criteria (clickability, SEO, clarity, emotional impact, memorability, shareability), and replaces the article's title with the winning candidate.
---

# Article Title Optimizer

## Overview

This skill transforms article titles into marketable, attention-grabbing headlines that follow the `<Title>: <Subtitle>` format while maintaining accuracy and avoiding deception. The skill analyzes article content deeply, generates five diverse title candidates using proven copywriting formulas, evaluates each against weighted success criteria, and automatically replaces the original title with the optimal choice.

## Workflow

Follow this sequential process to optimize article titles:

### Step 1: Read and Analyze the Article

Read the article file provided by the user to understand:
- **Core thesis or argument**: What is the main point or claim?
- **Key findings or insights**: What are the most important takeaways?
- **Primary audience**: Who is this written for? (Technical experts, general public, professionals, etc.)
- **Emotional tone**: Is it serious, provocative, optimistic, cautionary, analytical?
- **Main keywords**: What terms are central to the topic and likely search queries?
- **Article type**: Technical/professional, general interest, news, opinion/commentary, how-to guide

**Example analysis for a healthcare AI article:**
- Core thesis: AI in radiology has transformative potential but faces serious challenges around bias, transparency, and equity
- Key findings: AI systems show bias against underserved populations, black-box nature creates trust issues, most benefits accrue to wealthy institutions
- Primary audience: Healthcare professionals, policymakers, tech-aware general readers
- Emotional tone: Serious, cautionary, balanced
- Main keywords: AI, radiology, bias, healthcare equity, transparency, trust
- Article type: Long-form analysis/commentary on emerging technology

### Step 2: Research Title Best Practices

Before generating candidates, review `references/title_best_practices.md` which contains:
- Proven title formulas (question, how-to, problem-solution, contrarian, etc.)
- Success criteria and evaluation framework
- Common pitfalls to avoid
- Industry-specific considerations
- Before/after examples

If needed, use web search to research:
- Current trends in article title writing for the specific industry
- Successful titles in similar topic areas
- SEO best practices for the article's subject matter
- Audience preferences for the content type

**Note**: Research should inform title generation but titles must remain authentic to the article content.

### Step 3: Generate 5 Title Candidates

Create five diverse title candidates using different formulas from the reference guide. Each title must:
- Follow the `<Title>: <Subtitle>` format
- Be 10-12 words maximum (total for both parts)
- Accurately represent the article content
- Use different approaches/formulas to provide variety
- Avoid deception, clickbait, or misleading claims

**CRITICAL CONSTRAINTS - All titles must comply:**
1. **No AI-generated tropes**: Avoid obvious AI writing patterns, especially "Algorithm/Algorithmic/Algorithms", "Black-Box/Black Box", and clichéd phrasing like "The X Will See You Now", "Welcome to the Age of X", "The Rise of X"
2. **No apostrophes**: Do not use apostrophes anywhere in the title (not "don't", "can't", "it's", "AI's", etc.)
3. **No question marks in Title segment**: Question marks create visually awkward ?: combinations when rendered. Questions may be used in the Subtitle segment only, or rephrase as statements.

**Example candidates for healthcare AI article:**

1. **Statement Format**: "Medical AI and Trust: Why Bias Threatens Healthcare Equity"
2. **Problem-Solution Format**: "Opaque AI in Healthcare: Why Explainability Matters Now"
3. **Contrarian Format**: "AI Will Not Replace Radiologists: But Everything Changes"
4. **Impact Format**: "When Medical AI Fails Minorities: The Data Representation Crisis"
5. **Examination Format**: "Navigating Healthcare AI: Trust, Bias, and the Path Forward"

### Step 4: Evaluate Each Candidate Against Success Criteria

Score each title candidate (1-10 scale) across six weighted criteria:

1. **Clickability (25% weight)**: Attention-grabbing power, curiosity gap, use of power words
   - High: Creates strong curiosity, specific and compelling
   - Low: Generic, boring, or too vague

2. **SEO Effectiveness (20% weight)**: Search optimization and discoverability
   - Keyword placement in first 3-5 words
   - Length 50-60 characters ideal
   - Natural language, not keyword-stuffed

3. **Clarity/Informativeness (20% weight)**: How well title communicates content
   - High: Reader knows exactly what to expect
   - Low: Vague, confusing, or misleading

4. **Emotional Impact (15% weight)**: Emotional resonance and engagement
   - Curiosity, surprise, urgency, relevance to reader concerns

5. **Memorability (10% weight)**: Likelihood to stick in mind
   - Distinctive phrasing, rhythmic flow, concrete language

6. **Social Shareability (10% weight)**: Likelihood to be shared
   - Identity expression, conversation starter, platform fit

**Example evaluation for Candidate 1:**
- Clickability: 8/10 (trust and bias angle creates curiosity)
- SEO: 8/10 (strong keywords "Medical AI", "Trust", "Bias" well-placed)
- Clarity: 9/10 (very clear what article covers)
- Emotional Impact: 7/10 (trust and equity concerns resonate)
- Memorability: 7/10 (clear and direct phrasing)
- Shareability: 8/10 (addresses question many people have about AI)
- **Weighted Score**: (8×0.25) + (8×0.20) + (9×0.20) + (7×0.15) + (7×0.10) + (8×0.10) = **8.05**

### Step 5: Analyze and Select the Winner

After scoring all five candidates:

1. **Calculate weighted scores** for each candidate
2. **Identify top 2-3 performers** based on quantitative scores
3. **Apply qualitative judgment** considering:
   - Best fit for article tone and audience
   - Authenticity to content
   - No red flags (deception, offense, plagiarism)
   - Overall "feel" when reading aloud

4. **Select the winning title** that:
   - Has the highest overall score OR
   - Scores highly and best represents the article's unique angle
   - Passes all ethical/quality checks

**Example selection rationale:**
"After evaluation, Candidate 2 ('Opaque AI in Healthcare: Why Explainability Matters Now') scores highest with 8.3/10. It combines strong clickability (the 'Opaque' descriptor is clear and evocative), excellent clarity about the core issue, and solid SEO with well-placed keywords. While Candidate 1 scored well on clarity and Candidate 5 had good structure, Candidate 2 provides the best balance across all criteria. It avoids AI-generated tropes like 'Black-Box' or 'Algorithm', uses fresh language, and authentically represents the article without relying on clichéd phrasing."

### Step 6: Replace the Title in the Article

Use the Edit tool to replace the article's current title and ensure that you:-
- Find and replace the first H1 heading in the markdown file
- Preserve all other content
- Confirm successful replacement

### Step 7: Present Results to User

Provide the user with:
1. **The winning title** and brief explanation of why it was chosen
2. **All five candidates** with their scores (optional but recommended for transparency)
3. **Confirmation** that the title has been replaced in the file
4. **Key insights** from the evaluation (what made the winner stand out)

**Example output format:**

```
✓ Article title optimized successfully!

Winning Title (Score: 8.3/10):
"Opaque AI in Healthcare: Why Explainability Matters Now"

Why this title won:
- Highest overall score across all criteria
- Fresh "Opaque" descriptor avoids overused "Black-Box" trope
- Clear communication of article scope (AI + healthcare + transparency)
- Strong SEO with well-placed keywords
- Excellent balance of curiosity and clarity
- Avoids AI-generated tropes and clichéd phrasing

All candidates evaluated:
1. "Medical AI and Trust: Why Bias Threatens Healthcare Equity" (8.0/10)
2. "Opaque AI in Healthcare: Why Explainability Matters Now" (8.3/10) ← WINNER
3. "AI Will Not Replace Radiologists: But Everything Changes" (7.6/10)
4. "When Medical AI Fails Minorities: The Data Representation Crisis" (7.9/10)
5. "Navigating Healthcare AI: Trust, Bias, and the Path Forward" (7.7/10)

The title has been updated in: /path/to/article.md
```

## Key Principles

### Accuracy Over Attraction
While the goal is creating marketable titles, accuracy is non-negotiable:
- Never misrepresent article content
- Avoid clickbait or deceptive techniques
- Ensure promises in title are delivered in content
- Be specific, not vague

### Format Compliance
All titles must follow `<Title>: <Subtitle>` structure with strict constraints:
- **Title (main)**: Hook the reader, create curiosity
- **Subtitle**: Clarify, provide context, set expectations
- **Total length**: 10-12 words maximum
- **Balance**: Neither part should dominate excessively

**Mandatory Constraints:**
1. **No AI-generated tropes**: Never use "Algorithm/Algorithmic/Algorithms", "Black-Box/Black Box", or clichéd AI-content phrasing like "The X Will See You Now", "Welcome to the Age of X", "The Rise of X", "X: A Game Changer"
2. **No apostrophes**: Avoid contractions and possessives (use "do not" instead of "don't", "AI of the future" instead of "AI's future")
3. **No question marks in Title segment**: Questions create awkward ?: visual combinations. Use questions only in Subtitle, or rephrase as statements

### Diverse Candidate Generation
Generate candidates using different formulas to ensure variety:
- Question format (question must be in Subtitle segment only, or use statement form)
- How-to format
- Problem-solution format
- Contrarian/provocative format
- Future/trend format
- Emotional hook format
- Unexpected juxtaposition

Avoid generating five variations of the same approach. Remember: all candidates must comply with the three mandatory constraints (no AI tropes, no apostrophes, no question marks in Title segment).

### Evidence-Based Selection
Base the winning title selection on:
- **Quantitative scores** across six weighted criteria
- **Qualitative judgment** about fit and authenticity
- **Ethical checks** for deception, offense, or plagiarism
- **Alignment** with article tone and target audience

Document the reasoning for transparency.

## Common Scenarios

### Scenario 1: Technical Article for Expert Audience
**User request**: "Optimize the title for this technical paper on neural network architectures"
**Approach**:
- Prioritize clarity and precision over clever wordplay
- Use correct technical terminology
- Emphasize novelty or practical benefit
- Example: "Transformer Attention Mechanisms: Scaling Efficiency in Large Models"

### Scenario 2: General Interest Article
**User request**: "Make this article about climate change more engaging"
**Approach**:
- Avoid jargon, use accessible language
- Emphasize human impact and relevance
- Create emotional connection
- Example: "Why Your City Will Flood: Climate Change Comes Home"

### Scenario 3: How-To Guide
**User request**: "Create a better title for this tutorial"
**Approach**:
- Use action-oriented language
- Make the benefit clear
- Be specific about what readers will learn
- Example: "Master API Testing: Build Robust Tests in 30 Minutes"

### Scenario 4: Opinion/Commentary
**User request**: "This opinion piece needs a stronger title"
**Approach**:
- Signal the viewpoint clearly
- Be provocative within reason
- Create discussion-worthy angle
- Example: "The Silicon Valley AI Ethics Problem: Why Self-Regulation Failed"

## Troubleshooting

### Issue: All Candidates Score Very Similarly
**Solution**: Revisit generation step and create more diverse candidates using different formulas. Ensure variety in approach (question vs. statement, provocative vs. informative, etc.)

### Issue: No Candidates Meet Quality Bar
**Solution**: Return to article analysis. May have misunderstood core thesis or audience. Re-read article sections and regenerate candidates based on deeper understanding.

### Issue: User Rejects Winning Title
**Solution**: Ask for specific feedback about what doesn't work. Use that input to either:
- Select the second-place candidate if it addresses concerns
- Generate new candidates with adjusted focus
- Revise winning title while maintaining structure

### Issue: Title Length Exceeds 12 Words
**Solution**: Edit for conciseness:
- Remove filler words (very, really, actually, etc.)
- Use more concise phrasing
- Combine or eliminate redundant concepts
- Ensure both title and subtitle are pulling weight

## Resources

### references/title_best_practices.md
Comprehensive guide containing:
- Proven title formulas with examples
- Detailed success criteria and evaluation framework
- Common pitfalls to avoid
- Industry-specific considerations
- Before/after transformation examples

**When to reference**: Always review this before generating candidates to ensure adherence to best practices and proper use of formulas.
