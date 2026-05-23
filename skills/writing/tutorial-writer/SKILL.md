---
name: tutorial-writer
description: Creates beginner-friendly, learning-oriented tutorials following Diátaxis Tutorial pattern. Step-by-step guides with success criteria, time estimates, and complete working examples. Zero tolerance for fabricated APIs - all code verified against source. Use for new developer onboarding, teaching new features, guiding beginners through first steps, or when "getting started" documentation is missing.
version: 2.0.0
---

# Tutorial Writer Skill

## Purpose

Create comprehensive, beginner-friendly tutorials that take learners from zero to a working result. Follows the Diátaxis Tutorial pattern for learning-oriented documentation. Verifies all APIs against source code before documenting, with complete working examples that have been tested.

## When to Load Additional References

The workflow below covers the essential tutorial creation process. Load detailed references when:

**For complete tutorial structure and examples:**

```
Read `~/.claude/skills/tutorial-writer/references/TUTORIAL-TEMPLATE.md`
```

Use when: Creating a new tutorial, need complete markdown template, step structure examples, metadata format

**For avoiding common mistakes:**

```
Read `~/.claude/skills/tutorial-writer/references/PITFALLS-GUIDE.md`
```

Use when: Reviewing tutorial quality, 7 common pitfalls with BAD/GOOD examples, recovery strategies

**For testing and verification procedures:**

```
Read `~/.claude/skills/tutorial-writer/references/TESTING-VERIFICATION.md`
```

Use when: Need to test tutorial, create test environment, verify APIs, check time estimates, beginner testing protocol

**For detailed Diátaxis framework guidance:**

```
Read `~/.claude/skills/shared/references/DIATAXIS-FRAMEWORK.md`
```

Use when: Understanding Diátaxis tutorial pattern, comparing with other doc types (how-to, explanation, reference)

---

## Diátaxis Framework: Tutorial

**Tutorial Type Characteristics:**

- **Learning-oriented** - Teaching, not just documenting
- **Beginner-focused** - Takes learner from zero to working result
- **Step-by-step** - Explicit, numbered steps with clear progression
- **Success criteria** - Learner can verify each step worked
- **Minimal explanations** - WHAT to do, not WHY it works (link to explanations)
- **Safe environment** - No production concerns, focus on learning
- **Confidence building** - Early steps are very simple to build momentum
- **Complete examples** - Everything needed to succeed included

**What NOT to Include:**

- ❌ Complete API reference - Link to api-doc-writer docs
- ❌ Problem-solving patterns - That's migration-guide-writer territory
- ❌ Deep explanations of WHY - Link to explanation docs
- ❌ Production deployment - Keep focus on learning basics

---

## Critical Rules (Zero Tolerance)

### P0 - CRITICAL Violations (Must Fix)

1. **Fabricated APIs** - Methods that don't exist in source code
2. **Wrong Signatures** - Incorrect parameter types or names
3. **Invalid Code** - Examples that won't compile or run
4. **Missing Success Criteria** - Steps without verification method
5. **Untested Examples** - Code you haven't actually run

### P1 - HIGH Violations (Should Fix)

6. **Too Advanced** - Assumes knowledge beginner doesn't have
7. **No Prerequisites** - Doesn't state what's needed before starting
8. **Missing Expected Output** - Doesn't show what success looks like
9. **No Time Estimates** - Learner doesn't know how long it takes

### P2 - MEDIUM Violations

10. **Too Much Explanation** - Getting into WHY when should focus on WHAT
11. **Marketing Language** - Buzzwords instead of clear instructions

---

## Workflow Overview

### Step 1: Goal Definition (5-10 minutes)

Define the learning outcome:

- **What they'll learn**: Specific skill or capability
- **Target audience**: Experience level, prerequisites
- **Success criteria**: By the end, learner will be able to...
- **What they'll build**: Concrete deliverable (not abstract understanding)

### Step 2: Source Code Research (10-15 minutes)

**CRITICAL:** Verify all APIs before writing.

