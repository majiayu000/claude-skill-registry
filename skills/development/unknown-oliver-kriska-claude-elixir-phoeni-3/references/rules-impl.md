# MVP Rule Implementations

Eight detection routines. Each emits zero or more findings as
NDJSON lines (one JSON object per line) to the file named by
`${FINDINGS_FILE}` (defaults to
`${AUDIT_TMPDIR}/findings.jsonl`). The renderer aggregates by
package.

## Portability floor

Every new native regex rule MUST use **perl**, not `grep -P` or
`grep -E '{n,}'` for n > 255. macOS ships BSD grep, which:

- Lacks `-P` (no PCRE — Unicode character classes don't work).
- Caps interval quantifier `{n,}` at 255.

Perl is preinstalled on every supported platform (macOS, Linux, WSL,
Alpine via `apk add perl`). Treat perl as the cross-platform floor —
even Linux GNU-grep environments work without change.

Same applies to `comm` and `diff` for differential mode: BSD `comm`
requires pre-sorted inputs and BSD `diff` lacks `--no-dereference`.
Prefer Python (`scripts/diff_findings.py`) or jq for diffs.

## Common finding shape

```json
{"pkg": "phoenix", "version": "1.7.20", "rule_id": 3, "severity": "block",
 "file": "lib/foo.ex", "line": 14, "snippet": "System.cmd(\"curl\", url)",
 "message": "System.cmd called at module top level"}
```

`file` and `line` are nullable (for package-level findings like Rule 6).
`snippet` is truncated to 200 chars.

## Helper: emit a finding

```bash
emit() {
  jq -n -c \
    --arg pkg "$1" --arg version "$2" --argjson rule_id "$3" \
    --arg severity "$4" --arg file "$5" --arg line "$6" \
    --arg snippet "$7" --arg message "$8" \
    '{pkg:$pkg, version:$version, rule_id:$rule_id, severity:$severity,
      file:($file|select(.!="")), line:(if $line=="" then null else ($line|tonumber) end),
      snippet:$snippet, message:$message}' \
    >> "${FINDINGS_FILE:-${AUDIT_TMPDIR}/findings.jsonl}"
}
```

All rules below assume `$pkg` and `$ver` are set and `$tarball_dir` points
to the unpacked NEW version (e.g.,
`${AUDIT_TMPDIR}/tarballs/phoenix/1.7.20/`).

---

## Rule 1 — Bidi Unicode control chars (BLOCK)

CVE-2021-42574 Trojan Source. Grep for the 9 directional-override control
chars across all source files in the unpacked tarball.

```bash
rule_1_bidi() {
  local pkg="$1" ver="$2" dir="$3"
  # PUA + bidi overrides: U+202A..U+202E, U+2066..U+2069, U+200E, U+200F, U+061C.
  # macOS BSD grep lacks -P (PCRE), so use perl for Unicode classes.
  find "${dir}" \( -name '*.ex' -o -name '*.exs' -o -name '*.erl' \) -print0 \
  | xargs -0 perl -CSD -ne '
      if (/[\x{202A}-\x{202E}\x{2066}-\x{2069}\x{200E}\x{200F}\x{061C}]/) {
        chomp; printf("%s\x1f%s\x1f%s\n", $ARGV, $., $_);
      }
    ' 2>/dev/null \
  | while IFS=$'\x1f' read -r file line snippet; do
      emit "${pkg}" "${ver}" 1 "block" \
        "${file#${dir}/}" "${line}" "${snippet:0:200}" \
        "Bidi/directional Unicode control char in source (Trojan Source CVE-2021-42574)"
    done
}
```

**FP rate:** ~0%. Legit uses of bidi chars in code source are exceedingly
rare; localization strings live in `.po` files (not scanned).

---

## Rule 2 — `Code.eval_*` / `:erlang.apply` non-literal at module scope (BLOCK)

Detects dynamic code evaluation called outside a function body. Uses
`Code.string_to_quoted/2` to get an AST and walks it.

```bash
rule_2_eval() {
  local pkg="$1" ver="$2" dir="$3"

  find "${dir}" -name '*.ex' -o -name '*.exs' | while read -r file; do
    mix run --no-deps-check --no-compile -e "
      path = System.argv() |> List.first()
      {:ok, ast} = path |> File.read!() |> Code.string_to_quoted(file: path, columns: true)

      scan = fn ast, scan ->
        case ast do
          # def/defp/defmacro body — skip subtree (function-scope eval is fine)
          {form, _, _} when form in [:def, :defp, :defmacro, :defmacrop] -> :ok

          # Top-level eval — flag
          {{:., _, [{:__aliases__, _, [:Code]}, op]}, meta, [arg | _]}
              when op in [:eval_string, :eval_quoted] ->
            unless is_binary(arg) and op == :eval_string and String.length(arg) < 5 do
              IO.puts(\"#{meta[:line]}|Code.#{op}|non-literal eval at module scope\")
            end

          # :erlang.apply with non-literal MFA
          {{:., _, [:erlang, :apply]}, meta, [m, _f, _a]} when not is_atom(m) ->
            IO.puts(\"#{meta[:line]}|:erlang.apply|dynamic MFA at module scope\")

          {_, _, children} when is_list(children) -> Enum.each(children, &scan.(&1, scan))
          list when is_list(list) -> Enum.each(list, &scan.(&1, scan))
          _ -> :ok
        end
      end
      scan.(ast, scan)
    " -- "${file}" 2>/dev/null \
    | while IFS='|' read -r line snippet message; do
        emit "${pkg}" "${ver}" 2 "block" \
          "${file#${dir}/}" "${line}" "${snippet}" "${message}"
      done
  done
}
```

**FP rate:** ~1%. Legit eval at module scope is almost never seen; macros
that build code use `quote do ... end`, not `Code.eval_string`.

---

## Rule 3 — `System.cmd` / `:os.cmd` / `Port.open` at compile time (BLOCK)

Compile-time means: inside `defmacro`, `__before_compile__`,
`__after_compile__`, or at the module top level. Same AST walk as Rule 2,
different match patterns.

```bash
rule_3_compile_exec() {
  local pkg="$1" ver="$2" dir="$3"

  find "${dir}" -name '*.ex' -o -name '*.exs' | while read -r file; do
    mix run --no-deps-check --no-compile -e "
      path = System.argv() |> List.first()
      {:ok, ast} = path |> File.read!() |> Code.string_to_quoted(file: path, columns: true)

      scan = fn ast, in_compile, scan ->
        case ast do
          # entering a function body — out of compile scope
          {form, _, _} = node when form in [:def, :defp] -> :ok

          # entering a compile-time callback
          {form, _, children} when form in [:defmacro, :defmacrop] and is_list(children) ->
            Enum.each(children, &scan.(&1, true, scan))

          {:__before_compile__, _, _} -> Enum.each(elem(ast, 2) || [], &scan.(&1, true, scan))
          {:__after_compile__, _, _}  -> Enum.each(elem(ast, 2) || [], &scan.(&1, true, scan))

          # System.cmd / :os.cmd / Port.open at compile scope
          {{:., _, [{:__aliases__, _, [:System]}, :cmd]}, m, _} when in_compile ->
            IO.puts(\"#{m[:line]}|System.cmd|System.cmd at compile time\")
          {{:., _, [:os, :cmd]}, m, _} when in_compile ->
            IO.puts(\"#{m[:line]}|:os.cmd|:os.cmd at compile time\")
          {{:., _, [{:__aliases__, _, [:Port]}, :open]}, m, _} when in_compile ->
            IO.puts(\"#{m[:line]}|Port.open|Port.open at compile time\")

          {_, _, children} when is_list(children) ->
            Enum.each(children, &scan.(&1, in_compile, scan))
          list when is_list(list) -> Enum.each(list, &scan.(&1, in_compile, scan))
          _ -> :ok
        end
      end

      # Top-level expressions in a module body run at compile time
      scan.(ast, true, scan)
    " -- \"${file}\" 2>/dev/null \
    | while IFS='|' read -r line snippet message; do
        emit \"${pkg}\" \"${ver}\" 3 \"block\" \
          \"${file#${dir}/}\" \"${line}\" \"${snippet}\" \"${message}\"
      done
  done
}
```

**FP rate:** ~3%. Some legit build-tool packages (`make`-style wrappers)
shell out at compile time. Manual review needed when flagged.

---

## Rule 4 — `:erlang.binary_to_term/1` on literal without `:safe` (BLOCK)

Unsafe deserialization (CVE-2026-21619 in hex_core itself). Detect calls to
`:erlang.binary_to_term/1` without `[:safe]` in the second arg.

```bash
rule_4_binary_to_term() {
  local pkg="$1" ver="$2" dir="$3"

  find "${dir}" -name '*.ex' -o -name '*.exs' | while read -r file; do
    mix run --no-deps-check --no-compile -e "
      path = System.argv() |> List.first()
      {:ok, ast} = path |> File.read!() |> Code.string_to_quoted(file: path, columns: true)

      scan = fn ast, scan ->
        case ast do
          # arity-1: no opts at all
          {{:., _, [:erlang, :binary_to_term]}, m, [_]} ->
            IO.puts(\"#{m[:line]}|:erlang.binary_to_term/1|missing :safe option\")

          # arity-2: opts present but :safe not in list
          {{:., _, [:erlang, :binary_to_term]}, m, [_, opts]} when is_list(opts) ->
            unless :safe in opts do
              IO.puts(\"#{m[:line]}|:erlang.binary_to_term/2|:safe not in opts\")
            end

          {_, _, children} when is_list(children) -> Enum.each(children, &scan.(&1, scan))
          list when is_list(list) -> Enum.each(list, &scan.(&1, scan))
          _ -> :ok
        end
      end
      scan.(ast, scan)
    " -- \"${file}\" 2>/dev/null \
    | while IFS='|' read -r line snippet message; do
        emit \"${pkg}\" \"${ver}\" 4 \"block\" \
          \"${file#${dir}/}\" \"${line}\" \"${snippet}\" \"${message}\"
      done
  done
}
```

**FP rate:** ~2%. Internal serialization formats sometimes pass trusted
binaries — but those should still use `:safe`. The fix is one keyword.

---

## Rule 5 — New `:git` / `:path` dep in `mix.exs` (BLOCK)

Diff `deps/0` between OLD and NEW versions. Flag any new entry that uses
`:git:` or `:path:` (not `:hex` — hex is the trusted default).

```bash
rule_5_new_git_path() {
  local pkg="$1" ver="$2" new_dir="$3" old_dir="$4"

  [ -z "${old_dir}" ] && return 0   # no old version → skip diff rule

  extract_deps() {
    mix run --no-deps-check --no-compile -e "
      path = System.argv() |> List.first()
      {:ok, ast} = File.read!(path) |> Code.string_to_quoted()

      # locate deps/0 in module body
      deps = Macro.prewalk(ast, [], fn
        {:def, _, [{:deps, _, _} | _]} = node, acc -> {node, [node | acc]}
        other, acc -> {other, acc}
      end) |> elem(1) |> List.first()

      case deps do
        nil -> :ok
        {:def, _, [_head, [do: {:__block__, _, _} | _]]} -> :ok  # unusual
        {:def, _, [_head, [do: list]]} when is_list(list) ->
          for entry <- list do
            case entry do
              {dep, _, opts} when is_atom(dep) and is_list(opts) ->
                cond do
                  Keyword.has_key?(opts, :git) -> IO.puts(\"#{dep}|git|#{inspect(opts[:git])}\")
                  Keyword.has_key?(opts, :path) -> IO.puts(\"#{dep}|path|#{inspect(opts[:path])}\")
                  true -> :ok
                end
              _ -> :ok
            end
          end
        _ -> :ok
      end
    " -- "${1}" 2>/dev/null
  }

  local old_deps new_deps
  old_deps=$(extract_deps "${old_dir}/mix.exs" 2>/dev/null || true)
  new_deps=$(extract_deps "${new_dir}/mix.exs" 2>/dev/null || true)

  # New entries = in new_deps but not in old_deps
  comm -13 <(echo "${old_deps}" | sort -u) <(echo "${new_deps}" | sort -u) \
  | while IFS='|' read -r dep kind src; do
      [ -z "${dep}" ] && continue
      emit "${pkg}" "${ver}" 5 "block" \
        "mix.exs" "" "{:${dep}, ${kind}: ${src}}" \
        "New ${kind} dep added vs old version — bypasses Hex's checksumming"
    done
}
```

**FP rate:** ~5%. Some libraries legit use `:git` for transitive forks
(e.g., a pinned `phoenix_html` fork). Manual review acceptable.

---

## Rule 6 — Maintainer change between versions (BLOCK)

Implemented in `references/hex-api.md` as `maintainer_change()`. Reproduced
here for completeness:

```bash
rule_6_maintainer_change() {
  local pkg="$1" old_ver="$2" new_ver="$3" ver="$4"

  [ -z "${old_ver}" ] && return 0

  local out
  out=$(maintainer_change "${pkg}" "${old_ver}" "${new_ver}")
  if [ -n "${out}" ]; then
    local message=$(echo "${out}" | cut -d'|' -f3)
    emit "${pkg}" "${ver}" 6 "block" \
      "" "" "${message}" "${message}"
  fi
}
```

Depends on Hex API `/api/packages/:name/releases/:version` returning a
`publisher.username` field. **FP rate:** ~2%.

---

## Rule 7 — Base64 blob > 256 chars outside allowlisted dirs (WARN)

Regex for long base64-ish strings, excluding `priv/static/`,
`test/fixtures/`, `assets/`, `node_modules/` (if vendored).

```bash
rule_7_base64() {
  local pkg="$1" ver="$2" dir="$3"

  # macOS BSD grep caps repetition count at 255; use perl for the >=256 match.
  find "${dir}" \( -name '*.ex' -o -name '*.exs' \) \
    -not -path '*/priv/*' -not -path '*/test/*' \
    -not -path '*/assets/*' -not -path '*/node_modules/*' -print0 \
  | xargs -0 perl -ne '
      if (/"[A-Za-z0-9+\/]{256,}={0,2}"/) {
        chomp; my $s = substr($_, 0, 200);
        printf("%s\x1f%s\x1f%s\n", $ARGV, $., $s);
      }
    ' 2>/dev/null \
  | while IFS=$'\x1f' read -r file line snippet; do
      emit "${pkg}" "${ver}" 7 "warn" \
        "${file#${dir}/}" "${line}" "${snippet}" \
        "Base64-like string literal >256 chars outside priv/static, test/fixtures, assets/"
    done
}
```

**Portability note:** Rules 1 and 7 use perl instead of `grep -P` /
`grep -E '{256,}'` because (a) macOS BSD grep lacks `-P`, and (b) BSD grep
caps `{n,}` at 255. Linux GNU grep handles both natively, but perl works
identically on both — net win.

**FP rate:** ~8%. License headers, embedded SVG/PNG, fixture data. Bump
threshold to 512 if too noisy in real use. The directory exclude list
catches the most common legit cases.

---

## Rule 8 — Typosquat (Levenshtein ≤ 2 + 1000× download delta) (BLOCK)

Implemented in `references/hex-api.md` as `typosquat_check()`. Reproduced:

```bash
rule_8_typosquat() {
  local pkg="$1" ver="$2"

  typosquat_check "${pkg}" \
  | while IFS='|' read -r sev rule message; do
      [ -z "${sev}" ] && continue
      emit "${pkg}" "${ver}" 8 "block" \
        "" "" "${message}" "${message}"
    done
}
```

Depends on the top-500 cache (fetched daily) and per-package download
counts. **FP rate:** ~1%.

---

## Master runner

```bash
run_all_rules() {
  # Phase 2 differential mode: emit NEW findings to findings.jsonl AND
  # OLD findings to findings.old.jsonl in the same loop. When DIFFERENTIAL=0,
  # behave like Phase 1 (no OLD pass).
  : > ${AUDIT_TMPDIR}/findings.jsonl
  : > ${AUDIT_TMPDIR}/findings.old.jsonl

  local differential="${DIFFERENTIAL:-1}"

  jq -c '.changed[], .added[]' ${AUDIT_TMPDIR}/diff.json \
  | while IFS= read -r row; do
      pkg=$(echo "${row}" | jq -r '.[0]')
      old=$(echo "${row}" | jq -r '.[1]')
      new=$(echo "${row}" | jq -r '.[2]')
      [ "${new}" = "null" ] && continue

      new_dir="${AUDIT_TMPDIR}/tarballs/${pkg}/${new}"
      old_dir=""
      [ "${old}" != "null" ] && old_dir="${AUDIT_TMPDIR}/tarballs/${pkg}/${old}"

      # --- NEW pass: emit to findings.jsonl ---
      FINDINGS_FILE="${FINDINGS_FILE:-${AUDIT_TMPDIR}/findings.jsonl}" \
        rule_1_bidi              "${pkg}" "${new}" "${new_dir}" &
      FINDINGS_FILE="${FINDINGS_FILE:-${AUDIT_TMPDIR}/findings.jsonl}" \
        rule_2_eval              "${pkg}" "${new}" "${new_dir}" &
      FINDINGS_FILE="${FINDINGS_FILE:-${AUDIT_TMPDIR}/findings.jsonl}" \
        rule_3_compile_exec      "${pkg}" "${new}" "${new_dir}" &
      FINDINGS_FILE="${FINDINGS_FILE:-${AUDIT_TMPDIR}/findings.jsonl}" \
        rule_4_binary_to_term    "${pkg}" "${new}" "${new_dir}" &
      FINDINGS_FILE="${FINDINGS_FILE:-${AUDIT_TMPDIR}/findings.jsonl}" \
        rule_7_base64            "${pkg}" "${new}" "${new_dir}" &
      wait

      # --- OLD pass (differential mode): emit to findings.old.jsonl ---
      if [ "${differential}" = "1" ] && [ -n "${old_dir}" ] && [ -d "${old_dir}" ]; then
        FINDINGS_FILE=${AUDIT_TMPDIR}/findings.old.jsonl \
          rule_1_bidi              "${pkg}" "${old}" "${old_dir}" &
        FINDINGS_FILE=${AUDIT_TMPDIR}/findings.old.jsonl \
          rule_2_eval              "${pkg}" "${old}" "${old_dir}" &
        FINDINGS_FILE=${AUDIT_TMPDIR}/findings.old.jsonl \
          rule_3_compile_exec      "${pkg}" "${old}" "${old_dir}" &
        FINDINGS_FILE=${AUDIT_TMPDIR}/findings.old.jsonl \
          rule_4_binary_to_term    "${pkg}" "${old}" "${old_dir}" &
        FINDINGS_FILE=${AUDIT_TMPDIR}/findings.old.jsonl \
          rule_7_base64            "${pkg}" "${old}" "${old_dir}" &
        wait
      fi

      # Diff rules (intrinsically diff-aware — single pass).
      rule_5_new_git_path      "${pkg}" "${new}" "${new_dir}" "${old_dir}"

      # Hex API rules — package-scoped, not differential.
      rule_6_maintainer_change "${pkg}" "${old}" "${new}" "${new}"
      rule_8_typosquat         "${pkg}" "${new}"
    done

  # Set-subtract NEW vs OLD into new_signals / info_signals / dropped_signals.
  if [ "${differential}" = "1" ]; then
    python3 "${CLAUDE_SKILL_DIR}/scripts/diff_findings.py" \
      --new  ${AUDIT_TMPDIR}/findings.jsonl \
      --old  ${AUDIT_TMPDIR}/findings.old.jsonl \
      --new-out     ${AUDIT_TMPDIR}/new_signals.jsonl \
      --info-out    ${AUDIT_TMPDIR}/info_signals.jsonl \
      --dropped-out ${AUDIT_TMPDIR}/dropped_signals.jsonl
  fi
}
```

`FINDINGS_FILE` defaults to `findings.jsonl` for backward compat. The
`emit()` helper at the top of this file must be updated to redirect to
`${FINDINGS_FILE}` instead of the hard-coded path — that's a one-line
change inside `emit()`.

## Anti-FP notes

- **Rule 7 (base64)** is the dominant noise source. Always include `priv/`
  in the exclude list. Bumping threshold to 512 chars drops most legit
  embedded SVG.
- **Rules 2 + 3** rely on `Code.string_to_quoted/2` — files with syntax
  errors silently skip. This is acceptable (the package wouldn't compile
  anyway). Log skipped files in `--verbose` mode for debugging.
- **Rule 5** trips on `:path` deps used for monorepo umbrella apps. The
  intent of the rule is "dep added that bypasses Hex" — manual approval
  is reasonable when the user knows the path dep.

## Phase 2 additions

- **Differential mode** — `DIFFERENTIAL=1` (default) emits findings on
  OLD as well as NEW, then NDJSON set-subtracts via
  `scripts/diff_findings.py`. See `differential.md`.
- **Optional precision layers** — `semgrep --config priv/semgrep/` and
  `yara -r priv/yara/` run alongside native rules when available; both
  are soft deps. See `semgrep.md` and `yara.md`.
- **LLM triage** — high-score packages get verdicts via the
  `hex-deps-triager` sonnet agent with a `context-supervisor` (haiku)
  consolidating per-package output. See `llm-triage.md`.

## Out of scope (Phase 3+)

- Sourceror dependency for richer AST patterns (currently using built-in
  `Code.string_to_quoted/2`).
- Sobelow on unpacked tarballs (would cover Rules 2–4 with stronger taint
  analysis).
- Multi-agent orchestrator (5 specialist auditors) — Phase 2 native +
  Semgrep + YARA cover MVP.
- PreToolUse hook on `mix deps.get` — needs Phase 2 ledger to be solid.
