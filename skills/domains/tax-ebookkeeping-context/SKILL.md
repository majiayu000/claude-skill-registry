---
name: tax-ebookkeeping-context
description: >
  Background context for the Electronic Bookkeeping Act (電子帳簿保存法) in the
  shinkoku tax filing plugin. Contains requirements for electronic bookkeeping,
  scanner storage, mandatory electronic transaction data storage, and shinkoku's
  compliance status.
  This skill is not user-invocable — Claude loads it automatically when
  responding to electronic bookkeeping compliance questions.
user-invocable: false
---

# 電帳法コンテキスト（Electronic Bookkeeping Context）

このスキルは電子帳簿保存法の要件・対応状況に関するコンテキストを提供する。

## 電帳法の情報提供

電子帳簿保存法に関する回答を行う際は、`references/electronic-bookkeeping.md` を読み込んで以下を実行する:

1. 3つのカテゴリ（電子帳簿等保存・スキャナ保存・電子取引データ保存）を区別して説明する
2. 電子取引データ保存の義務化（令和6年1月1日〜）を確認・案内する
3. 優良な電子帳簿の要件と65万円控除（令和9年〜75万円控除）との関係を説明する
4. shinkoku の電帳法対応状況（一般・優良の両要件を充足）を確認する
5. 個人事業主向けの実務ガイダンス（最低限やるべきこと）を案内する

## 参照ファイル

| ファイル | 内容 |
|---------|------|
| `references/electronic-bookkeeping.md` | 電帳法3カテゴリ・要件・猶予措置・shinkoku対応状況・令和9年改正対応 |
