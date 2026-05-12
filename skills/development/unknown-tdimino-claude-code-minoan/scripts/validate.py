#!/usr/bin/env python3
"""Validate a DAG plan against a typed node registry.

Checks:
- All node registry_refs exist in the registry
- All edges connect existing nodes and ports
- No cycles in the graph
- Type compatibility at every edge
- Certificate predicate well-formedness
- Required inputs satisfied

Usage:
    python3 validate.py dag-plan.json --registry dag-registry.json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


class ValidationError:
    def __init__(self, level: str, node_id: str, message: str):
        self.level = level
        self.node_id = node_id
        self.message = message

    def __str__(self):
        return f"[{self.level}] {self.node_id}: {self.message}"


def validate_dag(plan: dict, registry: dict) -> list[ValidationError]:
    errors: list[ValidationError] = []

    registry_nodes = {n["name"]: n for n in registry.get("nodes", [])}
    dag_nodes = {n["id"]: n for n in plan.get("nodes", [])}
    edges = plan.get("edges", [])

    for node in plan.get("nodes", []):
        nid = node["id"]
        ref = node["registry_ref"]
        if ref not in registry_nodes:
            errors.append(ValidationError("ERROR", nid, f"registry_ref '{ref}' not found in registry"))

    node_ids = set(dag_nodes.keys())
    for edge in edges:
        if edge["from_node"] not in node_ids:
            errors.append(ValidationError("ERROR", edge["from_node"], f"edge source node not found in DAG"))
        if edge["to_node"] not in node_ids:
            errors.append(ValidationError("ERROR", edge["to_node"], f"edge target node not found in DAG"))

    adj: dict[str, list[str]] = defaultdict(list)
    for edge in edges:
        adj[edge["from_node"]].append(edge["to_node"])

    if _has_cycle(adj, node_ids):
        errors.append(ValidationError("ERROR", "DAG", "cycle detected in the execution graph"))

    for edge in edges:
        from_node = dag_nodes.get(edge["from_node"])
        to_node = dag_nodes.get(edge["to_node"])
        if not from_node or not to_node:
            continue

        from_ref = registry_nodes.get(from_node["registry_ref"])
        to_ref = registry_nodes.get(to_node["registry_ref"])
        if not from_ref or not to_ref:
            continue

        from_port = edge["from_port"]
        to_port = edge["to_port"]

        from_output = from_ref.get("output_schema", {})
        from_props = from_output.get("properties", {})
        if from_props and from_port not in from_props:
            errors.append(ValidationError("WARN", edge["from_node"],
                f"output port '{from_port}' not found in output schema of '{from_node['registry_ref']}'"))

        to_input = to_ref.get("input_schema", {})
        to_props = to_input.get("properties", {})
        if to_props and to_port not in to_props:
            errors.append(ValidationError("WARN", edge["to_node"],
                f"input port '{to_port}' not found in input schema of '{to_node['registry_ref']}'"))

        if from_props and to_props and from_port in from_props and to_port in to_props:
            if not _types_compatible(from_props[from_port], to_props[to_port]):
                errors.append(ValidationError("ERROR", f"{edge['from_node']}->{edge['to_node']}",
                    f"type mismatch: {from_port} ({json.dumps(from_props[from_port])}) "
                    f"-> {to_port} ({json.dumps(to_props[to_port])})"))

    for node in plan.get("nodes", []):
        cert = node.get("certificate")
        if not cert:
            continue
        if not cert.get("predicate_name"):
            errors.append(ValidationError("ERROR", node["id"], "certificate missing predicate_name"))
        if not cert.get("evidence_keys"):
            errors.append(ValidationError("WARN", node["id"], "certificate has no evidence_keys"))
        for upstream_id in cert.get("required_upstream_certs", []):
            if upstream_id not in node_ids:
                errors.append(ValidationError("ERROR", node["id"],
                    f"required_upstream_cert '{upstream_id}' not found in DAG"))

    source_nodes = node_ids - {e["to_node"] for e in edges}
    for nid in node_ids:
        if nid in source_nodes:
            continue
        node = dag_nodes[nid]
        ref = registry_nodes.get(node["registry_ref"])
        if not ref:
            continue
        required_inputs = ref.get("input_schema", {}).get("required", [])
        provided = set()
        for edge in edges:
            if edge["to_node"] == nid:
                provided.add(edge["to_port"])
        for mapping in node.get("input_mappings", []):
            provided.add(mapping["target_field"])
        for param_key in node.get("params", {}).keys():
            provided.add(param_key)
        missing = set(required_inputs) - provided
        if missing:
            errors.append(ValidationError("WARN", nid,
                f"required inputs not satisfied: {', '.join(sorted(missing))}"))

    return errors


def _has_cycle(adj: dict[str, list[str]], nodes: set[str]) -> bool:
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in nodes}

    def dfs(u: str) -> bool:
        color[u] = GRAY
        for v in adj.get(u, []):
            if color.get(v) == GRAY:
                return True
            if color.get(v) == WHITE and dfs(v):
                return True
        color[u] = BLACK
        return False

    return any(dfs(n) for n in nodes if color[n] == WHITE)


def _types_compatible(source: dict[str, Any], target: dict[str, Any]) -> bool:
    if not source or not target:
        return True
    if "$ref" in source or "$ref" in target:
        return True
    source_type = source.get("type")
    target_type = target.get("type")
    if source_type and target_type:
        if source_type == target_type:
            return True
        if source_type == "integer" and target_type == "number":
            return True
        return False
    return True


def main():
    parser = argparse.ArgumentParser(description="Validate a DAG plan against a registry")
    parser.add_argument("dag_plan", help="Path to dag-plan.json")
    parser.add_argument("--registry", "-r", default="dag-registry.json", help="Path to dag-registry.json")
    args = parser.parse_args()

    plan = json.loads(Path(args.dag_plan).read_text())
    registry = json.loads(Path(args.registry).read_text())

    errors = validate_dag(plan, registry)

    if not errors:
        print("DAG is valid. All checks passed.")
        sys.exit(0)

    error_count = sum(1 for e in errors if e.level == "ERROR")
    warn_count = sum(1 for e in errors if e.level == "WARN")

    for e in errors:
        print(str(e))

    print(f"\n{error_count} error(s), {warn_count} warning(s)")
    sys.exit(1 if error_count > 0 else 0)


if __name__ == "__main__":
    main()
