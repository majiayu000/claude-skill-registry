---
name: design-implementation-guide
description: アクセシビリティ（WCAG/ARIA/コントラスト比）やデザイントークンを実装する際に使用。フォーム・エラー表示・キーボード操作の実装時に参照。
---

## Overview

このスキルは、アクセシビリティと一貫性を重視したUI実装のガイドラインを提供します。

## Files in This Skill

- **SKILL.md** (this file) - 使用場面とルール概要
- **tokens.md** - デザイントークンとStyle Dictionary設定
- **accessibility.md** - WCAG、ARIA、キーボード操作、コントラスト
- **examples.md** - 実装例とサンプルコード

## 使う場面

- フォーム・ボタン・エラー表示を含むインタラクティブUIを新規作成する
- 既存コンポーネントのアクセシビリティ（ARIA・キーボード操作・コントラスト）を修正する
- デザイントークンをWeb/iOS/Android各プラットフォームへ自動出力する
- レスポンシブ環境でタイポ・余白を流体スケールで統一する
- 多言語・縦書き・RTL対応でレイアウトを論理プロパティへ移行する

## 12のルール

### 1. トークンを明示せよ
色・余白・文字サイズは全てCSS Custom Propertyで定義し、生値を直書きするな。

### 2. コントラスト比を数値で保証せよ
本文は4.5:1以上（WCAG AA）、18pt以上または太字14pt以上は3:1以上を維持せよ。

### 3. 可変フォントとclamp()で流体スケールを実装せよ
文字サイズは `clamp(1rem, 0.875rem + 0.5vw, 1.125rem)` のように下限・可変・上限を明記せよ。

### 4. 論理プロパティで物理方向依存を排除せよ
`margin-left` → `margin-inline-start`、`padding-top` → `padding-block-start` を用いよ。

### 5. 全インタラクティブ要素をキーボード到達可能にせよ
`<button>`, `<a>`, `<input>` 等のネイティブ要素を優先せよ。

### 6. 状態（hover/focus/active/disabled）を視覚とARIAで二重に伝達せよ
`:focus-visible` でフォーカスリングを表示し、`aria-disabled="true"` でスクリーンリーダーへ通知せよ。

### 7. エラーは要約→詳細の順で構造化せよ
フォーム送信失敗時、ページ上部に `role="alert"` でエラー数と各フィールドへのアンカーリンクを配置せよ。

### 8. エラーメッセージは行動を明示せよ
❌「入力が無効です」→ ✅「メールアドレスに@を含めてください」

### 9. 同期検証はaria-live、非同期はrole="status"を使い分けよ
入力中のリアルタイム検証は `aria-live="polite"`、非同期API応答は `role="status"` を使用せよ。

### 10. 最小タッチターゲットを守れ
モバイルは44×44px、デスクトップは24×24pxの最小タッチターゲットを確保せよ。

### 11. レスポンシブブレークポイントは流体スケールで不要とせよ
`clamp()` による連続スケールで段階的変化を排除せよ。

### 12. プラットフォーム出力は自動化せよ
`tokens.json` からStyle Dictionaryで各形式を生成し、手動コピーを禁止せよ。

## QAチェックリスト

1. **Tab**キーで全インタラクティブ要素へ順番に到達できる
2. エラー発生時、フォーカスがエラー要約（`role="alert"`）へ自動移動する
3. 各エラーメッセージが対応する入力フィールドに`aria-describedby`で紐付いている
4. 本文のコントラスト比が4.5:1以上
5. キーボードのみで全コンポーネントの状態が識別可能
6. ビューポート幅320px～1280pxで文字サイズ・余白が`clamp()`により連続的に変化する
7. `margin-inline-start`等の論理プロパティを使用
8. 状態色が各トーンで一貫したコントラスト比を保つ
9. `tokens.json`がStyle Dictionary経由で各形式へ出力可能
10. 各ルールに参照元ソースのURLを付与

## 参考リンク

- [Material Design 3](https://m3.material.io/components)
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [Fluent 2 Design System](https://fluent2.microsoft.design/)
- [GOV.UK Design System](https://design-system.service.gov.uk/)
- [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/)
- [WAI-ARIA APG](https://www.w3.org/WAI/ARIA/apg/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Style Dictionary](https://styledictionary.com/)
- [Utopia - Fluid Responsive Design](https://utopia.fyi/)

## See Also

- **tokens.md** - デザイントークンの詳細と設定方法
- **accessibility.md** - アクセシビリティ実装の詳細
- **examples.md** - 完全な実装例
