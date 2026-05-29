---
name: subagent-prompt
description: Produce a comprehensive prompt that hands off the current session's work to a fresh session for sub-agent-orchestrated execution. Use when the user wants to execute discussed/planned work in a new session, run a job to completion via sub-agents, or generate a portable handoff prompt with per-task verification. Triggers on "/subagent-prompt", "give me a prompt to run this in a new session", "hand this off to sub-agents", "execute this with sub-agents".
disable-model-invocation: true
user-invocable: true
---

# Sub-Agent Orchestration Prompt

Produce a single, self-contained prompt that the user can paste into a new Claude Code session to execute the work discussed in this conversation. The new session is the **orchestrator**: it dispatches a sub-agent per task and only synthesizes results — it does not implement code itself.

## Goal

Hand off the current session's work to a fresh context window in a form that:

- Runs to completion without needing the user to babysit each step
- Uses one sub-agent per task so each task has its own context window
- Forces each sub-agent to **verify** its own work before reporting back
- Leaves the orchestrator with enough material to confirm the whole job is functional at the end

## Gates

Complete in order. Do not advance until the **Pass when** condition holds.

1. **Source material identified** — **Pass when:** You can point to the concrete artifacts this prompt will hand off (a plan file, a checklist, a list of changes the user described, etc.). If the conversation has only vague intent, ask the user what the prompt should cover before drafting.
2. **Task decomposition explicit** — **Pass when:** You have a numbered list of tasks (or you can point to one already on disk) where each task is small enough for one sub-agent to own end-to-end. If the work is monolithic, decompose it before drafting the prompt.
3. **Verification per task specified** — **Pass when:** For every task, you have named the concrete check a sub-agent must run before reporting success (typecheck command, test command, lint, file inspection, etc.). "Verify it works" is not a pass.
4. **Prompt drafted and self-contained** — **Pass when:** The drafted prompt would make sense to a Claude session with zero memory of this conversation: it names paths, names tools, names verification commands, and names the success condition.

## What the Generated Prompt Must Contain

Draft the handoff prompt as a single fenced block the user can copy. It must include, in this order:

1. **Role line** — "You are the orchestrator. Dispatch one sub-agent per task. Do not implement code yourself."
2. **Context** — what the work is, where the source material lives (plan path, spec path, repo paths), and any non-obvious constraints. Reference files by absolute path so the new session can read them without guesswork.
3. **Task list** — each task numbered, with: title, input artifacts (paths/sections), sub-agent type to use, and the specific verification step that sub-agent must run and pass before reporting.
4. **Verification contract** — explicit instruction that each sub-agent reports back only after its verification passed, and reports back with: what it changed, the verification command run, and the verification output (last few lines or full output if short).
5. **Run-to-completion clause** — "Continue dispatching tasks until every task is complete. If a sub-agent reports verification failure, dispatch a follow-up sub-agent to diagnose and fix before moving on. Do not stop until the final integration check passes."
6. **Final integration check** — the single command (or short sequence) the orchestrator runs after all tasks complete to confirm the whole job is functional (project typecheck, full test suite, lint, smoke run). Name it concretely.
7. **Failure-handling policy** — what to do if a sub-agent gets stuck twice on the same step (escalate to the user, do not silently downscope).

## Drafting Discipline

- **Absolute paths only.** A new session can't resolve relative paths against this session's working directory.
- **Concrete commands only.** "Run the tests" is not a command. `cargo test --package osprey-core` is.
- **Name the sub-agent type.** If the project uses `general-purpose`, say so. If a specialized agent fits (`Explore` for a search-only task), name it. Don't leave the orchestrator guessing.
- **No "use your judgment" escape hatches.** If a task needs judgment, pre-specify the criteria. If you can't, the task isn't ready to hand off and you should say so to the user before drafting.
- **One source of truth.** If a plan file exists on disk, the prompt points the orchestrator at the plan file rather than restating the plan. Restating drifts; the file is authoritative.

## Workflow

1. Identify the source material (gate 1). If a `.beagle/concepts/<slug>/plan.md` or equivalent exists, that is the spine; if not, ask the user what to base the prompt on.
2. Confirm task decomposition (gate 2). If the source already enumerates tasks, reuse that numbering. Otherwise propose one and confirm with the user before drafting.
3. For each task, define the verification check (gate 3). Match it to the project's actual tooling — read `CLAUDE.md` and any `Makefile`/`package.json`/`Cargo.toml` to find the right command.
4. Draft the prompt as a single fenced block (gate 4). Include everything from the *What the Generated Prompt Must Contain* checklist.
5. Present the drafted prompt in chat. Tell the user to start a fresh session and paste it in.
6. Optionally offer to refine if the user spots a missing constraint, a wrong path, or a gap in the verification plan.

## When This Skill Is the Wrong Tool

- The work fits in one session and one context window — just do it.
- The work is exploratory or experimental and the user explicitly wants to stay in-loop — a heavy orchestration handoff is overkill.
- No concrete artifacts exist to hand off yet — route the user to `beagle-analysis:brainstorm-beagle` or `beagle-analysis:write-plan` first to produce the spec and plan that this skill will hand off.
