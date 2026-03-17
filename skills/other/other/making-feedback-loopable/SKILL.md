---
name: making-feedback-loopable
description: "Scaffolds build/test/lint/runtime checks so agents get structured, self-locating feedback with file paths, line numbers, and error codes. Use when setting up a repo for AI-assisted development, when an agent is failing to debug due to weak diagnostics, or when asked to make a codebase more LLM-friendly."
---

# Making Feedback Loopable

This skill sets up a project so that an LLM agent can autonomously build, test, lint, and debug by receiving structured, parseable feedback at every step. The core idea: **an agent is an LLM, a loop, and enough tokens** — but the loop only works if every iteration produces feedback the agent can act on.

## Principles

1. **Every action must produce readable output.** If the agent runs a command and gets no output, or gets output it can't parse, the loop is broken.
2. **Errors must be self-locating.** Feedback should include file paths, line numbers, and error codes — not just prose.
3. **Fast feedback beats thorough feedback.** A 2-second typecheck that catches 80% of issues is more valuable than a 2-minute full build.
4. **Feedback should be layered.** Structure the feedback pipeline as: typecheck → lint → unit test → integration test → runtime check. Each layer catches different classes of errors.
5. **The agent should never have to guess how to verify its work.** Document every verification command in AGENTS.md.

## Guardrails

- **Prefer existing tooling.** Use whatever the repo and CI already run. Do not introduce a new linter, type checker, or test framework unless the project has none and the user has asked for one.
- **Minimize new dependencies.** Each new tool added is a maintenance burden. Add only what's needed to close a feedback gap.
- **Don't be invasive.** Changing build configs, adding devDependencies, or restructuring test directories can break things. Make the smallest change that closes the loop.
- **Ask before adding.** If a major tool (e.g., ESLint, mypy, clippy) is missing, confirm with the user before adding it.

## Workflow

When this skill is invoked, follow these steps in order:

### Step 1: Audit the existing feedback surface

Read the project's README, AGENTS.md (if it exists), package.json / Cargo.toml / go.mod / Makefile / pyproject.toml (whichever applies), and CI config to answer:

- What build command exists? Does it produce structured output with file paths and line numbers?
- What test command exists? Does it report individual test names, pass/fail, and failure details?
- What linter exists? Does it output machine-readable diagnostics?
- What type checker exists?
- Are there any runtime health checks, dev servers with error overlays, or log outputs?
- How long does each command take to run?

Summarize findings as a checklist of what exists and what's missing.

### Step 2: Create or update AGENTS.md

Ensure the project has an AGENTS.md at the root with at minimum:

```markdown
## Build & Verify Commands

Run these commands to verify changes (ordered from fastest to most thorough):

1. **Typecheck**: `<command>` — catches type errors (~Xs)
2. **Lint**: `<command>` — catches style and correctness issues (~Xs)
3. **Unit tests**: `<command>` — runs fast isolated tests (~Xs)
4. **Full test suite**: `<command>` — runs all tests including integration (~Xs)
5. **Build**: `<command>` — full production build (~Xs)

After making changes, always run at least steps 1-3 before considering the task done.
```

Fill in the actual commands and approximate durations for this project. If commands don't exist yet, note that and proceed to step 3.

### Step 3: Add missing feedback infrastructure

For each gap identified in step 1, add the minimum scaffolding to close it. Common patterns by ecosystem:

#### TypeScript / JavaScript
- Add a `tsconfig.json` with `"noEmit": true` for fast typechecking via `tsc --noEmit`
- Add ESLint with `--format=compact` or `--format=json` for machine-readable output
- Ensure test runner (vitest, jest, etc.) is configured with `--reporter=verbose` so individual test names and failures are visible
- Add a `check` script to package.json: `"check": "tsc --noEmit && eslint . && vitest run"`

#### Rust
- Ensure `cargo check` works (fast typecheck without full compilation)
- Use `cargo clippy -- -D warnings` for lint
- Use `cargo test -- --nocapture` for test output with stdout visible
- Add a `check` alias or Makefile target: `check: cargo check && cargo clippy -- -D warnings && cargo test`

