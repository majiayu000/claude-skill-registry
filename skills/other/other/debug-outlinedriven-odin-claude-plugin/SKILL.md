---
name: debug
description: Hypothesis-driven defect isolation — stack-trace forensics, breakpoint strategy, state inspection, and root-cause confirmation via minimal repro. Use when a defect surfaces (test failure, crash, exception, wrong output, intermittent flake) and the cause is not immediately obvious from the change set.
---

A bug is a falsified assumption. Find the assumption, falsify it deliberately, observe the divergence, narrow until one line owns the lie. No speculation, no shotgun edits, no "fix and rerun" guessing.

## When to Apply / NOT

Apply: test fails and cause unclear; production stack trace; intermittent / flaky behavior; wrong output without crash; regression after known commit window; heisenbug.

NOT apply: performance regression with correct outputs; security defect; symptom obvious from one-line read; architectural confusion.

## Anti-patterns

- **Shotgun debugging**: editing several files hoping one fixes it.
- **Print-and-rerun**: adding logs without a target observation.
- **Premature fix**: patching symptom before isolating root cause.
- **Ignoring the trace**: stack frames are evidence.
- **Changing two variables at once**: defeats falsification.
- **Deleting the failing test**: capturing the bug is the asset.

## Hypothesis Loop (language-neutral)

1. **Observe** — Reproduce the failure deterministically.
2. **Trace** — Read the failure artifact (stack, log, core dump).
3. **Hypothesize** — One falsifiable claim. Rank hypotheses by likelihood.
4. **Instrument** — Insert minimum probe (breakpoint, structured log, assertion).
5. **Run** — Execute the minimal repro.
6. **Confirm or refute** — If refuted, demote and pick next hypothesis.
7. **Narrow** — Binary-search the suspect range. Use `git bisect` for regressions.
8. **Confirm root cause** — Inverse test: removing/altering the cause must restore correctness.
9. **Hand off** — Forward to TDD: minimal repro becomes permanent failing test.

## Stack-Trace Reading

- **Top frame is innermost**: the failure point.
- **Cause vs context**: An exception's `caused by` chain encodes *why*; the stack encodes *where*.
- **Async traces**: virtual stacks drop frames between awaits — capture causal context.
- **Symbol fidelity**: Strip-mode binaries lose frame names. Build with debug info.
- **Inlined / optimized frames**: `<inlined>` markers signal source-line-to-instruction map is approximate.

## Parallel Tooling

| Family | Live debugger | Postmortem / record | Remote attach |
|---|---|---|---|
| Systems (C/C++/Rust) | `gdb`, `lldb`, `rust-gdb`, `rust-lldb` | `coredumpctl` + `gdb core`, `rr record/replay` | `gdb -p <pid>` / `lldb -p <pid>` |
| Python | `pdb`, `ipdb`, `pdbpp`, `breakpoint()` | `faulthandler`, `py-spy dump`, traceback module | `debugpy --listen` |
| Go | `dlv debug`, `dlv test`, `dlv attach <pid>` | `runtime/pprof`, GOTRACEBACK=crash | `dlv connect <addr>` |
| Java/Kotlin | IntelliJ debugger, `jdb` | hs_err logs, JFR, heap dump (`jmap`) | JDWP `-agentlib:jdwp=...` |
| JavaScript/TypeScript | `node --inspect`, Chrome DevTools | `--report-uncaught-exception` reports | `--inspect=0.0.0.0:9229` |
| OCaml | `ocamldebug`, `Printexc.record_backtrace true` | core file + `ocaml-gdb`, memtrace | `ocamldebug -s <socket>` |

Use `procs` (not `ps`) for PID. Use `bat -P -p -n` (not `cat`) for trace files. Use `git grep -n -C 3 'pattern'` (not `grep`) for callsites.

## Constitutional Rules

1. **Reproduce before fixing**.
2. **One hypothesis at a time**.
3. **Evidence over inference**.
4. **Capture the bug as a test** (hand to TDD).
5. **Confirm with inverse**.
6. **Bisect for regressions**.
7. **No silent edits**.
