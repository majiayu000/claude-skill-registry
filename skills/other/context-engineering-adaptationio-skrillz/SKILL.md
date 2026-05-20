---
name: context-engineering
description: Optimize Claude Code context usage through monitoring, reduction strategies, progressive disclosure, planning/execution separation, and file-based optimization. Task-based operations for context window management, token efficiency, and maintaining conversation quality. Use when managing token costs, optimizing context usage, preventing context overflow, or improving multi-turn conversation quality.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
---

# Context Engineering

## Overview

context-engineering provides systematic strategies for optimizing Claude Code context window usage. It helps you monitor token consumption, reduce context load, design context-efficient skills, and apply proven optimization patterns.

**Purpose**: Maximize Claude Code effectiveness while managing token costs and maintaining conversation quality

**The 5 Context Optimization Operations**:
1. **Monitor Context Usage** - Track token consumption, identify heavy consumers
2. **Reduce Context Load** - Remove stale content, minimize loaded files
3. **Optimize Skill Design** - Progressive disclosure, efficient reference loading
4. **Separate Planning/Execution** - Keep execution context clean
5. **File-Based Strategies** - Externalize large data (95% token savings)

**Key Benefits**:
- **29-39% performance improvement** with context editing strategies
- **95% token savings** using file-based approaches for large data
- **Sustained quality** in multi-turn conversations
- **Cost reduction** through efficient token usage
- **Prevention** of context overflow and conversation drift

**Context Window Sizes** (2025):
- Sonnet 4/4.5: 200k tokens (standard), 500k-1M (beta for Tier 4)
- Auto-compaction: Triggers around 80% usage (~160k for 200k window)

## When to Use

Use context-engineering when:

1. **Approaching Context Limits** - Context usage >60-70%, need to optimize before hitting limits
2. **Building Large Skills** - Creating skills with extensive documentation, need efficient loading strategies
3. **Token Cost Management** - Reducing API costs through optimization
4. **Multi-Turn Conversations** - Maintaining coherence across extended sessions
5. **Skill Design Phase** - Planning context-efficient architecture from start
6. **Performance Optimization** - Improving response quality and latency
7. **Conversation Quality** - Preventing drift and maintaining focus
8. **MCP Integration** - Managing context from Model Context Protocol servers
9. **Large Data Handling** - Working with extensive datasets or outputs

## Prerequisites

- Understanding of Claude context windows
- Access to context monitoring (Claude Code `/context` command)
- Familiarity with progressive disclosure pattern
- Skills under development or optimization

## Operations

### Operation 1: Monitor Context Usage

**Purpose**: Track token consumption, identify context-heavy elements, and detect optimization opportunities

**When to Use This Operation**:
- Beginning of optimization effort (baseline measurement)
- During development (continuous monitoring)
- When approaching context limits (>60-70% usage)
- Investigating performance issues

**Process**:

1. **Check Current Context Usage**
   ```
   Use /context command in Claude Code to view:
   - Total tokens used
   - Percentage of context window
   - Files loaded
   - Recent tool calls
   ```

2. **Identify Heavy Consumers**
   - Large files loaded (>5,000 tokens each)
   - Extensive conversation history
   - Many tool call results
   - Large CLAUDE.md files

3. **Analyze Usage Patterns**
   - Which files are loaded but rarely referenced?
   - Are all tool results still relevant?
   - Is conversation history necessary?
   - Are there duplicate or redundant contexts?

4. **Document Baseline**
   - Record current token usage
   - Note context-heavy elements
   - Identify optimization targets

5. **Set Optimization Goals**
   - Target token reduction (e.g., reduce by 20%)
   - Performance improvement targets
   - Quality maintenance requirements

**Validation Checklist**:
- [ ] Current context usage measured (tokens and percentage)
- [ ] Context-heavy elements identified (files, history, tool results)
- [ ] Baseline documented for comparison
- [ ] Optimization targets set
- [ ] High-impact optimization opportunities noted

**Outputs**:
- Current context usage metrics
- List of context-heavy elements
- Baseline measurement
- Optimization targets
- Priority optimization opportunities

