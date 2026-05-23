---
name: humanizer_academic
description: "学術・医療文書を AI らしい硬さから自然な英語へ人間化するスキル。Use when 論文、研究計画書、学会抄録、医療文書、カバーレターの英文を自然化したい場面。キーワード: humanize, academic writing, medical writing, manuscript polish."
---

# Humanizer Academic

`humanizer_academic` は、学術・医療領域の英語文を「正確さを維持したまま」自然で読みやすい文体に整えるためのスキル。

## 目的

| 項目 | 内容 |
|------|------|
| 主目的 | AI らしい不自然さ・過剰定型表現の除去 |
| 維持するもの | 事実、主張、数値、引用関係、専門用語の意味 |
| 想定ドメイン | 医学、生命科学、工学、社会科学などの学術文書 |

## 基本ワークフロー

1. 入力文書の種類を判定（Abstract / Introduction / Methods / Results / Discussion / Cover Letter）。
2. 事実情報（数値、固有名詞、因果関係）を固定して書き換え対象から除外。
3. 文体を自然化（冗長表現、過剰受動態、AI 定型句の削減）。
4. 学術トーンを維持しつつ可読性を上げる。
5. 最終出力で「変更後テキスト」と「主要な編集意図」を提示。

## 編集ルール

| ルール | 指針 |
|------|------|
| 意味保全 | 主張やデータを変更しない |
| 学術性 | カジュアル化しすぎない |
| 明確性 | 曖昧語を減らし、論理接続を明確にする |
| 簡潔性 | 冗長・重複を削る |
| 一貫性 | 用語、時制、主語を揃える |

## 出力フォーマット

```markdown
## Humanized Draft
<自然化後の本文>

## Edit Notes
- Tone: ...
- Clarity: ...
- Concision: ...
- Consistency: ...
```

## ソース

- GitHub: `https://github.com/matsuikentaro1/humanizer_academic`
