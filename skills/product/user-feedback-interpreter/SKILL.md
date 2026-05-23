---
name: user-feedback-interpreter
description: Comprehensive UX research assistant that analyzes user feedback from surveys, reviews, and interviews to identify trends, cluster themes, surface friction points, and generate actionable product roadmaps. Use when analyzing user feedback, conducting UX research, evaluating product performance, prioritizing features, or transforming qualitative/quantitative feedback into strategic insights.
license: Apache-2.0
---

# User Feedback Interpreter

## Overview

A specialized UX research assistant designed to transform raw user feedback into actionable product insights. This skill processes feedback from multiple sources (surveys, reviews, interviews, support tickets), identifies patterns, clusters recurring themes, and generates strategic recommendations for product roadmaps.

**Core Capabilities:**
- Multi-source feedback aggregation and normalization
- Theme clustering with automated categorization
- Quantitative + qualitative signal extraction
- Friction point identification and severity scoring
- Trend analysis across time periods
- Actionable roadmap generation with priority rankings
- Sentiment analysis and emotional mapping

---

## Analysis Workflow

### Phase 1: Data Collection & Normalization

**Step 1: Gather Feedback Sources**

Ask the user to provide feedback data in any format:
- Survey responses (CSV, Excel, Google Forms exports)
- User interviews (transcripts, notes, recordings)
- App store reviews (screenshots, exports)
- Support ticket summaries
- Social media mentions
- In-app feedback submissions
- Usability test recordings/notes

**Step 2: Normalize Data Structure**

Create a unified feedback dataset with these fields:
```
- feedback_id: Unique identifier
- source: Origin (survey/review/interview/support/etc)
- date: When feedback was submitted
- user_segment: Type of user (new/power/churned/trial/etc)
- feedback_text: Raw feedback content
- rating: Numerical score if available (NPS, CSAT, stars)
- category: Initial categorization (if provided)
- metadata: Additional context (user_id, product version, platform)
```

**Step 3: Data Quality Check**

- Remove duplicates based on content similarity (>90% match)
- Flag incomplete responses
- Identify and separate actionable vs non-actionable feedback
- Note response rates and potential sampling bias

---

### Phase 2: Theme Clustering & Categorization

**Automated Theme Identification**

Analyze feedback to identify recurring themes using:

1. **Keyword Frequency Analysis**
   - Extract most mentioned terms/phrases
   - Group semantically similar terms
   - Calculate mention frequency by source type

2. **Topic Clustering**
   - Group feedback by semantic similarity
   - Identify 5-12 major themes
   - Name each theme descriptively

3. **Category Assignment**

Use this hierarchical taxonomy (see `references/THEME_TAXONOMY.md` for complete reference):

**Primary Categories:**
- **Usability**: Navigation, clarity, ease-of-use issues
- **Features**: Requests, missing functionality, enhancements
- **Performance**: Speed, reliability, bugs, crashes
- **Pricing**: Cost concerns, value perception, billing
- **Support**: Customer service, documentation, help resources
- **Onboarding**: First-time experience, learning curve, setup
- **Integration**: Third-party tools, API, import/export
- **Design**: Visual appearance, UI/UX, aesthetics
- **Security/Privacy**: Data concerns, compliance, permissions

**Secondary Tags:**
- Sentiment: Positive / Neutral / Negative / Critical
- Urgency: Low / Medium / High / Critical
- User Type: New / Experienced / Power / Churned
- Complexity: Simple fix / Medium effort / Major overhaul

---

### Phase 3: Quantitative Analysis

**Calculate Key Metrics:**

1. **Volume Metrics**
   - Total feedback items analyzed
   - Breakdown by source type
   - Items per time period
   - Response rates (if survey data)

2. **Theme Distribution**
   ```
   Theme                    | Count | % of Total | Avg Sentiment
   -------------------------|-------|------------|---------------
   Feature Request: Export  |   127 |      18%   |    Neutral
   Bug: Mobile Crashes      |    89 |      13%   |    Negative
   Pricing: Too Expensive   |    76 |      11%   |    Negative
   ```

3. **Sentiment Breakdown**
   - Overall sentiment distribution
   - Sentiment by theme
   - Sentiment trends over time

4. **Severity Scoring**

   For each theme, calculate severity:
   ```
   Severity = (Frequency × 0.4) + (Negative_Sentiment × 0.3) + (User_Impact × 0.3)
   
   Where:
   - Frequency: % of total feedback mentioning this theme
   - Negative_Sentiment: % of negative mentions for this theme
   - User_Impact: Estimated business impact (scale 1-10)
   ```

