---
name: systematic-debugging
description: "Use for bugs, test failures, or unexpected behavior needing root cause"
version: 1.0.0
---

<objective>
Find the root cause before writing fixes. Understanding why something breaks leads to correct fixes. Guessing wastes time and creates new problems.

Core principle: If you can't explain WHY it's broken, you're not ready to fix it. Every
fix must address a specific, understood root cause. </objective>

<when-to-use>
Use for any technical issue: test failures, build errors, bugs, unexpected behavior, performance problems. Especially valuable when previous attempts haven't worked or when tempted to try a "quick fix."
</when-to-use>

<start-with-evidence>
Read error messages completely. Stack traces, line numbers, and error codes contain valuable information. The error message often points directly to the problem.

Work to reproduce the issue reliably. If you can't trigger it consistently, gather more
data before proposing solutions. Document the exact steps that trigger the failure.

Check what changed recently. Review commits, new dependencies, configuration changes,
environmental differences. Most bugs correlate with recent changes.
</start-with-evidence>

<trace-the-problem>
Follow the data flow backward from the error. Where does the bad value originate? Work through the call stack until you find the source. Understanding the complete path from source to symptom reveals the true problem.

When multiple components interact, add diagnostic output at each boundary to identify
which component fails. This narrows the investigation to the specific failing layer.
</trace-the-problem>

<compare-with-working-code>
Find similar code that works correctly. Compare the working and broken versions systematically. Every difference matters until proven otherwise.

When implementing a pattern, read reference implementations thoroughly. Understand their
dependencies, settings, and environmental requirements. </compare-with-working-code>

<test-understanding>
Form a clear hypothesis: "X causes the problem because Y." Test with the smallest possible change. Change one variable at a time to isolate the cause.

When a hypothesis proves wrong, form a new one based on what you learned. Don't layer
fixes on top of failed attempts. </test-understanding>

<implement-fix>
Create a test that reproduces the issue before fixing it. This ensures you understand the problem and can verify the fix works.

Apply a single, focused fix that addresses the root cause. Resist bundling other
improvements or refactoring.

Verify the fix resolves the issue without breaking other functionality. </implement-fix>

<recognizing-architectural-problems>
When multiple fix attempts fail in different ways, the architecture might be the problem. Signs include:
- Each fix reveals new coupling or shared state issues
- Fixes require extensive refactoring to work properly
- Each attempted fix creates new symptoms elsewhere

These patterns suggest reconsidering the fundamental approach rather than continuing to
patch symptoms. </recognizing-architectural-problems>

<warning-signs>
Stop and investigate properly when thinking:
- "Try this and see if it works"
- "Quick fix for now, investigate later"
- "I don't fully understand but this might help"
- "Here are several things to try"

These thoughts signal you're guessing rather than debugging systematically.
</warning-signs>

<when-stuck>
If you don't understand something, say so clearly. Ask for help or research more. Understanding the problem before attempting fixes saves time and prevents introducing new bugs.

Systematic debugging finds and fixes the real problem. Random attempts waste time and
create new issues. </when-stuck>
