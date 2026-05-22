---
name: test
description: Persistent verification mode. Use when the user explicitly says `/test` or clearly wants exhaustive test, QA, and fix loops before signoff, especially when they want you to keep grinding while they are away. Bias Codex toward running the relevant existing test stack, browser or desktop verification, and diagnosis repeatedly until the requested surface is verified or a real blocker remains.
---

# Test

Use this as a verification-and-fix mode after implementation or during bug hunts. This is not just "run one test command". It is a persistent loop that keeps narrowing failures and rerunning checks until the requested behavior is verified.

## Default Loop

1. Define the verification target.
- affected files, routes, surfaces, and user-visible claims
- exact stopping condition for signoff
2. Build the smallest credible test matrix from the repo and task.
- code-level checks first
- integration and e2e next
- live runtime QA last
3. Run the relevant existing automated checks before inventing custom ones.
- prefer repo-native scripts and targeted specs or files
- use the stack already present: Vitest, Jest, Playwright, Cypress, pytest, go test, etc.
- widen scope only after the narrow failing checks pass
4. If the surface is interactive, verify the real runtime too.
- web: run relevant e2e flows or drive the app directly
- before browser DevTools inspection, probe `http://127.0.0.1:9333/json/version`
- if it is already live, reuse it
- if it is not live and a `chrome` launcher exists, start it automatically, wait for the port, then use `chrome-devtools`
- browser diagnosis: use `chrome-devtools` for console, network, DOM, accessibility, or performance inspection
- before Pix desktop DevTools inspection, probe `http://127.0.0.1:9334/json/version`
- if it is already live, reuse it
- if it is not live and a `tauri-pix` launcher exists, start it automatically, wait for the port, then use `tauri-devtools`
- Tauri desktop: use `tauri-devtools` and the fixed Tauri debug path when diagnosis is needed
- direct browser control: use the repo's Playwright setup or a persistent `js_repl` Playwright session when targeted manual proof is still needed
5. On failure, fix and rerun.
- repeat inspect -> patch -> rerun narrow checks -> rerun broader confidence checks
- do not stop after the first or second failed attempt
6. Before signoff, rerun the checks that support the final claims.

## Priority Rules

- Existing repo tests beat ad hoc manual clicks.
- Narrow targeted checks beat whole-suite runs unless the task truly warrants broader coverage.
- Browser or desktop verification complements automated tests; it does not replace them.
- When the repo has both unit-level tests and Playwright e2e, usually run the relevant unit or component checks first, then the relevant Playwright flow, then live diagnosis only if something is still unclear.
- When the required DevTools launcher exists, do not wait for the user to open it manually; check first, auto-launch if absent, and continue.
- If the user implies "I am stepping away" or "keep going until it is clean", keep iterating without asking after each failure.

## Good Targets

- "/test"
- "나 점심 먹고 올 테니 테스트랑 검증 끝까지 돌려"
- "버그 없어질 때까지 계속 확인해"
- "회귀까지 보고 진짜 끝내줘"
- "웹, 모바일, Tauri까지 확인하고 막아줘"

## Avoid

- Do not stop at "probably fixed".
- Do not run the whole monorepo matrix by reflex.
- Do not skip existing automated tests just because manual QA looked okay.
- Do not claim success if any required surface was not actually checked.
- Do not keep brute-forcing when a real external blocker is the limit; name it clearly.

## Finish

Return:
- verification target
- automated checks run
- runtime surfaces checked
- pass or fail
- remaining blockers or residual risk
