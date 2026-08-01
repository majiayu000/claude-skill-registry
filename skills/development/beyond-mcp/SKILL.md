---
name: beyond-mcp
description: 'Agent: Sub-Agent 4'
---

# Skill Approach Analysis

**Agent:** Sub-Agent 4
**Focus:** Compare Kalshi-markets skill (beyond-mcp) vs claude-mem search skill
**Goal:** Identify why one skill might be auto-invoked while another isn't

## 1. Skill Description Comparison

### Kalshi-Markets Skill (beyond-mcp)

**Description (from SKILL.md frontmatter):**
```
Access Kalshi prediction market data including market prices, orderbooks, trades,
events, and series information. Use when the user asks about prediction markets,
Kalshi markets, betting odds, market prices, or needs to search or analyze
prediction market data.
```

**Trigger keywords explicitly listed:**
- prediction markets
- Kalshi markets
- betting odds
- market prices
- search/analyze prediction market data

**Capability visibility:** HIGH
- Description immediately names concrete capabilities (market prices, orderbooks, trades, events, series)
- "Use when..." clause directly connects user language to skill activation
- SKILL.md is 72 lines, front-loads actionable information
- 10 scripts listed with clear "When to use" statements

**Lines in SKILL.md:** 72 lines total
- Frontmatter: 4 lines (name + 3-line description)
- Instructions: 6 lines
- Script list with contexts: 30 lines (10 scripts × 3 lines each)
- Architecture/Quick Start: 32 lines

### Claude-Mem Search Skill (current)

**Description (from SKILL.md frontmatter):**
```
Search claude-mem persistent memory for past sessions, observations, bugs fixed,
features implemented, decisions made, code changes, and previous work. Use when
answering questions about history, finding past decisions, or researching
previous implementations.
```

**Trigger keywords implied:**
- past sessions
- observations
- bugs fixed
- features implemented
- decisions made
- code changes
- previous work
- history
- past decisions
- previous implementations

**Capability visibility:** MEDIUM-LOW
- Description lists WHAT is searchable (sessions, observations, bugs) but...
- ...buries HOW in nested operations/ files (9 operations)
- "Use when..." clause is generic ("answering questions about history")
- SKILL.md is 97 lines but most points to subdirectories

**Lines in SKILL.md:** 97 lines total
- Frontmatter: 4 lines (name + 3-line description)
- "When to Use" section: 18 lines (good!)
- "Quick Decision Guide": 6 lines (good routing!)
- "Available Operations": 20 lines (list of 10 operations)
- Rest: Common workflows, formatting, technical notes (49 lines)

### Comparison

**Winner for discoverability:** Kalshi-Markets by a significant margin

**Key differences:**

1. **Description specificity:**
   - Kalshi: Names concrete data types (market prices, orderbooks, trades)
   - Claude-mem: Names abstract categories (observations, decisions, changes)

2. **Trigger keywords placement:**
   - Kalshi: In frontmatter description AND README (explicit listing)
   - Claude-mem: Only in frontmatter, no explicit "triggers on" section

3. **Capability visibility:**
   - Kalshi: 10 scripts visible in SKILL.md with "When to use" for each
   - Claude-mem: 10 operations hidden in subdirectories, must navigate

