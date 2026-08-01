---
name: beyond-mcp-v2
description: 'Description: "Access Kalshi prediction market data including market
  prices, orderbooks, trades, events, and series information. Use when the user asks
  about prediction markets, Kalshi markets, betting odds, market prices, or needs
  to search or analyze prediction market data."'
---

# Skill Approach Analysis

## 1. Skill Description Comparison

### Kalshi-Markets Skill (beyond-mcp)
**Description:** "Access Kalshi prediction market data including market prices, orderbooks, trades, events, and series information. Use when the user asks about prediction markets, Kalshi markets, betting odds, market prices, or needs to search or analyze prediction market data."

**Trigger keywords:** prediction markets, Kalshi markets, betting odds, market prices, search prediction market data, analyze prediction market data

**Capability visibility:** HIGH
- Explicit list of capabilities in description (market prices, orderbooks, trades, events, series)
- 10 scripts named directly in SKILL.md with "When to use" for each
- Clear progressive disclosure pattern with script names visible upfront

**Lines in SKILL.md:** 71 (compact but comprehensive)

### Claude-Mem Search Skill (current)
**Description:** "Search claude-mem persistent memory for past sessions, observations, bugs fixed, features implemented, decisions made, code changes, and previous work. Use when answering questions about history, finding past decisions, or researching previous implementations."

**Trigger keywords:** past sessions, observations, bugs fixed, features implemented, decisions made, code changes, previous work, history, past decisions, previous implementations

**Capability visibility:** MEDIUM-HIGH
- Good list of capabilities in description
- "When to Use This Skill" section lists 8 specific user questions
- BUT: Operations are hidden behind links - not immediately visible
- Quick Decision Guide requires loading skill first

**Lines in SKILL.md:** 96 (more verbose, more indirection)

### Comparison
**Winner for discoverability:** Kalshi-Markets

**Key differences:**
1. **Frontmatter description length:**
   - Kalshi: 3 sentences, very concrete (market prices, orderbooks, trades)
   - Claude-mem: 2 sentences, somewhat abstract (observations, decisions, code changes)

2. **Trigger keyword specificity:**
   - Kalshi: Domain-specific terms (Kalshi, prediction markets, betting odds)
   - Claude-mem: Generic dev terms (bugs, features, history, decisions)

3. **Capability surfacing:**
   - Kalshi: ALL 10 scripts listed directly in SKILL.md with "When to use"
   - Claude-mem: 9 operations hidden behind links in operations/ subdirectory

4. **Progressive disclosure balance:**
   - Kalshi: Script names + purpose visible; implementation hidden
   - Claude-mem: Operation names + links visible; details hidden behind two layers

**Missing from claude-mem:**
1. Direct listing of all capabilities in main SKILL.md (not behind links)
2. Concrete examples in description (e.g., "search for bug #1234" vs abstract "bugs fixed")
3. Simpler mental model (10 scripts vs 9 operations + workflows + formatting)
4. More specific domain triggers (claude-mem, persistent memory, session history)

## 2. Implementation Pattern Analysis

**Kalshi pattern:**
- SKILL.md structure:
  - Frontmatter with rich description and triggers
  - Direct list of 10 scripts with one-line purposes
  - Architecture section explaining self-contained pattern
  - Quick start with command examples
- Scripts approach:
  - Each script is 150-200 lines, self-contained
  - Embedded HTTP client in every script
  - All support --help and --json
  - No dependencies between scripts
- Progressive disclosure:
  - First layer (SKILL.md): Script names and purposes (71 lines)
  - Second layer (scripts/): Full implementation (150-200 lines each)
  - Total: ~1500 lines across 10 files, load individually

**Claude-mem pattern:**
- SKILL.md structure:
  - Frontmatter with description
  - "When to Use" section with 8 examples
  - "Quick Decision Guide" with links
  - "Available Operations" with 10 links
  - "Common Workflows" link
  - "Response Formatting" link
  - Technical notes, performance tips, error handling
- Operations docs:
  - 9 operation files (1.4-6.2k each)
  - 2 meta files (workflows, formatting)
  - Each operation: When to use, curl command, parameters, response structure, use cases, presentation format
