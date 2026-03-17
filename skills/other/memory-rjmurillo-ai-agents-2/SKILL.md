---
name: memory
version: 0.2.0
description: Unified four-tier memory system for AI agents. Tier 1 Semantic (Serena+Forgetful
  search), Tier 2 Episodic (session replay), Tier 3 Causal (decision patterns). Enables
  memory-first architecture per ADR-007.
license: MIT
model: claude-sonnet-4-5
metadata:
  adr: ADR-037, ADR-038
  timelessness: 8/10
---
# Memory System Skill

Unified memory operations across four tiers for AI agents.

---

## Quick Start

```powershell
# Check system health
pwsh .claude/skills/memory/scripts/Test-MemoryHealth.ps1

# Search memory (Tier 1)
pwsh .claude/skills/memory/scripts/Search-Memory.ps1 -Query "git hooks"

# Extract episode from session (Tier 2)
pwsh .claude/skills/memory/scripts/Extract-SessionEpisode.ps1 -SessionLogPath ".agents/sessions/2026-01-01-session-126.md"

# Update causal graph (Tier 3)
pwsh .claude/skills/memory/scripts/Update-CausalGraph.ps1
```

---

## When to Use This Skill

| Scenario | Use Memory Router? | Alternative |
|----------|-------------------|-------------|
| PowerShell script needs memory | ✅ Yes | - |
| Agent needs deep context | ❌ No | `context-retrieval` agent |
| Human at CLI | ❌ No | `/memory-search` command |
| Cross-project semantic search | ❌ No | Forgetful MCP directly |

