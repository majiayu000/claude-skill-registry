---
name: developing-python
description: Modern Python development guide covering project setup, tooling, and 125 Pythonic best practices. MUST load when pyproject.toml or requirements.txt is detected. Covers Python 3.13 + uv + ruff + mypy, FastAPI/FastMCP, pytest, Docker, and Effective Python items (idioms, data structures, concurrency, testing).
---

# Python開発環境（Modern Python Development）

## 🎯 使用タイミング
- **Pythonプロジェクト新規作成時**
- **FastAPI + FastMCP実装時**
- **Python開発環境の構成時**
- **CI/CDパイプライン構築時**
- **Dockerイメージ作成時**

## 📚 ドキュメント構成

このスキルは以下のドキュメントで構成されています：

### 1. [プロジェクト構造](./PROJECT-STRUCTURE.md)
Pythonプロジェクトの推奨ディレクトリ構成：
- src/パッケージレイアウト
- tests/ディレクトリの構成
- 設定ファイルの配置
- ドキュメント構成

### 2. [FastAPI + FastMCPガイド](./FASTAPI-GUIDE.md)
FastAPIとFastMCPを使用したベストプラクティス：
- FastAPIアプリケーション構成
- FastMCPサーバー実装パターン
- 依存性注入（DI）の活用
- エラーハンドリング戦略
- Pydanticによるバリデーション

### 3. [テスト戦略](./TESTING.md)
pytest + カバレッジ80%以上を達成する方法：
- pytest設定とマーカー
- 単体テスト/統合テストの分離
- fixtureの活用パターン
- モックとスタブの使い分け
- カバレッジ最適化戦略

### 4. [開発ツール](./TOOLING.md)
uv + ruff + mypyの統合開発環境：
- uvによる高速依存関係管理
- ruffによるlintとformat
- mypyによる型チェック
- mise.tomlによるツールバージョン管理
- pre-commit設定

### 5. [Docker構成](./DOCKER.md)
uvマルチステージビルドの最適化：
- マルチステージビルド戦略
- .venvの効率的なコピー
- イメージサイズ最適化
- ヘルスチェック設定
- Cloud Run対応

### 6. [実装例](./EXAMPLES.md)
実際のコード例とパターン：
- FastMCP基本実装
- 認証/認可パターン
- データベース接続
- 構造化ロギング
- エラーハンドリング

## 🎯 技術スタック概要

### コアツール
- **Python 3.13**: 推奨バージョン
- **uv**: 超高速パッケージマネージャー（Rust製）
- **ruff**: 最速linter + formatter（Rust製）
- **mypy**: 静的型チェッカー

### Webフレームワーク
- **FastAPI 0.115+**: 高性能非同期Webフレームワーク
- **FastMCP 2.12+**: MCP (Model Context Protocol) SDK
- **Pydantic 2.9+**: データバリデーション

### テスト
- **pytest 8.3+**: テストフレームワーク
- **pytest-asyncio**: 非同期テスト対応
- **pytest-cov**: カバレッジ測定（目標80%以上）

### その他
- **structlog**: 構造化ロギング
- **SQLAlchemy 2.0+**: ORMとデータベース抽象化

## 🚀 クイックスタート

### 1. プロジェクト初期化
```bash
# uvのインストール（まだの場合）
curl -LsSf https://astral.sh/uv/install.sh | sh

# プロジェクト作成
mkdir my-project && cd my-project
uv init

# pyproject.toml作成（詳細は TOOLING.md 参照）
```

### 2. 依存関係のインストール
```bash
# 本番依存関係のみ
uv sync --frozen

# 開発依存関係を含む
uv sync --frozen
```

### 3. 開発ツールの実行
```bash
# Lint + Format
uv run ruff check .
uv run ruff format .

# 型チェック
uv run mypy src/

# テスト実行
uv run pytest
```

## 💡 重要な原則

### 型安全性
- **any型の使用禁止**（詳細は `enforcing-type-safety` スキル参照）
- strict型チェックモードの活用
- Pydanticモデルによるランタイムバリデーション

### テスト駆動開発
- テストカバレッジ80%以上を維持
- pytest markersによるテスト分類
- 環境変数の適切な管理（詳細は `TESTING.md` 参照）

