---
name: review-flow
description: PR作成後に自動的に実行する必要があるフロースキルです
argument-hint: [--light | --deep]
---

PR について理解しPR authorの身になってレビューを開始します。

## 自動判定ロジック
引数がない場合、以下で判定：
- 変更ファイル数 ≤ 3 かつ 変更行数 ≤ 50 → light
- 認証/決済/API/DB/セキュリティ関連の変更 → deep
- それ以外 → light

## --light（model: haiku）
簡易チェック：
- lint漏れ、型エラー
- 明らかなバグ
- console.log の残存
- 未使用のインポート/変数

結果を簡潔に報告してください。

## --deep（model: opus）
設計レベルのレビュー。parallel に以下の subagents を実行：

1. code-review subagent
   - コード品質、可読性、保守性
   - エラーハンドリング
   - 型安全性

2. QA subagent
   - 動作確認手順の提示
   - 期待される結果
   - エッジケースの確認

3. security-reviewer（該当する場合）
   - 認証・認可の漏れ
   - 入力値検証
   - 機密情報の露出

## 脆弱性対応フロー（重要）

もし `security-reviewer` が **High/Critical** な脆弱性を検出した場合：

1. 具体的なリスクと攻撃シナリオを提示する
2. **「⚠️ マージ不可」**と明確に宣言する
3. 修正方針を提案：
   - **実装ミス**: 現在のPRで修正コミットを追加
   - **設計ミス**: `/reject-pr` でPRを閉じて再設計を推奨
4. 必要に応じて `ticket-feedback` で修正タスクをLinearに登録

## 出力順序
1. コードの解説（何を変更したか）
2. 各subagentのフィードバック
3. 改善提案（優先度付き）
4. セキュリティ問題がある場合は明確な警告
