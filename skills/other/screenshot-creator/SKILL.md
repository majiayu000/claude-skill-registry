---
name: screenshot-creator
description: >
  App Store / Google Play 用のプロモーションスクリーンショットを Pencil (.pen) で生成する
  シングルエージェントスキル。creative-director → copy-writer → screenshot-designer →
  spec-validator → quality-reviewer の役割を1エージェントが順番に担当し、
  Pencil MCP でデザインを構築する。エージェントチーム不使用（低コスト）。
  Use when: App Store スクリーンショットを作りたい、プロモーション画像を作成したい、
  スクショのデザインをしたい。
  Triggers: "スクリーンショット作成", "App Store 画像", "プロモーションスクショ",
  "screenshot creator", "スクショ作って", "App Store 素材"
---

# screenshot-creator スキル（シングルエージェント版）

**エージェントチームは使わない。** 以下の役割を1エージェントが順番に担当する:
`creative-director` → `copy-writer` → `screenshot-designer` → `spec-validator` → `quality-reviewer`

---

## ⚠️ 既知の落とし穴（必読 — 毎回ハマる）

| 落とし穴 | 症状 | 正しい対処 |
|---------|------|-----------|
| **テキストオーバーフロー** | ヘッドラインがフレーム左右にはみ出す | 全テキストノードに `width: "fill_container"` を必ず追加 |
| **fontSize 32 は大きすぎる** | 14文字の日本語ヘッドラインが内幅342pxに入らない | headline fontSize は **最大 22px**。32は絶対使わない |
| **親フレームに layout: "vertical" 必須** | CaptionAreaとMockupAreaが縦積みにならず横並びになる | 親フレーム（SS01_Hero等）に必ず `layout: "vertical"` を設定 |
| **`get_screenshot` はディスク保存しない** | base64をMCPレスポンスに返すだけ。ファイルは作られない | Step 7 ではシミュレータ直接撮影のファイルをそのまま使う |
| **Dynamic Island（黒いピル）が写り込む** | iPhone 14以降のシミュレータに黒いカプセルが表示される | **iPhone SE 3rd gen** シミュレータを使う（DI/ノッチなし）。または Python でトップをクロップ |
| **Pencil が画像キャッシュを捨てない** | 同じパスのファイルを上書きしても Pencil は古い画像を表示し続ける | 画像を差し替えるときは **必ず新しいファイル名** を使う |
| **PhoneMockup 内で x/y が効かない** | Pencilが「flexbox内でx/y無視」と警告する | 子ノードでのオーバーレイ配置は不可。画像自体をクロップして対処する |

---

## Step 0: シミュレータ準備（スクショ撮影前）

**Dynamic Island を含むスクショはNG。** iPhone SE 3rd gen を使う。

```bash
# iPhone SE 3rd gen 起動（Dynamic Island なし・ノッチなし）
xcrun simctl boot CBA51D41-D404-4843-AA18-738C5068FFE4

# アプリインストール（build済み .app のパス）
xcrun simctl install CBA51D41-D404-4843-AA18-738C5068FFE4 /path/to/App.app

# スクショ撮影
xcrun simctl io CBA51D41-D404-4843-AA18-738C5068FFE4 screenshot /path/to/screen_home.png
```

**万が一 iPhone 14+ のスクショを使う場合**: Dynamic Island（上部185px）を Python でクロップ:

```bash
python3 -c "
from PIL import Image
for src, dst in [('/tmp/screen_home.png','/tmp/screen_home_clean.png'),('/tmp/screen_history.png','/tmp/screen_history_clean.png')]:
    img = Image.open(src)
    img.crop((0, 185, img.width, img.height)).save(dst)
    print(dst, img.crop((0,185,img.width,img.height)).size)
"
```

⚠️ クロップ後は**必ず新しいファイル名**で保存すること（Pencilが同一パスを再読みしないため）。

---

## Step 1: ヒアリング

以下を確認する:

