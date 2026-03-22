---
name: synthesize-research
description: Synthesize interview notes, feedback, and transcripts into themed research findings with JTBD statements when the user asks to analyze research, synthesize interviews, or make sense of qualitative data
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Write
argument-hint: "[path to research files or folder]"
read-only: false
destructive: false
idempotent: false
open-world: false
user-invocable: true
tags: research, synthesis, analysis
---

# Synthesize Research

## Overview

Perform thematic analysis across multiple qualitative research sources — interview notes, user feedback, support transcripts, survey responses — to produce a structured synthesis with verbatim quotes, themed clusters, JTBD statements, contradictions, and actionable recommendations. This skill turns messy qualitative data into a decision-ready document.

## Workflow

1. **Read product context** — Load `.chalk/docs/product/0_product_profile.md` and any existing JTBD canvases or prior research syntheses. These provide the lens for interpreting new data: existing personas, known jobs, and previously identified themes. If no context exists, note this and proceed without assumptions.

2. **Locate source files** — Parse `$ARGUMENTS` to identify the research inputs. These may be:
   - Direct file paths or glob patterns (e.g., `.chalk/docs/research/*.md`)
   - A folder to scan (e.g., `.chalk/docs/research/`)
   - A list of file names

   Read all source files. If fewer than 3 sources are provided, warn the user that synthesis from limited sources carries high bias risk. If no files are found, ask the user to provide paths.

3. **Extract verbatim quotes** — Read each source and pull out direct quotes from participants. For each quote, tag:
   - **Speaker**: identifier or pseudonym (e.g., "P3", "User-Sarah", source filename)
   - **Quote**: exact words, in quotation marks
   - **Context**: what question or topic prompted this statement
   - **Emotional intensity**: neutral, moderate, strong (based on language, emphasis, or interviewer notes)

4. **Cluster into themes** — Group quotes by emergent themes using affinity mapping logic:
   - Start with individual quotes as atomic units
   - Group quotes that describe the same underlying phenomenon
   - Name each theme with a descriptive phrase (not a single word)
   - A theme must have quotes from at least 2 different sources to be valid
   - Track theme frequency (how many sources mention it) and intensity (how strongly they express it)

5. **Write theme analysis** — For each theme, produce:
   - **Theme name**: descriptive phrase capturing the insight
   - **Summary**: 2-3 sentence description of what this theme means
   - **Frequency**: X of Y sources mentioned this
   - **Intensity**: low / moderate / high (based on emotional language, emphasis, urgency)
   - **Supporting quotes**: minimum 3 verbatim quotes with speaker tags
   - **Confidence level**: high (5+ sources, consistent), medium (3-4 sources or some inconsistency), low (2 sources or contradictory)

6. **Generate JTBD statements** — Derive Jobs-to-be-Done statements from the themes. Each JTBD follows the format:
   - **When** [situation/trigger], **I want to** [action/goal], **so I can** [desired outcome].
   - Link each JTBD back to the supporting theme(s)
   - Note whether this is a new job or validates/extends an existing one from prior product docs

7. **Flag contradictions** — Identify places where sources disagree or tell conflicting stories. For each contradiction:
   - State the conflicting positions
   - Cite the sources on each side
   - Hypothesize why the contradiction exists (different personas? different contexts? different stages of adoption?)
   - Recommend how to resolve it (more research, segmentation, A/B test)

8. **Generate recommendations** — Based on the themes and JTBD statements, produce three lists:
   - **Build**: opportunities with strong evidence (high frequency + high intensity)
   - **Stop**: things users don't value or actively dislike, supported by evidence
   - **Investigate**: areas where signal is interesting but insufficient for a decision

9. **Determine the next file number** — Read filenames in `.chalk/docs/product/` to find the highest numbered file. The next number is `highest + 1`.

10. **Write the file** — Save to `.chalk/docs/product/<n>_research_synthesis_<topic_slug>.md`.

11. **Confirm** — Tell the user the synthesis was created, share the file path, report the number of sources analyzed, themes identified, and highlight the top 2-3 findings and any critical contradictions.

## Synthesis Structure

```markdown
# Research Synthesis: <Topic>

Last updated: <YYYY-MM-DD> (Initial draft)

## Research Overview

- **Sources analyzed**: <N> files
- **Source list**: <numbered list with filenames and brief descriptions>
- **Themes identified**: <N>
- **JTBD statements generated**: <N>
- **Contradictions flagged**: <N>

## Themes

### Theme 1: <Descriptive Theme Name>

**Frequency**: X of Y sources | **Intensity**: low/moderate/high | **Confidence**: low/medium/high

<2-3 sentence summary of what this theme means and why it matters>

**Supporting Quotes**:
- "..." — P1 (source file)
- "..." — P3 (source file)
- "..." — P5 (source file)

---

### Theme 2: <Descriptive Theme Name>

...

## Jobs-to-be-Done

| # | JTBD Statement | Supporting Themes | New or Validated |
|---|----------------|-------------------|------------------|
| J1 | When [situation], I want to [goal], so I can [outcome] | Theme 1, Theme 3 | New |
| J2 | ... | ... | Validates existing |

## Contradictions

### Contradiction 1: <Short description>

- **Position A**: "<quote>" — P1, P4
- **Position B**: "<quote>" — P2, P6
- **Possible explanation**: ...
- **Resolution path**: ...

## Recommendations

### Build (Strong Evidence)
- <recommendation> — Supported by Themes X, Y (N sources, high intensity)

### Stop (Evidence Against)
- <recommendation> — Supported by Themes X (N sources)

### Investigate (Insufficient Signal)
- <recommendation> — Based on Theme X (low confidence, needs more data)
```

## Output

- **File**: `.chalk/docs/product/<n>_research_synthesis_<topic_slug>.md`
- **Format**: Plain markdown, no YAML frontmatter
- **First line**: `# Research Synthesis: <Topic>`
- **Second line**: `Last updated: <YYYY-MM-DD> (Initial draft)`

## Anti-patterns

- **Cherry-picking quotes** — Selecting only quotes that support your preferred narrative is the cardinal sin of research synthesis. Include quotes that challenge your assumptions. If 4 out of 5 people love a feature but 1 person described a critical failure, that failure quote must appear.
- **One-interview conclusions** — A single interview is an anecdote, not evidence. Themes require supporting quotes from at least 2 sources. If a finding comes from only one source, it goes in "Investigate", not "Build."
- **Ignoring contradictory evidence** — Contradictions are the most valuable part of a synthesis because they reveal segmentation, context-dependence, or flawed assumptions. Never sweep them under the rug. Every contradiction gets its own section.
- **Themes without supporting quotes** — A theme with no verbatim quotes is an opinion, not a finding. Every theme must have at least 3 supporting quotes. If you cannot find 3 quotes, it is not a theme — it is a hunch.
- **Paraphrasing instead of quoting** — Synthesis loses power when you summarize what people said instead of quoting their actual words. Verbatim quotes carry emotional weight and specificity that summaries destroy. Use direct quotes in quotation marks with speaker attribution.
- **Treating frequency as the only signal** — Something mentioned by every participant might be table stakes, not an opportunity. Intensity matters as much as frequency. One person describing a problem with visible frustration is stronger signal than five people casually mentioning a mild annoyance.
- **Recommendations without evidence links** — Every recommendation must trace back to specific themes and quotes. "We should build X" without citing evidence is product opinion disguised as research.
- **Synthesizing without reading all sources** — Skimming sources or reading only the first few guarantees a biased synthesis. Read every source document completely before starting to cluster themes.
