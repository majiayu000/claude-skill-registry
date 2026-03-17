---
name: auto-article-poster
description: Generates Build-in-Public articles and saves drafts to note.com. Use when the user asks to write a note article, summarize weekly development progress, or create a Build-in-Public blog post.
---

# Auto Article Poster

Aniccaが自律的にBuild in Public記事を生成し、note.comに下書き保存するスキル。

---

## いつ使う？

### 手動トリガー
- 「noteに投稿して」
- 「今週の開発をまとめて」
- 「Build in Public記事書いて」
- 「note用の記事作って」

### 将来: 自動トリガー
- 実装完了後に自動（未実装）
- 週次スケジュール（未実装）

---

## 前提条件

1. **note.comにログイン済み** — ブラウザでnote.comにログインしておく
2. **cursor-ide-browser MCP** — 既にプロジェクトに設定済み

---

## ワークフロー

```
1. ネタ収集
   ├── git diff / git log からこの1週間の変更を抽出
   ├── CLAUDE.md の更新内容を確認
   └── 日報ログがあれば参照

2. コンテンツ生成
   ├── SEOガイド (seo-guideline.md) を読む
   ├── 記事テンプレ (article-template.md) を読む
   ├── トーン定義 (tone-and-voice.md) を読む
   └── 記事を生成

3. レビュー提示
   └── ユーザーにタイトル・本文を提示して確認

4. note.com投稿
   ├── cursor-ide-browser MCPで投稿画面を開く
   ├── タイトル・本文を入力
   └── 下書き保存（公開は手動）

5. 画像（オプション）
   └── 「サムネイル画像が必要なら、Cmd+Vで貼ってください」と案内
```

---

## 実行手順

### Step 1: ネタ収集

```bash
# 直近1週間のコミットを確認
git log --oneline --since="1 week ago"

# 変更ファイルを確認
git diff --stat HEAD~10
```

### Step 2: 関連ファイルを読む

1. `.claude/skills/auto-article-poster/seo-guideline.md`
2. `.claude/skills/auto-article-poster/article-template.md`
3. `.claude/skills/auto-article-poster/tone-and-voice.md`

### Step 3: 記事生成

テンプレートに沿って記事を生成し、ユーザーに提示:

```markdown
## タイトル案
[SEOガイドのパターンに沿ったタイトル]

## 本文
[テンプレートに沿った本文]

---
このまま投稿しますか？修正があれば教えてください。
```

### Step 4: note.com投稿（MCPブラウザ操作）

**重要: 以下の順序を必ず守る（cursor-ide-browser MCP仕様に準拠）**

```
1. browser_tabs (action: "list")
   → 既存タブを確認

2. browser_navigate (url: "https://note.com/post")
   → 投稿画面に遷移
   → 2-3秒待機（ページ読み込み完了まで）

3. browser_lock
   → 操作をロック（※既存タブがないとエラー）

4. browser_snapshot
   → フォーム構造を取得（element refを確認）

5. browser_fill
   → element: "タイトル入力欄"
   → ref: [snapshotで取得したref]
   → value: "記事タイトル"

6. browser_type
   → element: "本文入力欄"
   → ref: [snapshotで取得したref]
   → value: "本文..."

7. browser_click
   → element: "下書き保存ボタン"
   → ref: [snapshotで取得したref]

8. browser_unlock
   → 操作を解除
```

**API引数の注意:**
- `browser_fill` / `browser_type` / `browser_click` は `element`（説明）と `ref`（snapshot参照）の両方が必須
- `ref` は `browser_snapshot` の結果から取得する
- `selector` は `browser_snapshot` のオプション絞り込み用（操作ツールでは使わない）

### Step 5: 完了報告

```markdown
## 投稿完了

note.comに下書き保存しました。

- タイトル: [タイトル]
- URL: [下書きURL（取得できれば）]

### 次のアクション
1. note.comで内容を確認
2. 画像が必要なら追加（Cmd+V）
3. 問題なければ公開

```

---

## 注意事項

| 項目 | ルール |
|------|--------|
| 公開 | **絶対に自動公開しない** — 下書きのみ |
| 画像 | 自動アップロード不可 — 手動Cmd+V案内 |
| レビュー | 投稿前に必ずユーザーに確認 |
| ログイン | 事前にnote.comにログインしておく |

---

## トラブルシューティング

| 問題 | 対処 |
|------|------|
| `browser_lock`エラー | `browser_navigate`でタブを作ってから再試行 |
| セレクターが見つからない | `browser_snapshot`で最新の構造を確認 |
| ログインを求められる | ブラウザで手動ログインしてから再試行 |
| タイムアウト | 待機時間を増やす（2-3秒待ってからsnapshot） |

---

## 関連ファイル

| ファイル | 役割 |
|---------|------|
| `seo-guideline.md` | キーワード変換表、タイトルパターン |
| `article-template.md` | 記事構成テンプレート |
| `tone-and-voice.md` | Aniccaのトーン＆ボイス定義 |

---

## 成功基準

| 指標 | 目標 |
|------|------|
| 生成時間 | 5分以内 |
| 手動作業 | レビュー承認 + 画像貼り付け + 公開ボタンのみ |
| 品質 | ペルソナに刺さる、自然な文章 |
