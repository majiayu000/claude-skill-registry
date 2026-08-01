from __future__ import annotations

import importlib
import sys
from pathlib import Path


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    return importlib.import_module("check_taxonomy_governance")


def _taxonomy_module():
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    return importlib.import_module("category_taxonomy")


def test_current_taxonomy_has_no_governance_errors():
    governance = _load_module()
    taxonomy = _taxonomy_module().load_taxonomy()

    report = governance.build_report(taxonomy)

    assert report["schema_version"] == 2
    assert report["error_count"] == 0
    assert report["canonical_category_count"] > 0
    assert report["noncanonical_category_count"] == 0
    assert report["legacy_migration_count"] > 0
    assert report["status_counts"] == {"active": report["category_count"]}


def test_governance_reports_old_schema_error(tmp_path):
    governance = _load_module()
    taxonomy_module = _taxonomy_module()
    taxonomy_file = tmp_path / "categories.yaml"
    taxonomy_file.write_text(
        """
schema_version: 1
default_category: other
audit_sampling:
  schema_version: 1
  seed: test
  per_category: 1
  categories: [other]
categories:
  - slug: other
    code: oth
    display_name: Other
""",
        encoding="utf-8",
    )

    report = governance.build_report(taxonomy_module.load_taxonomy(taxonomy_file))

    codes = {error["code"] for error in report["errors"]}
    assert "schema-version" in codes
    assert "missing-inclusion-rule" in codes


def test_governance_rejects_noncanonical_publish_targets():
    governance = _load_module()
    taxonomy = _taxonomy_module().load_taxonomy()

    report = governance.build_report(
        taxonomy,
        publish_categories=["development", "docs", "applied", "engineering"],
    )

    codes = {error["category"]: error["code"] for error in report["errors"]}
    assert codes["docs"] == "unknown-publish-category"
    assert codes["applied"] == "unknown-publish-category"
    assert codes["engineering"] == "unknown-publish-category"
    assert "development" not in codes


def test_governance_requires_active_category_rules(tmp_path):
    governance = _load_module()
    taxonomy_module = _taxonomy_module()
    taxonomy_file = tmp_path / "categories.yaml"
    taxonomy_file.write_text(
        """
schema_version: 2
default_category: other
audit_sampling:
  schema_version: 1
  seed: test
  per_category: 1
  categories: [other]
categories:
  - slug: other
    code: oth
    display_name: Other
""",
        encoding="utf-8",
    )

    report = governance.build_report(taxonomy_module.load_taxonomy(taxonomy_file))

    codes = {error["code"] for error in report["errors"]}
    assert codes == {
        "missing-inclusion-rule",
        "missing-exclusion-rule",
        "missing-examples",
    }


def test_governance_strict_canonical_accepts_current_taxonomy():
    governance = _load_module()
    taxonomy = _taxonomy_module().load_taxonomy()

    report = governance.build_report(taxonomy, strict_canonical=True)

    assert report["error_count"] == 0


def test_governance_strict_canonical_rejects_transitional_definitions(tmp_path):
    governance = _load_module()
    taxonomy_module = _taxonomy_module()
    taxonomy_file = tmp_path / "categories.yaml"
    taxonomy_file.write_text(
        """
schema_version: 2
default_category: other
audit_sampling:
  schema_version: 1
  seed: test
  per_category: 1
  categories: [other]
categories:
  - slug: other
    code: oth
    display_name: Other
  - slug: old
    code: old
    display_name: Old
    status: review
  - slug: development
    code: dev
    display_name: Development
    aliases: [dev]
""",
        encoding="utf-8",
    )

    report = governance.build_report(
        taxonomy_module.load_taxonomy(taxonomy_file),
        strict_canonical=True,
    )

    codes = {error["code"] for error in report["errors"]}
    assert "noncanonical-taxonomy-category" in codes
    assert "canonical-category-aliases" in codes
