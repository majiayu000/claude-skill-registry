---
name: run
description: Run TypeScript solution against test cases. Use when user wants to test their code.
argument-hint: [solution-file]
allowed-tools: Read, Bash, Glob
---

Run the user's TypeScript solution against test cases.

File to run: $ARGUMENTS
(If empty, look for solution.ts in current directory)

Process:
1. Find the solution file
2. Find corresponding test file (solution.test.json or tests.json in same directory)
3. Execute with: npx tsx lib/leetcode_problem_runner/index.ts <file> [test-file]
4. Report results clearly

Test file format expected:
```json
{
  "functionName": "twoSum",
  "cases": [
    { "input": [[2,7,11,15], 9], "expected": [0,1] },
    { "input": [[3,2,4], 6], "expected": [1,2] }
  ]
}
```

Output format:
```
Running: [functionName]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Test 1: ✓ PASS (0.12ms)
  Input: [2,7,11,15], 9
  Expected: [0,1]
  Got: [0,1]

Test 2: ✗ FAIL (0.08ms)
  Input: [3,2,4], 6
  Expected: [1,2]
  Got: [0,2]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Results: 1/2 passed
Total time: 0.20ms
```

If tests fail, analyze the failure and offer to help debug.
If no test file exists, offer to create one based on the problem.
