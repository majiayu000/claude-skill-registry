---
name: slc-ideation
description: SLC（Simple, Lovable, Complete）フレームワークに基づいてプロダクトアイデアの壁打ちを行います。対話的な質問を通じてアイデアを洗練し、SLCの3要素を満たすまで繰り返し検証します。最終的にプロダクト仕様書を生成します。「プロダクトアイデアを壁打ちしたい」「新規プロダクトの企画」「アイデアをSLCで検証」などのリクエストで起動します。
---

# SLC壁打ち

## 概要

SLC（Simple, Lovable, Complete）フレームワークに基づき、プロダクトアイデアを対話的に洗練する。MVPではなく「顧客が実際に使いたいと思える製品」を目指し、3要素すべてを満たすまで質問を繰り返す。

## 参照ドキュメント

- SLCフレームワーク: [references/slc-framework.md](references/slc-framework.md)
- 出力テンプレート: [references/product-spec-template.md](references/product-spec-template.md)

## SLCの3要素（判定基準）

### Simple（シンプル）

- 30秒以内で説明できる
- コア価値が1つに絞られている
- 2-4週間でリリース可能なスコープ

### Lovable（愛される）

- ターゲットユーザーが「これ欲しい」と即座に感じる
- 感情的な繋がりを生む要素がある
- 競合との差別化ポイントが明確

### Complete（完全）

- 限定されたスコープ内で「完成」と言える
- 追加開発なしでも価値を提供し続けられる
- ユーザーに「未完成」という印象を与えない

## ワークフロー

### フェーズ0: 前提ドキュメントの読み込み

前のステップの出力ファイルを読み込む。

#### 読み込み対象
- `docs/PROBLEM_DEFINITION.md`
- `docs/COMPETITOR_ANALYSIS.md`

```javascript
Read({ file_path: "docs/PROBLEM_DEFINITION.md" })
Read({ file_path: "docs/COMPETITOR_ANALYSIS.md" })
```

#### ファイルが存在する場合

読み込んだ内容から以下を抽出し、フェーズ1で活用：
- ジョブ定義（解決すべき問題）
- ターゲットユーザー
- 差別化ポイント（競合分析から）

**遷移条件**: フェーズ1へ（アイデア把握の質問を具体化）

#### ファイルが存在しない場合

フェーズ1でAskUserQuestionを使ってアイデアを確認。

**遷移条件**: フェーズ1へ

### フェーズ1: アイデアの把握

ユーザーのプロダクトアイデアを理解する。

**注**: フェーズ0で前提ドキュメントを読み込み済みの場合、それらの情報を元にアイデアを確認・補完する。

```javascript
AskUserQuestion({
  questions: [
    {
      question: "どんなプロダクトを作りたいですか？簡単に教えてください。",
      header: "アイデア",
      options: [
        { label: "アイデアを入力", description: "プロダクトの概要を自由に記述" }
      ],
      multiSelect: false
    }
  ]
})
```

### フェーズ2: SLC検証ループ

3要素すべてが満たされるまで、以下のサイクルを繰り返す。

#### 2.1 Simple検証

```javascript
AskUserQuestion({
  questions: [
    {
      question: "このプロダクトのコア価値は何ですか？1つだけ挙げてください。",
      header: "コア価値",
      options: [
        { label: "コア価値を入力", description: "ユーザーに提供する最も重要な価値" }
      ],
      multiSelect: false
    },
    {
      question: "30秒で説明するとしたら、どう説明しますか？",
      header: "ピッチ",
      options: [
        { label: "説明を入力", description: "簡潔な説明文" }
      ],
      multiSelect: false
    }
  ]
})
```

**検証ポイント**:
- 説明が複雑すぎないか？
- 機能が多すぎないか？
- さらにシンプルにできないか？

不十分な場合の深堀り：
```javascript
AskUserQuestion({
  questions: [
    {
      question: "もっとシンプルにするために、削れる機能はありますか？",
      header: "機能削減",
      options: [
        { label: "削れる機能がある", description: "具体的に入力" },
        { label: "これ以上削れない", description: "最小限の機能のみ" }
      ],
      multiSelect: false
    }
  ]
})
```

#### 2.2 Lovable検証

```javascript
AskUserQuestion({
  questions: [
    {
      question: "ターゲットユーザーは誰ですか？具体的に教えてください。",
      header: "ターゲット",
      options: [
        { label: "ユーザー像を入力", description: "具体的なペルソナや属性" }
      ],
      multiSelect: false
    },
    {
      question: "ユーザーはなぜ既存の解決策ではなく、これを使いたいと思うのですか？",
      header: "差別化",
      options: [
        { label: "理由を入力", description: "競合との違い、感情的な訴求点" }
      ],
      multiSelect: false
    }
  ]
})
```

