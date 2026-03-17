---
name: implement-subtask-rules
description: container-workerがSubtask実装時に参照する詳細ルール（設計書参照、粒度、TDD、品質レビュー、出力形式）を定義
---

# Subtask実装ルール（トークン最適化版）

> **目的**: implement-issues.mdから詳細ルールを分離し、トークン消費を削減する。
> container-workerはこのスキルを参照して実装する。

---

## 1. 設計書参照ルール

### 絶対禁止: 設計書の全文読み込み

### 1.1 設計書参照マトリクス（実装タスク別）

> **Token最適化の核心**: 実装タスクに必要な設計書セクションを事前定義。
> 不要なセクションの読み込みを完全に排除。

| 実装タスク | 領域 | 必須セクション | 任意セクション | 読み込み禁止 |
|-----------|------|--------------|--------------|-------------|
| **Entity/型定義** | backend | `## データ型`, `## バリデーション` | `## ビジネスルール` | 画面仕様, API仕様 |
| **Repository実装** | backend | `## テーブル定義`, `## クエリパターン` | `## インデックス` | 画面仕様, セキュリティ |
| **UseCase実装** | backend | `## ユースケース詳細`, `## ビジネスルール` | `## エラーハンドリング` | 画面仕様, テーブル定義 |
| **API Controller** | backend | `## エンドポイント`, `## リクエスト/レスポンス` | `## 認証/認可` | 画面仕様, DB詳細 |
| **UI Component** | frontend | `## 画面仕様`, `## コンポーネント` | `## 状態遷移` | API詳細, DB詳細 |
| **カスタムHook** | frontend | `## 状態管理`, `## API連携` | `## エラーハンドリング` | DB詳細, インフラ |
| **テスト実装** | backend/frontend | `## テストケース`, `## 境界条件` | `## モックデータ` | 実装詳細 |
| **マイグレーション** | infra | `## テーブル定義`, `## マイグレーション` | `## データ移行` | 画面仕様, API仕様 |
| **Terraform** | infra | `## インフラ構成`, `## 環境変数` | `## スケーリング` | 画面仕様, API仕様 |
| **Docker設定** | infra | `## コンテナ設定`, `## 依存サービス` | `## ヘルスチェック` | 画面仕様, ビジネスロジック |

### 1.1.1 領域別の設計書ファイルマッピング

| 領域 | 参照すべき設計書 | 参照禁止の設計書 |
|------|----------------|----------------|
| **backend** | バックエンド設計書.md, データベース設計書.md | 画面設計書.md, フロントエンド設計書.md |
| **frontend** | 画面設計書.md, フロントエンド設計書.md | バックエンド設計書.md, データベース設計書.md |
| **infra** | インフラ設計書.md, データベース設計書.md | 画面設計書.md, フロントエンド設計書.md |

> **効果**: 領域外の設計書を読み込まないことで、1タスクあたり2,000-5,000トークン節約

### 1.2 セクション別トークン上限

| セクション | 上限 | 超過時の対応 |
|-----------|------|-------------|
| データ型 | 2,000トークン | サブセクション単位で分割読み込み |
| API仕様 | 2,000トークン | エンドポイント単位で分割読み込み |
| 画面仕様 | 2,000トークン | コンポーネント単位で分割読み込み |
| テーブル定義 | 2,000トークン | テーブル単位で分割読み込み |
| テストケース | 2,000トークン | カテゴリ単位で分割読み込み |

### 1.3 参照手順（具体的なツール操作）

```python
# Step 1: 目次のみ確認（50行）
outline = read(design_path, limit=50)

# Step 2: 対象セクションの行番号を特定
grep_result = grep(path=design_path, pattern="## データ型")
# 結果例: line 45 にマッチ

# Step 3: 該当部分のみピンポイントで読み込み
section_content = read(design_path, offset=44, limit=80)
# offset=行番号-1, limit=セクション想定行数

# ⛔ 禁止: read(design_path) での全文読み込み
# ⛔ 禁止: limit指定なしでの読み込み
```

