---
name: bookstrap-research
description: Execute research tasks autonomously by searching for sources, evaluating reliability, ingesting content, and resolving knowledge gaps
disable-model-invocation: true
allowed-tools: Bash, Read, Write, WebFetch, WebSearch, TaskGet, TaskUpdate
---

# /bookstrap-research - Execute Research Tasks

Execute research tasks autonomously to fill knowledge gaps identified during planning. Search the web for sources, evaluate their reliability, ingest relevant content, extract entities and relationships, and mark gaps as resolved.

## Purpose

Fill knowledge gaps by conducting autonomous web research. This command loads pending research tasks from the database, searches for high-quality sources, ingests them into the corpus, and resolves the associated knowledge gaps.

This command delegates the research work to the `researcher` agent, which operates in research mode with full web access.

## Input Arguments

None. This command reads pending research tasks from the database:
- Unresolved knowledge gaps with their questions and context
- Priority levels (high, medium, low)
- Chapters/sections blocked by each gap
- Previous research attempts (if any)

## Processing Workflow

### 1. Load Pending Research Tasks

Query the database to retrieve unresolved knowledge gaps:

```bash
# Query pending research tasks
surreal sql --conn http://localhost:2665 \
  --user root --pass root \
  --ns bookstrap --db <database-name> \
  --query "SELECT * FROM knowledge_gap WHERE resolved = false ORDER BY priority DESC, created_at ASC;"
```

Filter and prioritize:
- High priority tasks first (blocking core content)
- Tasks with existing context from BRD
- Tasks with clear, actionable research questions
- Skip tasks with failed attempts beyond retry limit

### 2. For Each Research Task

Execute research tasks one at a time, committing progress after each successful ingestion.

#### 2.1 Web Search for Sources

Use configured search provider (Tavily, Brave, Serper, Google) to find relevant sources:

```bash
# Perform web search based on research question
# Apply domain filters from bookstrap.config.json
# Respect rate limits
# Target max_sources_per_task from config (default: 5)
```

Search strategy:
- Start with the exact research question
- Broaden search if too few results
- Narrow search if too many irrelevant results
- Look for multiple source types (academic, primary, journalism)

#### 2.2 Evaluate Source Reliability

For each search result, assess reliability:

| Source Type | Reliability | Use Case |
|-------------|-------------|----------|
| Academic/peer-reviewed journals | High | Factual claims, scholarly arguments |
| Primary sources (archives, documents) | High | Historical facts, original evidence |
| Reputable journalism (NYT, BBC, etc.) | Medium-High | Recent events, context |
| Government/institutional sites | Medium-High | Official data, statistics |
| Expert blogs/substacks | Medium | Opinion, analysis, niche expertise |
| Wikipedia | Low (for leads only) | Starting point, bibliography mining |
| Random blogs/forums | Very Low | Avoid unless unique perspective needed |

Check reliability indicators:
- Author credentials and affiliations
- Publication date (prefer recent for current topics)
- Citations and references provided
- Domain authority and reputation
- Fact-checking and editorial standards

#### 2.3 Ingest Relevant Content

For approved sources, ingest into the database:

```bash
# Use ingest-file.py for web content
python ./scripts/ingest-file.py \
  --url <source-url> \
  --source-type <primary|secondary|web> \
  --reliability <high|medium|low> \
  --context "ingested_during:research" \
  --gap-id <knowledge-gap-id>
```

Ingestion performs:
1. **Fetch content**: Download and extract text
2. **Semantic chunking**: LLM identifies natural breakpoints
3. **Generate embeddings**: Via configured provider
4. **Extract entities**: Characters, locations, events, concepts, dates
5. **Auto-create relationships**: Build graph edges
6. **Update timeline**: Order events chronologically
7. **Link to knowledge gap**: Track which gap this resolves

#### 2.4 Extract Entities and Relationships

The ingestion script uses `extract-entities.py` with LLM-based extraction:

```bash
# Extract entities from ingested content
python ./scripts/extract-entities.py \
  --source-id <source-id> \
  --content <chunk-content> \
  --context <surrounding-context>
```

Extracts:
- **Characters/People**: Names, roles, descriptions, relationships
- **Locations**: Places, settings, geographic details
- **Events**: Occurrences, actions, dates, sequences
- **Concepts**: Ideas, theories, terminology, themes
- **Dates/Times**: Temporal markers for timeline

Creates relationships:
```surql
-- Link source to extracted entities
RELATE source:<id>->supports->concept:<id>;
RELATE event:<id>->precedes->event:<next-id>;
RELATE character:<id>->knows->character:<other-id>;
RELATE location:<id>->contains->location:<sub-id>;
```

