from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    return importlib.import_module("category_taxonomy")


def test_taxonomy_loads_current_category_set():
    taxonomy = _load_module()
    loaded = taxonomy.load_taxonomy()
    assert loaded.schema_version == 2
    assert loaded.default_category == "other"
    assert "development" in loaded.categories
    assert "other" in loaded.categories
    assert len(loaded.categories) >= 77
    assert loaded.categories["docs"].status == "deprecated"
    assert loaded.migration_target("docs") == "documents"


def test_taxonomy_resolves_aliases_and_codes():
    taxonomy = _load_module()
    assert taxonomy.resolve_category("Engineering") == "development"
    assert taxonomy.get_category_code("development") == "dev"
    assert taxonomy.get_category_code("unknown-new-bucket") == "unknown-new-bucket"


def test_taxonomy_rejects_alias_category_conflict(tmp_path):
    taxonomy = _load_module()
    taxonomy_file = tmp_path / "categories.yaml"
    taxonomy_file.write_text(
        """
schema_version: 1
default_category: other
categories:
  - slug: other
    code: oth
    aliases: [dev]
  - slug: dev
    code: dev
""",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="conflicts with an alias"):
        taxonomy.load_taxonomy(taxonomy_file)


def test_taxonomy_rejects_duplicate_codes(tmp_path):
    taxonomy = _load_module()
    taxonomy_file = tmp_path / "categories.yaml"
    taxonomy_file.write_text(
        """
schema_version: 1
default_category: other
categories:
  - slug: other
    code: oth
  - slug: development
    code: oth
""",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="maps to both"):
        taxonomy.load_taxonomy(taxonomy_file)


def test_taxonomy_rejects_deprecated_category_without_target(tmp_path):
    taxonomy = _load_module()
    taxonomy_file = tmp_path / "categories.yaml"
    taxonomy_file.write_text(
        """
schema_version: 2
default_category: other
categories:
  - slug: other
    code: oth
  - slug: old
    code: old
    status: deprecated
""",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="must declare migrate_to"):
        taxonomy.load_taxonomy(taxonomy_file)


def test_taxonomy_rejects_unknown_parent(tmp_path):
    taxonomy = _load_module()
    taxonomy_file = tmp_path / "categories.yaml"
    taxonomy_file.write_text(
        """
schema_version: 2
default_category: other
categories:
  - slug: other
    code: oth
  - slug: child
    code: child
    parent: missing
""",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="unknown parent"):
        taxonomy.load_taxonomy(taxonomy_file)
