---
name: verify
description: >-
  Verify a competitive programming or LeetCode solution for correctness, edge cases,
  and performance. Use when asked to "verify my solution", "check my code", "is this
  solution correct", "test my solution", "review my competitive programming answer",
  "validate my algorithm", or any solution verification request.
argument-hint: <problem-statement> [solution-code-or-file-path]
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Write, Glob, Grep, Bash, Task, AskUserQuestion
---

# Solution Verifier

Verify competitive programming and LeetCode solutions for correctness through static analysis, automated test case generation, and execution.

**CRITICAL: Complete ALL 4 phases. Do not stop after static analysis.**

## Phase 1: Parse Input

**Goal:** Extract the problem statement and solution code.

Parse `$ARGUMENTS` to extract:
1. **Problem statement** — the full problem description with constraints, I/O format, and examples
2. **Solution code** — the user's Python solution (inline code, file path, or pasted)

If both are in `$ARGUMENTS`, separate them. The problem statement typically comes first, followed by the solution code in a code block or after a separator.

If the solution is a file path, read it:
```
Read [file_path]
```

If the problem statement is missing, ask for it:
```
AskUserQuestion:
  question: "Please provide the problem statement for verification. I need it to generate test cases and validate correctness."
  options:
    - label: "Paste problem text"
      description: "Paste the full problem statement with constraints and examples"
    - label: "Describe the problem"
      description: "Describe what the problem asks — I'll generate test cases from that"
```

If the solution code is missing, ask for it:
```
AskUserQuestion:
  question: "Please provide your solution code to verify."
  options:
    - label: "Paste code"
      description: "Paste your Python solution code"
    - label: "Provide file path"
      description: "Give the path to your solution file"
```

If the solution is not Python, note this to the user and proceed with analysis (the verifier agent will handle language adaptation).

## Phase 2: Spawn Verifier Agent

**Goal:** Delegate verification to the specialized agent.

Use the Task tool to spawn the solution-verifier agent:

```
Task:
  subagent_type: "agent-alchemy-cs-tools:solution-verifier"
  prompt: |
    ## Problem Statement
    [full problem text with all constraints, I/O format, and examples]

    ## Solution Code
    ```python
    [the user's solution code]
    ```

    Perform full verification following your structured process:
    1. Static analysis for logic errors and edge case handling
    2. Generate test cases (basic, edge, stress)
    3. Write and execute test harness
    4. Compile report with verdict
```

## Phase 3: Receive Results

**Goal:** Collect and validate the agent's findings.

The agent returns a structured report containing:
- Static analysis findings with severity ratings
- Test results table (pass/fail per test case)
- Overall verdict (CORRECT / INCORRECT / PARTIALLY CORRECT / TLE RISK)
- Bug analysis for failures (root cause, affected lines, fix suggestion)
- Performance assessment (algorithm complexity vs constraint requirements)
- Improvement suggestions

Review the report for completeness. If the agent encountered infrastructure issues (test harness errors, not solution bugs), note this to the user.

## Phase 4: Present Report

**Goal:** Present the verification results with follow-up options.

Present the report to the user with clear formatting:

1. **Verdict** — the overall result prominently displayed
2. **Static Analysis** — findings table if there are any Critical or Warning findings
3. **Test Results** — the pass/fail table showing all test cases
4. **Bug Analysis** — for each failure: root cause, affected lines, and specific fix suggestion
5. **Performance Assessment** — whether the solution meets time/space requirements
6. **Improvement Suggestions** — code quality and optimization recommendations

After presenting the report, offer follow-up actions:

```
AskUserQuestion:
  question: "What would you like to do next?"
  options:
    - label: "Fix bugs and re-verify"
      description: "I'll apply the suggested fixes and run verification again"
    - label: "Show corrected solution"
      description: "Generate a complete corrected solution using /solve"
    - label: "Add more test cases"
      description: "Generate additional test cases targeting specific scenarios"
    - label: "Done"
      description: "Verification complete, no further action needed"
```

If the user selects "Fix bugs and re-verify":
- Apply the fix suggestions from the bug analysis
- Re-run Phase 2-4 with the corrected code

If "Show corrected solution":
- Suggest using `/solve` with the same problem statement to get a fresh, verified solution

If "Add more test cases":
- Ask what scenarios to target (specific edge cases, larger inputs, adversarial cases)
- Re-spawn the verifier with additional test requirements