**Time Estimate**: 10-15 minutes

**Example**:
```
Context Usage Analysis
======================
Current Usage: 145,000 tokens (72% of 200k window)

Heavy Consumers:
1. CLAUDE.md: 25,000 tokens (17%)
2. Large skill files: 40,000 tokens (28%)
   - planning-architect/SKILL.md: 15,000 tokens
   - development-workflow/common-patterns.md: 12,000 tokens
   - review-multi/scoring-rubric.md: 8,000 tokens
3. Conversation history: 30,000 tokens (21%)
4. Tool call results: 20,000 tokens (14%)

Optimization Opportunities:
- Split large CLAUDE.md (25k → 10k target)
- Use references/ loading instead of full files (40k → 15k)
- Clear old tool results (20k → 5k)

Target: Reduce to ~100k tokens (50% of window, 31% reduction)
```

---

### Operation 2: Reduce Context Load

**Purpose**: Remove stale content, minimize loaded files, and reduce token consumption

**When to Use This Operation**:
- Context usage >70% (approaching limits)
- Performance degradation noticed
- Before major operations (clear space)
- Periodic maintenance (every few hours)

**Process**:

1. **Remove Stale Tool Results**
   - Identify old tool call results no longer needed
   - Tool results from exploratory work
   - Superseded information

2. **Minimize File Loading**
   - Only load files actively needed
   - Use Grep instead of Read for searching
   - Load specific sections, not entire files
   - Unload files when done with them

3. **Optimize Conversation History**
   - Context editing auto-clears stale content
   - Summarize long conversations if needed
   - Start fresh session for new major tasks

4. **Reduce CLAUDE.md Size**
   - Keep only essential long-term instructions
   - Move project-specific details to separate files
   - Use CLAUDE.local.md for temporary preferences
   - Target: <5,000 tokens for CLAUDE.md

5. **Apply Progressive Loading**
   - Load overview/index files first
   - Load detailed references only when needed
   - Use skill references/ on-demand loading

**Validation Checklist**:
- [ ] Stale tool results cleared
- [ ] Only necessary files loaded
- [ ] CLAUDE.md size optimized (<5,000 tokens if possible)
- [ ] Progressive loading applied where relevant
- [ ] Context usage reduced measurably

**Outputs**:
- Reduced token count
- Cleaner context window
- List of removed/optimized elements
- New context usage measurement

**Time Estimate**: 15-30 minutes

**Example Reduction**:
```
Before Optimization: 145,000 tokens (72%)

Actions Taken:
1. Cleared 50 old tool results: -15,000 tokens
2. Unloaded 3 large files no longer needed: -18,000 tokens
3. Optimized CLAUDE.md (split to CLAUDE.local.md): -12,000 tokens
4. Used references/ loading instead of full files: -25,000 tokens

After Optimization: 75,000 tokens (37%)

Reduction: 70,000 tokens (48% reduction)
Quality Impact: None - relevant context maintained
```

---

### Operation 3: Optimize Skill Design

**Purpose**: Design context-efficient skills using progressive disclosure, lazy loading, and token-aware architecture

**When to Use This Operation**:
- Planning new skills (design for efficiency from start)
- Refactoring existing skills (improve context efficiency)
- Building large/complex skills (manage context proactively)
- Creating skill ecosystems (coordinate context usage)

**Process**:

