---
name: tax-housing-loan-context
description: >
  Background context for housing loan tax credit (住宅ローン控除) in the shinkoku
  tax filing plugin. Contains eligibility requirements, credit limits, calculation
  rules, and interaction with furusato-nozei for the current tax year.
  This skill is not user-invocable — Claude loads it automatically when
  responding to housing loan tax credit questions or calculations.
user-invocable: false
---

# 住宅ローン控除コンテキスト（Housing Loan Tax Credit Context）

このスキルは住宅ローン控除（租税特別措置法第41条）に関する判定・計算コンテキストを提供する。

## 住宅ローン控除の情報提供

住宅ローン控除に関する回答を行う際は、`references/housing-loan.md` を読み込んで以下を実行する:

1. 適用要件（住宅・所得・ローン要件）を確認し、ユーザーへの判定フローに沿って案内する
2. 借入限度額・控除率・控除期間を令和7年分の値で提示する
3. 子育て世帯・若者夫婦世帯の上乗せ措置の適用可否を確認する
4. ふるさと納税との相互影響を説明する（必要な場合）
5. 重複適用（中古購入＋リフォーム同時）の計算が必要な場合は按分計算を行う

## 参照ファイル

| ファイル | 内容 |
|---------|------|
| `references/housing-loan.md` | 控除額・借入限度額テーブル・適用要件・判定フロー・重複適用の計算例 |
