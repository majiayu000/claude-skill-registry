---
name: stop
description: 'Anti-premature-coding protocol. MANDATORY pre-coding checkpoint: execute
  BEFORE writing ANY code (new features, bug fixes, refactoring, optimization, tests).
  Use when user requests: "implement/add/fix'
---

---
name: stop
description: Anti-premature-coding protocol. MANDATORY pre-coding checkpoint: execute BEFORE writing ANY code (new features, bug fixes, refactoring, optimization, tests). Use when user requests: "implement/add/fix/refactor/optimize/create feature". Prevents "coding without reading" blindspot that causes most bugs, duplicated work, and broken architectures. Forces systematic investigation via Stop→Trace→Orient→Plan before touching keyboard.
---

# STOP - Stop Coding, Start Thinking

## The Blindspot

Your brain lies to you: "I understand the problem, let me start coding!"

This is the **most dangerous coding habit**. You see a requirement or bug, and your fingers automatically reach for the keyboard. But you haven't:

- Read the existing code
- Understood the architecture
- Found similar patterns
- Identified dependencies

**Result**: 3 hours coding → 2 hours fixing → because the function already existed / your change broke something / you misunderstood the requirement.

## The Philosophy

**盲目开工，必返工** (Blind work guarantees rework)

韩非子: "审时度势，而后可动。"

Your code doesn't exist in isolation—it's part of a living codebase. Writing code without reading first is like barging into a conversation and shouting over everyone.

**核心原则**: Read before you write. Always.

## The STOP Protocol

**Trigger**: When you want to write code (new feature, bug fix, refactor, optimization)

**Execute this 4-step protocol** (5-15 minutes total):

### S - Stop (30 seconds)

**Don't touch the keyboard.**

Pause. Take a breath. Ask yourself:

- "Do I REALLY understand what needs to be done?"
- "Have I read the relevant code?"
- "What am I missing?"

**If you can't answer confidently → Go to T**

### T - Trace (5-10 minutes)

**Map the existing landscape.**

Use tools to understand before you act:

1. **Find relevant files**
   - Use `Glob` to find related files by pattern
   - Example: `**/*user*.ts` for user-related code

2. **Search for similar implementations**
   - Use `Grep` to find patterns
   - Search for function names, error types, or keywords
   - Example: `pattern: "handleLogin"` to find existing login logic

3. **Read the actual code**
   - Use `Read` to see the full implementation
   - Don't skim—actually read it
   - Understand the WHY, not just the WHAT

4. **Trace call hierarchies**
   - Use `LSP incomingCalls` to see who calls this function
   - Use `LSP outgoingCalls` to see what this function calls
   - Understand dependencies and impact

