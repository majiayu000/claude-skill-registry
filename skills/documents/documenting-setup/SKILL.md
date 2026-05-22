---
name: documenting-setup
description: >
  Generate environment setup guide documentation from codebase analysis.
  Detects package managers, required tools, environment variables, and startup commands.
  Triggers: setup guide, environment setup, development environment.
allowed-tools: [Read, Write, Grep, Glob, Bash, Task]
context: fork
user-invocable: false
---

# 環境セットアップガイド生成

## 検出

| カテゴリ             | 対象                                                           |
| -------------------- | -------------------------------------------------------------- |
| パッケージマネージャ | package.json, yarn.lock, pnpm-lock, pyproject.toml, Cargo.toml |
| ツールバージョン     | .nvmrc, .python-version, .ruby-version, .tool-versions         |
| 環境                 | .env.example, .env.sample, .env.template                       |
| 設定ファイル         | tsconfig.json, eslint.config, vite.config, next.config         |
| コンテナ             | Dockerfile, docker-compose.yml, .devcontainer/                 |
| コマンド             | package.json scripts, Makefile, README                         |

## パッケージマネージャ識別子

| マネージャ | 識別子                          |
| ---------- | ------------------------------- |
| npm        | `package-lock.json`             |
| yarn       | `yarn.lock`                     |
| pnpm       | `pnpm-lock.yaml`                |
| pip        | `requirements.txt`, `setup.py`  |
| poetry     | `pyproject.toml`, `poetry.lock` |
| cargo      | `Cargo.toml`, `Cargo.lock`      |

## 参考

| トピック | ファイル                    |
| -------- | --------------------------- |
| 環境     | `references/environment.md` |
