---
name: explore-codebase
description: 'Find all files relevant to a query with orthogonal exploration for comprehensive coverage. Returns topic-specific overview + file list with line ranges. Uses parallel agents for thorough+ levels to ensure nothing is missed.'
context: fork
---

**User request**: $ARGUMENTS

Orchestrate codebase exploration agents to find all files relevant to a query, then synthesize into a unified reading list.

**Loop**: Determine thoroughness → [Quick/Medium: single agent → return] | [Thorough+: Create orchestration file → Decompose → Launch Wave 1 → Collect findings → Cross-reference → Evaluate gaps → [Gap-fill if needed] → Refresh context → Synthesize → Output]

**Orchestration file** (thorough+ only): `/tmp/explore-orchestration-{topic-slug}-{YYYYMMDD-HHMMSS}.md`

**You do NOT read source files** - you orchestrate agents and synthesize their findings into a unified reading list. The main agent reads the files after you return.

---

## Thoroughness Level

**FIRST**: Determine thoroughness before exploring. Parse from natural language or auto-select.

**Auto-selection**:
- Single entity lookup ("where is X?") → quick
- Single bounded feature/bug → medium
- Multi-area feature, interaction queries → thorough
- "comprehensive"/"all"/"architecture"/"audit" → very-thorough

| Level | Exploration Strategy |
|-------|---------------------|
| **quick** | Single agent, no orchestration file, return agent output directly |
| **medium** | Single agent, no orchestration file, return agent output directly |
| **thorough** | Orchestration file, orthogonal agents (2-3), cross-reference, optional gap-fill |
| **very-thorough** | Orchestration file, orthogonal agents (3-4), cross-reference, gap-fill wave |

**Topic-slug format**: Extract 2-4 key terms, lowercase, replace spaces with hyphens. Example: "authentication flow" → `authentication-flow`

State: `**Thoroughness**: [level] — [reason]` then proceed.

---

## Quick / Medium Flow

### 1. Launch single agent

```
Task(subagent_type: "vibe-workflow:codebase-explorer", prompt: "$ARGUMENTS")
```

### 2. Return agent output directly

When agent returns, its output becomes your output. No synthesis needed.

---

## Thorough / Very-Thorough Flow

### Phase 1: Initial Setup

#### 1.1 Get timestamp & create todo list

Run: `date +%Y%m%d-%H%M%S` → for filename and timestamps

**Starter todos** (seeds - list grows during decomposition):

```
- [ ] Create orchestration file; done when file created
- [ ] Topic decomposition→log; done when angles identified
- [ ] (expand: agent assignments as decomposition reveals)
- [ ] Launch Wave 1 agents; done when all agents spawned
- [ ] Collect Agent 1→log; done when findings written
- [ ] Collect Agent 2→log; done when findings written
- [ ] (expand: more agents as needed)
- [ ] Cross-reference→log; done when duplicates/conflicts resolved
- [ ] Evaluate gaps→log; done when gaps classified
- [ ] (expand: gap-fill if continuing)
- [ ] Refresh: read full orchestration file
- [ ] Synthesize→unified reading list; done when all files deduplicated + prioritized
```

**Critical todos** (never skip):
- `→log` after EACH agent completion
- `Refresh:` ALWAYS before synthesis

#### 1.2 Create orchestration file

Path: `/tmp/explore-orchestration-{topic-slug}-{YYYYMMDD-HHMMSS}.md`

```markdown
# Codebase Exploration Orchestration: {topic}
Timestamp: {YYYYMMDD-HHMMSS}
Thoroughness: {level}

## Exploration Query
{Original query}

## Topic Decomposition
- Core topic: {main thing to find}
- Angles to explore: (populated in Phase 2)
- Expected agent count: {based on level}

## Agent Assignments
(populated in Phase 2)

## Agent Status
(updated as agents complete)

## Collected Findings
(populated as agents return - includes OVERVIEW and FILES TO READ from each)

## Cross-Reference Analysis
(populated after all agents return)

## Gap Evaluation
(populated after cross-reference)

## Unified Reading List
(populated in synthesis)
```

### Phase 2: Decompose & Assign

#### 2.1 Decompose into orthogonal angles

**Standard angles for codebase exploration:**

| Angle | Focus | Example Scope |
|-------|-------|---------------|
| **Implementation** | Core logic files | "Files that implement {topic} behavior" |
| **Usage** | Callers, integration points | "Files that call/use {topic}" |
| **Tests** | Test files, fixtures | "Test files for {topic}" |
| **Config** | Configuration, environment | "Config files affecting {topic}" |

