---
name: deep-research
description: >-
  Deep, iterative, multi-source research that explores a topic from multiple
  perspectives, detects contradictions, and produces a comprehensive vault note
  with fact-level citations and a confidence map. Use this skill whenever the user
  says /deep-research, "deep research X", "research X thoroughly", "investigate X
  deeply", "I need to really understand X", or wants research that goes beyond a
  quick web search. Also use when the user wants to understand a complex, contested,
  or multi-faceted topic, compare competing approaches with evidence, or build a
  comprehensive mental model they can trust for decisions. This is heavier than
  /research — it searches web, academic papers, Reddit, and the vault, then loops
  through exploration and critique rounds until the evidence base is solid. When in
  doubt between /research and /deep-research, prefer this one if the topic is
  complex, contested, or the user wants depth over speed.
allowed-tools: Bash, Read, Write, Edit, Agent, Grep, Glob, WebFetch, WebSearch, mcp__reddit-mcp-buddy__search_reddit, mcp__reddit-mcp-buddy__get_post_details, mcp__obsidian-vault__search_notes, mcp__obsidian-vault__read_note, mcp__obsidian-vault__read_multiple_notes, mcp__obsidian-vault__write_note, mcp__obsidian-vault__update_frontmatter
argument-hint: "<topic or question> [--quick | --deep]"
---

<Purpose>
Iterative, multi-perspective research that explores broadly and goes deep. Unlike
`/research` (single-pass, web-only, 5-10 sources), this skill:
- Discovers PERSPECTIVES before searching (not just sub-questions)
- Searches 4 source types in parallel: web, academic papers, Reddit, vault
- Runs an exploration → critique loop that finds gaps, contradictions, and new angles
- Uses an outline-first approach to prevent hallucination
- Produces a note with fact-level citations, a confidence map, and explicit uncertainty

The architecture is inspired by Stanford's STORM (perspective discovery + outline-first),
Anthropic's multi-agent research system (parallel exploration + intelligent critique),
and pi-autoresearch (living state files that survive context resets).
</Purpose>

<Use_When>
- User wants DEEP understanding, not a quick summary
- Topic is complex, contested, or multi-faceted
- User needs to make a decision based on the research
- User wants to compare competing approaches with evidence
- User explicitly asks for /deep-research or "thorough research"
</Use_When>

<Do_Not_Use_When>
- User wants a quick answer (use /research instead)
- User wants to find academic papers specifically (use /paper-discover)
- User wants to process an existing vault note (use /process)
- User wants cross-domain vault synthesis (use /synthesize)
</Do_Not_Use_When>

<Steps>

## Stage 0: SETUP

Parse `$ARGUMENTS` for the topic and optional depth flag:
- `--quick`: faster, fewer rounds, sonnet everywhere, no perspective discovery
- `--deep`: more rounds, opus for critic and synthesis, outline reviewed by user
- Default (no flag): balanced — perspective discovery, 2-4 rounds, opus for synthesis

Create the workspace:
```bash
TOPIC_SLUG=$(echo "$TOPIC" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | cut -c1-30)
WORK_DIR="temp/research-${TOPIC_SLUG}"
mkdir -p "$WORK_DIR"/{findings,gaps}
```

**Resume check**: Before creating, check if the workspace already exists:
```bash
ls "$WORK_DIR/state.md" 2>/dev/null
```
If `state.md` exists, read it and ask the user: "Found incomplete research on
[topic] (round N). Resume or start fresh?" If resuming, read `state.md` to
determine which stage to skip to.

Tell the user what's happening:
```
Deep researching "{topic}" ({depth mode}).
Setting up workspace at {WORK_DIR}...
```

## Stage 1: PLAN — Decompose + Discover Perspectives

Read the agent definition:
```
Read(".claude/skills/deep-research/agents/research-planner.md")
```

Launch the planner agent:
```
Agent(
  model="sonnet",
  prompt="You are Research Planner. Follow these instructions exactly:

  [INSERT FULL CONTENT OF agents/research-planner.md HERE]

  TOPIC: {topic}
  DEPTH_MODE: {quick|standard|deep}
  WORK_DIR: {WORK_DIR}

  Write state.md and ideas.md to the WORK_DIR."
)
```

After the planner completes, read `state.md` briefly and tell the user:
```
Perspectives identified: {list}
Sub-questions: {count}
Exploration ideas: {count}
Starting exploration...
```

## Stage 2: EXPLORE — Parallel Deep Dives

Read the agent definition and source tiers reference:
```
Read(".claude/skills/deep-research/agents/research-explorer.md")
Read(".claude/skills/deep-research/references/source-tiers.md")
```