| 項目 | デフォルト |
|------|----------|
| アプリ名 | - |
| カテゴリ | ライフスタイル / 生産性 / ヘルス等 |
| 主要機能 | 3〜5個 |
| ターゲットユーザー | - |
| ブランドカラー | Step 2 のスタイルガイドから決定 |
| トーン | エモーショナル / プロフェッショナル等 |
| スクリーンショット枚数 | 3〜6枚（推奨） |
| 実スクリーンショット | アプリキャプチャの絶対パス（Step 0 で撮影済み） |
| .pen ファイルパス | 新規作成なら省略 |
| デバイスサイズ | iPhone 6.9"（390×844pt） |

---

## Step 2: スタイルガイド取得（Asian / Japanese テーマ）

`mcp__pencil__get_style_guide` を呼び出す。タグは **必ず以下を指定**:

```
tags: ["japanese", "zen", "wellness", "minimal", "calm"]
```

スタイルガイドが返ってきたら、カラーパレット・フォント・背景色をメモする。
指定がない場合は CaptionArea ライトパターン（`#F2F7F5` / `#1A1A1A` / `#6B7B75`）を使う。

---

## Step 3: コピー作成（copy-writer 役割）

各スクリーンのヘッドライン + サブテキスト2行を決定する。

### コピー原則

| ルール | 内容 |
|--------|------|
| ヘッドライン | 機能説明ではなく「ユーザーが得られるベネフィット」 |
| 文字数 | ヘッドライン **10〜14文字以内**、サブテキスト 1行 12文字以内 |
| 句読点 | ヘッドラインに「、」「。」は使わない |
| 行数 | ヘッドライン1行 + サブテキスト2行 = 計3行 |
| 言語 | 日本語優先（必要なら英語） |

> **14文字を超えるヘッドラインは fontSize 22px でも内幅342pxに収まらない。** 必ず14文字以内に収める。

### ヘッドラインパターン（参考）

| パターン | 例 |
|---------|-----|
| ベネフィット型 | 「悩みを書くだけ」 |
| 疑問型 | 「もっと早く使えばよかった」 |
| 数字型 | 「3,000人が変わった」 |
| 感情型 | 「もう迷わない」 |

---

## Step 4: .pen ファイル作成とデザイン構築（screenshot-designer 役割）

### 4-1. ドキュメント準備

```javascript
// 新規ファイルが必要な場合
mcp__pencil__open_document("new")
// または既存パスを開く
mcp__pencil__open_document("/path/to/file.pen")
```

### 4-2. フレーム作成（iPhone 6.9" = 390×844pt）

**親フレームに `layout: "vertical"` は必須。** これがないと CaptionArea と MockupArea が横並びになる。

```javascript
// 1枚目
frame1=I("document", {type: "frame", name: "SS01_Hero", layout: "vertical", width: 390, height: 844, fill: "#F2F7F5"})
// 2枚目（右に配置）
frame2=I("document", {type: "frame", name: "SS02_Feature1", layout: "vertical", x: 430, width: 390, height: 844, fill: "#F2F7F5"})
// 3枚目
frame3=I("document", {type: "frame", name: "SS03_Feature2", layout: "vertical", x: 860, width: 390, height: 844, fill: "#F2F7F5"})
```

### 4-3. 各フレームにコンテンツを構築

**構造（必須）:**

```
フレーム（390×844, layout: vertical） ← layout: "vertical" 必須
├── CaptionArea（height: 160, layout: vertical, alignItems: center, justifyContent: center）
│   ├── headline（fontSize: 22, fontWeight: 700, textAlign: center, width: fill_container）← 22px・fill_container 必須
│   ├── sub1（fontSize: 16, textAlign: center, width: fill_container）
│   └── sub2（fontSize: 16, textAlign: center, width: fill_container）
└── MockupArea（height: 684, alignItems: center, justifyContent: center）
    └── PhoneMockup（width: 320, height: 640, cornerRadius: 44）
        └── image fill（実スクリーンショット必須 — AI生成禁止）
```

**CaptionArea ライトパターン（デフォルト）:**

