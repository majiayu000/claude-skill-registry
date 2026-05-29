---
name: tax-legal-context
description: >
  Background legal and regulatory context for the shinkoku tax filing plugin.
  Contains the standard disclaimer about the scope of tax information provided,
  the relationship to the Tax Accountant Act (税理士法), and tool limitations.
  This skill is not user-invocable — Claude loads it automatically when
  generating tax-related responses that require a disclaimer.
user-invocable: false
---

# 税務法的コンテキスト（Tax Legal Context）

このスキルは shinkoku の税務関連回答における法的・免責コンテキストを提供する。

## 免責事項の提示

免責事項が必要な回答を行う際は、`references/disclaimer.md` を読み込んで以下を実行する:

1. `references/disclaimer.md` の「標準免責文」を回答末尾に付記する
2. 免責を強調すべきケース（グレーゾーン・高額案件等）に該当する場合は追加注意喚起を行う
3. 税理士法第52条の観点から、個別具体的な税務代理行為に該当しないよう留意する

## 参照ファイル

| ファイル | 内容 |
|---------|------|
| `references/disclaimer.md` | 標準免責文・税理士法との関係・ツール制限事項・情報の正確性 |
