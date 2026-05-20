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
    parent: str = ""
    migrate_to: str = ""


@dataclass(frozen=True)
class CategoryTaxonomy:
    schema_version: int
    default_category: str
    categories: dict[str, CategoryDefinition]
    aliases: dict[str, str]

    def resolve(self, raw_category: str | None, *, allow_unknown: bool = False) -> str:
        slug = category_slug(raw_category or self.default_category)
        if not slug:
            return self.default_category
        if slug in self.categories:
            return slug
        if slug in self.aliases:
            return self.aliases[slug]
        if allow_unknown:
            return slug
        raise UnknownCategoryError(f"Unknown category: {raw_category!r}")

    def code_for(self, raw_category: str | None) -> str:
        slug = self.resolve(raw_category, allow_unknown=True)
        definition = self.categories.get(slug)
        return definition.code if definition else slug

    def is_known(self, raw_category: str | None) -> bool:
        slug = category_slug(raw_category or "")
        return slug in self.categories

    def alias_target(self, raw_category: str | None) -> str | None:
        slug = category_slug(raw_category or "")
        return self.aliases.get(slug)

    def keyword_map(self) -> dict[str, list[str]]:
        return {
            slug: list(definition.keywords)
            for slug, definition in self.categories.items()
            if definition.keywords
        }

    def migration_target(self, raw_category: str | None) -> str | None:
        slug = self.resolve(raw_category, allow_unknown=True)
        definition = self.categories.get(slug)
        if not definition:
            return None
        return definition.migrate_to or None


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


def _as_optional_slug(value: Any) -> str:
    if value is None:
        return ""
    return category_slug(value)


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
    if categories[default_category].status == "deprecated":
        raise ValueError("default category must not be deprecated")

    for slug, definition in categories.items():
        if definition.parent:
            parent_definition = categories.get(definition.parent)
            if parent_definition is None:
                raise ValueError(
                    f"taxonomy category {slug!r} has unknown parent "
                    f"{definition.parent!r}"
                )
            if parent_definition.status == "deprecated":
                raise ValueError(
                    f"taxonomy category {slug!r} has deprecated parent "
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
                raise ValueError(
                    f"taxonomy category {slug!r} must not migrate to itself"
                )
            if target.status == "deprecated":
                raise ValueError(
                    f"taxonomy category {slug!r} migrates to deprecated target "
                    f"{definition.migrate_to!r}"
                )
        if definition.status == "deprecated" and not definition.migrate_to:
            raise ValueError(
                f"deprecated taxonomy category {slug!r} must declare migrate_to"
            )

    return CategoryTaxonomy(
        schema_version=int(payload.get("schema_version", 1)),
        default_category=default_category,
        categories=categories,
        aliases=aliases,
    )


@lru_cache(maxsize=1)
def get_taxonomy() -> CategoryTaxonomy:
    return load_taxonomy()


def known_categories() -> frozenset[str]:
    return frozenset(get_taxonomy().categories)


def category_aliases() -> dict[str, str]:
    return dict(get_taxonomy().aliases)


def resolve_category(raw_category: str | None, *, allow_unknown: bool = False) -> str:
    return get_taxonomy().resolve(raw_category, allow_unknown=allow_unknown)


def get_category_code(raw_category: str | None) -> str:
    return get_taxonomy().code_for(raw_category)


def category_keywords() -> dict[str, list[str]]:
    return get_taxonomy().keyword_map()


def category_migration_target(raw_category: str | None) -> str | None:
    return get_taxonomy().migration_target(raw_category)