#### 2.5 Mark Knowledge Gap Resolved

After successful ingestion, update the knowledge gap:

```surql
UPDATE knowledge_gap:<gap-id> SET
  resolved = true,
  resolved_by = source:<source-id>,
  resolved_at = time::now()
;
```

#### 2.6 Commit Progress

After each successfully resolved gap:

```bash
git add .
git commit -m "[bookstrap] Research: Resolved gap '<gap-question>' with <N> sources

Sources ingested:
- <source-1-title> (<reliability>)
- <source-2-title> (<reliability>)
...

Entities extracted: <count>
Relationships created: <count>

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### 3. Delegate to Researcher Agent

Invoke the `researcher` agent to perform the detailed research work:

```bash
# Load researcher agent with context
# Agent will:
# 1. Load next pending research task
# 2. Search web for sources
# 3. Evaluate source reliability
# 4. Ingest approved sources
# 5. Extract entities and relationships
# 6. Mark gap resolved
# 7. Commit progress
# 8. Continue to next task or exit if blocked
```

The researcher agent has read+write database access, web search capabilities, and uses the `research` and `surrealdb` skills.

### 4. Continue Until Complete or Blocked

The researcher agent continues processing tasks until:
- **All tasks complete**: All knowledge gaps resolved
- **Rate limited**: Search API rate limit reached (pause and resume)
- **No results found**: Research question too specific or unavailable
- **Quality threshold not met**: No sources meet reliability criteria
- **Manual intervention needed**: Gap requires human expertise or access

## Output Format

Report research progress to the user:

```
RESEARCH EXECUTION
==================

Configuration:
- Search provider: Tavily
- Max sources per task: 5
- Rate limit: 10 requests/min
- Database: bookstrap/my_book

TASK 1/12: High Priority
-------------------------
Question: "SOE wireless operator training protocols 1942-1943"
Context: Core to protagonist's role, zero sources
Blocks: Chapters 2, 4, 6

Web search: 15 results found
Evaluating sources...
  ✓ [HIGH] "SOE Training at Beaulieu" - Historical Society Journal
  ✓ [HIGH] "Wireless Operator Manual 1943" - National Archives
  ✓ [MEDIUM] "Special Operations Executive Training" - Imperial War Museum
  ✗ [LOW] Wikipedia article (using for bibliography only)

Ingesting 3 sources...
  → Source 1: 2,340 words, 4 chunks, 15 entities extracted
  → Source 2: 1,850 words, 3 chunks, 8 entities extracted
  → Source 3: 3,120 words, 5 chunks, 12 entities extracted

Entities extracted:
  - Characters: 5 (trainers, notable agents)
  - Locations: 3 (Beaulieu, training facilities)
  - Events: 12 (training procedures, protocols)
  - Concepts: 10 (wireless techniques, codes)
  - Dates: 8 (timeline entries)

Relationships created: 24 graph edges

Gap resolved ✓
Committed: [abc1234]

---

TASK 2/12: High Priority
-------------------------
Question: "Lyon Resistance network structure and key figures"
Context: Primary setting, only 2 tangential sources
Blocks: Chapters 3, 5, 7

Web search: 22 results found
Evaluating sources...
  ✓ [HIGH] "Combat: Resistance Movements in Lyon" - French Archives
  ✓ [MEDIUM] "The Lyon Resistance 1940-1944" - BBC History
  ✓ [MEDIUM] "Jean Moulin and Lyon Networks" - Resistance Museum
  ✗ [LOW] Blog post (insufficient citations)

Ingesting 3 sources...
[...]

---

PROGRESS SUMMARY
================

Tasks completed: 2/12
Tasks remaining: 10 (8 high priority, 2 medium priority)
Sources ingested: 6
Entities extracted: 35
Relationships created: 48
Knowledge gaps resolved: 2
Commits: 2

Time elapsed: 8 minutes
Rate limit status: 18/60 requests used this hour

