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
    assert report["status_counts"]["deprecated"] >= 1
    assert report["status_counts"]["review"] >= 1


def test_governance_reports_schema_v1_error(tmp_path):
    governance = _load_module()
    taxonomy_module = _taxonomy_module()
    taxonomy_file = tmp_path / "categories.yaml"
    taxonomy_file.write_text(
        """
schema_version: 1
default_category: other
categories:
  - slug: other
    code: oth
    display_name: Other
""",
        encoding="utf-8",
    )

    report = governance.build_report(taxonomy_module.load_taxonomy(taxonomy_file))

    assert report["error_count"] == 1
    assert report["errors"][0]["code"] == "schema-version"
