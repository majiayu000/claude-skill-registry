#!/usr/bin/env python3
"""Compose a DAG plan from natural language using a typed node registry.

In-session mode (default): prints a structured prompt for the current Claude Code
session to generate the DAG plan.

Headless mode: calls an OpenAI-compatible API endpoint directly.

Usage:
    python3 compose.py "task description" --registry dag-registry.json [--output dag-plan.json] [--provider session|openai]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = SKILL_ROOT / "schemas" / "dag-plan.schema.json"


def build_composition_prompt(task: str, registry: dict, schema: dict) -> str:
    node_summaries = []
    for node in registry.get("nodes", []):
        entry = f"- **{node['name']}** ({node['kind']}, {node['language']})"
        if node.get("description"):
            entry += f": {node['description']}"
        entry += f"\n  Input: {json.dumps(node['input_schema'], separators=(',', ':'))}"
        entry += f"\n  Output: {json.dumps(node['output_schema'], separators=(',', ':'))}"
        if node.get("tags"):
            entry += f"\n  Tags: {', '.join(node['tags'])}"
        if node.get("side_effects"):
            entry += "\n  Has side effects"
        node_summaries.append(entry)

    registry_text = "\n".join(node_summaries)

    return f"""Generate a DAG execution plan for the following task. Select nodes ONLY from the
typed registry below. Do NOT invent new operations — compose exclusively from registry entries.

## Task
{task}

## Available Nodes (Typed Registry)
{registry_text}

## Output Format
Return a single JSON object conforming to the DAG plan schema. Requirements:
- Each node must have: id (lowercase snake_case), registry_ref (exact name from registry), params (object)
- Each edge must have: from_node, from_port, to_node, to_port
- No cycles allowed
- All edges must be type-compatible (output schema of source port matches input schema of target port)
- Include certificate specs for nodes that validate data or have side effects

## Certificate Specification
For each node where verification matters, include a certificate object with:
- predicate_name: descriptive name for the check
- evidence_keys: what evidence to log
- predicate_expression: Python/JS boolean expression using `artifact` and `evidence` variables

## DAG Plan Schema (abbreviated)
Nodes: {{id, registry_ref, params, input_mappings: [{{source_node, source_field, target_field}}], certificate}}
Edges: {{from_node, from_port, to_node, to_port}}

Return ONLY the JSON object, no markdown fences, no explanation."""


def compose_session(task: str, registry: dict, schema: dict, output: Path) -> None:
    """Generate a prompt for in-session composition."""
    prompt = build_composition_prompt(task, registry, schema)
    print("=== DAG Composition Prompt ===")
    print()
    print(prompt)
    print()
    print("=== End Prompt ===")
    print()
    print(f"Paste the LLM's JSON response into: {output}")
    print("Then run: python3 validate.py <output> --registry dag-registry.json")


def compose_openai(task: str, registry: dict, schema: dict, output: Path) -> None:
    """Call an OpenAI-compatible API to compose the DAG."""
    try:
        import httpx
    except ImportError:
        print("Error: httpx required for headless mode. Install with: uv pip install httpx", file=sys.stderr)
        sys.exit(1)

    base_url = os.environ.get("DAG_LLM_BASE_URL", "https://openrouter.ai/api/v1")
    api_key = os.environ.get("DAG_LLM_API_KEY")
    model = os.environ.get("DAG_LLM_MODEL", "anthropic/claude-sonnet-4-20250514")

    if not api_key:
        print("Error: DAG_LLM_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    prompt = build_composition_prompt(task, registry, schema)

    response = httpx.post(
        f"{base_url}/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": "Generate DAG execution plans as JSON. Return only valid JSON, no markdown."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
            "max_tokens": 4096,
        },
        timeout=60,
    )

    if response.status_code != 200:
        print(f"API error {response.status_code}: {response.text}", file=sys.stderr)
        sys.exit(1)

    result = response.json()
    content = result["choices"][0]["message"]["content"]

    content = content.strip()
    if content.startswith("```"):
        content = content.split("\n", 1)[1]
        if content.endswith("```"):
            content = content[:-3]

    try:
        plan = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Failed to parse LLM response as JSON: {e}", file=sys.stderr)
        print(f"Raw response:\n{content}", file=sys.stderr)
        sys.exit(1)

    registry_content = json.dumps(registry, separators=(",", ":"))
    registry_hash = hashlib.sha256(registry_content.encode()).hexdigest()

    if "version" not in plan:
        plan["version"] = "1.0.0"
    if "metadata" not in plan:
        plan["metadata"] = {}
    plan["metadata"].update({
        "created_at": datetime.now(timezone.utc).isoformat(),
        "task_description": task,
        "registry_ref": "dag-registry.json",
        "registry_hash": registry_hash,
        "provider": base_url,
        "model": model,
    })

    output.write_text(json.dumps(plan, indent=2))
    print(f"DAG plan written to {output}")
    print(f"Nodes: {len(plan.get('nodes', []))}, Edges: {len(plan.get('edges', []))}")


def main():
    parser = argparse.ArgumentParser(description="Compose a DAG plan from natural language")
    parser.add_argument("task", help="Natural language task description")
    parser.add_argument("--registry", "-r", default="dag-registry.json")
    parser.add_argument("--output", "-o", default="dag-plan.json")
    parser.add_argument("--provider", "-p", choices=["session", "openai"], default="session")
    args = parser.parse_args()

    registry = json.loads(Path(args.registry).read_text())
    schema = json.loads(SCHEMA_PATH.read_text())
    output = Path(args.output)

    print(f"Registry: {registry['metadata']['node_count']} nodes")
    print(f"Task: {args.task}")
    print()

    if args.provider == "session":
        compose_session(args.task, registry, schema, output)
    else:
        compose_openai(args.task, registry, schema, output)


if __name__ == "__main__":
    main()
