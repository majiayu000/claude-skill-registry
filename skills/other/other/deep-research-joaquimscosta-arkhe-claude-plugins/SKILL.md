---
name: deep-research
description: >
  Deep research on technical topics using EXA tools with intelligent two-tier caching.
  Use when user asks to research a topic, investigate best practices, look up information,
  find patterns, or explore architectures. Also invoked by /research command.
  Triggers: "research", "look up", "investigate", "deep dive", "find information about",
  "what are best practices for", "how do others implement".
---

# Deep Research

Coordinate deep technical research with intelligent caching for cross-project reuse and team knowledge sharing.

## Quick Start

When research is needed:

1. **Resolve scripts path** - Find `plugins/core/skills/deep-research/scripts/` (or Glob for `**/deep-research/scripts/cache_manager.py`)
2. **Check cache first** - Run `python3 {scripts_dir}/cache_manager.py check "{topic}"`
3. **If cached and valid** - Run `cache_manager.py get "{slug}"` and return content directly (no agent needed)
4. **If cache miss** - Invoke `deep-researcher` agent for EXA research, which caches via `cache_manager.py put`
5. **Report findings** - Include cache status and promote suggestion

## Cache Architecture

| Tier | Location | Purpose | Shared |
|------|----------|---------|--------|
| 1 | `~/.claude/plugins/research/` | Fast, cross-project | User only |
| 2 | `docs/research/` | Curated, version controlled | Team |

## Operations

| Operation | Trigger | Fast Path? | Action |
|-----------|---------|------------|--------|
| Research | `/research <topic>` or natural language | Yes (cache hit) | Check cache → return if valid, else research → cache |
| Promote | `/research promote <slug>` | Yes | Run `promote.py {slug}` directly |
| Refresh | `/research refresh <slug>` | No | Spawn agent → fresh research → cache → update promoted |
| List | `/research list` | Yes | Run `cache_manager.py list` (project-scoped by default, `--all` for everything) |

## Project Scoping

Research entries are automatically associated with the current git repository when cached. The `list` operation filters by current project by default, so each project sees only its relevant research. Use `--all` to see everything.

- **Auto-detection**: Project name derived from `git rev-parse --show-toplevel` basename
- **Multi-project**: Entries can belong to multiple projects (associations merge, never replace)
- **Backward compatible**: Existing entries without project associations appear in `--all` but not in project-scoped views

## Scripts

All cache operations use Python scripts in `scripts/`:

| Script | Purpose |
|--------|---------|
| `research_utils.py` | Shared utilities (imported by all scripts) |
| `cache_manager.py` | Cache CRUD: get, put, check, list, delete |
| `promote.py` | Tier 1 → Tier 2 promotion with team notes |
| `index_generator.py` | README index generation for both tiers |

## Slug Normalization

Convert topics to cache keys:
- "Domain-Driven Design" → `domain-driven-design`
- "DDD" → `domain-driven-design` (via alias)
- "React Hooks" → `react-hooks`

## Output Format

After research, report:
```
## Research: {Topic}

**Cache:** {Hit | Miss | Expired}
**Source:** {Cached | Fresh research}
**Path:** ~/.claude/plugins/research/entries/{slug}/

[Brief summary of findings]

Run `/research promote {slug}` to add to project docs.
```

## Agent Delegation

For actual research execution (cache miss or refresh only), delegate to `deep-researcher` agent:
- Has MCP tool access (EXA web search, code context)
- Uses `cache_manager.py put` for cache write operations
- Structures research output consistently

## Additional Resources

- [WORKFLOW.md](WORKFLOW.md) - Detailed process flows
- [EXAMPLES.md](EXAMPLES.md) - Usage examples
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and solutions
