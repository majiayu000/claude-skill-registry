---
name: roster
description: Use when a goal or plan is about to fan out to concurrent agents but names no lanes — no answer to who runs what, in what order, verified how — or when orchestration is requested while the intent itself is still vague. Triggers on "plan this into lanes", "set up the board", "orchestrate this", handing a plan over for dispatch.
---

The stage before dispatch: elicit until the intent is solid, then project it onto the board as a flow roster — lanes, edges, acceptance — complete enough that a dispatcher re-derives nothing.

## 1. Intent check (skip when handed a solid plan)

Solid = you can state the goal, constraints, verification, non-goals, and risky surfaces from what the human gave you, without inventing any of them. Anything you'd have to invent, elicit:

- Interview one question at a time; stop when answers stop changing the roster.
- Ask for what only the human holds: risk tolerance, deadlines, what must not change, how they'll judge done.
- A hole in intent becomes an open question on the board, never an assumption.

## 2. Cut the roster

- **Lanes** — disjoint scopes. A scope that overlaps everything (sync, codegen, formatting) is a lane behind a blocking edge, never a concurrent one.
- **Edges** — blocked-by dependencies, explicit per lane, never implied in prose.
- **Acceptance per lane** — one check the lane's handoff can be verified against.
- **The serial rest** — what stays with the lead or the human: integration, anything whose next step depends directly on a result, edits too small to brief.

Concurrency cap, waves, and spawn mechanics belong to the dispatch stage — never in the roster.

## 3. Project onto the board

With solo MCP: the plan goes to a scratchpad with scannable headings — Goal, Current understanding, Lanes and flow, Verification, Risky files, Decisions, Open questions — and each lane becomes a todo carrying its objective, owned scope, a pointer to its scratchpad section (never a copy), its acceptance check, blockers, and tags. Without solo: a plan file plus the task tracker, same shape.

A cold agent must be able to run the roster from the board alone.

## 4. Gate

Present to the human: the lanes, the edges, what stays serial, and every open question. The human locks the roster; an answer arriving at the gate goes onto the board first. No dispatch here.
