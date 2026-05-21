# Gastown Origin: Sling Dispatch

## Where This Comes From

The sling-dispatch skill is a direct adaptation of Gastown's sling system, implemented across several Go source files in the original codebase. The `gt sling` command is the primary dispatch mechanism -- it takes a bead ID, finds an available polecat, sets up a worktree, injects the role context via `gt prime --hook`, and launches the agent into autonomous GUPP execution.

## Chipset Mapping: Instruction Dispatch Unit

In the chipset hardware metaphor, the sling maps to the **instruction fetch-decode-dispatch unit** of a CPU. A real processor's dispatch unit reads instructions from the instruction queue, decodes them, allocates execution resources (ALU, registers, execution ports), and dispatches the decoded instruction to the appropriate execution unit. Similarly, the sling fetches beads from state, decodes them into work items, allocates polecats from the agent pool, and dispatches the work to the allocated polecat.

| Hardware Component | Sling Function |
|-------------------|------------------|
| Instruction fetch | Resolve bead ID to work item (Stage 1) |
| Instruction decode | Parse work item details and requirements (Stage 1) |
| Register allocation | Select or spawn available polecat (Stage 2) |
| Execution port binding | Create isolated workspace and set hook (Stages 3-4) |
| Reservation station | Write dispatch args to durable state (Stage 5) |
| Issue to execution unit | Launch polecat session with GUPP context (Stage 6) |
| Reorder buffer entry | Record dispatch in convoy tracking (Stage 7) |

## Key Gastown Source Files

| File | What It Provides |
|------|-----------------|
| `internal/cmd/sling.go` | Core dispatch pipeline -- bead resolution, polecat allocation, hook injection |
| `internal/cmd/sling_batch.go` | Batch dispatch logic -- convoy creation for multi-bead dispatch to same rig |
| `internal/cmd/sling_formula.go` | Formula expansion -- TOML template to ordered bead sequence |
| `internal/cmd/sling_helpers.go` | Utility functions -- worktree creation, context assembly, dispatch record writing |
| `internal/polecat/manager.go` | Polecat pool management -- naming, allocation, lifecycle tracking |

## The 7-Stage Pipeline

Gastown's sling pipeline maps cleanly from Go to TypeScript:

1. **Fetch** (`sling.go:fetchBead`): Resolves bead ID against the rig's state file. In Go, this reads a JSON bead file from the `.gt/state/beads/` directory. In the skill, this becomes a `StateManager.getWorkItem()` call.

2. **Allocate** (`manager.go:Allocate`): The polecat manager maintains a pool of named polecats. It prefers recycling idle polecats over spawning new ones. The pool has a configurable maximum size. In Go, this creates a tmux session and git worktree. In the skill, it creates an agent identity record.

3. **Prepare** (`sling_helpers.go:prepareWorkspace`): Creates the git worktree from the rig's shared `.repo.git` bare repository. The worktree gets its own branch (`polecat/{beadId}`). In the skill, workspace preparation is abstracted to context assembly.

4. **Hook** (`sling.go:hookBead`): Runs `gt prime --hook` to inject the polecat role template with the specific bead context. This sets the work item status to `hooked` and writes the hook state file. In the skill, this becomes `state.setHook()` + `state.updateWorkItem()`.

5. **Store** (`sling_helpers.go:storeDispatch`): Writes the dispatch arguments to a durable state file that survives crashes. This is the crash recovery checkpoint -- if the process dies after this point, the dispatch can be resumed.

6. **Launch** (`sling.go:launchPolecat`): Attaches to the tmux session and sends the GUPP activation command. The polecat's session receives the role template and begins autonomous execution. In the skill, this becomes agent status update + mail notification.

7. **Confirm** (`sling.go:confirmDispatch`): Writes the dispatch record to the convoy's tracking state. This closes the dispatch pipeline and makes the assignment visible to the mayor and witness.

## Batch Mode Origin

Gastown's `sling_batch.go` implements convoy-based batch dispatch. When the mayor has multiple beads for the same rig, the sling groups them into a convoy and dispatches in parallel (up to the `max_parallel` limit from the rig configuration). The convoy tracks aggregate progress -- the mayor can query "how many beads in convoy X are done?" rather than checking individual beads.

The batch threshold (default 3) is set in the Gastown rig configuration. In the chipset YAML, this maps to `dispatch.batch_threshold`.

## Formula Mode Origin

Gastown's `sling_formula.go` implements template-driven dispatch. A formula is a TOML file that declares a multi-step workflow:

```toml
[formula]
name = "release"

[[steps]]
name = "bump-version"
description = "Update version number in package.json"

[[steps]]
name = "run-tests"
description = "Execute full test suite"
depends_on = ["bump-version"]

[[steps]]
name = "build"
description = "Build release artifacts"
depends_on = ["run-tests"]

[[steps]]
name = "tag"
description = "Create git tag for release"
depends_on = ["build"]
```

The sling expands this into four ordered beads, respects the dependency chain, and dispatches them sequentially (or in parallel where dependencies allow).

## Idempotency Design

From Gastown's design: the sling is explicitly idempotent. The `hookBead` function checks the bead's current status before proceeding. If the bead is already `hooked`, the sling returns immediately without side effects. This design choice comes from the crash recovery requirement -- if the sling crashes after hooking but before confirming, a retry must not create a duplicate dispatch.

## What Changed From Gastown

1. **Language:** Go sling commands to TypeScript StateManager operations
2. **Workspace:** Physical git worktree creation replaced with context assembly
3. **Session:** tmux session creation replaced with mail-based notification
4. **Pool management:** In-memory Go polecat pool replaced with filesystem-based agent records
5. **Formula format:** TOML templates preserved as the formula definition format
6. **Batch threshold:** Configurable via chipset YAML (`dispatch.batch_threshold`) instead of rig-level Go config
7. **Crash recovery:** Explicit dispatch record files instead of Go's in-process state recovery
