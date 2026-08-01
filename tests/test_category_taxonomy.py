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
    assert loaded.categories["development"].inclusion_rule
    assert loaded.categories["development"].exclusion_rule
    assert loaded.categories["development"].examples
    assert len(loaded.categories) >= 40
    assert "docs" not in loaded.categories
    assert loaded.migration_target("docs") == "documents"
    assert loaded.legacy_migration("docs").target == "documents"
    assert loaded.legacy_migration("applied").review_required is True
    assert len(loaded.categories) == 40
    assert len([item for item in loaded.categories.values() if not item.parent]) == 12
    assert loaded.audit_sampling.per_category == 50
    assert loaded.audit_sampling.categories == (
        "integration",
        "domains",
        "skills",
        "context-management",
        "data",
        "development",
    )
    for slug, definition in loaded.categories.items():
        assert loaded.slug_for_code(definition.code) == slug

    contract = loaded.public_contract(updated_at="2026-07-23T00:00:00Z")
    assert contract["category_count"] == 40
    assert contract["default_code"] == "oth"
    assert len({item["slug"] for item in contract["categories"]}) == 40
    assert len({item["code"] for item in contract["categories"]}) == 40


def test_taxonomy_rejects_aliases_by_default_and_codes():
    taxonomy = _load_module()
    with pytest.raises(taxonomy.UnknownCategoryError):
        taxonomy.resolve_category("Engineering")
    assert taxonomy.resolve_category("Engineering", allow_unknown=True) == "engineering"
    assert taxonomy.resolve_category("Engineering", allow_alias=True) == "development"
    assert taxonomy.get_category_code("development") == "dev"
    assert taxonomy.get_category_code("Engineering") == "dev"
    assert taxonomy.get_category_code("dev") == "dev"
    assert taxonomy.get_category_code("Engineering", allow_alias=True) == "dev"
    assert taxonomy.get_category_code("unknown-new-bucket") == "unknown-new-bucket"
    assert "development" in taxonomy.publishable_categories()
    assert "docs" not in taxonomy.publishable_categories()
    assert "applied" not in taxonomy.publishable_categories()


def test_taxonomy_rejects_legacy_migration_conflicts(tmp_path):
    taxonomy = _load_module()
    taxonomy_file = tmp_path / "categories.yaml"
    taxonomy_file.write_text(
        """
schema_version: 2
default_category: other
legacy_migrations:
  - slug: old
    target: missing
categories:
  - slug: other
    code: oth
""",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="unknown target"):
        taxonomy.load_taxonomy(taxonomy_file)


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


def test_taxonomy_rejects_self_parent_and_third_reporting_level(tmp_path):
    taxonomy = _load_module()
    self_parent = tmp_path / "self.yaml"
    self_parent.write_text(
        """
schema_version: 2
default_category: other
categories:
  - slug: other
    code: oth
    parent: other
audit_sampling:
  schema_version: 1
  seed: test
  per_category: 1
  categories: [other]
""",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="must not parent itself"):
        taxonomy.load_taxonomy(self_parent)

    deep = tmp_path / "deep.yaml"
    deep.write_text(
        """
schema_version: 2
default_category: other
categories:
  - slug: other
    code: oth
  - slug: child
    code: child
    parent: other
  - slug: grandchild
    code: grandchild
    parent: child
audit_sampling:
  schema_version: 1
  seed: test
  per_category: 1
  categories: [other]
""",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="exceeds two reporting levels"):
        taxonomy.load_taxonomy(deep)


def test_taxonomy_rejects_invalid_sampling_policy(tmp_path):
    taxonomy = _load_module()
    taxonomy_file = tmp_path / "categories.yaml"
    taxonomy_file.write_text(
        """
schema_version: 2
default_category: other
categories:
  - slug: other
    code: oth
audit_sampling:
  schema_version: 1
  seed: test
  per_category: 0
  categories: [other]
""",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="positive integer"):
        taxonomy.load_taxonomy(taxonomy_file)
