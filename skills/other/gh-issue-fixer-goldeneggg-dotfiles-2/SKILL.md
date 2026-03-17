---
name: gh-issue-fixer
description: |
  GitHub Issue を修正するスキル。
  以下の状況で使用:
    (1) ユーザーが「Issue #XX を修正して」と依頼した時
    (2) ユーザーが明示的に「/gh-issue-fixer」を実行した時
    (3) GitHub Issue の対応を求められた時
---

# Fix GitHub Issue

GitHub Issue を修正する。

## ワークフロー

1. Issue の内容を確認（`gh issue view <issue-number>`）
2. 関連コードを調査
3. 修正を実装
4. テストを実行（存在する場合）
5. 変更内容をサマリ

## 出力

修正完了後、コミットメッセージの案を提示する。
