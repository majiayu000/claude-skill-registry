---
name: stakeholder-management-expert
description: Public and Indigenous consultation, stakeholder feedback analysis, response strategy. Categorizes themes, performs sentiment analysis (support/opposition/neutral), generates prioritized response strategies, tracks commitments. Use for public meetings, consultation summaries, community engagement
tags: [stakeholder-engagement, public-consultation, sentiment-analysis, community-feedback, response-strategy, commitments-tracking]
capability: Provides systematic stakeholder feedback analysis including theme categorization, sentiment analysis, frequency weighting, response strategy generation by priority level, and commitments tracking matrix for infrastructure consultation processes
proactive: true
---

You are an expert in stakeholder consultation analysis, feedback summarization, sentiment analysis, and response strategy development for infrastructure and real estate projects.

# Stakeholder Management Expert Skill

Expert in stakeholder consultation analysis, feedback summarization, sentiment analysis, and response strategy development for infrastructure and real estate projects.

## When to Use This Skill

Use this skill when you need to:

- **Summarize stakeholder feedback** from public meetings, open houses, or consultations
- **Analyze sentiment** (support, opposition, neutral, mixed) across comments
- **Categorize themes** and identify key concerns from unstructured feedback
- **Generate response strategies** for addressing stakeholder concerns
- **Track commitments** made during consultation processes
- **Prepare briefing notes** for senior management on consultation outcomes
- **Develop communication plans** for stakeholder engagement

## Key Capabilities

### 1. Feedback Analysis
- Theme categorization using keyword matching
- Frequency weighting to identify top concerns
- Sentiment analysis (support/opposition/neutral/mixed)
- Multi-category comment identification
- Question vs. statement classification

### 2. Strategic Response
- Response strategy generation by priority
- Tactical recommendations for each theme
- Commitment extraction and tracking
- Risk identification and mitigation

### 3. Reporting
- Executive summaries for decision-makers
- Detailed theme breakdowns with sample quotes
- Sentiment analysis visualization
- Commitments tracking matrix
- Response strategy recommendations

## Tools Available

### Consultation Summarizer (`consultation_summarizer.py`)

Analyzes stakeholder feedback and generates comprehensive summary with response strategy.

**Purpose:** Summarize public meeting feedback and develop response strategy

**Input:** JSON file with meeting info, comments, and theme categories

**Output:** Markdown or JSON report with:
1. Meeting attendance and demographics
2. Key themes and concerns (categorized, frequency-weighted)
3. Sentiment analysis (support, opposition, neutral)
4. Response strategy recommendations
5. Commitments tracking matrix

**Usage:**
```bash
# Basic usage (auto-generates output in Reports/)
python consultation_summarizer.py samples/sample_1_station_public_meeting.json

# Specify output file
python consultation_summarizer.py input.json --output report.md

# JSON output format
python consultation_summarizer.py input.json --format json --output results.json

# Verbose mode
python consultation_summarizer.py input.json --verbose
```

**Input Schema:** See `consultation_input_schema.json`

## Input Format

### Basic Structure
```json
{
  "meeting_info": {
    "meeting_date": "2025-10-15",
    "meeting_type": "public_meeting",
    "attendance": 85,
    "location": "Community Center, 123 Main Street",
    "project_name": "North Transit Station Project",
    "phase": "preliminary_design"
  },

  "comments": [
    "Concerned about traffic congestion during construction",
    "Property values will decline",
    "Support this project! We need better transit.",
    ...
  ],

  "theme_categories": {
    "Traffic": ["traffic", "congestion", "parking", "road"],
    "Property Values": ["property value", "assessment", "market"],
    "Noise": ["noise", "sound", "quiet", "loud"],
    ...
  },

  "priorities": {
    "Traffic": 1,
    "Property Values": 2,
    "Noise": 3
  }
}
```

### Theme Categories

Define categories and keyword patterns for classification:

```json
{
  "Traffic": ["traffic", "congestion", "parking", "road"],
  "Property Values": ["property value", "market", "taxes"],
  "Business Impact": ["business", "customer", "sales", "revenue"],
  "Safety": ["safety", "crime", "security", "emergency"],
  "Accessibility": ["access", "wheelchair", "bike", "pedestrian"],
  "Environmental": ["dust", "air quality", "pollution", "trees"],
  "Compensation": ["compensation", "damages", "payment"],
  "Communication": ["information", "notice", "update"]
}
```

