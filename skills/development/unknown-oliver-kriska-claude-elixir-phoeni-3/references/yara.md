# YARA byte-pattern layer — optional defense in depth

YARA scans unpacked tarballs for byte-pattern signatures that are
cheaper to detect as byte-scans than as AST walks: large base64
blobs, embedded BEAM bytecode, gzip/zip magic in source files,
cross-ecosystem attack signatures translated from npm.

## Iron Laws

1. **SOFT DEPENDENCY.** If `yara` is absent, skip the layer with an
   install hint to stderr. Never block the audit on its absence.
2. **DEFENSE IN DEPTH.** YARA findings stack on native + Semgrep
   findings. Cross-ecosystem signatures (event-stream, flatmap-stream,
   XZ-style magic) live here precisely because AST detectors don't
   see byte patterns inside string literals.
3. **`yara` IS THE ONLY SUPPORTED BINARY.** Not `yara-x` (Rust port,
   different rule semantics). The plugin's starter rules target
   YARA 4.x. Test compatibility before swapping engines.
4. **NORMALIZE TO PHASE 1 SHAPE.** YARA findings parse into NDJSON
   with `rule_id` namespaced as `yara/<rule_name>`. Severity comes
   from the rule's `meta.severity` field.

## Starter rules — `priv/yara/hex-malware.yar`

The shipped starter file has 6 rules:

| Rule | Severity | Purpose |
|------|----------|---------|
| `large_base64_blob` | warn | Base64 ≥256 chars — faster than perl regex |
| `beam_magic_in_source` | block | BEAM bytecode magic `FOR1` inside source |
| `gzip_magic_in_source` | warn | Gzip magic — embedded payload |
| `zip_magic_in_source` | warn | Zip magic — embedded payload |
| `event_stream_flatmap_signature` | warn | npm event-stream attack literal |
| `curl_attacker_pattern` | warn | curl + http:// (non-TLS) URL pattern |

All rules emit through the metadata's `rule_id` and `severity`
fields so the parser stays generic.

## Subprocess invocation

```bash
run_yara() {
  local tarball_dir="$1"
  command -v yara >/dev/null 2>&1 || {
    echo "yara: not installed (skipping). Install via 'brew install yara'." >&2
    return 0
  }
  # -r recursive, -s show matched strings, -m show metadata.
  yara -r -s -m \
    "${CLAUDE_SKILL_DIR}/priv/yara/hex-malware.yar" \
    "${tarball_dir}" 2>/dev/null \
  | parse_yara_output_to_ndjson
}

parse_yara_output_to_ndjson() {
  # YARA output format (line-oriented):
  #   <rule_name> [meta1="val",meta2="val"] <file_path>
  #   0x<offset>:$<string_id>: <string_content>
  #
  # Group rule + per-match lines; emit one NDJSON per match.
  local current_rule="" current_file="" current_meta="{}"
  while IFS= read -r line; do
    if [[ "${line}" =~ ^([a-z_][a-z0-9_]*)\ \[(.+)\]\ (.+)$ ]]; then
      current_rule="${BASH_REMATCH[1]}"
      current_meta="${BASH_REMATCH[2]}"
      current_file="${BASH_REMATCH[3]}"
    elif [[ "${line}" =~ ^0x[0-9a-f]+: ]]; then
      # severity comes from metadata 'severity="..."'.
      local severity=warn
      [[ "${current_meta}" =~ severity=\"([^\"]+)\" ]] && severity="${BASH_REMATCH[1]}"
      jq -n -c \
        --arg pkg "${PKG}" --arg version "${VER}" \
        --arg rule_id "yara/${current_rule}" \
        --arg severity "${severity}" \
        --arg file "${current_file}" \
        --arg snippet "${line:0:200}" \
        --arg message "YARA: ${current_rule}" \
        '{pkg:$pkg, version:$version, rule_id:$rule_id, severity:$severity,
          file:$file, line:null, snippet:$snippet, message:$message}' \
      >> "${FINDINGS_FILE:-${AUDIT_TMPDIR}/findings.jsonl}"
    fi
  done
}
```

YARA emits `file:line` only for hex offsets, not source lines —
matches get `line: null`. The renderer handles null line numbers (it
already does for Rules 6 + 8).

## Severity from metadata

YARA's compiled rules don't carry severity natively. We use a
`meta.severity` string ("block" / "warn" / "info") parsed by the
NDJSON normalizer. Rules without a severity meta default to "warn".

## Performance

YARA is fast — typical run is <500ms per package for the starter
set. Negligible vs. the 5s Semgrep adds. Both layers can run in
parallel with the native rule loop via shell backgrounding.

## When NOT to enable YARA

- Air-gapped CI without `yara` installed and no network to fetch it
  — let the soft-dep skip take care of it.
- Codebases with large legitimate binary blobs (e.g., embedded
  graphics in `priv/static/`). YARA's magic-byte rules trip on
  those — the existing path-exclude logic (skip `priv/`, `assets/`,
  `test/fixtures/`) should cover it, but verify on first run.

## Rule growth roadmap

1. **XZ-style backdoor markers** — pull from public IoC feeds when
   YARA-format rules become available.
2. **Macro-bytecode in string literals** — Erlang `.beam` magic
   variants beyond the `FOR1` header.
3. **Reflection-loader strings** — `:code.load_binary`,
   `Module.create` with non-literal args (also caught by AST rules,
   but cheaper here for first-pass triage).

Each new rule MUST have a synthetic fixture in
`smoke-test/fixtures.d/` + an entry in the table above.
