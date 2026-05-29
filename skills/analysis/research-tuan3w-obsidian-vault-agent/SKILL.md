---
name: research
description: >-
  Research a topic and create a new note in the vault. Use this skill whenever
  the user wants to learn about a topic they don't know yet, investigate a
  question, explore an idea, or asks "what is X", "research X", "tell me about
  X", "I want to understand X", "look into X". Also triggers on /research.
  This is for BROAD research (web + vault) — for academic papers specifically,
  use /paper-discover instead.
allowed-tools: Bash, Read, Write, Edit, Agent, Grep, Glob, WebFetch, WebSearch
argument-hint: "<topic or question>"
---

<Purpose>
Deep research on any topic — search the web and the vault, then synthesize
findings into a high-quality vault note. Unlike a quick web search, this skill
decomposes the question, searches multiple angles, checks what the vault already
knows, and produces a note with source links, confidence levels, and vault
connections.
</Purpose>

<Use_When>
- User asks to research a topic ("research quantum error correction")
- User wants to understand something new ("what is RLHF and why does it matter?")
- User wants a research note created in the vault
- User uses /research with a topic
</Use_When>

<Do_Not_Use_When>
- User wants to find academic papers specifically (use /paper-discover)
- User wants to process an existing vault note (use /process)
- User wants to synthesize across existing vault notes (use /synthesize)
- User has a YouTube video to process (use /youtube)
</Do_Not_Use_When>

<Steps>

## Stage 1: PLAN — Decompose the Question

Parse the topic from $ARGUMENTS. If vague, ask one clarifying question.

Break the research topic into 3-5 **specific sub-questions** that together
cover the topic well. Think about:
- What IS it? (definition, core mechanism)
- Why does it matter? (motivation, impact, who cares)
- How does it work? (process, architecture, method)
- What are the tradeoffs? (limitations, alternatives, open problems)
- Where is it going? (trends, recent developments, future)

Present the sub-questions to the user briefly:
```
Researching "topic". Sub-questions:
1. ...
2. ...
3. ...
Searching now.
```

Don't wait for confirmation unless the topic is ambiguous — just show and go.

## Stage 2: SEARCH VAULT — What Do We Already Know?

Before hitting the web, check what the vault already contains:

```
Grep(pattern="KEYWORD", path="notes/", glob="*.md", head_limit=15)
```

Also try MCP search if available:
```
mcp__obsidian-vault__search_notes(query="KEYWORD", limit=10)
```

Note any existing vault notes that are relevant — these become [[wikilinks]]
in the output and inform what the web search should FOCUS on (gaps, not
repeats).

## Stage 3: SEARCH WEB — Multi-Query, Parallel

For each sub-question, run a targeted WebSearch:

```
WebSearch(query="specific sub-question query", num_results=5)
```

Then WebFetch the 3-5 most promising URLs to get full content:

```
WebFetch(url="URL", prompt="Extract key facts, data, and insights about [sub-question]. Include specific numbers, dates, names, and technical details.")
```

**Search strategy:**
- Use different query phrasings per sub-question (not just the topic repeated)
- Prefer recent sources (add "2025" or "2026" to queries when freshness matters)
- Mix source types: technical blogs, official docs, news, research summaries
- If initial results are thin, reformulate and search again

Run searches in parallel where possible (multiple WebSearch calls in one turn).

## Stage 4: DEEPEN — Find Gaps and Conflicts

After the first search round, review what you have:
- Which sub-questions are well-answered? Which are thin?
- Are there conflicting claims across sources?
- Did any source mention something surprising worth following up?

Run 1-2 targeted follow-up searches to fill gaps. This second pass is what
separates good research from a quick Google.

## Stage 5: SYNTHESIZE — Build the Note

Read the agent definition:
```
Read("${CLAUDE_SKILL_DIR}/agents/research-noter.md")
```

Launch the research-noter agent:

```
Agent(
  subagent_type="general-purpose",
  model="sonnet",
  prompt="You are Research Noter. Follow these instructions exactly:

  [INSERT FULL CONTENT OF agents/research-noter.md HERE]

  RESEARCH TOPIC: [topic]
  SUB-QUESTIONS: [list]

  VAULT CONTEXT (existing notes on this topic):
  [vault search results]

  WEB FINDINGS:
  [organized by sub-question, with source URLs]

  Produce the note body following the Output Format. Do NOT include frontmatter."
)
```

## Stage 6: INTEGRATE — Create the Vault Note

1. Generate timestamp ID: `date +%Y%m%d%H%M%S`

2. Determine subfolder — if the topic clearly fits an existing folder, use it.
   Otherwise default to `notes/research/`. Create the folder if needed.

3. Create the note:

```markdown
---
id: YYYYMMDDHHMMSS
type: note
processing_status: processed
created_date: YYYY-MM-DD
updated_date: YYYY-MM-DD
---

[AGENT OUTPUT — starts with # title]
```

4. Report to user:
   - Note path
   - Number of sources used
   - Key vault connections found
   - Any gaps flagged as uncertain

</Steps>

<Tool_Usage>
- **WebSearch**: Multi-query web search (one per sub-question)
- **WebFetch**: Deep-read promising URLs for full content
- **Grep/Glob**: Search vault for existing knowledge
- **MCP search_notes**: Vault search via Obsidian MCP
- **Agent**: Synthesis agent (sonnet)
- **Write**: Create the research note
- **Bash**: Generate timestamp ID
</Tool_Usage>

<Examples>
<Good>
User: /research RLHF vs DPO for language model alignment
1. Plan → 4 sub-questions: what is each, how do they differ mechanically,
   what are the empirical results, what's the current trend
2. Vault search → found (Term) RLHF, (Paper) DPO paper, 3 related notes
3. Web search → 8 sources across sub-questions, including recent benchmarks
4. Deepen → gap on compute costs, found 2 more sources
5. Synthesize → 5-section note with 12 sources, 6 vault wikilinks
6. Create → notes/ml/(Research) RLHF vs DPO - Alignment Methods Compared.md
</Good>

<Bad>
- Searches once and stops — no gap-finding, no deepening
- Creates a note that's just a list of links with no synthesis
- Ignores what the vault already knows about the topic
- Produces a wall of text instead of structured, bullet-point insights
- No source links — claims without evidence
</Bad>
</Examples>

<Escalation_And_Stop_Conditions>
- **Topic too broad** ("research AI"): Ask user to narrow down
- **No web results**: Inform user, offer to create note from vault knowledge only
- **Mostly paywalled sources**: Note the limitation, use what's available
- **Topic already well-covered in vault**: Show existing notes, ask if user wants a fresh perspective or an update
</Escalation_And_Stop_Conditions>

$ARGUMENTS
