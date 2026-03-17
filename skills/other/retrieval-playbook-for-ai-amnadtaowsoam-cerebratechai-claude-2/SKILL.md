---
name: Retrieval Playbook for AI
description: กลยุทธ์การ retrieve context ให้ AI อย่างมีประสิทธิภาพ - เลือกอะไร ไม่เลือกอะไร และจัดลำดับอย่างไร
---

# Retrieval Playbook for AI

## Overview

Playbook สำหรับตัดสินใจว่าจะ retrieve context อะไรให้ AI - เลือกแค่ที่จำเป็น ตัดที่ไม่เกี่ยว จัดลำดับให้เหมาะสม

## Why This Matters

- **Relevance**: เฉพาะที่เกี่ยวข้อง
- **Token efficiency**: ไม่เสีย token กับข้อมูลไม่เกี่ยว
- **Better results**: AI focus ได้ดีขึ้น
- **Faster**: น้อย context = เร็วขึ้น

---

## Decision Tree

```
Task received
    ↓
Is it code-related?
    ├─ Yes → Retrieve code files
    └─ No → Skip code
         ↓
Need current state?
    ├─ Yes → Include recent changes
    └─ No → Skip history
         ↓
Need examples?
    ├─ Yes → Include 1-2 examples
    └─ No → Skip examples
         ↓
Assemble context
```

---

## Retrieval Rules

### Rule 1: Only Direct Dependencies
```
❌ Include entire codebase
✅ Include only files directly related

Example:
Task: Fix bug in auth.ts
Include:
- auth.ts (the file)
- types.ts (if auth.ts imports it)
- config.ts (if auth.ts uses it)

Don't include:
- unrelated files
- test files (unless debugging tests)
- documentation
```

### Rule 2: Snippets Over Full Files
```
❌ Include entire 500-line file
✅ Include 20-line relevant function

Example:
Task: Fix validateToken function
Include:
- validateToken function (lines 45-60)
- Related types (5 lines)
- Helper functions used (10 lines)

Total: ~35 lines vs 500 lines
Savings: 93%
```

### Rule 3: Recent Over Old
```
✅ Last 3 commits
❌ Full git history

✅ Current implementation
❌ Deprecated code
```

### Rule 4: Examples Only When Needed
```
Include examples when:
✓ New pattern/concept
✓ Complex logic
✓ User explicitly asks

Skip examples when:
✗ Simple CRUD
✗ Standard patterns
✗ Self-explanatory
```

---

## Context Prioritization

### Priority 1: Critical (Always Include)
```
- File with the bug/feature
- Error messages
- Relevant types/interfaces
- Direct dependencies
```

### Priority 2: Important (Include if Space)
```
- Related functions
- Configuration
- Recent changes
- Test cases
```

### Priority 3: Nice-to-Have (Usually Skip)
```
- Full documentation
- Examples
- Comments
- Historical context
```

---

## Retrieval Strategies by Task Type

### Bug Fix
```
Retrieve:
✓ File with bug (snippet)
✓ Error message
✓ Stack trace
✓ Related types

Skip:
✗ Entire file
✗ Unrelated files
✗ Documentation
✗ Tests (unless test is failing)
```

### Feature Development
```
Retrieve:
✓ Similar existing features (1 example)
✓ Relevant types
✓ API contracts
✓ Configuration

Skip:
✗ Multiple examples
✗ Full documentation
✗ Unrelated features
```

### Code Review
```
Retrieve:
✓ Changed files (diff)
✓ Related files (if imports changed)
✓ Style guide (summary)

Skip:
✗ Unchanged files
✗ Full style guide
✗ Historical context
```

### Refactoring
```
Retrieve:
✓ File to refactor
✓ Files that import it
✓ Tests for it

Skip:
✗ Unrelated files
✗ Documentation
✗ Examples
```

---

## Smart Filtering

### Filter by Recency
```typescript
// Get files changed in last 7 days
const recentFiles = gitLog()
  .filter(commit => commit.date > sevenDaysAgo)
  .flatMap(commit => commit.files);
```

### Filter by Relevance
```typescript
// Score files by relevance
const relevantFiles = allFiles
  .map(file => ({
    file,
    score: calculateRelevance(file, task)
  }))
  .filter(f => f.score > 0.7)
  .sort((a, b) => b.score - a.score)
  .slice(0, 5);  // Top 5 only
```

### Filter by Size
```typescript
// Prefer smaller, focused files
const files = candidates
  .filter(f => f.lines < 200)  // Skip large files
  .sort((a, b) => a.lines - b.lines);
```

---

## Context Assembly

### Order Matters
```
1. Summary (what we're doing)
2. Error/issue (if applicable)
3. Relevant code (snippets)
4. Types/interfaces
5. Configuration (if needed)

❌ Don't:
- Start with full files
- Mix unrelated contexts
- Bury important info
```

### Example Assembly
```markdown
# Task: Fix login bug

## Issue
Login fails with "Invalid token" error

## Code
```typescript
// auth.ts:45-60
function validateToken(token: string) {
  // Bug: missing null check
  return jwt.verify(token, SECRET);
}
```

## Types
```typescript
interface Token {
  userId: string;
  exp: number;
}
```

## Goal
Add null check before jwt.verify
```

---

## Metrics to Track

### Retrieval Efficiency
```typescript
interface RetrievalMetrics {
  filesRetrieved: number;
  tokensUsed: number;
  relevanceScore: number;  // 0-1
  taskSuccess: boolean;
}

// Good retrieval:
{
  filesRetrieved: 3,
  tokensUsed: 500,
  relevanceScore: 0.9,
  taskSuccess: true
}

// Bad retrieval:
{
  filesRetrieved: 20,
  tokensUsed: 5000,
  relevanceScore: 0.3,
  taskSuccess: false
}
```

---

## Anti-Patterns

### ❌ Kitchen Sink Approach
```
"Include everything just in case"
Result: 10,000 tokens, AI confused
```

### ❌ No Filtering
```
"Retrieve all files that mention 'user'"
Result: 50 files, mostly irrelevant
```

### ❌ Full File Dumps
```
"Here's the entire codebase"
Result: Context limit exceeded
```

### ❌ No Prioritization
```
"All files are equally important"
Result: Critical info buried
```

---

## Quick Checklist

```
Before retrieving, ask:
☐ Is this directly related to the task?
☐ Can I use a snippet instead of full file?
☐ Is this the most recent version?
☐ Will AI actually use this?
☐ Am I under my token budget?

If any answer is "no", reconsider including it.
```

---

## Summary

**Retrieval Playbook:** เลือก context อย่างชาญฉลาด

**Rules:**
1. Only direct dependencies
2. Snippets over full files
3. Recent over old
4. Examples only when needed

**Priorities:**
- P1: Critical (always)
- P2: Important (if space)
- P3: Nice-to-have (skip)

**By Task:**
- Bug fix: Error + snippet
- Feature: Example + types
- Review: Diff only
- Refactor: File + dependents

**Target:**
- 3-5 files max
- 500-1000 tokens
- 90%+ relevance
