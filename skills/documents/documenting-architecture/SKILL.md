---
name: documenting-architecture
description: >
  Generate architecture overview documentation from codebase analysis.
  Uses tree-sitter-analyzer for precise code structure extraction.
  Use when documenting project structure, creating architecture diagrams, or when user
  mentions architecture overview, project structure, アーキテクチャ, 構成図.
allowed-tools: [Read, Write, Grep, Glob, Bash, Task]
context: fork
user-invocable: false
---

# Architecture Overview Generation

## Detection

| Category            | Targets                                |
| ------------------- | -------------------------------------- |
| Project Overview    | Tech stack, framework, database        |
| Directory Structure | tree command output                    |
| Module Composition  | Mermaid relationship diagrams          |
| Key Components      | Classes, functions, entry points       |
| Dependencies        | External packages, internal modules    |
| Statistics          | File count, line count, language ratio |

## Project Patterns

| Type        | Pattern                                     |
| ----------- | ------------------------------------------- |
| Node.js     | `package.json`, `node_modules/`             |
| Python      | `pyproject.toml`, `setup.py`, `__init__.py` |
| Rust        | `Cargo.toml`, `src/main.rs`, `src/lib.rs`   |
| Go          | `go.mod`, `main.go`, `go.sum`               |
| Java/Maven  | `pom.xml`, `src/main/java/`                 |
| Java/Gradle | `build.gradle`, `src/main/java/`            |
