---
name: documenting-setup
description: >
  コードベース分析から環境セットアップガイドドキュメントを生成。
  パッケージマネージャ、必要なツール、環境変数、起動コマンドを検出する。
  セットアップガイド作成、環境ドキュメント化、または
  setup guide, environment setup, 環境構築, 開発環境 に言及した時に使用。
allowed-tools: [Read, Write, Grep, Glob, Bash, Task]
context: fork
user-invocable: false
---

# 環境セットアップガイド生成

## 検出

| カテゴリ             | 対象                                                                  |
| -------------------- | --------------------------------------------------------------------- |
| パッケージマネージャ | package.json, yarn.lock, pnpm-lock, pyproject.toml, Cargo.toml        |
| ツールバージョン     | .nvmrc, .python-version, .ruby-version, .tool-versions                |
| 環境                 | .env.example, .env.sample, .env.template (→ 存在時はコピー手順を生成) |
| 設定ファイル         | tsconfig.json, eslint.config, vite.config, next.config                |
| コンテナ             | Dockerfile, docker-compose.yml, .devcontainer/                        |
| コマンド             | package.json scripts, Makefile, README                                |

## パッケージマネージャ識別子

| マネージャ | 識別子                          |
| ---------- | ------------------------------- |
| npm        | `package-lock.json`             |
| yarn       | `yarn.lock`                     |
| pnpm       | `pnpm-lock.yaml`                |
| pip        | `requirements.txt`, `setup.py`  |
| poetry     | `pyproject.toml`, `poetry.lock` |
| cargo      | `Cargo.toml`, `Cargo.lock`      |

## 参照

| トピック | ファイル                    |
| -------- | --------------------------- |
| 環境     | `references/environment.md` |
