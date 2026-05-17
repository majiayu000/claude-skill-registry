# Testing — Fixtures & Smoke Test

The plugin has no Elixir ExUnit harness of its own (it distributes skills,
agents, hooks — no `lib/` or `test/`). Tests for `/phx:deps-audit` rules
live as a bash smoke-test runner that materializes synthetic fixtures and
asserts each rule fires.

## Why heredoc fixtures, not committed `.ex` files

The plugin's PostToolUse hook (`format-elixir.sh`) treats every committed
`.ex` and `.exs` file as project source and runs `mix format
--check-formatted` against it. Our fixtures are intentionally malformed:

- Rule 1 fixture contains raw U+202E bidi bytes (Trojan Source).
- Rule 2 fixture calls `Code.eval_string(@payload)` at module top level —
  syntactically valid but semantically hostile.
- Rule 5 fixture pair carries an added `:git` dep that should be flagged.

Committing these would (a) flag the plugin's own format hook on every
write and (b) imply the plugin authors endorse the code as exemplary
Elixir. Both bad. Storing the fixture content as `setup.sh` heredocs
under `smoke-test/fixtures.d/<name>/` keeps them version-controlled
without polluting the plugin's lint surface.

## Harness layout (Phase 2)

```
smoke-test/
├── runner.sh             # driver — loads every fixtures.d/<name>/
├── lib/detectors.sh      # shared rule detectors (perl/grep/awk)
├── fixtures.d/<name>/    # one dir per fixture
│   ├── setup.sh          # heredoc'd fixture content, writes into $FIXTURE_DIR
│   └── expected.txt      # rule:N op:>= count:1 assertions
└── corpus.d/             # on-demand loader for real Hex tarballs
    ├── fetch.sh
    └── README.md
```

`runner.sh` discovers fixtures automatically — drop a new directory in
`fixtures.d/` and it runs next pass.

## Running the smoke test

```bash
bash plugins/elixir-phoenix/skills/deps-audit/smoke-test/runner.sh
```

Expected output (~1 second):

```
Running 7 fixture(s) under .../fixtures.d:
  ok 00_clean rule:1 == 0 (got 0)
  ok 00_clean rule:2 == 0 (got 0)
  ok 00_clean rule:3 == 0 (got 0)
  ok 00_clean rule:4 == 0 (got 0)
  ok 00_clean rule:7 == 0 (got 0)
  ok 01_bidi rule:1 >= 1 (got 1)
  ok 02_eval rule:2 >= 1 (got 1)
  ok 03_compile_exec rule:3 >= 1 (got 1)
  ok 04_binary_to_term rule:4 >= 1 (got 1)
  ok 05_git_dep rule:5 >= 1 (got 1)
  ok 07_base64 rule:7 >= 1 (got 1)

smoke: 7 pass, 0 fail
```

Exit `0` = all pass. Exit `1` with `fail` lines otherwise.

## Coverage matrix

| Rule | Fixture | Detector under test | Asserts |
|------|---------|---------------------|---------|
| Rule 1 (bidi) | `01_bidi/` — file with raw U+202E byte | perl `[\x{202A}-\x{202E}\x{2066}-\x{2069}\x{200E}\x{200F}\x{061C}]` | ≥1 finding |
| Rule 2 (eval) | `02_eval/` — top-level `Code.eval_string(@payload)` | grep `^[[:space:]]*Code\.eval_(string\|quoted)\(` | ≥1 finding |
| Rule 3 (compile exec) | `03_compile_exec/` — `System.cmd` inside `__before_compile__` | awk scope tracker | ≥1 finding |
| Rule 4 (binary_to_term) | `04_binary_to_term/` — `:erlang.binary_to_term(blob)` | grep `:erlang\.binary_to_term\([^,]+\)\s*$` | ≥1 finding |
| Rule 5 (new :git dep) | `05_git_dep/{old,new}` — new `git:` keyword | grep diff of `git:` count | ≥1 new dep |
| Rule 7 (base64) | `07_base64/` — 308-char base64 literal | perl `"[A-Za-z0-9+/]{256,}={0,2}"` | ≥1 finding |
| All | `00_clean/` — benign module | All 5 single-tarball rules | 0 findings each |

**Rules 6 and 8 are not smoke-tested** — both require live Hex API calls
and would make the smoke flaky/slow. They have unit-test stubs in
`references/hex-api.md` (synthetic JSON fixtures for the parser, no
network). Phase 2 will add VCR-style HTTP cassettes for full coverage.

## Detectors in the smoke test vs full `rules-impl.md`

The smoke test uses **lightweight detector approximations** (single-line
grep/perl/awk patterns) for speed. The full detectors in `rules-impl.md`
use AST walks (`Code.string_to_quoted/2`) and richer scope tracking —
they're more accurate but require a working Mix install. The smoke test's
job is to catch regressions in the *fixture shape* (e.g., did we accidentally
strip the bidi byte during a refactor?), not to validate the AST detectors
themselves.

When AST-detector behaviour is in question, run the deps-audit skill
against a real `mix.lock` change and compare output to the smoke
detectors. Discrepancies that favour the AST detector are usually correct;
discrepancies that favour the smoke detector are usually bugs in the AST
detector worth fixing.

## When to update fixtures

- A new rule lands → add a new `fixtures.d/<NN>_<name>/` directory with
  `setup.sh` + `expected.txt`. Runner picks it up automatically.
- An existing detector changes its output shape → adjust the
  `expected.txt` assertion, not the fixture, unless the fixture itself
  no longer represents the hostile pattern.
- A detector emits unexpected findings on `00_clean/` → that's a false
  positive regression. Investigate before relaxing the assertion.

## Phase 2 test plan

- VCR cassettes for Rules 6 and 8 (Hex API).
- Real malicious-package replay fixtures (synthetic but modelled on
  axios / event-stream patterns).
- FP audit on the top-50 most-installed Hex packages (manual review of
  clean output — listed in plan success criteria).
- Property-based testing for the rule combiner using StreamData (would
  need an Elixir test harness for the plugin, deferred).

## CI integration

For now the smoke test is run manually. To wire into the eval pipeline,
add a `smoke` target in `Makefile` whose recipe runs `runner.sh` from
the harness root. Deferred until corpus fetch from `corpus.d/fetch.sh`
is reliable enough for CI gating (it depends on hex.pm reachability).