### 1.4 Progressive Context Loading（段階的読み込み）

```python
def load_design_context(task_type: str, design_path: str) -> dict:
    """タスクタイプに応じた段階的コンテキスト読み込み"""
    
    REFERENCE_MATRIX = {
        # Backend tasks
        "entity": {
            "area": "backend",
            "required": ["## データ型", "## バリデーション"],
            "optional": ["## ビジネスルール"],
            "forbidden": ["## 画面仕様", "## API仕様"],
            "design_files": ["バックエンド設計書.md"]
        },
        "repository": {
            "area": "backend",
            "required": ["## テーブル定義", "## クエリパターン"],
            "optional": ["## インデックス"],
            "forbidden": ["## 画面仕様", "## セキュリティ"],
            "design_files": ["データベース設計書.md", "バックエンド設計書.md"]
        },
        "usecase": {
            "area": "backend",
            "required": ["## ユースケース詳細", "## ビジネスルール"],
            "optional": ["## エラーハンドリング"],
            "forbidden": ["## 画面仕様", "## テーブル定義"],
            "design_files": ["バックエンド設計書.md"]
        },
        "controller": {
            "area": "backend",
            "required": ["## エンドポイント", "## リクエスト/レスポンス"],
            "optional": ["## 認証/認可"],
            "forbidden": ["## 画面仕様", "## DB詳細"],
            "design_files": ["バックエンド設計書.md"]
        },
        # Frontend tasks
        "component": {
            "area": "frontend",
            "required": ["## 画面仕様", "## コンポーネント"],
            "optional": ["## 状態遷移"],
            "forbidden": ["## API詳細", "## DB詳細"],
            "design_files": ["画面設計書.md", "フロントエンド設計書.md"]
        },
        "hook": {
            "area": "frontend",
            "required": ["## 状態管理", "## API連携"],
            "optional": ["## エラーハンドリング"],
            "forbidden": ["## DB詳細", "## インフラ"],
            "design_files": ["フロントエンド設計書.md"]
        },
        # Infra tasks
        "migration": {
            "area": "infra",
            "required": ["## テーブル定義", "## マイグレーション"],
            "optional": ["## データ移行"],
            "forbidden": ["## 画面仕様", "## API仕様"],
            "design_files": ["データベース設計書.md"]
        },
        "terraform": {
            "area": "infra",
            "required": ["## インフラ構成", "## 環境変数"],
            "optional": ["## スケーリング"],
            "forbidden": ["## 画面仕様", "## API仕様"],
            "design_files": ["インフラ設計書.md"]
        },
        # Shared tasks
        "test": {
            "area": "backend|frontend",  # 両方で使用可能
            "required": ["## テストケース", "## 境界条件"],
            "optional": ["## モックデータ"],
            "forbidden": ["## 実装詳細"],
            "design_files": ["テスト項目書.md"]
        }
    }
    
    matrix = REFERENCE_MATRIX.get(task_type, {})
    context = {}
    
    # 必須セクションのみ読み込み
    for section in matrix.get("required", []):
        content = read_section(design_path, section)
        if content:
            context[section] = content
    
    # 任意セクションは必要に応じて
    # ⛔ forbidden セクションは絶対に読み込まない
    
    return context
```

**なぜ重要か**: 全文読み込みは5,000〜20,000トークンを消費。マトリクス参照で500〜2,000トークンに抑制。

---

## 1.5 設計書実現性チェック（Phase 3）

> **Token最適化**: Phase 2 で取得した `context` オブジェクトを直接埋め込む。
> **絶対に設計書を再読み込みしないこと**（ファイルアクセス 0回）。

### 判定プロンプト（Gate）

