#!/usr/bin/env python3
"""Canonical category taxonomy helpers for registry pipeline scripts."""

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TAXONOMY_PATH = ROOT / "taxonomy" / "categories.yaml"


class UnknownCategoryError(ValueError):
    """Raised when a category is not declared by the canonical taxonomy."""


@dataclass(frozen=True)
class CategoryDefinition:
    slug: str
    code: str
    display_name: str
    aliases: tuple[str, ...]
    keywords: tuple[str, ...]
    status: str = "active"
    description: str = ""
    inclusion_rule: str = ""
    exclusion_rule: str = ""
    examples: tuple[str, ...] = ()
    parent: str = ""
    migrate_to: str = ""


@dataclass(frozen=True)
class LegacyCategoryMigration:
    slug: str
    target: str = ""
    review_required: bool = True
    reason: str = ""


@dataclass(frozen=True)
class AuditSamplingPolicy:
    schema_version: int
    seed: str
    per_category: int
    categories: tuple[str, ...]


@dataclass(frozen=True)
class CategoryTaxonomy:
    schema_version: int
    default_category: str
    categories: dict[str, CategoryDefinition]
    codes: dict[str, str]
    aliases: dict[str, str]
    legacy_migrations: dict[str, LegacyCategoryMigration]
    audit_sampling: AuditSamplingPolicy

    def resolve(
        self,
        raw_category: str | None,
        *,
        allow_unknown: bool = False,
        allow_alias: bool = False,
    ) -> str:
        slug = category_slug(raw_category or self.default_category)
        if not slug:
            return self.default_category
        if slug in self.categories:
            return slug
        if allow_alias and slug in self.aliases:
            return self.aliases[slug]
        if allow_unknown:
            return slug
        raise UnknownCategoryError(f"Unknown category: {raw_category!r}")

    def code_for(self, raw_category: str | None, *, allow_alias: bool = False) -> str:
        slug = self.resolve(raw_category, allow_unknown=True, allow_alias=True)
        definition = self.categories.get(slug)
        return definition.code if definition else slug

    def slug_for_code(self, raw_code: str | None, *, allow_unknown: bool = False) -> str:
        code = category_slug(raw_code or "")
        if not code:
            return self.default_category
        if code in self.codes:
            return self.codes[code]
        if allow_unknown:
            return code
        raise UnknownCategoryError(f"Unknown category code: {raw_code!r}")

    def is_known(self, raw_category: str | None) -> bool:
        slug = category_slug(raw_category or "")
        return slug in self.categories

    def alias_target(self, raw_category: str | None) -> str | None:
        slug = category_slug(raw_category or "")
        return self.aliases.get(slug)

    def legacy_migration(self, raw_category: str | None) -> LegacyCategoryMigration | None:
        slug = category_slug(raw_category or "")
        return self.legacy_migrations.get(slug)

    def publishable_categories(self) -> frozenset[str]:
        return frozenset(
            slug
            for slug, definition in self.categories.items()
            if definition.status == "active"
        )

    def is_publishable(self, raw_category: str | None) -> bool:
        slug = self.resolve(raw_category, allow_unknown=True)
        definition = self.categories.get(slug)
        return bool(definition and definition.status == "active")

    def category_status(self, raw_category: str | None) -> str:
        slug = self.resolve(raw_category, allow_unknown=True)
        definition = self.categories.get(slug)
        if definition:
            return definition.status
        if slug in self.legacy_migrations:
            return "legacy"
        return "unknown"

    def keyword_map(self) -> dict[str, list[str]]:
        return {
            slug: list(definition.keywords)
            for slug, definition in self.categories.items()
            if definition.keywords
        }

    def migration_target(self, raw_category: str | None) -> str | None:
        slug = self.resolve(raw_category, allow_unknown=True)
        definition = self.categories.get(slug)
        if definition:
            return definition.migrate_to or None
        migration = self.legacy_migrations.get(slug)
        return migration.target if migration else None

    def public_contract(self, *, updated_at: str) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "taxonomy_schema_version": self.schema_version,
            "updated_at": updated_at,
            "default_category": self.default_category,
            "default_code": self.code_for(self.default_category),
            "category_count": len(self.categories),
            "categories": [
                {
                    "slug": definition.slug,
                    "code": definition.code,
                    "display_name": definition.display_name,
                    "parent": definition.parent,
                }
                for definition in self.categories.values()
            ],
        }


def category_slug(raw_category: str | None) -> str:
    text = str(raw_category or "").strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", text)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


