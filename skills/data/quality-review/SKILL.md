---
name: quality-review
description: Performs automated code quality review before commit/merge. Use this skill when reviewing code changes for Issue alignment, coding standards compliance, and potential issues.
---

# Quality Review

コード品質レビューを実施し、コミット/マージ前の品質保証を行う。

## Goal

AI生成コードの品質を保証し、Issue目的との整合性を確認する。

## Instructions

1. **変更内容を確認**
   ```bash
   git status
   git diff --stat
   git diff HEAD
   ```

2. **以下の観点でレビューを実施**

   | カテゴリ | チェック項目 |
   |----------|------------|
   | **Issue整合性** | 当初のIssue要件を満たしているか |
   | **ルール遵守** | `AGENTS.md` のルール（コミット規則、命名規則等）に従っているか |
   | **コード一貫性** | 命名規則、スタイル、アーキテクチャが既存コードと統一されているか |
   | **ハードコード** | マジックナンバー、固定パス、環境依存値が抽出されているか |
   | **ポータビリティ** | 他の環境でも動作するか |
   | **データ保護** | 重要データが `data/shared/` に保存されているか |
   | **テスト** | 必要なテストが実施されているか |
   | **品質** | lint, type check, 重複コード、過度な複雑性がないか |
   | **セキュリティ** | 脆弱性、機密情報の漏洩がないか |
   | **ドキュメント** | README やコメントが更新されているか |

3. **レビュー結果を報告**
   - 問題があれば修正提案を提示
   - 問題なければ次のステップへの進行を提案

## Output Format

```
【レビュー結果】
- Issue目的との整合性: ✅/❌
- プロジェクトルール遵守: ✅/❌
- 既存コードとの一貫性: ✅/❌
- ハードコーディング: ✅ なし / ❌ あり
- ポータビリティ: ✅/❌
- データ保護設計: ✅/❌
- テスト実施: ✅/❌
- コード品質: ✅/❌
- セキュリティ: ✅/❌
```

## Constraints

- 必ずユーザー承認を得てから次のステップに進む
- 問題がある場合は具体的な修正提案を行う
