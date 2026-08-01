from __future__ import annotations

import copy
import importlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest


def _load_modules():
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    return (
        importlib.import_module("audit_category_quality"),
        importlib.import_module("check_category_sample_review"),
    )


def _test_taxonomy():
    policy = SimpleNamespace(
        schema_version=1,
        seed="test",
        per_category=2,
        categories=("integration",),
    )
    return SimpleNamespace(
        audit_sampling=policy,
        default_category="other",
        publishable_categories=lambda: {"integration", "data"},
    )


def _evidence(tmp_path, taxonomy=None):
    audit, _ = _load_modules()
    skills_dir = tmp_path / "skills"
    for index in range(2):
        skill_dir = skills_dir / "integration" / f"skill-{index}"
        skill_dir.mkdir(parents=True)
        skill_path = skill_dir / "SKILL.md"
        metadata_path = skill_dir / "metadata.json"
        skill_path.write_text(f"---\nname: skill-{index}\n---\n", encoding="utf-8")
        metadata_path.write_text(
            f'{{"name":"skill-{index}","category":"integration"}}\n',
            encoding="utf-8",
        )
    sample = audit.build_stratified_sample(
        skills_dir,
        content_chars=128,
        taxonomy=taxonomy or _test_taxonomy(),
    )
    rows = sample["strata"][0]["samples"]
    review = {
        "schema_version": 1,
        "sample_digest": sample["digest"],
        "reviews": [
            {
                "path": row["path"],
                "source_sha256": row["source_sha256"],
                "metadata_sha256": row["metadata_sha256"],
                "expected_category": "integration",
            }
            for row in rows
        ],
    }
    return sample, review


def _use_test_policy(checker, monkeypatch):
    audit, _ = _load_modules()
    taxonomy = _test_taxonomy()
    monkeypatch.setattr(audit, "get_taxonomy", lambda: taxonomy)
    monkeypatch.setattr(checker, "get_taxonomy", lambda: taxonomy)
    return taxonomy


def test_review_gate_accepts_complete_fresh_review(tmp_path, monkeypatch):
    _, checker = _load_modules()
    taxonomy = _use_test_policy(checker, monkeypatch)
    sample, review = _evidence(tmp_path, taxonomy)
    result = checker.check_review(sample, review, min_accuracy=0.8)
    assert result["status"] == "passed"
    assert result["accuracy"] == 1
    assert result["categories"]["integration"]["total"] == 2


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (lambda sample, review: review["reviews"].pop(), "missing review paths"),
        (
            lambda sample, review: review["reviews"].append(
                copy.deepcopy(review["reviews"][0])
            ),
            "duplicate review path",
        ),
        (
            lambda sample, review: review["reviews"][0].update(
                source_sha256="f" * 64
            ),
            "stale source hashes",
        ),
        (
            lambda sample, review: review["reviews"][0].update(
                expected_category="not-canonical"
            ),
            "non-canonical expected category",
        ),
        (
            lambda sample, review: sample["strata"][0]["samples"][0].update(
                description="tampered"
            ),
            "sample stratum digest mismatch",
        ),
        (
            lambda sample, review: review.update(sample_digest="0" * 64),
            "review digest does not match sample",
        ),
    ],
)
def test_review_gate_rejects_incomplete_or_stale_evidence(
    mutation,
    message,
    tmp_path,
    monkeypatch,
):
    _, checker = _load_modules()
    taxonomy = _use_test_policy(checker, monkeypatch)
    sample, review = _evidence(tmp_path, taxonomy)
    mutation(sample, review)
    with pytest.raises(checker.ReviewEvidenceError, match=message):
        checker.check_review(sample, review, min_accuracy=0.8)


def test_review_gate_rejects_low_per_category_accuracy(tmp_path, monkeypatch):
    _, checker = _load_modules()
    taxonomy = _use_test_policy(checker, monkeypatch)
    sample, review = _evidence(tmp_path, taxonomy)
    review["reviews"][0]["expected_category"] = "data"
    with pytest.raises(checker.ReviewEvidenceError, match="accuracy.*below"):
        checker.check_review(sample, review, min_accuracy=0.8)


def test_review_gate_rejects_sources_changed_after_sampling(tmp_path, monkeypatch):
    _, checker = _load_modules()
    taxonomy = _use_test_policy(checker, monkeypatch)
    sample, review = _evidence(tmp_path, taxonomy)
    source_path = Path(sample["skills_dir"]) / sample["strata"][0]["samples"][0]["path"]
    source_path.write_text("changed after review\n", encoding="utf-8")

    with pytest.raises(
        checker.ReviewEvidenceError,
        match="sample no longer matches current population",
    ):
        checker.check_review(sample, review, min_accuracy=0.8)


def test_review_gate_rejects_noncanonical_sampling_policy(tmp_path):
    _, checker = _load_modules()
    sample, review = _evidence(tmp_path, _test_taxonomy())
    with pytest.raises(
        checker.ReviewEvidenceError,
        match="sample policy does not match canonical taxonomy",
    ):
        checker.check_review(sample, review, min_accuracy=0.8)


def test_review_gate_cli_reports_pass_and_failure(
    tmp_path,
    monkeypatch,
    capsys,
):
    _, checker = _load_modules()
    taxonomy = _use_test_policy(checker, monkeypatch)
    sample, review = _evidence(tmp_path, taxonomy)
    sample_path = tmp_path / "sample.json"
    review_path = tmp_path / "review.json"
    sample_path.write_text(json.dumps(sample), encoding="utf-8")
    review_path.write_text(json.dumps(review), encoding="utf-8")

    assert checker.main(
        ["--sample", str(sample_path), "--review", str(review_path)]
    ) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "passed"

    review["reviews"].pop()
    review_path.write_text(json.dumps(review), encoding="utf-8")
    assert checker.main(
        ["--sample", str(sample_path), "--review", str(review_path)]
    ) == 1
    assert json.loads(capsys.readouterr().out)["status"] == "failed"


def test_review_gate_rejects_archive_population_changes(tmp_path, monkeypatch):
    _, checker = _load_modules()
    taxonomy = _use_test_policy(checker, monkeypatch)
    sample, review = _evidence(tmp_path, taxonomy)
    new_skill = Path(sample["skills_dir"]) / "integration" / "new-skill"
    new_skill.mkdir(parents=True)
    (new_skill / "SKILL.md").write_text(
        "---\nname: new-skill\n---\n",
        encoding="utf-8",
    )
    (new_skill / "metadata.json").write_text(
        '{"name":"new-skill","category":"integration"}\n',
        encoding="utf-8",
    )

    with pytest.raises(
        checker.ReviewEvidenceError,
        match="sample no longer matches current population",
    ):
        checker.check_review(sample, review, min_accuracy=0.8)