5. **Trend Analysis**
   - Compare current period vs previous period
   - Identify growing vs declining themes
   - Track sentiment trajectory

---

### Phase 4: Qualitative Analysis

**Extract Deeper Insights:**

1. **Representative Quotes**

   For each major theme, select 3-5 quotes that:
   - Illustrate the issue clearly
   - Show different user perspectives
   - Highlight severity/emotion
   - Include positive examples (if available)

2. **User Journey Mapping**

   Identify friction points at each stage:
   ```
   Discovery → Signup → Onboarding → First Use → Regular Use → Advanced Features
      ↓          ↓          ↓            ↓            ↓                ↓
   [friction] [friction] [friction]  [friction]   [friction]      [friction]
   ```

3. **Pain Point Prioritization**

   Rank friction points by:
   - Frequency of mention
   - Severity of impact
   - Stage in user journey
   - Ease of fix (estimated)

4. **Feature Request Analysis**

   For each request, determine:
   - Underlying user need (the "why")
   - Workarounds users are currently using
   - Similar requests across different sources
   - Potential solutions beyond the specific request

---

### Phase 5: Actionable Roadmap Generation

**Output Format: Strategic Recommendations**

Generate a structured report with:

#### Executive Summary (2-3 paragraphs)
- Overall feedback sentiment and trends
- Top 3-5 critical issues requiring immediate attention
- Key opportunities for product improvement
- Comparison to previous period (if available)

#### Critical Issues (Immediate Action Required)

For each critical issue:
```
Issue: [Clear problem statement]
Impact: [Business/user impact description]
Evidence: 
  - Mentioned by X% of users
  - Negative sentiment: Y%
  - Severity score: Z/10
Representative Quotes: [2-3 quotes]
Recommended Action: [Specific next steps]
Success Metrics: [How to measure if fixed]
```

#### High-Priority Improvements (Next Quarter)

List of 5-10 improvements with:
- Theme name
- Frequency (% of feedback)
- User segments affected
- Estimated effort (T-shirt sizing: S/M/L/XL)
- Expected impact (Low/Medium/High/Very High)

#### Feature Requests Roadmap

Organize requests into categories:

**Quick Wins** (High impact, low effort):
- [Feature 1]: Mentioned by X users, affects [segment]
- [Feature 2]: Workaround currently: [description]

**Strategic Bets** (High impact, high effort):
- [Feature A]: Major opportunity, requires [resources]
- [Feature B]: Differentiator, affects [segment]

**Consider Later** (Lower priority):
- [Feature X]: Niche request, affects [small segment]

#### Trends & Patterns

- Emerging themes (growing mentions)
- Declining issues (improving areas)
- Seasonal patterns (if applicable)
- Segment-specific insights

#### Recommended Next Steps

1. **Immediate Actions** (this week)
   - Critical bugs to fix
   - Users to follow up with
   - Urgent communications needed

2. **Short-term** (this month)
   - Features to validate through prototypes
   - Additional research needed
   - Quick improvements to implement

3. **Long-term** (this quarter)
   - Strategic initiatives to plan
   - Resources required
   - Success metrics to track

---

## Sentiment Analysis

**Methodology:**

Use `scripts/sentiment_analyzer.py` for automated sentiment scoring, or manually classify using:

**Sentiment Categories:**
- **Very Positive** (9-10/10): Praise, love, exceptional satisfaction
- **Positive** (7-8/10): Satisfaction, appreciation, recommendations
- **Neutral** (5-6/10): Factual statements, neither positive nor negative
- **Negative** (3-4/10): Frustration, disappointment, complaints
- **Very Negative** (1-2/10): Anger, threats to churn, severe criticism

**Key Indicators:**

*Positive:* "love," "amazing," "exactly what I needed," "game-changer," "highly recommend"

*Negative:* "frustrating," "confusing," "disappointed," "waste of time," "considering alternatives," "canceling"

*Critical:* "unusable," "broken," "scam," "worst," "never again"

**Emotional Mapping:**

