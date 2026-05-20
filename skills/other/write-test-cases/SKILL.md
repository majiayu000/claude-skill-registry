---
name: write-test-cases
description: Research and write test cases for a rule. Spawns a test-researcher to produce a coverage matrix, then test-case-writers (one per category) to create the files.
disable-model-invocation: true
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
argument-hint: [RuleId]
hooks:
  Stop:
    - command: "bash .claude/hooks/log-skill-usage.sh write-test-cases"
---

# Write Test Cases for a Rule

Rule ID: `$ARGUMENTS`

## Step 1: Spawn the test-researcher agent

Spawn the `test-researcher` agent with:
- The rule ID: `$ARGUMENTS`
- The plan path (if known)

The researcher will produce a coverage matrix at `tests/Spire.Analyzers.Tests/$ARGUMENTS/coverage-matrix.md`.

## Step 2: Review the coverage matrix

Read the coverage matrix. Check:
- Are all relevant detection methods covered?
- Are all syntactic contexts enumerated?
- Are there enough should_pass cases for edge cases and false positives?
- Are the file names clear and consistent?

Add or remove cases as needed by editing the matrix.

## Step 3: Spawn test-case-writer agents

For each **category** in the matrix, spawn one `test-case-writer` agent in parallel:
- Tell it the rule ID: `$ARGUMENTS`
- Tell it which category to write (reference the section in the coverage matrix)

## Step 4: Verify

After all writers complete:
- Run `dotnet build` — the test project must compile cleanly.
- Count total case files vs matrix entries — ensure nothing was missed.
- Note: tests will FAIL at this stage because no analyzer exists yet. That is expected and correct (TDD).

## Constraints

- Review the matrix before spawning writers — this is the quality gate.
- If a writer runs out of budget, spawn another to continue the remaining cases from its category.
- Do NOT write case files yourself — delegate to the writer agents.
