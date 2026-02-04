---
user-invocable: true
description: "[デザイン] （任意）SSOT → 静的HTML を生成し、doc/input/design/html/ に保存"
---

# [デザイン] （任意）SSOT → 静的HTML を生成し、`doc/input/design/html/` に保存

## コマンド: /design-html [$PAGE_KEY]
設計JSON（SSOT）から**静的HTML**を生成し、`doc/input/design/html/` に保存する。

## いつ使う？（位置づけ）
- **ドキュメント共有/レビュー用**に「ブラウザで見られる見た目」が欲しいとき
- 実装スタックに依存しない形で、UIの骨格・トークン反映を目視確認したいとき
- `/design-ssot` または `/design-mock` で SSOT が揃っている前提（このコマンドはSSOTを作らない）

## 次に何をする？
- 見た目の調整が必要なら、HTMLの差分/変更点を根拠に SSOT（tokens/components/context）へ反映する
- 実装に進むなら `/design-ui` → `/design-components` → `/design-assemble`（READMEのフローに合流）

## 共通前提（参照）
- 口調・出力規約・差分出力の方針は `CLAUDE.md` に従う。
- `doc/input/rdd.md` を読み、該当する `.claude/skills/*` を適用して判断軸を揃える（例: `ui-designer` / `usability-psychologist` / `tailwind`）。
- 詳細運用（ADR-lite/差分/サンプル運用等）は `doc/guide/ai_guidelines.md` を参照。

## 見た目の基準（ビューポート）について
- まず `doc/input/rdd.md` の「ターゲット表示環境（事実）」を参照し、生成HTMLの確認は **そのビューポートを基準**に行う
- 未記入の場合は、以下を **推奨デフォルト**として仮置きする：
  - desktop: 1440x900
  - mobile: 390x844
  - tablet: 834x1194

### 入力
- $PAGE_KEY（任意）: 画面キー（`doc/input/design/design_context.json` の `pages[].key`）
  - 省略時: **全ページ**を生成する（複数ページ対応の既定）

### 出力（差分のみ）
- `doc/input/design/html/{page}.html`（tokens/variants/copy反映、外部依存なしで再現）

### 仕様
- 入力となるJSON（`doc/input/design/design-tokens.json`, `doc/input/design/components.json`, `doc/input/design/design_context.json`）が存在する前提（通常は `/design-ssot` の成果物）
- `doc/input/design/copy.json`（文言のSSOT。一字一句固定）が存在する前提（不足時は推測で補わず停止）
- `doc/input/design/assets/assets.json` が存在する場合は必ず参照し、画像アセットを反映する（baseDir配下の相対パス）
  - `assets.json` に `status: "failed"` がある場合は、**必ずユーザーに不足（動画/画像等）を報告**し、手元提供またはFigma Export設定の依頼をして停止する（推測で代替しない）
- React/Vue 等の実装に依存しない生成
- 画像は相対またはデータURIで完結
- **RDD準拠**のスタイルのみ（tokens必須）
- ここで停止

### ゲート
- 主要ブレイクポイントでレイアウト崩れなし（簡易スナップ）
- tokens外の値（magic number）が混入していない
- `copyKey` の不足0件（`design_context.json` の参照が `copy.json` で解決できる）