### セキュリティ
- CodeGuardによるセキュリティチェック（`securing-code` スキル参照）
- 機密情報は環境変数で管理
- 入力値の厳格なバリデーション

### パフォーマンス
- 非同期処理の積極活用（async/await）
- データベース接続プール
- Dockerマルチステージビルドによるイメージ最適化

## ユーザー確認の原則（AskUserQuestion）

**判断分岐がある場合、推測で進めず必ずAskUserQuestionツールでユーザーに確認する。**

### 確認すべき場面

| 確認項目 | 例 |
|---|---|
| Pythonバージョン | 3.11, 3.12, 3.13 |
| Webフレームワーク | FastAPI, Flask, Django |
| パッケージマネージャー | uv, pip, poetry |
| DB選択 | PostgreSQL, SQLite, MongoDB |
| ORM | SQLAlchemy, Prisma, Tortoise |
| テストランナー | pytest, unittest |

### 確認不要な場面

- pyproject.toml が既に存在し設定が明確な場合
- CLAUDE.mdや既存コードで技術スタックが指定済みの場合
- linter/formatterの選択（ruff + mypy がデフォルト）

## 🔗 関連スキル

- **[writing-clean-code](../writing-clean-code/SKILL.md)**: SOLID原則とクリーンコード
- **[enforcing-type-safety](../enforcing-type-safety/SKILL.md)**: 型安全性の確保
- **[testing](../testing/SKILL.md)**: テストファーストアプローチ
- **[securing-code](../securing-code/SKILL.md)**: セキュアコーディング
- **[writing-technical-docs](../writing-technical-docs/SKILL.md)**: ドキュメント作成

## 📖 次のステップ

1. **初めての方**: [プロジェクト構造](./PROJECT-STRUCTURE.md)から始めてください
2. **FastAPI開発**: [FastAPI + FastMCPガイド](./FASTAPI-GUIDE.md)を参照
3. **テスト作成**: [テスト戦略](./TESTING.md)でpytest設定を確認
4. **ツール設定**: [開発ツール](./TOOLING.md)でuv/ruff/mypy設定
5. **Docker化**: [Docker構成](./DOCKER.md)でマルチステージビルド
6. **コード例**: [実装例](./EXAMPLES.md)で具体的なパターンを確認

## Effective Python

125項目のPythonicコードベストプラクティス。

| ファイル | 内容 |
|---------|------|
| [EP-CH01-PYTHONIC.md](./EP-CH01-PYTHONIC.md) | Pythonicな考え方 |
| [EP-CH02-STRINGS-SLICES.md](./EP-CH02-STRINGS-SLICES.md) | 文字列とスライス |
| [EP-CH03-LOOPS-ITERATORS.md](./EP-CH03-LOOPS-ITERATORS.md) | ループとイテレータ |
| [EP-CH04-DICTIONARIES.md](./EP-CH04-DICTIONARIES.md) | 辞書 |
| [EP-CH05-FUNCTIONS.md](./EP-CH05-FUNCTIONS.md) | 関数 |
| [EP-CH06-COMPREHENSIONS.md](./EP-CH06-COMPREHENSIONS.md) | 内包表記とジェネレータ |
| [EP-CH07-CLASSES.md](./EP-CH07-CLASSES.md) | クラスと継承 |
| [EP-CH08-METACLASSES.md](./EP-CH08-METACLASSES.md) | メタクラスと属性 |
| [EP-CH09-CONCURRENCY.md](./EP-CH09-CONCURRENCY.md) | 並行処理と並列処理 |
| [EP-CH10-ROBUSTNESS.md](./EP-CH10-ROBUSTNESS.md) | 堅牢性と性能 |
| [EP-CH11-PERFORMANCE.md](./EP-CH11-PERFORMANCE.md) | パフォーマンス |
| [EP-CH12-DATA-STRUCTURES.md](./EP-CH12-DATA-STRUCTURES.md) | データ構造 |
| [EP-CH13-TESTING.md](./EP-CH13-TESTING.md) | テストとデバッグ |
| [EP-CH14-COLLABORATION.md](./EP-CH14-COLLABORATION.md) | コラボレーション |