#### Go
- Use `go vet ./...` for static analysis
- Use `golangci-lint run` if available
- Ensure `go test ./... -v` is the test command for verbose output
- Add a Makefile target: `check: go vet ./... && go test ./... -v`

#### Python
- Use `mypy` or `pyright` for type checking
- Use `ruff check` or `flake8` for linting with machine-readable output
- Ensure `pytest -v` is configured for verbose test output
- Add a script or Makefile: `check: mypy . && ruff check . && pytest -v`

#### General (any ecosystem)
- If no test framework exists, set one up with at least one example test
- If no linter exists, add one appropriate to the language
- If no type checker exists and the language supports one, add it
- Ensure all tools output file paths relative to the project root

### Step 4: Make error output agent-friendly

Review each feedback command's output format. Improve it where possible:

- **Prefer compact/machine-readable formats** over pretty-printed ones for CI and agent use. Many tools support `--format=json` or `--format=compact`.
- **Ensure file paths are relative to project root**, not absolute paths that vary by machine.
- **Limit output volume.** If a command can produce thousands of lines of errors, use tool-native limits rather than piping to `head` (which can swallow exit codes). Examples: ESLint's `--max-warnings`, pytest's `--maxfail=N`, Rust's default error limit. Flooding the context window with errors is counterproductive.
- **Add error-code references** where possible. Tools like ESLint rules, Rust error codes, and mypy error codes help the agent look up what went wrong.

### Step 5: Add structured checks for review

Create `.agents/checks/` directory with project-specific checks that encode team knowledge the agent wouldn't otherwise have. Examples:

```markdown
# .agents/checks/build-feedback.md
---
name: build-feedback
description: Ensures changes don't break the feedback loop
severity-default: high
tools: [Bash, Read]
---

Verify that these commands still work and produce useful output:
1. Run the typecheck command from AGENTS.md
2. Run the lint command from AGENTS.md
3. Run the test command from AGENTS.md

If any command fails with an error unrelated to the current changes,
or if any command produces no output at all, flag it.
```

```markdown
# .agents/checks/error-handling.md
---
name: error-handling
description: Ensures errors are observable and debuggable
severity-default: medium
tools: [Grep, Read]
---

Check that:
- No errors are silently swallowed (empty catch blocks, `_ = err`, etc.)
- Error messages include enough context to locate the problem (file, function, input)
- Logging is present at appropriate levels for debugging
- API endpoints return structured error responses, not bare strings
```

### Step 6: Add development-server and runtime feedback (if applicable)

For projects with a dev server or runtime component:

- Ensure the dev server logs errors with stack traces to stdout/stderr
- Add a health-check endpoint (e.g., `/healthz`) that the agent can curl
- If the project has a UI, ensure the agent can screenshot it (document the local URL in AGENTS.md)
- Add structured logging (JSON logs) so the agent can parse runtime errors

Document these in AGENTS.md:

```markdown
## Runtime Verification

- **Dev server**: `<start command>` → runs at `http://localhost:<port>`
- **Health check**: `curl http://localhost:<port>/healthz`
- **Logs**: visible in the terminal running the dev server
```

### Step 7: Validate the loop end-to-end

Introduce a small, intentional error (e.g., a type error or a failing test assertion) and run the full feedback pipeline to confirm:

1. The error is caught by at least one command
2. The error output includes the file path and line number
3. The error message is clear enough that an agent could fix it without additional context
4. After fixing the error, the commands pass cleanly

Remove the intentional error and confirm everything passes.

## Summary Checklist

After applying this skill, the project should have:

- [ ] AGENTS.md with ordered build/verify commands and approximate durations
- [ ] A fast typecheck command (< 10s)
- [ ] A linter with machine-readable output
- [ ] A test runner with verbose, per-test output
- [ ] A full build command
- [ ] `.agents/checks/` with at least one project-specific check
- [ ] All error output includes file paths and line numbers
- [ ] Runtime feedback documented (if applicable)
- [ ] The full feedback pipeline validated end-to-end
