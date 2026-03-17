---
name: decision-graph
description: Use when building a deciduous decision graph to capture design evolution, architecture history, or how a codebase's design changed over time. Provides the deciduous CLI commands and graph structure guidelines.
---

# Decision Graph Construction

You are building a **deciduous decision graph** - a DAG that captures the evolution of design decisions in a codebase.

Use the `deciduous` CLI (at ~/.cargo/bin/deciduous) to build the graph. Run deciduous commands in the current directory (not inside the source repo).

For git commands to explore commit history, use `git -C <repo-path>` to target the source repo.

**CRITICAL: Only use information from the repository itself (commits, code, comments, tests). Do not use your prior knowledge about the project. Everything must be grounded in what you find in the repo.**

## Commit Exploration

Use a layered strategy to find all relevant commits:

**Layer 1: See all commits.** Start with the full list when building narratives.

```bash
git log --oneline --after="..." --before="..." -- path/
```

**Layer 2: Keyword expansion.** Once you have narratives, search for spelling variations and related terms you might have missed (e.g., "cache" → "caching", "cached", "LRU", "invalidate"). For each key identifier in your narratives, trace its full lifecycle:

- Introduction
- Changes and modifications
- Renames
- Deprecation or removal
- Replacement by other mechanisms
- Becoming stable/public API

If there's a feature flag controlling the feature, search for commits mentioning that flag.

**Layer 3: Follow authors.** If a narrative has a key author, check their commits ±1 month from known commits. They often work on related things.

### DO NOT:

- `git log ... | head -100` — **NO.** You will miss commits in the middle.
- `git log ... | tail -200` — **NO.** Same problem.
- Start with keyword filtering — **NO.** You'll miss things with unexpected names.

### DO:

- See all commits first, filter mentally while building narratives
- Include "remove", "delete", "disable", "deprecate" in keyword searches — removals explain transitions
- Check the commit count first (`| wc -l`), but then see them all
- **Read full commit messages** for any commit whose title mentions an identifier or concept relevant to your narrative — you need precise understanding of what happened to each one you care about

## Finding the Story

Not every commit matters. Look for commits that change **the model** - how the system conceptualizes the problem:

- Existing tests modified (contract changing, not just bugs fixed)
- Data structures replaced or reworked
- Heuristics changed significantly
- New abstractions introduced
- API behavior shifts

Skip commits that are pure implementation (same model, different code) or routine fixes that just add tests.

Among model-changing commits, find the **spine**: what question keeps getting re-answered? What approach keeps getting replaced or refined? That's your central thread - build the graph around it.

## Narrative Tracking

**Don't build the graph as you explore.** First, collect commits into narratives.

Maintain `narratives.md` as you explore:

1. For each significant commit, read `narratives.md`
2. Ask: "Does this commit evolve an existing narrative?"
3. If yes: append the commit to that narrative's section
4. If no: add a new narrative section

Example `narratives.md`:

```
## Cache Strategy

**Arc:** The service initially hit the database on every request, which worked until traffic spiked and the DB became the bottleneck. An in-memory cache solved the latency problem but created a new one: each server instance had its own cache, so users saw inconsistent data depending on which instance handled their request. The team tried cache invalidation broadcasts, but the complexity exploded. Moving to Redis gave a single source of truth at the cost of network latency - but that latency was still 10x better than the DB, and consistency issues disappeared.

- a1b2c3d: Add in-memory cache
- e4f5g6h: Cache invalidation issues
- i7j8k9l: Switch to Redis

## API Rate Limiting

**Arc:** The API originally had no rate limits, which was fine until a misbehaving client brought down the service with a retry loop. The initial fix was simple per-IP throttling, but this broke legitimate use cases like corporate NATs where thousands of users share one IP. The insight was distinguishing between "sustained abuse" and "burst traffic" - a token bucket algorithm lets clients burst up to a limit while still preventing sustained overload. The final refinement added per-endpoint limits after discovering that the /search endpoint was 100x more expensive than others.

- m1n2o3p: Add basic throttling
- ...
```

The **Arc** tells the narrative as a story: what problem started it, what was tried, what went wrong, what insight emerged, and where it ended up. If your arc has gaps ("then somehow we ended up with X"), you're missing commits.

**Before building the graph**, take a critical pass over `narratives.md`:

- Merge narratives that are essentially the same evolving thing
- Ensure each narrative clearly explains how one independent piece evolved
- Note where narratives branch from or feed into each other

## Hardening Phase

