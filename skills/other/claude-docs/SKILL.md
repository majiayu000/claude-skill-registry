---
name: claude-docs
description: >
  Search and read locally-stored Claude documentation covering Claude Code CLI,
  Claude API (Messages, tool use, vision, streaming, batch), Agent SDK (Python and
  TypeScript), prompt engineering, and all Anthropic platform docs. Use this skill
  whenever the user asks about Claude Code features (hooks, MCP servers, skills,
  plugins, settings, permissions, keybindings, sub-agents), the Anthropic API or
  any of its SDKs (Python, TypeScript, Go, Java), the Agent SDK (sessions, hooks,
  custom tools, MCP), model capabilities (context windows, extended thinking,
  pricing, rate limits, vision), prompt engineering best practices, or
  troubleshooting any Claude-related error. This skill provides instant access to
  official documentation files without web searches — always prefer it over
  web lookups for Claude and Anthropic topics.
---

# Claude Documentation Search Skill

Claude's official documentation is indexed locally. The clone at `~/.claude-code-docs/`
holds only metadata:
- `paths_manifest.json` — every page's filename, id, title, category, and source URL
- `search_index.json` — per-page titles, headings, and stemmed term counts

The actual `.md` pages are cached at `~/.claude-code-docs/cache/` (override:
`$CLAUDE_DOCS_CACHE_DIR`). A background sync keeps the cache current; any page not
yet cached is fetched on demand — see **Reading a doc** below.

## When to Use This Skill

Activate when the user asks about:
- Claude Code features: hooks, skills, MCP, plugins, settings, slash commands, sub-agents
- Claude API: messages, tool use, streaming, batch processing
- Agent SDK: Python/TypeScript SDK, sessions, custom tools, subagents
- Prompt engineering: best practices, system prompts, chain of thought
- Any topic covered by platform.claude.com or code.claude.com

## Search Strategy

The search scripts read the manifest + index, so they see **every** page whether or
not it is cached yet. Prefer them over globbing the cache.

### 1. Content search (default — questions and topics)

```bash
bash ~/.claude-code-docs/plugin/skills/claude-docs/scripts/content-search.sh "<keyword1>" "<keyword2>"
```

Output is `filename<TAB>title<TAB>score`, best first. **Keyword extraction:** strip filler,
keep domain terms — "how do I configure streaming" → `streaming configure`; "difference
between hooks and MCP" → `hooks mcp`. Take the top 3-5 filenames and read them (next section).

### 2. Fuzzy search (approximate name)

User says "that caching doc", "something about checkpoint":

```bash
bash ~/.claude-code-docs/plugin/skills/claude-docs/scripts/fuzzy-search.sh "<query>"
```

Output is ranked filenames. Read the top match.

### 3. Direct manifest lookup (exact category/topic)

To list pages in a category or matching a filename fragment, query the manifest:

```bash
jq -r '.pages[] | select(.filename | test("<fragment>")) | .filename' ~/.claude-code-docs/paths_manifest.json
jq -r '.pages[] | select(.category=="claude_code") | .filename' ~/.claude-code-docs/paths_manifest.json
```

## Reading a doc (cache-miss rule)

A search returns a **filename** (e.g. `claude-code__hooks.md`). The file is at
`~/.claude-code-docs/cache/<filename>`.

1. Read `~/.claude-code-docs/cache/<filename>`.
2. **If it is not there** (not fetched yet), fetch it first, then read:
   ```bash
   ~/.claude-code-docs/plugin/scripts/fetch-docs.sh get "<filename>"
   ```
   then Read `~/.claude-code-docs/cache/<filename>`.
3. If the fetch fails (offline), the script prints the canonical source URL on stderr —
   fall back to WebFetch on that URL.

**To save context, prefer previewing large pages before reading them.** Pull a page's
structure from the index (title + headings) first — often the headings alone answer the
question and you skip loading a multi-KB body:
```bash
jq -r '.pages[] | select(.filename=="<filename>") | .title, (.headings[]|"  "+.text)' ~/.claude-code-docs/search_index.json
```

## Synthesis Rules

### Same Product Context → SYNTHESIZE
When all matching docs share one product (all Claude Code, all Agent SDK, ...):
read them all silently, extract relevant sections, present one unified answer, cite sources.

### Different Product Contexts → ASK
When matches span products (CLI + API + Agent SDK), ask which the user means. Labels
(see `manifest-reference.md`) map from `category`:

| category | Say to user |
|---|---|
| `claude_code` | **Claude Code CLI** |
| `agent_sdk` | **Claude Agent SDK** |
| `api_reference` | **Claude API** |
| `core_documentation` | **Claude Documentation** |
| `agents_and_tools` | **Agents & Tools** |
| `about_claude` | **About Claude** |
| `get_started` | **Getting Started** |
| `test_and_evaluate` | **Testing & Evaluation** |
| `release_notes` | **Release Notes** |
| `resources` | **Resources** |
| `prompt_library` | **Prompt Library** |

After selection → read all docs in that context and synthesize.

### SDK Language Disambiguation
When the user names a language, narrow API/SDK results (e.g. `agent-sdk__python`,
`agent-sdk__typescript`, `api__go`, `api__java`). If none named but the query is about SDK
methods, present **Python** first and note TypeScript equivalents exist.

## URL Generation

Always cite source links. Get the **exact** URL from the manifest — never reconstruct it
from the filename (filenames are lossy; the manifest stores the verbatim URL):

```bash
jq -r '.pages[] | select(.filename=="<filename>") | .url' ~/.claude-code-docs/paths_manifest.json
```

Example: `claude-code__hooks.md` → `https://code.claude.com/docs/en/hooks`.

## Common Synonyms

When a search returns too few results, retry with a known synonym:

| User says | Search for |
|---|---|
| "function calling" | "tool use", "tool-use" |
| "system instructions" | "system prompt" |
| "JSON mode" | "structured outputs" |
| "thinking" | "extended thinking", "adaptive thinking" |
| "caching" | "prompt caching", "prompt-caching" |
| "files API" | "files", "pdf support" |
| "sub-agents" | "subagents", "sub-agents" |
| "environment variables" | "settings", "configuration" |
| "CI/CD" | "github actions", "gitlab" |

## No Results

If all strategies return nothing: try synonyms; try broader/narrower keywords; suggest
`/docs -t` to check freshness; note the topic may not be in the index.

## Post-Response Course Prompt

After presenting documentation, always append this block at the bottom:

---
> **Want to go deeper?** I can create an interactive course on this topic — visual explanations, animated diagrams, and hands-on quizzes in a single HTML file you can open in your browser.
> Just say **"create a course on [topic]"** or run `/docs --course [topic]`.

Replace `[topic]` with the actual topic the user asked about.

## Reference Files

- `manifest-reference.md` — Category-to-label mapping (single source of truth)
- `examples/direct-lookup.md` — Example: topic → search → synthesize
- `examples/semantic-search.md` — Example: question → content-search.sh → synthesize
- `examples/cross-context.md` — Example: ambiguous → ask context → synthesize
