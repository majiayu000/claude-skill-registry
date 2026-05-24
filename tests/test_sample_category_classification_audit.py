from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    return importlib.import_module("sample_category_classification_audit")


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def test_builds_deterministic_sample_with_input_context(tmp_path):
    sampler = _load_module()
    workset = tmp_path / "workset.jsonl"
    classification = tmp_path / "classification.jsonl"
    _write_jsonl(
        workset,
        [
            {
                "path": "other/a/SKILL.md",
                "description": "A development helper",
                "content_excerpt": "Use for coding.",
                "semantic_sources": {"name": "frontmatter"},
            },
            {
                "path": "other/b/SKILL.md",
                "description": "A document helper",
                "content_excerpt": "Use for docs.",
                "semantic_sources": {"description": "body"},
            },
        ],
    )
    _write_jsonl(
        classification,
        [
            {
                "path": "other/a/SKILL.md",
                "name": "a",
                "current_category": "other",
                "llm_category": "development",
                "confidence": 0.95,
                "status": "ok",
                "reason": "code",
                "evidence": ["coding"],
                "source_sha256": "source-a",
            },
            {
                "path": "other/b/SKILL.md",
                "name": "b",
                "current_category": "other",
                "llm_category": "documents",
                "confidence": 0.5,
                "status": "ok",
                "reason": "docs",
                "evidence": ["document"],
            },
        ],
    )

    report = sampler.build_report(
        workset_jsonl=workset,
        classification_jsonl=classification,
        output_sample_size=5,
        seed="fixed",
        statuses={"ok"},
        min_confidence=0.9,
    )

    assert report["summary"]["classification_row_count"] == 2
    assert report["summary"]["candidate_count"] == 1
    assert report["summary"]["sample_count"] == 1
    assert report["samples"][0]["path"] == "other/a/SKILL.md"
    assert report["samples"][0]["source_sha256"] == "source-a"
    assert report["samples"][0]["description"] == "A development helper"