Beyond positive/negative, identify emotional states:
- Frustrated (can't accomplish task)
- Confused (unclear how to proceed)
- Delighted (exceeded expectations)
- Anxious (worried about security/data)
- Impatient (wants features now)

---

## Report Templates

Use `assets/feedback_report_template.md` as a starting point for final deliverables.

For different stakeholders, adjust focus:

**For Product Managers:**
- Feature requests with business impact
- User journey friction points
- Competitive comparison insights
- ROI estimation for fixes

**For Engineering:**
- Bug severity and frequency
- Performance issues with details
- Technical debt mentions
- Integration/API feedback

**For Design:**
- Usability issues with context
- Visual/aesthetic feedback
- User flow problems
- Accessibility mentions

**For Leadership:**
- Executive summary only
- Top 3 critical issues
- Strategic opportunities
- Trend comparisons

---

## Best Practices

**DO:**
- ✅ Combine quantitative data (metrics) with qualitative insights (quotes)
- ✅ Look for patterns across different feedback sources
- ✅ Identify the underlying need, not just the stated request
- ✅ Consider user segment differences (new vs power users)
- ✅ Acknowledge positive feedback and wins
- ✅ Provide specific, actionable recommendations
- ✅ Include confidence levels for interpretations
- ✅ Note limitations of the data (sample size, bias)

**DON'T:**
- ❌ Cherry-pick feedback to support predetermined conclusions
- ❌ Over-generalize from small sample sizes
- ❌ Ignore negative feedback
- ❌ Make assumptions without supporting evidence
- ❌ Present recommendations without priority/effort context
- ❌ Confuse correlation with causation
- ❌ Forget to validate findings with stakeholders

---

## Advanced Analysis Techniques

### Cohort Analysis

If timestamps and user IDs available, analyze feedback by cohorts:
- Users who joined in same time period
- Users with similar usage patterns
- Users from same acquisition channel
- Users with similar demographics

Compare feedback patterns across cohorts to identify:
- Onboarding issues affecting new users
- Power user needs
- Churn risk signals

### Competitive Insights

When feedback mentions competitors:
- List alternative products mentioned
- Note reasons users compare/consider switching
- Identify perceived advantages of competitors
- Find unique value propositions

### Time-series Analysis

Track themes over time to:
- Measure impact of product changes
- Identify seasonal patterns
- Spot emerging issues early
- Validate that fixes resolved issues

For detailed methodology, see `references/ANALYSIS_METHODS.md`

---

## Integration with MCP Tools

This skill works seamlessly with external data sources:

**Google Drive MCP:**
- Read survey exports from Google Sheets
- Access interview transcripts from Docs
- Pull historical feedback archives

**Slack MCP:**
- Analyze user feedback from support channels
- Review beta tester discussions
- Monitor community sentiment

**GitHub/Jira MCP:**
- Cross-reference feedback with bug reports
- Track feature request status
- Link customer quotes to issues

---

## Output Deliverables

Depending on user needs, generate:

1. **Executive Dashboard** (1 page)
   - Key metrics, top issues, recommended actions

2. **Detailed Analysis Report** (5-15 pages)
   - Complete findings with evidence and recommendations

3. **Theme Breakdown Spreadsheet**
   - All feedback items categorized and scored

4. **Presentation Slides**
   - Visual summary for stakeholder meetings

5. **Action Plan**
   - Prioritized list of next steps with owners

6. **Research Questions**
   - Follow-up questions for deeper investigation

---

## Quality Assurance

Before finalizing analysis:

- [ ] All feedback items reviewed and categorized
- [ ] Metrics calculated correctly
- [ ] Representative quotes selected for each theme
- [ ] Recommendations are specific and actionable
- [ ] Priority rankings justified with evidence
- [ ] Report tailored to intended audience
- [ ] Data limitations acknowledged
- [ ] Positive feedback highlighted
- [ ] Next steps clearly defined

---

## Resources

- **Detailed Methodologies**: `references/ANALYSIS_METHODS.md`
- **Complete Theme Taxonomy**: `references/THEME_TAXONOMY.md`
- **Report Templates**: `references/REPORT_TEMPLATES.md`
- **Sentiment Analysis Script**: `scripts/sentiment_analyzer.py`
- **Sample Data Structure**: `assets/feedback_template.csv`

---

## Example Usage

**User:** "I have 500 survey responses from our recent NPS campaign and 50 app store reviews. Can you analyze them and create a roadmap?"

**Claude:** "I'll analyze your feedback data comprehensively. Let me start by:

1. Reviewing the survey responses and app store reviews
2. Normalizing the data into a unified structure
3. Identifying recurring themes and patterns
4. Calculating key metrics and sentiment scores
5. Generating actionable recommendations

Please share the survey data and reviews, and let me know:
- What time period does this cover?
- Are there specific areas you want me to focus on?
- Who is the primary audience for this analysis?

Let's transform this feedback into strategic insights!"

---

## Notes

- This skill processes feedback objectively while highlighting both positive and negative signals
- Analysis quality depends on feedback volume and diversity - flag small sample sizes
- Always validate findings with product context and business objectives
- Consider running follow-up research for ambiguous or conflicting signals
- Update theme taxonomy based on your product domain and user base
