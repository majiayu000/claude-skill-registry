---
name: frontend-design
description: |
  Create distinctive, production-grade frontend interfaces with high design quality.
  Use when building web components, pages, or applications. Generates creative, polished UI
  that avoids generic "AI slop" aesthetics.
  Triggers: 「UIを作成」「コンポーネントを作って」「美しいページを」「デザインを改善」
  Project stack: Next.js 16 + React 19 + TailwindCSS 4 + shadcn/ui
---

# Frontend Design Skill

高品質なフロントエンドUI/UXを設計・実装するスキル。「AIスロップ」を回避する美学的指針を提供する。

## Project-Specific Stack

- **Framework**: Next.js 16 (App Router, 静的生成 `output: 'export'`)
- **UI Library**: React 19
- **Styling**: TailwindCSS 4 + shadcn/ui (Radix UI基盤)
- **Components**: `frontend/src/components/` に配置
- **Path Alias**: `@/*` → `./src/*`
- **Lint**: Biome 2（インデント2スペース、セミコロン付与、シングルクォート）

## Design Thinking

コーディング前に、コンテキストを理解し**大胆な**美的方向性を決定する:

1. **Purpose**: このインターフェースが解決する問題は？誰が使う？
2. **Tone**: 明確なトーンを選択（ミニマリスト、レトロフューチャー、ラグジュアリー、プレイフル等）
3. **Constraints**: 技術的制約（パフォーマンス、アクセシビリティ）
4. **Differentiation**: 何が**忘れられない**印象を与えるか？

## Aesthetics Guidelines

### DO ✅

- **Typography**: 美しく、ユニークなフォント選択。Google Fontsから特徴的なフォントを選ぶ
- **Color**: CSS変数で一貫性を保つ。ドミナントカラー + シャープなアクセント
- **Motion**: hover効果、マイクロアニメーション。CSS-onlyが理想
- **Spatial**: 予想外のレイアウト。非対称。オーバーラップ。豊かなネガティブスペース
- **Backgrounds**: 雰囲気と深度を作り出す。グラデーションメッシュ、ノイズテクスチャ、幾何学パターン

### DON'T ❌

- Inter、Roboto、Arial、システムフォントの使用
- 紫グラデーション on 白背景
- 予測可能なレイアウトとコンポーネントパターン
- 同じデザインの繰り返し（毎回異なるアプローチを取る）

## Implementation Rules

- `any` 禁止（TypeScript strict）
- アクセシビリティ（aria属性、キーボード操作）を考慮
- shadcn/uiコンポーネントを積極的に活用
- `@/` パスエイリアスでインポート
- Biome lint/formatに適合するコード

## Output

実装後、以下で確認:
```bash
cd frontend && npm run check:fix && npm run type-check
```
