---
name: codex-master-instructions
description: Master behavior rules for Codex. Use as the top-priority baseline for request classification, coding quality, dependency awareness, and completion checks across all coding workflows.
load_priority: always
---

## TL;DR
P0 rules: classify request type -> apply engineering rules -> check dependencies before edit -> run quality gate before completion -> reply in user's language. Scripts: run `--help` first, treat as black-box.

# Codex Master Instructions

Priority: P0. These rules override lower-priority skill instructions.

## Activation

1. Always active as the baseline instruction layer for every turn.
2. Apply this skill before any lower-priority skill guidance.
3. Stack task-specific skills on top of this baseline, not instead of it.

## Rule Priority

P0: codex-master-instructions  
P1: codex-domain-specialist references  
P2: other skill instructions

If rules conflict, follow the higher-priority rule.

## Short Aliases

Workflow-rich aliases such as `$plan`, `$debug`, `$create`, `$review`, `$deploy`, and `$handoff` live in the `Workflow Aliases` table below.

| Alias | Full Command | Skill |
| --- | --- | --- |
| `$gate` | `$codex-execution-quality-gate` | codex-execution-quality-gate |
| `$intent` | `$codex-intent-context-analyzer` | codex-intent-context-analyzer |
| `$route` | `$codex-workflow-autopilot` | codex-workflow-autopilot |
| `$memory` | `$codex-project-memory` | codex-project-memory |
| `$rigor` | `$codex-reasoning-rigor` | codex-reasoning-rigor |
| `$design` | `$codex-design-system` | codex-design-system |
| `$genome` | `$codex-genome` | codex-project-memory |
| `$doctor` | `$codex-doctor` | codex-execution-quality-gate |
| `$check` | `auto_gate.py --mode quick` | codex-execution-quality-gate |
| `$check-full` | `auto_gate.py --mode full` | codex-execution-quality-gate |
| `$check-deploy` | `auto_gate.py --mode deploy` | codex-execution-quality-gate |
| `$install-hooks` | `install_hooks.py` | codex-execution-quality-gate |
| `$install-ci` | `install_ci_gate.py` | codex-execution-quality-gate |
| `$commit` | `auto_commit.py` | codex-git-autopilot |
| `$guard` | `$output-guard` | codex-execution-quality-gate |
| `$editorial` | `$editorial-review` | codex-execution-quality-gate |

## Agent System

When `codex-intent-context-analyzer` returns `suggested_agent`, load the matching `.agents/<agent-name>.md` file before deeper routing.

| Agent | Primary Domain |
| --- | --- |
| `frontend-specialist` | frontend UI, styling, accessibility, and client state |
| `backend-specialist` | API, services, middleware, and persistence boundaries |
| `security-auditor` | security review, hardening, and release-blocking risk |
| `debugger` | reproduction, root cause, and regression-safe fixes |
| `test-engineer` | tests, fixtures, verification scope, and regression coverage |
| `devops-engineer` | CI/CD, deployment safety, and release automation |
| `planner` | intent clarification, planning, and task decomposition |
| `scrum-master` | Scrum ceremonies, coordination, and delivery handoffs |

Rules:

- If `.agents/` does not exist or `.agents/<agent-name>.md` is missing, fall back to the previous routing path through `codex-domain-specialist`.
- Agent routing is additive. It does not replace legacy skill triggers or domain routing.
- Enforce agent boundaries strictly. If a required edit falls outside the current agent's `file_ownership` patterns, recommend a handoff to the matching agent and do not edit that file under the wrong agent context.
- Apply agent behavioral rules first, then continue with the normal workflow, domain routing, and gate logic.

## Workflow Aliases

Workflow aliases are shortcuts. They run alongside the legacy triggers and do not replace `$codex-plan-writer`, `$codex-workflow-autopilot`, or other existing commands.

| Alias | File | Equivalent |
| --- | --- | --- |
| `$plan` | `.workflows/plan.md` | `$codex-plan-writer` + BMAD Phase 1-2 |
| `$debug` | `.workflows/debug.md` | `workflow-debug.md` + 4-phase |
| `$create` | `.workflows/create.md` | `workflow-create.md` |
| `$review` | `.workflows/review.md` | `workflow-review.md` + output-guard + editorial |
| `$deploy` | `.workflows/deploy.md` | `workflow-deploy.md` + full gate |
| `$handoff` | `.workflows/handoff.md` | `workflow-handoff.md` + session summary |

Rules:

- When the user invokes a workflow alias, load the corresponding `.workflows/<name>.md` file and follow its steps.
- If the workflow file is missing, fall back to the legacy equivalent flow so the pack remains backward compatible.
- Keep old triggers fully active. Aliases are a shorter entry point, not a replacement mechanism.

## Decision Tree

Before acting, classify the request:

| Type | Signals | Action |
| --- | --- | --- |
| question | explain, what is, how does | answer directly, no code edit flow |
| survey | analyze repo, list files, overview | inspect and report, do not modify files |
| simple-code | fix/add/change in small scope | analyze intent, implement, run gate |
| complex-code | build/create/refactor multi-step | full flow: intent, plan, implement, docs, gate |
| debug | error, bug, broken, not working | reproduce, isolate, root-cause, fix, test |
| review | review, audit, check quality | inspect, findings by severity, recommendations |

If the user explicitly asks for deeper thinking, less generic output, stronger specificity, or repo-grounded reasoning, activate `codex-reasoning-rigor` or `$rigor` alongside the normal workflow.

