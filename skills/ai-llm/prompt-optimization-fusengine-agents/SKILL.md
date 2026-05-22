---
name: prompt-optimization
description: Analyze and improve existing prompts for better performance
allowed-tools: Read, Write, Edit
---

# Prompt Optimization

Skill for analyzing and improving existing prompts.

## Optimization Workflow

```
1. ANALYZE current prompt
   ↓
2. IDENTIFY issues
   ↓
3. APPLY corrections
   ↓
4. VALIDATE improvement
   ↓
5. DOCUMENT changes
```

## Analysis Checklist

### Clarity
- [ ] Unambiguous instructions?
- [ ] Clearly defined objective?
- [ ] Precise vocabulary?

### Structure
- [ ] Well-delimited sections?
- [ ] Logical order?
- [ ] Clear hierarchy?

### Completeness
- [ ] Output format defined?
- [ ] Error cases handled?
- [ ] Examples if needed?

### Guardrails
- [ ] Explicit limits?
- [ ] Forbidden behaviors listed?
- [ ] Appropriate security?

## Common Problems and Solutions

### 1. Vague Instructions

**Before:**
```
Write a good summary.
```

**After:**
```
Write a 100-150 word summary that:
1. Captures the main idea in the first sentence
2. Includes 2-3 supporting key points
3. Uses accessible language (high school level)
4. Avoids technical jargon
```

### 2. Lack of Context

**Before:**
```
Analyze this code.
```

**After:**
```
Analyze this Python code focusing on:
- Performance (algorithmic complexity)
- Readability (PEP 8 conventions)
- Security (OWASP vulnerabilities)

Context: Code for production REST API, 10k requests/day.
```

### 3. Undefined Format

**Before:**
```
Give me recommendations.
```

**After:**
```
Provide 3-5 recommendations in this format:

## Recommendation [N]: [Short title]
**Impact:** [High/Medium/Low]
**Effort:** [High/Medium/Low]
**Action:** [1-2 sentence description]
```

### 4. No Error Handling

**Before:**
```
Translate this text to French.
```

**After:**
```
Translate this text to French.

IF the text is already in French:
  → Indicate "The text is already in French" and suggest style improvements.

IF the text contains technical jargon:
  → Keep technical terms in English with translation in parentheses.

IF the text is too long (>1000 words):
  → Ask for confirmation before proceeding.
```

### 5. Insufficient Emphasis

**Before:**
```
Don't make up information.
```

**After:**
```
CRITICAL - ZERO TOLERANCE: NEVER make up information.
IF uncertain → Explicitly say "I'm not sure about..."
IF no data → Say "I don't have this information"
```

## Improvement Techniques

### Add Chain-of-Thought

```markdown
# Addition
Before answering, think step by step:
1. What exactly is being asked?
2. What information do I have?
3. What is the best approach?
4. Are there pitfalls to avoid?
```

### Add Examples

```markdown
# Addition
## Examples

### Good example
Input: [...]
Output: [Expected output]

### Bad example (to avoid)
Input: [...]
Incorrect output: [What we don't want]
Why incorrect: [Explanation]
```

### Strengthen Guardrails

```markdown
# Addition
## Forbidden (STRICT)
- [Forbidden behavior 1]
- [Forbidden behavior 2]

## Required (ALWAYS)
- [Required behavior 1]
- [Required behavior 2]
```

## Optimization Report Format

```markdown
# Optimization of [Prompt Name]

## Before/After Score
| Criterion | Before | After |
|-----------|--------|-------|
| Clarity | X/10 | Y/10 |
| Structure | X/10 | Y/10 |
| Completeness | X/10 | Y/10 |
| Guardrails | X/10 | Y/10 |
| **Total** | **X/40** | **Y/40** |

## Identified Issues
1. [Issue 1]
2. [Issue 2]

## Applied Changes
| Before | After | Reason |
|--------|-------|--------|
| [...] | [...] | [...] |

## Optimized Prompt
---
[THE COMPLETE PROMPT]
---

## Recommended Tests
- [ ] Standard case test
- [ ] Edge case test 1
- [ ] Edge case test 2
```

## Forbidden

- Never change the original meaning of the prompt
- Never add unrequested features
- Never remove existing guardrails
- Never make the prompt longer without justification