Read `ideas.md` and pick the 3-5 highest-priority unexplored ideas.

For EACH selected idea, launch an explorer agent in the background:
```
Agent(
  model="sonnet",
  run_in_background=true,
  prompt="You are Research Explorer. Follow these instructions exactly:

  [INSERT FULL CONTENT OF agents/research-explorer.md HERE]

  SOURCE TIERS REFERENCE:
  [INSERT FULL CONTENT OF references/source-tiers.md HERE]

  ANGLE: {the idea to explore}
  PERSPECTIVE: {which perspective this serves}
  QUERIES: {the search queries from ideas.md}
  STATE_CONTEXT: {summary from state.md — what's already known}
  OUTPUT_FILE: {WORK_DIR}/findings/angle-{NN}-{slug}.md

  Write your findings to OUTPUT_FILE using the Write tool."
)
```

Wait for all explorer agents to complete. Verify each output file exists:
```bash
ls {WORK_DIR}/findings/
```

Update `ideas.md` — mark explored ideas as `[x]`. If explorers discovered new
threads, append them to ideas.md under "## Discovered During Research".

Tell the user:
```
Round {N} complete: explored {count} angles, found {count} sources.
Running critique...
```

## Stage 3: CRITIQUE — The Intelligence Layer

**For `--quick` mode**: skip the critic agent entirely. Instead, briefly review the
findings yourself — check if any sub-questions are obviously thin. If so, do ONE
more targeted search round. Then proceed to Stage 5.

**For standard and `--deep` mode**: Launch the critic agent.

Read the agent definition:
```
Read(".claude/skills/deep-research/agents/research-critic.md")
```

```
Agent(
  model="opus",
  prompt="You are Research Critic. Follow these instructions exactly:

  [INSERT FULL CONTENT OF agents/research-critic.md HERE]

  WORK_DIR: {WORK_DIR}
  ROUND: {current round number}

  Read all files in the workspace, then write your critique to
  {WORK_DIR}/gaps/critique-round-{N}.md.
  Also update {WORK_DIR}/state.md with the coverage map.
  If you have new research ideas, append them to {WORK_DIR}/ideas.md."
)
```

## Stage 4: DECIDE — Continue or Proceed

Read the critic's output: `{WORK_DIR}/gaps/critique-round-{N}.md`

Check the recommendation: CONTINUE or SUFFICIENT.

**If CONTINUE AND within guardrails**:
- Read updated `ideas.md` for new angles
- Loop back to Stage 2 with the new ideas

**If SUFFICIENT OR guardrails hit**:
- Proceed to Stage 5

**Guardrails** (override critic recommendation if needed):
- Max rounds: 2 (quick), 4 (standard), 8 (deep)
- Max total source files: 15 (quick), 30 (standard), 50 (deep)
- If the latest round's explorers produced < 3 new substantive claims → stop
- Count rounds by reading how many `critique-round-*.md` files exist

Tell the user:
```
Critic says: {CONTINUE/SUFFICIENT}. {brief reason}
{If continuing: "Exploring {N} more angles..."}
{If done: "Evidence base ready. Building outline..."}
```

## Stage 5: OUTLINE — Structure Before Content

Build an outline that maps each section to its supporting evidence. This is the
STORM discipline — commit to structure before writing to prevent hallucination.

Read the final critique, all findings files, and state.md. Then write
`{WORK_DIR}/outline.md` with this structure:

```markdown
# Outline: {Topic}

## TL;DR
- {Key finding 1} ← supported by: angle-{NN}, angle-{NN}
- {Key finding 2} ← supported by: angle-{NN}
- {Key finding 3} ← supported by: angle-{NN}, angle-{NN}

## Section: {Theme 1 — insight as heading}
- Key point: {insight}
- Sources: angle-{NN} (claims X,Y), angle-{NN} (claim Z)
- Vault links: [[(Type) Note]] if relevant

## Section: {Theme 2 — insight heading}
- Key point: {insight}
- Sources: ...

## Section: Where Experts Disagree
- Contradiction 1: angle-{NN} vs angle-{NN} on {topic}
- Contradiction 2: ...

## Section: What's Still Uncertain
- {Gap from critic}
- {Single-source claim}

## Confidence Map Notes
- {Finding}: {confidence level} — {evidence basis}
```

**For `--deep` mode**: Show the outline to the user and wait for approval:
"Here's the outline. Want me to adjust anything before I write the full note?"

**For standard and `--quick`**: Proceed automatically.

## Stage 6: SYNTHESIZE — Write the Research Note

Read the agent definition:
```
Read(".claude/skills/deep-research/agents/research-synthesizer.md")
```

