---
name: dk-local-follow-breadcrumb
description: "Consults existing breadcrumb analysis docs before exploring the codebase. Use this skill whenever the user asks about how a flow works, where something happens in the code, how to debug or test a specific area, what files are involved in a feature, or needs to understand the path data takes through the system. Also trigger when the user mentions 'where does X happen', 'how does Y work', 'trace this', 'what files handle Z', 'how to test this flow', 'debug this area', or when you're about to spawn multiple exploration subagents to understand a cross-cutting flow. Even if the user doesn't explicitly ask — if the task requires understanding how multiple layers connect (frontend → backend → worker → CLI), check breadcrumbs first. This is cheaper and more accurate than re-discovering the same information through code search."
argument-hint: "<what you're trying to understand, e.g. 'how does task execution work' or 'where do traces get ingested'>"
allowed-tools: Read, Grep, Glob, Task, Bash
---

# /dk-local-follow-breadcrumb — Breadcrumb-First Exploration

This skill is about reading before searching. The `docs/breadcrumb_analysis/` directory contains end-to-end workflow traces that have already been carefully researched and documented. Loading a relevant breadcrumb takes seconds and costs a fraction of what spawning exploration subagents costs. The breadcrumb docs are maintained alongside code changes, so they're the most reliable "map" of how flows work.

## Context

<exploration_context> $ARGUMENTS </exploration_context>

If the context above is empty, look at what the user is asking about in the conversation and infer the exploration target.

## Step 1: Load the index

Read `docs/breadcrumb_analysis/_INDEX.md`. This is the single source of truth for what's been documented.

The index has two sections that matter:

1. **Flows table** — lists every breadcrumb folder and what it traces. Scan this to find which breadcrumb(s) cover the user's question.
2. **Quick navigation** — maps common symptoms (e.g., "task stuck in IN_PROGRESS", "screenshots not showing") directly to the right DEBUG.md. If the user describes a symptom, check here first.

## Step 2: Match the question to breadcrumbs

Compare what the user is asking against the index entries. There are three outcomes:

### A. Direct hit — a breadcrumb covers exactly this flow

Load the relevant docs in order of increasing detail:

1. **FLOW.md** — Read this first. It's the high-level map (30-second read). Shows the path data takes, which files/functions are involved at each hop, and where branches occur. This alone often answers "where does X happen?" questions.

2. **DETAILS.md** — Read this if the user needs function-level specifics: what data goes in/out, what conditionals change behavior, what side effects exist. This answers "how does X work?" questions.

3. **DEBUG.md** — Read this if the user is debugging something broken, or wants to know how to test a flow. Contains log locations, grep patterns, quick commands, env vars, and common breakpoints. This answers "how do I debug/test X?" questions.

Don't load all three by default. Start with FLOW.md. Only go deeper if the user's question requires it. Present what you found and ask if they need more detail.

### B. Partial coverage — a breadcrumb covers part of the flow

Load the relevant breadcrumb for the covered portion. Then clearly tell the user:

```
The breadcrumb for <X> covers <these parts> of what you're asking about.
For <the uncovered parts>, I'll need to explore the code directly.
```

Then explore only the gaps — don't re-trace what the breadcrumb already documents.

### C. No coverage — nothing in the index matches

Tell the user:

```
No existing breadcrumb covers this flow. I'll explore the code directly.
Consider running /dk-breadcrumb-creator afterward to document this flow for next time.
```

Then proceed with normal exploration (grep, glob, file reads, subagents as needed).

## Step 3: Present findings

After loading the relevant breadcrumb docs, synthesize an answer to the user's actual question. Don't just dump the breadcrumb content — extract the specific information they need.

Good response pattern:
```
Based on the breadcrumb for <flow-name>:

<direct answer to their question, citing specific files/functions from the breadcrumb>

The key files involved are:
- `path/to/file.py` :: `function()` — <what it does in this context>
- `path/to/other.py` :: `other_func()` — <what it does>

<if debugging> Quick commands from the debug guide:
<relevant commands from DEBUG.md>
```

If the breadcrumb is stale (references files/functions that no longer exist), note which parts seem outdated and verify those specific points against the current code. Flag this to the user so the breadcrumb can be updated.

## Step 4: Suggest breadcrumb creation for gaps

If the user's exploration uncovered a flow that isn't documented (outcome C), or revealed that an existing breadcrumb is incomplete (outcome B with significant gaps), suggest:

```
This flow isn't documented in breadcrumb analysis yet. Want me to create one?
Run /dk-breadcrumb-creator to trace and document it for future reference.
```

This closes the loop — exploration that finds undocumented territory feeds back into the documentation system.

## When NOT to use this skill

- **Single-file questions** — "What does `function_name` in `file.py` do?" → Just read the file directly.
- **Creating new breadcrumbs** — Use `/dk-breadcrumb-creator` instead. This skill reads; that one writes.
- **General codebase search** — "Find all TODO comments" → Just grep. Breadcrumbs trace flows, not search for patterns.
