---
name: system-prompt-curator
description: Create or improve production-grade system prompts for autonomous coding agents using evidence-gated workflow, explicit tool contracts, and completion criteria. Use when "write a system prompt", "improve an agent prompt", "curate system prompt", "autonomous agent prompt", or "review my agent prompt".
metadata:
  short-description: Curate autonomous agent prompts
---

# System Prompt Curator — production agent prompt extension

`extend` op-cell: turn a role, task class, and tool surface into a durable autonomous-agent system prompt; or correct an existing prompt until its workflow and completion gates are load-bearing. Optimize for agents that must act in a repository, recover from tool failures, verify their work, and deliver evidence rather than analysis.

Keep the prompt self-contained. Do not depend on tribal context, hidden tools, model names, or sibling documents. The generated prompt must tell the agent who it is, where it works, what tools exist, what phases it must follow, what evidence gates completion, and how to recover when reality disagrees.

Core payloads:
- `references/principles.md` — ten research-backed prompt principles and the invariant each protects.
- `references/anti-patterns.md` — failure mode → why it fails → fix table used by `--improve`.
- `references/templates.md` — mandatory template, GitHub-issue template, research template, and harness-level reinforcements.

## When to Apply

- User asks to write, curate, review, or improve a system prompt for an autonomous coding agent, research agent, issue-to-PR agent, review agent, or orchestrator-dispatched worker.
- Existing prompt lets an agent stop after reading, answer instead of acting, discover tools lazily, skip verification, or call completion without concrete artifacts.
- A team needs a prompt that survives no-human-in-loop execution: repository exploration, code edits, failure recovery, tests, commit/PR, and evidence summary.
- The prompt will run inside a harness with tools and completion actions that can be made explicit.

## When NOT to Apply

- User wants a one-off chat reply, user-facing copy, marketing prose, or a normal instruction message.
- The target is a short non-agent prompt where no tools, workflow, or completion gate exists.
- The desired behavior depends on a harness feature that does not exist and cannot be expressed in the prompt. Report the missing harness primitive instead of pretending text can enforce it.
- The user asks for adversarial jailbreak language, hidden-policy bypasses, or threats. Replace with structured gates and normal imperative language.

## Workflow

### Mode A — create

1. **Clarify by axis with `ask`.** If role, tool surface, autonomy level, or deliverable is underspecified, ask single-select axes. Mark one boring default as Recommended.
   - Role anchor: software engineer / technical analyst / reviewer / orchestrator / domain specialist.
   - Execution mode: autonomous end-to-end / human-in-the-loop / read-only research / review-only.
   - Tool surface: filesystem, search, shell, editor, git, issue tracker, PR API, browser, debugger, memory, custom tools.
   - Deliverable: patch, PR, report, review findings, plan, migration, diagnosis.
   - Verification: unit tests, typecheck, lint, e2e, repro script, source citations, manual QA, external check.
2. **Select template.** Use `references/templates.md` mandatory skeleton unless the role exactly fits the GitHub-issue or research template. Preserve section order: IDENTITY → ENVIRONMENT → TOOLS → WORKFLOW → COMPLETION → TIPS → WHAT NOT TO DO → EXAMPLES.
3. **Instantiate concretely.** Replace every placeholder with real role, project context, tool docs, commands, completion fields, and failure-recovery guidance. Never invent tools. If a tool is unknown, omit it and state the assumption outside the prompt.
4. **Add a worked trajectory.** Include at least one complete successful path. For coding agents, show explore → fail/recover → patch → verify → deliver. For research agents, show source selection → conflicting evidence → uncertainty statement.
5. **Add harness recommendations.** For autonomous or orchestrator-dispatched agents, include harness-level reinforcements from `references/templates.md`: completion validation, separate help path, observation formatting, empty-output handling, truncation rules, environment suppression, history compression, malformed-output retry.
6. **Self-evaluate before returning.** Run the validation gate below. Fix violations before output.
7. **Output.** Return the prompt in a fenced block, followed by a compact design note: identity choice, completion gate, verification evidence, token estimate, and any harness assumptions.

### Mode B — `--improve`

1. **Read target first.** Inspect the full prompt file or pasted prompt. Do not rewrite from memory.
2. **Classify scope.** Determine agent role, autonomy level, tools, deliverable, completion action, and expected evidence.
3. **Scan anti-patterns.** Use `references/anti-patterns.md`; report every confirmed issue. Certainty:
   - HIGH: explicit text causes the failure (`complete immediately`, no phases, no completion preconditions, no tools, no verification).
   - MEDIUM: structure permits the failure (tools only discoverable, vague role, weak deliverable, no recovery example).
   - LOW: style risk or missing reinforcement (aggressive language, token bloat, weak harness hints).
