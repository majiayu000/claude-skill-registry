---
user-invocable: true
description: "[デザイン] 1.（Figma起点）SSOT（tokens/components/context/assets）を生成"
---

# [デザイン] 1.（Figma起点）SSOT（tokens/components/context/assets）を生成

## コマンド: /design-ssot $FIGMA_REFS
Figma MCPから設計情報を抽出し、AI/人間が参照するSSOTを作る。**実装はしない**。

## いつ使う？（位置づけ）
- Figma（Dev Mode）を根拠に、後続でブレない **SSOT（tokens/components/context/assets）** を確立したいとき
- 会話起点なら `/design-mock`、Figma起点ならこの `/design-ssot` から始める

## 次に何をする？
- 実装に進む → `/design-ui` → `/design-components` → `/design-assemble`
- ドキュメント/共有用の静的HTMLが欲しい → `/design-html`（任意）

## 共通前提（参照）
- 口調・出力規約・差分出力の方針は `CLAUDE.md` に従う。
- `doc/input/rdd.md` を読み、該当する `.claude/skills/*` を適用して判断軸を揃える（例: `ui-designer` / `usability-psychologist`）。
- 詳細運用（サンプル運用/依存評価補助/ADR-lite）は `doc/guide/ai_guidelines.md` を参照。

## 見た目の基準（ビューポート）について
- まず `doc/input/rdd.md` の「ターゲット表示環境（事実）」を参照し、**そのビューポートを基準**にSSOTを作る
- 未記入の場合は、以下を **推奨デフォルト**として仮置きし、出力やレビューの前提に明記する：
  - desktop: 1440x900
  - mobile: 390x844
  - tablet: 834x1194

## 事前チェック（必須）：Figma MCPが「使える」状態か
`/design-ssot` は **Figma MCPが利用可能であることが前提**。最初に必ず以下を確認してから進める。

### 1) Claude Code側：MCP登録の確認
- `claude mcp list` を確認し、`figma` が登録されていること

### 2) 接続先：Figma MCP（Dev Mode）の到達確認
- Figma MCPのエンドポイント（通常 `http://localhost:3845/mcp`）に到達できること
- 到達できない場合は、**MCPが未起動/未設定/権限不足**の可能性が高い（推測でSSOT生成を続けない）

### 3) うまくいかないとき（ユーザーにお願いする手順）
AI側で「MCPが無い/設定されていない」など見当違いな推測をしないために、まず以下をユーザーに依頼する：
0. **`/mcp` でFigmaの再接続を確認する（推奨）**
   - `/mcp` を実行
   - 一覧から **`figma` ツール**を選ぶ
   - **Reconnect**（再接続）を実行
   - 再度 `figma` ツールを選んだときに **"View tools" が表示されている状態**になっていることを確認する
   - 上記が満たせない場合は、以降の手順へ進まず停止（接続/権限/起動状態の問題の可能性が高い）
1. **Figma Desktop アプリで Dev Mode / MCP サーバーを有効化**する（Figma公式手順に従う）
2. それでもダメなら、ユーザーに以下を確認してもらう：
   - 3845番ポートが開いているか（Figma側のMCPが起動しているか）
   - URLが環境と合っているか（例: `http://localhost:3845/mcp`）
   - 必要なら MCP登録をやり直す

### 4) Figma MCPの登録
- **前提**
  - Figma Desktop 側で Dev Mode / MCP サーバーが有効で、MCPが起動していること
  - Claude Code（CLI）を実行する環境から、そのMCPのHTTPエンドポイントに到達できること
- **手順（最小）**
  1. `claude mcp list` を確認し、`figma` が無ければ登録する
     - 例: `claude mcp add --transport http figma "http://localhost:3845/mcp"`
  2. 到達できない場合は、ユーザーに「Figma側のMCP起動・権限・ポート・URL」を確認してもらう（推測で先に進めない）