4. **Progressive disclosure balance:**
   - Kalshi: Shows ALL capabilities upfront (72 lines), hides implementation (2377 lines in scripts/)
   - Claude-mem: Shows routing/meta info (97 lines), hides operations docs (operations/*.md)

5. **Actionability:**
   - Kalshi: "Use when user asks about X" → Direct action (run script Y)
   - Claude-mem: "Use when user asks about X" → Choose operation → Read operation doc → Execute

**Missing from claude-mem:**

1. No explicit trigger keyword list in SKILL.md or separate doc
2. No "When to use" statement per operation IN the main SKILL.md
3. Operations are abstractions (search by type) not concrete nouns (orderbook)
4. Two-hop navigation (SKILL.md → operations/ → execute) vs one-hop (SKILL.md → execute)

## 2. Implementation Pattern Analysis

### Kalshi Pattern

**SKILL.md structure:**
```
FRONTMATTER (trigger-rich description)
↓
INSTRUCTIONS (how to use scripts)
↓
PROGRESSIVE DISCLOSURE (warning against reading scripts)
↓
AVAILABLE SCRIPTS (10 × "When to use" statements)
↓
ARCHITECTURE (self-contained philosophy)
↓
QUICK START (immediate examples)
```

**Scripts approach:**
- 10 self-contained Python scripts (157-468 lines each)
- Each script is independently executable
- Embedded HTTP client in each (no shared dependencies)
- `--help` and `--json` flags standard
- Total: 2377 lines hidden in scripts/

**Progressive disclosure:**
- SKILL.md: Shows WHAT and WHEN (72 lines visible)
- scripts/: Shows HOW and implementation (2377 lines hidden)
- Instruction: "Don't read scripts unless absolutely needed"

**How integrated:**
- Claude reads SKILL.md → Identifies script → Runs `uv run scripts/X.py --help` → Executes
- One-hop: SKILL.md has enough info to choose and run script
- Scripts are terminal nodes (no further navigation)

### Claude-Mem Pattern

**SKILL.md structure:**
```
FRONTMATTER (trigger-rich description)
↓
WHEN TO USE (good examples)
↓
QUICK DECISION GUIDE (routing to operations)
↓
AVAILABLE OPERATIONS (list of 10 with file paths)
↓
COMMON WORKFLOWS (meta-guide)
↓
RESPONSE FORMATTING (meta-guide)
↓
TECHNICAL NOTES + PERFORMANCE TIPS
```

**Operations docs approach:**
- 10 operation documentation files (1.4k-6.2k bytes each)
- Each file explains one search pattern
- Documents HTTP API calls (not embedded tools)
- Operations are documentation, not executables

**Progressive disclosure:**
- SKILL.md: Shows categories and routing (97 lines visible)
- operations/: Shows API usage patterns (12 files to navigate)
- Additional docs: common-workflows.md, formatting.md

**How organized:**
- Claude reads SKILL.md → Chooses operation category → Reads operations/X.md → Executes HTTP call
- Two-hop: SKILL.md routes to operations/, then execute
- Operations are intermediate nodes (documentation layer)

### Comparison: Better for Autonomy?

**Winner: Kalshi pattern is better for autonomy**

**Reasoning:**

1. **Execution path length:**
   - Kalshi: 1 hop (SKILL.md → execute script)
   - Claude-mem: 2 hops (SKILL.md → operations doc → execute HTTP)

2. **Cognitive load:**
   - Kalshi: "When user asks about orderbook" → Run orderbook.py
   - Claude-mem: "When user asks about past bugs" → Choose operation (by-type? observations?) → Read doc → Execute

3. **Decision points:**
   - Kalshi: 1 decision (which script?)
   - Claude-mem: 2 decisions (which operation category? which specific doc?)

4. **Self-containment:**
   - Kalshi: Scripts are tools (executable)
   - Claude-mem: Operations are instructions (requires interpretation then tool use)

**However, claude-mem has advantages:**

1. More flexible (HTTP API can be called many ways)
2. Better for complex queries (multiple parameters, filters)
3. Better documentation of edge cases and formatting

**But these advantages hurt discoverability and autonomy in practice.**

## 3. Auto-Invocation Evidence

### README Claims

**Explicit claims from beyond-mcp/apps/4_skill/README.md:**

1. Line 7: "**Model-Invoked** - Claude autonomously activates based on context"
2. Line 16: "Claude (detects keyword) -> Loads SKILL.md -> Runs relevant script -> Kalshi API"
3. Line 19: "The skill automatically activates when Claude detects keywords like:"
4. Line 32: "# Claude will auto-detect and use the skill"
5. Line 75: "Want autonomous skill discovery"

### Evidence Found

**Type 1: Design patterns that support auto-invocation**

1. **Keyword-rich description in frontmatter:**
   ```
   Use when the user asks about prediction markets, Kalshi markets,
   betting odds, market prices, or needs to search or analyze
   prediction market data.
   ```
   This is the standard Claude Code pattern for skill triggering.

2. **Concrete capability nouns:**
   - Market prices, orderbooks, trades, events, series
   - These are specific enough to match user questions

3. **Direct "When to use" mappings:**
   Each script has a clear trigger statement visible in SKILL.md

**Type 2: Architecture supporting autonomy**

1. **Self-contained scripts** reduce context reading
2. **`--help` flag** allows Claude to discover usage without reading code
3. **`--json` flag** provides structured output for processing

**Type 3: Lack of counter-evidence**

- No "call Skill tool first" instructions
- No "remember to invoke skill" reminders
- README assumes autonomy as default behavior

### Evidence NOT Found

**Direct proof of auto-invocation:**
- No screenshots of Claude auto-invoking the skill
- No logs showing "skill auto-invoked"
- No metrics on invocation rate
- No A/B test showing improved discovery

**Mechanistic explanation:**
- No documentation of HOW Claude decides to load skills
- No threshold for trigger keywords (1 match? 2 matches?)
- No explanation of skill ranking/priority

### Confidence in Claim

**Confidence: MEDIUM-HIGH**

**Why Medium-High (not High):**

1. **README makes strong claims** but provides no empirical evidence
2. **Design patterns align with claimed behavior** (keyword-rich, self-contained)
3. **No counter-evidence** (no instructions to manually invoke)
4. **This is a showcase repo** - likely tested extensively before publishing

**Why not Low:**

1. The pattern is consistent across the repository
2. The README is detailed and professional (not marketing fluff)
3. The architecture makes sense for autonomy (reduce friction)

**What would raise confidence to High:**

1. Anthropic documentation confirming skill auto-invocation mechanism
2. Logs or screenshots of real usage
3. Metrics showing discovery rates
4. Code in Claude Code CLI showing skill matching logic

## 4. Root Cause Analysis: Why Claude Doesn't Use claude-mem

### Hypothesis A: Weak Description

**Evidence:**

1. **Trigger keyword density:**
   - Kalshi: 5 explicit trigger phrases in 3-line description
   - Claude-mem: 10 implied keywords in 3-line description
   - BUT: Kalshi's triggers are nouns (market prices), claude-mem's are abstractions (observations)

2. **Description specificity:**
   - Kalshi: "market prices, orderbooks, trades, events, series"
   - Claude-mem: "sessions, observations, bugs fixed, features implemented, decisions, code changes, previous work"
   - Claude-mem is LESS concrete (what's an "observation"?)

3. **"Use when" clarity:**
   - Kalshi: "user asks about prediction markets, Kalshi markets, betting odds, market prices"
   - Claude-mem: "answering questions about history, finding past decisions, researching previous implementations"
   - Claude-mem is more GENERIC (many tools could match "history")

4. **Missing explicit trigger list:**
   - Kalshi README has explicit section: "The skill automatically activates when Claude detects keywords like:"
   - Claude-mem has no equivalent

**Fix effort:** LOW (1-2 hours)
- Rewrite SKILL.md frontmatter description
- Add explicit trigger keyword list
- Use concrete nouns instead of abstractions

**Likelihood this is the root cause:** HIGH (70%)

**Reasoning:**
- This is the FIRST thing Claude sees when considering skills
- Weak triggers = low match probability
- Generic triggers = low priority vs other tools

### Hypothesis B: Progressive Disclosure Tradeoff

**Evidence:**

1. **Capability visibility in SKILL.md:**
   - Kalshi: All 10 scripts listed with "When to use" statements (30 lines)
   - Claude-mem: All 10 operations listed but as file paths (20 lines), no inline "When to use"

2. **Navigation depth:**
   - Kalshi: SKILL.md → execute (1 hop)
   - Claude-mem: SKILL.md → operations/ → execute (2 hops)

3. **Decision complexity:**
   - Kalshi: "User asks about orderbook" → orderbook.py (direct)
   - Claude-mem: "User asks about bugs" → by-type.md or observations.md? (ambiguous)

4. **Hidden information:**
   - Kalshi: Implementation hidden (2377 lines in scripts/)
   - Claude-mem: Usage patterns hidden (operations/ docs)
   - Claude-mem hides the WRONG thing (how to use) vs the RIGHT thing (implementation)

**Fix effort:** MEDIUM (1-2 days)
- Inline "When to use" statements for each operation in SKILL.md
- Reduce navigation depth (flatten operations/ into SKILL.md?)
- Simplify operation categorization

**Likelihood this is the root cause:** MEDIUM (50%)

**Reasoning:**
- Even after skill is loaded, Claude must navigate further
- Extra navigation = extra LLM calls = higher chance of abandoning skill
- BUT: The "Quick Decision Guide" section should help with this

### Hypothesis C: Pattern Limitation (Skills Inherently Limited)

**Evidence:**

1. **No official documentation** on skill auto-invocation mechanism
2. **Anecdotal evidence** suggests skills aren't reliably auto-invoked
3. **Alternative patterns exist** (MCP, sub-agents) that may be preferred by Claude
4. **Skill pattern is new** (introduced recently?) and may not be fully integrated

**Against this hypothesis:**

1. Beyond-MCP README confidently claims auto-invocation
2. Anthropic publishes skill examples, suggesting they work
3. Kalshi skill is well-designed and should work if any skill does

**Fix effort:** HIGH (weeks to months)
- Can't fix pattern limitations ourselves
- Would need Anthropic to improve skill discovery
- Alternative: Switch to different pattern (MCP, sub-agents)

**Likelihood this is the root cause:** LOW (20%)

**Reasoning:**
- Beyond-MCP demonstrates skills can work
- More likely our implementation is weak than pattern is broken
- BUT: Without official docs, we can't rule this out

### Most Likely Root Cause

**Answer: Hypothesis A (Weak Description) - 70% confidence**

**Reasoning:**

1. **Comparison shows clear gaps** in claude-mem's description vs Kalshi
2. **Trigger keywords matter** - this is how Claude matches user input to skills
3. **Quick fix with high impact** - rewriting description is low-effort, high-reward
4. **Supported by beyond-MCP evidence** - Kalshi's strong description is the first thing you see

**Combined factors:**
- Weak description (Hypothesis A) makes skill hard to discover
- Progressive disclosure tradeoff (Hypothesis B) makes skill hard to use after discovery
- Together these create a "double penalty" reducing autonomy

**Recommended approach:**
1. Fix Hypothesis A first (quick win)
2. Measure improvement (does Claude use skill more?)
3. If still not working, address Hypothesis B
4. If still not working, consider Hypothesis C (pattern limitation)

## 5. Specific Recommendations for claude-mem

### Quick Wins (Hours)

#### 1. Improve trigger keywords: Concrete nouns

**Current description:**
```
Search claude-mem persistent memory for past sessions, observations, bugs fixed,
features implemented, decisions made, code changes, and previous work.
```

**Problems:**
- "observations" is abstract (what's an observation?)
- "previous work" is generic (too broad)
- Missing user language ("what did we do last time?")

**Suggested rewrite:**
```
Search persistent memory for past sessions, bug fixes, feature implementations,
architectural decisions, code changes, and completed work. Use when user asks
"what did we do before?", "did we fix this already?", "how did we implement X?",
or needs historical context about the codebase.
```

**Improvements:**
- "bug fixes" (noun) vs "bugs fixed" (past participle)
- "feature implementations" (concrete) vs "features implemented" (abstract)
- "architectural decisions" (specific) vs "decisions made" (generic)
- Explicit user language examples in quotes

**Even better - add explicit trigger section after frontmatter:**

```markdown
## Auto-Invocation Triggers

This skill automatically activates when Claude detects user questions like:

- "What did we do last session?"
- "Did we fix this bug before?"
- "How did we implement authentication?"
- "What changes were made to auth/login.ts?"
- "What were we working on yesterday?"
- "Show me past decisions about database choice"

Keywords: past work, previous sessions, bug fix history, implementation details,
architectural decisions, code change history, historical context
```

#### 2. Surface capabilities: Show operations in SKILL.md

**Current structure:**
```
## Available Operations
1. Search Observations - Find observations by keyword
2. Search Sessions - Search session summaries
... (8 more with one-line descriptions)
```

**Problem:** No "When to use" statements visible in SKILL.md

**Suggested addition to SKILL.md:**

```markdown
## Available Operations (Quick Reference)

### Full-Text Search
- **Search Observations** - User asks: "How did we implement X?" or "What bugs did we fix?"
- **Search Sessions** - User asks: "What did we accomplish last time?" or "What was the goal?"
- **Search Prompts** - User asks: "Did I ask about this before?" or "What did I request?"

### Filtered Search
- **Search by Type** - User asks: "Show me all bug fixes" or "List features we added"
- **Search by Concept** - User asks: "What patterns did we discover?" or "Show gotchas"
- **Search by File** - User asks: "What changes to auth.ts?" or "History of this file"

### Context Retrieval
- **Get Recent Context** - User asks: "What's been happening?" or "Catch me up"
- **Get Timeline** - User asks: "What was happening around date X?" or "Show me context"
- **Timeline by Query** - User asks: "When did we implement auth?" (search + timeline)

For detailed usage of each operation, see operations/ directory.
```

**Impact:** Claude can make routing decision without reading operations/ files

#### 3. Reduce cognitive load: Simplify decision tree

**Current problem:** 10 operations organized into 4 categories feels complex

**Suggested simplification in SKILL.md:**

```markdown
## Quick Decision Guide

**Step 1: What's the user asking about?**

1. Recent work (last few sessions) → [Get Recent Context](operations/recent-context.md)
2. Specific topic/keyword → [Search Observations](operations/observations.md)
3. Specific file history → [Search by File](operations/by-file.md)
4. Timeline/chronology → [Get Timeline](operations/timeline.md)
5. Other/complex query → Read full guide below

**Step 2: Execute the search** (see operation file for details)

**Step 3: Present results** (see [formatting guide](operations/formatting.md))
```

**Impact:** Reduces decision points from 10 options to 5 common cases

### Medium Effort (Days)

#### 1. Adopt scripts pattern: Executable helpers

**Current pattern:**
- Operations are documentation
- Claude reads operations/X.md → Constructs HTTP call → Executes

**Suggested pattern:**
- Operations are scripts
- Claude reads SKILL.md → Runs script with `--help` → Executes

**Example: scripts/search-observations.py**

```python
#!/usr/bin/env python3
"""
Search claude-mem observations by keyword.

Usage:
    uv run scripts/search-observations.py "authentication" --limit 10 --format index
    uv run scripts/search-observations.py "bug" --project myapp --format full
"""
import click
import httpx

@click.command()
@click.argument('query')
@click.option('--format', default='index', type=click.Choice(['index', 'full']))
@click.option('--limit', default=10)
@click.option('--project', default=None)
def search(query, format, limit, project):
    """Search observations by keyword"""
    params = {'query': query, 'format': format, 'limit': limit}
    if project:
        params['project'] = project

    response = httpx.get('http://localhost:37777/api/search/observations', params=params)
    click.echo(response.text)

if __name__ == '__main__':
    search()
```

**Benefits:**
- Reduces navigation depth (1 hop instead of 2)
- Scripts are self-documenting (`--help`)
- Easier for Claude to discover usage patterns
- Matches the Kalshi pattern

**Effort:** 1-2 days to create 10 scripts + update SKILL.md

#### 2. Rebalance progressive disclosure: Show more, hide less

**Current approach:**
- SKILL.md shows meta-information (97 lines)
- operations/ shows usage patterns (hidden)

**Suggested approach:**
- SKILL.md shows usage patterns (150 lines?)
- scripts/ shows implementation (hidden)

**What to move INTO SKILL.md:**
- "When to use" for each operation (from operations/*.md)
- Common example queries (from common-workflows.md)
- Response format examples (from formatting.md)

**What to move OUT of SKILL.md:**
- Technical notes (port, FTS5 details)
- Performance tips (can be in individual scripts)
- Error handling details (in scripts)

**Effort:** 1 day to reorganize

### Large Changes (Weeks)

#### 1. Change pattern entirely: MCP vs Skills

**If quick and medium efforts don't improve auto-invocation:**

Consider switching from Skill pattern to MCP pattern:

**MCP advantages:**
- Explicitly listed in Claude's tool list (high discoverability)
- Structured function signatures (clear inputs/outputs)
- Better for complex multi-parameter operations

**MCP disadvantages:**
- Requires server process (complexity)
- Context loss between calls (stateless)
- Not git-shareable (server config required)

**Effort:** 1-2 weeks to implement MCP server + test

**Likelihood needed:** LOW (10%)
- Try fixing description first
- Skills should work if implemented well

## 6. Agent Autonomy Assessment

### Auto-Invoked?

**Answer: ❌ No (currently), ✅ Yes (possible with improvements)**

### Why?

**Current state (No):**

1. **Weak trigger keywords** - "observations", "previous work" are too abstract
2. **Generic use cases** - "answering questions about history" matches many tools
3. **Hidden capabilities** - Must navigate to operations/ to understand what's possible
4. **High cognitive load** - 10 operations in 4 categories requires multiple decisions

**After improvements (Possible Yes):**

1. **Strong trigger keywords** - Explicit list with user language examples
2. **Specific use cases** - Clear mapping from user question to operation
3. **Visible capabilities** - "When to use" statements in SKILL.md
4. **Low cognitive load** - Quick decision guide with 5 common cases

### Why Kalshi Works (Inference)

**Kalshi is auto-invoked (likely) because:**

1. **Rich trigger keywords in description:**
   - "prediction markets, Kalshi markets, betting odds, market prices"
   - These are concrete, specific nouns
   - High match probability when user asks about these topics

2. **Clear capability visibility:**
   - 10 scripts listed with "When to use" statements
   - No hidden navigation required
   - One-hop execution path

3. **Low cognitive load:**
   - User question → Matching script (direct mapping)
   - No intermediate routing decisions

4. **Explicit design for autonomy:**
   - "Don't read scripts unless absolutely needed"
   - `--help` flag for discovery
   - Self-contained tools

### Confidence

**Confidence in autonomy assessment: HIGH (80%)**

**Why High:**

1. **Clear comparison** shows specific gaps in claude-mem implementation
2. **Design patterns** align with autonomy principles
3. **Quick wins identified** that directly address the gaps

**Why not 100%:**

1. No official documentation on skill auto-invocation mechanism
2. No empirical testing of improvements yet
3. Possible that pattern itself has limitations

### Evidence from README

**Beyond-MCP README evidence supporting auto-invocation:**

1. **Explicit claim:** "Model-Invoked - Claude autonomously activates based on context"
2. **Keyword detection:** "The skill automatically activates when Claude detects keywords like:"
3. **Flow diagram:** "Claude (detects keyword) -> Loads SKILL.md -> Runs relevant script"
4. **Usage examples:** "# Claude will auto-detect and use the skill"
5. **Feature list:** "Want autonomous skill discovery"

**Quality of evidence: MEDIUM**

- Claims are clear and specific
- No empirical proof (logs, metrics, screenshots)
- Consistent pattern across repository
- Professional presentation suggests testing

**Inference:** Auto-invocation is likely real but depends on proper implementation

---

## Summary & Next Steps

### Key Findings

1. **Root cause:** Weak trigger keywords and hidden capabilities
2. **Quick fix:** Rewrite SKILL.md description with concrete triggers
3. **Pattern validation:** Kalshi demonstrates skills CAN be auto-invoked
4. **Confidence:** HIGH that improvements will help

### Recommended Actions

**Phase 1: Quick Wins (2-4 hours)**
1. Rewrite SKILL.md description with concrete trigger keywords
2. Add explicit "Auto-Invocation Triggers" section with user language examples
3. Add "When to use" statements inline for each operation in SKILL.md

**Phase 2: Validation (1-2 days)**
1. Test with real user questions: "what did we do last time?"
2. Observe if Claude invokes skill autonomously
3. Measure improvement vs baseline

**Phase 3: Medium Effort (if needed)**
1. Create executable scripts (adopt Kalshi pattern)
2. Rebalance progressive disclosure (show usage, hide implementation)
3. Simplify decision tree (5 common cases instead of 10 operations)

**Phase 4: Pattern Switch (if still needed)**
1. Consider MCP implementation
2. Compare discoverability metrics
3. Choose best pattern for claude-mem use case

### Confidence in Recommendations

**Confidence: HIGH (85%)**

- Comparison clearly shows gaps
- Kalshi pattern is proven (in showcase repo)
- Quick wins are low-risk, high-reward
- Medium effort changes are well-understood

**Risk factors:**
- No official documentation on skill matching algorithm
- Beyond-MCP might be showcase (not production-tested)
- Pattern limitations can't be ruled out without trying

**Mitigation:**
- Start with quick wins (low investment)
- Measure impact before medium effort changes
- Keep MCP as backup plan

---

**Document version:** 1.0
**Date:** 2025-11-10
**Agent:** Sub-Agent 4 (Skill Analysis)
**Status:** Analysis complete, recommendations ready for implementation
