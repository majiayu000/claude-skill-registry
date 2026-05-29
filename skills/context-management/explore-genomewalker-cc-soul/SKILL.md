---
name: explore
description: RLM-style recursive memory exploration - dynamically navigate the memory graph
execution: inline
model: inherit
aliases: [deep-recall, rlm]
---

# Memory Exploration (RLM-style)

Instead of injecting top-k memories, explore the memory graph dynamically.

## How It Works

1. Start with a query
2. Get initial hints via `explore_recall`
3. Iteratively decide: peek, expand, follow neighbors, or answer
4. Accumulate relevant findings
5. Answer when sufficient context gathered

## Exploration Protocol

You have these primitives (via chitta RPC):

| Tool | Purpose | Token Cost |
|------|---------|------------|
| `explore_recall` | Semantic search, returns hints (id, title, score) | ~100 |
| `explore_peek` | Get 200-char summary of a memory | ~50 |
| `explore_expand` | Get full memory content | ~200-500 |
| `explore_neighbors` | Get triplet connections from a node | ~100 |

## Agent Loop

```
query = user's question
context = []
trace = []
max_iterations = 10

# Initial hints
hints = explore_recall(query, limit=5)
trace.append(("recall", query, hints))

for i in range(max_iterations):
    # Decide next action based on query + current context
    action = decide_action(query, context, hints)

    if action == "ANSWER":
        break
    elif action.startswith("PEEK"):
        id = extract_id(action)
        summary = explore_peek(id)
        context.append(summary)
        trace.append(("peek", id, summary))
    elif action.startswith("EXPAND"):
        id = extract_id(action)
        full = explore_expand(id)
        context.append(full)
        trace.append(("expand", id, len(full)))
    elif action.startswith("NEIGHBORS"):
        node = extract_node(action)
        neighbors = explore_neighbors(node)
        hints.extend(relevant_neighbors(neighbors))
        trace.append(("neighbors", node, len(neighbors)))
    elif action.startswith("RECALL"):
        new_query = extract_query(action)
        new_hints = explore_recall(new_query, limit=5)
        hints.extend(new_hints)
        trace.append(("recall", new_query, new_hints))

# Generate answer from accumulated context
answer = synthesize(query, context)
return answer, trace
```

## Decision Prompt

At each iteration, decide:

```
Query: {query}

Current context ({len(context)} items):
{format_context(context)}

Available hints:
{format_hints(hints)}

Recent trace:
{format_trace(trace[-3:])}

What should I explore next?
- PEEK(id) - get summary of a promising hint
- EXPAND(id) - get full content (use sparingly)
- NEIGHBORS(node) - explore triplet connections
- RECALL("query") - search for more hints
- ANSWER - I have enough context

Respond with just the action, e.g.: PEEK(00000000-0000-0000-0000-0000000001bd)
```

## When to Use

Use `/explore` instead of regular recall when:
- Memory store is large (>1000 memories)
- Query needs associative exploration
- Top-k might miss relevant context
- You want to understand the exploration path

## Execution

When user invokes `/explore <query>`:

1. **Initial recall**: Call `explore_recall` with the query
2. **Show hints**: Display the hints found
3. **Exploration loop** (max 10 iterations):
   - Based on hints and accumulated context, decide:
     - `PEEK(id)` if a hint looks promising but need more info
     - `EXPAND(id)` if confident this memory is highly relevant
     - `NEIGHBORS(node)` if you want to follow relationships
     - `RECALL("new query")` if you need different search terms
     - `ANSWER` if you have enough context
   - Execute the action using the chitta RPC tool
   - Add results to context
4. **Synthesize**: Generate answer from accumulated context
5. **Show trace**: Display exploration path (what was searched, peeked, expanded)

## Token Comparison

Show at the end:
- Tokens used in exploration: ~N (sum of all actions)
- Equivalent full_resonate: ~M (10 full memories)
- Savings: X%

## Example

```
User: /explore How does the daemon handle authentication?

Claude: Starting exploration for "How does the daemon handle authentication?"

[Step 1] explore_recall("daemon authentication")
  Found 5 hints:
  [45%] id:123 - [mcp] cc-soul socket connection
  [38%] id:456 - [wisdom] JSON-RPC protocol
  [32%] id:789 - Unix socket permissions
  ...

[Step 2] PEEK(123) - socket connection looks relevant
  Summary: "cc-soul daemon uses Unix socket at /tmp/chitta-*.sock..."

[Step 3] NEIGHBORS("daemon")
  Found: daemon → uses → json_rpc
         daemon → listens_on → unix_socket

[Step 4] EXPAND(456) - JSON-RPC protocol details needed
  Full content loaded (342 chars)

[Step 5] ANSWER - have enough context

=== Answer ===
The daemon uses Unix socket authentication via file permissions.
No explicit auth - relies on filesystem access control to /tmp/chitta-*.sock.

=== Exploration Trace ===
1. recall("daemon authentication") → 5 hints
2. peek(123) → 200 chars
3. neighbors("daemon") → 5 connections
4. expand(456) → 342 chars

Tokens: ~692 exploration vs ~1500 full_resonate (54% savings)
```

## RPC Commands

Use these chitta commands during exploration:

```bash
# Lightweight recall
chitta explore_recall --query "your search" --limit 5

# Peek at summary
chitta explore_peek --id "00000000-0000-0000-0000-000000000123"

# Full content
chitta explore_expand --id "00000000-0000-0000-0000-000000000123"

# Graph neighbors
chitta explore_neighbors --node "Mind" --direction both
```