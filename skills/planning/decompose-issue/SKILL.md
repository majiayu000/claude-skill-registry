---
name: decompose-issue
description: 既存の大きなIssueを適切な粒度のSubtaskに分解します。200行以下・3ファイル以下の粒度で子Issueを作成し、並列実装を可能にします。
---

# Issue分解コマンド (/decompose-issue)

既存の大きなIssueを適切な粒度のSubtask（子Issue）に分解します。
**200行以下・3ファイル以下**の粒度で子Issueを作成し、並列実装を可能にします。

---

## 処理フロー

```
1. 親Issue解析
   ↓
2. 依存関係グラフ作成
   ↓
3. 分解計画の作成（Phase 3.5 承認ゲート）
   ↓
4. 子Issue作成（GitHub API）
   ↓
5. 親Issue更新（タスクリスト追加）
```

---

## 1. 粒度判定（分解が必要か？）

> **参照元**: `issue-size-estimation` skill

| 状況 | 推定サイズ | アクション |
|------|-----------|----------|
| **すでに適切な粒度のIssue** | 200行以下 | 直接実装 |
| **大きなIssue** | 200行超 | **`/decompose-issue` で分解** |

### 目安となるキーワード
- "Implement entire feature..."
- "Create CRUD for..."
- "Add authentication system..."

---

## 2. 分解戦略（Decomposition Strategy）

### 2.1 水平分割（レイヤー別）

機能全体をレイヤーごとに分割する（最も一般的）。

- **Subtask 1**: DB Schema & Model
- **Subtask 2**: API/Backend Logic
- **Subtask 3**: Frontend UI

### 2.2 垂直分割（機能別）

独立した機能ごとに分割する。

- **Subtask 1**: Login API
- **Subtask 2**: Register API
- **Subtask 3**: Forgot Password API

### 2.3 依存関係の考慮

- `Is blocking`: 先に実装する必要があるIssue
- `Blocked by`: 依存先のIssueが完了するまで着手できないIssue

---

## 3. 出力形式

### Phase 3.5: 分解計画承認（Approval Gate）

Subtask作成前に、ユーザーに分解計画を提示して承認を得る。

```markdown
## 🧩 Issue分解計画承認

### 親Issue
#123: ユーザー認証機能の実装

### 提案するSubtask構成

| ID | Subtask名 | 依存関係 | 推定行数 |
|----|-----------|---------|---------|
| **S1** | DBスキーマとマイグレーション | - | 50行 |
| **S2** | バックエンドAPI実装 | Blocked by S1 | 150行 |
| **S3** | フロントエンドログイン画面 | Blocked by S2 | 100行 |

### 合計
- Subtask数: 3
- 総推定行数: 300行

---
**この計画でSubtaskを作成しますか？**

1. 作成する → GitHub Issueを作成
2. 修正する → 構成を見直す
3. キャンセル
```

---

## 4. Subtask作成後のアクション

Subtask作成後、Sisyphusに次のアクションを提示する。

```markdown
✅ Subtaskを作成しました。

### 作成されたIssue
- #124: DBスキーマとマイグレーション
- #125: バックエンドAPI実装
- #126: フロントエンドログイン画面

### 次のステップ
1. 実装に進む（順次実装）
```

---

## コマンド使用方法

```bash
/decompose-issue <issue_id>
```

**例**:
```bash
/decompose-issue 123
```

---

## エラーハンドリング

| エラー | 原因 | 対応 |
|--------|------|------|
| Issue not found | ID間違い | ID確認して再実行 |
| Already decomposed | 既に分解済み | 既存のSubtaskを確認 |
| Too small to decompose | 既に小さい | 分解不要と報告 |

---

## 関連スキル

- `issue-size-estimation`: 粒度判定ロジック
- `github-issue-dependency`: 依存関係設定
- `approval-gate`: 承認ゲートフォーマット
