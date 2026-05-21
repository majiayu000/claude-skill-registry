---
name: deep-research
description: >
  Deep research with NotebookLM + web search. Iterative multi-source research
  with domain boost, source credibility, and post-research artifact generation
  (podcast, video, slides, quiz). Free alternative to Perplexity/Gemini Pro.
  Use when user says "/deep-research", "research this", "deep dive into",
  or "investigate".
user-invokable: true
argument-hint: '"topic" [--domain maritime|legal|academic] [--continue] [--compare "X vs Y"]'
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebSearch
  - WebFetch
  - Agent
  - AskUserQuestion
---

# Deep Research

Free Perplexity/Gemini-level deep research for any AI coding agent. Combines NotebookLM's Gemini-powered research engine with iterative web search, domain-aware routing, and post-research artifact generation.

## Activation

Triggered by `/deep-research "topic"` or intent detection ("research this", "deep dive into", "investigate").

### Argument Parsing

- `"topic"` — required, the research query
- `--domain maritime|legal|academic` — optional domain boost
- `--continue` — resume previous research session
- `--compare "X vs Y"` — structured comparison mode

If no arguments provided, ask: "What topic should I research?"

## Dependency Check

Before starting, determine available capabilities:

1. Try `notebooklm status` first. If command not found, try `python3 -m notebooklm status` or `python -m notebooklm status`. Use whichever works for all subsequent notebooklm commands.
   - If success: **Full mode** (NotebookLM + WebSearch)
   - If all fail: **Fallback mode** (WebSearch only)

2. If fallback mode, inform user:
   > "NotebookLM not detected. Running in web-search-only mode.
   > For full features (deep research, podcast, video, slides, quiz), install:
   > `pip install notebooklm-py && notebooklm login`"

3. Store mode for pipeline decisions.

## Pre-flight

Present this prompt and WAIT for user response before proceeding:

```
Research Topic: "{topic}"

Depth:
  1 = Quick (fast mode, 5-10 sources, ~1 min)
  2 = Moderate (fast + 1 WebSearch round, 10-15 sources)
  3 = Standard (deep mode, 20+ sources, ~3 min)  [default]
  4 = Deep (deep + 1 WebSearch round, 30+ sources)
  5 = Exhaustive (deep + 2 WebSearch rounds, 40+ sources)

Source focus:
  A = Everything (web + your notebooks)  [default]
  B = Academic only (papers, journals, research)
  C = News & current events (last 12 months)
  D = Technical docs & specs
  E = Custom (tell me what to focus on)

Enter choices (e.g. "3, A") or press Enter for defaults:
```

Parse response:
- Default if empty: depth=3, focus=A
- Extract depth (1-5) and focus (A-E)
- If focus=E, ask follow-up: "What should I focus on?"

## Pipeline — Full Mode (NotebookLM available)

### Step 1: Check existing notebooks

Run: `notebooklm list --json`

Search results for notebooks with titles matching the topic.
If found, ask user: "Found existing notebook '{title}' with {n} sources. Use it? (y/n)"
- If yes: `notebooklm use {id}`, skip to Step 3
- If no: continue to Step 2

### Step 2: Create research notebook

Run: `notebooklm create "Research: {topic}" --json`
Parse notebook ID from output.
Run: `notebooklm use {id}`

### Step 3: Query existing sources (if focus=A and existing notebook)

If existing notebook was selected, run:
`notebooklm ask "What information do you have about {topic}?" --json`
Store response as baseline context.

### Step 4: Launch deep research

Determine mode from depth:
- Depth 1-2: `--mode fast`
- Depth 3-5: `--mode deep`

Run: `notebooklm source add-research "{topic_query}" --mode {fast|deep} --no-wait`

Show progress: `[2/5] Starting deep research... (mode: {mode})`

### Step 5: Wait for research completion

Run: `notebooklm research wait --import-all --timeout 300`

Show progress: `[3/5] Waiting for sources... (processing...)`

When complete, run: `notebooklm source list --json`
Report: `[3/5] {n} sources imported and ready.`

### Step 6: Extra WebSearch rounds (depth > 3)