```javascript
captionArea=I(frame1, {type: "frame", layout: "vertical", alignItems: "center",
  justifyContent: "center", gap: 6, height: 160, padding: [40, 24, 12, 24], fill: "#F2F7F5"})

// ⚠️ width: "fill_container" は必須。これがないとテキストがフレーム外にはみ出す
headline=I(captionArea, {type: "text", content: "ヘッドライン",
  fontSize: 22, fontWeight: "700", textAlign: "center", fill: "#1A1A1A", width: "fill_container"})
sub1=I(captionArea, {type: "text", content: "サブテキスト1行目",
  fontSize: 16, textAlign: "center", fill: "#6B7B75", width: "fill_container"})
sub2=I(captionArea, {type: "text", content: "サブテキスト2行目",
  fontSize: 16, textAlign: "center", fill: "#6B7B75", width: "fill_container"})
```

**MockupArea + PhoneMockup:**

```javascript
// alignItems + justifyContent で PhoneMockup を中央配置
mockupArea=I(frame1, {type: "frame", width: "fill_container", height: 684,
  alignItems: "center", justifyContent: "center", padding: [0, 35, 20, 35]})

// ⚠️ 実スクリーンショット必須（AI生成禁止）
// Step 0 で撮影した Dynamic Island なしのスクショを使う
phoneMockup=I(mockupArea, {type: "frame", width: 320, height: 640,
  fill: {type: "image", url: "/absolute/path/to/screenshot_clean.png", mode: "fill"},
  cornerRadius: [44, 44, 44, 44]})
```

### 4-4. 画像確認

各フレーム構築後に `mcp__pencil__get_screenshot` で目視確認する。

**チェックリスト:**
- ヘッドラインがフレーム内に収まっているか（左右にはみ出ていないか）
- CaptionArea → MockupArea の順で縦積みになっているか（横並びはNG）
- PhoneMockup内のアプリ画面に Dynamic Island（黒いピル）が映っていないか
- PhoneMockup の角が丸くクリップされているか

### 4-5. 禁止事項

| 禁止 | 理由 |
|------|------|
| **AI生成画像（`G(..., "ai", ...)`）を使う** | **絶対禁止。App Store に AI 生成スクショは出さない** |
| **`width: "fill_container"` を省略する** | テキストがフレーム外にはみ出す。全テキストノードに必須 |
| **headline fontSize > 22** | 14文字の日本語が内幅342pxに収まらない |
| **親フレームの `layout: "vertical"` を省略する** | CaptionAreaとMockupAreaが横並びになる |
| CaptionArea に装飾フレーム（アクセントバー等） | モックアップ上端に線が出る |
| `\n` 改行 | 縦長になる。テキストノードを分割すること |
| テキストノード4つ以上 | 読まれない |
| PhoneMockupのはみ出し | MockupArea 内に完全に収めること |
| Dynamic Island が映ったままアップロード | App Storeで見栄えが悪い。Step 0 で必ず除去 |

---

## Step 5: 技術仕様バリデーション（spec-validator 役割）

`mcp__pencil__batch_get` と `mcp__pencil__snapshot_layout` で以下を数値検証:

| # | 検証項目 | 基準 | 判定 |
|---|---------|------|------|
| 1 | フレームサイズ | width=390, height=844 | 完全一致のみ PASS |
| 2 | 親フレームのlayout | layout="vertical" | PASS |
| 3 | PhoneMockup 面積比 | ≥ 50%（320×640=204800 / 329160 = 62.2%） | PASS |
| 4 | 画像 fill | fill.type="image", url 有効 | PASS |
| 5 | テキストノードの width | width="fill_container" | PASS |
| 6 | テキストサイズ | headline ≤ 22pt, sub ≥ 14pt | PASS |
| 7 | コントラスト比 | ≥ 4.5:1（通常テキスト） | PASS |
| 8 | テキストノード数 | CaptionArea に ≤ 3 | PASS |
| 9 | 中央揃え | alignItems: center, textAlign: center | PASS |
| 10 | Dynamic Island | PhoneMockup 内に黒いピル形状なし | PASS |

