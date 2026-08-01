#!/usr/bin/env python3
"""Fail closed unless a category sample has complete, fresh human review evidence."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from audit_category_quality import (
    build_stratified_sample,
    canonical_digest,
    file_sha256,
)
from category_taxonomy import get_taxonomy


class ReviewEvidenceError(ValueError):
    """Raised when review evidence is incomplete, stale, or non-canonical."""


def _exact_fields(value: Any, fields: set[str], label: str) -> None:
    if not isinstance(value, dict) or set(value) != fields:
        raise ReviewEvidenceError(f"{label} shape mismatch")


def _sample_rows(sample: dict[str, Any]) -> list[dict[str, Any]]:
    _exact_fields(
        sample,
        {
            "schema_version",
            "status",
            "skills_dir",
            "policy",
            "sample_count",
            "digest",
            "strata",
            "errors",
        },
        "sample",
    )
    if sample["schema_version"] != 1 or sample["status"] != "complete":
        raise ReviewEvidenceError("sample is not complete schema v1")
    if sample["errors"] or not isinstance(sample["strata"], list):
        raise ReviewEvidenceError("sample contains errors or invalid strata")
    _exact_fields(
        sample["policy"],
        {"seed", "per_category", "categories", "content_chars"},
        "sample policy",
    )
    policy = sample["policy"]
    if (
        not isinstance(policy["seed"], str)
        or not policy["seed"]
        or not isinstance(policy["per_category"], int)
        or policy["per_category"] <= 0
        or not isinstance(policy["categories"], list)
        or not policy["categories"]
        or len(set(policy["categories"])) != len(policy["categories"])
        or not isinstance(policy["content_chars"], int)
        or policy["content_chars"] <= 0
    ):
        raise ReviewEvidenceError("sample policy identity mismatch")

    rows: list[dict[str, Any]] = []
    digest_inputs: list[dict[str, str]] = []
    stratum_categories: list[str] = []
    sample_fields = {
        "path",
        "name",
        "current_category",
        "description",
        "content_excerpt",
        "semantic_sources",
        "source_sha256",
        "metadata_sha256",
        "sample_key",
    }
    for index, stratum in enumerate(sample["strata"]):
        _exact_fields(
            stratum,
            {
                "category",
                "population_count",
                "sample_count",
                "quota",
                "digest",
                "samples",
            },
            f"sample stratum {index}",
        )
        if not isinstance(stratum["samples"], list):
            raise ReviewEvidenceError("sample stratum samples must be a list")
        if (
            stratum["sample_count"] != len(stratum["samples"])
            or stratum["quota"] != policy["per_category"]
            or stratum["sample_count"] != stratum["quota"]
            or stratum["population_count"] < stratum["quota"]
        ):
            raise ReviewEvidenceError("sample stratum count mismatch")
        for row_index, row in enumerate(stratum["samples"]):
            _exact_fields(row, sample_fields, f"sample row {index}:{row_index}")
            if row["current_category"] != stratum["category"]:
                raise ReviewEvidenceError("sample row category mismatch")
            for hash_field in ("source_sha256", "metadata_sha256", "sample_key"):
                if (
                    not isinstance(row[hash_field], str)
                    or len(row[hash_field]) != 64
                    or any(char not in "0123456789abcdef" for char in row[hash_field])
                ):
                    raise ReviewEvidenceError(f"sample row invalid {hash_field}")
        calculated_digest = canonical_digest(stratum["samples"])
        if stratum["digest"] != calculated_digest:
            raise ReviewEvidenceError("sample stratum digest mismatch")
        stratum_categories.append(stratum["category"])
        digest_inputs.append(
            {"category": stratum["category"], "digest": calculated_digest}
        )
        rows.extend(stratum["samples"])
    if stratum_categories != policy["categories"]:
        raise ReviewEvidenceError("sample strata do not match policy categories")
    if sample["sample_count"] != len(rows):
        raise ReviewEvidenceError("sample total count mismatch")
    if sample["digest"] != canonical_digest(digest_inputs):
        raise ReviewEvidenceError("sample overall digest mismatch")
    return rows


def check_review(
    sample: dict[str, Any],
    review: dict[str, Any],
    *,
    min_accuracy: float,
) -> dict[str, Any]:
    if not 0 <= min_accuracy <= 1:
        raise ReviewEvidenceError("min_accuracy must be between 0 and 1")
    rows = _sample_rows(sample)
    policy = get_taxonomy().audit_sampling
    if (
        sample["schema_version"] != policy.schema_version
        or sample["policy"]["seed"] != policy.seed
        or sample["policy"]["per_category"] != policy.per_category
        or sample["policy"]["categories"] != list(policy.categories)
    ):
        raise ReviewEvidenceError("sample policy does not match canonical taxonomy")

    skills_dir = Path(sample["skills_dir"]).resolve()
    fresh_sample = build_stratified_sample(
        skills_dir,
        content_chars=sample["policy"]["content_chars"],
        taxonomy=get_taxonomy(),
    )
    if fresh_sample["status"] != "complete":
        raise ReviewEvidenceError("current sample population is incomplete")
    if (
        fresh_sample["digest"] != sample["digest"]
        or fresh_sample["strata"] != sample["strata"]
    ):
        raise ReviewEvidenceError("sample no longer matches current population")

    for row in rows:
        rel = Path(row["path"])
        if (
            rel.is_absolute()
            or ".." in rel.parts
            or rel.name != "SKILL.md"
        ):
            raise ReviewEvidenceError(f"unsafe sample path: {row['path']}")
        source_path = skills_dir / rel
        metadata_path = source_path.parent / "metadata.json"
        if not source_path.is_file() or not metadata_path.is_file():
            raise ReviewEvidenceError(f"sample source is missing: {row['path']}")
        if (
            file_sha256(source_path) != row["source_sha256"]
            or file_sha256(metadata_path) != row["metadata_sha256"]
        ):
            raise ReviewEvidenceError(f"sample source changed: {row['path']}")

    _exact_fields(review, {"schema_version", "sample_digest", "reviews"}, "review")
    if review["schema_version"] != 1 or review["sample_digest"] != sample["digest"]:
        raise ReviewEvidenceError("review digest does not match sample")
    if not isinstance(review["reviews"], list):
        raise ReviewEvidenceError("reviews must be a list")

    sample_by_path = {row.get("path"): row for row in rows}
    if len(sample_by_path) != len(rows) or None in sample_by_path:
        raise ReviewEvidenceError("sample paths must be unique and non-empty")

    reviewed: dict[str, dict[str, Any]] = {}
    active = get_taxonomy().publishable_categories()
    for index, item in enumerate(review["reviews"]):
        _exact_fields(
            item,
            {"path", "source_sha256", "metadata_sha256", "expected_category"},
            f"review entry {index}",
        )
        path = item["path"]
        if path in reviewed:
            raise ReviewEvidenceError(f"duplicate review path: {path}")
        sample_row = sample_by_path.get(path)
        if sample_row is None:
            raise ReviewEvidenceError(f"review path is not sampled: {path}")
        if (
            item["source_sha256"] != sample_row.get("source_sha256")
            or item["metadata_sha256"] != sample_row.get("metadata_sha256")
        ):
            raise ReviewEvidenceError(f"stale source hashes for: {path}")
        if item["expected_category"] not in active:
            raise ReviewEvidenceError(
                f"non-canonical expected category for: {path}"
            )
        reviewed[path] = item

    missing = sorted(set(sample_by_path) - set(reviewed))
    if missing:
        raise ReviewEvidenceError(f"missing review paths: {', '.join(missing[:3])}")

    correct_by_category: Counter[str] = Counter()
    total_by_category: Counter[str] = Counter()
    for path, sample_row in sample_by_path.items():
        category = sample_row["current_category"]
        total_by_category[category] += 1
        if reviewed[path]["expected_category"] == category:
            correct_by_category[category] += 1

    per_category = {}
    for category in sorted(total_by_category):
        total = total_by_category[category]
        accuracy = correct_by_category[category] / total
        per_category[category] = {
            "correct": correct_by_category[category],
            "total": total,
            "accuracy": accuracy,
        }
        if accuracy < min_accuracy:
            raise ReviewEvidenceError(
                f"{category} accuracy {accuracy:.3f} is below {min_accuracy:.3f}"
            )

    overall_correct = sum(correct_by_category.values())
    overall_accuracy = overall_correct / len(rows) if rows else 0.0
    if overall_accuracy < min_accuracy:
        raise ReviewEvidenceError(
            f"overall accuracy {overall_accuracy:.3f} is below {min_accuracy:.3f}"
        )
    return {
        "schema_version": 1,
        "status": "passed",
        "sample_digest": sample["digest"],
        "min_accuracy": min_accuracy,
        "correct": overall_correct,
        "total": len(rows),
        "accuracy": overall_accuracy,
        "categories": per_category,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample", type=Path, required=True)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--min-accuracy", type=float, default=0.8)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result = check_review(
            json.loads(args.sample.read_text(encoding="utf-8")),
            json.loads(args.review.read_text(encoding="utf-8")),
            min_accuracy=args.min_accuracy,
        )
    except (OSError, json.JSONDecodeError, ReviewEvidenceError) as error:
        print(json.dumps({"status": "failed", "error": str(error)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