After building initial narratives, harden them to ensure nothing is missed.

**Assume the commit list is incomplete.** Your first pass probably missed things. Before synthesizing the narrative into a graph, actively search for what's missing. If a commit mentions a new term or concept you hadn't searched for, search for that too. Follow the trail until searches stop turning up new relevant commits.

### Step 1: Extract concepts per narrative

For each narrative, list the key concepts/APIs/identifiers and their lifecycle stage:

- **Introduced**: First appearance of the concept
- **Changed**: Modifications to behavior or implementation
- **Renamed/Deprecated/Removed**: End of life or replacement
- **Marked stable**: Became public API or removed "unstable\_" prefix

Example addition to narrative:

```
## Cache Strategy
Concepts: cache, LRUCache, cacheTimeout, invalidate

Lifecycle:
- cache: introduced (a1b2c3d), changed (e4f5g6h), renamed to LRUCache (x1y2z3)
- cacheTimeout: introduced (e4f5g6h), removed (i7j8k9l)
- LRUCache: introduced via rename (x1y2z3), marked stable (p1q2r3)

Commits:
- a1b2c3d: Add in-memory cache
- ...
```

### Step 2: Exhaustive search per concept

For each concept, search full commit messages (not just subject lines):

```bash
git log --all --after="..." --before="..." --grep="<concept>" --format="%H %s" -- path/
```

For each match, read the full commit message:

```bash
git show <sha> --format="%B" --no-patch
```

### Step 3: Follow replacements

When something is removed or deprecated, **trace what replaced it**. The replacement mechanism is its own concept that needs lifecycle tracking.

Example: If you find "Remove ManualCache in favor of AutoCache", then:

1. Add `AutoCache` to your concepts list
2. Search for all commits mentioning `AutoCache`
3. Track its full lifecycle (introduced, changed, etc.)

Replacements often represent a distinct design phase. Don't collapse "X removed, Y introduced" into a single node - model Y's introduction and evolution as its own chain.

### Step 4: Rewrite narratives with gaps filled

Rewrite `narratives.md` integrating any newly discovered commits. The rewritten version should:

- Include ALL commits found for each concept
- Include replacement mechanisms as first-class concepts
- Update the lifecycle tracking for each concept
- Ensure the arc is complete (if something was introduced, when was it changed/removed?)

