---
name: no-comments
description: 'Use when asked to audit comments in code files and propose structural replacements or deletions with per-candidate approval. Enumerates comments in C, JavaScript, TypeScript, HTML, CSS, and shell-style syntax, classifies each as earned or unearned, drafts structural alternatives, and returns a complete accounting ledger. Not for deterministic commented-out-code removal; use deslop.'
---

# No comments

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Audit comments in code files and propose structural replacements or deletions with per-candidate approval. |
| Authority | Read target files and write the audit ledger. Does not modify source files without per-candidate user approval. Approved edits are reversible local writes; revert each edited file to its captured pre-edit state on failure. |
| Side effect | Writes an audit ledger. Applies accepted edits only after the user chooses an action for each candidate. |
| Done | A complete audit ledger with one decision per comment and no unprocessed candidates. |

## Inputs

Required:
- Target file paths: one or more file paths or glob patterns identifying files to audit.
- Comment-syntax catalog: the comment syntax families present in the target files. Supported syntaxes are `//`, `/* */`, `///`, `/** */` (C, JavaScript, TypeScript, Rust, Go, Java, Kotlin, Swift, C#), `<!-- -->` (HTML, XML, Markdown), `#` (Python, Ruby, shell, YAML, TOML), `--` (SQL, Lua, Haskell), `{- -}` (Haskell). Files using unsupported syntax are reported and excluded.

Optional:
- Veto list: specific comment lines, line ranges, or patterns to preserve regardless of category. If no veto list is supplied, every comment is subject to the audit criteria.

## Procedure

1. Receive and validate target file paths. Reject paths that escape the working directory or are not readable. Detect the comment syntax family for each file from its extension or content. Report and exclude files whose syntax is not in the supported catalog. Done when: all valid paths are accepted with their syntax family, and invalid or unsupported-syntax paths are rejected with a reason.
2. Scan each target file for comments in its detected syntax family. Record line number, text content, and syntax form. Done when: every comment in every target file is recorded with line number, text, and form.
3. Classify each comment into one of these categories:

   a. **Legal or business rule**: names a legal or business rule, cites a regulation or license term. Retained.
   b. **API contract**: documents a public API contract, parameter, return value, or thrown exception. Retained.
   c. **Design decision**: preserves a non-obvious design decision or cites a specification. Retained.
   d. **Dead code**: commented-out code or broken examples. Deletion candidate.
   e. **Redundant**: restates what the code already expresses without ambiguity. Deletion candidate.
   f. **TODO marker**: `TODO`, `FIXME`, `HACK`, `XXX`, or equivalent. Deletion candidate unless tied to an open issue in the same repository.
   g. **Vague**: contains indefinite words (`soon`, `later`, `maybe`, `should`, `improve`, `optimize`) without a concrete action or specification. Deletion candidate.
   h. **Noise**: empty comment, repeated punctuation, or whitespace. Deletion candidate.

   Done when: every comment has a category assignment.
4. For each deletion candidate that would leave the code less readable, draft one structural alternative: rename a variable or function to make the comment redundant, extract a named function or constant to make the intent explicit, add an assertion or test that enforces the same constraint, or introduce a well-named guard clause. Each deletion candidate has either a structural alternative or a delete-only plan. Done when: every deletion candidate has a proposed action.
5. Present the candidates to the user and require a choice for each one: delete the comment, accept the structural alternative, or retain the comment unchanged. Done when: the user has chosen an action for every deletion candidate.
6. Write the audit ledger: one row per comment with file, line, text, category, proposed action, and user decision. Done when: the ledger is written with one decision per comment and no unprocessed candidates.
7. Apply each accepted edit. Before applying an edit to a file, capture its current content in memory. If the edit fails or the result is syntactically invalid, revert that file to the captured content and record the failure in the ledger. Continue to the next file. Done when: all accepted edits are applied and verified, or failed edits are reverted and recorded.

## Failure and recovery

| Failure class | Condition | Result |
|---|---|---|
| `invalid-path` | A target path is outside the working directory or unreadable | Stop before scanning. Report the path. |
| `unsupported-syntax` | A file uses a comment syntax not in the supported catalog | Report the file and exclude it. Continue with the remaining files. |
| `edit-failure` | An edit write or syntax check fails on a file | Revert that file to its captured pre-edit content. Record the failure in the ledger. Continue to the next file. |
| `rollback-failure` | A revert cannot restore a file to its pre-edit state | Stop. Report the file and the inability to recover. Do not continue to other files. |
| `no-targets` | No valid target file paths were supplied | Stop. Report the missing input. |
| `ledger-write-failure` | The audit ledger cannot be written | Report the failure. The audit is complete but undelivered; the user has the chat output as a fallback. |

Partial-result rule: if edits succeed on some files before a failure, the ledger records the edited set and the failed set separately. Files that were not yet processed are listed as remaining work.

## Output

One audit ledger: file, line, text, category, proposed action, and user decision per comment, plus status and remaining work. Accepted edits are applied to source files; failed edits are reverted and recorded.