If depth >= 4, run 1 WebSearch round:
- Generate 3-5 targeted search queries based on initial findings
- For each query: WebSearch, then read top 3 results with WebFetch
- Add discovered URLs as sources: `notebooklm source add "{url}"`

If depth = 5, run a second WebSearch round:
- Generate 3-5 NEW queries based on combined findings
- Same process: search, fetch, add as sources
- Wait for new sources: `notebooklm source wait {id}`

Show progress: `[4/5] Running additional searches... ({n} extra sources)`

### Step 7: Domain boost (if --domain specified)

Run domain-specific searches from the Domain Boost section below.
Add discovered URLs as sources to the notebook.

### Step 8: Synthesize

Run structured synthesis query:

```bash
notebooklm ask "Based on ALL sources in this notebook, provide a comprehensive research report on '{topic}'.

Structure your response as:

1. EXECUTIVE SUMMARY (3-5 sentences, key takeaways)

2. MAIN FINDINGS (organized by theme, each finding citing specific sources)

3. KEY FINDINGS (bullet list of most important discoveries)

4. CONTRADICTIONS & OPEN QUESTIONS (where sources disagree or gaps exist)

5. For each claim, note which source(s) support it.

Be thorough, analytical, and cite sources precisely." --json
```

Parse response and extract references. Format into the Report Format below.

## Pipeline — Fallback Mode (WebSearch only)

Used when NotebookLM is not available. Iterative WebSearch + WebFetch.

### Round 1: Broad search

Generate 5 search queries from the topic (different angles).
For each query:
1. WebSearch to collect top 5 URLs
2. WebFetch top 3 URLs to extract key findings
3. Store findings + source URLs

Show progress: `[1/{total_rounds}] Broad search... ({n} sources found)`

### Round 2+ (if depth > 1): Deep dive

For each round (up to depth-1 additional rounds):
1. Analyze findings from previous round
2. Identify gaps and unanswered questions
3. Generate 3-5 new targeted queries
4. WebSearch + WebFetch for each
5. Merge new findings with existing

Show progress: `[{round}/{total_rounds}] Deep dive round {n}... ({total} sources)`

### Domain boost in fallback

Same domain-specific queries as full mode, but results stay in-memory
instead of being added to a NotebookLM notebook.

### Synthesis in fallback

Compile all findings into the Report Format below.
Synthesis is done by the agent directly from collected findings.

### Limitations in fallback mode

Post-research actions NOT available without NotebookLM:
- Podcast generation
- Video generation
- Slide deck generation
- Quiz/flashcard generation
- Follow-up questions against persistent notebook

Available actions in fallback:
- Save as .md
- Go deeper (additional WebSearch rounds)
- Compare mode

## Domain Boost

When `--domain` is specified, add these targeted searches to the pipeline.

### Maritime (`--domain maritime`)

Additional search queries:
- `"{topic}" site:imo.org`
- `"{topic}" SOLAS regulation`
- `"{topic}" STCW code`
- `"{topic}" ISM Code`
- `"{topic}" site:iacs.org.uk`
- `"{topic}" Maritime Safety Committee MSC circular`
- `"{topic}" class society guidelines`

