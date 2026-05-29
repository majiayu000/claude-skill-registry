---
name: ideation
description: アイデア・企画フェーズを実行。problem-definition → competitor-analysis → slc-ideation を順次実行し、PRODUCT_SPEC.md を生成。「企画フェーズを開始」「アイデアをまとめたい」「/ideation」などで起動。
---

# アイデア・企画フェーズ

## 概要

3つのスキルを順次実行し、プロダクトアイデアを仕様書にまとめる。

## 実行スキル

1. **problem-definition** → docs/PROBLEM_DEFINITION.md
2. **competitor-analysis** → docs/COMPETITOR_ANALYSIS.md
3. **slc-ideation** → docs/PRODUCT_SPEC.md

## ワークフロー

### フェーズ0: 既存ドキュメントの確認

以下のファイルを確認し、開始ポイントを提案する。

```javascript
Read({ file_path: "docs/PROBLEM_DEFINITION.md" })
Read({ file_path: "docs/COMPETITOR_ANALYSIS.md" })
Read({ file_path: "docs/PRODUCT_SPEC.md" })
```

存在するファイルがあれば、スキップするか確認：

```javascript
AskUserQuestion({
  questions: [{
    question: "既存のドキュメントがあります。どこから開始しますか？",
    header: "開始ポイント",
    options: [
      { label: "最初から", description: "problem-definitionから開始" },
      { label: "competitor-analysisから", description: "PROBLEM_DEFINITION.mdを活用" },
      { label: "slc-ideationから", description: "既存の分析結果を活用" }
    ],
    multiSelect: false
  }]
})
```

**遷移条件**: 開始ポイントが決まったら該当ステップへ

### ステップ1: 問題定義

進捗を表示：

```
📍 アイデア・企画フェーズ [1/3]
   ├─ ▶ problem-definition（実行中）
   ├─ ○ competitor-analysis
   └─ ○ slc-ideation
```

Skill toolで起動：

```javascript
Skill({ skill: "problem-definition" })
```

完了後、確認：

```javascript
AskUserQuestion({
  questions: [{
    question: "problem-definitionが完了しました。次に進みますか？",
    header: "次のステップ",
    options: [
      { label: "次へ進む", description: "competitor-analysisを開始" },
      { label: "ここで終了", description: "後で続きを実行" }
    ],
    multiSelect: false
  }]
})
```

**遷移条件**: 「次へ進む」選択でステップ2へ、「終了」で完了

### ステップ2: 競合分析

進捗を表示：

```
📍 アイデア・企画フェーズ [2/3]
   ├─ ✓ problem-definition（完了）
   ├─ ▶ competitor-analysis（実行中）
   └─ ○ slc-ideation
```

Skill toolで起動：

```javascript
Skill({ skill: "competitor-analysis" })
```

完了後、確認：

```javascript
AskUserQuestion({
  questions: [{
    question: "competitor-analysisが完了しました。次に進みますか？",
    header: "次のステップ",
    options: [
      { label: "次へ進む", description: "slc-ideationを開始" },
      { label: "ここで終了", description: "後で続きを実行" }
    ],
    multiSelect: false
  }]
})
```

**遷移条件**: 「次へ進む」選択でステップ3へ、「終了」で完了

### ステップ3: SLC壁打ち

進捗を表示：

```
📍 アイデア・企画フェーズ [3/3]
   ├─ ✓ problem-definition（完了）
   ├─ ✓ competitor-analysis（完了）
   └─ ▶ slc-ideation（実行中）
```

Skill toolで起動：

```javascript
Skill({ skill: "slc-ideation" })
```

### 完了

```
✅ アイデア・企画フェーズ完了

生成されたドキュメント：
- docs/PROBLEM_DEFINITION.md
- docs/COMPETITOR_ANALYSIS.md
- docs/PRODUCT_SPEC.md

次のステップ：
- /requirements で要件・設計フェーズへ
```

## 完了条件

- [ ] 3つのスキルがすべて実行された（またはスキップ）
- [ ] PRODUCT_SPEC.mdが生成された

## 関連スキル

- **requirements**: 次フェーズ（要件・設計）へ進む場合に使用
