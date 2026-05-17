# Semgrep ruleset — optional precision layer

Native rules (`rules-impl.md`) carry the high-severity detection load.
Semgrep is an **optional precision layer** that stacks on top —
findings from both sources merge into the same NDJSON stream and
flow through the differ + renderer.

## Iron Laws

1. **SOFT DEPENDENCY.** If `semgrep` is not installed, the audit
   skips the layer with a one-line install hint. Never auto-install,
   never block the audit run on its absence.
2. **DEFENSE IN DEPTH, NOT REPLACEMENT.** Semgrep findings stack
   on native findings — they don't shadow them. A pattern caught by
   both layers shows up as two findings (with different `rule_id`
   namespaces), and the differ + ledger de-dup naturally.
3. **NO `--diff-depth`.** Semgrep's `--diff-depth N` flag is for
   git-diff scanning. We run on full unpacked tarballs and diff
   findings ourselves via `diff_findings.py`. Don't conflate.
4. **NORMALIZE TO PHASE 1 SHAPE.** Semgrep JSON output is parsed and
   coerced into the existing finding JSON shape — same field names,
   same severity vocabulary. The renderer doesn't know which layer a
   finding came from.

## Starter ruleset — `priv/semgrep/elixir-supply-chain.yaml`

```yaml
# Phase 2 starter ruleset. Sevens rules covering the patterns most
# robust to AST detection vs. ad-hoc regex. Soft dep — install
# instructions in the README.
rules:
  - id: elixir-compile-time-http
    message: HTTP fetch at compile time inside __before_compile__
    languages: [elixir]
    severity: ERROR
    pattern-either:
      - patterns:
          - pattern-inside: |
              defmacro __before_compile__($ENV) do
                ...
              end
          - pattern: System.cmd("curl", $ARGS)
      - patterns:
          - pattern-inside: |
              defmacro __before_compile__($ENV) do
                ...
              end
          - pattern: HTTPoison.get(...)

  - id: elixir-eval-string
    message: Code.eval_string with non-literal argument
    languages: [elixir]
    severity: ERROR
    pattern-either:
      - pattern: Code.eval_string($PAYLOAD)
      - pattern: Code.eval_quoted($PAYLOAD)
    pattern-not: Code.eval_string("$LITERAL")
    pattern-not: Code.eval_quoted("$LITERAL")

  - id: elixir-dynamic-system-cmd
    message: System.cmd with variable first argument
    languages: [elixir]
    severity: WARNING
    pattern: System.cmd($CMD, $ARGS)
    pattern-not: System.cmd("$LITERAL", $ARGS)

  - id: elixir-base64-to-eval
    message: Base.decode64 result fed directly to Code.eval_string
    languages: [elixir]
    severity: ERROR
    pattern-either:
      - pattern: Code.eval_string(Base.decode64!($X))
      - patterns:
          - pattern: |
              $X = Base.decode64!(...)
              ...
              Code.eval_string($X)

  - id: elixir-on-load-with-side-effects
    message: __on_load__ callback running System.cmd / File.write
    languages: [elixir]
    severity: ERROR
    pattern-either:
      - patterns:
          - pattern-inside: |
              def __on_load__() do
                ...
              end
          - pattern: System.cmd(...)
      - patterns:
          - pattern-inside: |
              def __on_load__() do
                ...
              end
          - pattern: File.write(...)

  - id: elixir-binary-to-term-literal
    message: :erlang.binary_to_term called without :safe option
    languages: [elixir]
    severity: ERROR
    patterns:
      - pattern: :erlang.binary_to_term($X)
      - pattern-not: :erlang.binary_to_term($X, [:safe])

  - id: elixir-erlang-apply-dynamic
    message: :erlang.apply with non-literal module or function name
    languages: [elixir]
    severity: ERROR
    pattern: :erlang.apply($MOD, $FUN, $ARGS)
    pattern-not: :erlang.apply($MOD, :$LITERAL_ATOM, $ARGS)
```

## Subprocess invocation

```bash
run_semgrep() {
  local tarball_dir="$1"
  command -v semgrep >/dev/null 2>&1 || {
    echo "semgrep: not installed (skipping). Install via 'brew install semgrep'." >&2
    return 0
  }
  semgrep \
    --config "${CLAUDE_SKILL_DIR}/priv/semgrep/elixir-supply-chain.yaml" \
    --lang elixir \
    --json \
    --quiet \
    --error \
    --metrics off \
    "${tarball_dir}" 2>/dev/null \
  | jq -c '.results[]?' \
  | while IFS= read -r r; do
      # Normalize Semgrep JSON to Phase 1 finding shape.
      jq -n -c \
        --arg pkg "${PKG}" --arg version "${VER}" \
        --arg rule_id "$(echo "${r}" | jq -r '.check_id')" \
        --arg severity "$(echo "${r}" | jq -r '.extra.severity | ascii_downcase')" \
        --arg file "$(echo "${r}" | jq -r '.path')" \
        --argjson line "$(echo "${r}" | jq -r '.start.line')" \
        --arg snippet "$(echo "${r}" | jq -r '.extra.lines | .[0:200]')" \
        --arg message "$(echo "${r}" | jq -r '.extra.message')" \
        '{pkg:$pkg, version:$version, rule_id:("semgrep/" + $rule_id),
          severity: (if $severity == "error" then "block" elif $severity == "warning" then "warn" else "info" end),
          file:$file, line:$line, snippet:$snippet, message:$message}' \
      >> "${FINDINGS_FILE:-${AUDIT_TMPDIR}/findings.jsonl}"
    done
}
```

Note the `rule_id` namespacing: native rules use integers 1-8;
Semgrep rules use string prefixes (`semgrep/elixir-eval-string`).
The differ's polymorphic key extraction handles string rule_ids
via the `unknown` fallback path — a conservative high-entropy key
keeps Semgrep findings stable across re-runs.

## Severity mapping

| Semgrep severity | Phase 1 severity |
|------------------|------------------|
| ERROR | block |
| WARNING | warn |
| INFO | info |

## Performance

Semgrep typically runs in ~5 seconds per package for the 7-rule
starter set. On a 20-package audit run, that's 100s additional —
considered acceptable for the precision boost. Parallelism via
the `run_all_rules` master loop (rules are already backgrounded).

## When NOT to enable Semgrep

- CI environments where install adds >2 minutes — pin a Docker image
  in CI rather than installing fresh each run.
- Codebases with non-standard Elixir dialects (Phoenix LiveView
  HEEx templates inside `.ex` strings) — Semgrep's Elixir parser
  may stumble. Native rules don't care about embedded HEEx.

## Future ruleset growth

The starter set covers the highest-precision wins. Additions in
priority order:

1. Module-attribute persistence of decoded payloads (cross-line
   data-flow).
2. `:os.cmd` and `Port.open` in compile-time contexts.
3. ETF (Erlang term format) literal patterns in source.
4. `Cachex.put_or_create` with dynamic module names.

Each new rule MUST land alongside a synthetic fixture in
`smoke-test/fixtures.d/` plus an entry in this file's table.
