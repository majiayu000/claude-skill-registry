---
name: quality-reflective-questions
description: |
  Provides reflective questioning framework to challenge assumptions about work completeness,
  catching incomplete implementations before they're marked "done". Use before claiming features
  complete, before moving ADRs to completed status, during self-review, or when declaring work
  finished. Triggers on "is this really done", "self-review my work", "challenge my assumptions",
  "verify completeness", or proactively before marking tasks complete. Works with any type of
  implementation work. Enforces critical thinking about integration, testing, and execution proof.

---

# Reflective Questions for Work Completeness

## Quick Start

Before marking ANYTHING as "done", ask yourself these questions and provide HONEST answers:

### The Four Mandatory Questions

1. **How do I trigger this?** (What's the entry point?)
2. **What connects it to the system?** (Where's the wiring?)
3. **What evidence proves it runs?** (Show me the logs)
4. **What shows it works correctly?** (What's the outcome?)

If you **cannot answer ALL FOUR** with specific, concrete details, **the work is NOT complete**.

### The Honesty Test

Replace vague answers with specific evidence:

❌ **Bad (vague):** "It's integrated" → ✅ **Good (specific):** "Imported in builder.py line 45"
❌ **Bad (vague):** "It works" → ✅ **Good (specific):** "Logs show execution at 10:30:45"
❌ **Bad (vague):** "Tests pass" → ✅ **Good (specific):** "46 unit tests + 2 integration tests pass"

## Table of Contents

1. When to Use This Skill
2. What This Skill Does
3. The Four Mandatory Questions (Deep Dive)
4. Category-Specific Questions
5. Red Flag Questions
6. The Honesty Checklist
7. Common Self-Deception Patterns
8. Supporting Files
9. Expected Outcomes
10. Requirements
11. Red Flags to Avoid

## When to Use This Skill

### Explicit Triggers
- "Challenge my assumptions about completeness"
- "Ask me reflective questions about my work"
- "Self-review my implementation"
- "Is this really done?"
- "Verify my work is complete"
- "Question my completion claims"

### Implicit Triggers (PROACTIVE)
- **Before marking any task complete** (every single time)
- **Before moving ADR from in_progress to completed**
- **Before claiming "feature works"**
- **Before self-approving work**
- **After implementing any feature**
- **When about to say "all tests passing ✅"**

### Debugging Triggers
- "Why do I feel uncertain about this?"
- "Something seems incomplete but I can't pinpoint it"
- "I want to mark this done but have doubts"
- "Am I missing something?"

## What This Skill Does

This skill provides a **structured framework of reflective questions** that:

1. **Challenges assumptions** about what "done" means
2. **Exposes gaps** between claimed completion and actual completion
3. **Forces specificity** instead of vague assurances
4. **Prevents premature completion** by requiring evidence
5. **Catches integration failures** before they become incidents

**This skill complements `quality-verify-implementation-complete`** by providing the mental framework for self-questioning BEFORE running technical verification.

## The Four Mandatory Questions (Deep Dive)

These questions MUST be answered for EVERY piece of work before claiming "done".

### Question 1: How do I trigger this?

**Purpose:** Verify the feature has a reachable entry point

**What it really asks:**
- Can a user/system actually invoke this code?
- Is there a documented way to make this execute?
- Could someone else trigger this without asking me?

**Good Answers (Specific):**
- ✅ "Run: `uv run temet-run -a talky -p 'analyze code'`"
- ✅ "Call: `curl -X POST /api/endpoint -d '{...}'`"
- ✅ "Import: `from myapp import MyService; MyService().method()`"
- ✅ "Event: Coordinator triggers when `should_review_architecture()` returns True"

**Bad Answers (Vague):**
- ❌ "Run the system"
- ❌ "It's automatic"
- ❌ "The coordinator calls it"
- ❌ "When needed"

**Follow-up Questions:**
- "Can you show me the EXACT command right now?"
- "What arguments/parameters are required?"
- "Under what conditions does this trigger?"
- "Could you trigger this in the next 30 seconds if asked?"

**If you cannot answer specifically:** The feature has no entry point → NOT COMPLETE

### Question 2: What connects it to the system?

**Purpose:** Verify the artifact is actually wired into the codebase

**What it really asks:**
- Where is the import statement?
- Where is the registration/initialization?
- Where is the configuration that enables this?
- Can you show me the LINE NUMBER where this is connected?

**Good Answers (Specific):**
- ✅ "builder.py line 45: `from .architecture_nodes import create_review_node`"
- ✅ "main.py line 12: `app.add_command(my_command)`"
- ✅ "container.py line 67: `container.register(MyService, scope=Scope.SINGLETON)`"
- ✅ "routes.py line 23: `router.add_route('/endpoint', handler)`"

**Bad Answers (Vague):**
- ❌ "It's imported"
- ❌ "It's in the builder"
- ❌ "It's registered"
- ❌ "It's wired up"

**Follow-up Questions:**
- "Can you paste the EXACT import line?"
- "What FILE and LINE NUMBER has the registration?"
- "Can you show me with grep output?"
- "Could I find this connection in 60 seconds if I looked?"

**If you cannot answer specifically:** The artifact is orphaned → NOT COMPLETE

### Question 3: What evidence proves it runs?

**Purpose:** Verify the code actually executes at runtime

**What it really asks:**
- Have you ACTUALLY triggered this and observed execution?
- What logs/traces show this code path was hit?
- Can you show me timestamped evidence of execution?
- Did you observe this with your own eyes (or grep)?

**Good Answers (Specific):**
- ✅ "Logs: `[2025-12-07 10:30:45] INFO architecture_review_triggered agent=talky`"
- ✅ "Output: `✓ Task completed successfully` (from CLI run at 10:30)"
- ✅ "Trace: OpenTelemetry span `architecture_review` with duration 1.2s"
- ✅ "Debug: Added print statement, saw output 'Node executed'"

**Bad Answers (Vague):**
- ❌ "It should run"
- ❌ "Tests pass"
- ❌ "No errors when I ran it"
- ❌ "The system works"

**Follow-up Questions:**
- "Can you paste the ACTUAL log line showing execution?"
- "What TIMESTAMP did this execute?"
- "Did you observe this directly or are you assuming?"
- "Could you trigger this RIGHT NOW and show me the logs?"

**If you cannot answer specifically:** No execution proof → NOT COMPLETE

### Question 4: What shows it works correctly?

**Purpose:** Verify the code produces the expected outcome

**What it really asks:**
- What observable outcome proves correct behavior?
- What state changed as a result of execution?
- What output/artifact was created?
- How do you KNOW it did the right thing?

**Good Answers (Specific):**
- ✅ "State: `result.architecture_review = ArchitectureReviewResult(status=APPROVED, violations=[])`"
- ✅ "Database: Row inserted with ID 123, verified with query"
- ✅ "File: Created `output.txt` with expected contents (see: cat output.txt)"
- ✅ "API: Returned HTTP 200 with JSON body containing expected fields"

**Bad Answers (Vague):**
- ❌ "It works"
- ❌ "No errors"
- ❌ "Tests pass"
- ❌ "Everything looks good"

**Follow-up Questions:**
- "Can you show me the EXACT output/state change?"
- "What VALUE did this produce?"
- "How do you KNOW this is correct vs just 'no errors'?"
- "Could you demonstrate correct behavior RIGHT NOW?"

**If you cannot answer specifically:** No outcome proof → NOT COMPLETE

## Category-Specific Questions

Apply the Four Questions framework to specific implementation types. For detailed questions by category, see [references/category-specific-questions.md](./references/category-specific-questions.md).

**Categories covered:**
- **Modules/Files**: Import verification, call-site validation
- **LangGraph Nodes**: Graph registration, edge connectivity
- **CLI Commands**: Registration, --help visibility, execution
- **Service Classes (DI)**: Container registration, injection points
- **API Endpoints**: Route registration, response validation

## Red Flag Questions

These questions expose common self-deception patterns. If you answer "yes" to any, **stop and investigate**.

### Integration Red Flags

1. **"Did I only test this in isolation?"**
   - If YES: You might have orphaned code
   - Action: Add integration test, verify in real system

2. **"Am I assuming something is connected without verifying?"**
   - If YES: Assumption might be wrong
   - Action: Grep for imports, verify connection exists

3. **"Did I only run unit tests, not integration tests?"**
   - If YES: Integration might be broken
   - Action: Create/run integration tests

4. **"Am I relying on 'should' or 'probably' language?"**
   - If YES: You're guessing, not verifying
   - Action: Replace guesses with evidence

5. **"Could this code exist and never execute?"**
   - If YES: It might be orphaned
   - Action: Verify call-sites exist in production code

### Execution Red Flags

6. **"Have I not actually triggered this feature?"**
   - If YES: You don't know if it works
   - Action: Trigger it, observe execution

7. **"Am I claiming it works based on 'no errors' vs positive proof?"**
   - If YES: Absence of errors ≠ presence of success
   - Action: Show positive evidence of correct behavior

8. **"Did I forget to check logs after running?"**
   - If YES: No execution proof
   - Action: Run again, capture logs

9. **"Am I trusting tests alone without manual verification?"**
   - If YES: Tests might be mocked/isolated
   - Action: Manual E2E test, verify in real environment

10. **"Could this feature be wired but the conditional never triggers?"**
    - If YES: Dead code path
    - Action: Verify the condition is reachable

### Completion Red Flags

11. **"Am I rushing to mark this complete?"**
    - If YES: Slow down, verify properly
    - Action: Run through Four Questions again

12. **"Do I have doubts I'm ignoring?"**
    - If YES: Your instinct is usually right
    - Action: Investigate the doubt before proceeding

13. **"Would I bet $1000 this works end-to-end?"**
    - If NO: You're not confident
    - Action: Find out why, verify until confident

14. **"Could someone else verify this works without asking me?"**
    - If NO: Insufficient documentation/evidence
    - Action: Document entry point, provide evidence

15. **"Am I self-approving without external review?"**
    - If YES: You might miss blind spots
    - Action: Request reviewer agent or peer review

## The Honesty Checklist

Before marking ANYTHING complete, answer these honestly:

### Evidence Requirements

- [ ] **I can paste the exact command to trigger this feature**
      (Not "run the system" - the EXACT command with args)

- [ ] **I can show the file and line number where this is imported/registered**
      (Not "it's in builder.py" - the EXACT line number)

- [ ] **I have actual logs showing this code executed**
      (Not "it should log" - actual timestamped log lines)

- [ ] **I can show the specific output/state change this produced**
      (Not "it works" - the EXACT output/data)

- [ ] **I triggered this manually and observed it work**
      (Not "tests pass" - I personally ran it)

### Integration Requirements

- [ ] **This code is imported in at least one production file**
      (grep output shows import, not just tests)

- [ ] **This code has call-sites in production paths**
      (grep output shows calls, not just definitions)

- [ ] **This code is registered/wired where it needs to be**
      (container, graph, router, CLI - verified)

- [ ] **Integration tests verify this component is in the system**
      (Not just unit tests - integration/E2E tests exist)

### Outcome Requirements

- [ ] **I can demonstrate this works to someone else right now**
      (Could walk someone through triggering and observing)

- [ ] **The behavior matches the specification**
      (Not just "no errors" - correct behavior observed)

- [ ] **I would bet money this works end-to-end**
      (Confident enough to stake reputation on it)

- [ ] **I have answered all Four Questions with specific details**
      (No vague answers, all concrete)

### If ANY checkbox is unchecked: **NOT COMPLETE**

## Common Self-Deception Patterns

Be aware of these patterns that lead to premature completion claims. For detailed analysis and fixes, see [references/self-deception-patterns.md](./references/self-deception-patterns.md).

**Common Patterns:**
1. **"Tests Pass" Syndrome** - Unit tests pass but integration untested
2. **"Should Work" Fallacy** - Using assumptions instead of evidence
3. **"No Errors" Confusion** - Equating silence with correctness
4. **"File Exists" Completion** - Code written but not integrated
5. **"Looks Good" Approval** - Vague approval without specifics
6. **"I Remember Doing It"** - Trusting memory over verification
7. **"Later Will Be Fine"** - Deferring critical verification steps

## Usage

1. **Before marking work complete**, run through the Four Questions
2. **Check the Honesty Checklist** - all boxes must be checked
3. **Verify no Red Flags** are present
4. **If uncertain**, review [references/category-specific-questions.md](./references/category-specific-questions.md) for your implementation type

**Supporting Files:**
- [references/category-specific-questions.md](./references/category-specific-questions.md) - Detailed questions by category
- [references/self-deception-patterns.md](./references/self-deception-patterns.md) - Pattern recognition and fixes

## Expected Outcomes

### Successful Self-Review

```
Reflective Questions Self-Review
Feature: ArchitectureReview Node
Date: 2025-12-07

FOUR MANDATORY QUESTIONS:

1. How do I trigger this?
   ✅ SPECIFIC: uv run temet-run -a talky -p "Write a function"
   When should_review_architecture() returns True (when code_changes detected)

2. What connects it to the system?
   ✅ SPECIFIC: builder.py line 12: from .architecture_nodes import create_architecture_review_node
   builder.py line 146: graph.add_node("architecture_review", review_node)
   builder.py line 189: Conditional edge from "query_claude"

3. What evidence proves it runs?
   ✅ SPECIFIC: Logs from execution at 2025-12-07 10:30:45:
   [INFO] architecture_review_triggered agent=talky session=abc123
   [INFO] architecture_review_complete status=approved violations=0

4. What shows it works correctly?
   ✅ SPECIFIC: state.architecture_review = ArchitectureReviewResult(
       status=ReviewStatus.APPROVED,
       violations=[],
       recommendations=["Code follows Clean Architecture"]
   )

HONESTY CHECKLIST:
✅ All evidence specific, not vague
✅ All connections verified with grep
✅ Execution observed directly
✅ Outcome matches specification

SELF-DECEPTION CHECK:
✅ Not relying on "tests pass" alone
✅ Not using "should" or "probably"
✅ Not assuming - all verified
✅ Would bet $1000 this works

DECISION: ✅ WORK IS COMPLETE
Ready to mark as done.
```

### Failed Self-Review (Catches Incompleteness)

```
Reflective Questions Self-Review
Feature: ArchitectureReview Node
Date: 2025-12-05 (BEFORE FIX)

FOUR MANDATORY QUESTIONS:

1. How do I trigger this?
   ⚠️  VAGUE: "Run the coordinator"
   FOLLOW-UP: What's the EXACT command?
   RE-ANSWER: uv run temet-run -a talky -p "..."
   ⚠️  STILL VAGUE: What prompts trigger the node?

2. What connects it to the system?
   ❌ VAGUE: "It should be in builder.py"
   FOLLOW-UP: Can you show me the line number?
   RE-CHECK: grep "architecture_nodes" builder.py
   RESULT: (empty) ❌
   CRITICAL: MODULE IS NOT IMPORTED

3. What evidence proves it runs?
   ❌ ASSUMPTION: "Tests pass so it should run"
   FOLLOW-UP: Have you actually run it and seen logs?
   RE-ANSWER: "No, just ran unit tests"
   CRITICAL: NO EXECUTION PROOF

4. What shows it works correctly?
   ❌ ASSUMPTION: "Tests verify behavior"
   FOLLOW-UP: What actual output did you observe?
   RE-ANSWER: "Just the test assertions passing"
   CRITICAL: NO RUNTIME OUTCOME PROOF

HONESTY CHECKLIST:
❌ Using vague language ("should", "I think")
❌ No specific line numbers or imports shown
❌ No execution logs captured
❌ Relying on tests, not runtime verification

SELF-DECEPTION CHECK:
❌ Relying on "tests pass" only
❌ Using "should" repeatedly
❌ Assuming instead of verifying
❌ Would NOT bet $1000 (honest answer: no)

DECISION: ❌ WORK IS NOT COMPLETE
Critical issues found:
1. Module not imported in builder.py
2. No runtime execution proof
3. No integration test

DO NOT mark as done. Fix integration first.
```

## Requirements

### Tools Required
- None (this is a mental framework)

### Knowledge Required
- Understanding of what "done" means in your domain
- Willingness to be honest with yourself
- Ability to distinguish vague from specific answers

### Mindset Required
- **Intellectual honesty** - Admit when you don't know
- **Rigor** - Don't accept vague answers from yourself
- **Patience** - Take time to verify properly
- **Courage** - Admit incompleteness vs rushing to "done"

## Red Flags to Avoid

### Do Not
- ❌ Accept vague answers from yourself
- ❌ Use "should", "probably", "I think" language
- ❌ Rush through questions to mark done faster
- ❌ Skip questions that feel uncomfortable
- ❌ Trust memory instead of current verification
- ❌ Assume connection without grep proof
- ❌ Claim execution without logs
- ❌ Rely on unit tests alone for integration work

### Do
- ✅ Answer all Four Questions with specific details
- ✅ Replace assumptions with evidence
- ✅ Be honest about gaps and uncertainties
- ✅ Verify current state, don't trust memory
- ✅ Show concrete proof (line numbers, logs, output)
- ✅ Admit incompleteness when found
- ✅ Fix gaps before marking complete
- ✅ Use this framework for EVERY completion claim

## Notes

- This skill was created in response to ADR-013 (2025-12-07)
- The pattern: Self-deception about completeness led to orphaned code
- This skill provides the mental framework BEFORE technical verification
- Pair this with `quality-verify-implementation-complete` for full coverage
- The Four Questions are the MINIMUM bar, not the complete verification
- Honesty with yourself is the foundation of quality work

**Remember:** The person you're most likely to deceive is yourself. These questions force honesty.
