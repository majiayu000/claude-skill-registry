---
name: deep-research-team
description: >
  This skill should be used when the user asks for "deep research", "research team",
  "comprehensive analysis", "research report", "investigate thoroughly", "compare X vs Y in
  depth", or needs synthesis across multiple sources with verification. It spawns a coordinated
  team of researcher agents across multiple rounds, with the lead triaging findings and creating
  targeted follow-up tasks. Scales from Focused (2 researchers, 1-2 rounds) to Comprehensive (4
  researchers, 3-4 rounds with cross-verification). Do NOT use for simple lookups, debugging, or
  questions answerable with 1-2 searches.
---

# Deep Research Team (Lead Orchestrator)

Conduct thorough, iterative research by coordinating a persistent team of researcher agents across
multiple rounds. This architecture enables mid-investigation steering, targeted follow-up based on
emerging findings, and cross-agent verification.

## Architecture Overview

```
Round 1: Investigation      Round 2: Follow-up          Synthesis

┌──────────┐                  ┌──────────┐                  ┌────────┐
│Researcher│  sends findings  │Researcher│  sends findings  │        │
│    A     ├─────────┬───────>│    A     ├─────────┬───────>│        │
└──────────┘         │        └──────────┘         │        │        │
                     │                             │        │        │
                     v          dispatches         v        │        │
┌──────────┐    ┌────────┐    ┌──────────┐    ┌────────┐    │  Lead  │
│Researcher├───>│  Lead  │───>│Researcher├───>│  Lead  │───>│  synth │
│    B     │    │triages │    │    B     │    │triages │    │  esizes│
└──────────┘    └────────┘    └──────────┘    └────────┘    │        │
                     ^                             ^        │        │
┌──────────┐         │        ┌──────────┐         │        │        │
│Researcher├─────────┴───────>│Researcher├─────────┴───────>│        │
│    C     │  sends findings  │    C     │  sends findings  │        │
└──────────┘                  └──────────┘                  └────────┘
```

**Key principles:**

1. **No peer-to-peer researcher communication.** All coordination goes through the lead. This
   preserves the independence that accounts for 87% of multi-agent gains (Choi et al.) and avoids
   sycophancy failures (Wynn et al.). Researchers never see each other's findings.

2. **Multi-round iteration.** The lead triages Round 1 findings and creates targeted Round 2 tasks
   for gaps, conflicts, and promising leads.

3. **Cross-agent verification (Comprehensive scope).** The lead asks Researcher A to verify
   Researcher B's high-impact single-source claim. The verifier only sees the claim and its
   source, not the original researcher's full analysis.

4. **Dynamic task evolution.** The shared task list starts with pre-planned angles but grows
   organically as follow-up tasks emerge from findings. The lead dispatches follow-up tasks
   directly to specific researchers via SendMessage.

## When to Use

**Use this skill for:**

- Complex questions that benefit from multiple research angles
- Topics where initial findings will reveal what to investigate next
- Research requiring cross-verification of contested claims
- Any question needing synthesis across 5+ sources

**Do NOT use for:**

- Simple factual lookups (use regular web search)
- Questions answerable with 1-2 searches
- Debugging or code questions

## Effort Calibration

| Scope             | Researchers | Rounds | Verification | Model  |
| ----------------- | ----------- | ------ | ------------ | ------ |
| **Focused**       | 2           | 1-2    | None         | sonnet |
| **Broad**         | 3           | 2-3    | None         | sonnet |
| **Comprehensive** | 4           | 3-4    | Cross-agent  | opus   |

Round counts are heuristics, not targets. Stop early when you hit citation convergence --
additional rounds that don't surface new substantive findings waste tokens and context. A
Broad run that converges in 2 rounds is a success, not a shortcut. After each round's triage,
ask: "Would another round change the report's conclusions?" If not, proceed to synthesis.

Default scope is determined by question type (see `references/question-types.md`).
Present the recommended scope to the user and allow override.

**Model selection:**

- **Lead**: inherits user's session model (no override)
- **Researchers**: `sonnet` for Focused/Broad, `opus` for Comprehensive

(Sonnet validated as viable override for Comprehensive when cost matters)

## Output Directory

Research artifacts persist to disk for resumability and backup.

**Directory resolution** -- run this command FIRST, before creating anything. The output is
your `{output_dir}`. Only the fallback branch creates a directory; the others reuse what exists.