### Priorities

Assign priority levels (1=highest, 5=lowest) for response strategy:

```json
{
  "Traffic": 1,
  "Construction Impact": 1,
  "Business Impact": 2,
  "Property Values": 2,
  "Noise": 3,
  "Accessibility": 3
}
```

### Optional Demographics
```json
{
  "demographics": {
    "residents": 52,
    "business_owners": 18,
    "property_owners": 10,
    "elected_officials": 2,
    "advocacy_groups": 3
  }
}
```

### Output Options
```json
{
  "output_options": {
    "include_quotes": true,
    "max_quotes_per_sentiment": 5,
    "include_commitments": true,
    "output_format": "markdown"
  }
}
```

## Output Format

### Markdown Report Structure

```markdown
# Stakeholder Consultation Summary

## North Transit Station Project

**Meeting Type:** Public Meeting
**Meeting Date:** 2025-10-15
**Location:** Community Center, 123 Main Street
**Project Phase:** Preliminary Design

## Attendance

**Total Attendance:** 85 people

### Demographic Breakdown
- Residents: 52 (61.2%)
- Business Owners: 18 (21.2%)
- Property Owners: 10 (11.8%)
...

## Overview Statistics

**Total Comments Received:** 85
**Categorized Comments:** 82 (96.5%)
**Themes Identified:** 10

### Sentiment Overview
**Overall Sentiment:** Moderate Opposition

- Support: 15
- Opposition: 42
- Neutral: 18
- Mixed: 10

## Key Themes and Concerns

| Rank | Theme | Comments | Percentage |
|------|-------|----------|------------|
| 1 | Traffic | 28 | 32.9% |
| 2 | Construction Impact | 22 | 25.9% |
| 3 | Business Impact | 15 | 17.6% |
...

### Top 3 Themes (Detailed)

#### Traffic (28 comments)
- "Very concerned about traffic congestion during construction..."
- "Traffic on Oak Avenue is already terrible..."
- "Traffic study is incomplete..."

## Response Strategy Recommendations

### High Priority

#### Traffic (28 comments)
**Strategy:** Prepare detailed traffic management plan and commit to mitigation measures

**Tactics:**
- Present traffic study with before/after analysis
- Commit to construction traffic routing away from residential streets
- Provide timeline for peak construction activities
- Establish complaint hotline for traffic issues

## Commitments Tracking Matrix

| Theme | Commitment | Responsible | Deadline | Status |
|-------|-----------|-------------|----------|--------|
| Traffic | No construction traffic on Main St | Project Team | Before construction | Pending |
...

## Recommended Next Steps
1. Circulate Summary
2. Implement High Priority Responses
3. Track Commitments
4. Follow-up Communication
5. Schedule Next Consultation
```

## Shared Utilities Used

This skill uses the following shared utility functions:

### From `Shared_Utils/stakeholder_utils.py`:
- `categorize_themes()` - Categorize feedback into themes
- `sentiment_analysis()` - Analyze sentiment (support/opposition/neutral)
- `frequency_weighting()` - Weight themes by frequency
- `generate_response_strategy()` - Generate response strategies
- `commitments_matrix()` - Extract and track commitments
- `extract_key_quotes()` - Extract representative quotes

### From `Shared_Utils/report_utils.py`:
- `format_markdown_table()` - Format data as markdown tables
- `eastern_timestamp()` - Generate Eastern Time timestamps

## Module Structure

```
stakeholder-management-expert/
├── SKILL.md                              # This file
├── consultation_summarizer.py            # Main calculator
├── consultation_input_schema.json        # JSON Schema validation
├── modules/
│   ├── validators.py                     # Input validation
│   ├── nlp_processing.py                 # Natural language processing
│   └── output_formatters.py              # Report formatting
└── samples/
    └── sample_1_station_public_meeting.json  # Sample input
```

## Examples

### Example 1: Transit Station Public Meeting

**Scenario:** Transit authority holds public meeting for new station. 85 attendees provide feedback.

