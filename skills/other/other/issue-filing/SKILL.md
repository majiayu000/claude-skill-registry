---
name: issue-filing
description: >
  File framework issues after exhausting other approaches. Document complex
  problems with multiple failed attempts for framework authors. REQUIRES user
  permission. Use only after checking docs, community-docs, and trying multiple
  approaches.
---

# Filing Issues

**Location:** `patterns/$GITHUB_USER/issues/` for framework issues or pattern architecture questions

**IMPORTANT: File issues ONLY after exhausting all other approaches AND getting user permission.**

**Prerequisites before filing:**
1. ✅ Checked official `~/Code/labs/docs/common/` documentation
2. ✅ Searched community-docs superstitions
3. ✅ Studied similar working patterns
4. ✅ Tried multiple different approaches (document all attempts)
5. ✅ **Asked user if they want you to file an issue**

**Never file an issue without explicit user permission!**

## When to File an Issue

**After above prerequisites:**
- Encountering framework behavior you don't understand
- Pattern architecture questions that aren't answered by docs
- Suspected framework bugs or limitations
- Questions about "correct" way to do something
- Edge cases that might help others

**File naming:** `ISSUE-Brief-Title.md`

**Example:** `ISSUE-Automatic-Side-Effects.md`, `ISSUE-Reactive-Computed-Timing.md`

## Issue Template

```markdown
# Issue: [Brief Question/Problem Title]

## Summary

1-2 sentence summary of the issue or question.

## Use Case

**Pattern:** Name of the pattern where this came up

**What you're trying to accomplish:**
- Clear description of the goal
- Why you need this behavior
- Context about the pattern

## Current State (What Works)

Show what you have working currently (if anything):

```typescript
// Code that works (even if not ideal)
```

## What We Tried (Failed Attempts)

### Attempt 1: [Approach Name]

```typescript
// Code that didn't work
```

**Error:**
```
Exact error message
```

**Analysis:** Why you think this didn't work

---

### Attempt 2: [Another Approach]

[Same structure]

---

## Questions

1. **Main question about correct approach?**
2. **Alternative approaches to consider?**
3. **Is this even possible in current framework?**
4. **Missing something obvious?**

## Desired Behavior

What you want to happen:
1. Step 1
2. Step 2
3. Expected outcome

## Environment

- CommonTools framework (latest version)
- Any relevant pattern features being used
- Related patterns or components

---

**Any guidance on the correct approach would be greatly appreciated!**
```

## When to File vs. When to Use Community Docs

**File an issue when:**
- ✅ You have a specific, complex problem
- ✅ You've tried multiple approaches
- ✅ You have code examples showing what didn't work
- ✅ It's a framework design or architecture question
- ✅ It might be a framework bug or limitation
- ✅ You want framework author feedback

**Use community-docs/superstitions when:**
- ✅ You discovered a simple pattern that works
- ✅ It's a one-line fix or small code pattern
- ✅ You want to share empirical knowledge
- ✅ It might help others encountering similar issues
- ✅ You're not sure if it's the "right" way

**Examples:**

**Issue:** "How do I automatically trigger side effects when reactive values change?" (complex architecture question, multiple failed attempts)

**Superstition:** "Use `Cell<Item[]>` not `Cell<OpaqueRef<Item>[]>` in handler signatures" (simple pattern that works)

## Workflow

**CRITICAL: Issues are a last resort. Only create after exhausting all other options.**

1. **Encounter framework confusion** that docs don't resolve
2. **Exhaust recovery strategies:**
   - Check official labs/docs/
   - Search community-docs superstitions
   - Study similar working patterns
   - Try multiple different approaches
   - Consider asking user for clarification first
3. **Ask user permission:**
   ```
   "I've tried [list approaches]. This seems like a framework architecture question.
   Would you like me to file an issue in patterns/$GITHUB_USER/issues/ to document
   this for framework authors to review?"
   ```
4. **Only if user says yes:**
   - Check if similar issue exists in your issues/ folder
   - Create new issue file with template
   - Include all failed attempts with code
   - Document clear problem statement
   - Commit: `"Add issue: [brief description]"`

**Never file an issue proactively - always get user approval first.**

**Issues are questions for framework authors, not empirical discoveries.**

## Related Skills

- **recovery-strategies** - Use issue filing as final escalation step
- **community-docs** - Check before filing issues
- **pattern-development** - Issues arise during development
