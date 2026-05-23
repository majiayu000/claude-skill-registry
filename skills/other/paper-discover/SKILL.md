---
name: paper-discover
description: >-
  Use when searching for academic papers related to a topic, finding papers
  similar to one already in the vault, or discovering research gaps.
  Triggers on "find papers", "related papers", "paper search", "literature",
  "what papers should I read about X".
allowed-tools: Bash, Read, Write, Edit, Agent, TodoWrite, Grep, Glob
---

<Purpose>
Search academic databases (Semantic Scholar) for papers relevant to a topic
or related to an existing vault note. Returns ranked results with relevance
assessment against vault content. Optionally creates formatted paper notes
in the vault's inbox for processing.
</Purpose>

<Use_When>
- User asks to find papers on a topic ("find papers about scaling laws")
- User wants papers related to an existing note ("what papers connect to this?")
- User is /processing a paper and wants to find related work
- User asks "what should I read about X?"
- User provides a DOI or paper title and wants similar papers
- User wants to fill gaps in a knowledge domain
</Use_When>

<Do_Not_Use_When>
- User has a paper file to analyze (use /paper or /book-analyzer)
- User wants to process an existing vault note (use /process)
- User wants general web research, not academic papers (use /research)
</Do_Not_Use_When>

<Execution_Policy>
- Search first, present results, then create notes only if user approves
- Always check vault for existing paper notes before creating duplicates
- Rank by vault relevance, not just citation count
- Cap at 10 results per search — quality over quantity
- Respect Semantic Scholar rate limits (100 req/5min)
</Execution_Policy>

<Steps>

## Stage 1: PARSE QUERY AND CONTEXT

Determine the search mode from user input:

**Mode A — Topic search** (default):
User provides a topic or question. Extract search terms.
```
"find papers about scaling laws for LLMs" → query: "scaling laws large language models"
```

**Mode B — Similar papers**:
User references an existing vault note or provides a paper ID/DOI.
1. Read the referenced note to extract title, key concepts
2. Use the paper's Semantic Scholar ID or DOI for recommendations
3. Fall back to keyword search if no ID available

**Mode C — Gap filling**:
User asks about a domain. Search vault first to identify what's covered,
then search for papers on uncovered subtopics.

## Stage 2: SEARCH

Run the search script:

```bash
SKILL_DIR="${CLAUDE_SKILL_DIR}"

# Topic search
python3 "$SKILL_DIR/scripts/search_papers.py" "QUERY" --limit 20 --min-citations 5

# With year filter
python3 "$SKILL_DIR/scripts/search_papers.py" "QUERY" --limit 20 --year-from 2020

# Get recommendations from a paper
python3 "$SKILL_DIR/scripts/search_papers.py" "" --recommend-from "DOI:10.xxxx/xxxxx"

# Look up specific paper
python3 "$SKILL_DIR/scripts/search_papers.py" "" --paper-id "DOI:10.xxxx/xxxxx"
```

Script returns JSON array of papers with: title, authors, year, abstract,
tldr, citation_count, influential_citations, url, doi, arxiv_id, fields_of_study.

## Stage 3: RANK AND PRESENT

Read the agent definition from `agents/paper-writer.md` in the skill directory.

Search the vault for existing paper notes on this topic using the MCP tool:
```
search_notes(query="KEYWORD", limit=20)
```
Or fall back to Grep if MCP is unavailable:
```
Grep(pattern="KEYWORD", path="notes/", glob="*.md", head_limit=20)
```

Launch the paper-writer agent to rank and present:

```
Agent(
  subagent_type="general-purpose",
  model="sonnet",
  run_in_background=false,
  prompt="You are Paper Writer. Follow these instructions exactly:

  [INSERT FULL CONTENT OF agents/paper-writer.md HERE]

  SEARCH CONTEXT:
  - User query: [original query]
  - Search mode: [topic/similar/gap]
  - Vault topics: [detected from search/tags]

  EXISTING VAULT PAPERS:
  [List any matching paper notes already in the vault]

  SEARCH RESULTS:
  [INSERT JSON FROM STAGE 2 HERE]

  Rank these papers by relevance to the vault's existing knowledge.
  Present the top 10 with your assessment. Do NOT create notes yet —
  just present the ranked list for user triage."
)
```

## Stage 4: CREATE NOTES (on user approval)

After user selects which papers to add:

For each selected paper, create a vault note:
1. Generate timestamp ID: `date +%Y%m%d%H%M%S`
2. Create the note file with proper frontmatter and body
3. Check for duplicate titles before creating

Note template:
```markdown
---
id: YYYYMMDDHHMMSS
created_date: YYYY-MM-DD
updated_date: YYYY-MM-DD
type: paper
category:
link: [paper URL]
processing_status: inbox
---

# Title
- **🏷️Tags** : #paper #topic-tag #MM-YYYY

[ ](#anki-card)

## Abstract
- [Synthesized abstract bullets]

## Notes

## Questions

## Related links
- [Paper URL](url)
- [[(Type) Related Vault Note]]
```

Place the note in `notes/paper/` (or appropriate topic folder).

</Steps>

<Tool_Usage>
- **Bash**: Run search_papers.py script, generate timestamps
- **Read**: Read agent definition, read existing vault notes for context
- **Write/Edit**: Create paper notes in vault
- **Agent**: Delegate ranking/presentation to paper-writer (sonnet)
- **Grep/Glob**: Search vault for existing papers and related notes
- **TodoWrite**: Track progress through stages
</Tool_Usage>

<Examples>
<Good>
User: "find papers about scaling laws for neural networks"
1. Search → 20 results from Semantic Scholar
2. Check vault → found 3 existing scaling law papers
3. Agent ranks → filters to 8 new papers, ranked by vault relevance
4. Present: "Found 8 papers you don't have. Top pick: 'Chinchilla' (2022,
   4200 citations) — connects to your [[Scaling Laws]] and [[Compute-Optimal Training]]"
5. User picks 3 → create 3 paper notes in notes/paper/ with inbox status
</Good>

<Good>
User: "what papers are related to this one?" (while viewing a paper note)
1. Read current note → extract title, DOI
2. Get recommendations via Semantic Scholar API
3. Check vault → filter out papers already present
4. Present ranked list with connections to existing notes
</Good>

<Bad>
User: "find papers about ML"
- Too broad — should ask: "ML is a wide field. What aspect? Scaling laws,
  reinforcement learning, attention mechanisms, optimization...?"
</Bad>
</Examples>

<Escalation_And_Stop_Conditions>
- **No results**: Try broader query, suggest alternative terms
- **API rate limited**: Wait and retry (script handles this automatically)
- **Query too broad**: Ask user to narrow down the topic
- **All results already in vault**: Report "your vault already covers this well"
- **Network error**: Inform user, suggest trying again later
</Escalation_And_Stop_Conditions>

$ARGUMENTS
