---
name: tidar-thread-probe
description: TIDAR Thread Probe Skill
version: 1.0.0
---

# TIDAR Thread Probe Skill

Tree-structured Iterative Decomposition And Recombination for cross-system thread pattern discovery across AMP, Claude, Codex, and Warp.

## Capability

Analyzes threads across multiple AI agent interaction surfaces using ordered locale site semantics:

1. **Shared Patterns**: Fields/behaviors present in ALL systems
2. **Pairwise Patterns**: Fields shared by exactly 2 systems
3. **Unique Patterns**: System-specific fields and behaviors
4. **Perplexing Patterns**: Anomalies, contradictions, mysteries

## Ordered Locale vs Ordered Locale Sites

- **Ordered Locale**: Complete Heyting algebra (frame) L with compatible preorder ≤ satisfying open cone condition. Each thread lives in an ordered locale (its workspace/project).

- **Ordered Locale Site**: Grothendieck site on ordered locale with coverage relation J. Cross-system observation uses ordered locale sites where sheaves model behavioral coalgebra.

## Thread Counts (as of 2025-12-26)

| Source | Threads | Sessions | Messages |
|--------|---------|----------|----------|
| AMP | 616 | - | 2,535 tool calls |
| Claude | - | 236 | 36,057 messages |
| Codex | - | 36+ | ~400 records |
| **Total** | **888** canonical threads |

## Canonical Universal Schema

```
ATOMIC FIELDS (required):
  thread_id   : string  - unique session/thread identifier
  timestamp   : int64   - Unix ms (or ISO-8601 converted)
  workspace   : string  - absolute path to project/cwd
  role        : enum    - user|assistant|system|tool
  content     : string  - message text content

OPTIONAL ATOMIC:
  model       : string  - model identifier
  originator  : string  - source tool (amp, claude, codex)

DERIVED FIELDS:
  message_count    : COUNT(messages in thread)
  tool_call_count  : COUNT(tool invocations)
  acceptance_rate  : 1 - (reverted / total)
  trit             : GF(3) from hash(thread_id) mod 3 - 1
  role_semantic    : trit → {validator, coordinator, generator}
```

## GF(3) Conservation Status

Current cross-system trit distribution:
- MINUS (-1): 284 threads
- ERGODIC (0): 288 threads
- PLUS (+1): 316 threads
- **Σ trits = 32 (mod 3 = 2) → NOT CONSERVED**

Need 1 more MINUS thread or 2 more ERGODIC threads to balance.

## Usage

```bash
# Run TIDAR analysis
python3 src/universal_thread_schema.py

# Query specific source
duckdb trit_stream.duckdb -c "SELECT * FROM amp_threads LIMIT 10"
jq -s '.' ~/.claude/history.jsonl | head
```

## Perplexing Patterns

1. AMP `.org` files have **45% revert rate** vs 0% for .clj/.jl/.bb
2. AMP threads with 40+ hour durations but only 5-9 tool calls
3. Codex uses `danger-full-access` sandbox policy in production
4. Claude longest session: 841 messages in 182 seconds (4.6 msg/sec)
5. AMP bimodal acceptance: threads cluster at 0% or 100%
6. Codex embeds ~50KB instructions per session (redundant)
7. Claude `pastedContents` used in only 0.5% of entries

## Source-Specific Mappings

### AMP → Canonical
- thread_id → thread_id
- first_ts/last_ts → timestamp range
- uri → workspace (extracted)
- tool_id → tool invocation
- reverted → acceptance tracking

### Claude → Canonical
- sessionId → thread_id
- timestamp → timestamp (already Unix ms)
- project → workspace
- display → content

### Codex → Canonical
- payload.id → thread_id
- timestamp → timestamp (ISO-8601 → Unix ms)
- cwd → workspace
- message/content → content

## Integration with Gay-MCP Colors

Each thread's trit determines its Gay-MCP hue:
- MINUS (-1): Cold hues (180-300°) - Blue/Violet spectrum
- ERGODIC (0): Neutral hues (60-180°) - Green/Cyan spectrum
- PLUS (+1): Warm hues (0-60°, 300-360°) - Red/Yellow spectrum

Visualization: `scripts/gay_stream.py --threads`

## Dependencies

- `duckdb` for AMP queries
- `jq` for Claude JSONL parsing
- Python 3.10+ with dataclasses

## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
tidar-thread-probe (+) + SDF.Ch10 (+) + [balancer] (+) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch3: Variations on an Arithmetic Theme
- Ch4: Pattern Matching
- Ch8: Degeneracy

### Connection Pattern

Adventure games synthesize techniques. This skill integrates multiple patterns.
