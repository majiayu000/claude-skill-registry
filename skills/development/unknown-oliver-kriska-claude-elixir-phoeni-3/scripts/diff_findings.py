#!/usr/bin/env python3
"""
diff_findings.py — NDJSON set-subtract for /phx:deps-audit differential mode.

Reads two findings.jsonl streams (NEW and OLD) and emits three NDJSON
streams: signals that are new in this version, signals shared across
both versions (downgraded to INFO), and signals dropped since OLD.

Keying is polymorphic per rule:

  - Rules 1, 2, 3, 4, 7 (file-scoped):
      (rule_id, file, fn_name, sha256(snippet)[:12])
  - Rule 5 (mix.exs dep diff):
      (rule_id, dep_name, kind)        # kind ∈ {git, path}
  - Rules 6, 8 (package-scoped):
      (rule_id, pkg)

Added-package mode: when --old is omitted or empty, every NEW finding is
emitted as a new signal (no subtraction). This matches Phase 1 behavior
and is the documented decision for net-new dependencies.

Cache invalidation: the caller is responsible for namespacing the cache
by a rules-checksum (sha256 of references/rules-impl.md mtime + commit
SHA). This script is content-pure and does not maintain its own cache.

Usage:
    python3 diff_findings.py --new findings.jsonl --old findings.old.jsonl \\
        --new-out new_signals.jsonl --info-out info_signals.jsonl \\
        --dropped-out dropped_signals.jsonl
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable


FILE_SCOPED_RULES = {1, 2, 3, 4, 7}
MIX_EXS_RULE = 5
PACKAGE_SCOPED_RULES = {6, 8}


def sha12(s: str) -> str:
    return hashlib.sha256((s or "").encode("utf-8")).hexdigest()[:12]


# Match `def`, `defp`, `defmacro`, `defmacrop` with their name. The AST
# walk in rule emitters is preferred (see `fn_name_for_line` notes in
# differential.md), but this regex walk is the portable fallback when no
# Elixir tooling is present.
_FN_DEF = re.compile(
    r"^\s*(?:def|defp|defmacro|defmacrop)\s+([a-z_][A-Za-z0-9_?!]*)"
)


def fn_name_for_line(source_lines: list[str], line_no: int) -> str:
    """Walk upward from line_no to find enclosing named function.

    Falls back to 'module_scope' for top-level code (no enclosing def)
    or 'anonymous' for code inside an anonymous fn. The differ favors
    stability over precision — even an approximate function name is a
    better stability anchor than line number alone.
    """
    if not source_lines or line_no < 1:
        return "module_scope"
    for i in range(min(line_no, len(source_lines)) - 1, -1, -1):
        m = _FN_DEF.match(source_lines[i])
        if m:
            return m.group(1)
    return "module_scope"


def finding_key(finding: dict[str, Any]) -> tuple:
    """Polymorphic key for set-subtraction.

    Phase 1 emitters do not write fn_name. When unset, we derive it
    cheaply from snippet text only — full AST walks happen in the
    rule layer, not here.
    """
    rule_id = finding.get("rule_id")
    if rule_id in FILE_SCOPED_RULES:
        snippet = finding.get("snippet", "") or ""
        fn_name = finding.get("fn_name") or _approx_fn_from_snippet(snippet)
        return (
            "file",
            rule_id,
            finding.get("file", ""),
            fn_name,
            sha12(snippet),
        )
    if rule_id == MIX_EXS_RULE:
        return (
            "mix",
            rule_id,
            finding.get("dep_name", "") or _dep_name_from_message(finding),
            finding.get("kind", "git"),
        )
    if rule_id in PACKAGE_SCOPED_RULES:
        return ("pkg", rule_id, finding.get("pkg", ""))
    # Unknown rule_id → fall back to a conservative high-entropy key so
    # diff never silently drops signals.
    return ("unknown", rule_id, json.dumps(finding, sort_keys=True))


def _approx_fn_from_snippet(snippet: str) -> str:
    m = _FN_DEF.match(snippet)
    return m.group(1) if m else "module_scope"


def _dep_name_from_message(finding: dict[str, Any]) -> str:
    # Rule 5 message format: 'new :git dep "phoenix_extras"'
    msg = finding.get("message", "") or ""
    m = re.search(r'"([a-z_][a-z0-9_]*)"', msg)
    return m.group(1) if m else ""


def load_ndjson(path: Path | None) -> list[dict[str, Any]]:
    if path is None or not path.exists():
        return []
    out: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for ln, raw in enumerate(fh, 1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                out.append(json.loads(raw))
            except json.JSONDecodeError as e:
                print(
                    f"diff_findings: skip {path}:{ln} (invalid JSON: {e})",
                    file=sys.stderr,
                )
    return out


def write_ndjson(path: Path, rows: Iterable[dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with path.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, separators=(",", ":")) + "\n")
            n += 1
    return n


def diff(
    new: list[dict[str, Any]], old: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    new_by_key = {finding_key(f): f for f in new}
    old_keys = {finding_key(f) for f in old}

    new_signals: list[dict[str, Any]] = []
    info_signals: list[dict[str, Any]] = []
    for key, f in new_by_key.items():
        if key in old_keys:
            downgraded = dict(f)
            downgraded["severity"] = "info"
            downgraded["differential"] = "carried"
            info_signals.append(downgraded)
        else:
            promoted = dict(f)
            promoted["differential"] = "new"
            new_signals.append(promoted)

    new_keys = set(new_by_key.keys())
    dropped = []
    for f in old:
        if finding_key(f) not in new_keys:
            d = dict(f)
            d["differential"] = "dropped"
            dropped.append(d)

    return new_signals, info_signals, dropped


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="NDJSON differential for deps-audit findings")
    p.add_argument("--new", required=True, help="findings.jsonl on NEW version")
    p.add_argument("--old", required=False, help="findings.old.jsonl on OLD version")
    p.add_argument("--new-out", default="new_signals.jsonl")
    p.add_argument("--info-out", default="info_signals.jsonl")
    p.add_argument("--dropped-out", default="dropped_signals.jsonl")
    p.add_argument(
        "--added-package-mode",
        choices=("emit-all", "skip"),
        default="emit-all",
        help="how to handle an absent --old (default: emit-all = Phase 1 behavior)",
    )
    args = p.parse_args(argv)

    new_path = Path(args.new)
    old_path = Path(args.old) if args.old else None

    new = load_ndjson(new_path)
    if old_path is None or not old_path.exists() or not load_ndjson(old_path):
        if args.added_package_mode == "skip":
            print(
                f"diff_findings: no OLD findings; --added-package-mode=skip → 0 signals",
                file=sys.stderr,
            )
            write_ndjson(Path(args.new_out), [])
            write_ndjson(Path(args.info_out), [])
            write_ndjson(Path(args.dropped_out), [])
            return 0
        all_new = [dict(f, differential="new") for f in new]
        write_ndjson(Path(args.new_out), all_new)
        write_ndjson(Path(args.info_out), [])
        write_ndjson(Path(args.dropped_out), [])
        print(
            f"diff_findings: no OLD; emitted {len(all_new)} signals as NEW",
            file=sys.stderr,
        )
        return 0

    old = load_ndjson(old_path)
    new_signals, info_signals, dropped = diff(new, old)
    n_new = write_ndjson(Path(args.new_out), new_signals)
    n_info = write_ndjson(Path(args.info_out), info_signals)
    n_dropped = write_ndjson(Path(args.dropped_out), dropped)
    print(
        f"diff_findings: {n_new} new, {n_info} carried/info, {n_dropped} dropped",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
