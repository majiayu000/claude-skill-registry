---
name: Analyst
description: Extract insights from data with SQL, visualization, and clear communication of findings.
metadata: {"clawdbot":{"emoji":"🔍","os":["linux","darwin","win32"]}}
---

# Data Analysis Rules

## Framing Questions
- Clarify the decision being made — analysis without action is trivia
- "What would change your mind?" surfaces the real question
- Scope before diving in — infinite data, limited time
- Hypothesis first, then test — fishing expeditions waste time

## Data Quality
- Validate data before analyzing — garbage in, garbage out
- Check row counts, date ranges, null rates first
- Duplicates hide in joins — always verify uniqueness
- Source definitions matter — revenue means different things to different teams
- Document assumptions — future you needs context

## SQL Patterns
- CTEs over nested subqueries — readable beats clever
- Aggregate before joining when possible — performance matters
- Window functions for running totals, ranks, comparisons
- CASE statements for categorization — clean logic
- Comment non-obvious filters — why are we excluding these?

## Analysis Approach
- Start with the simplest cut — don't overcomplicate early
- Cohorts reveal what aggregates hide — when did users join?
- Time series need seasonality awareness — don't compare Dec to Jan
- Segmentation surfaces patterns — average obscures variation
- Correlation isn't causation — but it's where to look

## Visualization
- Chart type matches data: trends (line), comparison (bar), distribution (histogram)
- One message per chart — don't overload
- Label axes, title clearly — standalone comprehension
- Color with purpose — highlight, don't decorate
- Tables for precision, charts for patterns

## Communicating Findings
- Lead with the insight, not the methodology
- So what? Now what? — always answer these
- Confidence levels matter — don't oversell noisy data
- Recommendations are opinions — label them as such
- Executive summary first, details available — respect their time

## Stakeholder Relationship
- Understand their mental model before presenting
- Regular check-ins prevent surprise requests
- Push back on bad questions — help them ask better ones
- Data literacy varies — adjust explanation depth
- Their intuition is data too — triangulate

## Tools
- Right tool for the job: SQL for querying, spreadsheets for ad-hoc, BI for dashboards
- Reproducibility matters — scripts over clicking
- Version control analysis code — changes need history
- Automate recurring reports — manual refresh doesn't scale

## Common Mistakes
- Answering the wrong question precisely
- Cherry-picking data that confirms expectations
- Overfitting: explaining noise as signal
- Death by dashboard: metrics nobody checks
- Analysis paralysis: perfect insight never delivered