**Input:**
```json
{
  "meeting_info": {
    "meeting_date": "2025-10-15",
    "attendance": 85,
    "project_name": "North Transit Station Project"
  },
  "comments": [
    "Concerned about traffic congestion during construction",
    "Support this project! We need better transit.",
    ...
  ],
  "theme_categories": {
    "Traffic": ["traffic", "congestion", "parking"],
    "Property Values": ["property value", "market"],
    ...
  }
}
```

**Analysis Results:**
- **Overall Sentiment:** Moderate Opposition
- **Top Theme:** Traffic (32.9% of comments)
- **Support vs. Opposition:** 15 support, 42 opposition
- **Response Strategies:** 10 strategies generated (prioritized)
- **Commitments Tracked:** 8 commitments identified

### Example 2: Infrastructure Project Workshop

**Scenario:** Highway expansion project holds workshop. Focus on business impacts.

**Key Findings:**
- Business Impact is top concern (45% of comments)
- Strong opposition (60% opposition, 20% support)
- Compensation questions dominate
- High priority response: Business liaison program

## Key Terms and Concepts

### Sentiment Categories
- **Support:** Positive sentiment toward project
- **Opposition:** Negative sentiment, concerns, objections
- **Neutral:** Questions, requests for information
- **Mixed:** Both positive and negative elements

### Priority Levels (1-5)
- **1 (Critical):** Immediate response required, high impact
- **2 (High):** Important concerns, significant stakeholder impact
- **3 (Medium):** Standard concerns, moderate impact
- **4 (Low):** Minor concerns, limited impact
- **5 (Very Low):** Informational, minimal response needed

### Response Strategy Components
- **Strategy:** High-level approach to addressing concern
- **Tactics:** Specific actions to implement strategy
- **Priority:** Urgency and importance level
- **Responsible Party:** Who will implement response

## Best Practices

### Theme Category Design
1. **Use clear, distinct categories** - Avoid overlap between themes
2. **Include comprehensive keywords** - Cover synonyms and variations
3. **Limit to 10-15 themes** - Too many dilutes analysis
4. **Test and refine** - Iterate based on uncategorized comments

### Priority Assignment
1. **Consider impact** - Frequency + severity
2. **Assess urgency** - Timeline constraints
3. **Evaluate resources** - Feasibility of response
4. **Align with project goals** - Strategic importance

### Commitment Tracking
1. **Document all commitments** - Even informal ones
2. **Assign responsibility** - Clear ownership
3. **Set deadlines** - Realistic timelines
4. **Track status** - Regular updates
5. **Communicate fulfillment** - Close the loop with stakeholders

### Response Strategy
1. **Acknowledge concerns** - Validate stakeholder input
2. **Provide factual information** - Counter misinformation
3. **Commit to specific actions** - Concrete steps
4. **Establish feedback mechanisms** - Ongoing communication
5. **Follow through** - Deliver on commitments

## Integration with Other Skills

This skill works well with:

- **Transit Station Site Acquisition Strategy** - Stakeholder feedback informs site selection
- **Expropriation Timeline Expert** - Consultation requirements and timelines
- **Briefing Note Expert** - Convert consultation summary to executive briefing
- **Agricultural Easement Negotiation** - Stakeholder concerns in rural areas

## Limitations

- **Keyword-based categorization** - May miss nuanced comments not matching keywords
- **Simple sentiment analysis** - No deep learning or context understanding
- **Manual priority assignment** - Requires human judgment for priorities
- **English language only** - No support for multilingual feedback
- **Text-only input** - Cannot analyze verbal feedback or body language

## Future Enhancements

Potential improvements:
1. Machine learning-based theme classification
2. Advanced sentiment analysis using NLP models
3. Automatic priority assignment based on impact assessment
4. Multilingual support
5. Integration with survey platforms
6. Trend analysis across multiple consultations
7. Stakeholder segmentation analysis
8. Geographic clustering of concerns

## References

- Ontario Environmental Assessment Act - Public Consultation Requirements
- IAP2 Public Participation Spectrum
- Best Practices in Stakeholder Engagement (Infrastructure Ontario)
- Transit Project Assessment Process (Metrolinx)

---

**Last Updated:** 2025-11-17

**Version:** 1.0

**Author:** Reggie Chan, CFA, FRICS - VP Leasing & Asset Management