```bash
if [ -d "$(pwd)/deep-research" ]; then
  echo "$(pwd)/deep-research"
elif [ -n "$CLAUDE_DEEP_RESEARCH_DIR" ]; then
  eval echo "$CLAUDE_DEEP_RESEARCH_DIR"
else
  mkdir -p "$(pwd)/deep-research"
  echo "$(pwd)/deep-research"
fi
```

After resolving `{output_dir}`, create only the topic subdirectory in Phase 3.

Each session creates a subdirectory: `{output_dir}/{topic-slug}/`

**Contents:**

- `state.md` -- triage checkpoint, cross-references, follow-up plan (written in Phase 4)
- `researcher-{letter}-findings.md` -- backup of each researcher's findings
- `report.md` -- final synthesized report (written in Phase 6)

## Calibrated Confidence Language

Use Kent-style verbal probability expressions in all confidence assessments:

| Term           | Range  | Use When                                  |
| -------------- | ------ | ----------------------------------------- |
| Almost certain | 93-99% | Multiple high-quality sources, no dissent |
| Highly likely  | 80-92% | Strong evidence, minor caveats            |
| Likely         | 63-79% | Good evidence, some gaps                  |
| Roughly even   | 40-62% | Conflicting evidence, genuinely uncertain |
| Unlikely       | 20-39% | Limited or weak evidence                  |

Always pair the verbal term with the probability range in the final report.

## Process

### Phase 0: Classify Question Type

Silently classify the user's question before any interaction.

1. Read `references/question-types.md` for the full taxonomy.
2. Assign a primary type: Factual, Scientific/Health, Consumer, Technical, Opinion/Sentiment,
   Contested, or Emerging/Frontier.
3. For compound questions, decompose into sub-questions and classify each.
4. Note the default scope from the type-to-scope mapping.

**Resume check:** Before starting, list the subdirectories in `{output_dir}` and scan for any
that look related to the current question (similar topic, overlapping keywords). If you find
a plausible match, read its `state.md` and offer to resume: present what was completed, what
remains, and ask the user whether to resume or start fresh. If resuming, create a new team
and tasks for only the remaining work.

**Topic slug:** When creating a new session, generate a slug (lowercase, hyphenated, max 40
chars) for the subdirectory name: `{output_dir}/{slug}/`.

Classification is internal—do not present it to the user.

### Phase 1: Clarify and Plan