```python
# Phase 2 で取得済みの context を使用
def check_feasibility(context: dict) -> GateResult:
    """設計書の実現性をチェック（読み込み済みのコンテキストを使用）"""
    
    PROMPT = f"""
あなたはシニアエンジニアです。以下の設計書セクションだけを読んで、**迷いなくコードに落とし込めますか？**

## 判定基準
1. **NG**: 型定義が曖昧（`object`, `any` 等）
2. **NG**: 必須パラメータの欠落
3. **NG**: エラー時の挙動が未定義
4. **NG**: 依存するAPI/DB定義が存在しない
5. **NG**: 実装者の推測で補完する必要がある

## コンテキスト（読み込み済み）
{json.dumps(context, indent=2)}

## 出力
{{
  "feasibility": "OK" | "NG",
  "reason": "NGの場合の具体的理由（なければnull）",
  "questions": ["設計者への質問リスト"]
}}
"""
    # 呼び出し (readツールは使用しない)
    return llm.generate(PROMPT)
```

### NG時の対応（Blocked移行）

判定が **NG** の場合、即座に作業を中断し、以下の手順を実行：

1. Issue を `blocked` 状態に更新（{{skill:github-issue-state-management}} API）：
   ```bash
   bash .opencode/skill/github-issue-state-management/scripts/issue-state.sh block <issue-num> design_ambiguity "[判定AIが出力した reason]"
   ```
2. ユーザー（Sisyphus）に報告して終了

**⛔ 絶対禁止**: 「たぶんこうだろう」と推測して実装を進めること。

---

## 2. 粒度ルール

| 項目 | 上限 | 違反時 |
|------|------|--------|
| コード量 | 200行 | 即時中断、親に報告 |
| ファイル数 | 3ファイル | 即時中断、親に報告 |
| リトライ | 3回 | Draft PR作成 |

---

## 3. TDDフロー

```
🔴 Red: テスト作成 → 失敗確認
    ↓
🟢 Green: 最小実装 → 成功確認
    ↓
🔵 Refactor: 整形 → 再テスト
```

---

## 4. 品質レビュー

| スコア | アクション |
|--------|----------|
| 9-10点 | PR作成へ |
| 7-8点 | 修正 → 再レビュー |
| 6点以下 | 報告 → 設計見直し |

### レビュー観点（6項目）

> **詳細**: {{skill:quality-review-flow}} セクション2（客観的品質基準）を参照

1. 設計書との整合性
2. コード品質（SOLID、命名）
3. エラーハンドリング
4. テストカバレッジ
5. セキュリティ
6. **定義-使用相関**（スタブ検出）→ 詳細は {{skill:quality-review-flow}} セクション2.3 参照

---

## 5. 出力形式（必須）

### 成功時（最小JSON）

```json
{
  "subtask_id": N,
  "pr_number": N,
  "env_id": "xxx",
  "score": N,
  "status": "success"
}
```

### 失敗時

```json
{
  "subtask_id": N,
  "env_id": "xxx",
  "status": "failed",
  "error": "簡潔なエラー説明"
}
```

---

## 6. 禁止事項

| 禁止 | 代替 |
|------|------|
| ホストで `edit`/`write` | `environment_file_write` |
| ホストで `bash cargo test` | `environment_run_cmd` |
| 設計書全文読み込み | セクション単位参照 |
| レビュースキップ | 必ず実行 |
| 冗長な出力 | 最小JSON形式 |

---

## 7. プラットフォーム例外

macOS専用API（`objc2`, `cocoa`等）使用時のみホスト環境を許可。
必ず報告してから作業開始。

---

## 8. 撤退条件（必ず守る）

| 状況 | アクション |
|------|----------|
| 環境作成が3回失敗 | 中断、Sisyphusに報告 |
| テストが10回連続失敗 | 中断、設計見直し要請 |
| レビュー3回失敗 | Draft PR作成、中断 |
| 200行超過の見込み | 即時中断、粒度違反報告 |
| 1時間経過 | 進捗報告、継続可否確認 |

**⛔ 絶対禁止**: 無限ループ、エンドレスリトライ
