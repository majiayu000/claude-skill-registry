---
name: deepen-plan
description: "Enhance an existing plan with parallel research, per-section analysis, and updated beads tasks."
allowed-tools: Read, Bash, Glob, Grep, Write, Edit, AskUserQuestion, Task, WebSearch, mcp__plugin_context7_context7__resolve-library-id, mcp__plugin_context7_context7__query-docs
---

# Deepen Plan: $ARGUMENTS

You are enhancing an existing plan with parallel research agents, skill applications, learnings from prior work, and detailed per-section analysis. The result is a deeply grounded, production-ready plan with concrete implementation details.

**Note: The current year is 2026.** Use this when searching for recent documentation and best practices.

**NEVER CODE! Just research and enhance the plan.**

## Phase 1: Find Plan

### If argument provided:
Look for a plan matching `$ARGUMENTS`:
```bash
ls docs/plans/*${ARGUMENTS}* 2>/dev/null
```

### If no argument:
Find the most recent plan:
```bash
ls -lt docs/plans/*.md 2>/dev/null | head -5
```

If no plans found:
"No plan files found in `docs/plans/`. Run `/plan` first to create one."
Then STOP.

Read the plan file.

## Phase 2: Parse and Analyze Plan Structure

Read the plan file and extract:
- [ ] Overview/Problem Statement
- [ ] Proposed Solution sections
- [ ] Technical Approach/Architecture
- [ ] Implementation phases/steps
- [ ] Code examples and file references
- [ ] Acceptance criteria
- [ ] Any UI/UX components mentioned
- [ ] Technologies/frameworks mentioned (Rails, React, Python, TypeScript, etc.)
- [ ] Domain areas (data models, APIs, UI, security, performance, etc.)

**Create a section manifest:**
```
Section 1: [Title] - [Brief description of what to research]
Section 2: [Title] - [Brief description of what to research]
...
```

## Phase 3: Discover and Apply Available Skills

Dynamically discover all available skills and match them to plan sections. Don't assume what skills exist — discover them at runtime.

**Step 1: Discover ALL available skills**

```bash
# 1. Project-local skills (highest priority)
ls .claude/skills/*/SKILL.md 2>/dev/null

# 2. User's global skills
ls ~/.claude/skills/*/SKILL.md 2>/dev/null
```

**Step 2: For each discovered skill, read its SKILL.md to understand what it does**

```bash
cat [skill-path]/SKILL.md
```

**Step 3: Match skills to plan content**

For each skill discovered:
- Read its SKILL.md description
- Check if any plan sections match the skill's domain
- If there's a match, spawn a sub-agent to apply that skill's knowledge

**Step 4: Spawn a sub-agent for EVERY matched skill**

For each matched skill:
```
Task general-purpose: "You have the [skill-name] skill available at [skill-path].

YOUR JOB: Use this skill on the plan.

1. Read the skill: cat [skill-path]/SKILL.md
2. Follow the skill's instructions exactly
3. Apply the skill to this content:

[relevant plan section or full plan]

4. Return the skill's full output

The skill tells you what to do - follow it. Execute the skill completely."
```

**Spawn ALL skill sub-agents in PARALLEL.** No limit on skill sub-agents — spawn one for every skill that could possibly be relevant.

## Phase 4: Discover and Apply Learnings/Solutions

Check for documented learnings from `/compound`. These are solved problems stored as markdown files.

**Step 1: Find ALL learning markdown files**

```bash
# Project-level learnings
find docs/solutions -name "*.md" -type f 2>/dev/null

# Global learnings
find ~/.claude/docs/solutions -name "*.md" -type f 2>/dev/null
```

**Step 2: Read frontmatter of each learning to filter**

Each learning file has YAML frontmatter with metadata:

```yaml
---
title: "N+1 Query Fix for Briefs"
category: performance-issues
tags: [activerecord, n-plus-one, includes, eager-loading]
module: Briefs
symptom: "Slow page load, multiple queries in logs"
root_cause: "Missing includes on association"
---
```

```bash
# Read first 20 lines of each learning (frontmatter + summary)
head -20 docs/solutions/**/*.md
```

