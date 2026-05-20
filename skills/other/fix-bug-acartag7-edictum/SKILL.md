---
name: fix-bug
description: Fix a correctness bug in Edictum. Mandatory procedure covering root cause analysis, behavior test, fix, and full verification. Use for any bug fix touching src/edictum/.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
---

# Fix Bug Procedure

Read CLAUDE.md first. Understand the tier boundary and terminology rules before writing code.

## Step 1: Understand the bug

- Read the issue description or task assignment completely
- Read the source file containing the bug
- Read ALL existing tests for that module (`tests/test_{module}.py`)
- Identify the exact code path that fails

## Step 2: Root cause analysis

Write down (in your commit message or PR body):
1. What the code currently does
2. What it should do
3. Why the existing tests did not catch it (this identifies the test gap)

## Step 3: Write failing behavior test FIRST

Before touching source code, write a test in `tests/test_behavior/` that demonstrates the bug.

The test MUST:
- Assert the expected behavior of the public API
- Fail with the current code
- Follow the naming convention: `test_{module}_{parameter_or_feature}_{expected_behavior}`
- Live in `tests/test_behavior/test_{module}_behavior.py`

Run the test to confirm it fails:
```bash
pytest tests/test_behavior/test_{module}_behavior.py -v -k "test_name"
```

## Step 4: Fix the source code

Make the minimal change to fix the bug. Do NOT:
- Refactor surrounding code in the same commit
- Add features beyond what the fix requires
- Change unrelated files

## Step 5: Verify the fix

```bash
pytest tests/ -v --tb=short
ruff check src/ tests/
```

The behavior test from Step 3 must now pass.

## Step 6: Check regression scope

If the fix changes behavior of a public API parameter:
- Search docs for references to that parameter: search for `{parameter_name}` in `docs/`
- If docs describe the old (wrong) behavior, update them
- If the fix touches an adapter, run the adapter parity check:
  ```bash
  pytest tests/test_adapter_parity.py -v
  ```

## Step 7: Docs-code sync check

```bash
pytest tests/test_docs_sync.py -v
```

## Step 8: Full verification

```bash
pytest tests/ -v && ruff check src/ tests/ && python -m mkdocs build --strict
```

ALL must pass before committing.

## Step 9: Commit

- Conventional commit: `fix: {description}`
- No Co-Authored-By
- Include root cause analysis in commit body

## Do NOT

- Skip the behavior test — every bug fix must prove the fix works
- Fix multiple bugs in one commit — one fix per commit
- Import from `ee/` — core is self-contained
- Use banned terminology — check `.docs-style-guide.md` before writing any user-facing string
