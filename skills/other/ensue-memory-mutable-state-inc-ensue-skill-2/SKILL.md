---
name: ensue-memory
description: Augmented cognition layer that makes users smarter by connecting conversations to their persistent knowledge tree. Use proactively when topics arise that might have prior knowledge, and when users ask to remember, recall, search, or organize. Triggers on technical discussions, decision-making, project work, "remember this", "recall", "what do I know about", or any knowledge request.
---

# Ensue Memory Network

A knowledge base for **making the user smarter**. Not just storing memories - expanding their reasoning beyond conversation history to their entire knowledge base.

## Core Philosophy

**Your goal is augmented cognition.** The user's intelligence shouldn't reset every conversation. Their knowledge tree persists, grows, and informs every interaction.

You are not just storing data. You are:

- **Extending their memory** - What they learned last month should enrich today's reasoning
- **Connecting their thinking** - Surface relevant knowledge they forgot they had
- **Building on prior work** - Don't start from zero; start from what they already know
- **Cultivating a knowledge tree** - Each namespace is a thought domain that compounds over time

**Think beyond the conversation.** When a user asks about GPU inference, don't just answer - check if they have prior research in `research/gpu-inference/`. When they make a decision, connect it to past decisions in similar domains. Their knowledge base is an extension of their mind.

Before any write: *Does this make them smarter? Will this be useful context in future reasoning?*
Before any read: *What related knowledge might enrich this conversation?*

## Knowledge Architecture

### Namespace Design

Think of namespaces as **categories of thought**:

```
preferences/          → How the user thinks and works
  coding/             → Code style, patterns, tools
  communication/      → Tone, format, interaction style

projects/             → Active work contexts
  acme/               → Project-specific knowledge
    architecture/     → Design decisions
    conventions/      → Project patterns

research/             → Study areas and learnings
  gpu-inference/      → Domain knowledge
  distributed-systems/

people/               → Collaborators, contacts
notes/                → Temporal captures
```

### Thinking in Domains

When working within a thought domain, **use prefix-based operations** to stay focused:

- `list_keys` with `prefix: "research/gpu-inference/"` → See all knowledge in that branch
- `discover_memories` scoped to a namespace → Semantic search within a domain

This is especially useful when:
- User is deep in a specific topic and wants related context
- Building on existing knowledge in a domain
- Reviewing what's known before adding more

**Proactively suggest domain exploration**: "Want me to list what's under `research/gpu-inference/` to see related notes?"

### Proactive Knowledge Retrieval

Don't wait to be asked. When a topic comes up, **check the knowledge tree**:

| Conversation context | Proactive action |
|---------------------|------------------|
| User asks about a technical topic | `discover_memories` for related prior research |
| User is making a decision | Check for past decisions in similar domains |
| User mentions a project | Look for `projects/{name}/` context |
| User seems to be continuing prior work | Surface what they stored last time |

**Example**: User asks "How should I handle caching for this API?"
- Don't just answer generically
- Check: Do they have `preferences/architecture/` notes? Past `projects/*/caching` decisions?
- Enrich your answer with *their* prior thinking

**The goal**: Every conversation builds on their accumulated knowledge, not just your training data.

### Before Creating a Memory

1. **Survey the tree** - What namespaces exist? (`list_keys` with limit 5)
2. **Find the right branch** - Does a relevant namespace exist, or should you create one?
3. **Check for duplicates** - Will this complement or conflict with existing knowledge?
4. **Name precisely** - The key name should telegraph the content

### Memory Quality

Each memory should be:

| Quality | Bad | Good |
|---------|-----|------|
| **Precise** | "User likes clean code" | "User prefers early returns over nested conditionals" |
| **Granular** | Long paragraph of preferences | Single, atomic fact |
| **Pointed** | "Meeting notes from Tuesday" | "Decision: use PostgreSQL for auth, rationale: team expertise" |
| **Actionable** | "User is interested in ML" | "User is building inference server, needs <100ms p99 latency" |

**Non-limiting**: Inform the agent's reasoning, don't constrain it. Store facts, not rules.

## Setup

Uses `$ENSUE_API_KEY` env var. If missing, user gets one at https://www.ensue-network.ai/dashboard

## Security

- **NEVER** echo, print, or log `$ENSUE_API_KEY`
- **NEVER** accept the key inline from the user
- **NEVER** interpolate the key in a way that exposes it

