---
name: research
description: Gather external context on a topic. Use when you need industry trends, best practices, evidence base, and recent developments before analysis.
context: fork
agent: analysis-researcher
allowed-tools: [Read, WebFetch, WebSearch]
---

# Research

Gather external context on the following topic. **Prioritize the most recent information available.** Start with the current year, then work backward only as needed.

## Persona

If a persona or role is specified, such as "as a financial analyst", adopt that expertise lens:
- Prioritize sources that persona would trust
- Focus on metrics and frameworks that persona uses
- Surface information that persona would consider essential
- Use terminology natural to that domain

## Focus

- Industry trends and where things are heading
- Best practices and common approaches
- Counter examples and failures worth learning from
- Recent developments: prioritize current year sources, then last 12 months. Older material only if foundational.
- Credible sources: prefer primary sources, industry reports, and established publications over blog posts and aggregators
- **Comparative analysis**: When multiple approaches or solutions exist, compare them directly. Do not present options in isolation.

Do not evaluate or recommend yet. The goal is to build a foundation of evidence and context for later analysis.

Be thorough but concise. Flag where evidence is thin or conflicting.

## Source Resilience

When a WebFetch returns a 403 or 404, you **must** take action before moving on:
1. Log the failed source in the "Sources Attempted But Inaccessible" section so the user can see what was lost
2. **Immediately run a new WebSearch** to find a different source covering the same topic. Do not skip this step. The goal is to replace the lost information, not just document the gap.
3. In the Evidence Quality Assessment, explicitly note if high quality sources were disproportionately inaccessible and how this may skew findings
4. If more than half of attempted sources fail, flag the research as potentially incomplete and recommend the user manually review the inaccessible sources listed

## Required Output Format

Structure all research output using this template:

### Key Findings
Numbered list of the most important discoveries, each with a source citation.

### Evidence Quality Assessment
Rate the overall evidence base: Strong, Moderate, or Thin. Note any areas where evidence is conflicting or where source accessibility issues may have skewed findings.

### Sources Consulted
List all sources used, with titles and URLs. Each finding above should trace back to a source listed here.

### Sources Attempted But Inaccessible
List any sources that returned errors or were behind paywalls. Note what topic each was expected to cover.

### Gaps
What important questions could not be answered with available evidence? What areas need deeper investigation?

---

Every factual claim must cite its source. Use inline citations linking to the Sources Consulted list, such as "according to [Source Name]" or a numbered reference.

Topic: $ARGUMENTS
