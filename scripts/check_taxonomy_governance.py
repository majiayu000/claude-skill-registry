#!/usr/bin/env python3
"""Validate canonical taxonomy governance rules."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from category_taxonomy import CategoryTaxonomy, load_taxonomy

REVIEW_NAME_TOKENS = {
    "applied",
    "core",
    "extended",
    "foundation",
    "misc",
    "other",
    "project",
    "specialized",
    "string",
    "template",
    "test",
    "utility",
}


@dataclass(frozen=True)
class GovernanceIssue:
    severity: str
    code: str
    category: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {
            "severity": self.severity,
            "code": self.code,
            "category": self.category,
            "message": self.message,
        }


def _slug_tokens(slug: str) -> set[str]:
    return {part for part in slug.split("-") if part}


def publish_category_issues(
    taxonomy: CategoryTaxonomy,
    categories: Iterable[str],
) -> list[GovernanceIssue]:
    issues: list[GovernanceIssue] = []
    for raw_category in sorted(
        {str(category) for category in categories if str(category)}
    ):
        slug = taxonomy.resolve(raw_category, allow_unknown=True)
        definition = taxonomy.categories.get(slug)
        if definition is None:
            issues.append(
                GovernanceIssue(
                    severity="error",
                    code="unknown-publish-category",
                    category=slug,
                    message="published category is not declared by the canonical taxonomy",
                )
            )
            continue
        if definition.status != "active":
            issues.append(
                GovernanceIssue(
                    severity="error",
                    code="noncanonical-publish-category",
                    category=slug,
                    message=(
                        "published category must be active in the canonical taxonomy"
                    ),
                )
            )
    return issues


def build_report(
    taxonomy: CategoryTaxonomy,
    *,
    publish_categories: Iterable[str] | None = None,
    strict_canonical: bool = False,
) -> dict[str, Any]:
    issues: list[GovernanceIssue] = []

    if taxonomy.schema_version < 2:
        issues.append(
            GovernanceIssue(
                severity="error",
                code="schema-version",
                category="",
                message=(
                    "taxonomy file schema_version is too old for canonical "
                    "governance metadata"
                ),
            )
        )

    for slug, definition in sorted(taxonomy.categories.items()):
        if not definition.display_name.strip():
            issues.append(
                GovernanceIssue(
                    severity="error",
                    code="missing-display-name",
                    category=slug,
                    message="category must declare display_name",
                )
            )
        if len(definition.code) > 24:
            issues.append(
                GovernanceIssue(
                    severity="warning",
                    code="long-code",
                    category=slug,
                    message="category code is long for compact index consumers",
                )
            )
        if strict_canonical and definition.status != "active":
            issues.append(
                GovernanceIssue(
                    severity="error",
                    code="noncanonical-taxonomy-category",
                    category=slug,
                    message="strict canonical taxonomy may only declare active categories",
                )
            )
        if strict_canonical and definition.aliases:
            issues.append(
                GovernanceIssue(
                    severity="error",
                    code="canonical-category-aliases",
                    category=slug,
                    message="canonical category definitions must not declare inbound aliases",
                )
            )
        if strict_canonical and definition.migrate_to:
            issues.append(
                GovernanceIssue(
                    severity="error",
                    code="canonical-category-migrate-to",
                    category=slug,
                    message="canonical category definitions must not carry migration targets",
                )
            )
        if definition.status == "active" and not definition.inclusion_rule:
            issues.append(
                GovernanceIssue(
                    severity="error",
                    code="missing-inclusion-rule",
                    category=slug,
                    message="active canonical category must declare an inclusion_rule",
                )
            )
        if definition.status == "active" and not definition.exclusion_rule:
            issues.append(
                GovernanceIssue(
                    severity="error",
                    code="missing-exclusion-rule",
                    category=slug,
                    message="active canonical category must declare an exclusion_rule",
                )
            )
        if definition.status == "active" and not definition.examples:
            issues.append(
                GovernanceIssue(
                    severity="error",
                    code="missing-examples",
                    category=slug,
                    message="active canonical category must declare at least one example",
                )
            )
        broad_name = bool(_slug_tokens(slug) & REVIEW_NAME_TOKENS)
        if (
            definition.status == "active"
            and broad_name
            and not (definition.description or definition.inclusion_rule)
        ):
            issues.append(
                GovernanceIssue(
                    severity="warning",
                    code="broad-active-name",
                    category=slug,
                    message=(
                        "category name is broad; add a precise description or "
                        "move the slug into legacy_migrations"
                    ),
                )
            )
        if definition.status == "review" and not definition.description:
            issues.append(
                GovernanceIssue(
                    severity="warning",
                    code="missing-description",
                    category=slug,
                    message="category should describe the user-facing inclusion rule",
                )
            )
        if definition.status == "deprecated" and definition.keywords:
            issues.append(
                GovernanceIssue(
                    severity="warning",
                    code="deprecated-keywords",
                    category=slug,
                    message="deprecated categories should not attract new keyword matches",
                )
            )

    if publish_categories is not None:
        issues.extend(publish_category_issues(taxonomy, publish_categories))

    errors = [issue.as_dict() for issue in issues if issue.severity == "error"]
    warnings = [issue.as_dict() for issue in issues if issue.severity == "warning"]
    status_counts: dict[str, int] = {}
    for definition in taxonomy.categories.values():
        status_counts[definition.status] = status_counts.get(definition.status, 0) + 1
    canonical_categories = taxonomy.publishable_categories()

    return {
        "schema_version": taxonomy.schema_version,
        "category_count": len(taxonomy.categories),
        "canonical_category_count": len(canonical_categories),
        "noncanonical_category_count": len(taxonomy.categories) - len(canonical_categories),
        "legacy_migration_count": len(taxonomy.legacy_migrations),
        "publish_category_count": (
            len({str(category) for category in publish_categories if str(category)})
            if publish_categories is not None
            else None
        ),
        "status_counts": dict(sorted(status_counts.items())),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
    }


def print_report(report: dict[str, Any], *, limit: int) -> None:
    print(
        "Taxonomy governance "
        f"(schema={report['schema_version']}, categories={report['category_count']}, "
        f"canonical={report.get('canonical_category_count', 0)}, "
        f"legacy_migrations={report.get('legacy_migration_count', 0)})"
    )
    print(f"Errors: {report['error_count']}")
    print(f"Warnings: {report['warning_count']}")
    if report["errors"]:
        print("Error examples:")
        for item in report["errors"][:limit]:
            print(f"- {item['code']} {item['category']}: {item['message']}")
    if report["warnings"]:
        print("Warning examples:")
        for item in report["warnings"][:limit]:
            print(f"- {item['code']} {item['category']}: {item['message']}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--taxonomy", type=Path, default=None)
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--fail-on-warnings", action="store_true")
    parser.add_argument(
        "--strict-canonical",
        action="store_true",
        help="Fail if taxonomy definitions include non-active transitional categories.",
    )
    parser.add_argument(
        "--publish-category",
        action="append",
        default=[],
        help="Validate a category slug that is intended for published output.",
    )
    parser.add_argument("--limit", type=int, default=20)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        taxonomy = load_taxonomy(args.taxonomy) if args.taxonomy else load_taxonomy()
        report = build_report(
            taxonomy,
            publish_categories=args.publish_category or None,
            strict_canonical=args.strict_canonical,
        )
    except Exception as exc:
        report = {
            "schema_version": None,
            "category_count": 0,
            "status_counts": {},
            "error_count": 1,
            "warning_count": 0,
            "errors": [
                {
                    "severity": "error",
                    "code": "load-failed",
                    "category": "",
                    "message": str(exc),
                }
            ],
            "warnings": [],
        }

    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    print_report(report, limit=args.limit)
    if report["error_count"]:
        return 1
    if args.fail_on_warnings and report["warning_count"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
