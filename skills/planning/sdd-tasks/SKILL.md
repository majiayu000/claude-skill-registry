---
name: sdd-tasks
description: Kiro形式の実行計画(tasks.md)を生成。要件からフェーズ分割・タスク依存関係・マイルストーンを定義し、Ganttチャートを含む。
argument-hint: "[spec-slug] [target-dir(optional)]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep
model: opus
---

# sdd-tasks — Kiro-format Task Breakdown Generator

## 0. 目的
- 要件定義から実装可能なタスクに分解
- フェーズ構造（準備→基盤→コア→拡張→検証→運用）で整理
- 依存関係を明確化し、並列実行可能なタスクを特定
- Mermaid Ganttチャートで可視化

## 1. 入力と出力

### 入力
- /sdd-tasks $ARGUMENTS
  - $0 = spec-slug（例: google-ad-report）
  - $1 = target-dir（任意。未指定なら `.kiro/specs/<spec-slug>/` を使う）
- 前提: requirements.md と design.md が存在すること

### 出力（必須）
- <target-dir>/tasks.md

### 参照
- templates/tasks.template.md : タスクテンプレート
- <target-dir>/requirements.md : 要件定義
- <target-dir>/design.md : 設計書

## 2. 重要ルール

1. **Kiro形式厳守**: 各タスクにID、タイトル、説明、依存関係を明記
2. **フェーズ分割**: 6フェーズ構造（Phase 0-5）
3. **依存関係**: 循環依存禁止、クリティカルパスを特定
4. **要件トレーサビリティ**: 各タスクがどのREQを実現するか明記

## 3. フェーズ構造

| Phase | 名称 | 内容 |
|-------|------|------|
| 0 | Preparation | 環境構築、依存関係インストール |
| 1 | Foundation | データモデル、基本API構造 |
| 2 | Core | 主要機能の実装 |
| 3 | Extension | 追加機能、最適化 |
| 4 | Validation | テスト、セキュリティレビュー |
| 5 | Operations | デプロイ、監視、ドキュメント |

## 4. 手順

### Step A: 入力読み込み
1. requirements.md から機能要件を抽出
2. design.md からコンポーネント構造を抽出
3. 既存タスクがあれば差分更新

### Step B: タスク分解
1. 各REQを実装タスクに分解
2. 1タスク = 1-4時間で完了可能なサイズ
3. 曖昧なタスクは分割（「〜を実装」→具体的なサブタスク）

### Step C: 依存関係定義
1. 前提タスクを特定（blockedBy）
2. 後続タスクを特定（blocks）
3. 循環依存がないことを確認

### Step D: フェーズ割り当て
1. 各タスクを適切なフェーズに配置
2. 同一フェーズ内で並列実行可能なタスクを特定
3. クリティカルパスを算出

### Step E: Ganttチャート生成
1. Mermaid Gantt形式で可視化
2. マイルストーンを配置
3. 依存関係を反映

## 5. タスクフォーマット

```markdown
### TASK-001: <タイトル>
- **Phase**: 1 - Foundation
- **Implements**: REQ-001, REQ-002
- **blockedBy**: (none)
- **blocks**: TASK-002, TASK-003
- **Description**: <具体的な実装内容>
- **Acceptance Criteria**:
  - [ ] <完了条件1>
  - [ ] <完了条件2>
```

## 6. 実行例

```bash
/sdd-tasks google-ad-report
```

前提:
- .kiro/specs/google-ad-report/requirements.md
- .kiro/specs/google-ad-report/design.md

出力:
- .kiro/specs/google-ad-report/tasks.md
