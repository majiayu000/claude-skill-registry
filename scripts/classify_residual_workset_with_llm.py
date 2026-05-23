#!/usr/bin/env python3
"""Batch-classify residual category worksets with an OpenAI-compatible model."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from category_taxonomy import get_taxonomy
from review_category_plan_with_llm import (
    DEFAULT_API_KEY_ENV,
    DEFAULT_BASE_URL,
    DEFAULT_MAX_COMPLETION_TOKENS,
    DEFAULT_MODEL,
    DEFAULT_THINKING,
    LLMReviewError,
    OpenAICompatibleClient,
    parse_json_content,
)

CHECKPOINT_SCHEMA_VERSION = 1


def active_category_payload() -> list[dict[str, str]]:
    taxonomy = get_taxonomy()
    return [
        {
            "slug": definition.slug,
            "display_name": definition.display_name,
            "description": definition.description,
        }
        for definition in sorted(taxonomy.categories.values(), key=lambda item: item.slug)
        if definition.status == "active"
    ]


def load_work_items(path: Path, *, limit: int | None = None) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            payload = json.loads(line)
            if not isinstance(payload, dict):
                raise ValueError(f"work item row {line_number} must be an object")
            payload["_input_index"] = len(items)
            items.append(payload)
            if limit is not None and len(items) >= max(limit, 0):
                break
    return items


def item_review_key(item: dict[str, Any]) -> str:
    payload = {
        "workset": item.get("workset", ""),
        "path": item.get("path", ""),
        "name": item.get("name", ""),
        "description": item.get("description", ""),
        "tags": item.get("tags", []),
        "previous_classification": item.get("previous_classification", {}),
        "content_excerpt": item.get("content_excerpt", ""),
    }
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def load_checkpoint(
    path: Path | None,
    *,
    reusable_statuses: set[str] | None = None,
) -> tuple[dict[str, dict[str, Any]], int, int]:
    if path is None or not path.exists():
        return {}, 0, 0
    rows: dict[str, dict[str, Any]] = {}
    malformed = 0
    ignored = 0
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                malformed += 1
                continue
            if not isinstance(payload, dict) or not isinstance(payload.get("review_key"), str):
                malformed += 1
                continue
            status = str(payload.get("status") or "")
            if reusable_statuses is not None and status not in reusable_statuses:
                ignored += 1
                continue
            rows[payload["review_key"]] = payload
    return rows, malformed, ignored


def append_checkpoint(path: Path, row: dict[str, Any], lock: threading.Lock) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with lock:
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            handle.flush()


def compact_candidate(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": item["_batch_id"],
        "workset": item.get("workset", ""),
        "reason": item.get("reason", ""),
        "path": item.get("path", ""),
        "name": item.get("name", ""),
        "description": item.get("description", ""),
        "tags": item.get("tags", []),
        "current_category": item.get("current_category", ""),
        "metadata": item.get("metadata", {}),
        "previous_classification": item.get("previous_classification", {}),
        "content_excerpt": item.get("content_excerpt", ""),
    }


def build_messages(items: list[dict[str, Any]]) -> list[dict[str, str]]:
    categories = active_category_payload()
    system_prompt = (
        "You are classifying reusable AI skills into a registry taxonomy. "
        "Use SKILL.md frontmatter/body semantics first, then metadata and path. "
        "Choose one category slug from allowed_categories. Prefer a concrete active "
        "category over 'other'. Use 'other' only when no active category is defensible, "
        "and then set confidence <= 0.65. Do not choose review or deprecated categories. "
        "Return only valid compact JSON: an array of objects with keys "
        "id, category, confidence, reason, evidence. confidence must be 0..1."
    )
    payload = {
        "allowed_categories": categories,
        "candidates": [compact_candidate(item) for item in items],
    }
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
    ]


def parse_batch_content(content: str) -> tuple[list[dict[str, Any]] | None, str]:
    parsed, status = parse_json_content(content)
    if status == "ok" and isinstance(parsed, dict):
        for key in ("classifications", "items", "results"):
            value = parsed.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)], "ok"
        return None, "invalid_json"
    if status == "ok" and isinstance(parsed, list):
        return [item for item in parsed if isinstance(item, dict)], "ok"
    stripped = strip_json_fence(content)
    if stripped.startswith("["):
        try:
            value = json.loads(stripped)
        except json.JSONDecodeError:
            return None, "invalid_json"
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)], "ok"
    return None, status


def strip_json_fence(content: str) -> str:
    stripped = content.strip()
    if not stripped.startswith("```"):
        return stripped
    lines = stripped.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


def normalized_confidence(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int | float):
        confidence = float(value)
        if 0.0 <= confidence <= 1.0:
            return confidence
    return None


def build_result_entry(
    item: dict[str, Any],
    *,
    review_key: str,
    model_payload: dict[str, Any] | None,
    parse_status: str,
    raw_error: str = "",
) -> dict[str, Any]:
    taxonomy = get_taxonomy()
    category = ""
    confidence = None
    reason = raw_error
    evidence: list[Any] = []
    status = parse_status
    if model_payload:
        raw_category = str(model_payload.get("category") or "")
        category = taxonomy.resolve(raw_category, allow_unknown=True) if raw_category else ""
        confidence = normalized_confidence(model_payload.get("confidence"))
        reason = str(model_payload.get("reason") or "")
        raw_evidence = model_payload.get("evidence")
        evidence = raw_evidence if isinstance(raw_evidence, list) else []
        definition = taxonomy.categories.get(category)
        if status == "ok" and (not definition or definition.status != "active"):
            status = "unknown_or_inactive_category"
        if status == "ok" and confidence is None:
            status = "invalid_confidence"
    return {
        "checkpoint_schema_version": CHECKPOINT_SCHEMA_VERSION,
        "review_key": review_key,
        "path": item.get("path", ""),
        "name": item.get("name", ""),
        "current_category": item.get("current_category", ""),
        "llm_category": category,
        "confidence": confidence,
        "status": status,
        "reason": reason,
        "evidence": evidence,
        "workset": item.get("workset", ""),
        "previous_classification": item.get("previous_classification", {}),
        "input_index": item.get("_input_index"),
    }


def classify_batch(
    batch: list[dict[str, Any]],
    *,
    client: OpenAICompatibleClient,
    retries: int = 0,
    retry_sleep_seconds: float = 2.0,
) -> list[dict[str, Any]]:
    for index, item in enumerate(batch):
        item["_batch_id"] = str(index)
    keys = [item_review_key(item) for item in batch]
    last_error = ""
    for attempt in range(max(retries, 0) + 1):
        try:
            content = client.complete(build_messages(batch))
            parsed, parse_status = parse_batch_content(content)
            break
        except LLMReviewError as exc:
            last_error = str(exc)
            if attempt >= max(retries, 0):
                return [
                    build_result_entry(
                        item,
                        review_key=key,
                        model_payload=None,
                        parse_status="api_error",
                        raw_error=last_error,
                    )
                    for item, key in zip(batch, keys, strict=True)
                ]
            if retry_sleep_seconds > 0:
                time.sleep(retry_sleep_seconds * (attempt + 1))
    parsed_items = parsed or []
    payload_by_id = {
        str(payload.get("id")): payload for payload in parsed_items if "id" in payload
    }
    payload_by_path = {
        str(payload.get("path")): payload
        for payload in parsed_items
        if isinstance(payload.get("path"), str)
    }
    payload_by_position = (
        {str(index): payload for index, payload in enumerate(parsed_items)}
        if parse_status == "ok" and len(parsed_items) == len(batch)
        else {}
    )
    entries: list[dict[str, Any]] = []
    for item, key in zip(batch, keys, strict=True):
        payload = (
            payload_by_id.get(str(item["_batch_id"]))
            or payload_by_path.get(str(item.get("path", "")))
            or payload_by_position.get(str(item["_batch_id"]))
        )
        status = parse_status if payload is not None else "missing_result"
        entries.append(
            build_result_entry(
                item,
                review_key=key,
                model_payload=payload,
                parse_status=status,
            )
        )
    return entries


def chunks(items: list[dict[str, Any]], size: int) -> list[list[dict[str, Any]]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def run_classification(
    *,
    workset_jsonl: Path,
    client: OpenAICompatibleClient,
    checkpoint_jsonl: Path | None,
    resume: bool,
    limit: int | None,
    batch_size: int,
    workers: int,
    sleep_seconds: float,
    retries: int = 0,
    retry_sleep_seconds: float = 2.0,
    checkpoint_reuse_statuses: set[str] | None = None,
) -> dict[str, Any]:
    items = load_work_items(workset_jsonl, limit=limit)
    checkpoint_rows, malformed, ignored = load_checkpoint(
        checkpoint_jsonl if resume else None,
        reusable_statuses=checkpoint_reuse_statuses if resume else None,
    )
    checkpoint_lock = threading.Lock()
    selected: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []
    skipped = 0
    for item in items:
        key = item_review_key(item)
        if key in checkpoint_rows:
            results.append(checkpoint_rows[key])
            skipped += 1
        else:
            selected.append(item)

    batches = chunks(selected, max(batch_size, 1))
    if workers <= 1:
        for batch_number, batch in enumerate(batches):
            if batch_number and sleep_seconds > 0:
                time.sleep(sleep_seconds)
            entries = classify_batch(
                batch,
                client=client,
                retries=retries,
                retry_sleep_seconds=retry_sleep_seconds,
            )
            for entry in entries:
                if checkpoint_jsonl:
                    append_checkpoint(checkpoint_jsonl, entry, checkpoint_lock)
                results.append(entry)
    else:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(
                    classify_batch,
                    batch,
                    client=client,
                    retries=retries,
                    retry_sleep_seconds=retry_sleep_seconds,
                ): batch
                for batch in batches
            }
            for future in as_completed(futures):
                entries = future.result()
                for entry in entries:
                    if checkpoint_jsonl:
                        append_checkpoint(checkpoint_jsonl, entry, checkpoint_lock)
                    results.append(entry)
                if sleep_seconds > 0:
                    time.sleep(sleep_seconds)

    results.sort(key=lambda row: int(row.get("input_index") or 0))
    status_counts = Counter(str(row.get("status") or "") for row in results)
    category_counts = Counter(str(row.get("llm_category") or "") for row in results)
    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "workset_jsonl": str(workset_jsonl),
        "summary": {
            "input_count": len(items),
            "reviewed_count": len(results),
            "new_review_count": len(selected),
            "skipped_checkpoint_count": skipped,
            "malformed_checkpoint_row_count": malformed,
            "ignored_checkpoint_row_count": ignored,
            "status_counts": dict(sorted(status_counts.items())),
            "category_counts": dict(sorted(category_counts.items())),
        },
        "rows": results,
        "notes": [
            "This report does not modify archive files.",
            "Rows with status ok are compatible with apply_category_migration.py classification input.",
            "API credentials are read from the selected environment variable and are not written to output.",
        ],
    }


def write_classification_jsonl(report: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for row in report["rows"]:
            payload = {
                "path": row.get("path", ""),
                "name": row.get("name", ""),
                "current_category": row.get("current_category", ""),
                "llm_category": row.get("llm_category", ""),
                "confidence": row.get("confidence"),
                "status": row.get("status", ""),
                "reason": row.get("reason", ""),
                "evidence": row.get("evidence", []),
                "workset": row.get("workset", ""),
            }
            handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def print_text_report(report: dict[str, Any], *, limit: int) -> None:
    summary = report["summary"]
    print("Residual LLM classification")
    print(f"Inputs: {summary['input_count']}")
    print(f"Reviewed: {summary['reviewed_count']}")
    print(f"New reviews: {summary['new_review_count']}")
    print(f"Status: {summary['status_counts']}")
    print(f"Categories: {summary['category_counts']}")
    for row in report["rows"][: max(limit, 0)]:
        print(
            f"- {row.get('status')} {row.get('path')}: "
            f"{row.get('llm_category')} q={row.get('confidence')}"
        )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workset-jsonl", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--classification-output", type=Path)
    parser.add_argument("--checkpoint-jsonl", type=Path)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument(
        "--reuse-status",
        action="append",
        default=["ok"],
        help="checkpoint status to reuse during --resume; repeat for more statuses",
    )
    parser.add_argument("--limit", type=int)
    parser.add_argument("--batch-size", type=int, default=5)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--sleep-seconds", type=float, default=0.0)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--retry-sleep-seconds", type=float, default=2.0)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--api-key-env", default=DEFAULT_API_KEY_ENV)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--max-completion-tokens", type=int, default=DEFAULT_MAX_COMPLETION_TOKENS)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--thinking", choices=["disabled", "default"], default=DEFAULT_THINKING)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--print-limit", type=int, default=20)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    api_key = os.environ.get(args.api_key_env)
    if not api_key:
        raise SystemExit(f"Missing API key environment variable: {args.api_key_env}")
    if args.resume and not args.checkpoint_jsonl:
        raise SystemExit("--resume requires --checkpoint-jsonl")
    client = OpenAICompatibleClient(
        api_key=api_key,
        base_url=args.base_url,
        model=args.model,
        timeout=args.timeout,
        max_completion_tokens=args.max_completion_tokens,
        temperature=args.temperature,
        thinking=args.thinking,
    )
    report = run_classification(
        workset_jsonl=args.workset_jsonl,
        client=client,
        checkpoint_jsonl=args.checkpoint_jsonl,
        resume=args.resume,
        limit=args.limit,
        batch_size=args.batch_size,
        workers=args.workers,
        sleep_seconds=args.sleep_seconds,
        retries=args.retries,
        retry_sleep_seconds=args.retry_sleep_seconds,
        checkpoint_reuse_statuses=set(args.reuse_status),
    )
    payload = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    if args.classification_output:
        write_classification_jsonl(report, args.classification_output)
    if args.json:
        print(payload)
    else:
        print_text_report(report, limit=args.print_limit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