**Decomposition rules:**
- thorough: 2-3 angles (usually Implementation + Usage + Tests)
- very-thorough: 3-4 angles (all four)
- Each angle gets explicit boundaries to prevent overlap

**Orthogonality check**: Before assigning agents, verify no two angles would naturally search the same files.

#### 2.2 Plan agent assignments with boundaries

| Angle | Focus | Explicitly EXCLUDE |
|-------|-------|-------------------|
| Implementation | Core {topic} files | callers, tests, config |
| Usage | Files that call {topic} | core implementation, tests, config |
| Tests | Test files for {topic} | implementation, callers, config |
| Config | Config affecting {topic} | implementation, callers, tests |

#### 2.3 Expand todos for each agent

```
- [x] Topic decomposition→log; angles identified
- [ ] Agent 1: implementation angle; done when core files found
- [ ] Agent 2: usage angle; done when callers identified
- [ ] Agent 3: tests angle; done when test files found
- [ ] Launch Wave 1 agents (parallel); done when all spawned
- [ ] Collect Agent 1→log; done when findings written
- [ ] Collect Agent 2→log; done when findings written
- [ ] Collect Agent 3→log; done when findings written
- [ ] Cross-reference→log; done when duplicates/conflicts resolved
...
```

#### 2.4 Update orchestration file

```markdown
## Topic Decomposition
- Core topic: {topic}
- Angles identified:
  1. Implementation: {what this covers}
  2. Usage: {what this covers}
  3. Tests: {what this covers}

## Agent Assignments
| Agent | Angle | Prompt | Status |
|-------|-------|--------|--------|
| 1 | Implementation | "{prompt}" | Pending |
| 2 | Usage | "{prompt}" | Pending |
| 3 | Tests | "{prompt}" | Pending |
```

### Phase 3: Launch Parallel Agents

#### 3.1 Launch agents in single message

Use Task tool with `subagent_type: "vibe-workflow:codebase-explorer"` for each angle. **Launch all agents in parallel** (single message with multiple Task tool calls).

**Agent prompt template:**
```
{Specific exploration focus for this angle}

YOUR ASSIGNED SCOPE:
- {what to explore}
- {specific patterns or areas}

DO NOT EXPLORE (other agents cover these):
- {angles assigned to other agents}

Thoroughness within scope: medium
```

**Example for "authentication" query (thorough):**

Agent 1 (Implementation):
```
Find core authentication implementation files.

YOUR ASSIGNED SCOPE:
- Auth service/module files
- Token generation, validation logic
- Session management implementation
- Password hashing, credential verification

DO NOT EXPLORE (other agents cover these):
- Files that CALL auth (usage patterns)
- Test files
- Config files

Thoroughness within scope: medium
```

Agent 2 (Usage):
```
Find files that use/call authentication.

YOUR ASSIGNED SCOPE:
- Route handlers that require auth
- Middleware that checks auth
- Services that depend on auth context
- Integration points with auth

DO NOT EXPLORE (other agents cover these):
- Core auth implementation files
- Test files
- Config files

Thoroughness within scope: medium
```

Agent 3 (Tests):
```
Find authentication test files.

YOUR ASSIGNED SCOPE:
- Unit tests for auth
- Integration tests for auth flows
- Test fixtures and mocks for auth
- E2E tests involving authentication

DO NOT EXPLORE (other agents cover these):
- Core auth implementation
- Files that use auth
- Config files

Thoroughness within scope: medium
```

#### 3.2 Update orchestration file after EACH agent completes

**After EACH agent returns**, immediately write findings:

```markdown
## Collected Findings

### Agent 1: Implementation
**Status**: Complete
**Files Found**: {count}

#### OVERVIEW (from agent)
{paste agent's overview}

#### FILES TO READ (from agent)
MUST READ:
- {paste agent's must-read list}

SHOULD READ:
- {paste agent's should-read list}

REFERENCE:
- {paste agent's reference list}

#### OUT OF SCOPE (from agent)
- {paste any out-of-scope discoveries}

---

### Agent 2: Usage
...
```

**Mark the write-to-log todo complete after each write.**

### Phase 4: Cross-Reference & Evaluate Gaps

#### 4.1 Analyze findings across agents

After ALL agents complete, analyze for:

- **Duplicates**: Same file in multiple agents' lists
- **Overlapping ranges**: Same file with different line ranges
- **Out-of-scope discoveries**: Items agents noted but didn't pursue
- **Coverage gaps**: Obvious areas no agent covered
- **Priority conflicts**: Same file at different priority levels

#### 4.2 Update orchestration file with cross-reference