**Step 1: Make sure you understand the question.** Before planning anything, ask yourself:
do I understand what the user is asking and *why* well enough to design research angles that
will actually be useful to them? If not, use `AskUserQuestion` to fill the gaps. This isn't
just about ambiguous wording -- a perfectly clear question can still lack enough context to
research well ("How does Nix handle dependencies?" means very different research depending on
whether you're evaluating Nix, debugging an issue, or writing docs). If the question and its
context are clear, skip this step.

**Step 2: Scope and decompose.** Determine the appropriate scope (Phase 2 has the details)
and decompose the question into independent research angles. Default angle counts by scope:

- Focused: 2 angles
- Broad: 3 angles
- Comprehensive: 4 angles

These are defaults, not caps. If the decomposition reveals one more genuinely independent
facet than the default, add it (e.g., 3 angles for a Focused run). If the question has
fewer real facets, use fewer. Beyond ±1 from the default, re-scope rather than stretching --
the scope was probably wrong. Each angle must be independent and substantial enough to
warrant a dedicated researcher; "I can think of another angle" isn't sufficient.

For compound questions, map sub-questions to angles. Multiple sub-questions can share an
angle if closely related; a single sub-question can span multiple angles if it has distinct
facets.

**Step 3: Confirm if high-investment.** For compound, contested, or Comprehensive-scope
questions, present the research plan for user approval before spawning researchers:

> Research plan for "{question}":
>
> - Type: {type} | Scope: {scope} | {N} researchers, {M} rounds
> - Angles: {list of planned angles}
> - [If compound] Sub-question → angle mapping: ...
>
> Proceed, or adjust?

For clear, low-scope questions, skip confirmation and proceed.

### Phase 2: Calibrate Effort

Select the scope tier based on question type defaults from `references/question-types.md`,
then apply the scope modifiers from that file (de-escalation and escalation signals).
Also adjust for:

- User's explicit preference (if stated)
- Structural complexity (compound questions with 3+ sub-types escalate)

Announce the plan: "Starting {scope} team research with {N} researchers."

### Phase 3: Team Setup

**Step 1: Create the output directory**

```bash
mkdir -p {output_dir}/{topic-slug}
```

**Step 2: Create the team**

```
TeamCreate:
  team_name: "deep-research-{topic-slug}"
  description: "Researching {topic} in {scope} scope"
```

**Step 3: Create initial tasks**

One `TaskCreate` per research angle:

```
TaskCreate:
  subject: "Investigate {angle title}"
  description: |
    Research angle: {angle description}
    Topic context: {brief topic summary}
    Question type: {type from Phase 0}
    Focus: {what specifically to investigate}
    Return structured findings via SendMessage to the lead.
  activeForm: "Investigating {angle title}"
```

**Task brief clarity:** Make scope boundaries explicit between researchers to avoid overlap
and gaps. Flag name ambiguities (e.g., multiple products sharing a name). Mark optional
sub-tasks clearly (e.g., "if time permits" vs required).

**Step 4: Spawn researchers**

Launch ALL researchers in a SINGLE message. Each researcher gets:

```
Task:
  subagent_type: "general-purpose"
  name: "researcher-{letter}"
  team_name: "deep-research-{topic-slug}"
  model: "sonnet"  (or "opus" for Comprehensive)
  description: "Spawn researcher {letter}"
  prompt: |
    You are a research agent on a team. Your job is to investigate research tasks
    by searching the web, evaluating sources, and reporting structured findings.

    FIRST: Read your methodology at: {absolute path to references/researcher-prompt.md}

    Question type: {type from Phase 0}
    Output directory: {output_dir}/{topic-slug}
    Your researcher letter: {letter} (use LOWERCASE in filenames: researcher-{lowercase letter})
    Lead name: team-lead (send all findings to this name via SendMessage)

    Your assigned task is #{id}: "{subject}"
    Use TaskGet for full details, then begin investigation.

    After completing your task, go idle. The lead will message you directly
    when new tasks are available.
```

Include the task ID, subject, question type, output directory, researcher letter,
and lead name directly in each researcher's spawn prompt.

### Phase 4: Investigation Loop

This is the core research cycle. Each iteration is a **round**: researchers investigate,
the lead triages, then either dispatches follow-ups (another round) or exits to synthesis.

#### Round structure

**Investigate:** Researchers work on their assigned tasks. Each researcher will:

1. Read the methodology reference file
2. Load web search and content extraction tools via ToolSearch
3. Execute the investigation loop (search -> evaluate -> reflect -> decide)
4. Write findings to `{output_dir}/{topic-slug}/researcher-{letter}-findings.md`
5. Notify the lead via `SendMessage` with the file path (not the full findings --
   avoids doubling output tokens)
6. Mark their task as completed via `TaskUpdate`
7. Go idle and wait for the lead to dispatch follow-up tasks via `SendMessage`

**Monitoring**: The lead reads each researcher's findings file after receiving
their notification. No polling needed.

**Handling partial results**: If a researcher reports rate limit issues or thin coverage,
note the gap for triage rather than immediately spawning replacements.

**Triage:** After all tasks for the current round complete, systematically review findings.

*Step 1: Extract and cross-reference claims*

For each significant claim across all researcher findings:

- How many **independent sources** support it? (Different researchers finding the same
  source counts as one source, not two.)
- **HIGH confidence**: 3+ independent sources of different types (e.g., paper + dataset +
  practitioner account), no credible dissent
- **MEDIUM confidence**: 2 independent sources, or multiple sources of the same type
- **LOW confidence**: Single source, or multiple sources that trace back to one original

*Step 2: Identify gaps and conflicts*

- What angles remain uncovered?
- Where do researchers contradict each other?
- What findings are surprising and deserve deeper investigation?
- Which claims rest on a single source?

*Step 3: Decide whether to continue or exit*

Exit to Phase 5 (Synthesis) if findings have converged -- another round wouldn't change the
report's conclusions. Continue if significant gaps, conflicts, or single-source high-impact
claims remain and the scope's round budget allows.

If findings reveal more complexity than anticipated (e.g., Broad scope uncovering deeply
contested claims requiring steelmanning), escalate: spawn an additional researcher or add
a round beyond the default budget.

*Step 4: Persist triage state*

Write or update `{output_dir}/{topic-slug}/state.md`:

```markdown
# Research State: {topic}

## Status: TRIAGE_COMPLETE (Round {N})

## Question Type: {type}

## Scope: {scope}

## Round {N} Summary

{brief cross-reference of key findings, gaps, conflicts}

## Follow-up Plan

{list of planned follow-up tasks with rationale, or "Proceeding to synthesis"}
```

#### Dispatching follow-up tasks

If continuing, create targeted tasks based on what triage revealed. These are all just
task types -- they use the same dispatch mechanism:

> **Gap-fill**: "No researcher covered {aspect}. Investigate {specific question}."

> **Conflict-resolution**: "One source says X, another says Y. Search for additional
> sources that clarify which is accurate and why they might differ."

> **Deep-dive**: "Initial findings revealed {unexpected thing}. Investigate further:
> {specific follow-up questions}."

> **Verification** (Comprehensive scope): Use when high-impact claims rest on a single
> source, factual conflicts remain unresolved, or claims are in specialized/niche domains
> where citation error rates are higher. Assign to a researcher who did NOT make the
> original claim. Task description contains only the claim and its source URL:
>
> ```
> TaskCreate:
>   subject: "Verify: {claim summary}"
>   description: |
>     Verification task. Search for ADDITIONAL sources (not the original) and determine
>     if they support, contradict, or add nuance to this claim.
>
>     CLAIM: {specific factual claim}
>     ORIGINAL SOURCE: {URL}
>
>     Report your verdict as: SUPPORTED, SUPPORTED WITH NUANCE, CONTESTED, or UNCHANGED
>     Include the additional sources you found and any important nuance.
>   activeForm: "Verifying claim about {topic}"
> ```

**Critical**: Follow-up task descriptions contain just enough context without revealing
other researchers' full conclusions. This preserves independence.

**Assignment strategy:** The lead assigns follow-up tasks directly via `SendMessage` rather
than relying on researchers to self-claim. Choose assignees based on task type:

- **Deep-dives and gap-fills**: Assign to the researcher who covered the related angle
  (continuity -- they have context on what was already found).
- **Conflict resolution and verification**: Assign to a researcher who did NOT cover either
  side (fresh perspective avoids confirmation bias).
- **If researchers outnumber tasks**: Idle researchers wait or are shut down early.

```
SendMessage:
  type: "message"
  recipient: "researcher-{letter}"
  content: "New task available: #{id} -- {subject}. Please claim it and begin."
  summary: "Follow-up task assignment"
```

Then loop back to **Investigate** above.

**Interpreting verification results:** When a verification task returns, adjust confidence:

- **SUPPORTED**: Upgrade confidence; note additional sources
- **SUPPORTED WITH NUANCE**: Directionally correct but specific details differ or require
  qualification. Upgrade confidence for the general claim; add caveats for specifics.
- **CONTESTED**: Flag explicitly; present both sides with evidence
- **UNCHANGED**: Keep original confidence level

### Phase 5: Synthesize (Type-Aware)

Combine all findings from all rounds into a coherent report. Select the synthesis template
matching the question type from Phase 0. For compound questions, use the template for each
sub-question's type, then add an overall synthesis section.

**End-of-sequence awareness:** Draft Confidence Assessment and Limitations sections **early**,
not last. Review final paragraphs specifically for unsourced claims.

#### Template Selection

Read the template file matching the question type from Phase 0. Each template includes the
full report structure (executive summary, type-specific body, confidence assessment,
limitations, sources). For compound questions, read the template for each sub-question's
type and add an overall synthesis section.

| Question Type         | Template File                                |
| --------------------- | -------------------------------------------- |
| **Factual**           | `references/templates/factual.md`            |
| **Scientific/Health** | `references/templates/scientific-health.md`  |
| **Consumer**          | `references/templates/consumer.md`           |
| **Technical**         | `references/templates/technical.md`          |
| **Opinion/Sentiment** | `references/templates/opinion-sentiment.md`  |
| **Contested**         | `references/templates/contested.md`          |
| **Emerging/Frontier** | `references/templates/emerging-frontier.md`  |

### Phase 6: Persist Report

Write the final report:

```
Write: {output_dir}/{topic-slug}/report.md
```

Update `state.md` status to `COMPLETE`:

```
Edit: {output_dir}/{topic-slug}/state.md
  old_string: "## Status: TRIAGE_COMPLETE"
  new_string: "## Status: COMPLETE"
```

**Format output files (optional):** If `prettier` is available, run it on all markdown files
in the output directory to normalize formatting:

```bash
prettier --write --prose-wrap preserve "{output_dir}/{topic-slug}/**/*.md"
```

If prettier is not installed, skip this step silently -- it is cosmetic, not functional.

Inform the user: "Report saved to `{output_dir}/{topic-slug}/report.md`."

### Phase 7: Cleanup

Shut down the team cleanly.

**Step 1: Shut down researchers**

Send `shutdown_request` to each researcher via `SendMessage`:

```
SendMessage:
  type: "shutdown_request"
  recipient: "researcher-a"
  content: "Research complete. Shutting down."
```

Repeat for each researcher. Wait for shutdown responses.

**Step 2: Read researcher feedback**

After all researchers have shut down, read any feedback files written to
`{output_dir}/{topic-slug}/researcher-{letter}-feedback.md`. These contain notes on
tool usage (Exa parameters, Firecrawl usage), issues encountered (400 errors, rate limits),
and suggestions. Use this feedback to identify patterns for skill improvement.

**Step 3: Delete team**

```
TeamDelete
```

## Writing Standards

- Prose paragraphs, not bullet lists (bullets only for distinct enumerations)
- Specific data: "increased 23%" not "increased significantly"
- Cite inline with markdown footnotes: "The market grew 15%[^1]" not "The market grew.[^1]"
- Each finding: 2-4 paragraphs with evidence
- Distinguish FACTS (cited) from ANALYSIS (synthesis)

## Anti-Hallucination Protocol

- Every factual claim must cite a source immediately
- Mark synthesis distinctly: "This suggests..." or "Synthesizing these findings..."
- If uncertain, say so: "Sources disagree on..." or "Limited evidence for..."
- Never fabricate sources -- all citations come from researcher findings

## Additional Resources

### Reference Files

- **`references/question-types.md`** -- 7-type taxonomy, signals, decomposition rules,
  type-to-scope defaults. Read in Phase 0.
- **`references/researcher-prompt.md`** -- Investigation methodology, type-aware source
  evaluation, output format. Path provided to researchers in spawn prompt. (Tool guidance
  extracted to the standalone `search-tips` skill, which researchers load as their first step.)
- **`references/templates/`** -- Type-specific synthesis templates. Read the relevant
  template(s) in Phase 5. See Template Selection table above.

### Scripts

- **`scripts/analyze-transcripts.py`** -- Post-hoc analysis of researcher tool usage.
  Extracts MCP tool call parameters from subagent JSONL transcripts and produces a
  compliance report. Usage:
  - `python3 scripts/analyze-transcripts.py --session ${CLAUDE_SESSION_ID}` -- current session
  - `python3 scripts/analyze-transcripts.py "topic keyword"` -- auto-detect session by keyword
  - `python3 scripts/analyze-transcripts.py --list` -- list recent sessions with subagents

### Development History

- **`dev/RESEARCH.md`** -- Design rationale with 50+ sources justifying the architecture
- **`dev/ITERATION-LOG.md`** -- 13 iterations of improvement with backlog
- **`dev/iterations/`** -- Detailed notes for each iteration

## Quick Reference

0. **Classify** question type (silent) and check for resume
1. **Clarify** -- understand the question, resolve ambiguity, confirm plan if high-investment
2. **Calibrate** effort: announce scope and researcher count
3. **Setup**: create output dir, TeamCreate, TaskCreate per angle, spawn researchers
4. **Investigation loop**: investigate → triage → dispatch follow-ups or exit. Repeat until converged.
5. **Synthesize**: type-aware template, calibrated confidence language
6. **Persist**: write report.md, update state.md to COMPLETE, tell user file location
7. **Cleanup**: shutdown_request to each researcher, then TeamDelete

**Context budget:**

- Lead context: reserve for triage + synthesis
- Researcher contexts: handle all search/scrape operations
- Researcher spawn prompts: compact (~30 lines), point to reference file
- Researcher findings: structured summaries (~120 lines each)