Launch the synthesizer:
```
Agent(
  model="opus",  # sonnet for --quick
  prompt="You are Research Synthesizer. Follow these instructions exactly:

  [INSERT FULL CONTENT OF agents/research-synthesizer.md HERE]

  WORK_DIR: {WORK_DIR}
  OUTPUT_FILE: {WORK_DIR}/synthesis.md

  Read outline.md, all findings files, all gap files, and state.md.
  Write the complete vault note body to OUTPUT_FILE.
  Do NOT include frontmatter — just the note content starting with # title."
)
```

## Stage 7: INTEGRATE — Create Vault Note

1. Read `{WORK_DIR}/synthesis.md`

2. Generate timestamp:
   ```bash
   date +%Y%m%d%H%M%S
   ```

3. Determine subfolder — match the topic to existing vault folders:
   - ML/AI topics → `notes/ml/`
   - Startup/business → `notes/startup/`
   - Psychology → `notes/psychology/`
   - Finance → `notes/finance/`
   - Default → `notes/research/`

4. Create the vault note using `mcp__obsidian-vault__write_note` or Write:

   ```markdown
   ---
   id: {YYYYMMDDHHMMSS}
   type: note
   processing_status: processed
   created_date: {YYYY-MM-DD}
   updated_date: {YYYY-MM-DD}
   ---

   {synthesis.md content}
   ```

5. Report to user:
   ```
   Research complete! Created: {note path}

   - Sources: {N} web, {N} academic, {N} community, {N} vault
   - Exploration rounds: {N}
   - Contradictions found: {N}
   - Key uncertainty: {biggest gap}

   Suggested next steps:
   - Extract terms: {list of concepts for extraction}
   - Related research: {follow-up topics}
   - Vault connections: {notes that should link to this}

   Workspace at {WORK_DIR}/ — delete when done.
   ```

</Steps>

<Tool_Usage>
- **Agent**: 4 agent types — planner (sonnet), explorer (sonnet, parallel), critic (opus), synthesizer (opus)
- **WebSearch**: Multi-query web search within explorer agents
- **WebFetch**: Deep-read URLs within explorer agents
- **Bash**: Workspace creation, timestamp, search_papers.py execution
- **Grep/Glob**: Vault search within planner agent
- **MCP obsidian-vault**: Vault search and note creation
- **MCP reddit**: Community source search within explorer agents
- **Read**: Agent definitions, workspace files, source tiers reference
- **Write**: Workspace files (state, ideas, outline), vault note creation
</Tool_Usage>

<Examples>
<Good>
User: /deep-research context engineering for AI agents
1. Setup → temp/research-context-engineering/
2. Plan → 4 perspectives (researcher, practitioner, framework builder, skeptic),
   6 sub-questions, 12 exploration ideas
3. Round 1 → 4 explorer agents, 16 sources (web + papers + Reddit)
4. Critique → "practitioner perspective is thin, contradictions on context window
   vs. summarization tradeoff, missing: cost analysis angle"
5. Round 2 → 3 more explorers targeting gaps, 9 new sources
6. Critique → "SUFFICIENT — good coverage, 2 genuine ongoing debates to present"
7. Outline → 5 themes + disagreements + uncertainties, all mapped to sources
8. Synthesize → 55-bullet note with 25 sources, confidence map, 4 vault connections
9. Integrate → notes/ml/(Research) Context Engineering for AI Agents.md
</Good>

<Bad>
- Searches once and stops — no critique, no gap-filling
- Creates a note that just lists what each source said
- Ignores the vault — no wikilinks, no checking what already exists
- All sources are web — no papers, no Reddit, no diversity
- No confidence map — claims everything with equal certainty
- No "Where Experts Disagree" — hides contradictions instead of presenting them
- Doesn't write workspace files — can't resume if interrupted
</Bad>
</Examples>

<Escalation_And_Stop_Conditions>
- **Topic too broad** ("deep research AI"): Ask user to narrow. Suggest 2-3 specific angles.
- **No results from any source**: Inform user, offer to create a vault-only synthesis from existing notes.
- **Mostly paywalled academic sources**: Note limitation, prioritize open-access and preprints.
- **Topic already deeply covered in vault**: Show existing notes, ask if user wants fresh perspectives or an update.
- **Explorer agent fails**: Check the output file. If missing, log the failure and continue with other angles — don't block the entire research on one failed agent.
- **Context getting large**: The workspace files ARE the state. If context is approaching limits, the user can restart and the skill will offer to resume from the workspace.
</Escalation_And_Stop_Conditions>

$ARGUMENTS