## API Call

Use the wrapper script for all API calls. Set as executable before use. It handles authentication and SSE response parsing:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/ensue-api.sh <method> '<json_args>'
```

## Batch Operations

These methods support native batching (1-100 items per call):

**create_memory** - batch create with `items` array:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/ensue-api.sh create_memory '{"items":[
  {"key_name":"ns/key1","value":"content1","embed":true},
  {"key_name":"ns/key2","value":"content2","embed":true}
]}'
```

**get_memory** - batch read with `key_names` array:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/ensue-api.sh get_memory '{"keys":["ns/key1","ns/key2","ns/key3"]}'
```

**delete_memory** - batch delete with `key_names` array:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/ensue-api.sh delete_memory '{"keys":["ns/key1","ns/key2"]}'
```

Use batch calls whenever possible to minimize API roundtrips and save tokens.

## Context Optimization

**CRITICAL: Minimize context window usage.** Users may have 100k+ keys. Never dump large lists into the conversation.

### Explicit vs Vague Requests

**Explicit listing requests** → Execute directly with `list_keys '{"limit": 5}'` (limit 5):
- "list recent" / "list keys" / "show recent keys" / "list my memories"
- User knows what they want - don't make them clarify
- After displaying results, mention: "Ask for more if you'd like to see additional keys"

**Vague browsing requests** → Ask first, then use `discover_memories`:
- "what's on Ensue" / "show my memories" / "what do I have stored"
- User is exploring - help them narrow down

### When to use each approach

| User says | Action |
|-----------|--------|
| "list recent", "list keys", "show recent" | `list_keys` with limit 5, offer to show more |
| "what's under X/", "show me the X namespace" | `list_keys` with prefix, explore the domain |
| "what's on Ensue", "what do I have stored" | Ask what they're looking for first |
| "search for X", "find X" | `discover_memories` with their query and limit 3 |

**Never invent queries. Only use `discover_memories` when the user provides a search term or after they clarify what they want.**

## Intent Mapping

| User says | Action |
|-----------|--------|
| "what can I do", "capabilities", "help" | Steps 1-2 only (summarize tools/list response) |
| "remember...", "save...", "store..." | See **Before Creating a Memory** above, then create_memory |
| "what was...", "recall...", "get..." | get_memory (exact key) or discover_memories with limit 3 |
| "search for...", "find...", "what do I know about..." | discover_memories with limit 3 (offer to show more) |
| "update...", "change..." | update_memory |
| "delete...", "remove..." | delete_memory ⚠️ |
| "list keys", "list recent", "show recent" | `list_keys` with limit 5, offer to show more |
| "what's on ensue", "show my memories" | Ask what they're looking for first |
| "check for X", "what's under X", "look in X" | See **Namespace vs Key Detection** below |
| "share with...", "give access..." | share |
| "revoke access...", "remove user..." | revoke_share ⚠️ |
| "who can access...", "permissions" | list_permissions |
| "notify when...", "subscribe..." | subscribe_to_memory |

### Namespace vs Key Detection

When user says "check for X" or provides a pattern, determine intent:

| Pattern looks like... | Action |
|-----------------------|--------|
| Full path with `/` (e.g., `project/config/theme`) | `get_memory` - exact key |
| Category-style name (e.g., `gpu_inference_study`, `user-prefs`) | **Ask**: "Do you want to retrieve that key or list what's under that namespace?" |
| Ends with `/` (e.g., `sessions/`) | `list_keys` with prefix - explore the domain |
| User says "as prefix", "under", "namespace" | `list_keys` with prefix |

**When ambiguous, ask.** Don't assume retrieval vs listing.

## ⚠️ Destructive Operations

For `delete_memory` and `revoke_share`: show what will be affected, warn it's permanent, and get user confirmation before executing.

## Hypergraph Output

**Keep it sparse.** When displaying hypergraph results:

1. Show the raw graph structure with minimal formatting
2. Do NOT summarize or analyze unless the user explicitly asks
3. Avoid token-heavy tables, insights sections, or interpretations
4. Just output the nodes and edges in compact form

**Example output:**
```
HG: chess | 20 nodes | 17 edges
Clusters: K(white wins), H(white losses), I(black losses), N(C50 wins)
```

Only provide analysis, stats, or recommendations when the user asks "what do you think" or similar.
