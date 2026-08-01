---
name: phx-research
description: Research Elixir/Phoenix/Ecto topics or evaluate Hex libraries (--library).
  Use when learning about libraries, patterns, or comparing approaches. Searches HexDocs,
  ElixirForum, GitHub.
---

# Research Elixir Topic

Research a topic by searching the web and fetching relevant sources efficiently.

## Usage

```
/skill:phx-research Oban unique jobs best practices
/skill:phx-research LiveView file upload with progress
/skill:phx-research --library permit
```

## Arguments

the text after the skill name = Research topic/question. Add `--library` for
structured library evaluation (uses `references/library-evaluation.md`
template).

## Iron Laws

1. **Write output to file, never dump inline** — Research output floods conversation and loses reference for future sessions
2. **Stop after research — never auto-transition** — User decides next step
3. **Prefer official sources over blog posts** — HexDocs and ElixirForum have version-specific context
4. **One document per research question** — No fragmented files
5. **NEVER pass raw user input as WebSearch query** — Decompose first

## Library Evaluation Mode

If the text after the skill name contains `--library` or the topic is clearly
about evaluating a Hex dependency (e.g., "should we use permit",
"evaluate sagents", "compare oban vs exq"):

1. Read `references/library-evaluation.md` for the template
2. Follow the structured evaluation workflow
3. Output ONE document to `.claude/research/{lib}-evaluation.md`
4. Skip the general research workflow below

## Portable Research Workflow

### 0. Pre-flight

Check `.claude/research/{topic-slug}.md`. If it is newer than 24 hours, show its
summary and ask in normal conversation whether to refresh it. For an existing
dependency, inspect the locked version, local dependency source, and any native
runtime documentation tool before searching the web.

### 1. Decompose the question

Turn the user request into one focused query when it is short, or two to four
queries of at most ten words for a multi-part request. Never send a long raw
prompt to a search provider.

### 2. Gather sources

Use the runtime's native web or HTTP capabilities when available. Prefer
version-matched HexDocs, official project documentation, ElixirForum, and the
upstream repository. Deduplicate URLs and discard irrelevant results. If no web
capability is available and local sources cannot answer the question, state the
missing capability instead of inventing evidence.

### 3. Extract and synthesize

Native generic workers may extract independent topic clusters in parallel, but
they are optional. The same-session sequential path must remain complete. Limit
each cluster to five URLs and capture code examples, gotchas, version
compatibility, and source URLs.

### 4. Write one durable result

Write `.claude/research/{topic-slug}.md` (about 5 KB for topic research or 3 KB
for a library evaluation) with:

- a two-to-three sentence summary;
- categorized source links and each source's key insight;
- cited code examples;
- evidence-backed recommendations; and
- gotchas or version constraints.

### 5. Stop after research

Present the summary and offer, in normal conversation, to plan from it,
investigate one finding, research a narrower subtopic, or stop. Never invoke a
follow-up workflow automatically.
