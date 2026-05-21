from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from urllib.error import HTTPError

import pytest


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    return importlib.import_module("review_category_plan_with_llm")


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


class FakeResponse:
    def __init__(self, payload: dict):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def read(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")


class FakeErrorBody:
    def read(self) -> bytes:
        return b'{"error":{"message":"bad request"}}'

    def close(self) -> None:
        return None


def _change(
    path: str,
    *,
    confidence: str,
    proposed_category: str,
    action: str = "heuristic_reclassify",
) -> dict:
    return {
        "path": path,
        "name": path.split("/")[-2],
        "action": action,
        "confidence": confidence,
        "current_category": "other",
        "proposed_category": proposed_category,
        "raw_sources": {"directory": "other"},
        "resolved_sources": {"directory": "other"},
        "signals": ["video"],
        "reason": "keyword match",
        "score": 4,
        "current_score": 0,
    }


def test_review_report_records_agree_override_and_uncertain():
    reviewer = _load_module()
    plan = {
        "changes": [
            _change("other/high/SKILL.md", confidence="high", proposed_category="devops"),
            _change("other/low/SKILL.md", confidence="low", proposed_category="data"),
            _change("other/medium/SKILL.md", confidence="medium", proposed_category="marketing"),
        ]
    }
    client = FakeClient(
        [
            '{"category":"documents","confidence":0.91,"reason":"doc workflow","evidence":["pdf"]}',
            '{"category":"marketing","confidence":0.99,"reason":"campaign copy","evidence":["seo"]}',
            '{"category":"not-a-category","confidence":0.95,"reason":"bad","evidence":[]}',
        ]
    )

    report = reviewer.build_review_report(
        plan,
        client=client,
        model="mimo-v2.5-pro",
        base_url="https://token-plan-sgp.xiaomimimo.com/v1",
        api_key_env="MIMO_API_KEY",
        limit=3,
    )

    assert [review["path"] for review in report["reviews"]] == [
        "other/low/SKILL.md",
        "other/medium/SKILL.md",
        "other/high/SKILL.md",
    ]
    assert report["reviews"][0]["decision"] == "override"
    assert report["reviews"][0]["llm_proposed_category"] == "documents"
    assert report["reviews"][1]["decision"] == "agree"
    assert report["reviews"][2]["decision"] == "uncertain"
    assert report["reviews"][2]["parse_status"] == "unknown_category"
    assert report["summary"]["decision_counts"] == {
        "agree": 1,
        "override": 1,
        "uncertain": 1,
    }
    assert report["policy"]["apply_mode"] == "review-only"
    assert "MIMO_API_KEY" in report["notes"][1]


def test_openai_compatible_client_posts_chat_completion(monkeypatch):
    reviewer = _load_module()
    captured = {}

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["timeout"] = timeout
        captured["headers"] = dict(request.header_items())
        captured["payload"] = json.loads(request.data.decode("utf-8"))
        return FakeResponse(
            {
                "choices": [
                    {
                        "message": {
                            "content": '{"category":"data","confidence":0.8,"reason":"etl","evidence":[]}'
                        }
                    }
                ]
            }
        )

    monkeypatch.setattr(reviewer, "urlopen", fake_urlopen)
    client = reviewer.OpenAICompatibleClient(
        api_key="secret",
        base_url="https://example.test/v1/",
        model="m",
        timeout=7,
        max_completion_tokens=123,
    )

    content = client.complete([{"role": "user", "content": "hello"}])

    assert content == '{"category":"data","confidence":0.8,"reason":"etl","evidence":[]}'
    assert captured["url"] == "https://example.test/v1/chat/completions"
    assert captured["timeout"] == 7
    assert captured["headers"]["Authorization"] == "Bearer secret"
    assert captured["payload"]["model"] == "m"
    assert captured["payload"]["max_completion_tokens"] == 123
    assert captured["payload"]["stream"] is False


def test_openai_compatible_client_reports_api_shape_errors(monkeypatch):
    reviewer = _load_module()
    monkeypatch.setattr(reviewer, "urlopen", lambda request, timeout: FakeResponse({"choices": []}))
    client = reviewer.OpenAICompatibleClient(api_key="secret")

    with pytest.raises(reviewer.LLMReviewError, match="did not include choices"):
        client.complete([{"role": "user", "content": "hello"}])


def test_openai_compatible_client_reports_http_errors(monkeypatch):
    reviewer = _load_module()

    def fake_urlopen(request, timeout):
        raise HTTPError(
            request.full_url,
            401,
            "Unauthorized",
            hdrs=None,
            fp=FakeErrorBody(),
        )

    monkeypatch.setattr(reviewer, "urlopen", fake_urlopen)
    client = reviewer.OpenAICompatibleClient(api_key="secret")

    with pytest.raises(reviewer.LLMReviewError, match="HTTP 401"):
        client.complete([{"role": "user", "content": "hello"}])


def test_review_report_filters_actions_and_confidences():
    reviewer = _load_module()
    plan = {
        "changes": [
            _change("other/a/SKILL.md", confidence="high", proposed_category="devops"),
            _change(
                "other/b/SKILL.md",
                confidence="low",
                proposed_category="data",
                action="resolve_source_conflict",
            ),
            _change("other/c/SKILL.md", confidence="low", proposed_category="security"),
        ]
    }
    client = FakeClient(
        ['{"category":"security","confidence":0.7,"reason":"audit","evidence":["scan"]}']
    )

    report = reviewer.build_review_report(
        plan,
        client=client,
        model="m",
        base_url="u",
        api_key_env="KEY",
        actions={"heuristic_reclassify"},
        confidences={"low"},
        limit=10,
    )

    assert len(client.messages) == 1
    assert report["reviews"][0]["path"] == "other/c/SKILL.md"
    assert report["reviews"][0]["decision"] == "agree"
    prompt_payload = json.loads(client.messages[0][1]["content"])
    assert prompt_payload["candidate"]["path"] == "other/c/SKILL.md"
    assert {item["slug"] for item in prompt_payload["allowed_categories"]} >= {
        "security",
        "data",
    }
    assert "docs" not in {item["slug"] for item in prompt_payload["allowed_categories"]}


def test_review_report_can_preserve_plan_order_sleep_and_raw(monkeypatch):
    reviewer = _load_module()
    plan = {
        "changes": [
            _change("other/high/SKILL.md", confidence="high", proposed_category="data"),
            _change("other/low/SKILL.md", confidence="low", proposed_category="data"),
        ]
    }
    client = FakeClient(
        [
            '{"category":"data","confidence":0.5,"reason":"match","evidence":[]}',
            '{"category":"data","confidence":0.5,"reason":"match","evidence":[]}',
        ]
    )
    sleeps = []
    monkeypatch.setattr(reviewer.time, "sleep", sleeps.append)

    report = reviewer.build_review_report(
        plan,
        client=client,
        model="m",
        base_url="u",
        api_key_env="KEY",
        limit=None,
        priority="plan",
        sleep_seconds=0.25,
        include_raw=True,
    )

    assert [review["path"] for review in report["reviews"]] == [
        "other/high/SKILL.md",
        "other/low/SKILL.md",
    ]
    assert sleeps == [0.25]
    assert report["reviews"][0]["raw_response"].startswith('{"category":"data"')


def test_candidate_review_key_changes_when_candidate_changes():
    reviewer = _load_module()
    first = _change("other/a/SKILL.md", confidence="low", proposed_category="data")
    second = _change("other/a/SKILL.md", confidence="low", proposed_category="security")

    assert reviewer.candidate_review_key(first) != reviewer.candidate_review_key(second)


def test_review_report_writes_checkpoint_and_resume_skips_completed(tmp_path):
    reviewer = _load_module()
    checkpoint_path = tmp_path / "review.checkpoint.jsonl"
    plan = {
        "changes": [
            _change("other/a/SKILL.md", confidence="low", proposed_category="data"),
            _change("other/b/SKILL.md", confidence="medium", proposed_category="security"),
        ]
    }
    client = FakeClient(
        [
            '{"category":"data","confidence":0.9,"reason":"etl","evidence":["csv"]}',
            '{"category":"security","confidence":0.9,"reason":"audit","evidence":["scan"]}',
        ]
    )

    report = reviewer.build_review_report(
        plan,
        client=client,
        model="m",
        base_url="u",
        api_key_env="KEY",
        limit=2,
        checkpoint_path=checkpoint_path,
    )

    checkpoint_rows = [
        json.loads(line) for line in checkpoint_path.read_text(encoding="utf-8").splitlines()
    ]
    assert len(client.messages) == 2
    assert len(checkpoint_rows) == 2
    assert {row["review_key"] for row in checkpoint_rows} == {
        review["review_key"] for review in report["reviews"]
    }
    assert report["summary"]["new_review_count"] == 2
    assert report["summary"]["skipped_checkpoint_count"] == 0

    resume_client = FakeClient([])
    resumed = reviewer.build_review_report(
        plan,
        client=resume_client,
        model="m",
        base_url="u",
        api_key_env="KEY",
        limit=2,
        checkpoint_path=checkpoint_path,
        resume=True,
    )

    assert resume_client.messages == []
    assert [review["path"] for review in resumed["reviews"]] == [
        "other/a/SKILL.md",
        "other/b/SKILL.md",
    ]
    assert resumed["summary"]["new_review_count"] == 0
    assert resumed["summary"]["skipped_checkpoint_count"] == 2
    assert checkpoint_path.read_text(encoding="utf-8").count("\n") == 2


def test_resume_ignores_malformed_checkpoint_rows(tmp_path):
    reviewer = _load_module()
    change = _change("other/a/SKILL.md", confidence="low", proposed_category="data")
    review_key = reviewer.candidate_review_key(change)
    checkpoint_path = tmp_path / "review.checkpoint.jsonl"
    checkpoint_path.write_text(
        "not-json\n"
        + json.dumps(
            {
                "review_key": review_key,
                "path": "other/a/SKILL.md",
                "name": "a",
                "action": "heuristic_reclassify",
                "current_category": "other",
                "heuristic_proposed_category": "data",
                "llm_proposed_category": "data",
                "llm_confidence": 0.9,
                "decision": "agree",
                "parse_status": "ok",
                "review_required": True,
                "reason": "checkpointed",
                "evidence": [],
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    report = reviewer.build_review_report(
        {"changes": [change]},
        client=FakeClient([]),
        model="m",
        base_url="u",
        api_key_env="KEY",
        checkpoint_path=checkpoint_path,
        resume=True,
    )

    assert report["reviews"][0]["reason"] == "checkpointed"
    assert report["summary"]["malformed_checkpoint_row_count"] == 1
    assert report["summary"]["skipped_checkpoint_count"] == 1


def test_review_report_marks_api_error_without_raising():
    reviewer = _load_module()
    client = FakeClient([reviewer.LLMReviewError("temporary outage")])

    report = reviewer.build_review_report(
        {"changes": [_change("other/a/SKILL.md", confidence="low", proposed_category="data")]},
        client=client,
        model="m",
        base_url="u",
        api_key_env="KEY",
    )

    assert report["reviews"][0]["decision"] == "uncertain"
    assert report["reviews"][0]["parse_status"] == "api_error"
    assert "temporary outage" in report["reviews"][0]["reason"]


def test_parse_json_content_accepts_markdown_fence_and_rejects_non_objects():
    reviewer = _load_module()

    payload, status = reviewer.parse_json_content(
        '```json\n{"category":"data","confidence":0.8,"reason":"etl","evidence":["csv"]}\n```'
    )

    assert status == "ok"
    assert payload == {
        "category": "data",
        "confidence": 0.8,
        "reason": "etl",
        "evidence": ["csv"],
    }
    assert reviewer.parse_json_content("not-json") == (None, "invalid_json")
    assert reviewer.parse_json_content("[1, 2, 3]") == (None, "invalid_json")
    assert reviewer.normalized_confidence(True) is None
    assert reviewer.normalized_confidence(1.5) is None


def test_main_requires_api_key(monkeypatch, tmp_path):
    reviewer = _load_module()
    plan_path = tmp_path / "plan.json"
    plan_path.write_text('{"changes":[]}', encoding="utf-8")
    monkeypatch.delenv("MIMO_API_KEY", raising=False)

    with pytest.raises(SystemExit, match="Missing API key environment variable"):
        reviewer.main(["--plan", str(plan_path)])


def test_main_requires_checkpoint_for_resume(monkeypatch, tmp_path):
    reviewer = _load_module()
    plan_path = tmp_path / "plan.json"
    plan_path.write_text('{"changes":[]}', encoding="utf-8")
    monkeypatch.setenv("MIMO_API_KEY", "secret")

    with pytest.raises(SystemExit, match="--resume requires --checkpoint-jsonl"):
        reviewer.main(["--plan", str(plan_path), "--resume"])


def test_main_rejects_same_output_and_checkpoint(monkeypatch, tmp_path):
    reviewer = _load_module()
    plan_path = tmp_path / "plan.json"
    output_path = tmp_path / "review.json"
    plan_path.write_text('{"changes":[]}', encoding="utf-8")
    monkeypatch.setenv("MIMO_API_KEY", "secret")

    with pytest.raises(SystemExit, match="must be different paths"):
        reviewer.main(
            [
                "--plan",
                str(plan_path),
                "--output",
                str(output_path),
                "--checkpoint-jsonl",
                str(output_path),
            ]
        )


def test_main_writes_json_report(monkeypatch, tmp_path, capsys):
    reviewer = _load_module()
    plan_path = tmp_path / "plan.json"
    output_path = tmp_path / "review.json"
    checkpoint_path = tmp_path / "review.checkpoint.jsonl"
    plan_path.write_text(
        json.dumps(
            {
                "changes": [
                    _change("other/a/SKILL.md", confidence="low", proposed_category="data")
                ]
            }
        ),
        encoding="utf-8",
    )

    class FakeOpenAICompatibleClient:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

        def complete(self, messages):
            return '{"category":"data","confidence":0.9,"reason":"etl","evidence":["csv"]}'

    monkeypatch.setenv("MIMO_API_KEY", "secret")
    monkeypatch.setattr(reviewer, "OpenAICompatibleClient", FakeOpenAICompatibleClient)

    assert (
        reviewer.main(
            [
                "--plan",
                str(plan_path),
                "--output",
                str(output_path),
                "--json",
                "--limit",
                "1",
                "--checkpoint-jsonl",
                str(checkpoint_path),
            ]
        )
        == 0
    )
    stdout = capsys.readouterr().out
    output = json.loads(output_path.read_text(encoding="utf-8"))
    assert json.loads(stdout)["summary"]["reviewed_count"] == 1
    assert output["reviews"][0]["decision"] == "agree"
    assert checkpoint_path.exists()
