---
name: backlog-groomer
description: "Manage the beads backlog for this project. Use when the user wants to review or triage open issues, reprioritize the backlog, identify obsolete issues to close, investigate a topic to inform future work, create new issues from research findings, or enrich an existing issue with external context. Trigger phrases: 'groom', 'triage', 'backlog review', 'reprioritize', 'stale issues', 'what should we close', 'too many issues', 'backlog health', 'investigate for backlog', 'research and create issues', 'add context to issue', 'enrich issue', 'plan the work for', 'break down into issues', or any request to audit, prune, or research work tracked in beads."
argument-hint: "[topic]"
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - mcp__basic-memory__search_notes
  - mcp__basic-memory__read_note
  - mcp__tavily__tavily_search
  - mcp__tavily__tavily_extract
  - mcp__deepwiki__ask_question
  - mcp__raindrop__find_bookmarks
  - mcp__raindrop__fetch_bookmark_content
---

# Backlog Groomer

Triage, prioritize, and research work tracked in the beads issue tracker. This
skill operates on the `bd` CLI — all mutations (create, close, update) require
explicit user approval before execution.

Determine which workflow the user needs based on their request. If ambiguous,
default to workflow 1 (review and triage) for grooming requests, or workflow 4
(investigate) for research requests.

## Grooming Workflows

### 1. Review and triage

Scan the open backlog for issues that need attention: stale items, potential
duplicates, blocked chains, and missing context.

**Steps:**

1. Run `bd list --status open` and `bd list --status in_progress` to get the
   full picture. Run `bd stats` for summary counts.
2. Run `bd stale --days 60` to flag aging issues. Separately flag `in_progress`
   issues stale >30 days as "stalled."
3. Run `bd duplicates` to detect content-hash matches (if available; if not,
   use `bd search` with keywords from suspicious titles for near-matches).
4. Run `bd blocked` to identify issues stuck on unresolved dependencies.
5. Cross-reference with `UPSTREAM-*.md` files if they exist (use `Glob` to
   find them). Note any UPSTREAM friction that should have a corresponding
   beads issue.
6. If Basic Memory MCP tools are available, call
   `mcp__basic-memory__search_notes` for key dependencies from `package.json`
   to surface known friction not yet in the backlog. Skip silently if
   unavailable.
7. Present a structured triage table:

   ```
   | ID | Title | Age | Priority | Flags |
   |----|-------|-----|----------|-------|
   | vp-beads-xxx | ... | 45d | P3 | stale, missing description |
   ```

8. Suggest per-issue actions: close, reprioritize, merge with duplicate, refine
   scope, or leave as-is. **No mutations without explicit per-item approval.**

### 2. Reprioritize

Propose a priority reordering based on current sprint goals and blocking
relationships.

**Steps:**

1. Ask the user for current sprint goals if not obvious from conversation
   context. Infer from recent commits and `bd list --status in_progress` if
   the user does not state goals explicitly.
2. Run `bd list --status open` to get all open issues with current priorities.
3. Run `bd blocked` to identify blocked chains. If `bd dep tree` is available,
   use it to visualize blocking power — issues that unblock the most downstream
   work should rank higher.
4. Propose a reordered priority list with reasoning per change. Present as a
   diff: current priority → proposed priority, with a one-line rationale.
5. User approves, edits, or rejects each proposed change.
6. Run `bd update <id> --priority N` per approved change.

### 3. Suggest closures

Identify issues that are likely obsolete and propose closing them.

**Steps:**

1. Run `bd list --status open`, focusing on P3/P4 items and issues older than
   60 days.
2. Cross-reference `git log --oneline -50` with issue titles — use `Grep` to
   match issue keywords against commit messages. Find issues already addressed
   by commits but never formally closed.
3. Check `bd list --status closed` for issues that supersede open ones.
4. Run `bd stale --days 90` for deeply stale items.
5. Classify each closure candidate:
   - **Addressed by commit**: cite the commit
   - **Superseded**: cite the replacement issue
   - **Out of scope**: note the scope shift (user must confirm)
   - **Stale beyond recovery**: >120 days, no activity, low priority
6. Present candidates with rationale per item.
7. `bd close <id> --reason "..."` per approved closure.

See `references/backlog-health-heuristics.md` for closure criteria and
staleness thresholds.

## Research Workflows

### 4. Investigate a topic

Research a topic to inform future work. Takes a topic from the user's request
or the `argument-hint`.

**Steps:**

1. Parse the user's topic. Classify: technology/library question, project
   refactor, or feature request. This guides the research tool mix.