See [context-retrieval agent](../../../.claude/agents/context-retrieval.md#memory-interface-decision-matrix) for complete decision tree.

---

## Memory-First as Chesterton's Fence

**Core Insight**: Memory-first architecture implements Chesterton's Fence principle for AI agents.

> "Do not remove a fence until you know why it was put up" - G.K. Chesterton

**Translation for agents**: Do not change code/architecture/protocol until you search memory for why it exists.

### Why This Matters

**Without memory search** (removing fence without investigation):

- Agent encounters complex code, thinks "this is ugly, I'll refactor it"
- Removes validation logic that prevents edge case
- Production incident occurs
- Memory contains past incident that explains why validation existed

**With memory search** (Chesterton's Fence investigation):

- Agent encounters complex code
- Searches memory: `Search-Memory.ps1 -Query "validation logic edge case"`
- Finds past incident explaining why code exists
- Makes informed decision: preserve, modify, or replace with equivalent safety

### Investigation Protocol

When you encounter something you want to change:

| Change Type | Memory Search Required |
|-------------|------------------------|
| Remove ADR constraint | `Search-Memory.ps1 -Query "[constraint name]"` |
| Bypass protocol | `Search-Memory.ps1 -Query "[protocol name] why"` |
| Delete >100 lines | `Search-Memory.ps1 -Query "[component] purpose"` |
| Refactor complex code | `Search-Memory.ps1 -Query "[component] edge case"` |
| Change workflow | `Search-Memory.ps1 -Query "[workflow] rationale"` |

### What Memory Contains (Git Archaeology)

**Tier 1 (Semantic)**: Facts, patterns, constraints

- Why does PowerShell-only constraint exist? (ADR-005)
- Why do skills exist instead of raw CLI? (usage-mandatory)
- What incidents led to BLOCKING gates? (protocol-blocking-gates)

**Tier 2 (Episodic)**: Past session outcomes

- What happened when we tried approach X? (session replay)
- What edge cases did we encounter? (failure episodes)

**Tier 3 (Causal)**: Decision patterns

- What decisions led to success? (causal paths)
- What patterns should we repeat/avoid? (success/failure patterns)

### Memory-First Gate (BLOCKING)

**Before changing existing systems, you MUST**:

1. `pwsh .claude/skills/memory/scripts/Search-Memory.ps1 -Query "[topic]"`
2. Review results for historical context
3. If insufficient, escalate to Tier 2/3
4. Document findings in decision rationale
5. Only then proceed with change

**Why BLOCKING**: <50% compliance with "check memory first" guidance. Making it BLOCKING achieves 100% compliance (same pattern as session protocol gates).

**Verification**: Session logs must show memory search BEFORE decisions, not after.

### Connection to Chesterton's Fence Analysis

See `.agents/analysis/chestertons-fence.md` for:

- 4-phase decision framework (Investigation → Understanding → Evaluation → Action)
- Application to ai-agents project (ADR-037 recursion guard, skills-first violations)
- Decision matrix for when to investigate
- Implementation checklist

**Key takeaway**: Memory IS your investigation tool. It contains the "why" that Chesterton's Fence requires you to discover.

---

## Context Engineering

This skill implements [progressive disclosure principles](../../../.agents/analysis/context-engineering.md) from Anthropic and claude-mem.ai research through three-layer architecture.

### Architecture

| Layer | Tool | Cost | When to Use |
|-------|------|------|-------------|
| **Index** | `Search-Memory.ps1` | ~100-500 tokens | Always start here |
| **Details** | `mcp__serena__read_memory` | ~500-10K tokens | After index confirms relevance |
| **Deep Dive** | Follow cross-references | Variable | For complete understanding |

### Token Cost Visibility

```bash
# Count tokens before retrieval (informed ROI decision)
python3 .claude/skills/memory/scripts/count_memory_tokens.py .serena/memories/memory-index.md

# Output: memory-index.md: 2,450 tokens
```

**Caching**: SHA-256 hash-based cache in `.serena/.token-cache.json` provides 10-100x speedup on repeated queries.

See: [scripts/README-count-tokens.md](scripts/README-count-tokens.md)

### Size Validation

```bash
# Pre-commit hook: enforce atomicity thresholds
python3 .claude/skills/memory/scripts/test_memory_size.py .serena/memories --pattern "*.md"

# Exit 0 (pass) or 1 (fail) with decomposition recommendations
```

**Thresholds** (from `memory-size-001-decomposition-thresholds`):

- Max 10,000 chars (~2,500 tokens, atomic memory)
- Max 15 skills (independent concepts per file)
- Max 5 categories (domain focus)

See: [scripts/README-test-size.md](scripts/README-test-size.md)

### Principles

**Progressive Disclosure**: List names → Read details → Deep dive on cross-references. Prevents loading 9,500 tokens when only 1,200 are relevant (87% waste reduction).

**Just-in-Time Retrieval**: Serena-first with Forgetful augmentation. High precision through lexical search before expensive semantic operations.

**Size Enforcement**: Atomic memories prevent token waste. One retrievable concept per file.

For full analysis, see: `.agents/analysis/context-engineering.md`

---

## Triggers

Use this skill when the user says:

- `search memory` for semantic search across tiers
- `check memory health` for system status
- `extract episode from session` for session replay
- `update causal graph` for pattern tracking
- `count memory tokens` for budget analysis

---

## Quick Reference

| Operation | Name | Key Parameters |
|-----------|------|----------------|
| Search facts/patterns | `Search-Memory.ps1` | `-Query`, `-LexicalOnly`, `-MaxResults` |
| Get single session | `Get-Episode` | `-SessionId` |
| Find multiple sessions | `Get-Episodes` | `-Outcome`, `-Task`, `-Since` |
| Trace causation | `Get-CausalPath` | `-FromLabel`, `-ToLabel` |
| Find success patterns | `Get-Patterns` | `-MinSuccessRate` |
| Extract episode | `Extract-SessionEpisode.ps1` | `-SessionLogPath` |
| Update patterns | `Update-CausalGraph.ps1` | `-EpisodePath`, `-DryRun` |
| Health check | `Test-MemoryHealth.ps1` | `-Format` (Json/Table) |

---

## Decision Tree

```text
What do you need?
│
├─► Current facts, patterns, or rules?
│   └─► TIER 1: Search-Memory.ps1
│
├─► What happened in a specific session?
│   └─► TIER 2: Get-Episode -SessionId "..."
│
├─► Recent sessions with specific outcome?
│   └─► TIER 2: Get-Episodes -Outcome "failure" -Since 7days
│
├─► Why did decision X lead to outcome Y?
│   └─► TIER 3: Get-CausalPath -FromLabel "..." -ToLabel "..."
│
├─► What patterns have high success rate?
│   └─► TIER 3: Get-Patterns -MinSuccessRate 0.7
│
├─► Need to store new knowledge?
│   ├─ From completed session? → Extract-SessionEpisode.ps1
│   └─ Factual knowledge? → using-forgetful-memory skill
│
└─► Not sure which tier?
    └─► Start with TIER 1 (Search-Memory), escalate if insufficient
```

---

## Anti-Patterns

| Anti-Pattern | Do This Instead |
|--------------|-----------------|
| Skipping memory search | Always search before multi-step reasoning |
| Tier confusion | Follow decision tree explicitly |
| Forgetful dependency | Use `-LexicalOnly` fallback |
| Stale causal graph | Run `Update-CausalGraph.ps1` after extractions |
| Incomplete extraction | Only extract from COMPLETED sessions |

---

## See Also

| Document | Content |
|----------|---------|
| [quick-start.md](references/quick-start.md) | Common workflows |
| [skill-reference.md](references/skill-reference.md) | Detailed script parameters |
| [tier-selection-guide.md](references/tier-selection-guide.md) | When to use each tier |
| [memory-router.md](references/memory-router.md) | ADR-037 router architecture |
| [reflexion-memory.md](references/reflexion-memory.md) | ADR-038 episode/causal schemas |
| [troubleshooting.md](references/troubleshooting.md) | Error recovery |
| [benchmarking.md](references/benchmarking.md) | Performance targets |
| [agent-integration.md](references/agent-integration.md) | Multi-agent patterns |

---

## Storage Locations

| Data | Location |
|------|----------|
| Serena memories | `.serena/memories/*.md` |
| Forgetful memories | HTTP MCP (vector DB) |
| Episodes | `.agents/memory/episodes/*.json` |
| Causal graph | `.agents/memory/causality/causal-graph.json` |

---

## Verification

| Operation | Verification |
|-----------|--------------|
| Search completed | Result count > 0 OR logged "no results" |
| Episode extracted | JSON file in `.agents/memory/episodes/` |
| Graph updated | Stats show nodes/edges added |
| Health check | All tiers show "available: true" |

```powershell
pwsh .claude/skills/memory/scripts/Test-MemoryHealth.ps1 -Format Table
```

---

## Process

### Phase 1: Query

Determine the memory tier and run the appropriate script.

### Phase 2: Validate

Verify results are non-empty and relevant to the query context.

### Phase 3: Report

Return structured results to the caller with source attribution.

---

## Scripts

| Script | Purpose | Exit Codes |
|--------|---------|------------|
| `Search-Memory.ps1` | Tier 1 semantic search across Serena and Forgetful | 0=success, 1=error |
| `count_memory_tokens.py` | Token counting with tiktoken caching | 0=success, 1=error |
| `test_memory_size.py` | Memory atomicity validation | 0=pass, 1=violations |
| `Test-MemoryHealth.ps1` | System health dashboard | 0=healthy, 1=degraded |

---

## Related Skills

| Skill | When to Use Instead |
|-------|---------------------|
| `using-forgetful-memory` | Deep Forgetful operations (create, update, link) |
| `curating-memories` | Memory maintenance (obsolete, deduplicate) |
| `exploring-knowledge-graph` | Multi-hop graph traversal |
