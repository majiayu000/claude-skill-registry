from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    return importlib.import_module("classify_residual_workset_with_llm")


class FakeClient:
    def __init__(self, responses: list[str | Exception]):
        self.responses = responses
        self.messages: list[list[dict[str, str]]] = []

    def complete(self, messages: list[dict[str, str]]) -> str:
        self.messages.append(messages)
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


def _work_item(path: str, *, workset: str = "classification_gap") -> dict:
    return {
        "workset": workset,
        "reason": "test",
        "path": path,
        "name": path.split("/")[-1],
        "description": "Build and test source code",
        "tags": ["code", "test"],
        "current_category": "other",
        "metadata": {"repo": "owner/repo", "path": ".claude/skills/test/SKILL.md"},
        "previous_classification": {},
        "source_sha256": f"skill-{path}",
        "metadata_sha256": f"metadata-{path}",
        "semantic_text_sha256": f"semantic-{path}",
        "content_excerpt": "Use this skill for coding workflows and unit tests.",
    }


def _write_workset(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def test_batch_classification_accepts_json_array_and_writes_apply_rows(tmp_path):
    classifier = _load_module()
    workset = tmp_path / "workset.jsonl"
    _write_workset(workset, [_work_item("other/dev"), _work_item("other/docs")])
    client = FakeClient(
        [
            json.dumps(
                [
                    {
                        "id": "0",
                        "category": "development",
                        "confidence": 0.94,
                        "reason": "coding workflow",
                        "evidence": ["unit tests"],
                    },
                    {
                        "id": "1",
                        "category": "documents",
                        "confidence": 0.91,
                        "reason": "document workflow",
                        "evidence": ["docs"],
                    },
                ]
            )
        ]
    )

    report = classifier.run_classification(
        workset_jsonl=workset,
        client=client,
        checkpoint_jsonl=tmp_path / "checkpoint.jsonl",
        resume=False,
        limit=None,
        batch_size=2,
        workers=1,
        sleep_seconds=0,
    )
    output = tmp_path / "classification.jsonl"
    classifier.write_classification_jsonl(report, output)
    rows = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]

    assert len(client.messages) == 1
    assert report["summary"]["status_counts"] == {"ok": 2}
    assert report["summary"]["category_counts"] == {
        "development": 1,
        "documents": 1,
    }
    assert rows[0]["path"] == "other/dev"
    assert rows[0]["llm_category"] == "development"
    assert rows[0]["status"] == "ok"
    assert rows[0]["workset"] == "classification_gap"
    assert rows[0]["source_sha256"] == "skill-other/dev"
    assert rows[0]["metadata_sha256"] == "metadata-other/dev"
    assert rows[0]["semantic_text_sha256"] == "semantic-other/dev"


def test_batch_classification_accepts_fenced_json_array(tmp_path):
    classifier = _load_module()
    workset = tmp_path / "workset.jsonl"
    _write_workset(workset, [_work_item("other/research")])
    client = FakeClient(
        [
            """```json
[
  {
    "id": "0",
    "category": "analysis",
    "confidence": 0.92,
    "reason": "research workflow",
    "evidence": ["analysis"]
  }
]
```"""
        ]
    )

    report = classifier.run_classification(
        workset_jsonl=workset,
        client=client,
        checkpoint_jsonl=None,
        resume=False,
        limit=None,
        batch_size=1,
        workers=1,
        sleep_seconds=0,
    )

    assert report["summary"]["status_counts"] == {"ok": 1}
    assert report["rows"][0]["llm_category"] == "analysis"


def test_resume_uses_checkpoint_without_calling_client(tmp_path):
    classifier = _load_module()
    item = _work_item("other/reused")
    workset = tmp_path / "workset.jsonl"
    _write_workset(workset, [item])
    key = classifier.item_review_key({**item, "_input_index": 0})
    checkpoint = tmp_path / "checkpoint.jsonl"
    checkpoint.write_text(
        json.dumps(
            {
                "review_key": key,
                "path": "other/reused",
                "name": "reused",
                "current_category": "other",
                "llm_category": "development",
                "confidence": 0.93,
                "status": "ok",
                "reason": "checkpoint",
                "evidence": [],
                "workset": "classification_gap",
                "input_index": 0,
            }
        )
        + "\n",
        encoding="utf-8",
    )
    client = FakeClient([])

    report = classifier.run_classification(
        workset_jsonl=workset,
        client=client,
        checkpoint_jsonl=checkpoint,
        resume=True,
        limit=None,
        batch_size=1,
        workers=1,
        sleep_seconds=0,
    )

    assert client.messages == []
    assert report["summary"]["skipped_checkpoint_count"] == 1
    assert report["summary"]["ignored_checkpoint_row_count"] == 0
    assert report["summary"]["new_review_count"] == 0
    assert report["rows"][0]["reason"] == "checkpoint"


def test_resume_retries_non_ok_checkpoint_rows(tmp_path):
    classifier = _load_module()
    item = _work_item("other/retry-checkpoint")
    workset = tmp_path / "workset.jsonl"
    _write_workset(workset, [item])
    key = classifier.item_review_key({**item, "_input_index": 0})
    checkpoint = tmp_path / "checkpoint.jsonl"
    checkpoint.write_text(
        json.dumps(
            {
                "review_key": key,
                "path": "other/retry-checkpoint",
                "name": "retry-checkpoint",
                "current_category": "other",
                "llm_category": "",
                "confidence": None,
                "status": "api_error",
                "reason": "rate limited",
                "evidence": [],
                "workset": "classification_gap",
                "input_index": 0,
            }
        )
        + "\n",
        encoding="utf-8",
    )
    client = FakeClient(
        [
            json.dumps(
                [
                    {
                        "id": "0",
                        "category": "development",
                        "confidence": 0.91,
                        "reason": "retried",
                        "evidence": ["code"],
                    }
                ]
            )
        ]
    )

    report = classifier.run_classification(
        workset_jsonl=workset,
        client=client,
        checkpoint_jsonl=checkpoint,
        resume=True,
        limit=None,
        batch_size=1,
        workers=1,
        sleep_seconds=0,
        checkpoint_reuse_statuses={"ok"},
    )

    assert len(client.messages) == 1
    assert report["summary"]["ignored_checkpoint_row_count"] == 1
    assert report["summary"]["status_counts"] == {"ok": 1}
    assert report["rows"][0]["reason"] == "retried"


