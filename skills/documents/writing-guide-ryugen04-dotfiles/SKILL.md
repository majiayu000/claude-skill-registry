---
name: writing-guide
description: 'Use when creating or reviewing technical documentation. Provides guidelines
  for natural, readable Japanese writing without AI-generated artifacts. Triggers:
  (1) creating technical documents or READMEs'
---

---
name: writing-guide
description: Use when creating or reviewing technical documentation. Provides guidelines for natural, readable Japanese writing without AI-generated artifacts. Triggers: (1) creating technical documents or READMEs, (2) proofreading or reviewing existing documents, (3) writing blog posts or technical explanations.
---

# 技術ドキュメント作成・校正

## 実行方法

ドキュメント作成・校正はsubagentを起動して実行すること。
大量のコードからドキュメントを生成する場合はGemini MCPに委託する。

## 禁止事項

- 太字（`**`）は3回未満に制限
- 見出し・文末でのコロン使用禁止
- 「以下に〜」「次に〜」「最後に〜」の定型表現禁止
- 「おそらく」「思われます」など推測表現禁止
- 同一専門用語の不自然な繰り返し禁止
- 体言止めの連続使用禁止

## 必須要素

- 技術情報にはバージョン情報と情報源を明記
- 具体例やコード例を提供
- 自然で人間らしい表現

## 校正チェックリスト

文体:
- [ ] 太字3回未満
- [ ] コロン不使用
- [ ] 定型・推測表現なし

技術的正確性:
- [ ] 情報源あり
- [ ] 具体例あり