def _as_string_list(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ValueError("taxonomy aliases/keywords must be lists")
    return tuple(category_slug(item) for item in value if category_slug(item))


def _as_plain_string_list(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ValueError("taxonomy examples must be lists")
    return tuple(str(item).strip() for item in value if str(item).strip())


def _as_optional_slug(value: Any) -> str:
    if value is None:
        return ""
    return category_slug(value)


def _as_bool(value: Any, *, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    raise ValueError("taxonomy boolean fields must be true or false")


def load_taxonomy(path: Path = DEFAULT_TAXONOMY_PATH) -> CategoryTaxonomy:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("taxonomy file must contain an object")

    default_category = category_slug(payload.get("default_category", "other")) or "other"
    categories_raw = payload.get("categories")
    if not isinstance(categories_raw, list) or not categories_raw:
        raise ValueError("taxonomy must declare at least one category")

    categories: dict[str, CategoryDefinition] = {}
    aliases: dict[str, str] = {}
    codes: dict[str, str] = {}

    for entry in categories_raw:
        if not isinstance(entry, dict):
            raise ValueError("taxonomy category entries must be objects")
        slug = category_slug(entry.get("slug"))
        if not slug:
            raise ValueError("taxonomy category missing slug")
        if slug in categories:
            raise ValueError(f"duplicate taxonomy category slug: {slug}")
        if slug in aliases:
            raise ValueError(f"taxonomy category {slug!r} conflicts with an alias")
        code = category_slug(entry.get("code") or slug)
        if code in codes:
            raise ValueError(
                f"taxonomy code {code!r} maps to both {codes[code]!r} and {slug!r}"
            )
        codes[code] = slug
        display_name = str(entry.get("display_name") or slug.replace("-", " ").title())
        category_aliases = _as_string_list(entry.get("aliases"))
        keywords = _as_string_list(entry.get("keywords"))
        status = category_slug(entry.get("status") or "active")
        if status not in {"active", "review", "deprecated"}:
            raise ValueError(
                f"taxonomy category {slug!r} has invalid status {status!r}"
            )
        description = str(entry.get("description") or "").strip()
        inclusion_rule = str(entry.get("inclusion_rule") or "").strip()
        exclusion_rule = str(entry.get("exclusion_rule") or "").strip()
        examples = _as_plain_string_list(entry.get("examples"))
        parent = _as_optional_slug(entry.get("parent"))
        migrate_to = _as_optional_slug(entry.get("migrate_to"))
        categories[slug] = CategoryDefinition(
            slug=slug,
            code=code,
            display_name=display_name,
            aliases=category_aliases,
            keywords=keywords,
            status=status,
            description=description,
            inclusion_rule=inclusion_rule,
            exclusion_rule=exclusion_rule,
            examples=examples,
            parent=parent,
            migrate_to=migrate_to,
        )
        for alias in category_aliases:
            if alias in categories:
                raise ValueError(f"taxonomy alias {alias!r} conflicts with a category slug")
            existing = aliases.get(alias)
            if existing and existing != slug:
                raise ValueError(f"taxonomy alias {alias!r} maps to both {existing!r} and {slug!r}")
            aliases[alias] = slug

    if default_category not in categories:
        raise ValueError(f"default category {default_category!r} is not declared")
    if categories[default_category].status != "active":
        raise ValueError("default category must be active")

    for slug, definition in categories.items():
        if definition.parent:
            parent_definition = categories.get(definition.parent)
            if parent_definition is None:
                raise ValueError(
                    f"taxonomy category {slug!r} has unknown parent "
                    f"{definition.parent!r}"
                )
            if parent_definition.status != "active":
                raise ValueError(
                    f"taxonomy category {slug!r} has non-active parent "
                    f"{definition.parent!r}"
                )
            if definition.parent == slug:
                raise ValueError(f"taxonomy category {slug!r} must not parent itself")
            if parent_definition.parent:
                raise ValueError(
                    f"taxonomy category {slug!r} exceeds two reporting levels via "
                    f"{definition.parent!r}"
                )
        if definition.migrate_to:
            target = categories.get(definition.migrate_to)
            if target is None:
                raise ValueError(
                    f"taxonomy category {slug!r} has unknown migrate_to "
                    f"{definition.migrate_to!r}"
                )
            if definition.migrate_to == slug:
                raise ValueError(f"taxonomy category {slug!r} must not migrate to itself")
            if target.status != "active":
                raise ValueError(
                    f"taxonomy category {slug!r} migrates to non-active target "
                    f"{definition.migrate_to!r}"
                )
        if definition.status == "deprecated" and not definition.migrate_to:
            raise ValueError(
                f"deprecated taxonomy category {slug!r} must declare migrate_to"
            )

    legacy_migrations: dict[str, LegacyCategoryMigration] = {}
    legacy_raw = payload.get("legacy_migrations") or []
    if not isinstance(legacy_raw, list):
        raise ValueError("taxonomy legacy_migrations must be a list")
    for entry in legacy_raw:
        if not isinstance(entry, dict):
            raise ValueError("taxonomy legacy migration entries must be objects")
        slug = category_slug(entry.get("slug"))
        if not slug:
            raise ValueError("taxonomy legacy migration missing slug")
        if slug in categories:
            raise ValueError(
                f"legacy category migration {slug!r} conflicts with active category"
            )
        if slug in legacy_migrations:
            raise ValueError(f"duplicate legacy category migration slug: {slug}")
        target = _as_optional_slug(entry.get("target"))
        if target:
            target_definition = categories.get(target)
            if target_definition is None:
                raise ValueError(
                    f"legacy category migration {slug!r} has unknown target {target!r}"
                )
            if target_definition.status != "active":
                raise ValueError(
                    f"legacy category migration {slug!r} targets non-active category {target!r}"
                )
            aliases[slug] = target
        review_required = _as_bool(entry.get("review_required"), default=not bool(target))
        reason = str(entry.get("reason") or "").strip()
        legacy_migrations[slug] = LegacyCategoryMigration(
            slug=slug,
            target=target,
            review_required=review_required,
            reason=reason,
        )

    sampling_raw = payload.get("audit_sampling")
    if not isinstance(sampling_raw, dict):
        raise ValueError("taxonomy audit_sampling must contain an object")
    sampling_schema_version = sampling_raw.get("schema_version")
    if sampling_schema_version != 1:
        raise ValueError("taxonomy audit_sampling schema_version must be 1")
    sampling_seed = str(sampling_raw.get("seed") or "").strip()
    if not sampling_seed:
        raise ValueError("taxonomy audit_sampling seed must be non-empty")
    sampling_quota = sampling_raw.get("per_category")
    if (
        isinstance(sampling_quota, bool)
        or not isinstance(sampling_quota, int)
        or sampling_quota <= 0
    ):
        raise ValueError("taxonomy audit_sampling per_category must be a positive integer")
    sampling_categories = _as_string_list(sampling_raw.get("categories"))
    if not sampling_categories or len(set(sampling_categories)) != len(sampling_categories):
        raise ValueError("taxonomy audit_sampling categories must be unique and non-empty")
    for sampling_category in sampling_categories:
        definition = categories.get(sampling_category)
        if definition is None or definition.status != "active":
            raise ValueError(
                "taxonomy audit_sampling category must be active: "
                f"{sampling_category!r}"
            )
    audit_sampling = AuditSamplingPolicy(
        schema_version=sampling_schema_version,
        seed=sampling_seed,
        per_category=sampling_quota,
        categories=sampling_categories,
    )

    return CategoryTaxonomy(
        schema_version=int(payload.get("schema_version", 1)),
        default_category=default_category,
        categories=categories,
        codes=codes,
        aliases=aliases,
        legacy_migrations=legacy_migrations,
        audit_sampling=audit_sampling,
    )


@lru_cache(maxsize=1)
def get_taxonomy() -> CategoryTaxonomy:
    return load_taxonomy()


def known_categories() -> frozenset[str]:
    return frozenset(get_taxonomy().categories)


def category_aliases() -> dict[str, str]:
    return dict(get_taxonomy().aliases)


def legacy_category_migrations() -> dict[str, LegacyCategoryMigration]:
    return dict(get_taxonomy().legacy_migrations)


def publishable_categories() -> frozenset[str]:
    return get_taxonomy().publishable_categories()


def category_status(raw_category: str | None) -> str:
    return get_taxonomy().category_status(raw_category)


def resolve_category(
    raw_category: str | None,
    *,
    allow_unknown: bool = False,
    allow_alias: bool = False,
) -> str:
    return get_taxonomy().resolve(
        raw_category,
        allow_unknown=allow_unknown,
        allow_alias=allow_alias,
    )


def get_category_code(raw_category: str | None, *, allow_alias: bool = False) -> str:
    return get_taxonomy().code_for(raw_category, allow_alias=allow_alias)


def get_category_slug_from_code(
    raw_code: str | None, *, allow_unknown: bool = False
) -> str:
    return get_taxonomy().slug_for_code(raw_code, allow_unknown=allow_unknown)


def category_keywords() -> dict[str, list[str]]:
    return get_taxonomy().keyword_map()


def category_migration_target(raw_category: str | None) -> str | None:
    return get_taxonomy().migration_target(raw_category)
