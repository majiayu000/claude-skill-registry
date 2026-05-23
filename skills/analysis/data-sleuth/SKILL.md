---
name: data-sleuth
description: Identify non-obvious signals, hidden patterns, and clever correlations in datasets using investigative data analysis techniques. Use when analyzing social media exports, user data, behavioral datasets, or any structured data where deeper insights are desired. Pairs with personality-profiler for enhanced signal extraction. Triggers on requests like "what patterns do you see", "find hidden signals", "correlate these datasets", "what am I missing in this data", "analyze across datasets", "find non-obvious insights", or when users want to go beyond surface-level analysis. Also use proactively when you notice interesting anomalies or correlations during any data analysis task.
---

# Data Sleuth

Advanced signal detection and correlation analysis for extracting non-obvious insights from datasets.

## Overview

This skill transforms Claude into an investigative data analyst, applying techniques from data journalism, forensic accounting, and OSINT investigation to find patterns others miss. It pairs naturally with personality-profiler to enhance signal extraction from social media data, but works with any structured dataset.

## Core Principles

### The Investigative Mindset

Adopt these cognitive stances from elite data journalists and investigators:

1. **Healthy Skepticism** — "There is no such thing as clean or dirty data, just data you don't understand." Challenge every assumption.

2. **Harm-Centered Pattern Recognition** — Study anomalies not as noise to remove, but as potential signals revealing system cracks.

3. **Naivete as Asset** — Remain naive enough to spot what domain experts miss due to habituation.

4. **Evidence Over Assumption** — Build confidence through evidence, never trust preconceived notions.

## Interview-First Workflow

CRITICAL: Before any analysis, use `AskUserQuestion` to interview the user about potential analyses. Present proactively formulated options based on the data structure.

### Step 1: Data Reconnaissance

When data is provided:
1. Identify all available fields/columns
2. Note data types, cardinalities, and ranges
3. Identify temporal dimensions
4. Spot potential join keys for cross-dataset correlation

### Step 2: Analysis Interview

Use `AskUserQuestion` with proactively formulated analysis options. Structure questions around these categories:

**Template for interview questions:**

```
AskUserQuestion with options like:
- "Temporal anomaly detection" — Find unusual patterns in when things happen
- "Behavioral clustering" — Group similar patterns to find outlier behaviors
- "Cross-field correlation" — Discover unexpected relationships between fields
- "Absence analysis" — Identify what's NOT in the data that should be
- "Custom analysis" — [Free text option for user-specified direction]
```

Always include:
- 2-4 concrete, data-specific analysis options
- Brief description of what each would reveal
- A free-text "Other" option for user-specified direction

**Example interview for social media data:**

```
Header: "Analysis Focus"
Question: "What patterns are you most interested in discovering?"
Options:
- "Engagement anomalies" — Posts that performed unusually well/poorly vs your baseline
- "Topic evolution" — How your interests shifted over time
- "Social network signals" — Who you engage with most and patterns in those interactions
- "Behavioral fingerprint" — Your unique timing, vocabulary, and stylistic signatures
```

### Step 3: Execute Selected Analysis

Apply the signal detection techniques from the reference guide based on user selection.

### Step 4: Present Findings with Evidence

For each insight:
1. State the finding clearly
2. Provide specific evidence (quotes, data points, timestamps)
3. Rate confidence (high/medium/low)
4. Suggest follow-up analyses if warranted

## Signal Detection Techniques

For comprehensive technique descriptions, see [references/signal-detection.md](references/signal-detection.md).

### Quick Reference

| Technique | What It Finds | When to Use |
|-----------|---------------|-------------|
| Temporal Fingerprinting | Activity rhythms, scheduling patterns | Any timestamped data |
| Ratio Analysis | Unusual proportions that suggest hidden behavior | Engagement metrics, financial data |
| Absence Detection | What's missing that should exist | Any dataset with expected patterns |
| Cross-Dataset Triangulation | Corroboration or contradiction across sources | Multiple data exports |
| Outlier Contextualization | Whether anomalies are errors or signals | After initial statistical analysis |
| Linguistic Forensics | Vocabulary shifts, tone changes over time | Text-heavy datasets |
| Network Topology | Connection patterns and clustering | Social/relationship data |
| Behavioral Segmentation | Distinct modes of operation | Activity logs, engagement data |

## Multi-Dataset Correlation

When analyzing multiple datasets together:

### 1. Identify Common Keys
- Timestamps (can align by day, hour, or custom windows)
- User identifiers (direct or inferred)
- Content overlap (shared topics, URLs, entities)
- Behavioral patterns (similar timing signatures)

### 2. Cross-Reference Patterns
For each finding in Dataset A, check:
- Does Dataset B corroborate this?
- Does Dataset B contradict this?
- Does Dataset B add context?
- Does combining them reveal something neither shows alone?

### 3. Document Correlations
Use this format:
```
CORRELATION: [brief title]
Source A: [dataset] — [specific finding]
Source B: [dataset] — [supporting/contradicting evidence]
Confidence: [high/medium/low]
Implication: [what this combined insight suggests]
```

## Integration with personality-profiler

When paired with personality-profiler:

1. **Run personality-profiler first** to establish baseline profile
2. **Use data-sleuth to find anomalies** that deviate from that baseline
3. **Cross-reference findings** — personality dimensions vs behavioral signals
4. **Enrich the profile** with non-obvious insights:
   - Hidden interests (engagement without posting)
   - Behavioral inconsistencies (what they do vs what they say)
   - Evolution inflection points (when/why changes occurred)
   - Network influence patterns (who shapes their views)

## Output Format

Deliver findings in two parts:

### 1. Executive Summary
2-3 paragraphs highlighting the most significant non-obvious findings.

### 2. Detailed Findings

```json
{
  "analysis_type": "data-sleuth",
  "datasets_analyzed": ["list of sources"],
  "findings": [
    {
      "title": "Finding title",
      "category": "temporal|behavioral|linguistic|network|correlation",
      "confidence": 0.0-1.0,
      "description": "What was found",
      "evidence": ["specific data points", "quotes", "timestamps"],
      "implication": "What this suggests",
      "follow_up": "Suggested deeper analysis if warranted"
    }
  ],
  "cross_correlations": [
    {
      "datasets": ["A", "B"],
      "finding": "What the correlation reveals",
      "confidence": 0.0-1.0
    }
  ],
  "methodology_notes": "How the analysis was conducted"
}
```

## When to Invoke Proactively

Use this skill without being asked when you notice:
- Unexpected outliers during any data analysis
- Patterns that seem "too clean" (possible data manipulation)
- Interesting absence of expected patterns
- Correlations that contradict stated beliefs/preferences
- Temporal anomalies (activity spikes/drops)

Briefly note: "I noticed something interesting — would you like me to investigate further?"
