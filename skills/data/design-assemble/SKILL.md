---
user-invocable: true
description: "[デザイン] 4. variants → 型付きProps/属性にマッピングして結合（再利用UI）"
---

# [デザイン] 4. variants → 型付きProps/属性にマッピングして結合（再利用UI）

## コマンド: /design-assemble [$TARGET]
`doc/input/design/components.json` の variants を **型付きProps/属性** にマッピングし、選択スタックへ**結合（再利用可能UI）**するアダプタ層。
既定は doc/input/rdd.md の技術スタック。引数で変更する際は **ADR-lite承認必須**。

## いつ使う？（位置づけ）
- `/design-ui` → `/design-components` が終わって、見た目の部品が分離できたあと
- `components.json` の variants を「実装の分岐（props/attrs/enum）」に落とし、再利用可能なUIとして仕上げたいとき

## 次に何をする？
- 実装タスクへ合流（状態/データ取得/ルーティング等は別工程で入れる）

## 共通前提（参照）
- 口調・出力規約・差分出力の方針は `CLAUDE.md` に従う。
- `doc/input/rdd.md` を読み、該当する `.claude/skills/*` を適用して判断軸を揃える。
  - 例（ロール）: `frontend-implementation` / `accessibility-engineer`
  - 例（tech）: `react` / `astro` / `svelte` / `tailwind`（※テンプレートでは固定せず、RDDのスタックに合わせて選ぶ）
- 詳細運用（ADR-lite/差分/サンプル運用等）は `doc/guide/ai_guidelines.md` を参照。
- SSOT JSON のスキーマ（variants命名/props/slots）は `doc/input/design/ssot_schema.md` を参照。

### 入力
- $TARGET（任意）: react | vue | svelte | swiftui | flutter | web-components | plain-html …

### 出力（差分のみ）
- スタック別の再利用UI
  - React: `src/components/{Name}.tsx`（Props型: size/tone/state…）, `src/stories/*`, `__tests__/*`
  - Vue: `src/components/{Name}.vue`（props + Story）
  - Svelte: `src/lib/{Name}.svelte`（props + Story）
  - SwiftUI: `Sources/UI/{Name}.swift`（case/enumでvariants）
  - Flutter: `lib/widgets/{name}.dart`（enum/Theme拡張）
  - Web Components: `src/components/{name}.ts`（attrs/reflect + CSS Custom Props）
- すべて **差分リファクタ**（skeleton → 再利用化）。仕様追加禁止。

### マッピング規約（例）
- variants.size → props.size（"sm"|"md"|"lg"）/ enum 等
- variants.tone → tokensのsemantic colorキーにバインド
- state（hover/disabled） → スタック標準のstate表現
- Docコメント（JSDoc/Docstring/Swift Doc/ Dartdoc）必須

### ルール
- **RDD準拠/SOLID**。逸脱は ADR-lite で理由と影響を明記
- **a11y必須**（セマンティックHTML/JSX + 必要最小限のWAI-ARIA）。詳細は `.claude/skills/accessibility-engineer/SKILL.md` に従う。
- Lint/Type/Test/Story すべて緑
- ここで停止

### ゲート
- Storybook/Preview で全variants表示OK
- Lint/Type/Test green（対応スタックのみ）