**What you're looking for**:
- Does this already exist? (Don't reinvent the wheel)
- How is this pattern currently implemented? (Follow conventions)
- What will break if I change this? (Understand impact)
- What's the architecture? (Respect the design)

### O - Orient (2-3 minutes)

**Locate yourself in the context.**

Now that you've traced the code, answer:

1. **Where does my change fit?**
   - Which file/module?
   - What's the existing pattern?
   - Should I follow or create new pattern?

2. **What's the minimal change?**
   - What's the smallest thing that works?
   - Can I reuse existing code?
   - Should I refactor instead?

3. **What are the risks?**
   - What depends on this code?
   - What could break?
   - What tests exist?

**If you can't answer these → Go back to T**

### P - Plan (1-2 minutes)

**Define your approach before coding.**

Write down:

1. **The specific change**
   - File: `src/auth/login.ts`
   - Function: `add error handling to authenticate()`
   - Approach: `wrap in try-catch, log error, rethrow`

2. **The testing strategy**
   - How will you verify it works?
   - What edge cases exist?

3. **The rollback plan**
   - If it breaks, how do you undo?

**Only NOW can you start coding.**

## When to Use STOP

**ALWAYS. Use for EVERY coding scenario:**

✅ **New features** - Read existing patterns, follow conventions
✅ **Bug fixes** - Trace the error source, understand the flow
✅ **Refactoring** - Understand why it's written this way first
✅ **Optimization** - Find the actual bottleneck before optimizing
✅ **Code reviews** - Understand the intent before judging
✅ **Debugging** - Map the call stack before adding logs

## Examples

### Example 1: New Feature

**Task**: "Add user logout functionality"

**Without STOP**: Write `logout()` function from scratch, spend 2 hours

**With STOP**:
- **S**: Stop
- **T**: Search `Grep: "login"` → find `login.ts` → Read it → See session management pattern
- **O**: Logout should mirror login's session cleanup, just reverse
- **P**: Add `logout()` in same file, reuse `clearSession()` helper
- **Result**: 15 minutes, follows existing pattern

### Example 2: Bug Fix

**Task**: "Fix: User can't update profile"

**Without STOP**: Add console.log everywhere, randomly change code

**With STOP**:
- **S**: Stop
- **T**: Find profile update code → Read it → Search for "validation" → Find validation middleware blocking update
- **O**: The bug isn't the update function, it's overly strict validation
- **P**: Relax validation rule, not rewrite update logic
- **Result**: Fix in 5 minutes

### Example 3: Refactoring

**Task**: "Clean up this messy function"

**Without STOP**: Rewrite from scratch, break things

**With STOP**:
- **S**: Stop
- **T**: Read function → Trace all callers → Understand why it's complex (handles 7 edge cases)
- **O**: The complexity is necessary—refactor into smaller helpers but keep logic
- **P**: Extract 3 helper functions, preserve edge cases
- **Result**: Cleaner code, same functionality, no bugs

## Edge Cases

**"The codebase is too big/large/complex"**
- Use STOP more, not less
- Start with the specific file/component
- Expand outward as needed

**"I'm just adding a small one-line change"**
- Especially then
- One-line changes often have hidden impact
- 2 minutes of tracing saves 2 hours of debugging

**"It's new code, nothing exists yet"**
- Trace similar patterns in the codebase
- Follow existing architecture
- Respect the conventions

**"I'm the only one working on this"**
- Doesn't matter
- Future you will thank present you
- Code is communication with your future self

**"I'm in a rush"**
- STOP saves time, doesn't cost it
- 15 minutes now > 3 hours of debugging later
- 韩非子: "欲速则不达" (Haste makes waste)

## Integration into Workflow

**Make it a habit:**

1. **Before every coding session**
   - Literal trigger: Hands on keyboard → STOP
   - Mental trigger: "I'm about to code" → "Have I STOP'd?"

2. **Code review checklist**
   - "Did you STOP before coding?"
   - "Show me what you traced"

3. **Pair programming**
   - Driver and Navigator both STOP
   - Compare findings before implementing

4. **Team culture**
   - "Did you read the code?" > "Did you write the code?"
   - Celebrate thorough investigation over quick fixes

## Common Anti-patterns

❌ **"I'll just code it and see"** - Gambling with time
❌ **"The code is self-explanatory"** - It's not, read it
❌ **"I know this pattern"** - This codebase might do it differently
❌ **"Searching takes too long"** - Debugging takes longer
❌ **"I'm an expert, I don't need to read"** - Experts read the most

## The Mantra

**不读就写，就是赌博** (Not reading before coding is gambling)

Every time you start coding without STOP, you're betting:
- The function doesn't already exist (it does)
- Your understanding is correct (it's not)
- Nothing will break (it will)

**House always wins. STOP beats the house.**

## Quick Reference

```
S - Stop    (30 sec)   - Don't touch keyboard
T - Trace   (5-10 min) - Read existing code, find patterns
O - Orient  (2-3 min)  - Understand context, locate change
P - Plan    (1-2 min)  - Define approach, then code
```

**Total time**: 5-15 minutes
**Time saved**: Hours of debugging, refactoring, and embarrassment

## Bundled Resources

### Advanced Tool Patterns

When you need detailed guidance on using Glob, Grep, Read, and LSP tools during the **Trace** phase, see [references/tool-patterns.md](references/tool-patterns.md).

Contains:
- Common search patterns for each tool
- Typical TRACE workflows with step-by-step examples
- Tool selection guide (when to use which tool)
- Pro tips and common pitfalls

**When to read**: You're in the Trace phase and want to maximize investigation efficiency.

---

### Complex Scenarios

When dealing with large codebases, legacy code, microservices, or other complex situations, see [references/complex-scenarios.md](references/complex-scenarios.md).

Contains:
- Large codebases (>100k lines): How to scope investigation
- Legacy code with no tests: Risk containment strategies
- Microservices: Mapping service boundaries
- Multiple valid approaches: Comparative analysis
- Emergency/hotfix: Focused investigation protocol
- Foreign codebases: Learning mode for new projects
- Performance optimization: Measure-first methodology

**When to read**: Your scenario doesn't fit the basic examples and needs adaptation.

---

### Plan Template

When documenting your Plan phase, use the template at [assets/plan-template.md](assets/plan-template.md).

Contains:
- Structured sections for documenting S-T-O-P findings
- Testing strategy checklist
- Rollback planning guide
- Execution log template
- Post-implementation review

**When to use**: You want to systematically document your investigation and plan.

---

**Remember**: The best code you write is the code you didn't have to write because you read it first.