If a concept has an incomplete arc (e.g., introduced but never removed, yet it's not in current code), investigate further.

## Cross-Narrative Connections

When building the graph, capture how narratives relate - but **only connect things that are causally related**.

### The Causality Test

Before connecting A → B, ask: **Would B have happened anyway if A hadn't existed?**

- **Yes, B would happen anyway** → They're parallel concerns. Both branch from their common parent (often the goal).
- **No, B only exists because of A** → Sequential. A leads_to B.

Examples:

```
# WRONG - these are parallel concerns, not causal
outcome: "Improved fallback display heuristics"
    → observation: "Developers need more control over timing"

# Why wrong? Developers wanting control isn't CAUSED BY the heuristics improvement.
# They're both responses to the same parent goal.

# RIGHT - branch both from the goal
goal: "Make Suspense fallback behavior good"
    → decision: "How to improve heuristics?"
    → decision: "How to give developers control?"
```

```
# RIGHT - actually causal
outcome: "Timeout mechanism works"
    → observation: "But it deletes children, losing state"
    → decision: "How to preserve state?"

# Why right? The state preservation question AROSE FROM implementing timeout.
# They wouldn't be asking this if timeout hadn't been built first.
```

### Types of Causal Connections

**Prerequisite:** B literally couldn't exist without A. B extends, refines, or builds on A.

- Connect: outcome(A) → decision(B)
- Example: "Add cache eviction policies" requires the cache to exist first
- Example: "Optimize query batching" requires the query layer to exist first
- This is the most common causal connection - features building on features

**Caused problem:** A working revealed a new problem that B addresses.

- Connect: outcome(A) → observation("problem") → decision(B)
- Example: Cache works → but causes stale reads → how to invalidate?

**Made obsolete:** A's success made B unnecessary.

- Connect: outcome(A) → observation("B no longer needed")
- Example: Auto-scaling works → observation: manual capacity planning no longer needed

**Informed by:** Learning from A directly shaped how B was designed.

- Connect: observation(from A) → decision(B)
- Example: Observation about user behavior from A informed the API design of B

### NOT Causal (Keep Parallel)

**Same timeframe:** A and B happened around the same time, but neither caused the other.

- Both branch from common parent.

**Same area:** A and B both touch the same code, but are independent concerns.

- Both branch from common parent.

**Same author:** Same person worked on both, but they're separate problems.

- Both branch from common parent.

### Before Building the Graph

List cross-narrative connections explicitly, but **only include causal ones**:

```markdown
## Cross-Narrative Connections

**Causal connections:**

- Narrative B branched from Narrative A's outcome because [specific reason]
- Observation X from Narrative A informed Decision Y in Narrative B because [specific reason]

**Parallel concerns (no connection needed):**

- Narratives C and D both address [goal] but don't causally relate
```

If you can't articulate WHY one caused the other, they're probably parallel.

## Node Types

| Type            | Purpose                                               |
| --------------- | ----------------------------------------------------- |
| **goal**        | High-level objective being pursued                    |
| **decision**    | A choice point with multiple possible paths           |
| **option**      | A possible approach to a decision                     |
| **observation** | Learning, insight, or new information discovered      |
| **action**      | Something that was done (must reference a commit)     |
| **outcome**     | Result or consequence of an action                    |
| **revisit**     | Pivot point where a previous approach is reconsidered |

## CLI Commands

```bash
# Add nodes (returns node ID)
deciduous add goal "Title of the goal"
deciduous add decision "The question or choice point"
deciduous add option "One possible approach"
deciduous add observation "Something learned or discovered"
deciduous add action "Descriptive title of what was done"
deciduous add outcome "What resulted from the action"
deciduous add revisit "Reconsidering previous approach"

# Add nodes with descriptions (use -d for explanations and sources)
deciduous add action "Title" -d "Explanation of what happened and why.

Sources:
- abc123: 'Relevant quote from commit message'"

# Set status on options
deciduous status <id> rejected    # option that wasn't chosen
deciduous status <id> completed   # option that was chosen

# Connect nodes (from → to means "from leads_to to")
deciduous link <from-id> <to-id>
deciduous link <from-id> <to-id> -r "Why this led to that"

# View/restructure
deciduous nodes           # list all
deciduous edges           # list connections
deciduous unlink <from> <to>   # remove edge
deciduous delete <id>          # remove node and edges
```

## Narrative Discipline

You're not collecting facts - you're crafting a story. Every node needs a _raison d'être_.

Before adding a node, stop and ask: **Why does this exist? What prompted it?**

- Is this commit evolving something that's already in the graph? Then connect it there - it's a continuation, not a new branch.
- Is this a response to an observation about existing work? Then chain from that observation - something was learned, and this is the reaction.
- Did the winds change? Look for the moment the team realized the old approach wasn't working. That's an observation node, and it's the bridge to what came next.

**Don't branch from the goal unless it's genuinely new.** If you're about to draw an edge from the root goal, ask: does this replace or refine something we already designed? If yes, find that thing and connect there instead.

The test: can someone read your graph and understand not just _what_ happened, but _why_ each thing happened? Every node should feel inevitable given what came before it.

Think of commits as chapters in a story. Each chapter exists because of what happened in previous chapters. Your job is to find those causal threads and make them explicit.

## Temporal Rule

**Time flows forward. Past influences future, never reverse.**

Options under a decision are alternatives considered _at the same time_. If an approach was tried, failed, and a new approach was designed later - that's a **new decision node**, connected by observations about why the old approach failed.

Example - DON'T model sequential attempts as parallel options:

```
# WRONG - these were decided years apart, not simultaneously
decision: "How to handle caching?"
  ├→ option: in-memory cache (2019)
  ├→ option: Redis (2020)
  └→ option: CDN (2021)
```

Example - DO model as chain of decisions with learning:

```
# RIGHT - each attempt informs the next, options are simultaneous alternatives
decision: "How to handle caching?" (2019)
  ├→ option: in-memory cache [chosen]
  └→ option: no caching [rejected] "Perf requirements too strict"
        ↓
option: in-memory cache → action → outcome
        ↓
observation: "Doesn't scale across instances"
        ↓
decision: "How to share cache across instances?" (2020)
  ├→ option: Redis [chosen] "Team has Redis experience"
  ├→ option: Memcached [rejected] "Less feature-rich"
  └→ option: database caching [rejected] "Adds DB load"
        ↓
option: Redis → action → outcome
        ↓
observation: "Latency too high for hot paths"
        ↓
decision: "How to reduce latency for static assets?" (2021)
  └→ option: CDN [chosen]
```

Multiple observations can converge into one decision. Multiple options can branch from one decision. But the graph flows forward in time.

## Edge Types

Use specific edge types to show relationships:

```bash
deciduous link <from> <to> -t chosen -r "Why this was selected"
deciduous link <from> <to> -t rejected -r "Why this wasn't selected"
deciduous link <from> <to> -t leads_to -r "How this led to that"
```

- `decision --chosen--> option` - This option was selected
- `decision --rejected--> option` - This option was considered but not selected (with rationale)
- `decision --leads_to--> option` - Lists available options

For post-hoc abandonment (tried something, it failed later):

- Mark the option status as `rejected`: `deciduous status <id> rejected`
- Create an observation explaining why it failed
- Link observation to the new decision it triggered

## Link Patterns

- `goal → decision` - Goal leads to choice point
- `decision → option` - Decision has options (use chosen/rejected edge types)
- `option → action` - Chosen option leads to implementation
- `action → outcome` - Action produces result
- `outcome → observation` - Result reveals new insight
- `observation → decision` - Insight triggers new choice (can have multiple observations converging)
- `observation → revisit` - Insight forces reconsideration of previous approach
- `revisit → decision` - Pivot leads to new choice point

When a design approach is abandoned and replaced:

```bash
deciduous add observation "JWT too large for mobile"
deciduous add revisit "Reconsidering token strategy"
deciduous link <observation> <revisit> -r "forced rethinking"
deciduous status <old_decision> superseded
```

Revisit nodes connect old approaches to new ones, capturing WHY things changed.

## Grounding Requirements

1. **Actions must cite commits**: Every action node must reference a real commit SHA in its description. Use `-d` when adding the node.

2. **Observations from evidence**: Observations should come from commit messages, code comments, or test descriptions you find in the repo.

3. **No speculation**: If you can't find evidence for something in the repo, don't include it. An incomplete but grounded graph is better than a complete but speculative one.

4. **Quote sources**: When possible, quote or paraphrase the actual commit message or comment that supports a node.

## Rich Node Content

The graph is an **alternative interface to browsing commit history**. Someone reading a node should understand what happened without looking up commits.

**Every node needs a description** - especially outcome and observation nodes. The description should be readable to someone exploring the graph who doesn't have the commits open.

### Structure: Explanation first, then sources

1. **Start with a readable explanation** that makes sense within the narrative. What happened? Why? How does it connect to what came before?
2. **Add sources below** with direct quotes from commits that support the explanation.

If you find your explanation doesn't make sense in context - something feels like a leap or a gap - that's a signal to dig deeper. There's probably a missing commit or transition you haven't found yet.

The relationship is many-to-many:

- One node may reference multiple commits (a decision informed by several changes)
- One commit may appear in multiple nodes (a large commit touching several concerns)

### Example

```bash
deciduous add decision "Should we switch from SQL to a document store?" -d "The team decided to switch from SQL to a document store.
This eliminated the impedance mismatch between the object model and storage,
at the cost of losing ad-hoc query capability (which wasn't being used anyway).

Sources:
- a1b2c3d: 'Our access patterns are almost entirely key-value lookups. The
  JOIN operations we wrote are never actually used in production.'
- e4f5g6h: 'Document store removes the ORM layer entirely - one less thing
  to maintain and debug.'"
```

### BAD - Quote-heavy, hard to read:

```
Sources:
- abc123: 'Redis gives us shared state across instances.'
- def456: 'In-memory cache doesn't work when we scale horizontally.'

This allows distributed caching.
```

### GOOD - Explanation first, quotes support:

```
The in-memory cache worked well for a single server, but broke down when
the team scaled to multiple instances - each had its own cache, leading to
inconsistencies. Redis provided a shared cache that all instances could use,
solving the consistency problem at the cost of added latency.

Sources:
- abc123: 'Redis gives us shared state across instances.'
- def456: 'In-memory cache doesn't work when we scale horizontally.'
```

### DO NOT:

- Leave nodes with just a title and no description
- Put quotes/sources first - the explanation must come first
- Write explanations that don't make sense in the narrative flow (this signals missing context)
- Just paraphrase the quotes - add insight about WHY and HOW it connects

### DO:

- Write 2-4 sentence explanations that flow from the previous node
- Explain the problem being solved, not just what was done
- Include direct quotes that support (not replace) the explanation
- Treat gaps in the story as prompts to investigate further

## Output

When done, run `deciduous graph > graph.json` to export.
