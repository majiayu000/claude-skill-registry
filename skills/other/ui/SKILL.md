---
name: ui
description: "Generates UI components and feedback forms. Use when user mentions コンポーネント, component, UI, ヒーロー, hero, フォーム, form, フィードバック, feedback, 問い合わせ. Do NOT load for: 認証機能, バックエンド実装, データベース操作, ビジネスロジック."
allowed-tools: ["Read", "Write", "Edit", "Bash"]
metadata:
  skillport:
    category: ui
    tags: [ui, component, form, feedback]
    alwaysApply: false
---

# UI Skills

UIコンポーネントとフォームの生成を担当するスキル群です。

## 含まれる小スキル

| スキル | 用途 |
|--------|------|
| component | UIコンポーネント生成 |
| feedback | フィードバックフォーム生成 |

## ルーティング

- コンポーネント生成: component/doc.md
- フィードバックフォーム: feedback/doc.md

## 実行手順

1. **品質判定ゲート**（Step 0）
2. ユーザーのリクエストを分類
3. 適切な小スキルの doc.md を読む
4. その内容に従って生成

### Step 0: 品質判定ゲート（a11y チェックリスト）

UI コンポーネント生成時は、アクセシビリティを確保:

```markdown
♿ アクセシビリティチェックリスト

生成する UI は以下を満たすことを推奨：

### 必須項目
- [ ] 画像に alt 属性を設定
- [ ] フォーム要素に label を関連付け
- [ ] キーボード操作可能（Tab でフォーカス移動）
- [ ] フォーカス状態が視覚的に分かる

### 推奨項目
- [ ] 色だけに依存しない情報伝達
- [ ] コントラスト比 4.5:1 以上（テキスト）
- [ ] aria-label / aria-describedby の適切な使用
- [ ] 見出し構造（h1 → h2 → h3）が論理的

### インタラクティブ要素
- [ ] ボタンに適切なラベル（「詳細」ではなく「製品詳細を見る」）
- [ ] モーダル/ダイアログのフォーカストラップ
- [ ] エラーメッセージがスクリーンリーダーで読まれる
```

### VibeCoder 向け

```markdown
♿ 誰でも使えるデザインにするために

1. **画像には説明をつける**
   - 「商品画像」ではなく「赤いスニーカー、正面から」

2. **クリックできる場所はキーボードでも操作可能に**
   - Tab キーで移動、Enter で決定

3. **色だけで判断させない**
   - 赤=エラー だけでなく、アイコン+テキストも
```