```bash
# Read source files for APIs
Read [source_files_for_apis]

# Extract exact signatures
# Verify imports
# Find or create working example
# Check test files for usage patterns
```

**Create API verification checklist:**

```markdown
## APIs to Use in Tutorial

- [ ] `APIMethod1` - Verified in [source_file.ext:line]
- [ ] `APIMethod2` - Verified in [source_file.ext:line]
- [ ] `ConfigOption1` - Verified in [config_file.ext]

All signatures copied exactly ✅
All imports verified ✅
```

**Test the example yourself** - This is REQUIRED, don't guess!

### Step 3: Step Breakdown (10-15 minutes)

Break working example into logical steps:

**Principles:**

1. **Start absurdly simple** - First step should be trivial (builds confidence)
2. **One concept per step** - Don't introduce multiple new things at once
3. **Clear success criteria** - Each step has verifiable outcome
4. **Realistic time estimates** - Be honest about time needed
5. **Progressive complexity** - Each step slightly harder than previous

**For complete step breakdown examples:** See `references/TUTORIAL-TEMPLATE.md`

### Step 4: Writing (20-30 minutes)

**Tutorial structure:**

```markdown
# Getting Started with [System/Feature]

[Brief introduction - 2-3 sentences]

## Prerequisites

**Before you start, you need:**

- [Requirements with version numbers]

**Check your setup:** [commands to verify]

## What You'll Build

- ✅ [Concrete outcome 1]
- ✅ [Concrete outcome 2]

**Total time**: [Realistic estimate]

---

## Step 1: [Action] ([time] minutes)

[Very brief context - 1-2 sentences max]

[Code with VERIFIED APIs]

**Run it:** [command]

**Expected output:** [EXACT output from testing]

✅ **Success check**: [Verification]

---

[Continue with remaining steps...]

## Complete Working Code

[Full, tested code]

## What You Learned

- ✅ [Skill 1]
- ✅ [Skill 2]

## Next Steps

- **Explore more**: [API Reference link]
- **Solve problems**: [How-To Guides link]
```

**For complete template with all sections:** See `references/TUTORIAL-TEMPLATE.md`

### Step 5: Testing (15-20 minutes)

**CRITICAL:** Actually run through the tutorial yourself.

This is NOT optional. You MUST test the tutorial.

```bash
# Create fresh environment
# Follow your own tutorial exactly
# Do NOT skip any steps
# Do NOT assume things work
```

**As you test, verify:**

- [ ] Each command produces stated output
- [ ] Success criteria are achievable
- [ ] Time estimates are realistic (add 50% buffer for beginners)
- [ ] No steps are confusing or ambiguous
- [ ] Prerequisites are sufficient
- [ ] Complete code at end works
- [ ] All APIs work as shown

**If ANY step fails during testing:**

- ❌ Do NOT publish tutorial
- Fix the step
- Test again from beginning
- Only publish after complete successful run-through

**For detailed testing procedures:** See `references/TESTING-VERIFICATION.md`

### Step 6: Verification (5-10 minutes)

**Verification checklist:**

```markdown
## Tutorial Verification Checklist

### Testing (P0 - CRITICAL)

- [ ] Tutorial tested start-to-finish
- [ ] All commands run successfully
- [ ] All outputs match documentation
- [ ] Complete code tested and works

### API Verification (P0 - CRITICAL)

- [ ] All APIs verified against source
- [ ] All signatures exact
- [ ] All imports real
- [ ] No fabricated methods

### Learning Structure (P1 - HIGH)

- [ ] Success criteria for each step
- [ ] Time estimates for each step
- [ ] Prerequisites clearly stated
- [ ] Expected outputs documented
```

**Add metadata footer to tutorial:**

```markdown
---

**Tutorial Metadata**

**Last Updated**: [YYYY-MM-DD]
**System Version**: [Version this tutorial is for]
**Verified**: ✅ Tutorial tested and working
**Test Date**: [YYYY-MM-DD]

**Verification**:

- ✅ All code examples tested
- ✅ All APIs verified against source
- ✅ Expected outputs confirmed

**Source files verified**:

- `path/to/source/file1.ext`
```

---

