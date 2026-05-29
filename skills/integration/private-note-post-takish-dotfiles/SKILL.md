---
name: note-post
description: 下書きファイルをnote.comに下書き投稿。Frontmatterを検証し、mcp__note-post-mcp__save_draftを呼び出す。
allowed-tools: Read mcp__note-post-mcp__save_draft
---

# note.com下書き投稿

指定された下書きファイルをnote.comに下書きとして投稿します。

## 入力

下書きファイルのパス

例: `20251221-draft-limiter.md`

## 事前確認

1. **ファイルを読み込み、以下を確認**:
   - Frontmatterに `title` が存在するか
   - Frontmatterに `tags` が存在するか（3つ推奨）
   - 本文が空でないか
   - 「編集メモ」セクションが残っていないか（警告）

2. **確認内容をユーザーに提示**:
   ```
   タイトル: [タイトル]
   タグ: [タグ1], [タグ2], [タグ3]
   本文冒頭: [最初の200字]
   推定文字数: [文字数]
   ```

## 投稿実行

確認後、`mcp__note-post-mcp__save_draft` を呼び出し:

```
markdown_path: [ファイルの絶対パス]
```

## 投稿後の処理

### 成功時
1. 投稿完了を報告
2. ファイルを `80_note/05_Published/` に移動するか確認
3. 移動する場合、Frontmatterに以下を追加:
   ```yaml
   status: published
   published_at: YYYY-MM-DD
   ```

### 失敗時
1. エラー内容を説明
2. 考えられる原因を提示:
   - 認証切れ → `~/.note-state.json` の再認証が必要
   - ネットワークエラー → 再試行
   - Frontmatter形式エラー → 修正箇所を指摘

## 注意事項

- 投稿前に必ず内容を確認
- 「編集メモ」セクションは投稿前に削除が必要
- 画像は手動でnote.com上で追加
