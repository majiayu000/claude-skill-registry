---
name: context-engineering
description: Context engineering and prompt patterns for AI agents
allowed-tools: Read, Grep, Write, Edit, Bash, WebSearch
---

# SKILL.md - Context Engineering & AI Agent Skills

> **核心理念**: 2025年不再是"Prompt Engineering"，而是**"Context Engineering"** —— 设计动态系统，为AI模型提供最相关的上下文信息。

---

## Table of Contents

1. [Core Principles](#core-principles)
2. [Context Engineering Patterns](#context-engineering-patterns)
3. [High-Frequency Scenarios](#high-frequency-scenarios)
4. [Best Practice Templates](#best-practice-templates)
5. [Anti-Patterns](#anti-patterns)
6. [Quality Checklist](#quality-checklist)

---

## Core Principles

### Design Philosophy

| Principle | Description | Example |
|-----------|-------------|---------|
| **简洁优雅** | Minimal code for maximum function | 3 similar lines > premature abstraction |
| **高效纯粹** | Single responsibility per component | Database tables: minimal & maintainable |
| **失败安全** | Edge cases first, not afterthought | Validate before processing |
| **显式记录** | Formulas and results must be traceable | KPI calculations: formula + amount recorded |

### Context Engineering Three Laws

1. **稳定前缀定律**: System prompts remain stable, avoid frequent modifications
2. **追加式定律**: Recorded data is append-only, never modified
3. **缓存标记定律**: Explicit cache boundaries to avoid redundant computation

---

## Context Engineering Patterns

### Pattern 1: Structured Task Decomposition

```markdown
# Task: [Concise Title]

## Context
- Project: [Project Name]
- Current State: [Description]
- Goal: [Clear Objective]

## Constraints
- Must: [Hard requirements]
- Must Not: [Explicit prohibitions]
- Optimize: [Concise, elegant, efficient, pure]

## Acceptance Criteria
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]
```

### Pattern 2: Business Logic Review

```markdown
# Business Logic Review: [System Name]

## Core Rules
1. [Rule 1 - Dynamically adjustable]
2. [Rule 2 - Calculation method]
3. [Rule 3 - Traceability requirements]

## Review Focus
- Correctness: Business logic compliant with specifications
- Completeness: All scenarios covered
- Traceability: Calculation process recorded
- Maintainability: Code is clean and clear

## Optimization Suggestions
- [If any] Clearly implementable improvements
```

### Pattern 3: Data Integration MVP

```markdown
# MVP Data Integration: [Module Name]

## Database Design Principles
- Table Count: As few as possible (simple & maintainable)
- Fields: Explicit naming, avoid abbreviations
- Relations: Foreign keys when necessary, avoid over-normalization

## Integration Steps
1. Build independent MVP modules
2. Identify shared data
3. Minimize table integration
4. Automate calculation logic

## Testing & Validation
- [ ] Data integrity
- [ ] Calculation accuracy
- [ ] Edge case handling
```

---

## High-Frequency Scenarios

### Scenario 1: Code Review

```markdown
Use code-reviewer skill to check code modifications:

1. **Business Logic**: Correct and complete
2. **Security**: No vulnerabilities (OWASP Top 10)
3. **Performance**: Obvious optimization opportunities
4. **Maintainability**: Code is concise and elegant

**Key**: Ignore trivial details, focus on clearly implementable improvements.
Implementation: Concise, elegant, efficient, pure
```

### Scenario 2: Financial System Review

```markdown
# Financial System Audit Focus

## Business Logic Validation
- [ ] Amount calculation formulas correct
- [ ] Debit-credit balance verification
- [ ] Tax/fee rates dynamically configurable
- [ ] Multi-currency support (if needed)

## Data Integrity
- [ ] Transaction logs never lost
- [ ] Balance changes traceable
- [ ] Audit logs complete
- [ ] Abnormal transactions marked

## Database Design
- Minimal table count (simple & maintainable)
- Necessary indexes established
- Foreign key constraints properly set
```

### Scenario 3: KPI System Review

```markdown
# KPI System Three Key Points

## 1. Dynamic Bonus Ratio
- Monthly bonus ratios configurable
- Historical configurations preserved
- Effective time clearly defined

## 2. Excess Calculation Method
- Salesperson excess = Monthly high option fee
- Calculation formula explicitly recorded
- Results verifiable

## 3. Traceable Design
- Recorded data never modified
- Calculation formulas explicitly defined
- Result amounts traceable
```

### Scenario 4: Frontend Testing

```markdown
# Minimal Viable Testing Plan

## Pre-Test Preparation
1. Confirm backend APIs working
2. Prepare test dataset
3. Clear browser cache

## Test Steps
1. **Functional Test**: [Specific steps]
   - Expected: [Clear expectation]
   - Actual: [Record actual]
   - Pass: ✓ / ✗

2. **Boundary Test**: [Extreme values]
   - Expected: [Clear expectation]

## Issue Debugging
If not as expected:
1. Check console errors
2. Check network requests
3. Check backend logs
4. Gradually narrow scope
```

### Scenario 5: Document Conversion

```markdown
# PDF → Markdown Conversion Requirements

## Information Completeness
- [ ] Text content (including tables)
- [ ] Images and charts
- [ ] Format hierarchy (headings, lists)
- [ ] Page/chapter references

## Readability Optimization
- Standard Markdown syntax
- Tables converted to Markdown
- Code blocks with syntax highlighting
- Add table of contents with anchors

## Output Format
- Standard CommonMark syntax
- UTF-8 encoding
- Filename: [original_name].md
```

---

## Best Practice Templates

### Template A: Deep Analysis Mode

When encountering unfamiliar code or problems:

```markdown
# Deep Analysis: [Topic]

## Step 1: Understand Current State
- [ ] Read relevant code files
- [ ] Search docs and best practices
- [ ] Review similar implementations

## Step 2: Locate Problem
- [ ] Narrow problem scope
- [ ] Confirm reproduction steps
- [ ] Collect error information

## Step 3: Design Solution
- [ ] List possible approaches
- [ ] Evaluate pros/cons
- [ ] Select best approach

## Step 4: Verify Results
- [ ] Unit tests
- [ ] Integration tests
- [ ] Regression tests
```

### Template B: User Friendliness Review

```markdown
# UI/UX Consistency Review

## Consistency Check
- [ ] Terminology unified (same concept = same wording)
- [ ] Interaction patterns consistent (save/cancel/delete positions)
- [ ] Visual styles consistent (colors/fonts/spacing)
- [ ] Feedback mechanisms consistent (success/error messages)

## User Friendliness
- [ ] Minimize operation steps
- [ ] Error messages clear and specific
- [ ] Loading states have feedback
- [ ] Key information highlighted

## Accessibility
- [ ] Keyboard navigation support
- [ ] Focus management reasonable
- [ ] Contrast meets standards
```

### Template C: Progress Sync Template

```markdown
# Progress Update: [Feature/Module]

## Completed
- ✅ [Specific completed tasks]

## In Progress
- 🔄 [Current task] (Progress: X%)

## Issues
- ⚠️ [Issue description]
- Impact: [Impact scope]
- Solution: [Planned solution]

## Next Steps
- 📋 [Planned tasks]
```

---

## Anti-Patterns

### Patterns to Avoid

| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Over-abstraction | Creating utilities for 3 uses | Copy-paste, abstract when >3 |
| Premature optimization | Planning for hypothetical needs | YAGNI principle, add when needed |
| Silent failures | Errors swallowed silently | Explicit handling or propagate up |
| Magic numbers | Hard-coded constants | Extract to named constants |
| Nesting hell | 5-layer if nesting | Early returns, guard clauses |

### Common Traps

1. **Over-commenting**: Code should be self-documenting; comments explain "why" not "what"
2. **Ignoring edges**: Only handling happy path, exceptions unhandled
3. **Database over-design**: Too many tables, complex relationships hard to maintain
4. **Insufficient testing**: Only normal flow tested, edges uncovered
5. **Poor communication**: Not asking when stuck, blindly trying

---

## Quality Checklist

### Code Quality

- [ ] Business logic correct and complete
- [ ] No security vulnerabilities (injection, XSS, etc.)
- [ ] Error handling comprehensive
- [ ] Code concise and readable
- [ ] Naming clear and accurate
- [ ] No code duplication

### Data Integrity

- [ ] Calculation formulas explicitly recorded
- [ ] Results traceable and verifiable
- [ ] Historical data never modified
- [ ] Abnormal data marked
- [ ] Transaction consistency guaranteed

### User Experience

- [ ] Workflow concise
- [ ] Error messages clear
- [ ] Loading state feedback
- [ ] Interface style consistent
- [ ] Key information prominent

---

## Sources

### Context Engineering
- [Effective Context Engineering for AI Agents - Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Context Engineering for AI Agents: Lessons from Building Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- [Context Engineering in LLM-Based Agents](https://jtanruan.medium.com/context-engineering-in-llm-based-agents-d670d6b439bc)

### Prompt Engineering
- [10 Best Practices for Building Reliable AI Agents in 2025](https://www.uipath.com/blog/ai/agent-builder-best-practices)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [OpenAI Prompt Engineering Documentation](https://platform.openai.com/docs/guides/prompt-engineering)

### Code Review Automation
- [AI Code Review Implementation Best Practices - Graphite](https://graphite.com/guides/ai-code-review-implementation-best-practices)
- [AI Code Review with Claude Skills Guide](https://medium.com/@r0r1/ai-code-review-with-claude-skills-from-diy-to-team-ready-636966cb8e36)

### MVP & Data Integration
- [7 Key Steps for MVP Development in Banking and Finance](https://medium.com/@KMSSolutions/7-key-steps-for-effective-mvp-development-in-banking-and-finance-ebc12434628a)
- [System Integration Best Practices](https://cadabra.studio/blog/system-integration-guide)

---

## Appendix: Quick Commands

### Claude Code Skills

```bash
# Code review
/code-reviewer

# Debug assistant
/debugging-assistant

# Git analysis
/git-analyzer

# Product management
/product-manager

# UI/UX principles
/ui-ux-principles

# Context engineering (this skill)
/context-engineering

# Commit code
/commit [message]

# Add rule
/add-rule

# Analyze document
/analyze-doc
```

---

**Version**: 1.0.0
**Updated**: 2025-01-01
**Maintainer**: Veld Team
