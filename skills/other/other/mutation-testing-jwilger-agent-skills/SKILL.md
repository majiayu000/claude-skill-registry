---
name: mutation-testing
description: >-
  Mutation testing to validate test quality before PR creation. Runs mutation
  tools, enforces 100% kill rate, reports surviving mutants with recommended
  fixes. Activate when validating test coverage, preparing pull requests,
  checking test quality, or when asked about mutation testing.
license: CC0-1.0
compatibility: Requires a mutation testing tool (cargo-mutants, Stryker, mutmut, or Muzak)
metadata:
  author: jwilger
  version: "1.0"
  requires: [tdd-cycle]
  context: [test-files, source-files]
  phase: ship
  standalone: true
---

# Mutation Testing

**Value:** Feedback -- mutation testing closes the verification loop by
proving that tests actually detect the bugs they claim to prevent. Without
it, passing tests may provide false confidence.

## Purpose

Teaches the agent to run mutation testing as a quality gate before PR
creation. Mutation testing makes small changes (mutations) to production
code and checks whether tests catch them. Surviving mutants reveal gaps
where bugs could hide undetected. The required mutation kill rate is 100%.

## Practices

### Detect and Run the Right Tool

Detect the project type and run the appropriate mutation testing tool.

1. Check for project markers:
   - `Cargo.toml` -> Rust -> `cargo mutants`
   - `package.json` -> TypeScript/JavaScript -> `npx stryker run`
   - `pyproject.toml` or `setup.py` -> Python -> `mutmut run`
   - `mix.exs` -> Elixir -> `mix muzak`

2. Verify the tool is installed. If not, provide installation instructions:
   - Rust: `cargo install cargo-mutants`
   - TypeScript: `npm install --save-dev @stryker-mutator/core`
   - Python: `pip install mutmut`
   - Elixir: add `{:muzak, "~> 1.0", only: :test}` to deps

3. Run mutation testing against the relevant scope. Prefer scoping to
   changed files or packages rather than the entire codebase when possible:
   ```
   # Rust (scoped to package)
   cargo mutants --package <package> --jobs 4

   # TypeScript
   npx stryker run

   # Python (scoped to source)
   mutmut run --paths-to-mutate=src/
   mutmut results

   # Elixir
   mix muzak
   ```

### Parse and Report Results

Extract from the mutation tool output:
- Total mutants generated
- Mutants killed (tests detected the change)
- Mutants survived (tests did NOT detect the change)
- Timed-out mutants
- Mutation score percentage

### Analyze Surviving Mutants

For each surviving mutant, report three things:

1. **Location:** File and line number
2. **Mutation:** What was changed (e.g., "replaced `+` with `-`")
3. **Meaning:** What class of bug this lets through

Common mutation types and what survival indicates:
- **Arithmetic** (`+` -> `-`, `*` -> `/`): Calculations not verified
- **Comparison** (`>` -> `>=`, `==` -> `!=`): Boundary conditions untested
- **Boolean** (`&&` -> `||`, `!` removed): Logic branches not covered
- **Return value** (`true` -> `false`, `Ok` -> `Err`): Return paths not
  checked
- **Statement removal** (line deleted): Side effects not asserted

### Recommend Missing Tests

For each surviving mutant, suggest a specific test:

```
Surviving: src/money.rs:45 -- replaced `+` with `-` in Money::add()
Recommend: Test that adding Money(50) + Money(30) equals Money(80),
           not Money(20). The current tests do not assert the sum value.

Surviving: src/account.rs:78 -- replaced `>` with `>=` in check_balance()
Recommend: Test the exact boundary -- check_balance with exactly zero
           balance. Current tests only check positive and negative.
```

### Enforce the Quality Gate

The required mutation kill rate is **100%**. All mutants must be killed.

- If score is 100%: Report success, proceed to PR creation
- If score is below 100%: List all survivors with recommendations. Block
  PR creation with a clear warning. The user may override, but the default
  is to fix first.

**Do:**
- Scope mutation runs to changed code when possible
- Report survivors with actionable fix recommendations
- Re-run after fixes to confirm all mutants are now killed
- Treat timeouts as killed (the mutation broke something)

**Do not:**
- Skip mutation testing before PR creation
- Accept surviving mutants without reporting them
- Run mutations on the entire codebase when only a module changed
- Recommend tests for data validation that belongs in domain types

## Enforcement Note

This skill provides advisory guidance. It instructs the agent to run
mutation testing and enforce a 100% kill rate, but cannot mechanically
prevent PR creation with surviving mutants. On harnesses with plugin
support, enforcement plugins can gate PR creation on mutation score. On
other harnesses, the agent follows this practice by convention. If you
observe the agent skipping mutation testing before a PR, point it out.
For available enforcement plugins, see the
[Harness Plugin Availability](../../README.md#harness-plugin-availability) table.

## Verification

After completing mutation testing, verify:

- [ ] Mutation testing tool was run against the relevant scope
- [ ] All surviving mutants are listed with file, line, and mutation type
- [ ] Each survivor has a specific test recommendation
- [ ] Mutation score is 100% (or user explicitly chose to override)
- [ ] If fixes were made, mutation testing was re-run to confirm

If any criterion is not met, revisit the relevant practice before proceeding.

## Dependencies

This skill works standalone but is most valuable as a pre-PR quality gate.
It integrates with:

- **tdd-cycle:** TDD produces the tests that mutation testing validates;
  surviving mutants indicate the TDD cycle missed a case
- **code-review:** Mutation results inform code review -- reviewers can
  check that new code has no surviving mutants

Missing a dependency? Install with:
```
npx skills add jwilger/agent-skills --skill tdd-cycle
```
