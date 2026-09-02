---
name: unlazy
description: 'Use when task decomposition needs gate-file proof before a done claim, or when the user says "unlazy", "depth tree", "gates", or "do not stop until it is done". Detects half-done work, premature done claims, stubs, and silently narrowed scope. In orchestrated mode (tree 4+), enforces dispatch-state, human approval binding, and parent reverification before a done claim.'
---

# Unlazy

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User invokes 'unlazy', 'depth tree', 'gates', or 'do not stop until it is done'; laziness symptoms appear (half-done work, premature done claims, stubs, silently narrowed scope); or a build decomposes three or more layers deep. |
| Authority | Reversible-local: writes only named local gate files and evidence; rollback is file deletion of the created .outline/ tree. |
| Side effect | Creates .outline/GATES.md and per-leaf gate files; executes gate_check.py; flips checkboxes; records EVIDENCE. In orchestrated mode, writes .outline/dispatch.json and approval logs. No remote mutation. |
| Done | Solo mode: gate_check.py exits 0; every leaf box is checked and EVIDENCE is non-pending; no stubs, placeholders, or follow-up remain. Honestly surfaced abandonment (ABANDON lines with reasons) is accounted in the report but blocks a clean done: the report carries the abandoned count and ids. Orchestrated mode: same gate requirements plus every returned leaf is parent-reverified, dispatch state is valid, and abandoned count is zero: any abandonment produces HANDOFF REQUIRED and blocks done per `references/dispatch-gates.md`. |

## Inputs

Required: task decomposition and intended outcome. Optional: depth hint (tree N) and any work already in progress. The skill directory is found by locating scripts/gate_check.py relative to the working directory.

## Gate format

Each item in the gates file is a checkbox with a unique ID, an observable outcome statement, and either an automated CHECK/EXPECT pair or a manual EVIDENCE field. CHECK is the shell command; EXPECT is the substring or /regex/ the output must contain. A checked box with EVIDENCE still reading pending counts as UNMET. Template files live in assets/gates.md under the skill directory.

- Box format: `- [ ] <id>: <observable outcome>`
- Automated gate: `  CHECK: <command>` / `  EXPECT: <substring or /regex/>` / `  EVIDENCE: pending`
- Manual gate: `  EVIDENCE: pending`
- Abandoned gate: `ABANDON: <id> <reason>`, reported, not deleted
- Leaf IDs: G1, G2, … inside a leaf gates file
- Branch/root IDs: N1, N2, … inside a branch gates file

Templates: plan contract, leaf gates, and branch gates in assets/gates.md.

## Procedure

1. Locate the skill directory by finding scripts/gate_check.py relative to the working directory. **Done when:** the skill directory is located.
2. If .outline/GATES.md does not exist, create it from the templates. Decompose the task into a depth tree: Layer 1 is the task; leaves are the only places real work happens. Depth guidance: tree 2-3 for a feature, bug hunt, or document (solo); tree 4-5 for a subsystem or serious refactor; tree 6-7 for an entire project built to a high bar, orchestrated with leaves on disjoint work units. **Done when:** the depth tree is decomposed and GATES.md is created.
3. Before real work starts, write the acceptance gates to .outline/GATES.md (solo) or .outline/gates/leaf-*.md (orchestrated), using the templates. One checkbox per observable outcome the task requires. For command-checkable outcomes, add CHECK (runnable command) and EXPECT (required output). The Hoare contract: CHECK is the test, EXPECT is the postcondition, EVIDENCE is the recorded proof. **Done when:** every observable outcome has a checkbox with CHECK/EXPECT or manual EVIDENCE.
4. Work each leaf in four passes: implement completely without placeholders, reread as a domain expert, hunt defects, then polish at zero cost. **Done when:** a full four-pass review finds no change worth making.
5. During and after work, run gate_check.py:
   ```
   python3 <skill-dir>/scripts/gate_check.py [.outline/GATES.md ...]
   ```
   It runs each CHECK command, compares output against EXPECT (substring by default, or /regex/ with flags), flips a box from `[ ]` to `[x]` when the gate is met, and records EVIDENCE with the actual command output. --status reports without changing anything. **Done when:** gate_check.py has been run and boxes are flipped or unmet gates are identified.
6. Before reporting done, run gate_check.py again. If any gate is still unchecked or has pending evidence, stop and do that work instead. The done state is the gates file, not the feeling of done. In orchestrated mode, unmet gates block done unconditionally: there is no abandonment path; see `references/dispatch-gates.md`. **Done when:** all gates are checked with non-pending EVIDENCE, or remaining work is identified.
7. Solo mode only: if a gate becomes genuinely impossible, add ABANDON: <id> <reason> to the gates file and surface it in the report. Visible surrender is honest; silent scope-narrowing is not. Abandonment is accounted but blocks a clean done: the report carries the abandoned count and ids. In orchestrated mode, abandonment is not permitted; an impossible gate produces HANDOFF REQUIRED per `references/dispatch-gates.md`. **Done when:** the ABANDON line is added and surfaced (solo), or the handoff is declared (orchestrated).
8. Report the gates ledger: paste the file with its count, N of N checked, all EVIDENCE lines with actual output, and every ABANDON line surfaced. In orchestrated mode, report zero abandoned or declare HANDOFF REQUIRED. **Done when:** the report contains the full ledger with counts, evidence, and abandons.
9. In orchestrated mode (tree 4+), apply the dispatch enforcement layers in `references/dispatch-gates.md`: strict parsing without executing, human approval bound to the exact CHECK before execution, the dispatch state machine in `.outline/dispatch.json`, and parent reverification of every returned leaf. A CHECK cannot approve itself; child-produced evidence alone cannot mark a leaf VERIFIED. The parent reruns every runnable leaf CHECK on return. **Done when:** every returned leaf is parent-reverified, dispatch state is valid, and branch integration gates pass.

## Failure and recovery
- Missing gates file: create it from templates and run step 3 before continuing.
- Checker non-zero: count unmet boxes; stop and do the remaining work.
- Unchecked box with pending EVIDENCE: counts as UNMET; do not report done.
- Box is checked but evidence still pending: counts as UNMET; do not report done.
- Gate becomes impossible: add ABANDON: <id> <reason>; report it; do not silently drop.
- Stop when gates are unmet rather than narrowing scope or claiming done.
- Orchestrated mode: missing or stale approval for a CHECK: display the complete binding and leave CHECK unexecuted; never reuse a near match.
- Orchestrated mode: invalid dispatch transition: leave dispatch.json unchanged; report current state, rejected event, and allowed next events.
- Orchestrated mode: child return without parent proof: keep leaf unverified; rerun its approved oracles and parent integration gates.

## Output
The gates ledger with every box and its EVIDENCE line showing actual command output, a summary line (N of N checked, M abandoned with reasons), and the final report. Solo mode: abandonment is surfaced honestly with ids and reasons but blocks a clean done. Orchestrated mode: zero abandonment required; any abandonment produces HANDOFF REQUIRED and blocks done per `references/dispatch-gates.md`.
