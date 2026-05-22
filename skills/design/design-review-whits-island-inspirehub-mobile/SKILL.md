---
name: design-review
description: 画面設計書とSwiftUIデザインガイドに対して現在の実装の準拠状況をレビューする
user-invocable: true
argument-hint: "[画面名|all] (例: HomeView, DetailView, all)"
allowed-tools: Read, Grep, Glob, mcp__xcode__XcodeRead, mcp__xcode__RenderPreview
---

# デザインレビュースキル

画面設計書とSwiftUIデザインガイドに対して、現在の実装の準拠状況をレビューする。

## 参照ドキュメント

- `docs/design/画面設計_ネイティブアプリ.md` — 画面仕様
- `docs/design/swiftui_design_guide.md` — デザインシステム

## 処理フロー

1. 参照ドキュメントを読み込み
2. 引数で指定された画面（またはall）のSwiftUIファイルを検査
3. チェック項目に沿って検査
4. 差分・未実装項目をリスト化
5. 改善提案をレポート出力

## チェック項目

### カラーパレット

- Primary: Blue
- Accent: Orange
- Issue badge: Orange
- Idea badge: Yellow

### タイポグラフィ

- largeTitle.bold, title2.bold, headline, body, caption

### スペーシング

- 4pt基準

### コンポーネント構成

- 画面設計書で定義されたUI要素が実装されているか

### アクセシビリティ

- Dynamic Type対応
- VoiceOver対応
- 44ptタッチターゲット
- WCAG AA準拠

## 出力フォーマット

```markdown
## デザインレビュー: [画面名]

### 準拠状況
| チェック項目 | ステータス | 詳細 |
|-------------|-----------|------|
| カラーパレット | 準拠 / 非準拠 | ... |
| タイポグラフィ | 準拠 / 非準拠 | ... |

### 未実装項目
- [ ] 画面設計書のXXセクションが未実装

### 改善提案
- ...
```
