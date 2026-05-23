---
name: dr-build
description: >
  dr-synthesize の implementation_plan.md を実装に落とし込む。PoC/MVP/Production の段階的実装を支援。
disable-model-invocation: true
argument-hint: "[plan_path] | stage=poc|mvp|production | stack=python|node|go | storage=sqlite|postgres|qdrant"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(git:*), Bash(python:*), Bash(node:*), Bash(docker:*)
---

# dr-build

## 方針
- いきなり全部作らない。PoC → MVP → Production の順で段階的に
- すべての実装は「どの証拠/要件に対応するか」を追跡できるようにする（planへのリンク）
- 秘密情報はコミットしない（.env / secrets manager 前提）

## 入力

| パラメータ | 説明 | デフォルト |
|-----------|------|-----------|
| plan_path | implementation_plan.mdのパス | 最新run |
| stage | poc/mvp/production | poc |
| stack | python/node/go | python |
| storage | sqlite/postgres/qdrant | sqlite |

## 実装の基本手順

### Step 1: 計画の読み込み
1. `implementation_plan.md` を読み、対象stageのスコープを確定
2. 依存関係を確認（前stageが完了しているか）
3. 必要な外部サービス/APIを確認

### Step 2: プロジェクト構造の作成

```
dr-system/
├── README.md           # セットアップ・実行手順
├── pyproject.toml      # Python依存関係
├── .env.example        # 環境変数テンプレート
├── .gitignore          # 秘密情報除外
├── src/
│   ├── __init__.py
│   ├── connectors/     # データソース接続
│   │   ├── __init__.py
│   │   ├── base.py     # 抽象基底クラス
│   │   ├── rss.py
│   │   ├── web_search.py
│   │   └── sns.py
│   ├── extractor/      # 本文抽出
│   │   ├── __init__.py
│   │   └── html_to_text.py
│   ├── normalizer/     # 正規化・重複排除
│   │   ├── __init__.py
│   │   ├── url.py
│   │   ├── dedup.py
│   │   └── metadata.py
│   ├── storage/        # 永続化
│   │   ├── __init__.py
│   │   ├── sqlite.py
│   │   └── evidence.py
│   ├── rag/            # ベクトル検索（MVP以降）
│   │   ├── __init__.py
│   │   └── vector_store.py
│   └── cli.py          # CLIエントリポイント
├── tests/
│   ├── __init__.py
│   ├── test_connectors.py
│   ├── test_normalizer.py
│   └── test_storage.py
└── research/           # 調査データ（既存）
    └── runs/
```

### Step 3: 段階別実装

#### PoC（最小構成）

**目標**: 動くことを確認する

```python
# src/connectors/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

@dataclass
class Evidence:
    id: str
    source_type: str
    source_url: str
    retrieved_at: str
    title: str
    author: str | None
    published_at: str | None
    language: str
    excerpt: str
    notes: str
    claims: List[str]
    reliability_score: int
    reliability_rationale: str

class BaseConnector(ABC):
    @abstractmethod
    def fetch(self, query: str, limit: int = 10) -> List[Evidence]:
        pass
```

```python
# src/storage/sqlite.py
import sqlite3
import json
from pathlib import Path

class SQLiteStorage:
    def __init__(self, db_path: str = "research.db"):
        self.conn = sqlite3.connect(db_path)
        self._init_schema()

    def _init_schema(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS evidence (
                id TEXT PRIMARY KEY,
                source_type TEXT,
                source_url TEXT,
                retrieved_at TEXT,
                title TEXT,
                author TEXT,
                published_at TEXT,
                language TEXT,
                excerpt TEXT,
                notes TEXT,
                claims TEXT,
                reliability_score INTEGER,
                reliability_rationale TEXT
            )
        """)
        self.conn.commit()

    def save(self, evidence: dict):
        # Implementation
        pass

    def load_run(self, run_id: str) -> list:
        # Implementation
        pass
```

#### MVP（実用レベル）

**追加目標**:
- 複数connectors
- ベクトル検索
- 基本的なテスト
- エラーハンドリング

#### Production（本番レベル）

**追加目標**:
- Docker化
- CI/CD
- 監視・アラート
- ドキュメント

### Step 4: テスト作成

```python
# tests/test_normalizer.py
import pytest
from src.normalizer.url import normalize_url
from src.normalizer.dedup import deduplicate

def test_normalize_url():
    assert normalize_url("https://example.com/page?ref=123") == "https://example.com/page"
    assert normalize_url("http://example.com") == "https://example.com"

def test_deduplicate():
    evidences = [
        {"id": "1", "source_url": "https://a.com"},
        {"id": "2", "source_url": "https://a.com"},  # 重複
        {"id": "3", "source_url": "https://b.com"},
    ]
    result = deduplicate(evidences)
    assert len(result) == 2
```

### Step 5: ドキュメント作成

```markdown
# README.md

## セットアップ

1. 依存関係インストール
   ```bash
   pip install -e .
   ```

2. 環境変数設定
   ```bash
   cp .env.example .env
   # .envを編集
   ```

3. 実行
   ```bash
   python -m src.cli explore "AI Agent" --depth lite
   ```

## 使い方

### 調査実行
```bash
python -m src.cli explore "トピック" --domain ai_system --depth standard
```

### レポート生成
```bash
python -m src.cli synthesize research/runs/20260131-120000__topic
```
```

## 出力

- プロジェクトディレクトリ構造
- 最小実装コード（stage依存）
- テストコード
- README.md
- .env.example
- .gitignore

## 品質チェックリスト

### PoC
- [ ] 1つのconnectorが動作する
- [ ] evidenceがSQLiteに保存される
- [ ] CLIで実行できる

### MVP
- [ ] 複数connectorが動作する
- [ ] テストが通る（カバレッジ70%以上）
- [ ] エラーハンドリングがある
- [ ] ログ出力がある

### Production
- [ ] Dockerで起動できる
- [ ] CI/CDが動作する
- [ ] 監視メトリクスがある
- [ ] ドキュメントが完備
