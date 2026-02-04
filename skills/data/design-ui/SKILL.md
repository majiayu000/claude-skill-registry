---
user-invocable: true
description: "[デザイン] 2. SSOT → 静的UI骨格（見た目のみ）を生成"
---

# [デザイン] 2. SSOT → 静的UI骨格（見た目のみ）を生成

## コマンド: /design-ui [$TARGET] [$PAGE_KEY]
設計JSON（tokens/components/design_context）を参照し、**静的UI骨格**のみ生成。
ロジック/状態/データ取得は入れない。ターゲットは **doc/input/rdd.md** の技術スタックを既定とし、引数で上書きする場合は **ADR-lite承認必須**。

## いつ使う？（位置づけ）
- `/design-ssot` または `/design-mock` で **SSOT（tokens/components/context）** が揃ったあと
- 「実装スタック準拠のファイル配置」で **見た目だけの骨格**を先に作りたいとき（後で分割・結合する前提）

## 次に何をする？
- 重複UIを減らして保守しやすくする → `/design-components`
- variantsを型付きprops/属性に落として再利用UIにする → `/design-assemble`

## 共通前提（参照）
- 口調・出力規約・差分出力の方針は `CLAUDE.md` に従う。
- `doc/input/rdd.md` を読み、該当する `.claude/skills/*` を適用して判断軸を揃える。
  - 例（ロール）: `frontend-implementation` / `accessibility-engineer`
  - 例（tech）: `react` / `astro` / `svelte` / `tailwind`（※テンプレートでは固定せず、RDDのスタックに合わせて選ぶ）
- 詳細運用（サンプル運用/依存評価補助/ADR-lite）は `doc/guide/ai_guidelines.md` を参照。

## 見た目の基準（ビューポート）について
- まず `doc/input/rdd.md` の「ターゲット表示環境（事実）」を参照し、プレビュー/Story等の確認は **そのビューポートを基準**に行う
- 未記入の場合は、以下を **推奨デフォルト**として仮置きする：
  - desktop: 1440x900
  - mobile: 390x844
  - tablet: 834x1194

### 入力
- $TARGET（任意）: react | vue | svelte | swiftui | flutter | web-components | plain-html など
- $PAGE_KEY（任意）: 画面キー（`doc/input/design/design_context.json` の `pages[].key`）
  - 省略時: **全ページ**を対象に生成する（複数ページ対応の既定）

### 出力（差分のみ）
- スタック別の標準配置へ静的UIファイル一式
  - 例: React → `src/components/*`, `src/stories/*`, `tailwind.config.js`(tokens反映)
  - 例: Vue → `src/components/*.vue`, `src/stories/*`
  - 例: SwiftUI → `Sources/UI/*`
- Storybook/プレビュー（対応スタックのみ）

### 前提（入力ファイル）
- `doc/input/design/design-tokens.json`
- `doc/input/design/components.json`
- `doc/input/design/design_context.json`
- `doc/input/design/copy.json`（文言のSSOT。一字一句固定）
 - `doc/input/design/assets/assets.json`（任意。存在する場合は必ず参照して画像を配置する）
（通常は `/design-ssot` の成果物）

### 参照（スキーマ）
- constraints/resizing/autoLayout の解釈とレスポンシブ対応表は `doc/input/design/ssot_schema.md` を参照する

### レスポンシブ適用規則（Figma→CSS/スタイル）
- Auto Layout → `flex` 等 + tokens の `gap/padding`
- constraints/resizing マッピング
  - horizontal: SCALE → `w-full` / `flex-grow` 等
  - vertical: TOP_BOTTOM → `h-full`（文脈でcol）
  - resizing: FILL → `flex-1` / `w-full`
  - resizing: HUG → `inline-size: max-content` / `inline-block`
- breakpoints → `doc/input/design/design-tokens.json` の `primitives.breakpoints` 準拠
- **tokens外の値禁止 / magic number禁止**

### 禁止
- 状態/ロジック/フェッチの追加
- RDD逸脱スタックの導入（$TARGET指定時はADR-lite要）
- `copy.json` の文言を推測/言い換えして埋めること（不足は不足として止める）
 - `div` クリック等でボタン/リンク相当を作ること（セマンティック要素を優先し、必要最小限のWAI-ARIAに限定する）

### 文言（copy）の適用ルール
- `design_context.json` の text ノードは `copyKey` を持つ前提で、対応する文言を `doc/input/design/copy.json` から参照して埋め込む
- `copyKey` が未定義/不足している場合は、**推測で生成しない**。ユーザーに以下を依頼して停止する：
  - `FIGMA_REF` を再提示して `/design-ssot` をやり直す
  - または `copy.json` の差分（追加すべきキーと文言）を提供してもらう

### 画像アセット（assets.json）の適用ルール
- `doc/input/design/assets/assets.json` が存在する場合は、`baseDir` 配下にある画像を参照してUI骨格に反映する
  - 例: Next/Astro/React → `public/design-assets/*`
  - 例: SvelteKit → `static/design-assets/*`
- `components.json` の `slots` や `usedBy` 情報と照合し、画像が必要な箇所（ロゴ/アイコン/イラスト/写真）の取りこぼしを防ぐ
- 画像の最適化（次世代フォーマット変換/圧縮/レスポンシブ画像生成等）は、この工程では必須にしない（まず再現性を優先）
- `assets.json` に `status: "failed"` がある場合は、**必ずユーザーに不足（動画/画像等）を報告**し、手元提供またはFigma Export設定の依頼をして停止する（推測で代替しない）

### ゲート
- 見た目一致（主要variantsのプレビュー/Story）
- tokens外の値0件 / Lint/Type green

**Agent Browser利用可能時（自律確認）:**
```bash
# Storybook または開発サーバーを起動後
agent-browser open http://localhost:6006  # Storybook
# または
agent-browser open http://localhost:3000/{対象パス}

# スナップショットで要素構造を確認
agent-browser snapshot -i

# 主要breakpointsでの表示確認（viewport変更）
# 問題発見時は修正後に再スナップショット
```
- デザインとの差異（余白/色/タイポ）を目視確認
- レスポンシブ崩れがないか確認

- ここで停止