**検証ポイント**:
- ターゲットが具体的か？
- 感情的な繋がりがあるか？
- 「欲しい」と思わせる要素があるか？

不十分な場合の深堀り：
```javascript
AskUserQuestion({
  questions: [
    {
      question: "ユーザーがこのプロダクトを友達に勧めるとしたら、何と言いますか？",
      header: "推薦理由",
      options: [
        { label: "推薦文を入力", description: "ユーザー視点での価値" }
      ],
      multiSelect: false
    }
  ]
})
```

#### 2.3 Complete検証

```javascript
AskUserQuestion({
  questions: [
    {
      question: "v1.0として必要な機能は何ですか？（最大3つ）",
      header: "必須機能",
      options: [
        { label: "機能を入力", description: "v1.0に必須の機能リスト" }
      ],
      multiSelect: false
    },
    {
      question: "これらの機能だけで、ユーザーは満足しますか？",
      header: "完成度",
      options: [
        { label: "はい", description: "この機能で十分な価値を提供できる" },
        { label: "追加が必要", description: "足りない機能がある" },
        { label: "削減が必要", description: "機能が多すぎる" }
      ],
      multiSelect: false
    }
  ]
})
```

**検証ポイント**:
- この範囲で「完成」と言えるか？
- 「未完成」という印象を与えないか？
- 継続開発なしでも価値があるか？

### フェーズ3: SLC達成確認

3要素すべてを満たしたことを確認する。

```
## SLCチェックリスト

### Simple
- [x] 30秒以内で説明できる
- [x] コア価値が1つに絞られている
- [x] スコープが限定されている

### Lovable
- [x] ターゲットユーザーが明確
- [x] 感情的な繋がりを生む要素がある
- [x] 差別化ポイントが明確

### Complete
- [x] 限定スコープ内で完成している
- [x] 追加開発なしでも価値がある
- [x] 未完成という印象を与えない
```

未達成の項目があれば、該当フェーズに戻って深堀りを続ける。

### フェーズ4: プロダクト仕様書生成

SLCを満たしたアイデアをドキュメントにまとめる。

テンプレートは [references/product-spec-template.md](references/product-spec-template.md) を参照。

```javascript
Write({
  file_path: "docs/PRODUCT_SPEC.md",
  content: productSpecContent
})
```

### フェーズ5: セルフレビュー（サブエージェント）

生成したドキュメントのレビューをサブエージェントに委譲する。

```javascript
Task({
  description: "プロダクト仕様書レビュー",
  subagent_type: "general-purpose",
  prompt: `
以下のプロダクト仕様書をレビューし、問題があれば修正してください。

## レビュー対象ファイル
- docs/PRODUCT_SPEC.md

## レビュー観点

1. **Simpleの達成**: 30秒で説明できるか、コア価値が1つに絞られているか
2. **Lovableの達成**: ターゲットが明確か、差別化ポイントが魅力的か
3. **Completeの達成**: 限定スコープ内で完成しているか、未完成感がないか
4. **一貫性**: 各セクション間で矛盾がないか
5. **具体性**: 曖昧な表現がなく、実装に移れる具体性があるか

## 出力形式

1. 発見した問題のリスト（問題がない場合は「問題なし」）
2. 各問題の修正内容
3. 修正後のファイル更新（Editツールで修正）

問題がなくなるまでレビューと修正を繰り返すこと。
`
})
```

## 壁打ち時の質問パターン

### スコープを絞る質問

- 「これをさらにシンプルにできないか？」
- 「本当に必要な機能はどれか？」
- 「v2以降に回せる機能はないか？」

### 愛される要素を引き出す質問

- 「ユーザーはなぜこれを使いたいと思うか？」
- 「競合にはない魅力は何か？」
- 「ユーザーの感情に訴えかける要素は何か？」

### 完成度を確認する質問

- 「この状態でリリースして恥ずかしくないか？」
- 「追加開発なしでも価値を提供できるか？」
- 「ユーザーに未完成という印象を与えないか？」

## 完了条件

- [ ] SLCの3要素すべてが満たされている
- [ ] プロダクト仕様書（PRODUCT_SPEC.md）が生成されている
- [ ] セルフレビューが完了し、問題が解消されている
- [ ] ユーザーがアイデアに納得している

## 関連スキル

- **analyzing-requirements**: 仕様が固まった後、詳細な設計を行う場合に使用
- **planning-tasks**: 実装タスクの分解を行う場合に使用