FAIL 項目は `U("{nodeId}", {property: value})` で即修正する。

---

## Step 6: 品質レビュー（quality-reviewer 役割）

`mcp__pencil__get_screenshot` で全フレームを確認し、10点満点でスコアリング:

| カテゴリ | 基準 |
|---------|------|
| ビジュアル品質 | コントラスト、余白、フォント |
| コピー品質 | ベネフィット訴求、14文字以内 |
| 構成 | 最初の3枚が重要機能を強調 |
| 統一感 | 全スクリーンでスタイル統一 |
| クリーンさ | Dynamic Island・ノッチ・余計なUI要素なし |

**合格基準: 7/10 以上。** 7未満なら問題箇所を特定して修正する。

---

## Step 7: PNG エクスポートとアップロード

**`get_screenshot` はディスクに書かない。** base64 をMCPレスポンスで返すだけ。

**正しいフロー:**

1. Step 0 で撮影したシミュレータスクショ（例: `/path/to/screen_home_clean.png`）を直接使う
2. `sips -z 2796 1290` で App Store 必須サイズ（1290×2796）にリサイズ:

```bash
# ⚠️ sips の引数順は height width（幅が先ではない）
cp /path/to/screen_home_clean.png /path/to/screen1.png
cp /path/to/screen_history_clean.png /path/to/screen2.png
cp /path/to/screen_paywall_clean.png /path/to/screen3.png

sips -z 2796 1290 /path/to/screen1.png
sips -z 2796 1290 /path/to/screen2.png
sips -z 2796 1290 /path/to/screen3.png
```

3. `asc screenshots upload` でアップロード（version-localization ID は `asc-id-resolver` スキルで取得）:

```bash
asc screenshots upload --version-localization <LOC_ID> --path /path/to/screen1.png --device-type APP_IPHONE_67
asc screenshots upload --version-localization <LOC_ID> --path /path/to/screen2.png --device-type APP_IPHONE_67
asc screenshots upload --version-localization <LOC_ID> --path /path/to/screen3.png --device-type APP_IPHONE_67
```

4. 報告フォーマット:

```
## スクリーンショット完成

.pen ファイル: {filePath}

| スクリーン | フレーム名 | フレームID | PNG |
|-----------|----------|---------|-----|
| SS01 | SS01_Hero | {id} | screen1.png |
| SS02 | SS02_Feature1 | {id} | screen2.png |
| SS03 | SS03_Feature2 | {id} | screen3.png |

spec-validator: 全10項目 PASS
quality-reviewer: {X}/10
ASC upload: 完了 ✅
```

---

## 出力成果物

- Pencil `.pen` ファイル（全スクリーンショット）
- 各フレームのノードID一覧
- コピーテキスト一覧（日本語）
- 技術仕様バリデーション結果（10項目 PASS/FAIL）
- 品質スコア（10点満点）

---

## App Store スクリーンショット仕様

詳細は [references/app-store-screenshot-specs.md](references/app-store-screenshot-specs.md) を参照。

---

## PhoneMockup レイアウトガイドライン

### アスペクト比の一致（重要）

PhoneMockup のアスペクト比は **実際のスクリーンショット画像の比率と一致** させること。

| 項目 | 値 |
|------|-----|
| 推奨 PhoneMockup サイズ | **320 × 640**（比率 0.50） |
| iPhone 標準比率 | 約 0.46（390/844） |
| シミュレータスクショ比率 | 約 0.50（864/1723） |

### CaptionArea とのバランス

| エリア | 推奨高さ |
|--------|---------|
| CaptionArea | 160pt |
| MockupArea | 684pt |

> CaptionArea を小さく、PhoneMockup を大きくして、アプリ画面をできるだけ多く見せる。

### 推奨シミュレータ（Dynamic Island なし）

| デバイス | UDID（このMac） | 備考 |
|---------|--------------|------|
| iPhone SE 3rd gen | CBA51D41-D404-4843-AA18-738C5068FFE4 | ノッチなし・DI なし・最もクリーン |
