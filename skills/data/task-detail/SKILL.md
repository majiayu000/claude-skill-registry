---
user-invocable: true
description: "[タスク] 2. Issue詳細化 + 依存関係設定"
---

# [タスク] 2. Issue詳細化 + 依存関係設定

## 入力: $ARGUMENTS
- Milestone名（例: `sprint-1`）または Issue番号（例: `#123`）

---

## 🎯 目的
- 指定したSprint（Milestone）内のIssueに **実装詳細** を追記する
- 組み込みTaskの **依存関係（blocks/blockedBy）** を設定する
- 実装前の調査・準備を明示的に行い、品質を担保する
- GitHub Issue と 組み込みTask の両方に依存関係を反映する

---

## 共通前提（参照）
- 口調・出力規約・TDD・Docコメント等は `CLAUDE.md` に従う
- `doc/input/rdd.md` を読み、該当する `.claude/skills/*` を適用
- 詳細運用は `doc/guide/ai_guidelines.md` を参照

---

## 実行手順

### 1. 対象Issue一覧取得
```bash
# Milestone指定の場合
gh issue list --milestone "sprint-1" --state open --json number,title,body

# Issue番号指定の場合
gh issue view 123 --json number,title,body
```

### 2. 一覧表示 + 選択
```
📋 Sprint: sprint-1

┌────┬─────────────────────┬──────────┬─────────────┬─────────────┐
│ #  │ Title               │ Issue    │ Task Status │ 詳細化      │
├────┼─────────────────────┼──────────┼─────────────┼─────────────┤
│ 1  │ ユーザー認証実装     │ #123     │ pending     │ ❌ 未       │
│ 2  │ ログイン画面作成     │ #124     │ pending     │ ❌ 未       │
│ 3  │ API設計             │ #125     │ pending     │ ✅ 済       │
└────┴─────────────────────┴──────────┴─────────────┴─────────────┘

→ どのIssueを詳細化する？ [番号を入力]
```

### 3. 調査・準備
選択したIssueに対して以下を調査：

1. **コードベース分析**
   - 類似機能/参照ファイル/命名規約/テスト雛形の抽出
   - **重複回避**を最優先し、既存拡張で解決できるか確認

2. **外部調査**
   - 公式Doc(URL)、GitHub実装例、StackOverflow（出典実在のみ）

3. **RDD整合チェック**
   - 技術スタック/制約/非機能要件の遵守を確認
   - **決定理由/背景**を記録

4. **依存関係の特定**
   - このタスクが依存するタスク（blockedBy）
   - このタスクを待っているタスク（blocks）

### 4. Issue本文に詳細追記
```bash
# 現在の本文を取得
BODY=$(gh issue view 123 --json body --jq '.body')

# 詳細を追記（⚠️ 確認あり）
gh issue edit 123 --body "${BODY}

---
## 実装詳細（/task-detail で追記）

### 技術スタック
{RDD指定のスタック}

### 参照ドキュメント
- [公式Doc] {タイトル} — {URL}
- [既存コード] {path/to/file}

### 実装ブループリント
\`\`\`typescript
// 擬似コード
function example() {
  // ...
}
\`\`\`

### 依存関係
- **blockedBy**: #124（これが完了してから着手）
- **blocks**: #126（これの完了を待っている）

### 難所検証方針
- {最小サンプルで検証する内容}

### 変更要求（必要時のみ）
> **ADR-lite**: {変更内容と理由}
> **承認状況**: 待ち / 承認済み
"
```

### 5. 組み込みTask依存関係設定
GitHub Issue の依存関係を組み込みTaskにも反映する：

```
TaskUpdate:
  taskId: "{task-id}"        # metadata.issueNumber で特定
  addBlockedBy: ["{blocking-task-id}"]
  addBlocks: ["{blocked-task-id}"]
```

### 6. ラベル追加
```bash
# 詳細化完了を示すラベル（⚠️ 確認あり）
gh issue edit 123 --add-label "ready-for-dev"
```

---

## 依存関係の可視化
```
📊 依存関係グラフ

#123 ユーザー認証実装
  └─→ #124 ログイン画面作成（#123 完了後）
       └─→ #125 E2Eテスト（#124 完了後）

#126 API設計（独立、並行実行可）
```

---

## 出力

### GitHub
- **Issue本文**: 実装詳細セクションを追記
- **ラベル**: `ready-for-dev` を追加

### 組み込みTask
- **TaskUpdate**: blocks/blockedBy で依存関係を設定

---

## 品質チェックリスト
- [ ] 参照ドキュメントが**実在**するURLである
- [ ] 既存コードの参照箇所が特定されている
- [ ] 実装ブループリント（擬似コード）が明確
- [ ] 依存関係がIssue本文と組み込みTaskの**両方**に設定されている
- [ ] `ready-for-dev` ラベルが付与されている
- [ ] 変更要求がある場合は**承認待ち**を明記

---

## 自己評価
- **成功自信度**: (1-10)
- **一言理由**: {短く理由を記載}

---

## 次のステップ
```bash
/task-run  # 実行可能なIssue（依存解決済み）を表示・実行
```