```markdown
## Cross-Reference Analysis

### Duplicates Found
- {file}: appeared in Agent 1 (MUST READ) and Agent 3 (SHOULD READ) → keep MUST READ
- {file}: appeared in Agent 1 (:50-100) and Agent 2 (:80-150) → merge to :50-150

### Out-of-Scope Discoveries (need follow-up?)
- Agent 1 noted: {discovery} → excluded because: {reason}
- Agent 2 noted: {discovery} → excluded because: {reason}

### Coverage Check
- [ ] Core entry points covered?
- [ ] Error handling paths covered?
- [ ] Configuration dependencies identified?
- [ ] Test coverage visible?

### Gaps Identified
- {Gap 1}: {why it's a gap}
- {Gap 2}: {why it's a gap}
```

#### 4.3 Evaluate gaps

```markdown
## Gap Evaluation

### Gaps Requiring Follow-up
- [ ] {Gap}: {specific - e.g., "No agent explored error handling paths"}

### Gaps to Note (don't pursue)
- {Gap}: {why minor - e.g., "Logging files not critical for understanding topic"}

### Decision
- Gaps requiring follow-up: {count}
- **Action**: {LAUNCH GAP-FILL | PROCEED TO SYNTHESIS}
```

**Gap-fill rules:**
- thorough: only for obvious critical gaps (missing core area)
- very-thorough: for any identified gaps
- Maximum 1-2 gap-fill agents

#### 4.4 Launch gap-fill (if needed)

**Gap-fill prompt:**
```
Fill exploration gap: {specific gap}

Context from initial exploration:
- Already found: {summary of files from initial agents}
- Gap identified: {what's missing}

Focus narrowly on this gap. Don't re-explore already-covered areas.

Thoroughness: medium
```

After gap-fill agents return, write findings to orchestration file and update cross-reference.

### Phase 5: Synthesize Unified Reading List

#### 5.1 Refresh context (MANDATORY)

**CRITICAL**: Read the FULL orchestration file using Read tool to restore ALL agent findings into context.

```
- [x] Refresh context: read full orchestration file  ← Must complete BEFORE synthesis
- [ ] Synthesize unified reading list
```

**Why this matters**: By this point, findings from multiple agents have been written to the file. Context degradation means details may have faded. Reading the full file brings all findings into recent context.

#### 5.2 Generate unified reading list

**Only after completing 5.1** - synthesize all agent findings:

```markdown
## OVERVIEW

[Merged overview combining insights from all agents. 150-400 words.
Describe: file organization, relationships between areas, entry points, data flow.
Synthesize structural knowledge from all angles explored.]

## FILES TO READ

MUST READ:
- path/file.ext:lines - [reason]
...

SHOULD READ:
- path/file.ext:lines - [reason]
...

REFERENCE:
- path/file.ext - [reason]
...

## EXPLORATION SUMMARY

| Angle | Agent | Files Found | Key Discovery |
|-------|-------|-------------|---------------|
| Implementation | 1 | N | {1-liner} |
| Usage | 2 | N | {1-liner} |
| Tests | 3 | N | {1-liner} |
| Gap-fill | 4 | N | {1-liner} |

**Gaps noted but not explored**: {list or "none"}

---
Orchestration file: {path}
```

**Deduplication rules:**
- Same file from multiple agents → keep highest priority, note "(multiple agents)"
- Overlapping line ranges → merge into single range (union)
- Conflicting priorities → use higher priority (MUST > SHOULD > REFERENCE)

#### 5.3 Mark all todos complete

---

## Key Principles

| Principle | Rule |
|-----------|------|
| Thoroughness first | Determine level before any exploration |
| Write after each agent | Write to orchestration file after EACH agent |
| Todos with write-to-log | Each agent collection gets a write-to-orchestration-file todo |
| Parallel launch | All initial agents in single message |
| Cross-reference | Analyze for duplicates, gaps, conflicts after agents return |
| Limited gap-fill | At most 1-2 gap-fill agents, not unbounded |
| **Context refresh** | **Read full orchestration file BEFORE synthesis - non-negotiable** |
| No source file reads | You orchestrate and synthesize - main agent reads files after |

**Log Pattern Summary**:
1. Create orchestration file at start
2. Add write-to-log todos after each agent collection
3. Write findings after EVERY agent returns
4. "Refresh context: read full orchestration file" todo before synthesis
5. Read FULL file before synthesis (restores all context)

## Never Do

- Read source files yourself (you synthesize agent findings, not file contents)
- Skip write-to-log todos (every agent completion must be written)
- Synthesize without completing "Refresh context" todo first
- Launch agents sequentially when they could be parallel
- Skip cross-reference step for thorough+
- Launch unbounded gap-fill waves
- Let agents explore overlapping areas
