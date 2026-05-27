---
name: deep-reflect
description: Analyzes development sessions to extract patterns, preferences, and learnings. Use after significant work sessions to capture insights, document system understanding, and improve future interactions.
allowed-tools: [Read, Write, Edit, Grep, Glob, AskUserQuestion, TodoWrite]
# model: opus
---

## Reference Files

- [framework.md](framework.md) - The 5-dimension analysis framework
- [output-template.md](output-template.md) - Structured reflection format

---

# Deep Reflect

Comprehensive session analysis to build cumulative knowledge across interactions.

## Objective

Extract reusable insights from the session that make future sessions more effective. Focus on patterns, not just facts.

## When to Use

- After significant debugging or problem-solving sessions
- When you've learned something important about the codebase
- After discovering user preferences through trial and error
- When system relationships became clearer through investigation

## Analysis Framework

Examine the session through 5 dimensions:

### 1. Problems & Solutions

- What symptoms were reported?
- What root causes were discovered?
- What solutions worked (and didn't)?
- What key insights emerged?

### 2. Code Patterns & Architecture

- What design decisions were made?
- What architecture choices emerged?
- What code relationships were discovered?
- What integration points were identified?

### 3. User Preferences & Workflow

- Communication style preferences
- Decision-making patterns
- Quality standards expressed
- Workflow preferences revealed
- Direct quotes that reveal preferences

### 4. System Understanding

- Component interactions discovered
- Critical paths and dependencies
- Failure modes and recovery patterns
- Performance considerations learned

### 5. Knowledge Gaps & Improvements

- Where did misunderstandings occur?
- What information was missing?
- What better approaches were discovered?
- What should be done differently next time?

## Process

1. **Review** - Walk through the session conversation
2. **Extract** - Identify insights in each dimension
3. **Synthesize** - Connect related learnings
4. **Document** - Create structured reflection
5. **Act** - Generate concrete deliverables

## Deliverables

Based on the analysis, generate applicable items:

- **CLAUDE.md updates** - Preferences and patterns to remember
- **Code comments** - System understanding to preserve
- **Documentation** - Workflows or processes to document
- **Future considerations** - Things to address in later sessions

## Guidelines

- Focus on reusable patterns, not session-specific facts
- Capture the "why" behind decisions, not just the "what"
- Preserve user voice when documenting preferences
- Prioritize insights by impact on future effectiveness
- Build cumulative knowledge, not just session notes
