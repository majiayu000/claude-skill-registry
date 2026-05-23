---
name: pr-description
description: >-
  ユーザーが「PR説明を生成」「PR本文を作って」「プルリクエストの説明が欲しい」等と要求した時、または他のスキル（issue-fixなど）から呼び出された時に発動。
  git diffから変更内容を分析し、詳細なPR本文を生成する。
  チームの規約に準拠したフォーマットで出力する。
allowed-tools: Read, Bash, Grep
---

### 手順
1. **変更内容の取得**: `git diff main...HEAD` または指定されたブランチ間の差分を取得
2. **変更の分類**: ファイルごと、機能ごとに変更を整理
3. **影響範囲の分析**: 変更がどのコンポーネントに影響するかを特定
4. **テスト結果の取得**: 該当する場合、`go test` の結果を含める
5. **PR本文の生成**: 以下のセクションを含むマークダウン形式で生成
   - **Summary**: 変更の概要（1-3文）
   - **Changes**: 主な変更点の箇条書き
   - **Test Results**: テスト実行結果（成功/失敗、カバレッジ）
   - **Impact Analysis**: この変更が影響する範囲
   - **Verification**: レビュアーが確認すべきポイント
   - **Rollback Plan**: 問題発生時の復旧方法（重要な変更の場合）
6. **テンプレート適用**: `.claude/skills/issue-fix/templates/pr_template.md` が存在する場合は優先使用

### 出力フォーマット例
```markdown
## Summary
- Fix off-by-one error in Sum() function
- Add comprehensive test coverage

## Changes
- `pkg/calc/sum.go`: Fixed loop condition from `i < len(nums)-1` to `i < len(nums)`
- `pkg/calc/sum_test.go`: Added edge case tests (empty array, single element, negative numbers)

## Test Results
✅ All tests pass
- Coverage: 85% → 95%

## Impact Analysis
Low risk - isolated change in utility function with comprehensive tests

## Verification
- [ ] Confirm all existing tests still pass
- [ ] Verify new edge cases are covered
```

### ベストプラクティス
- 変更の「なぜ」を明確に説明（what だけでなく why）
- 技術的な詳細と、ビジネス/ユーザーへの影響の両方を含める
- 既存のPRを参考に、チームのトーンとスタイルに合わせる