1. **Apply Progressive Disclosure**
   - **SKILL.md**: Overview + essentials only (<1,200 lines, ~3,000-5,000 tokens)
   - **references/**: Detailed guides loaded on-demand (300-600 lines each, ~1,000-2,000 tokens)
   - **scripts/**: Automation loaded when needed

   **Token Impact**: 70-80% reduction vs monolithic (5k vs 20k+ tokens)

2. **Design for Lazy Loading**
   - Separate content into focused reference files
   - Each reference file covers one topic
   - Load specific reference, not entire skill
   - Example: Load `references/structure-review-guide.md` not entire review-multi

3. **Optimize File Sizes**
   - SKILL.md target: 800-1,200 lines (2,500-4,000 tokens)
   - Reference files: 300-600 lines (1,000-2,000 tokens each)
   - Keep files focused and concise

4. **Use Token-Efficient Formats**
   - Tables instead of prose (higher information density)
   - Lists instead of paragraphs (more scannable)
   - Code blocks for examples (clear and concise)
   - Quick Reference sections (high-density lookup)

5. **Consider Context Budget**
   - Estimate token usage for skill
   - Simple skill: 3,000-8,000 tokens total
   - Medium skill: 10,000-20,000 tokens total
   - Complex skill: 25,000-40,000 tokens total
   - Design within budget

**Validation Checklist**:
- [ ] Progressive disclosure applied (SKILL.md + references/)
- [ ] SKILL.md <1,200 lines (~4,000 tokens or less)
- [ ] Reference files 300-600 lines each
- [ ] Files focused on single topics (lazy loadable)
- [ ] Token-efficient formats used (tables, lists, code blocks)
- [ ] Estimated total tokens within budget
- [ ] Skill can be partially loaded (references/ on-demand)

**Outputs**:
- Context-efficient skill design
- Token budget estimate
- Progressive disclosure plan
- Reference file organization

**Time Estimate**: 20-40 minutes (during planning phase)

**Example**:
```
Skill Design: api-integration

Token Budget Analysis:
- SKILL.md: 900 lines → ~3,000 tokens
- references/ (3 files):
  - api-guide.md: 400 lines → ~1,300 tokens
  - auth-patterns.md: 350 lines → ~1,200 tokens
  - examples.md: 300 lines → ~1,000 tokens
- README.md: 300 lines → ~1,000 tokens

Total if all loaded: ~7,500 tokens
Typical usage: SKILL.md only → 3,000 tokens (60% savings)
With 1 reference: 3,000 + 1,200 → 4,200 tokens (44% savings)

Progressive Disclosure Impact:
- Monolithic (all in SKILL.md): ~7,500 tokens always loaded
- Progressive (SKILL.md + on-demand refs): 3,000-4,500 tokens typical
- Token Savings: 40-60% depending on usage

Design: ✅ Context-efficient with progressive disclosure
```

---

### Operation 4: Separate Planning from Execution

**Purpose**: Keep execution context clean by separating exploratory planning from focused implementation

**When to Use This Operation**:
- Starting complex development work
- Context getting cluttered with exploration
- Need clean context for implementation
- Before critical/focused work

**Process**:

1. **Planning Phase** (Separate Session)
   - Broad codebase exploration
   - Research and pattern discovery
   - Architecture decisions
   - Task breakdown
   - Output: Plan documents, task lists

   **Characteristics**: High context usage, exploratory, broad

2. **Execution Phase** (Fresh Session)
   - Load plan documents (not exploration history)
   - Focused implementation
   - Specific file operations
   - Minimal context bloat

   **Characteristics**: Clean context, focused, efficient

3. **Session Transition**
   - End planning session when plan complete
   - Save planning artifacts (plans, task lists, decisions)
   - Start new session for execution
   - Load only: plan docs, CLAUDE.md, immediate dependencies

4. **Maintain Clean Execution Context**
   - Don't re-explore during execution
   - Follow plan, don't re-research
   - Load files as needed, unload when done
   - Keep focus on implementation

**Validation Checklist**:
- [ ] Planning and execution in separate sessions (when appropriate)
- [ ] Planning artifacts saved and documented
- [ ] Execution session starts with clean context
- [ ] Only plan docs and essentials loaded for execution
- [ ] No re-exploration during execution
- [ ] Context stays focused on current task

**Outputs**:
- Clean execution context
- Focused implementation
- Reduced context bloat
- Better performance and quality

**Time Estimate**: Planning decision (0-5 min), session management (as needed)

**Example**:
```
Planning Session (Context: 150k tokens, 75% usage):
- Explored 20 files for research
- Analyzed patterns across codebase
- Made architecture decisions
- Created detailed plan
- Output: skill-plan.md (comprehensive)

[End session, save plan]

Execution Session (Context: 30k tokens, 15% usage):
- Load: CLAUDE.md + skill-plan.md + development-workflow
- Context: Clean, focused, 30k tokens
- Implementation: Follow plan, build skill
- Load references as needed (not all at once)

Result: 80% context reduction (150k → 30k)
Quality: Higher (clean context, focused work)
```

**Research Finding**: *"Separating planning from execution keeps implementation context clean"* - confirmed by 2025 best practices

---

### Operation 5: File-Based Optimization

**Purpose**: Externalize large data to temporary files for on-demand analysis, achieving 95% token savings

**When to Use This Operation**:
- Handling large data sets (>5,000 tokens)
- Processing extensive outputs (logs, reports)
- Working with large MCP responses
- Managing generated content

**Process**:

1. **Identify Large Data**
   - Data >5,000 tokens (typically >10,000 characters)
   - Repeated reference to same large content
   - Extensive generated outputs
   - Large MCP server responses

2. **Externalize to Files**
   ```bash
   # Save large data to temp file
   echo "large data here" > /tmp/large-data.txt
   ```

   Instead of keeping in conversation context

3. **Reference File Instead of Content**
   ```markdown
   Large dataset saved to: /tmp/analysis-data.json (50,000 tokens)

   To analyze: Read /tmp/analysis-data.json when needed
   ```

   **Token Impact**: 50,000 tokens → ~500 tokens (95% reduction)

4. **Load On-Demand**
   - Read file only when specific analysis needed
   - Process in chunks if necessary
   - Don't keep full content in context

5. **Clean Up Temp Files**
   - Remove temp files when no longer needed
   - Don't accumulate unused files

**Validation Checklist**:
- [ ] Large data identified (>5,000 tokens)
- [ ] Data externalized to files
- [ ] File paths documented (reference in conversation)
- [ ] On-demand loading used (not full content in context)
- [ ] Token savings measured (before/after)
- [ ] Quality maintained (can access data when needed)
- [ ] Temp files cleaned up when done

**Outputs**:
- Externalized data files
- File path references
- Significant token savings (often 90-95%)
- Maintained data accessibility

**Time Estimate**: 10-20 minutes (setup and management)

**Example**:
```
Scenario: Analyzing large log file (100,000 tokens)

Before Optimization:
- Full log in conversation context: 100,000 tokens
- Context usage: 50% just for log data

After Optimization:
1. Save log to /tmp/app-log.txt
2. Reference in context: "Log saved to /tmp/app-log.txt (100k tokens)"
3. Read specific sections when needed:
   - Read first 50 lines for overview
   - Grep for errors
   - Read relevant sections on-demand

Token Usage:
- Before: 100,000 tokens in context
- After: ~500 tokens (file reference) + ~2,000 tokens (specific reads)
- Savings: 97,500 tokens (97.5% reduction)

Quality: Maintained - can still analyze log on-demand
Access: Full log available when needed
```

**Research Finding**: *"File-based approach achieves 95% token savings"* - proven in 2025 optimization studies

---

## Best Practices

### 1. Quality Over Quantity
**Practice**: Focus on relevant, high-quality context rather than loading everything

**Rationale**: Every piece should be current, accurate, and directly relevant to task

**Application**: Before loading file, ask: "Do I need this right now for current task?"

### 2. Progressive Disclosure Always
**Practice**: Design all skills with SKILL.md + references/ pattern

**Rationale**: 70-80% token reduction vs monolithic design

**Application**: SKILL.md <1,200 lines, details in references/ loaded on-demand

### 3. Monitor Regularly
**Practice**: Check context usage periodically, especially in long sessions

**Rationale**: Auto-compaction triggers at ~80%, but proactive monitoring prevents drift

**Application**: Check `/context` every 30-60 minutes in active development

### 4. File-Based for Large Data
**Practice**: Externalize data >5,000 tokens to files

**Rationale**: 95% token savings while maintaining accessibility

**Application**: Save to /tmp/, reference file path, load on-demand

### 5. Separate Planning from Execution
**Practice**: Plan in one session, execute in clean session with plan artifacts

**Rationale**: Keeps execution context focused, prevents exploratory noise

**Application**: When planning >1 hour, start fresh session for implementation

### 6. Clean Context Before Critical Work
**Practice**: Reduce context load before important/complex operations

**Rationale**: Clean context improves quality and performance

**Application**: Before complex implementation, clear unnecessary context

### 7. Use Appropriate Tools
**Practice**: Choose tools that minimize context usage

**Rationale**: Some tools add more context than others

**Application**:
- Grep instead of Read for searching (doesn't load full file)
- Glob for finding files (doesn't load content)
- Task agents for exploration (separate context)

### 8. Optimize CLAUDE.md
**Practice**: Keep CLAUDE.md concise (<5,000 tokens), split if needed

**Rationale**: CLAUDE.md loaded every session, large files waste context

**Application**:
- Essential standards in CLAUDE.md (project level)
- Temporary preferences in CLAUDE.local.md
- Specific domain knowledge in separate files loaded as needed

---

## Context Budgets for Skills

### Simple Skills (Total: 5,000-10,000 tokens)

**Structure**:
- SKILL.md only or SKILL.md + 1-2 small references
- No scripts or minimal automation
- ~400-800 lines total

**Token Breakdown**:
- SKILL.md: 3,000-4,000 tokens
- References (if any): 1,000-2,000 tokens each
- README: 1,000 tokens

**Example**: format-validator, simple helpers

---

### Medium Skills (Total: 15,000-30,000 tokens)

**Structure**:
- SKILL.md + 3-5 references + scripts
- ~1,500-3,000 lines total

**Token Breakdown**:
- SKILL.md: 3,000-5,000 tokens
- References: 4-6 files × 1,500 tokens = 6,000-9,000 tokens
- Scripts: 2-3 files × 1,000 tokens = 2,000-3,000 tokens
- README: 1,000-1,500 tokens

**Progressive Loading**: Load SKILL.md (3-5k) + specific reference when needed (+1.5k) = 4.5-6.5k typical

**Example**: prompt-builder, skill-researcher

---

### Complex Skills (Total: 40,000-60,000 tokens)

**Structure**:
- SKILL.md + 7-10 references + 4+ scripts
- ~4,000-7,000 lines total

**Token Breakdown**:
- SKILL.md: 4,000-6,000 tokens
- References: 7-10 files × 2,000 tokens = 14,000-20,000 tokens
- Scripts: 4-6 files × 1,500 tokens = 6,000-9,000 tokens
- README: 1,500-2,000 tokens

**Progressive Loading**: Load SKILL.md (4-6k) + 1-2 references as needed (+2-4k) = 6-10k typical

**Example**: review-multi, testing-validator

**Key**: Even complex skills only load 6-10k tokens typically (not full 40-60k)

---

## Common Mistakes

### Mistake 1: Loading Everything Upfront
**Symptom**: Context quickly fills with all skill files

**Cause**: Reading all files instead of progressive loading

**Fix**: Load SKILL.md first, load references/ only when needed for specific operations

**Prevention**: Follow progressive disclosure pattern

### Mistake 2: Not Monitoring Context
**Symptom**: Unexpected context overflow, performance degradation

**Cause**: No visibility into token usage

**Fix**: Check `/context` regularly, monitor usage patterns

**Prevention**: Check context every 30-60 min in active sessions

### Mistake 3: Large Monolithic CLAUDE.md
**Symptom**: Every session starts with 20k-50k tokens used

**Cause**: Putting everything in CLAUDE.md

**Fix**: Split CLAUDE.md - essentials only, separate files for detailed knowledge

**Prevention**: Keep CLAUDE.md <5,000 tokens, use multiple files

### Mistake 4: Keeping Stale Tool Results
**Symptom**: Context bloated with old exploratory results

**Cause**: Not clearing old tool calls

**Fix**: Context editing auto-clears, but can manually manage by starting fresh sessions

**Prevention**: Fresh session for major transitions (planning → execution)

### Mistake 5: Not Using File-Based Strategies
**Symptom**: Large data sets consuming 30-50% of context

**Cause**: Keeping large outputs in conversation

**Fix**: Save to /tmp/ files, reference file path, load on-demand

**Prevention**: Any data >5,000 tokens → externalize to file

### Mistake 6: Ignoring Progressive Disclosure
**Symptom**: Skills with 2,000+ line SKILL.md files

**Cause**: Not using references/ for detailed content

**Fix**: Extract detailed content to references/, keep SKILL.md as overview

**Prevention**: Design with progressive disclosure from start (use planning-architect)

---

## Quick Reference

### Context Window Limits (2025)

| Model | Standard | Beta (Tier 4) | Auto-Compact |
|-------|----------|---------------|--------------|
| Sonnet 4/4.5 | 200k tokens | 500k-1M tokens | ~80% (~160k for 200k) |

### Token Savings Strategies

| Strategy | Token Savings | Application |
|----------|---------------|-------------|
| Progressive Disclosure | 70-80% | SKILL.md + references/ vs monolithic |
| File-Based Externalization | 95% | Large data >5k tokens to /tmp/ files |
| Context Editing | 29-39% | Auto-clears stale content |
| Lazy Loading | 60-70% | Load references on-demand vs all upfront |
| Optimized CLAUDE.md | Variable | Keep <5k tokens vs 20-50k bloat |

### Skill Token Budgets

| Skill Complexity | Total Tokens | Typical Load | Progressive Load |
|------------------|--------------|--------------|------------------|
| Simple | 5k-10k | 3k-4k | SKILL.md only |
| Medium | 15k-30k | 4k-6k | SKILL.md + 1 reference |
| Complex | 40k-60k | 6k-10k | SKILL.md + 2 references |

### Context Usage Guidelines

| Usage % | Status | Action |
|---------|--------|--------|
| <50% | ✅ Healthy | Normal operation |
| 50-70% | ⚠️ Monitor | Check periodically, plan optimization |
| 70-80% | ⚠️ Optimize | Reduce context load soon |
| >80% | ❌ Critical | Immediate optimization needed (auto-compact triggers) |

### Optimization Decision Tree

```
Is context >70%?
├─ Yes → Reduce immediately (Operation 2)
│   ├─ Clear stale tool results
│   ├─ Unload unnecessary files
│   └─ Start fresh session if needed
│
└─ No → Preventive optimization
    ├─ Is data >5k tokens? → File-based (Operation 5)
    ├─ Building skills? → Progressive disclosure (Operation 3)
    └─ Long session? → Consider planning/execution split (Operation 4)
```

### Quick Optimization Actions

**Immediate** (When context >80%):
```bash
1. Check usage: /context command
2. Clear old tool results (context editing helps)
3. Start fresh session with essentials only
4. Load plan docs, not exploration history
```

**Preventive** (During development):
```
1. Design skills with progressive disclosure
2. Use file-based for large data (>5k tokens)
3. Monitor context every 30-60 min
4. Separate planning from execution (for complex work)
```

### Common Commands

```bash
# Monitor context usage
/context

# Read specific lines (not full file)
Read file_path --limit 50

# Search without loading (uses Grep, more efficient)
Grep "pattern" path/

# Find files without loading content
Glob "*.py" path/

# Externalize large data
Bash: command > /tmp/output.txt
# Then reference: "See /tmp/output.txt for results"
```

### Token Estimation

**Quick Estimation**:
- 1 line of code/text ≈ 3-4 tokens (average)
- 1,000 lines ≈ 3,000-4,000 tokens
- Dense prose: 3-3.5 tokens/line
- Code with comments: 2.5-3 tokens/line
- Tables/lists: 2-2.5 tokens/line (more efficient)

### For More Information

- **Context monitoring**: references/context-monitoring-guide.md
- **Reduction strategies**: references/reduction-strategies.md
- **Optimization patterns**: references/optimization-patterns.md
- **Analysis script**: scripts/analyze-context-usage.py

---

**context-engineering** helps you maximize Claude Code effectiveness through strategic context management, ensuring optimal performance, quality, and cost-efficiency throughout development.