NEXT STEPS
----------
Continue research: /bookstrap-research (auto-resumes)
Check progress: /bookstrap-status
View corpus: /bookstrap-query "What sources do we have about wireless training?"
```

## Behavior Characteristics

### Research Mode (Web Access Enabled)

This command operates in **research mode**:
- ✓ Can access web via search APIs
- ✓ Can fetch external URLs
- ✓ Fills gaps in corpus
- ✓ Exploratory and messy (casts wide net)
- ✓ Commits after each successful ingestion
- ✗ Does NOT write manuscript content
- ✗ Does NOT access during write mode

### Autonomous Execution

Runs fully autonomously:
- No human approval needed per source (uses reliability rubric)
- Processes tasks sequentially (easier to debug and resume)
- Commits atomic progress (recoverable if interrupted)
- Respects rate limits (pauses and resumes)
- Logs all decisions (source acceptance/rejection reasons)

### Quality Over Quantity

Prioritizes source quality:
- Better to skip a gap than ingest poor sources
- Prefers fewer high-quality sources over many weak ones
- Flags gaps as "needs human review" if no quality sources found
- Logs rejected sources with reasons for transparency

## Rate Limiting and Resumption

Handles rate limits gracefully:

```json
{
  "research": {
    "provider": "tavily",
    "rate_limit": {
      "requests_per_minute": 10,
      "retry_after_seconds": 60,
      "max_retries": 3
    }
  }
}
```

If rate limited:
1. Log current progress
2. Wait for rate limit reset
3. Resume from next pending task
4. Continue until complete

Re-running `/bookstrap-research` after interruption:
- Skips already resolved gaps
- Resumes from next pending task
- Maintains priority order
- Idempotent (safe to run multiple times)

## Configuration

Research behavior configured in `bookstrap.config.json`:

```json
{
  "research": {
    "provider": "tavily",
    "api_key_env": "TAVILY_API_KEY",
    "rate_limit": {
      "requests_per_minute": 10
    },
    "blocked_domains": ["example-spam-site.com"],
    "allowed_domains": [],
    "max_sources_per_task": 5,
    "min_reliability": "medium",
    "auto_commit": true,
    "max_retries_per_task": 3
  }
}
```

Settings:
- `provider`: Search API (tavily, brave, serper, google)
- `max_sources_per_task`: Limit sources per research question (prevents over-research)
- `min_reliability`: Minimum acceptable source quality (low, medium, high)
- `blocked_domains`: Never fetch from these domains
- `allowed_domains`: If set, only fetch from these domains
- `auto_commit`: Commit after each gap resolved (recommended)
- `max_retries_per_task`: Abandon task after N failed attempts

## Error Handling

| Error | Recovery |
|-------|----------|
| Search API unavailable | Skip to next task, flag for manual research |
| Rate limit exceeded | Pause, wait for reset, resume |
| No sources found | Flag gap as "no sources available", continue |
| All sources rejected (low quality) | Flag gap as "needs human review", continue |
| Ingestion failure | Log error, skip source, try next source |
| Database write failure | Abort, report error, preserve uncommitted work |
| Network timeout | Retry up to max_retries, then skip |

## Pre-requisites

Before running `/bookstrap-research`:

1. **BRD created**: `/bookstrap-init` must have been run
2. **SurrealDB running**: Database must be accessible
3. **Research tasks generated**: `/bookstrap-plan-research` must have identified gaps
4. **Search API configured**: API key in environment, provider configured
5. **Embedding provider configured**: For ingesting new content

## Related Commands

- `/bookstrap-plan-research` - Generate research tasks (run this first)
- `/bookstrap-ingest` - Ingest user-provided sources (manual alternative)
- `/bookstrap-status` - Monitor research progress and gap resolution
- `/bookstrap-query` - Query ingested sources
- `/bookstrap-plan-write` - Generate writing tasks (run after research complete)

## Supporting Agents

| Agent | Role |
|-------|------|
| `researcher` | Executes web research, evaluates sources, ingests content |

## Supporting Skills

| Skill | Purpose |
|-------|---------|
| `research/` | Source evaluation, web search strategies, entity extraction patterns |
| `surrealdb/` | Database query patterns for gap tracking and entity storage |

## Supporting Scripts

| Script | Purpose |
|--------|---------|
| `ingest-file.py` | Ingest content from URLs or files |
| `generate-embedding.py` | Generate embeddings via configured provider |
| `extract-entities.py` | LLM-based entity extraction |
| `chunk.py` | Semantic chunking strategies |

## Example Usage

```bash
# After identifying gaps, execute research
/bookstrap-plan-research
/bookstrap-research

# Research interrupted? Resume where you left off
/bookstrap-research

# Check progress
/bookstrap-status

# Continue research if new gaps found during writing
/bookstrap-write
# (discovers gaps)
/bookstrap-plan-research
/bookstrap-research
/bookstrap-write
```

## Integration with Research Loop

This command is part of the research-write cycle:

```
init → ingest → plan-research → research
                     ↑              │
                     │              ▼
                     │         plan-write → write → edit
                     │              │
                     └──── gaps ────┘
