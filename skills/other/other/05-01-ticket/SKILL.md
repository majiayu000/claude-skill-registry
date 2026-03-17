---
name: 05-01-ticket
description: "Working with tk / ticket — lifecycle, dependencies, agent coordination, session protocol"
---

## Task tracking

You MUST track work and tasks. This project uses a CLI ticket system for task management.
Oneshot is `ID=$(tk create "Move magic values to config" -t task -p 1 --tags config,refactor -d "Relocate constants into config module.") && tk start $ID && printf '\n## Goal\nRelocate constants into config module.\n\n## Acceptance Criteria\n- [ ] All magic values moved\n- [ ] Usages wired\n\n## Verification\n- [ ] Tests pass\n\n## Worktree\n- .\n' >> .tickets/$ID.md`. Run `tk help` when you need details.
The ONLY exception is the small-change exemption (all must be true): one file, 10 lines or fewer (excluding whitespace-only), and docs-only or comment/typo-only changes. Otherwise, create a ticket.

### Agent Coordination (CRITICAL)

Before creating a ticket, search for related work: `tk ls --status=open` and check memory for prior context.

- **Found related ticket?** → `tk dep <new> <existing>` (blocks on it) or `tk link <new> <existing>` (related, not blocking)
- **Discovered a bug/issue mid-task?** → Create ticket, dep/link it to current ticket, `tk add-note <current> "found <issue>, see <new-id>"`
- **State changed?** (blocker found, approach shifted, partial progress) → `tk add-note <id> "<what changed>"`
- **Pick work from** `tk ready`, **never from** `tk blocked`

### Ticket Lifecycle (CRITICAL)

Every ticket you start MUST be closed when its work is done. The lifecycle is:

`tk create` → `tk start` → (do work) → `tk close` → `git commit`

- Before you commit you ALWAYS update / close your ticket
- **Worker/team agents:** You MUST `tk close <id>` your assigned ticket before reporting completion.
- **If work is incomplete:** Use `tk reopen <id>` to set it back to `open`, not left as `in_progress`.

### Acceptance Criteria Completeness (CRITICAL)

Acceptance criteria MUST account for ALL work in the ticket. Closing a ticket means "nothing is left to track" — if AC only covers partial work, closing the ticket **destroys visibility into remaining work**.

**The rule:** When a ticket is closed, zero work items should be orphaned. Either:

1. All work is done (AC covers everything), OR
2. AC explicitly includes creating follow-up tickets for remaining work

```
WRONG (epic with P0-P3 work):
  AC: "P0 items implemented" → close → P1-P3 work is now untracked, lost forever

RIGHT:
  AC: "All P0-P3 items implemented" (full completion)

RIGHT (if splitting):
  AC: "P0 items implemented" + "Follow-up ticket created for P1-P3 with full item list"
```

**Never let closing a ticket silently drop work items.** A closed ticket with uncovered work is worse than no ticket — it gives the illusion that everything is handled.

```
RIGHT: tk close t-1234 && git commit -m "feat(x): implement feature (t-1234)"
WRONG: git commit (ticket still in_progress, forgotten forever)
```

```
USER: Change that line for me.
WRONG: The editing task is likely a single-file change but since work tracking is required except for single command edits, it's safer to create and track a ticket for this.
RIGHT:**MAKES EDIT**
```

```
USER: Can you fix this quickly in local main?
WRONG: **MAKES EDIT**
RIGHT: **CREATES TICKET FIRST**
```

#### Ready-Work-First Workflow

Before starting new work, check what's unblocked:

```bash
tk ready                    # Tasks with all dependencies resolved
tk ready -a "agent-name"    # Filtered to your assigned work
tk blocked                  # Tasks waiting on unfinished deps — DO NOT pick these
```

`tk ready` is the **work queue**. It shows only tickets whose dependencies are all closed. If a ticket appears in `tk blocked`, someone else needs to finish its prerequisites first. Agents pick from `ready`, never from `blocked`.

#### Dependencies vs Links

tk has two relationship types. Use the right one:

| Command                   | Meaning                    | Effect on `tk ready`                          |
| ------------------------- | -------------------------- | --------------------------------------------- |
| `tk dep <child> <parent>` | Child **blocks on** parent | Child hidden from `ready` until parent closes |
| `tk link <a> <b>`         | Symmetric "see also"       | No effect — purely informational              |

**Use `dep` when:** Work cannot start until another ticket completes. A frontend feature needs a backend endpoint. Tests can't run until the harness exists.

