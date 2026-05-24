---
name: vault-graph
description: >-
  Use when analyzing vault structure, finding orphan notes, discovering missing
  connections, identifying bridge concepts, or checking vault health from a
  graph perspective. Triggers on "vault graph", "map vault", "find orphans",
  "missing links", "vault structure", "knowledge graph".
allowed-tools: Bash, Read, Agent, TodoWrite, Grep, Glob
---

<Purpose>
Analyze the vault's wikilink structure as a directed graph. Computes PageRank
(most influential concepts), betweenness centrality (bridge nodes connecting
domains), orphan detection, cluster analysis, and missing-link discovery.
Combines deterministic graph computation (Python/NetworkX) with intelligent
interpretation (agent) to surface actionable insights.
</Purpose>

<Use_When>
- User asks about vault structure, connections, or health
- User wants to find orphan notes (unlinked, isolated)
- User wants to discover missing connections between notes
- User wants to identify the most important concepts in the vault
- User asks "what should I link?" or "what's disconnected?"
- As part of /health workflow for structural metrics
- User says "map", "graph", "network", "connections", "orphans", "bridges"
</Use_When>

<Do_Not_Use_When>
- User wants to search note CONTENT (use Grep/search_notes instead)
- User wants to process a single note (use /process)
- User wants tag analysis without graph structure (use /health)
</Do_Not_Use_When>

<Execution_Policy>
- Run the Python script first — it handles all graph math deterministically
- Pipe script output to the graph-analyst agent for interpretation
- Report progress via TodoWrite
- If uv is not installed, provide install command and stop
- Script runs on the full vault — no sampling needed (handles 5000+ notes)
</Execution_Policy>

<Steps>

## Stage 1: RUN GRAPH ANALYSIS

Run the analysis script from the skill directory:

```bash
SKILL_DIR="${CLAUDE_SKILL_DIR}"
uv run "$SKILL_DIR/scripts/analyze_vault_graph.py" "." --top 20
```

The script outputs JSON to stdout with:
- `summary`: total notes, edges, orphans, density, clustering coefficient
- `top_pagerank`: most influential notes
- `top_betweenness`: bridge concepts connecting clusters
- `top_in_degree`: most referenced notes
- `top_out_degree`: most connecting notes
- `orphans`: notes with zero links in/out
- `dead_ends`: notes referenced but linking nowhere
- `clusters`: connected components with dominant types
- `missing_links`: wikilinks pointing to non-existent notes
- `type_distribution`: counts by note type
- `status_distribution`: counts by processing status

Requires `uv` installed (`brew install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`). Dependencies auto-install on first run.

## Stage 2: INTERPRET WITH AGENT

Read the agent definition from `agents/graph-analyst.md` in the skill directory.

Launch the analyst agent:

```
Agent(
  subagent_type="general-purpose",
  model="sonnet",
  run_in_background=false,
  prompt="You are Graph Analyst. Follow these instructions exactly:

  [INSERT FULL CONTENT OF agents/graph-analyst.md HERE]

  VAULT CONTEXT:
  - This is a Zettelkasten-style Obsidian vault
  - Note types: term (atomic concepts), thought (original synthesis),
    paper/post/book (sources), note (explanations), decision-log
  - Tags are inline (#topic), not frontmatter
  - Cross-domain connections are the vault's highest-value links

  GRAPH ANALYSIS RESULTS:
  [INSERT JSON OUTPUT FROM STAGE 1 HERE]

  Produce your analysis following the Output Format specified above."
)
```

## Stage 3: PRESENT RESULTS

Present the agent's analysis to the user. Include:
1. The health score and top findings
2. Specific bridge concepts and orphans
3. Missing notes worth creating
4. Suggested new connections

If the user wants to ACT on suggestions (create notes, add links), help them
do so using standard vault tools (Edit, write_note, etc.).

</Steps>

<Tool_Usage>
- **Bash**: Run analyze_vault_graph.py script
- **Read**: Read agent definition from agents/graph-analyst.md
- **Agent**: Delegate interpretation to graph-analyst (sonnet)
- **TodoWrite**: Report progress at each stage
- **Grep/Glob**: Follow-up searches if user wants to explore specific findings
</Tool_Usage>

<Examples>
<Good>
User: "Show me my vault's knowledge graph health"
1. Run script → JSON with 847 notes, 2341 edges, 43 orphans
2. Agent interprets → "Your ML cluster is dense but isolated from psychology.
   [[Reinforcement Learning]] and [[Operant Conditioning]] both describe
   reward-based behavior but aren't linked."
3. Present: 5 findings, 8 bridge suggestions, 12 orphans worth connecting
</Good>

<Good>
User: "Find orphan notes"
1. Run script → 43 orphans identified
2. Agent filters → 15 are legitimately standalone (daily notes, clippings),
   28 should be connected
3. Present prioritized list: "[[Loss Aversion]] is a term note with zero
   links — should connect to [[Prospect Theory]] and [[Pricing Psychology]]"
</Good>

<Bad>
User: "Map my vault"
- Dumps raw JSON metrics without interpretation
- Should: Run agent to explain what the numbers MEAN
</Bad>
</Examples>

<Escalation_And_Stop_Conditions>
- **uv not installed**: Print install command (`brew install uv`), stop
- **Vault too small** (<10 notes): Warn that graph analysis needs mass to be useful
- **Script error**: Report error, don't proceed to interpretation
</Escalation_And_Stop_Conditions>

$ARGUMENTS