**Step 3: Filter — only spawn sub-agents for LIKELY relevant learnings**

Compare each learning's frontmatter against the plan:
- `tags:` — Do any tags match technologies/patterns in the plan?
- `category:` — Is this category relevant?
- `module:` — Does the plan touch this module?
- `symptom:` / `root_cause:` — Could this problem occur with the plan?

**SKIP** learnings that are clearly not applicable. **SPAWN** sub-agents for learnings that MIGHT apply.

**Step 4: Spawn sub-agents for filtered learnings**

For each learning that passes the filter:

```
Task general-purpose: "
LEARNING FILE: [full path to .md file]

1. Read this learning file completely
2. This learning documents a previously solved problem

Check if this learning applies to this plan:

---
[full plan content]
---

If relevant:
- Explain specifically how it applies
- Quote the key insight or solution
- Suggest where/how to incorporate it

If NOT relevant after deeper analysis:
- Say 'Not applicable: [reason]'
"
```

**Spawn sub-agents in PARALLEL for all filtered learnings.** These learnings are institutional knowledge — applying them prevents repeating past mistakes.

## Phase 5: Per-Section Research Agents

For each major section in the plan, spawn dedicated sub-agents to research improvements.

**Explore agents for open-ended research:**

```
Task Explore: "Research best practices, patterns, and real-world examples for: [section topic].
Find:
- Industry standards and conventions
- Performance considerations
- Common pitfalls and how to avoid them
- Documentation and tutorials
Return concrete, actionable recommendations."
```

**Context7 MCP for framework documentation:**

For any technologies/frameworks mentioned in the plan:
```
mcp__plugin_context7_context7__resolve-library-id: Find library ID for [framework]
mcp__plugin_context7_context7__query-docs: Query documentation for specific patterns
```

**WebSearch for current best practices:**

Search for recent (2024-2026) articles, blog posts, and documentation on topics in the plan.

## Phase 6: Discover and Run Review Agents

Dynamically discover every available review/research agent and run them ALL against the plan.

**Step 1: Discover ALL available agents**

```bash
# Project-local agents
find .claude/agents -name "*.md" 2>/dev/null

# User's global agents
find ~/.claude/agents -name "*.md" 2>/dev/null
```

**Step 2: For each discovered agent, read its description**

Read the first few lines of each agent file to understand what it reviews/analyzes.

**Step 3: Launch ALL agents in parallel**

For EVERY agent discovered, launch a Task in parallel:

```
Task [agent-name]: "Review this plan using your expertise. Apply all your checks and patterns. Plan content: [full plan content]"
```

**Rules:**
- Do NOT filter agents by "relevance" — run them ALL
- Launch ALL agents in a SINGLE message with multiple Task tool calls
- 20, 30, 40 parallel agents is fine — use everything available
- Each agent may catch something others miss
- The goal is MAXIMUM coverage, not efficiency

**Also run research agents** (`best-practices-researcher`, `framework-docs-researcher`, `git-history-analyzer`, `repo-research-analyst`, `learnings-researcher`) for relevant plan sections.

## Phase 7: Wait and Synthesize

Wait for ALL parallel agents to complete — skills, learnings, research agents, review agents, everything. Then synthesize all findings.

**Collect outputs from ALL sources:**

1. **Skill-based sub-agents** — Each skill's full output (code examples, patterns, recommendations)
2. **Learnings/Solutions sub-agents** — Relevant documented learnings from `/compound`
3. **Research agents** — Best practices, documentation, real-world examples
4. **Review agents** — All feedback from every reviewer (architecture, security, performance, simplicity, etc.)
5. **Context7 queries** — Framework documentation and patterns
6. **Web searches** — Current best practices and articles

**For each agent's findings, extract:**
- [ ] Concrete recommendations (actionable items)
- [ ] Code patterns and examples (copy-paste ready)
- [ ] Anti-patterns to avoid (warnings)
- [ ] Performance considerations (metrics, benchmarks)
- [ ] Security considerations (vulnerabilities, mitigations)
- [ ] Edge cases discovered (handling strategies)
- [ ] Documentation links (references)
- [ ] Skill-specific patterns (from matched skills)
- [ ] Relevant learnings (past solutions that apply)

