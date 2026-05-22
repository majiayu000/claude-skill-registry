---
name: developing-python
description: Guides modern Python project development. Use when pyproject.toml or requirements.txt is detected. Supports Python 3.13 + uv + ruff + mypy environment, FastAPI/FastMCP implementation, pytest, and Docker configuration.
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

## 🔗 関連スキル

- **[applying-solid-principles](../applying-solid-principles/SKILL.md)**: SOLID原則とクリーンコード
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