def test_batch_classification_can_match_by_path_or_position(tmp_path):
    classifier = _load_module()
    workset = tmp_path / "workset.jsonl"
    _write_workset(workset, [_work_item("other/by-path"), _work_item("other/by-position")])
    client = FakeClient(
        [
            json.dumps(
                [
                    {
                        "path": "other/by-path",
                        "category": "development",
                        "confidence": 0.91,
                        "reason": "path match",
                        "evidence": ["code"],
                    },
                    {
                        "category": "documents",
                        "confidence": 0.92,
                        "reason": "position match",
                        "evidence": ["docs"],
                    },
                ]
            )
        ]
    )

    report = classifier.run_classification(
        workset_jsonl=workset,
        client=client,
        checkpoint_jsonl=None,
        resume=False,
        limit=None,
        batch_size=2,
        workers=1,
        sleep_seconds=0,
    )

    assert report["summary"]["status_counts"] == {"ok": 2}
    assert [row["llm_category"] for row in report["rows"]] == [
        "development",
        "documents",
    ]


def test_prompt_payload_includes_taxonomy_boundaries_and_blocked_labels():
    classifier = _load_module()

    messages = classifier.build_messages([{**_work_item("other/automation"), "_batch_id": "0"}])
    prompt_payload = json.loads(messages[1]["content"])

    categories = {item["slug"]: item for item in prompt_payload["allowed_categories"]}
    assert "automation" not in categories
    assert categories["development"]["inclusion_rule"]
    assert categories["development"]["exclusion_rule"]
    assert categories["development"]["examples"]
    assert categories["development"]["keywords"]

    contract = prompt_payload["taxonomy_contract"]
    assert contract["source"] == "taxonomy/categories.yaml active categories only"
    assert "allowed_categories" in contract["valid_category_rule"]
    assert "last-resort" in contract["other_rule"]
    blocked_slugs = {item["blocked_slug"] for item in contract["noncanonical_category_guidance"]}
    assert blocked_slugs == {"automation", "research", "education", "content"}
    automation_guidance = next(
        item
        for item in contract["noncanonical_category_guidance"]
        if item["blocked_slug"] == "automation"
    )
    assert {target["slug"] for target in automation_guidance["active_targets"]} >= {
        "workflow",
        "productivity",
        "devops",
        "orchestration",
        "integration",
        "platform",
    }
    assert "non-canonical category labels" in messages[0]["content"]


def test_invalid_model_category_fails_closed(tmp_path):
    classifier = _load_module()
    workset = tmp_path / "workset.jsonl"
    _write_workset(workset, [_work_item("other/bad")])
    client = FakeClient(
        [
            json.dumps(
                [
                    {
                        "id": "0",
                        "category": "not-a-real-category",
                        "confidence": 0.99,
                        "reason": "bad",
                        "evidence": [],
                    }
                ]
            )
        ]
    )

    report = classifier.run_classification(
        workset_jsonl=workset,
        client=client,
        checkpoint_jsonl=None,
        resume=False,
        limit=None,
        batch_size=1,
        workers=1,
        sleep_seconds=0,
    )

    assert report["summary"]["status_counts"] == {"unknown_or_inactive_category": 1}
    assert report["rows"][0]["llm_category"] == "not-a-real-category"


def test_blocked_natural_label_from_model_fails_closed(tmp_path):
    classifier = _load_module()
    workset = tmp_path / "workset.jsonl"
    _write_workset(workset, [_work_item("other/automation")])
    client = FakeClient(
        [
            json.dumps(
                [
                    {
                        "id": "0",
                        "category": "automation",
                        "confidence": 0.99,
                        "reason": "broad label",
                        "evidence": [],
                    }
                ]
            )
        ]
    )

    report = classifier.run_classification(
        workset_jsonl=workset,
        client=client,
        checkpoint_jsonl=None,
        resume=False,
        limit=None,
        batch_size=1,
        workers=1,
        sleep_seconds=0,
    )

    assert report["summary"]["status_counts"] == {"unknown_or_inactive_category": 1}
    assert report["rows"][0]["llm_category"] == "automation"


def test_api_errors_are_retried_before_fail_closed(tmp_path):
    classifier = _load_module()
    workset = tmp_path / "workset.jsonl"
    _write_workset(workset, [_work_item("other/retry")])
    client = FakeClient(
        [
            classifier.LLMReviewError("rate limited"),
            json.dumps(
                [
                    {
                        "id": "0",
                        "category": "development",
                        "confidence": 0.91,
                        "reason": "coding",
                        "evidence": ["tests"],
                    }
                ]
            ),
        ]
    )

    report = classifier.run_classification(
        workset_jsonl=workset,
        client=client,
        checkpoint_jsonl=None,
        resume=False,
        limit=None,
        batch_size=1,
        workers=1,
        sleep_seconds=0,
        retries=1,
        retry_sleep_seconds=0,
    )

    assert len(client.messages) == 2
    assert report["summary"]["status_counts"] == {"ok": 1}
    assert report["rows"][0]["llm_category"] == "development"
