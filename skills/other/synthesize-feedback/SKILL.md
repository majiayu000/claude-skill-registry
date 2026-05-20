---
name: synthesize-feedback
description: Synthesize customer feedback into thematic clusters when the user asks to analyze feedback, review VoC data, or understand customer sentiment
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Write
argument-hint: "[feedback source or time period]"
read-only: false
destructive: false
idempotent: false
open-world: false
user-invocable: true
tags: feedback, synthesis, research
---

# Synthesize Feedback

## Overview

Perform Voice of Customer (VoC) analysis by clustering raw feedback into themes, quantifying frequency and sentiment, and separating signal from noise. Connects feedback patterns to product roadmap items.

## Workflow

1. **Read product context** — Scan `.chalk/docs/product/` for the product profile, existing PRDs, and roadmap docs. These anchor the analysis by providing the product's current priorities and known gaps.

2. **Gather feedback data** — Parse `$ARGUMENTS` to identify the feedback source and time period. If the user provides raw feedback inline, use that directly. If they reference files, read them. If no data is provided, ask the user to supply feedback data before proceeding.

3. **Clean and normalize** — For each feedback item, extract the core request or complaint. Strip duplicate phrasing, normalize terminology (e.g., "crash" and "app freezes" map to the same theme), and tag the source channel (support, NPS, review, social, interview).

4. **Cluster into themes** — Group feedback into 5-10 themes using affinity mapping. Each theme gets a label, a one-sentence description, and representative quotes. Avoid single-item themes unless the signal is strong (e.g., a security concern).

5. **Quantify each theme** — For each theme, calculate: mention count, percentage of total feedback, average sentiment (positive / neutral / negative), and trend direction (new, growing, stable, declining) if historical data is available.

6. **Separate signal from noise** — Flag themes that are: (a) high frequency + negative sentiment (urgent), (b) low frequency but high severity (monitor), (c) feature requests from power users vs. casual users (weight accordingly), (d) already addressed in the roadmap (acknowledge).

7. **Connect to roadmap** — Cross-reference themes against existing PRDs and roadmap items in `.chalk/docs/product/`. Mark themes as: addressed, partially addressed, unaddressed, or contradicting current direction.

8. **Determine the next file number** — Read filenames in `.chalk/docs/product/` to find the highest numbered file. Use `highest + 1`.

9. **Write the synthesis** — Save to `.chalk/docs/product/<n>_feedback_synthesis_<period>.md`.

10. **Confirm** — Share the file path and highlight the top 3 themes by urgency.

## Output

- **File**: `.chalk/docs/product/<n>_feedback_synthesis_<period>.md`
- **Format**: Markdown with a summary table of themes, detailed theme sections, and a roadmap alignment section
- **Key sections**: Executive Summary, Theme Table (theme / count / sentiment / trend), Theme Details (with quotes), Signal vs Noise Assessment, Roadmap Alignment, Recommended Actions

## Anti-patterns

- **Counting without context** — Raw frequency is misleading. Ten mentions from one angry user is not the same as ten mentions from ten different users. Always deduplicate by user.
- **Ignoring sentiment polarity** — A theme with 50 mentions that are mostly positive ("love the new search") is not the same as 50 negative mentions. Always report sentiment alongside frequency.
- **Treating all sources equally** — NPS detractors and churned-user exit interviews carry more weight than a casual app store review. Weight signals by source reliability and user commitment level.
- **Missing the silent majority** — Vocal users are not representative. Note when feedback comes from a small, self-selected group and flag the survivorship bias.
- **Synthesizing without connecting to action** — A synthesis that does not recommend what to do next is just a report. Every synthesis should end with prioritized recommendations.
