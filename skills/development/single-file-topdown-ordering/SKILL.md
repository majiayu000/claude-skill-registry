---
name: single-file-topdown-ordering
description: 'Use when a single file is difficult to understand top-down because the public surface is buried or definitions appear before the behavior they support. Goal: restore a clear reading flow without changing semantics.'
metadata:
  short-description: Read top-down
---

# Code Ordering

Restore a top-down narrative inside a single file: start from the public surface, then unfold supporting details.

## Core Rule

Blocks that depend on other blocks appear earlier. Their dependencies appear later.

Only reorder when language semantics remain correct.

## Block Scope

Blocks are structural units such as exported/public declarations, classes, functions/methods, and relevant type definitions.
Imports and module-level conventions stay untouched.

## Dependency Detection

For a block, collect dependencies in this order:

1. Signature dependencies: types and interfaces referenced by the declaration.
2. Body dependencies: symbols required by the implementation, ordered by semantic execution and control flow.

## Ordering Process

Treat the file as breadth-first expansion from public entry blocks.

1. Collect exported/public entry blocks.
2. Sort entry blocks by dependency-after: if an entry block depends on another entry block, place the dependent first. If no ordering is implied, keep original order.
3. Repeat the following layer step until no new blocks are discovered:

   * Scan every block in the current layer and collect dependencies using Dependency Detection.
   * Remove blocks already placed and anything out of scope.
   * The remaining blocks become the next layer, preserving first-encounter order across the scan.
   * Append the next layer after the current layer.

## Cycles

Cycles are common. Keep best-effort ordering and treat a cycle as a single group during layering.

Warn only when the cycle prevents a stable, semantics-preserving top-down order. Otherwise, do not warn.

## Review Checklist

* Public surface appears before supporting details.
* A block appears before the blocks it depends on whenever a valid order exists.
* Signature dependencies are introduced before body dependencies for the same dependent.
* The result reads top-down without changing behavior.