## Common Pitfalls to Avoid

1. **Assuming Too Much Knowledge** - Start from absolute zero
2. **Missing Expected Output** - Show exact output for every command
3. **No Success Verification** - Every step needs verification method
4. **Too Many Concepts Per Step** - One new concept at a time
5. **Fabricated or Untested Code** - All code must be tested
6. **Too Much Explanation** - Focus on WHAT, link to WHY
7. **Unrealistic Time Estimates** - Test with beginners, include buffer

**For detailed pitfall examples with BAD/GOOD comparisons:** See `references/PITFALLS-GUIDE.md`

---

## Integration with Other Skills

### Works With:

- **api-doc-writer** - Link to API reference for deeper info
- **migration-guide-writer** - After tutorial, guide to migrate existing code
- **api-documentation-verify** - Verify tutorial code accuracy

### Invokes:

- None (standalone skill)

### Invoked By:

- User (manual invocation)
- When onboarding documentation needed
- After major feature releases

---

## Output Format

**Primary Output**: Markdown file with structured tutorial

**File Location**:

- `docs/tutorials/getting-started-with-[feature].md`
- `TUTORIAL.md` in project root
- `docs/getting-started/[feature].md`

---

## Time Estimates

**Simple Tutorial** (< 5 steps, single concept): 1-2 hours to create
**Medium Tutorial** (5-10 steps, multiple concepts): 2-4 hours to create
**Complex Tutorial** (10+ steps, advanced concepts): 4-8 hours to create

**Include testing time!** Testing often takes as long as writing.

---

## Success Criteria

Tutorial is complete when:

- ✅ Tested start-to-finish successfully
- ✅ All APIs verified against source code
- ✅ All code examples work
- ✅ All commands produce documented output
- ✅ Success criteria clear for each step
- ✅ Time estimates realistic for beginners
- ✅ Prerequisites clearly stated
- ✅ Progressive complexity (simple → complex)
- ✅ Complete working code at end
- ✅ No fabricated APIs
- ✅ No marketing language
- ✅ Minimal explanations (WHAT not WHY)

---

## Special Considerations

### Emoji Usage (Exception to No-Emoji Rule)

Tutorials ARE allowed to use structural emojis for clarity:

✅ **Allowed** (structural/functional):

- ✅ Success checkmarks for verification
- ❌ Error indicators
- ⚠️ Warning symbols

❌ **Not Allowed** (decorative/marketing):

- 🚀 "Blazing fast"
- 💯 "Perfect"
- 🎉 "Exciting"

### Language Style

**Use clear, direct language:**

- "Create a file" not "Let's create a file"
- "Run the command" not "Now we'll run the command"
- "Install the package" not "You need to install the package"

**Be encouraging but factual:**

- ✅ "You've successfully created your first task"
- ❌ "Amazing! You're doing great!"

### Beginner-Friendly Practices

1. **No jargon without explanation**
2. **Link to prerequisite concepts**
3. **Show exact commands, not descriptions**
4. **Include complete context (imports, setup)**
5. **Verify each step immediately**
6. **Build confidence with early wins**
7. **Keep explanations minimal**
8. **Link to deeper explanations**

---

## Example Usage

```bash
# Manual invocation
/skill tutorial-writer

# User request
User: "I need a getting started guide for new developers"
Assistant: "I'll use tutorial-writer to create a beginner-friendly tutorial"

# After testing
User: "Create a tutorial for the TaskService API"
Assistant: "I'll create a step-by-step tutorial, test it, and verify all APIs"
```

---

## References

- Diátaxis Framework: https://diataxis.fr/tutorials/
- Tutorial Template: `references/TUTORIAL-TEMPLATE.md`
- Pitfalls Guide: `references/PITFALLS-GUIDE.md`
- Testing & Verification: `references/TESTING-VERIFICATION.md`
- Diátaxis Details: `~/.claude/skills/shared/references/DIATAXIS-FRAMEWORK.md`

---

## Related Agent

For comprehensive documentation guidance that coordinates this and other documentation skills, use the **`documentation-coordinator`** agent.
