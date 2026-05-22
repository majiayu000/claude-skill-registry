---
name: focus-problem
description: Problem analysis using Explore agents
user-invocable: true
---

# Focus Problem Analysis

Analyze: $ARGUMENTS

## Explore Codebase First

Before diving in, use the Explore agent to understand the context:

```markdown
Task(subagent_type="Explore", model="haiku", prompt="""
Explore the codebase for: $ARGUMENTS (thoroughness: medium)
Focus on:
1. Relevant files and modules
2. Existing similar features
3. Test patterns
4. Architecture patterns
""")
```

## Analysis Framework

### 1. Core Problem Identification
- **What is the real problem?**
- **Why does it need to be solved?**
- **What happens if we don't solve it?**

### 2. Minimal Solution Scope
- **What's the minimum change needed?**
- **Which features are essential?**
- **What can be deferred or omitted?**

### 3. Solution Evaluation
- **Option A (Simplest):**
- **Option B (Balanced):**
- **Option C (Complete):**
- **Recommendation:** Choose the simplest viable option

### 4. Implementation Plan
- **Step 1:** Write tests
- **Step 2:** Minimal implementation
- **Step 3:** Update documentation
- **Step 4:** Commit changes

## Output Template

```markdown
## Problem Definition

### Summary
[One sentence description]

### User Need
[Who needs this? What do they want to achieve?]

### Success Criteria
[How do we know it's done?]

### Scope
- In scope: [List]
- Out of scope: [List]

### Affected Files
- [file1.ts] - [why]
- [file2.ts] - [why]

### Risk Assessment
- [Potential risks and mitigations]
```

---

Follow this process strictly. Don't skip steps.