**Deduplicate and prioritize:**
- Merge similar recommendations from multiple agents
- Prioritize by impact (high-value improvements first)
- Flag conflicting advice for human review
- Group by plan section

## Phase 8: Enhance Plan Sections

Merge research findings back into the plan, adding depth without changing the original structure.

**Enhancement format for each section:**

```markdown
## [Original Section Title]

[Original content preserved]

### Research Insights

**Best Practices:**
- [Concrete recommendation 1]
- [Concrete recommendation 2]

**Performance Considerations:**
- [Optimization opportunity]
- [Benchmark or metric to target]

**Implementation Details:**
```[language]
// Concrete code example from research
```

**Edge Cases:**
- [Edge case 1 and how to handle]
- [Edge case 2 and how to handle]

**References:**
- [Documentation URL 1]
- [Documentation URL 2]
```

## Phase 9: Add Enhancement Summary

At the top of the plan, add:

```markdown
## Enhancement Summary

**Deepened on:** [Date]
**Sections enhanced:** [Count]
**Research agents used:** [List]

### Key Improvements
1. [Major improvement 1]
2. [Major improvement 2]
3. [Major improvement 3]

### New Considerations Discovered
- [Important finding 1]
- [Important finding 2]
```

## Phase 10: Update Plan File

**Write the enhanced plan:**
- Preserve original filename
- Add `-deepened` suffix if user prefers a new file
- Update any timestamps or metadata

## Phase 11: Update Beads Tasks

For each task that gained new detail:

```bash
bd update <task-id> --description "<enhanced description with implementation notes and refined acceptance criteria>"
```

For newly discovered tasks:
```bash
bd create "<title>" --type task --priority <P1/P2/P3> --description "<description>"
bd dep add <new-id> <parent-id>
```

For tasks that are now obsolete:
```bash
bd close <task-id> --reason="Obsoleted during plan deepening: <reason>"
```

```bash
bd sync
```

## Quality Checks

Before finalizing:
- [ ] All original content preserved
- [ ] Research insights clearly marked and attributed
- [ ] Code examples are syntactically correct
- [ ] Links are valid and relevant
- [ ] No contradictions between sections
- [ ] Enhancement summary accurately reflects changes

## Post-Enhancement Options

After writing the enhanced plan, use the **AskUserQuestion tool** to present these options:

**Question:** "Plan deepened at `[plan_path]`. What would you like to do next?"

**Options:**
1. **View diff** — Show what was added/changed (`git diff [plan_path]`)
2. **Run `/multi-review`** — Get feedback from reviewers on enhanced plan
3. **Run `/dispatch`** — Spawn parallel workers to implement
4. **Run `/start-task <id>`** — Begin implementing a specific task
5. **Deepen further** — Run another round of research on specific sections

## Example Enhancement

**Before (from `/plan`):**
```markdown
## Technical Approach

Use React Query for data fetching with optimistic updates.
```

**After (from `/deepen-plan`):**
```markdown
## Technical Approach

Use React Query for data fetching with optimistic updates.

### Research Insights

**Best Practices:**
- Configure `staleTime` and `cacheTime` based on data freshness requirements
- Use `queryKey` factories for consistent cache invalidation
- Implement error boundaries around query-dependent components

**Performance Considerations:**
- Enable `refetchOnWindowFocus: false` for stable data to reduce unnecessary requests
- Use `select` option to transform and memoize data at query level
- Consider `placeholderData` for instant perceived loading

**Implementation Details:**
```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,
      retry: 2,
      refetchOnWindowFocus: false,
    },
  },
});
```

**Edge Cases:**
- Handle race conditions with `cancelQueries` on component unmount
- Implement retry logic for transient network failures
- Consider offline support with `persistQueryClient`

**References:**
- https://tanstack.com/query/latest/docs/react/guides/optimistic-updates
- https://tkdodo.eu/blog/practical-react-query
```

**NEVER CODE! Just research and enhance the plan.**
