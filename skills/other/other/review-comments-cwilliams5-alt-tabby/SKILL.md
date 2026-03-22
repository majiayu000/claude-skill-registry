---
name: review-comments
description: Audit comments for staleness — stale identifier references, outdated behavioral claims, and unverifiable flags
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Three-phase comment audit with decreasing confidence at each tier. Use maximum parallelism — spawn explore agents for independent file groups.

## The Asymmetry

Stale comments are worse than no comments — they actively mislead. But removing a good comment is worse than keeping a stale one. The hard-won "Windows reuses HWNDs for temporary windows" comment took a painful debugging session to earn and costs nothing to keep. **When in doubt, flag for human review. Never recommend removing a comment you can't prove is wrong.**

## Phase 1 — Identifier Cross-Reference (Mechanical, High Confidence)

Grep all `.ahk` files in `src/` for comments (lines containing `;` after code, or `;`-prefixed comment lines). Extract any identifiers mentioned in comments and cross-reference against the current codebase.

### What to cross-reference

- **Function names** — comment says "calls _FooBar()" or "see _FooBar" — does `_FooBar` still exist? Use `query_function_visibility.ps1` to check. Use `query_impact.ps1` to validate comment references to affected functions.
- **Global variable names** — comment references `gSomeGlobal` — does it still exist? Use `query_global_ownership.ps1` to check.
- **File names** — comment says "see gui_store.ahk" or "defined in old_file.ahk" — does that file still exist? Use glob to check.
- **Config keys** — comment references a config key name — does it still exist in the registry? Use `query_config.ps1` to check.
- **IPC message types** — comment references `IPC_MSG_SOMETHING` — does that message type still exist? Use `query_ipc.ps1` to check.
- **TODO/FIXME/HACK markers** — extract the description and check if the referenced issue still applies. Some may reference GitHub issues by number — check if those issues are closed.

### Classification

- **Provably stale**: The identifier doesn't exist in the codebase. The comment is referencing something that was renamed or deleted.
- **Possibly stale**: The identifier exists but was renamed/moved — comment references old name alongside or near the new one (suggests it survived a refactor without update).
- **Current**: The identifier exists and the reference makes sense in context.

Only provably stale findings are high-confidence. Report the others but flag the confidence level.

## Phase 2 — Behavioral Claim Verification (LLM-Assisted, Medium Confidence)

For comments that make behavioral claims about the surrounding code, read the code and check whether the described behavior still matches.

### What to check

The skill **can** verify:
- "This loop processes items in reverse order" — does it? Read the loop.
- "We skip cloaked windows here" — is there a cloaked check? Read the function.
- "This returns early if no windows are eligible" — is there an early return with that condition?
- "This timer fires every 500ms" — what's the actual SetTimer interval?
- "The store is cleared before repopulating" — does the code still clear-then-repopulate?

The skill **cannot** verify:
- "...because Windows does X" — domain claim about OS behavior
- "...because GDI+ leaks if you don't" — domain claim about library behavior
- "...this was tried and reverted" — historical claim (would need git history)
- "...for performance" — would need benchmarking to verify the claim still matters

### Classification

- **Code contradicts comment**: The comment describes behavior X, but the code clearly does Y. The comment is stale. **Quote both the comment and the contradicting code.**
- **Code matches comment**: The described behavior is still present. Comment is current (regardless of whether the *reason* is still valid).
- **Can't verify from code alone**: The comment makes a claim the skill can't check by reading code. Pass to Phase 3.

## Phase 3 — Unverifiable Flags (Human Review)

Comments that survived Phase 1 and Phase 2 without being classified as stale or current. These make claims that require domain knowledge, historical context, or testing to verify.

### Do NOT recommend removing these

Instead, present them for human review with context:

- The comment text
- The surrounding code (enough to evaluate relevance)
- Why the skill can't verify (domain claim? historical reference? external dependency?)
- Any supporting evidence either way (e.g., "the comment mentions WM_COPYDATA but this file now uses named pipes — the mechanism changed but the comment's *principle* may still apply")

### Priority within Phase 3

Higher priority (more likely stale):
- Comments in heavily-refactored sections (many recent git changes around the comment)
- Comments referencing architecture that has changed (old IPC model, old process model)
- Comments with specific numbers that may have drifted ("buffer size is 4096" — is it still?)

Lower priority (more likely still valid):
- Comments about Windows OS behavior or Win32 API quirks
- Comments about AHK v2 language behavior
- Comments flagged with "CRITICAL" or "DO NOT" — these were written with emphasis for a reason

## Scope

All `.ahk` files in `src/` (excluding `src/lib/` — third-party code). Focus effort proportionally:
- `src/core/` and `src/gui/` — highest churn, most likely to have stale comments
- `src/shared/` — moderate churn
- `src/editors/`, `src/pump/` — lower churn but still worth scanning

## Explore Strategy

Split by directory (run in parallel):

- **Core producers** — all files in `src/core/`
- **GUI files** — all files in `src/gui/`
- **Shared infrastructure** — all files in `src/shared/`
- **Other** — `src/editors/`, `src/pump/`, `src/alt_tabby.ahk`

Each agent performs Phase 1 (identifier cross-reference) for its file group. Phase 2 (behavioral claims) can run in the same pass — read the comment, read the surrounding code, classify.

## Validation

After explore agents report back, **validate every finding yourself**.

For each candidate:

1. **Cite evidence**: Quote the comment AND the code it describes. For Phase 1 stale findings, show the grep proving the identifier doesn't exist. For Phase 2 contradictions, quote both the comment's claim and the contradicting code.
2. **Check for renames**: Before calling an identifier "missing," check if it was renamed. `_OldFunc` might now be `_NewFunc` doing the same thing — the comment needs updating, not removal.
3. **Check the whole function**: A comment at line 50 might reference behavior at line 80 of the same function. Don't flag it as stale just because line 51 doesn't match.
4. **Counter-argument**: "What would make removing/updating this comment a mistake?" — Does the comment capture knowledge that would be lost? Is the "stale" part actually still relevant in a way you're not seeing?

## Plan Format

**Section 1 — Provably stale (Phase 1, high confidence):**

| File:Line | Comment | Referenced Identifier | Status | Action |
|-----------|---------|----------------------|--------|--------|
| `gui_data.ahk:42` | `; see gui_store.ahk for delta logic` | `gui_store.ahk` | File deleted in refactor | Remove or update to current file |
| `komorebi_sub.ahk:88` | `; calls _KS_OldProcess()` | `_KS_OldProcess` | Function renamed to `_KS_ProcessState` | Update reference |

**Section 2 — Code contradicts comment (Phase 2, medium confidence):**

| File:Line | Comment | What Code Actually Does | Action |
|-----------|---------|------------------------|--------|
| `winevent_hook.ahk:55` | `; process in reverse for MRU order` | Loop processes forward (`for i, item in arr`) | Update comment to match current behavior |

**Section 3 — Flagged for human review (Phase 3):**

| File:Line | Comment | Why Unverifiable | Supporting Evidence |
|-----------|---------|-----------------|-------------------|
| `gui_state.ahk:120` | `; Windows sends spurious focus events during workspace switch` | OS behavior claim — can't verify from code | MRU suppression logic around this comment suggests the claim is still acted upon |

Order Section 1 and 2 by file (group related stale comments together for efficient batch fixes). Order Section 3 by priority (most likely stale first).

Ignore any existing plans — create a fresh one.
