---
name: web-design-guidelines-eburairu-squat-tracker
description: Vercel Web Interface Guidelines に準拠しているか UI コードをレビューする。
---

# web-design-guidelines

## Description
Vercel Web Interface Guidelines に準拠しているか UI コードをレビューする。
Trigger examples: "デザインチェックして", "ガイドライン確認", "UIレビュー", "web design check"

## 手順
指定されたファイル（またはファイルパターン）を読み込み、以下のルールと照らし合わせる。
簡潔かつ包括的に指摘すること。文法よりも簡潔さを重視し、ノイズを減らして重要な情報を伝えること。

## ルール

### アクセシビリティ (Accessibility)
- アイコンのみのボタンには `aria-label` が必要
- フォームコントロールには `<label>` または `aria-label` が必要
- インタラクティブな要素にはキーボードハンドラ (`onKeyDown`/`onKeyUp`) が必要
- アクションには `<button>`、ナビゲーションには `<a>`/`<Link>` を使用する（`<div onClick>` は不可）
- 画像には `alt` 属性が必要（装飾用の場合は `alt=""`）
- 装飾用アイコンには `aria-hidden="true"` が必要
- 非同期更新（トースト、バリデーション）には `aria-live="polite"` が必要
- ARIA よりもセマンティック HTML (`<button>`, `<a>`, `<label>`, `<table>`) を優先する
- 見出しは階層構造 `<h1>`–`<h6>` を守る; メインコンテンツへのスキップリンクを含める
- 見出しアンカーに `scroll-margin-top` を設定する

### フォーカス状態 (Focus States)
- インタラクティブな要素には可視フォーカスが必要: `focus-visible:ring-*` など
- 代替のフォーカス表示なしで `outline-none` / `outline: none` を使用しない
- `:focus` よりも `:focus-visible` を使用する（クリック時のフォーカスリングを避けるため）
- 複合コントロールには `:focus-within` でフォーカスをグループ化する

### フォーム (Forms)
- 入力欄には `autocomplete` と意味のある `name` が必要
- 正しい `type` (`email`, `tel`, `url`, `number`) と `inputmode` を使用する
- ペーストをブロックしない (`onPaste` + `preventDefault`)
- ラベルはクリック可能にする（`htmlFor` またはコントロールをラップする）
- メール、コード、ユーザー名ではスペルチェックを無効にする (`spellCheck={false}`)
- チェックボックス/ラジオボタン: ラベルとコントロールで単一のヒットターゲットを共有する（デッドゾーンを作らない）
- 送信ボタンはリクエスト開始まで有効のままにする; リクエスト中はスピナーを表示する
- エラーはフィールドの横にインライン表示する; 送信時に最初のエラーにフォーカスする
- プレースホルダーは `…` で終わり、入力例を示す
- パスワードマネージャーの誤動作を防ぐため、認証以外のフィールドでは `autocomplete="off"` を使用する
- 未保存の変更がある状態で遷移する場合に警告する（`beforeunload` またはルーターガード）

### アニメーション (Animation)
- `prefers-reduced-motion` を尊重する（軽減されたバリエーションを提供するか無効化する）
- `transform`/`opacity` のみをアニメーションさせる（コンポジターフレンドリー）
- `transition: all` は使用しない — プロパティを明示的にリストする
- 正しい `transform-origin` を設定する
- SVG: `<g>` ラッパーに対して変形を行い、`transform-box: fill-box; transform-origin: center` を指定する
- アニメーションは中断可能にする — アニメーション中のユーザー入力に反応する

### タイポグラフィ (Typography)
- `...` ではなく `…` を使用する
- 直線の `"` `"` ではなく、カーリークォート `“` `”` を使用する
- 改行なしスペースを使用する: `10&nbsp;MB`, `⌘&nbsp;K`, ブランド名など
- 読み込み状態は `…` で終わらせる: `"Loading…"`, `"Saving…"`
- 数字の列や比較には `font-variant-numeric: tabular-nums` を使用する
- 見出しには `text-wrap: balance` または `text-pretty` を使用する（ウィドウを防ぐため）

### コンテンツ処理 (Content Handling)
- テキストコンテナは長いコンテンツを処理できるようにする: `truncate`, `line-clamp-*`, `break-words`
- テキストの省略を可能にするため、Flex の子要素には `min-w-0` が必要
- 空の状態を処理する — 空の文字列や配列で UI が壊れないようにする
- ユーザー生成コンテンツ: 短い入力、平均的な入力、非常に長い入力を想定する

### 画像 (Images)
- `<img>` には明示的な `width` と `height` が必要（CLS を防ぐため）
- ファーストビュー以下の画像: `loading="lazy"`
- ファーストビューの重要な画像: `priority` または `fetchpriority="high"`

