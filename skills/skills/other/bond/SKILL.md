---
name: bond
description: Design agent team structure for a task. Use when "set up a team", "team for this", "should I use agents", "design a team", "bond a team", "how many agents", "agent team".
model: opus
---

# Role

COMPOSE. Assess whether a task benefits from parallel agents. Design roles,
boundaries, coordination. Prevent merge conflicts over maximizing
parallelism.

## Principles

1. **User owns composition** — Bond recommends team structure. The user
   approves, adjusts, or cancels before any team is created.
2. **Merge conflicts kill teams** — Any Solo in File ownership → Solo
   verdict, regardless of other dimensions. Overlapping file boundaries
   are the #1 cause of wasted agent work.
3. **Not every task needs a team** — Most tasks are better as solo or
   subagent work. Team overhead only pays off with genuine independence
   across multiple modules.
4. **Each role owns distinct files** — No overlap in file ownership
   between teammates. If overlap is unavoidable, merge the roles.
5. **Coupling check before creation** — For each pair of roles: "If role
   A changes X, does role B's work break?" If yes → merge or add explicit
   coordination checkpoint.

## Process

1. **Assess fitness** — Score 4 dimensions from task description.

   | Dimension      | Team                                        | Subagent                            | Solo                          |
   | -------------- | ------------------------------------------- | ----------------------------------- | ----------------------------- |
   | Independence   | Workers don't need each other's output      | Tasks isolated, only results matter | Sequential dependency chain   |
   | File ownership | Each role owns distinct areas               | Each task touches isolated files    | Same files need editing       |
   | Coordination   | Must share findings or challenge each other | Only report back                    | One mind holds it all         |
   | Scope          | Multi-module, 8+ story points               | Focused exploration or analysis     | Single file, 1-3 story points |

   Majority column wins. **Override:** Any Solo in File ownership → Solo.
   **Default when tied:** Subagent (cheaper, less coordination overhead).
   **Shape mode input:** When shape recommended Colleague, bias toward Team —
   persistent dialogue preserves understanding better than fire-and-forget
   subagents. Tool-Review/Tool modes don't override fitness assessment.

   Red flags — warn before proceeding:

   | Red Flag                       | Suggest Instead                            |
   | ------------------------------ | ------------------------------------------ |
   | All roles touch same files     | Single session or sequential subagents     |
   | >5 teammates                   | Reduce scope or phase the work             |
   | Tasks have serial dependencies | Single session with subagents for research |
   | Task is ≤3 story points        | Just do it in current session              |
   | >3 teammates for Collab/Guided | Reduce to 2-3 or phase sequentially       |

   If not Team → explain why, suggest subagent or solo approach, stop.

2. **Design team** — Decompose into independent workstreams.

   | Decision        | Heuristic                                                           |
   | --------------- | ------------------------------------------------------------------- |
   | Teammate count  | 1 per independent workstream (2-5, never more)                      |
   | Role names      | By responsibility ("auth-impl", "api-reviewer"), never generic      |
   | File boundaries | Each role owns distinct directories — flag any overlap              |
   | Models          | Opus: architecture, review. Sonnet: implementation. Haiku: research |
   | Permission mode | `plan`: risky changes. `default`: clear scope                       |
   | Task count      | 5-6 per teammate, each self-contained                               |

   Coupling check: for each role pair, ask "If A changes X, does B break?"
   If yes → merge roles or add coordination checkpoint.

3. **Confirm + create** — Present blueprint to user:
   `Team Blueprint: [name] | Roles: [N] | Coordination: [delegate/active-lead]`
   Per role: name, model, focus, owned files/dirs.
   User: Yes → create team and spawn agents:

   TeamCreate(team_name="[name]", description="[objective from intent]")

   Per role:
   Task(team_name="[name]", name="[role-name]",
     prompt="[SESSION marker + criteria[] + mustNot[] + ACCEPTANCE criteria]
     Role: [name]. Focus: [description]. Owned files: [dirs].

     Execute using loop mechanics:
     1. Decompose your scope into atomic work items (one sentence each,
        no 'and'). Every criteria[] maps to ≥1 item.
     2. Execute in waves — reversible before irreversible.
     3. Per wave: report Done/Carry/Stall. Carry items retry with
        [VERIFY] FAIL: [reason]. Stall items → diagnose, revise.
     4. Verify against ACCEPTANCE and STOP conditions.
     5. mustNot violations are hard stops — surface immediately.

     Retrieve facts with tools before asserting from memory.",
     subagent_type="[model from design table]",
     mode="[permission mode from design table]")

   After creation, pipeline is complete — each member executes using
   loop mechanics independently.

   Adjust → revise blueprint. Cancel → suggest solo or subagent approach.

## Boundaries

Bond recommends team structure; user owns the final composition. Bond
designs after explicit approval — Claude creates with native tools.

## Handoff

Bond returns results to the calling phase:
- Team verdict → creates team with full context. Pipeline complete.
- Solo/Subagent verdict → returns recommendation. Caller proceeds to
  loop for execution.
