---
name: review-option-interaction
description: Test combinatorial interactions between install options, launch modes, and user journeys
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Deep-research all interactions between installation options, launch modes, admin state, and user journeys. Think carefully about every path a user could take. Use maximum parallelism — spawn an agent team if desired.

## The Problem

The app has many options, features, and launch modes that interact combinatorially. Past reviews have repeatedly found edge-case bugs where one option conflicts with another or a UAC refusal leaves the system in a half-applied state. The combinatorial space is large and keeps growing.

## Step 1 — Inventory the Moving Parts

Before testing combinations, build a current inventory by reading the code. These categories have historically caused interactions, but the code is the source of truth — discover what exists now, don't assume this list is complete:

**User-facing options:**
- Install to Program Files
- Run at startup (scheduled task)
- Run as admin
- Add to Start Menu
- Check for updates
- First-launch wizard

**Features with interaction surfaces:**
- Multi-process architecture (launcher + gui + pump)
- Auto-update (rename running exe, replace, relaunch)
- Duplicate version detection (already running → compare versions → offer restart/upgrade)
- Wizard skip / duplicate version skip flags
- Various launch flags (`--gui-only`, `--config`, `--wizard-continue`, `--enable-admin-task`, etc.)
- Menu items / dashboard actions that trigger installs or config changes

**Confounding factors (things users do that the code must handle):**
- Rename the exe (e.g., "AltTabby new v4.exe") — does every path handle non-standard names?
- Rename the exe in Program Files after installation
- Have existing configs/stats/blacklists in Program Files or the local launch directory
- Refuse UAC prompts at any elevation step
- Scheduled tasks missing, renamed, or corrupted
- Multiple copies of the exe in different directories
- Running from unusual locations (network drives, paths with spaces/unicode)

## Step 2 — Test Combinatorial Paths

For each pair/group of options, trace the user journey through the code. Use `query_callchain.ps1` to follow how config option reads flow through functions across files. Use `query_ipc.ps1` to check cross-process message flows that can trigger option interactions. Use `query_function_visibility.ps1 <funcName>` to find all callers of elevation/UAC functions. Use `query_global_ownership.ps1 <globalName>` to trace install state ownership across files:

- How does feature X behave when run as admin vs not admin?
- What happens if UAC is refused at each elevation prompt?
- What if the user has option A enabled but then changes option B?
- What if the exe is already running when an install/update/config change happens?
- What state is left behind if a multi-step operation fails halfway?

**Focus on state transitions that span multiple steps** — wizard → install → create task → relaunch. If any step fails, is the state recoverable? Does the next launch detect the partial state correctly?

## By-Design Choices (Do NOT Flag)

These are intentional — do not propose changing them:
- Install path is hardcoded to Program Files
- Exe name is hardcoded when installed to Program Files

Issues **around** or **caused by** these choices (e.g., "what if the user renames the installed exe and then auto-update tries to find it") are real findings. The design choices themselves are not.

## Step 3 — DRY Consolidation

Multiple bugs in these flows have come from duplicated logic across files. After identifying bugs, also look for:
- Same path-resolution logic implemented differently in multiple places
- Same "is admin?" / "is installed?" / "is running?" check duplicated with slight variations
- Elevation patterns that could share a common helper

DRY findings are secondary to bug findings but help prevent future regressions.

## Validation

After explore agents report back, **validate every finding yourself**. These flows have a lot of defensive code that may look like bugs but is handling edge cases intentionally.

For each candidate:

1. **Cite evidence**: "I verified by reading `file.ahk` lines X–Y" with actual code quoted. Trace the full path through multiple files if the journey spans them.
2. **Trace the user journey**: Describe the exact sequence of user actions that triggers the bug (e.g., "User installs to PF → renames exe → launches renamed exe → auto-update runs → ...").
3. **Counter-argument**: "What existing code handles this?" — Is there a fallback path that catches this case? Does the code already detect and recover from this state?
4. **Observed vs inferred**: Did you trace the code path through all branches, or infer the bug from one function without checking its callers?

## Plan Format

**Section 1 — Interaction bugs** (specific failure paths):

| Journey | Steps | Failure Point | File:Lines | Impact | Fix |
|---------|-------|--------------|-----------|--------|-----|
| Install → rename exe → update check | 1. Install to PF 2. User renames exe 3. Auto-update downloads | Update writes to hardcoded name, old renamed exe orphaned | `update.ahk:142` | Stale exe left behind | Check actual exe name, not hardcoded |

**Section 2 — UAC refusal gaps** (what happens when elevation is denied):

| Operation | UAC Point | Behavior if Refused | Clean? | Fix if Needed |
|-----------|----------|-------------------|--------|--------------|
| Enable admin mode | Task creation | Falls back to non-admin | Yes | None |
| Install to PF | File copy | ??? | ??? | ??? |

**Section 3 — DRY consolidation opportunities**:

| Pattern | Files | Variations | Proposed Consolidation |
|---------|-------|-----------|----------------------|
| "Is installed to PF?" check | `launcher_main.ahk:30`, `update.ahk:55`, `wizard.ahk:80` | Slightly different path comparisons | Shared `IsInstalledToProgramFiles()` helper |

Order by severity: data-loss risks first, cosmetic inconsistencies last.

Ignore any existing plans — create a fresh one.
