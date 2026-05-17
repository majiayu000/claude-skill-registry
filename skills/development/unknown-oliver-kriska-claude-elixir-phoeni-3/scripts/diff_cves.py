#!/usr/bin/env python3
"""
diff_cves.py — CVE set difference for /phx:deps-audit differential pass.

Reads cves_old.json and cves_new.json (produced by mix_audit_diff in
references/external-tools.md) and categorizes CVEs into three sets:

  - patched:       in OLD, not in NEW (the security changelog)
  - introduced:    in NEW, not in OLD (regression — block)
  - still_exposed: in both           (didn't fix it — block)

Input shape (mix_audit JSON):

    {
      "pass": false,
      "vulnerabilities": [
        {
          "advisory": {
            "id": "GHSA-xxxx-xxxx-xxxx",
            "cve": "CVE-2026-12345",
            "title": "...",
            "description": "...",
            "severity": "high",
            "patched_versions": "~> 1.2.3",
            "disclosure_date": "2026-05-07"  // optional
          },
          "dependency": {"package": "decimal", "version": "2.3.0"}
        }
      ]
    }

Keying: (ghsa_id, package). Version is intentionally NOT part of the
key — a CVE that affected OLD 2.3.0 and ALSO affects NEW 2.4.0 is
"still exposed", regardless of version drift.

Output (NDJSON, one finding per line):

    {
      "category": "patched" | "introduced" | "still_exposed",
      "rule_id": "ext:mix-audit:diff",
      "severity": "block" | "warn" | "info",
      "ghsa_id": "GHSA-xxxx-xxxx-xxxx",
      "cve_id": "CVE-2026-12345",
      "package": "decimal",
      "old_version": "2.3.0",     // null when category == "introduced"
      "new_version": "3.1.0",     // null when category == "patched"
      "severity_label": "high",
      "title": "Decimal DoS via unbounded exponent",
      "disclosed_at": "2026-05-07",
      "exposure_days": 5,
      "message": "decimal 2.3.0 → 3.1.0: CVE-2026-32686 (high) ..."
    }

Severity mapping per category:
  - patched     → info  (informational — the update is the fix)
  - introduced  → block (the update regressed security)
  - still_exposed → block (update didn't address the CVE)

The renderer (references/output-renderer.md) lifts patched findings to
the headline section despite their low severity.

Usage:
    python3 diff_cves.py \\
      --old cves_old.json \\
      --new cves_new.json \\
      --out diff_cves.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable


def _normalize_severity(raw: str | None) -> str:
    if not raw:
        return "moderate"
    s = raw.lower().strip()
    if s in {"critical"}:
        return "critical"
    if s in {"high"}:
        return "high"
    if s in {"medium", "moderate"}:
        return "moderate"
    if s in {"low"}:
        return "low"
    return s


def _patched_severity(category: str, raw_sev: str) -> str:
    """Map mix_audit severity → deps-audit severity per category.

    patched     → info  (the update IS the fix; informational)
    introduced  → block (regression — block the update)
    still_exposed → block (didn't fix it — block until further update)
    """
    if category == "patched":
        return "info"
    if raw_sev in {"critical", "high"}:
        return "block"
    if raw_sev == "moderate":
        return "warn"
    return "info"


def _key(vuln: dict[str, Any]) -> tuple[str, str]:
    advisory = vuln.get("advisory", {}) or {}
    dependency = vuln.get("dependency", {}) or {}
    ghsa_id = advisory.get("id") or advisory.get("cve") or ""
    package = dependency.get("package") or ""
    return (ghsa_id, package)


def _exposure_days(disclosed_at: str | None) -> int | None:
    if not disclosed_at:
        return None
    try:
        d = datetime.strptime(disclosed_at, "%Y-%m-%d").date()
    except ValueError:
        return None
    delta = date.today() - d
    return max(delta.days, 0)


def _load_vulns(path: Path | None) -> list[dict[str, Any]]:
    if path is None or not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"diff_cves: invalid JSON in {path}: {e}", file=sys.stderr)
        return []
    if isinstance(data, list):
        return data  # already a list of vulns
    return data.get("vulnerabilities", []) or []


def _build_finding(
    category: str,
    vuln_old: dict[str, Any] | None,
    vuln_new: dict[str, Any] | None,
) -> dict[str, Any]:
    # Prefer NEW for introduced/still_exposed (current state), OLD for
    # patched (what got fixed).
    primary = vuln_new if vuln_new and category != "patched" else (
        vuln_old or vuln_new or {}
    )
    advisory = primary.get("advisory", {}) or {}

    old_dep = (vuln_old or {}).get("dependency", {}) or {}
    new_dep = (vuln_new or {}).get("dependency", {}) or {}

    package = old_dep.get("package") or new_dep.get("package") or ""
    old_version = old_dep.get("version")
    new_version = new_dep.get("version")
    disclosed_at = advisory.get("disclosure_date") or advisory.get("disclosed_at")

    ghsa_id = advisory.get("id") or ""
    cve_id = advisory.get("cve") or ""
    raw_sev = _normalize_severity(advisory.get("severity"))
    severity = _patched_severity(category, raw_sev)
    title = advisory.get("title") or ""

    # Compose a human-readable message tailored per category.
    if category == "patched":
        message = (
            f"{package} {old_version} → {new_version}: "
            f"{cve_id or ghsa_id} ({raw_sev}) — {title}"
        )
    elif category == "introduced":
        message = (
            f"REGRESSION: {package} {new_version} introduces "
            f"{cve_id or ghsa_id} ({raw_sev}) — {title}"
        )
    else:  # still_exposed
        delta = (
            f"{old_version} → {new_version}"
            if old_version and new_version and old_version != new_version
            else (new_version or old_version or "")
        )
        message = (
            f"STILL EXPOSED: {package} {delta} remains vulnerable to "
            f"{cve_id or ghsa_id} ({raw_sev}) — {title}"
        )

    finding = {
        "category": category,
        "rule_id": "ext:mix-audit:diff",
        "severity": severity,
        "ghsa_id": ghsa_id,
        "cve_id": cve_id,
        "package": package,
        "old_version": old_version,
        "new_version": new_version,
        "severity_label": raw_sev,
        "title": title,
        "disclosed_at": disclosed_at,
        "exposure_days": _exposure_days(disclosed_at),
        "message": message,
    }
    return finding


def diff_cves(
    old: list[dict[str, Any]], new: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    old_by_key = {_key(v): v for v in old}
    new_by_key = {_key(v): v for v in new}

    findings: list[dict[str, Any]] = []

    for key, vuln in old_by_key.items():
        if not key[0]:  # skip vulns with no GHSA/CVE id
            continue
        if key in new_by_key:
            findings.append(_build_finding("still_exposed", vuln, new_by_key[key]))
        else:
            findings.append(_build_finding("patched", vuln, new_by_key.get(key)))

    for key, vuln in new_by_key.items():
        if not key[0]:
            continue
        if key not in old_by_key:
            findings.append(_build_finding("introduced", None, vuln))

    # Stable sort: patched first (headline), then introduced/still_exposed
    # (blockers), each group sorted by package then ghsa_id.
    category_order = {"patched": 0, "introduced": 1, "still_exposed": 2}
    findings.sort(
        key=lambda f: (category_order.get(f["category"], 9), f["package"], f["ghsa_id"])
    )
    return findings


def write_ndjson(path: Path, rows: Iterable[dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with path.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, separators=(",", ":")) + "\n")
            n += 1
    return n


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="CVE set difference for deps-audit")
    p.add_argument("--old", required=True, help="cves_old.json from mix_audit")
    p.add_argument("--new", required=True, help="cves_new.json from mix_audit")
    p.add_argument("--out", default="diff_cves.jsonl", help="NDJSON output path")
    p.add_argument(
        "--summary",
        action="store_true",
        help="print a one-line summary to stderr (count per category)",
    )
    args = p.parse_args(argv)

    old = _load_vulns(Path(args.old))
    new = _load_vulns(Path(args.new))
    findings = diff_cves(old, new)
    n = write_ndjson(Path(args.out), findings)

    if args.summary:
        counts = {"patched": 0, "introduced": 0, "still_exposed": 0}
        for f in findings:
            counts[f["category"]] = counts.get(f["category"], 0) + 1
        print(
            f"diff_cves: {n} findings — patched={counts['patched']} "
            f"introduced={counts['introduced']} "
            f"still_exposed={counts['still_exposed']}",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