- Progressive disclosure:
  - First layer (SKILL.md): Operation categories and links (96 lines)
  - Second layer (operations/*.md): Full instructions (1.4-6.2k per file)
  - Total: ~30k total characters across 12 files, unclear which to load first

**Better for autonomy:** Kalshi pattern

**Reasoning:**
1. **Cognitive load:** 10 scripts with clear names vs 9 operations + 2 meta files + decision trees
2. **Action clarity:** "Run status.py" vs "Read operations/recent-context.md then run curl command"
3. **Self-contained execution:** Scripts have embedded logic; operations require curl + parsing
4. **Discovery path:** Kalshi shows all tools immediately; claude-mem requires reading links to understand capabilities
5. **Token efficiency:** Kalshi loads 150-200 lines per task; claude-mem must load SKILL.md (96) + operation file (1.4-6.2k) + possibly formatting.md (6.2k)

## 3. Auto-Invocation Evidence

**README claims:** "Model-Invoked - Claude autonomously activates based on context" and "The skill automatically activates when Claude detects keywords like: prediction markets, Kalshi markets, betting odds, market prices"

**Evidence found:**
1. **Claim source:** README.md line 7 and lines 19-23
2. **Mechanism described:** "Claude (detects keyword) -> Loads SKILL.md -> Runs relevant script -> Kalshi API"
3. **No testing evidence:** No test logs, no metrics, no user reports, no examples of auto-invocation
4. **No verification code:** No tests that verify auto-invocation works
5. **Marketing language:** "Model-Invoked", "autonomously activates", "automatically activates" are aspirational claims
6. **Keyword list provided:** This suggests the author WANTS auto-invocation but doesn't prove it works

**Actual evidence pattern:**
- This is a DEMONSTRATION/EXAMPLE project in beyond-mcp
- Claims are based on Claude Code skill design pattern expectations
- No empirical evidence of autonomous invocation
- Keywords in description are BEST PRACTICE, not proof of auto-invocation

**Confidence in claim:** LOW

**Reality check:** The skill follows best practices for discoverability (good trigger keywords, clear description), but there's no evidence that Claude Code actually auto-invokes skills reliably. The claims are likely based on:
1. Understanding of how skill descriptions work
2. Belief that good keywords = auto-invocation
3. Marketing the skill approach vs MCP approach

## 4. Root Cause Analysis: Why Claude Doesn't Use claude-mem

### Hypothesis A: Weak Description
**Evidence:**
- Description uses generic terms (bugs, features, history) that apply to ANY development work
- Missing domain-specific triggers like "claude-mem", "persistent memory", "session history"
- No concrete examples in description (e.g., "find bug #1234 details" vs "bugs fixed")
- Trigger keywords compete with native Claude capabilities (Claude already remembers recent conversation)

**Fix effort:** LOW - Rewrite SKILL.md frontmatter description (1-2 hours)

**Likelihood:** HIGH

This is the most likely root cause. Compare:
- Kalshi: "prediction markets, Kalshi markets, betting odds" (unique, specific domain)
- Claude-mem: "bugs fixed, features implemented, decisions made" (generic, applies to any dev work)

When user says "what bugs did we fix?", Claude can answer from current session context. No trigger to think "I need to check persistent memory across sessions."

### Hypothesis B: Progressive Disclosure Tradeoff
**Evidence:**
- SKILL.md shows 9 operations but hides details behind links
- User must ask about "past work" -> Claude loads SKILL.md -> Claude must read operations/*.md to know what's possible
- Compare to Kalshi: User asks about "markets" -> Claude loads SKILL.md -> Claude sees all 10 scripts immediately
- claude-mem requires TWO reads (SKILL.md + operation file), Kalshi requires ONE read (SKILL.md lists everything)
- Token burden: claude-mem forces loading SKILL.md (96 lines) first, then operations (1.4-6.2k), total 1.5-6.3k
- Token burden: Kalshi loads SKILL.md (71 lines), done - all tools visible

**Fix effort:** MEDIUM - Rebalance what's in SKILL.md vs operations/ (4-8 hours)

**Likelihood:** MEDIUM

This is a contributing factor. Even if Claude loads the skill, it doesn't immediately know what claude-mem can DO without reading additional files. Kalshi shows all capabilities in 71 lines.

### Hypothesis C: Pattern Limitation
**Evidence:**
- Skills are passive documentation, not active agents
- Claude must CHOOSE to invoke skill tool
- No evidence that ANY skill reliably auto-invokes (including Kalshi)
- MCP tools appear in tool list automatically; skills require explicit invocation decision
- Skill pattern depends on LLM detecting keywords and deciding to load skill
- This is an LLM routing problem, not a documentation problem

**Fix effort:** HIGH - Change to MCP server pattern or slash command pattern (2-4 weeks)

**Likelihood:** MEDIUM

This is possible but less likely to be the PRIMARY cause. The skill pattern CAN work if the description is good enough. The issue is likely that claude-mem's description isn't triggering the "load this skill" decision.

**Most likely root cause:** A (Weak Description)

**Combined factors:** A + B (Weak description AND too much hidden behind links)

The description doesn't clearly differentiate claude-mem's persistent memory from Claude's native conversation memory. Users ask "what did we do?" and Claude answers from current session context, never thinking to check a persistent database across sessions. Add to this that even IF Claude loads the skill, it must read additional files to understand capabilities, making it less likely to succeed.

## 5. Specific Recommendations for claude-mem

### Quick Wins (Hours)

#### 1. Rewrite SKILL.md frontmatter description with unique triggers
**Current:**
```yaml
description: Search claude-mem persistent memory for past sessions, observations, bugs fixed, features implemented, decisions made, code changes, and previous work. Use when answering questions about history, finding past decisions, or researching previous implementations.
```

**Recommended:**
```yaml
description: Search claude-mem's persistent cross-session memory database to find work from previous conversations. Access past session summaries, bug fixes, feature implementations, and decisions that are NOT in the current conversation context. Use when user asks about work from days/weeks/months ago, previous sessions, or "did we already solve this?". Searches observations, session summaries, and user prompts across the entire project history stored in the PM2-managed database.
```

**Key improvements:**
- Add "claude-mem" to description (unique trigger)
- Add "cross-session memory database" (differentiates from current conversation)
- Add "NOT in current conversation context" (clear value prop)
- Add "days/weeks/months ago" (temporal trigger)
- Add "previous sessions" (specific trigger phrase)
- Add "did we already solve this?" (concrete user question)
- Add "PM2-managed database" (shows it's a real system, not just Claude's memory)

#### 2. Surface all 9 operations directly in SKILL.md
**Current pattern:** Links to operations/*.md files

**Recommended pattern:** List all operations with one-line purposes, like Kalshi does

```markdown
## Available Operations

### Search Operations
- **observations.md** - Full-text search across all observations (bugs, features, decisions)
- **sessions.md** - Search session summaries to find what was accomplished when
- **prompts.md** - Find what users have asked about in past sessions

### Filtered Search
- **by-type.md** - Filter by observation type (bugfix, feature, refactor, decision, discovery, change)
- **by-concept.md** - Find observations tagged with specific concepts (problem-solution, how-it-works, gotcha)
- **by-file.md** - Find all work related to a specific file path across all sessions

### Timeline & Context
- **recent-context.md** - Get last N sessions with summaries and observations
- **timeline.md** - Get chronological context around a specific point in time (before/after)
- **timeline-by-query.md** - Search first, then get timeline context around best match

For detailed instructions on any operation, read the corresponding file in operations/.
```

**Benefits:**
- Shows ALL capabilities in ~15 lines vs requiring link clicking
- Claude can immediately see what's possible without reading 9 separate files
- Pattern matches Kalshi's successful approach
- Still preserves progressive disclosure (details in operations/)

#### 3. Add concrete examples to trigger phrases
**Current:** "Use when answering questions about history, finding past decisions"

**Recommended additions:**
```markdown
## Trigger Phrases

Use this skill when you see phrases like:
- "Did we already fix this bug?"
- "How did we solve X last time?"
- "What did we do in yesterday's session?"
- "Show me all authentication-related changes"
- "What features did we add last week?"
- "Why did we choose this approach?" (for decisions made in past sessions)
- "What files did we modify when we added X?"
```

**Benefits:**
- Concrete user phrases vs abstract categories
- Claude can pattern-match actual user language
- Clear differentiation from current-session questions

### Medium Effort (Days)

#### 4. Adopt embedded curl commands pattern
**Current pattern:** operations/*.md files show curl commands; Claude must read file then execute command

**Recommended pattern:** Create scripts/ directory with simple wrapper scripts, like Kalshi

```bash
scripts/
├── recent.sh          # Wraps curl for recent context
├── search-obs.sh      # Wraps curl for observation search
├── search-session.sh  # Wraps curl for session search
├── by-type.sh         # Wraps curl for type-based search
└── timeline.sh        # Wraps curl for timeline
```

**Benefits:**
- Single action: `./scripts/recent.sh --limit 5` vs read operations/recent-context.md then construct curl
- Matches Kalshi's successful pattern
- Reduces cognitive load and steps
- Each script can include --help and --json like Kalshi

**Downside:**
- More files to maintain
- Duplicates some logic from operations/*.md

#### 5. Reduce SKILL.md line count to <80 lines
**Current:** 96 lines with lots of sections

**Recommended:** Consolidate to match Kalshi's 71-line approach

Remove from main SKILL.md and move to operations/README.md:
- Common Workflows section (already in operations/common-workflows.md)
- Response Formatting section (already in operations/formatting.md)
- Technical Notes (can be in operations/help.md)
- Performance Tips (can be in operations/help.md)
- Error Handling (can be in operations/help.md)

Keep in SKILL.md:
- Description (enhanced)
- When to Use (enhanced with concrete phrases)
- Quick Decision Guide (simplified)
- Available Operations (expanded to show all 9 with purposes)
- Quick examples

**Benefits:**
- Faster load time = more likely Claude loads it
- Clearer signal-to-noise ratio
- Matches successful pattern

### Large Changes (Weeks)

#### 6. Convert to MCP server pattern
**Effort:** 2-4 weeks

**Rationale:**
- MCP tools appear in Claude's tool list automatically
- No routing/invocation decision required
- Skills require Claude to decide "should I load this skill?"
- MCP bypasses this decision point

**Tradeoff:**
- Loses context preservation benefit of skills
- Requires running server (already have PM2 worker, so not a huge change)
- Better discovery but loses the skill pattern's conversation flow

**Recommendation:** Try Quick Wins first before this nuclear option

## 6. Agent Autonomy Assessment

**Auto-invoked:** ❌ No (for both Kalshi and claude-mem)

**Why:**

1. **No empirical evidence:** Kalshi README claims "model-invoked" and "autonomously activates" but provides zero evidence:
   - No test logs showing autonomous invocation
   - No metrics on auto-invocation success rate
   - No user testimonials or examples
   - No code that verifies auto-invocation behavior

2. **Skills are passive:** The skill pattern is documentation that Claude CAN load, not tools that Claude MUST see. The invocation flow is:
   - User says something
   - Claude decides "should I load a skill?"
   - Claude searches available skills
   - Claude matches description keywords
   - Claude invokes Skill tool
   - Claude reads SKILL.md
   - Claude uses the skill

   This is a 5-step process with a critical decision point at step 2. Compare to MCP:
   - User says something
   - Claude sees all MCP tools in tool list
   - Claude uses appropriate tool

   MCP is 2 steps with no decision point.

3. **Keywords are necessary but not sufficient:** Good keywords in the description (like Kalshi has) make auto-invocation MORE LIKELY but don't guarantee it. They increase the probability that step 2 above ("should I load a skill?") results in "yes."

4. **Beyond-MCP is aspirational:** The repository is called "beyond-mcp" and is demonstrating alternatives to MCP. The claims about auto-invocation are ASPIRATIONAL (this is how skills SHOULD work) not EMPIRICAL (this is how skills DO work).

**Confidence:** HIGH

**Evidence-based conclusion:**
- Kalshi skill has BETTER discoverability than claude-mem (stronger keywords, clearer capabilities)
- This makes it MORE LIKELY to be auto-invoked
- But there's no evidence EITHER skill reliably auto-invokes
- The skill pattern depends on LLM routing decisions that are probabilistic, not deterministic
- claude-mem's weak description makes it LESS LIKELY to win the routing lottery
- Improving the description per Quick Wins above will increase probability but not guarantee auto-invocation

**Bottom line:** Fix the description to match Kalshi's quality, but don't expect magic. Skills are inherently less discoverable than MCP tools because they require an extra routing decision.