```

When writing discovers knowledge gaps:
1. Writing task marks gap and continues to next task
2. User runs `/bookstrap-plan-research` to generate research tasks
3. User runs `/bookstrap-research` to fill gaps
4. User runs `/bookstrap-write` to resume writing (now unblocked)

## Statistics to Track

Calculate and report:
- Tasks completed vs. remaining
- Sources ingested per task (average)
- Entities extracted per source (average)
- Reliability distribution (high/medium/low sources)
- Time per task (estimate remaining time)
- Rate limit usage (requests per hour)
- Gaps flagged for human review
- Success rate (gaps resolved / gaps attempted)

## Logging

Detailed logging for transparency:

```
[2024-01-15 14:23:45] [RESEARCH] Task 1/12 started: "SOE wireless protocols"
[2024-01-15 14:23:47] [SEARCH] Query: "SOE wireless operator training 1942-1943"
[2024-01-15 14:23:49] [SEARCH] Found 15 results
[2024-01-15 14:23:50] [EVAL] Source 1: "SOE Training at Beaulieu" - HIGH (academic journal)
[2024-01-15 14:23:51] [EVAL] Source 2: "Wireless Manual 1943" - HIGH (primary source)
[2024-01-15 14:23:52] [EVAL] Source 3: "Random blog post" - REJECTED (insufficient citations)
[2024-01-15 14:23:55] [INGEST] Source 1: 2,340 words, 4 chunks, 15 entities
[2024-01-15 14:24:12] [INGEST] Source 2: 1,850 words, 3 chunks, 8 entities
[2024-01-15 14:24:28] [GRAPH] Created 24 relationships
[2024-01-15 14:24:30] [DB] Gap resolved: knowledge_gap:gap-001
[2024-01-15 14:24:32] [GIT] Committed: abc1234
[2024-01-15 14:24:33] [RESEARCH] Task 1/12 complete (8m 48s)
```

## Implementation Notes

### Agent Delegation

This command is a thin wrapper that:
1. Verifies database connection
2. Checks that research tasks exist
3. Loads research configuration
4. Invokes the `researcher` agent
5. Displays the agent's output
6. Reports final statistics

The actual research logic lives in the `researcher` agent to keep concerns separated.

### Idempotency

Re-running `/bookstrap-research` is safe:
- Only processes unresolved gaps
- Skips already-ingested sources (via URL deduplication)
- Maintains priority order
- Can be interrupted and resumed
- No duplicate ingestion

### Separation of Concerns

Research mode vs. Write mode:
- **Research mode**: Web access, fills gaps, commits per task
- **Write mode**: Database only, flags gaps, commits per section

This command operates exclusively in research mode and is never invoked during writing. Writing discovers gaps but never fills them.

## Advanced Features

### Bibliography Mining

When ingesting academic sources:
- Extract citations and references
- Add cited works to research queue
- Build citation graph
- Track source quality via citation chains

### Iterative Deepening

For complex topics:
1. First pass: Broad overview sources
2. Identify sub-topics needing depth
3. Second pass: Targeted deep dives
4. Mark topic as "exhausted" when no new info found

### Cross-referencing

Validate facts across sources:
- Flag contradictions between sources
- Prefer higher-reliability sources in conflicts
- Store conflicting claims for human review
- Track consensus vs. outlier claims

## Troubleshooting

### No sources found

```
Gap: "Obscure technical detail from 1943"
Status: No sources found after 3 searches
Action: Flagged for human review
```

Possible solutions:
- Rephrase research question
- Broaden search terms
- Accept lower reliability threshold
- Provide sources manually via `/bookstrap-ingest`

### All sources rejected

```
Gap: "Controversial historical claim"
Status: 8 sources found, all rejected (reliability too low)
Action: Flagged for human review
```

Possible solutions:
- Lower `min_reliability` threshold in config
- Manually review rejected sources
- Provide trusted sources via `/bookstrap-ingest`

### Rate limit exceeded

```
Status: Rate limit hit (60/60 requests this hour)
Action: Paused, resuming at 15:00
```

Automatic recovery:
- Wait for rate limit reset
- Resume processing
- No action needed

## Security Considerations

### Domain Filtering

Use `blocked_domains` to prevent fetching from:
- Known malware/phishing sites
- Misinformation sources
- Copyright-violating content farms
- Sites that violate robots.txt

### API Key Protection

Never log or display API keys:
- Read from environment variables only
- Don't commit to git
- Rotate keys periodically
- Use least-privilege API scopes

### Content Sanitization

Before ingesting web content:
- Strip JavaScript and active content
- Sanitize HTML to prevent injection
- Validate URLs before fetching
- Respect robots.txt and rate limits