### 入力
- $FIGMA_REFS: Figma参照（MCPが認識できる指定）
  - **単一**: これまで通り1つのFigma URL/参照を渡す
  - **複数（推奨）**: 複数のフレーム/ページURLを「ページキー付き」で羅列する（複数ページでも再現性を落とさないため）

#### 複数指定の書式（固定）
- 1行に1件: `{PageKey}={FIGMA_REF}`
  - 例: `HomePage=https://...`
  - 例: `PricingPage=https://...`
- **禁止**: URLだけの羅列（ページキーが安定しないため）。複数指定時は必ず `PageKey=` を付ける

#### PageKeyのルール（固定）
- `PascalCase` 推奨（例: `HomePage`, `PricingPage`, `LoginPage`）
- 既存の `doc/input/design/design_context.json` に同名 `pages[].key` がある場合は「追記/更新」扱い
- 同名キーで別画面を指す場合は **衝突**として停止（推測でマージしない）

#### 例
- 単一:
  - `/design-ssot https://...`
- 複数:
  - `/design-ssot HomePage=https://... PricingPage=https://... LoginPage=https://...`

### 出力（差分のみ）
- doc/input/design/design_context.json   # 画面/レイアウト/constraints/resizing
- doc/input/design/design-tokens.json    # 色/タイポ/spacing/半径/影/枠線/不透明度/breakpoints（単位明記）
- doc/input/design/components.json       # 主要コンポーネント + variants（例: size/tone/state）
- doc/input/design/copy.json             # 文字の文言（copyKey→文言）。一字一句固定（言い換え禁止）
- (スタック既定の置き場)/design-assets/  # 画像アセット（Figmaからexportして保存）
- doc/input/design/assets/assets.json          # 画像アセットのmanifest（どの要素がどのファイルに対応するか）

### ルール
- JSONは**単位明記**（px/%/unitless）
- tokens は「物理値」と「semantic（意味）」を混ぜない（例: `color.gray.900` と `color.text.primary` を分け、semanticは物理へ参照する）
- variants は **props/属性に落とせる粒度**（例: { size:["sm","md","lg"] }）
- **文字の文言は必ずSSOT化**する（`doc/input/design/copy.json`）
  - `design_context.json` の text ノードは **必ず `copyKey` で `copy.json` を参照**する（文言の直書き禁止）
  - `copy.json` に無い `copyKey` を参照してはいけない（不足時は生成を止め、ユーザーに `FIGMA_REF` 再提示 or 文言提供を依頼する）
- **CSSで指定できる見た目は可能な限りSSOT化する**（後続の再現性を上げる）
  - 例: background（塗り/グラデ）/ border（stroke: 色・太さ・style・位置）/ radius / shadow / opacity / blur / blend mode
  - blur は **filter（要素自体）** と **backdrop-filter（背景）** を区別してSSOTに残す
  - 取りこぼしやすい: 「枠線だけある」「背景だけある」「hoverだけ変わる」など
- `components.json` には、可能な限り `styles`（background/border/radius/shadow/textColor など）を tokens 参照で残す（値の直書き禁止）
- **RDD遵守**（doc/input/rdd.md のスタック/制約に反しない）
- 技術スタックの既定は `doc/input/rdd.md`。このコマンドの出力（SSOT JSON）は可能な限りスタック非依存に保ち、後続（`/design-ui` / `/design-assemble`）が `doc/input/rdd.md` を参照して生成する。
- SSOTの最低限スキーマは `doc/input/design/ssot_schema.md` を参照。
- `doc/input/design/components.json` の variants 命名規約は `doc/input/design/ssot_schema.md` に従い、プロジェクト横断で揃える。
- 画像（アイコン/ロゴ/イラスト/写真など）で **CSSだけでは再現できないもの**は、可能な限りFigmaからexportして「スタック既定の置き場」に保存し、`assets.json` に対応関係を残す
- 動画/アニメ（MP4/GIF/Lottie等）も同様に **assetsとしてmanifest化**する（取得できなければ `status: failed` + `error` を必ず記録し、ユーザーに手順を依頼する）
- **複数入力のマージ規約（固定）**
  - `design_context.json.pages` は **入力した PageKey の配列**として統合する
  - `copy.json` の `copyKey` は **必ずページキーで名前空間を切る**（例: `homePage.hero.title`）
  - `assets.json` の `assetKey` も **ページ横断で一意**にする
    - 同じ `assetKey` が複数入力に現れた場合は、同一ファイル（同一内容）であることが確認できる場合のみOK
    - 内容が異なる場合は **衝突**として停止し、ユーザーにキー命名の修正を依頼する
