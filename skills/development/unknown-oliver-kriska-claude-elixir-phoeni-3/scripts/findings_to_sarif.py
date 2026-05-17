#!/usr/bin/env python3
"""
findings_to_sarif.py — emit SARIF 2.1.0 from phx-deps-audit NDJSON.

Reads one NDJSON file (Phase 2 `new_signals.jsonl` by default; supply
`findings.jsonl` when running --no-differential), writes a SARIF log
to the path given as the second argument.

Each input line is a JSON object with at minimum: rule_id, severity,
optionally: file, line, snippet, message, package, version,
previous_version, differential.

Usage:
    python3 findings_to_sarif.py <findings.jsonl> <out.sarif> [--plugin-version 3.0.0]

Output: SARIF 2.1.0 JSON conforming to
    https://json.schemastore.org/sarif-2.1.0.json
"""

import argparse
import json
import sys
from pathlib import Path

LEVELS = {"block": "error", "warn": "warning", "info": "note"}
KINDS = {"block": "fail", "warn": "fail", "info": "informational"}

RULE_DESCRIPTIONS = {
    1: ("BidiUnicodeControlChar", "Bidi Unicode control char in source",
        "Detects directional-override Unicode control characters in source files (Trojan Source CVE-2021-42574)."),
    2: ("DynamicEvalAtModuleScope", "Code.eval_* or :erlang.apply with non-literal MFA",
        "Detects evaluator calls with runtime-determined target at module scope."),
    3: ("CompileTimeShellExec", "System.cmd / :os.cmd / Port.open at compile time",
        "Detects shell-exec calls in compile-time macros."),
    4: ("UnsafeBinaryToTerm", ":erlang.binary_to_term/1 on literal without :safe",
        "Detects unsafe deserialization without the :safe option."),
    5: ("NewNonHexDep", "New :git or :path dep in mix.exs",
        "Detects dependencies that bypass the Hex registry."),
    6: ("MaintainerChange", "Maintainer change between versions",
        "Detects Hex package ownership change between the audited and previous version."),
    7: ("LargeBase64Blob", "Base64 blob >256 chars outside priv/static/, test/fixtures/, assets/",
        "Detects suspiciously large base64 strings in source."),
    8: ("TyposquatCandidate", "Typosquat candidate (Levenshtein + download delta)",
        "Detects packages with names ≤2 edits from top-500 and >1000x download delta."),
}


def rule_definition(rule_id: int) -> dict:
    name, short, full = RULE_DESCRIPTIONS.get(
        rule_id,
        (f"Rule{rule_id}", f"Rule {rule_id}", f"phx-deps-audit rule {rule_id}"),
    )
    return {
        "id": f"phx-deps-audit/rule-{rule_id}",
        "name": name,
        "shortDescription": {"text": short},
        "fullDescription": {"text": full},
        "helpUri": (
            "https://github.com/oliver-kriska/claude-elixir-phoenix/blob/main/"
            f"plugins/elixir-phoenix/skills/deps-audit/references/heuristics.md#rule-{rule_id}"
        ),
        "defaultConfiguration": {"level": "error"},
    }


def finding_to_result(f: dict) -> dict:
    rule_id = f["rule_id"]
    severity = f.get("severity", "warn")
    package = f.get("package", "")
    version = f.get("version", "")

    region = {"startLine": int(f.get("line") or 1)}
    if f.get("snippet"):
        region["snippet"] = {"text": f["snippet"]}

    loc = {
        "physicalLocation": {
            "artifactLocation": {"uri": f.get("file") or "mix.exs"},
            "region": region,
        }
    }
    if package:
        loc["logicalLocations"] = [
            {"name": package, "kind": "package"},
            {"name": version, "kind": "version"},
        ]

    return {
        "ruleId": f"phx-deps-audit/rule-{rule_id}",
        "level": LEVELS.get(severity, "warning"),
        "kind": KINDS.get(severity, "fail"),
        "message": {"text": f.get("message") or RULE_DESCRIPTIONS.get(rule_id, ("", "", ""))[1]},
        "locations": [loc],
        "properties": {
            "package": package,
            "version": version,
            "previous_version": f.get("previous_version", ""),
            "differential": f.get("differential", "new"),
        },
    }


def load_ndjson(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    with path.open() as fh:
        for raw in fh:
            raw = raw.strip()
            if not raw:
                continue
            out.append(json.loads(raw))
    return out


def build_sarif(findings: list[dict], plugin_version: str) -> dict:
    rule_ids = sorted({f["rule_id"] for f in findings})
    return {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "phx-deps-audit",
                        "version": plugin_version,
                        "informationUri": "https://github.com/oliver-kriska/claude-elixir-phoenix",
                        "rules": [rule_definition(rid) for rid in rule_ids],
                    }
                },
                "results": [finding_to_result(f) for f in findings],
            }
        ],
    }


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="Convert phx-deps-audit NDJSON to SARIF 2.1.0")
    p.add_argument("findings", type=Path, help="NDJSON findings file")
    p.add_argument("out", type=Path, help="SARIF output path")
    p.add_argument("--plugin-version", default="3.0.0", help="Plugin version for tool.driver.version")
    args = p.parse_args(argv)

    findings = load_ndjson(args.findings)
    sarif = build_sarif(findings, args.plugin_version)
    args.out.write_text(json.dumps(sarif, indent=2) + "\n")
    print(f"sarif: {len(findings)} findings → {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
