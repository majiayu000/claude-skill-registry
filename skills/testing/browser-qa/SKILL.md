---
name: browser-qa
description: 'Use when the user runs /browser-qa to run the QA verification pass and return report-only results without entering a fix loop. Runs configured build, test, and lint checks in order, collects findings, and writes one local report. Not for remote, credential, publish, deploy, or irreversible changes.'
---

# Browser qa

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The user runs /browser-qa to run a QA verification pass and get report-only results. |
| Authority | Write one local QA report under the working tree. No source, VCS, credential, paid, published, deployed, or remote mutation. Reversible by deleting the report. |
| Side effect | A QA report only. No fix loop, no file edits, no further checks after the report is returned. |
| Done | Report-only verification results are returned: per-check status and findings in one local report file. |

## Inputs

- The working tree or change set to verify. Supply a scope (paths or diff range) to narrow the pass; without one, verify the whole tree.
- Optional: an ordered list of check commands to run. If omitted, run the project's configured QA checks in order: build, then tests, then lint.

## Procedure

1. Bound scope to the supplied paths or diff range, or the whole tree when none is given. Do not read or change files outside that scope. Done when: the scope boundary is established and enforced.
2. Run each configured QA check in order (build, then tests, then lint) and capture exit status, stdout, and stderr for each. Done when: every check has been run or recorded as non-runnable.
3. Collect every finding into a single list tagged by check name and severity. Done when: all findings are collected with their check and severity tags.
4. Write the findings to one local QA report file under the repository working tree. Done when: the report file exists with all findings.
5. Return the report contents as the result. Done when: the report contents are returned.
6. After step 5, do not apply fixes, edit files, or run more checks. This report-only variant intentionally skips the fix loop. Done when: no fixes are applied and no further checks run.

## Failure and recovery

- Check command missing or non-runnable: record the command name and error in the report; continue the remaining checks. Do not substitute a different command.
- A check returns non-zero: that is a finding, not a skill failure. Record it and proceed to the next check.
- Report file unwritable: return the findings inline and state that the write failed; do not create a partial file.
- Rollback: delete the report file. No source, VCS, or remote state is mutated, so no further recovery is required.
- Blocked: return a report listing which checks ran, which could not, and the findings collected. Never claim the done predicate when a requested check never ran.

## Output

One local QA report file containing per-check status and findings, plus the same findings returned as the result. No fixes are applied.