- **tokensの整合（固定）**
  - 複数入力で tokens が矛盾する場合（例: `semantic.color.text.primary` の参照先がページで違う）は **衝突**として停止
  - 推測で片方に寄せたり、別名tokenを勝手に増やさない（必要ならユーザーと命名/設計を合意してから）
- ここで停止

### ゲート
- tokens/variantsに未定義値なし
- design_context.json に constraints/resizing が含まれる
- components.json のvariantsが「実装の分岐」に落とせる粒度になっている
- `copy.json` に未定義文言なし（参照される `copyKey` の不足0件）
- border/background/gradient/blur/blend/strokeAlign が存在する要素について、tokens と components の `styles` 参照に落ちている（取りこぼし0）
- 画像アセットが必要な箇所（ロゴ/アイコン/イラスト/写真）が「スタック既定の置き場」 と `doc/input/design/assets/assets.json` に落ちている（取りこぼし0）
  - `assets.json` に `status: "failed"` が1件でもある場合は、**必ずユーザーに失敗理由と次アクション**（Figma Export設定/権限/再提示/手元提供）を明示して停止する

### 再現性（会話コンテキストがクリアでも再現するためのルール）
- 後続のdesign系コマンドは、`doc/input/design/*` のSSOT（tokens/components/context/copy/assets）だけで再現できる状態を目標にする
- もしSSOTが不足/破損している場合は、**推測で補わない**。次のどちらかをユーザーに依頼する：
  - `FIGMA_REF`（Figma URL等）を再提示して、`/design-ssot` を再実行する
  - 不足しているSSOT（例: `copy.json` / `assets.json`）の差分をユーザーに提供してもらう

### 画像アセットの扱い（重要）
#### アセットの保存先（スタック既定）
`doc/input/rdd.md` の技術スタックに合わせて、アセット実体は以下へ保存する（SSOTのmanifestは `doc/` に残す）：
- Next.js / React / Astro: `public/design-assets/`
- SvelteKit: `static/design-assets/`
- （判定できない場合）: まず `public/` があれば `public/design-assets/`、なければ `static/design-assets/`

- **優先形式**
  - アイコン/ロゴ: SVG（可能なら単色・パス化）
  - 写真/ラスタ: WebP または PNG（透過が必要ならPNG）
  - 複雑なイラスト: SVG優先、無理ならPNG
- **命名**
  - `public/design-assets/{kind}/{name}@{scale}.{ext}` または `static/design-assets/{kind}/{name}@{scale}.{ext}` を基本
    - 例: `icons/search@1x.svg`, `images/hero@2x.webp`
  - `name` は英小文字 + `-`（kebab-case）で安定させる

### ダウンロードできない場合（ユーザーにお願いする手順）
Figma側の状態によっては、MCPが画像を取り出せないことがあります。次をユーザーに確認・依頼する：
1. **対象レイヤー/フレームを export 可能にする**
   - Figma右パネルの **Export** を追加し、形式（SVG/PNG等）と倍率（1x/2x等）を設定する
2. **権限の確認**
   - そのFigmaファイルにアクセス権があるか（閲覧のみでexportが制限されていないか）
3. **画像の代替入力**
   - どうしてもMCPで取得できない場合は、ユーザーに「SVG/PNG/WebPを手元からアップロード」または「アセットの配布方法（zip等）を提示」してもらい、`doc/input/design/assets/` に配置してもらう
