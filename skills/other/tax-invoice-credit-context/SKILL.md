---
name: tax-invoice-credit-context
description: >
  Background context for invoice-system input tax credit rules (仕入税額控除)
  in the shinkoku tax filing plugin. Contains eligibility requirements,
  the 6 permanent exceptions (帳簿のみ保存の恒久特例), transitional measures
  for purchases from tax-exempt businesses, and storage requirements.
  This skill is not user-invocable — Claude loads it automatically when
  responding to input tax credit questions under the invoice system.
user-invocable: false
---

# インボイス仕入税額控除コンテキスト（Input Tax Credit Context）

このスキルはインボイス制度における仕入税額控除の要件・例外に関するコンテキストを提供する。

## 仕入税額控除の情報提供

仕入税額控除に関する回答を行う際は、`references/input-tax-credit-rules.md` を読み込んで以下を実行する:

1. 原則（適格請求書＋帳簿の保存）を確認して案内する
2. 帳簿のみ保存の恒久特例6類型（公共交通機関・自販機・郵便等）への該当を確認する
3. 免税事業者からの仕入れに係る経過措置の控除率（80%→70%→50%→30%→0%）を案内する
4. 課税売上割合に応じた控除方式（全額控除・個別対応方式・一括比例配分方式）を説明する
5. 保存期間（7年間）と電子取引データ保存の要件を案内する

## 参照ファイル

| ファイル | 内容 |
|---------|------|
| `references/input-tax-credit-rules.md` | 仕入税額控除の原則・帳簿記載要件・恒久特例6類型・経過措置・課税売上割合と控除方式 |