Source priority (highest to lowest):
1. IMO resolutions, circulars, guidelines
2. SOLAS/STCW/ISM Code references
3. IACS unified requirements
4. Class society publications (Lloyd's, DNV, BV, ABS)
5. Maritime industry papers (BIMCO, ICS, INTERCARGO)
6. General maritime publications

Citation format: include regulation references when available.
Example: "SOLAS Ch. III, Reg. 19.3.3" or "STCW Code Table A-VI/1"

### Legal (`--domain legal`)

Additional search queries:
- `"{topic}" legislation regulation`
- `"{topic}" official journal law`
- `"{topic}" court decision ruling`
- `"{topic}" regulatory framework directive`
- `"{topic}" compliance requirements`

Source priority:
1. Official government legislation/gazettes
2. Court decisions and rulings
3. Regulatory body publications
4. Legal databases and commentary
5. Law firm analysis and white papers

### Academic (`--domain academic`)

Additional search queries:
- `"{topic}" research paper study`
- `"{topic}" peer-reviewed journal`
- `"{topic}" systematic review meta-analysis`
- `"{topic}" site:arxiv.org`
- `"{topic}" site:researchgate.net`
- `"{topic}" IEEE conference proceedings`

Source priority:
1. Peer-reviewed journal articles
2. Systematic reviews and meta-analyses
3. Conference proceedings
4. Preprints (arXiv, SSRN)
5. University research reports
6. Technical reports and white papers

## Report Format

Format the final output as a Gemini Deep Research-style report:

```markdown
# {Topic} — Deep Research Report

**Generated:** {date} | **Sources:** {count} | **Depth:** {depth_label} | **Domain:** {domain or "General"}

## Executive Summary

{3-5 sentence overview of the most important findings. Lead with the answer,
not the process. What does the user need to know?}

## 1. {First Major Theme}

{Detailed analysis. Every factual claim includes a footnote reference.^1
When sources disagree, note the disagreement explicitly.^2,3}

## 2. {Second Major Theme}

{Continue with thematic sections. Number of sections scales with depth:
depth 1-2 = 2-3 sections, depth 3 = 3-5 sections, depth 4-5 = 5-8 sections.}

## Key Findings

- {Most important finding — with practical implication}
- {Second finding — actionable takeaway}
- {Third finding — what this means for the user}

## Contradictions & Open Questions

- {Where Source A says X but Source B says Y — explain why}
- {Gaps in current research or knowledge}
- {Areas where no consensus exists}

---

### Sources

^1 {Title} — {URL} — [{credibility_tag}]
^2 {Title} — {URL} — [{credibility_tag}]
^3 {Title} — {URL} — [{credibility_tag}]
```

### Source Credibility Tags

Assign one tag to each source based on its origin:

| Tag | Criteria |
|-----|----------|
| `official` | Government body, regulatory org, international org (IMO, EU, WHO) |
| `academic` | Peer-reviewed journal, university publication, .edu domain |
| `industry` | Professional association, established trade publication |
| `news` | Major news outlet, established journalist |
| `blog` | Personal site, forum, social media, unverified source |

Display format in sources list: `^1 Title — URL — [official]`

## Post-Research Actions

After displaying the report, present this menu:

```
Research complete! What next?

  [S] Save as .md file
  [P] Generate podcast from findings
  [V] Generate video explainer
  [D] Generate slide deck
  [Q] Generate quiz/flashcards
  [F] Ask follow-up questions
  [+] Go deeper on a specific section
  [C] Compare with another topic
  [X] Done

Choose (or multiple, e.g. "S, P"):
```

**In fallback mode**, only show: S, F (as new search), +, C, X.

### Action: Save as .md [S]

Ask: "Where should I save the report?"
Wait for path. Default suggestion: `./research/{topic-slug}.md`
Write the report to the specified path.

### Action: Podcast [P] (Full mode only)

```bash
notebooklm generate audio "Create an engaging podcast discussion about the research findings. Focus on the most important and surprising discoveries. Make it conversational and accessible." --json
```

Note the artifact ID. Inform user:
"Podcast generating (~10-20 min). I'll download it when ready."
Spawn background agent to wait + download:
`notebooklm artifact wait {id} && notebooklm download audio ./research/{topic-slug}-podcast.mp3`

### Action: Video [V] (Full mode only)

```bash
notebooklm generate video "Create an explainer video covering the key findings of this research." --json
```

Same pattern: note artifact ID, spawn background agent for wait + download to `./research/{topic-slug}-video.mp4`

### Action: Slide Deck [D] (Full mode only)

```bash
notebooklm generate slide-deck --format detailed --json
```

Download as .pptx when ready:
`notebooklm download slide-deck ./research/{topic-slug}-slides.pptx --format pptx`

### Action: Quiz/Flashcards [Q] (Full mode only)

Ask: "Quiz or flashcards?"

Quiz:
```bash
notebooklm generate quiz --difficulty medium --json
```
Download: `notebooklm download quiz ./research/{topic-slug}-quiz.md --format markdown`

Flashcards:
```bash
notebooklm generate flashcards --difficulty medium --json
```
Download: `notebooklm download flashcards ./research/{topic-slug}-cards.md --format markdown`

### Action: Follow-up [F]

Ask: "What would you like to know more about?"
- Full mode: `notebooklm ask "{follow-up question}" --json`
- Fallback mode: Run new WebSearch round focused on the follow-up question

Display answer, then show the menu again.

### Action: Go Deeper [+]

Ask: "Which section should I investigate further? (enter number)"
Take the section topic, run an additional research round:
- Full mode: `notebooklm source add-research "{section topic details}" --mode deep`
- Fallback mode: Additional WebSearch round on that section

Re-synthesize the specific section with new sources. Display updated section.
Show menu again.

### Action: Compare [C]

Ask: "Compare '{topic}' with what?"
Transition to compare mode with current topic as side A.
Run full research pipeline on side B.
Generate comparison report (see Compare Mode section).

## Continue Mode (`--continue`)

When invoked with `--continue`:

1. Run `notebooklm list --json`
2. Filter notebooks with titles starting with "Research:"
3. Present list:

```
Previous research sessions:

  1. "Research: ballast water treatment" (24 sources)
  2. "Research: enclosed space regulations" (18 sources)
  3. "Research: AI in maritime training" (12 sources)

Pick a session to continue (or 0 for new research):
```

4. If user picks a session:
   - `notebooklm use {id}`
   - Ask: "What aspect should I research further?"
   - Run additional research round with the new query
   - Re-synthesize all sources (old + new)
   - Display updated report
   - Show post-research menu

5. If user picks 0: start normal research flow

In fallback mode, `--continue` is not available (no persistent notebooks).
Inform user: "Continue mode requires NotebookLM. Install with: `pip install notebooklm-py && notebooklm login`"

## Compare Mode (`--compare "X vs Y"`)

When invoked with `--compare`:

1. Parse X and Y from arguments
2. Ask depth (same pre-flight prompt, default=3)
3. Create notebook: `notebooklm create "Research: {X} vs {Y}" --json`
4. Add research for X: `notebooklm source add-research "{X}" --mode deep`
5. Add research for Y: `notebooklm source add-research "{Y}" --mode deep`
6. Wait for both to complete
7. Synthesize with comparison prompt:

```bash
notebooklm ask "Compare {X} and {Y} based on all sources. Structure as:

1. OVERVIEW: What is X? What is Y? (2-3 sentences each)

2. COMPARISON TABLE: Side-by-side comparison of key dimensions
   | Dimension | X | Y |

3. STRENGTHS: What X does better, what Y does better

4. WEAKNESSES: Limitations of each

5. USE CASES: When to choose X, when to choose Y

6. VERDICT: Your recommendation with reasoning

Cite sources for all claims." --json
```

8. Format as comparison report with footnotes
9. Show post-research menu

In fallback mode, compare runs two separate WebSearch pipelines and synthesizes both.

## Progress Indicator

Display real-time status throughout the pipeline. Update after each step:

```
[1/6] Checking existing notebooks...
[2/6] Creating research notebook...
[3/6] Running deep research... (mode: deep)
[4/6] Waiting for sources... (18 found, processing...)
[5/6] Running domain-specific searches... (+3 sources)
[6/6] Synthesizing findings...

Done — 24 sources analyzed. Report below.
```

Step count adjusts based on pipeline:
- No domain boost: 5 steps
- With domain boost: 6 steps
- With extra WebSearch rounds: +1 per round
- Fallback mode: `[{round}/{total_rounds}]` format

## Error Handling

| Error | Detection | Action |
|-------|-----------|--------|
| NotebookLM not authenticated | `notebooklm status` fails with auth error | Show: "Run `notebooklm login` to authenticate" |
| NotebookLM not installed | `notebooklm` command not found | Switch to fallback mode, inform user |
| Research timeout | `research wait` returns exit code 2 | "Research timed out. Showing partial results from {n} sources found so far." |
| Rate limit on generation | `generate` returns exit code 1 with rate limit | "Rate limited. Try again in 5-10 minutes, or use NotebookLM web UI." |
| No sources found | Research returns 0 sources | "No sources found via NotebookLM. Falling back to web search." Then run fallback pipeline. |
| WebSearch returns no results | All queries return empty | "Could not find relevant sources. Try rephrasing your topic or using a broader query." |
| Source processing stuck | Sources stay in "processing" > 5 min | Proceed with ready sources, note incomplete ones |
