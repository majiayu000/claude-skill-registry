---
name: sdd-tasks
description: 設計書に基づき実装タスクを分解し、タスクリスト（tasks.md）を作成する。
---

# sdd-tasks

## Description
設計書に基づき実装タスクを分解し、タスクリスト（tasks.md）を作成する。
Trigger examples: "タスク分解", "タスク出し", "実装計画", "break down tasks", "create task list", "タスクリスト作成", "TODO作成"

## 前提確認とspec特定
1. `.sdd/target-spec.txt` からspec名を取得し、`.sdd/specs/[spec名]/` の存在を確認する。
2. ステアリング情報（product.md, tech.md, structure.md）を読み込む。
3. 設計書（design.md）を読み込む。
   - 存在しない場合は `/sdd-design` を案内する。

## ステップ1：実装タスクリストの作成
`.sdd/specs/[spec名]/tasks.md` を作成する。
**重要**: 各タスクは「1〜3時間」で完了できる粒度に分解し、design.md の内容と対応付けること。

```markdown
# 実装タスクリスト

## セクション1：データモデル・準備
- [ ] 1.1 [タスク名]
  - 詳細: [design.mdの対応箇所]

## セクション2：コアロジック
- [ ] 2.1 [タスク名]
  - 詳細: ...

## セクション3：UI/API
- [ ] 3.1 [タスク名]

## セクション4：統合・テスト
- [ ] 4.1 結合テストの実装
- [ ] 4.2 受入基準の確認
```

## 完了確認
「タスクリスト完了。
実装を開始するには `/sdd-implement` を実行してください。
※すべてのタスクは順番に実装されるため、特定のタスクのみを選択するオプションはありません。」