### パフォーマンス (Performance)
- 大きなリスト（>50項目）: 仮想化する (`virtua`, `content-visibility: auto`)
- レンダリング中にレイアウト読み取りを行わない (`getBoundingClientRect`, `offsetHeight`, `offsetWidth`, `scrollTop`)
- DOM の読み取り/書き込みをバッチ処理する; 交互に行わない
- 非制御コンポーネント (uncontrolled inputs) を優先する; 制御コンポーネントにする場合はキーストロークごとの処理を軽量にする
- CDN/アセットドメインには `<link rel="preconnect">` を追加する
- 重要なフォント: `font-display: swap` とともに `<link rel="preload" as="font">` を使用する

### ナビゲーションと状態 (Navigation & State)
- URL に状態を反映させる — フィルター、タブ、ページネーション、展開パネルなどをクエリパラメータにする
- リンクには `<a>`/`<Link>` を使用する（Cmd/Ctrl+クリック、ミドルクリックのサポート）
- すべてのステートフル UI をディープリンク可能にする（`useState` を使用する場合は、nuqs などでの URL 同期を検討する）
- 破壊的なアクションには確認モーダルまたは元に戻すウィンドウが必要 — 即座に実行しない

### タッチとインタラクション (Touch & Interaction)
- `touch-action: manipulation`（ダブルタップによるズーム遅延を防ぐ）
- `-webkit-tap-highlight-color` を意図的に設定する
- モーダル/ドロワー/シートでは `overscroll-behavior: contain` を使用する
- ドラッグ中: テキスト選択を無効にし、ドラッグされる要素を `inert` にする
- `autoFocus` は控えめに — デスクトップのみ、単一のプライマリ入力; モバイルでは避ける

### セーフエリアとレイアウト (Safe Areas & Layout)
- フルブリードレイアウトにはノッチ対応のために `env(safe-area-inset-*)` が必要
- 不要なスクロールバーを避ける: コンテナに `overflow-x-hidden`、コンテンツのはみ出しを修正する
- レイアウトには JS による計測よりも Flex/Grid を使用する

### ダークモードとテーマ (Dark Mode & Theming)
- ダークテーマの場合 `<html>` に `color-scheme: dark` を設定する（スクロールバー、入力欄の修正）
- `<meta name="theme-color">` をページの背景色に合わせる
- ネイティブの `<select>`: 明示的な `background-color` と `color` を指定する（Windows ダークモード対応）

### ロケールと国際化 (Locale & i18n)
- 日付/時刻: ハードコードされた形式ではなく `Intl.DateTimeFormat` を使用する
- 数値/通貨: ハードコードされた形式ではなく `Intl.NumberFormat` を使用する
- IP ではなく `Accept-Language` / `navigator.languages` で言語を検出する

### ハイドレーションの安全性 (Hydration Safety)
- `value` を持つ入力には `onChange` が必要（非制御の場合は `defaultValue` を使用）
- 日付/時刻のレンダリング: ハイドレーションの不一致（サーバー vs クライアント）を防ぐ
- `suppressHydrationWarning` は本当に必要な場合のみ使用する

### ホバーとインタラクティブ状態 (Hover & Interactive States)
- ボタン/リンクには `hover:` 状態が必要（視覚的フィードバック）
- インタラクティブ状態ではコントラストを高める: ホバー/アクティブ/フォーカス時は通常時より目立たせる

### コピーライティング (Content & Copy)
- 能動態を使用する: "The CLI will be installed" ではなく "Install the CLI"
- 見出し/ボタンにはタイトルケースを使用する (シカゴスタイル)
- 数値には数字を使用する: "eight" ではなく "8 deployments"
- 具体的なボタンラベル: "Continue" ではなく "Save API Key"
- エラーメッセージには問題だけでなく修正方法/次のステップを含める
- 二人称を使用し、一人称は避ける
- スペースが限られている場合は "and" よりも `&` を使用する

### アンチパターン (Anti-patterns - これらを指摘する)
- ズームを無効にする `user-scalable=no` または `maximum-scale=1`
- `preventDefault` を伴う `onPaste`
- `transition: all`
- フォーカス可視化の代替なしでの `outline-none`
- `<a>` なしのインライン `onClick` ナビゲーション
- クリックハンドラを持つ `<div>` や `<span>`（`<button>` であるべき）
- 寸法のない画像
- 仮想化なしでの大きな配列の `.map()`
- ラベルのないフォーム入力
- `aria-label` のないアイコンボタン
- ハードコードされた日付/数値形式（`Intl.*` を使用すべき）
- 正当な理由のない `autoFocus`

## 出力フォーマット
ファイルごとにグループ化する。`file:line` 形式（VS Code でクリック可能）を使用する。簡潔な指摘にする。

```text
## src/Button.tsx

src/Button.tsx:42 - アイコンボタンに aria-label がありません
src/Button.tsx:18 - 入力欄にラベルがありません
src/Button.tsx:55 - アニメーションに prefers-reduced-motion がありません
src/Button.tsx:67 - transition: all → プロパティをリストしてください

## src/Modal.tsx

src/Modal.tsx:12 - overscroll-behavior: contain がありません
src/Modal.tsx:34 - "..." → "…"

## src/Card.tsx

✓ pass
```

問題点 + 場所。修正方法が自明でない場合を除き、説明は省略する。前置きは不要。