4. **Check all principles.** Evaluate each principle in `references/principles.md` as PASS / FAIL / PARTIAL. Do not skip principles because the prompt is short.
5. **Report findings table before rewrite.** Columns: Severity, Principle, Evidence, Risk, Fix. Keep evidence concrete: quote the phrase or section name.
6. **Rewrite.** Apply all HIGH and MEDIUM fixes. Apply LOW fixes when they reduce entropy without changing the intended role. Preserve useful domain content; delete ceremony, threats, hidden assumptions, placeholders, and duplicated instructions.
7. **Explain delta.** After the improved prompt, list material changes by invariant: identity, tool contract, workflow, completion, verification, examples, harness recommendations.
8. **Self-evaluate before returning.** Run the validation gate below against the rewritten prompt.

## Findings Severity

| Severity | Meaning | Required Action |
|---|---|---|
| HIGH | Prompt can complete without work, call finish without evidence, use nonexistent tools, or skip verification | Fix before returning |
| MEDIUM | Prompt likely drifts: vague identity, weak phases, no recovery guidance, lazy tool discovery, missing example | Fix unless user explicitly requested minimal prompt |
| LOW | Style or harness hardening issue: aggressive phrasing, token bloat, missing observation formatting, no output truncation rule | Fix when cheap; otherwise recommend |

## Constitutional Rules

1. **Identity is behavioral.** Name the work the agent performs: senior software engineer, technical analyst, security reviewer. Avoid abstract labels that do not imply action.
2. **Autonomy is explicit.** If the agent is autonomous, it continues until the deliverable exists or a named blocker is proven. Analysis is not completion.
3. **Tools are declared upfront.** Every tool used by the workflow appears in the prompt with when-to-use guidance. No hidden tool discovery.
4. **Phases are ordered.** Explore → Plan → Implement → Verify → Deliver for coding work. Research substitutes Scope → Investigate → Analyze → Report. Do not let Plan or Analyze be an exit.
5. **Completion is evidence-gated.** The finish path requires concrete artifacts: modified files, tests or citations, commit/PR/report URL, blockers tried, and summary.
6. **Failure recovery is taught.** Include at least one command/tool failure path and instructions to change approach before retrying.
7. **Tone is firm, not theatrical.** Use normal imperative language and checklists. Threats, all-caps warnings, and panic language add noise.
8. **Self-contained over clever.** The prompt must survive being copied into a fresh harness. Embed the necessary rules; do not rely on references available only to the author.

## Validation Gates

Before returning any created or improved prompt, verify:

| Gate | Pass Criteria | Blocking |
|---|---|---|
| Role anchor | Identity matches task type and implies the correct behavior | Yes |
| Tool contract | Prompt lists actual available tools and when to use them | Yes |
| Ordered workflow | Prompt has explicit phases and no analysis-phase completion | Yes |
| Artifact mandate | Prompt states the concrete deliverable and forbids read-only completion for action tasks | Yes |
| Verification | Prompt names the verification command/method or evidence substitute | Yes |
| Completion schema | Finish action requires non-empty evidence fields appropriate to the task | Yes |
| Failure recovery | Tips or example show a failed command/tool call and changed approach | Yes for autonomous agents |
| Convention discovery | Coding agents must inspect existing project patterns before editing | Yes |
| Tone | No adversarial threat block or exaggerated all-caps rule wall | Yes |
| Self-eval | All ten principles checked PASS or justified PARTIAL | Yes |

## Output Contracts

Create mode output:

```text
PROMPT:
<complete system prompt>

DESIGN NOTES:
- Identity: ...
- Completion gate: ...
- Verification: ...
- Harness assumptions: ...
- Approx tokens: ...
```

Improve mode output:

```text
FINDINGS:
| Severity | Principle | Evidence | Risk | Fix |
|---|---|---|---|---|
...

IMPROVED PROMPT:
<complete rewritten system prompt>

DELTA:
- ...

SELF-EVAL:
| Principle | Status | Note |
|---|---|---|
...
```

## Anti-patterns

- **Prompt as wish list.** Long list of virtues without phases, tools, or completion evidence. Compress into executable contract.
- **Completion as escape hatch.** Any `complete`, `finish`, or `return` instruction without preconditions. Gate it.
- **Tool mysticism.** `Use available tools as needed` with no tool list. Enumerate tools or state they are unavailable.
- **Threat stack.** `CRITICAL`, `NEVER FAIL`, `YOU WILL BE PENALIZED` blocks. Replace with normal checklists.
- **Generic identity.** `You are a focused AI agent`. Replace with role tied to task and deliverable.
- **No examples.** Agent has not seen a successful trajectory. Add one with recovery.
- **Harness-in-prompt overreach.** Trying to enforce git diff checks or output parsing only with prose when the harness can validate. Recommend harness gates separately.