**Use `link` when:** Tickets are related but independent. Two tickets touch the same module. A bug report relates to a feature ticket but doesn't block it.

```bash
# "optimize-physics" cannot start until "test-harness" is done
tk dep t-opt t-harness

# These two tickets touch the same subsystem but are independent work
tk link t-abc t-def
```

#### Discovered-From Pattern

When working on ticket X and you discover new work Y, **create Y and wire the dependency**:

```bash
# While working on t-abc, you find a bug that needs fixing first
NEW=$(tk create "Fix race condition in sync loop" -t bug -p 1 --tags sync,discovered -d "Found while working on t-abc: sync loop has TOCTOU race.")
tk dep t-abc $NEW          # t-abc now blocked on the new bug
tk add-note t-abc "Blocked: discovered race condition, see $NEW"
```

This preserves the discovery chain. `tk dep tree t-abc` will show _why_ t-abc is blocked and what spawned the blocker. Without this, discovered work gets lost or duplicated by the next agent.

#### Notes as Inter-Agent Communication

`tk add-note` is the message channel between agents and sessions. Leave notes when:

- **Handing off work:** What you tried, what's left, what's tricky
- **Discovering blockers:** Why you stopped, what needs to happen first
- **Recording decisions:** Why you chose approach A over B
- **Flagging surprises:** Unexpected behavior that future agents should know about

```bash
# Handoff note — next agent knows exactly where to pick up
tk add-note t-abc "Implemented the reducer. Tests pass locally but edge case still fails. Suspect timing — the client subscribes after the update runs. Next step: add re-subscribe on completion."

# Decision note — prevents the next agent from re-litigating
tk add-note t-def "Chose persistent objects over create/destroy on proximity. Reason: creation allocates and the rebuild is O(n). Sleeping objects are nearly free."
```

#### Dependency Tree Visualization

Before starting complex work, understand the full dependency graph:

```bash
tk dep tree t-1444          # See the full tree with status of each node
tk dep tree --full t-1444   # Disable deduplication — shows every path
tk dep cycle                # Find circular dependencies (must be zero)
```

If `tk dep cycle` returns anything, **fix it immediately** — circular deps mean `tk ready` can never surface those tickets.

#### Session Completion Protocol (Landing the Plane)

When ending a work session, complete ALL of these steps:

1. **Close finished tickets** — `tk close <id>` for every ticket you completed
2. **Reopen incomplete tickets** — `tk reopen <id>` (not left as `in_progress`)
3. **File follow-up tickets** for any discovered work, wire deps
4. **Leave handoff notes** — `tk add-note` on any ticket the next agent will touch
5. **Commit** — Only after all ticket states are correct
6. **Push** — Unpushed work is invisible to other agents

```bash
# Landing example
tk close t-abc                                         # Done
tk reopen t-def                                        # Not done, back to open
NEW=$(tk create "Handle edge case X" -t task -p 2 --tags follow-up -d "Found during t-abc")
tk dep t-def $NEW                                      # Wire dependency
tk add-note t-def "Paused: needs $NEW resolved first. Auth token refresh works but edge case X causes silent failure on expired tokens."
git commit -m "feat(sync): implement reducer (t-abc)"
git push
```

**The plane is NOT landed until `git push` succeeds.** Unpushed ticket state causes other agents to duplicate work, pick up blocked tickets, or miss context entirely.

#### Quick Reference

| What you want                | Command                      |
| ---------------------------- | ---------------------------- |
| What can I work on?          | `tk ready`                   |
| What's stuck?                | `tk blocked`                 |
| Who depends on what?         | `tk dep tree <id>`           |
| Any circular deps?           | `tk dep cycle`               |
| This blocks that             | `tk dep <blocked> <blocker>` |
| These are related            | `tk link <a> <b>`            |
| Leave context for next agent | `tk add-note <id> "..."`     |
| See ticket detail + notes    | `tk show <id>`               |
| All tickets as JSON          | `tk query`                   |

### Agent Coordination (CRITICAL)

Before creating a ticket, search for related work: `totalrecall tk recall "<topic>" | head -n 40`

- **Found related ticket?** → `tk dep <new> <existing>` (blocks on it) or `tk link <new> <existing>` (related, not blocking)
- **Discovered a bug/issue mid-task?** → Create ticket, dep/link it to current ticket, `tk add-note <current> "found <issue>, see <new-id>"`
- **State changed?** (blocker found, approach shifted, partial progress) → `tk add-note <id> "<what changed>"`
- **Pick work from** `tk ready`, **never from** `tk blocked`