2. **Basic Memory search first** (non-negotiable). Call
   `mcp__basic-memory__search_notes` for the topic and related terms. For
   relevant matches, call `mcp__basic-memory__read_note` to get full content —
   surface existing engineering notes, package notes, or upstream friction
   entries. If Basic Memory is unavailable, note the gap and proceed.
3. Check existing beads issues: `bd search <keywords>` to find overlap with
   already-tracked work.
4. Scan the codebase: use Glob and Grep for existing code related to the topic.
   Understand the current state — what exists, what patterns are established.
5. Check Raindrop bookmarks: call `mcp__raindrop__find_bookmarks` with topic
   keywords to surface previously bookmarked articles and resources. If
   relevant bookmarks are found, use `mcp__raindrop__fetch_bookmark_content`
   to extract key insights. Skip silently if unavailable.
6. External research (if needed based on classification):
   - `mcp__deepwiki__ask_question` for package/framework architecture questions
   - `mcp__tavily__tavily_search` for broader implementation patterns
   - `mcp__tavily__tavily_extract` for deep-diving specific URLs found in search
   If external tools are unavailable, proceed with what is available.
7. Synthesize into a concise brief: what exists now, what needs to change, key
   technical decisions, known pitfalls. Cap at 4-6 bullet points.
8. Flag items that should become issues (hand off to workflow 5) or enrich an
   existing issue (hand off to workflow 6).

### 5. Create issues from findings

Turn research findings into structured beads issues. Takes output from
workflow 4 or user-provided findings.

**Steps:**

1. Review the findings and identify discrete, actionable items. Each issue
   should be completable in roughly one session of focused work.
2. Dedup check: run `bd search <keywords>` for each proposed title against
   existing issues. Surface near-matches for the user to review.
3. Propose structured issues. For each:
   - **Title**: `[Area] Action verb + subject` convention
   - **Type**: bug / task / feature / chore (see reference file for logic)
   - **Priority**: 0-4 with explicit reasoning
   - **Description**: problem + why it matters + suggested first step
4. If >3 related issues emerge from one topic: propose a tracking issue
   (`bd create -t epic`) as a group container, with child issues linked.
5. If >8 issues from one topic: suggest splitting into multiple research
   sessions rather than creating a sprawling epic.
6. User approves, edits, or rejects each proposed issue before any `bd create`
   command runs. Present the full list first, then confirm.
7. Run `bd create "title" -t <type> -p <priority> --description "..."` per
   approved issue.
8. Add dependencies where natural ordering exists: `bd dep add <child> <parent>`.
9. Report: created issue IDs, dependency graph, and suggested first issue to
   start (highest priority with no unsatisfied dependencies).

See `references/backlog-health-heuristics.md` for title conventions, description
templates, and creation limits.

### 6. Enrich an existing issue

Add research context to an existing issue that needs more information before
work can begin.

**Steps:**

1. User identifies the issue by ID or title. Run `bd show <id>` to read the
   current state (title, description, status, priority, dependencies).
2. Research the topic using the same pipeline as workflow 4: Basic Memory
   search → Raindrop bookmarks → codebase scan → external research (DeepWiki,
   Tavily) as needed.
3. Draft an enriched description. Preserve the original description and append
   a `## Research Context` section with findings, relevant links, and suggested
   approach.
4. Show the draft to the user for approval before applying.
5. Run `bd update <id> --description "..."` with the enriched description after
   approval.

## Guidelines

- **User approval is non-negotiable.** Every write operation (`bd create`,
  `bd close`, `bd update`) must be explicitly approved per item. Present
  candidates first, confirm, then execute. Never auto-mutate.
- **Beads is optional.** Guard all `bd` commands with availability checks.
  If `.beads/` does not exist or `bd` is not found, report that backlog
  grooming requires beads and stop.
- **Basic Memory is opportunistic.** Check for BM tool availability and skip
  silently if unavailable. BM enriches grooming with cross-project context but
  is not required for the core workflows.
- **Infer from context.** When the user asks to groom or research, read the
  conversation history for recent friction, decisions, and goals rather than
  starting a Q&A. The user should not have to re-explain context.
- **Keep output scannable.** Use tables for triage results, diffs for priority
  changes, numbered lists for issue proposals. Cap output at what fits in a
  conversation turn.
- **Respect the priority vocabulary.** Use the 0-4 numeric scale consistently:
  0=critical, 1=high, 2=medium, 3=low, 4=backlog.