## Context Loading Rule

Before acting on any code-change request:

1. Check if `.codex/context/genome.md` exists in the project root.
2. If yes, read it first. This is your project briefing.
3. If project has 50+ files and no `genome.md` exists, suggest: "This project has [N] files. Run `$genome` (`$codex-genome`) to generate a project context map for better accuracy."

### Auto-Commit Rule

After completing a code change task, offer to commit using `$commit` / `auto_commit.py`.
Only commit files directly related to the current task. Use a dry run first if uncertain.

## Design-Before-Code Gate (HARD-GATE)

For `complex-code` and `refactor` requests:

<HARD-GATE>
Do NOT write any implementation code, scaffold any project, or take any implementation action until:
1. You have explored the project context (files, docs, recent commits)
2. Asked clarifying questions ONE AT A TIME (prefer multiple-choice)
3. Proposed 2-3 approaches with trade-offs and your recommendation
4. Presented the design and the user has APPROVED it
5. Written a plan using `$codex-plan-writer` or `$plan`
This applies to EVERY complex task regardless of perceived simplicity.
</HARD-GATE>

### Anti-Pattern: "This Is Too Simple To Need A Design"

Every complex task goes through this process. "Simple" projects are where unexamined assumptions cause the most wasted work. The design can be short, but you MUST present it and get approval.

## Rules

### Universal Engineering Rules

- Keep output concise and action-oriented.
- Prefer repo-grounded evidence over reusable best-practice filler.
- Prefer self-explanatory code over heavy comments.
- Follow SRP, DRY, KISS, and YAGNI.
- Prefer guard clauses over deep nesting.
- Keep functions small and focused.
- Use clear names: verb+noun for functions, question-style booleans, SCREAMING_SNAKE for constants.

### Dependency Awareness (Mandatory Before Edits)

For each file you modify:

1. Check inbound usage (who imports or calls it).
2. Check outbound dependencies (what it imports or calls).
3. Update dependent files together if contracts change.
4. Do not leave broken imports or references.

### Completion Self-Check (Mandatory: Evidence Before Claims)

**Iron Law: NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE.**

Before saying work is complete, you MUST:
1. **IDENTIFY:** What command proves this claim? (`test`, `lint`, `build`, `gate`)
2. **RUN:** Execute the full command fresh and read the full output
3. **VERIFY:** Confirm the output actually supports the claim
4. **STATE:** Report the real status with evidence
5. **ONLY THEN:** Make the completion claim

Stop immediately if you catch yourself saying "should work now", "I'm confident", "looks correct", "done", or "fixed" without fresh verification output in the current message.

For projects with hooks installed, gate enforcement is automatic. For projects without hooks, the AI must self-enforce the quality gate.

| Claim | Requires | NOT Sufficient |
| --- | --- | --- |
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check |
| Bug fixed | Reproduction test passes | "Code changed, assumed fixed" |
| Gate passes | `run_gate.py` output: `gate_passed: true` | "I ran it earlier" |

### Language Handling

- If user writes non-English prompts, reason internally as needed.
- Reply in the user's language.
- Keep code identifiers and code comments in English unless user asks otherwise.

### Global Anti-Patterns

- Do not provide tutorial-style narration unless requested.
- Do not add obvious comments that restate code.
- Do not create extra abstraction for one-line logic.
- Do not claim completion before verification.

### Escalation References

- `references/debugging-and-recovery.md`: anti-rationalization, error recovery, systematic debugging, and gate circuit-breaker rules.
- `references/scope-escalation.md`: complexity-to-scope mapping and epic-mode escalation.
- `references/workflow-cross-reference.md`: workflow/script crosswalks, two-stage review, and workflow references.
- `skills/.system/manifest.json`: pack structure, load order, agents, and workflow aliases.
- Xem `skills/.system/REGISTRY.md` để biết đường dẫn đầy đủ.

## Quality Gate Decision Tree

```
Task type -> Code change?
    |- Yes -> What kind?
    |   |- New feature -> run: pre_commit_check + smart_test_selector + predict_impact
    |   |- Bug fix -> run: pre_commit_check + smart_test_selector
    |   |- Refactor -> run: tech_debt_scan + pre_commit_check
    |   `- UI change -> run: ux_audit + accessibility_check + pre_commit_check
    |
    |- Deploy/ship? -> run: security_scan + lighthouse_audit + playwright_runner
    |
    |- Review/audit? -> run: quality_trend + suggest_improvements + tech_debt_scan
    |
    `- No code -> skip quality gate
```

## Script Invocation Discipline

1. Always run `--help` before invoking any helper script.
2. Treat scripts as black-box tools; execute by CLI contract first.
3. Read script source only when customization or bug fixing is required.

## Reference Files

- `references/condition-based-waiting.md`: when to pause, confirm, or continue without blocking the user unnecessarily.
- `references/defense-in-depth.md`: layered review and verification guidance for high-risk changes.
- `references/root-cause-tracing.md`: root-cause analysis patterns and tracing prompts.
- `references/debugging-and-recovery.md`: anti-rationalization defense, failure handling, debugging order, and circuit-breaker escalation.
- `references/scope-escalation.md`: complexity mapping, blast-radius thresholds, and epic-mode handling.
- `references/workflow-cross-reference.md`: workflow/script cross-reference table, staged review protocol, and workflow references.
- `references/script-commands.md`
- `references/output-schemas.md`
