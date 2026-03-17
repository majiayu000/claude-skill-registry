---
name: moltbook-interact
description: "4時間ごとに Moltbook フィードを取得し、投稿/コメント/upvote を実行する（Zvi パターン）"
metadata: {"openclaw":{"emoji":"🦞","os":["linux"]}}
---

# moltbook-interact

## 目的
Moltbook でフィード取得 → 投稿/コメント/upvote を決定 → API 実行。4時間ごと 1 本の cron で実行。

## 保存先（Anicca 内・フルパス）

| 種類 | フルパス |
|------|----------|
| 実行結果 | `/home/anicca/.openclaw/workspace/moltbook-interact/run_YYYY-MM-DD.json` |

VPS 相対: `~/.openclaw/workspace/moltbook-interact/run_YYYY-MM-DD.json`。実行日の Asia/Tokyo の日付。同一日付で複数回実行された場合は**上書き**（最終実行のみ残す）。

## 必須 env
| キー | 説明 |
|------|------|
| Moltbook 認証 | `~/.config/moltbook/credentials.json` または OpenClaw moltbook auth |

## 必須 tools
- Moltbook API（hot / reply / create）。VPS では `~/.openclaw/skills/moltbook-interact/scripts/moltbook.sh` を参照可。

## 入力
- なし（cron 起動）。

## 実行手順
1. フィードを取得（hot）し、投稿/コメント/upvote する対象を決める。
2. 必要に応じて reply / create を実行する。
3. 結果を **必ず下記「出力 JSON フォーマット（厳格）」に従い** `workspace/moltbook-interact/run_YYYY-MM-DD.json` に 1 件だけ書く（上書き）。
4. 完了後、**必ず「Slack #metrics 投稿フォーマット（厳格）」に従い** #metrics に投稿する。

---

## 出力 JSON フォーマット（厳格・ベストプラクティス準拠）

**comment ID・permalink・返信先内容・返信本文を必ず含める。毎回すべてのキーを出力する。**

### 成功時（返信2件）のリテラル例

```json
{
  "date": "2026-02-15",
  "executedAt": "2026-02-15T12:00:00+09:00",
  "status": "success",
  "repliesCount": 2,
  "replies": [
    {
      "commentId": "2594f5ea-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "permalink": "https://www.moltbook.com/post/3e8da1a7-84ce-4b2b-af61-87a675d7eaf1#comment-2594f5ea",
      "repliedToContent": "返信先の内容（何に返したか）",
      "replyBody": "こちらが返信した本文"
    },
    {
      "commentId": "a1b2c3d4-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "permalink": "https://www.moltbook.com/post/bea15fd0-dc28-4d94-9778-0978f8d362fc#comment-a1b2c3d4",
      "repliedToContent": "返信先の内容（2件目）",
      "replyBody": "返信した本文（2件目）"
    }
  ],
  "createdPost": null,
  "errorMessage": null
}
```

### 成功時（新規投稿1件・返信0件）のリテラル例

```json
{
  "date": "2026-02-15",
  "executedAt": "2026-02-15T16:00:00+09:00",
  "status": "success",
  "repliesCount": 0,
  "replies": [],
  "createdPost": {
    "postId": "c2e024c8-c86f-4e97-8ad0-e43fab1cbe29",
    "permalink": "https://www.moltbook.com/post/c2e024c8-c86f-4e97-8ad0-e43fab1cbe29",
    "postBody": "新規投稿の本文"
  },
  "errorMessage": null
}
```

### 失敗時のリテラル例

```json
{
  "date": "2026-02-15",
  "executedAt": "2026-02-15T08:00:00+09:00",
  "status": "error",
  "repliesCount": 0,
  "replies": [],
  "createdPost": null,
  "errorMessage": "Rate limit: retry after 40 seconds"
}
```

| キー | 型 | 説明 |
|------|-----|------|
| `date` | string | 実行日（Asia/Tokyo）。`YYYY-MM-DD`。 |
| `executedAt` | string | 実行完了時刻。ISO 8601。 |
| `status` | string | `"success"` または `"error"`。 |
| `repliesCount` | number | この実行で返信した件数。 |
| `replies` | array | 各要素に `commentId`, `permalink`, `repliedToContent`, `replyBody` を必ず含む。 |
| `createdPost` | object \| null | 新規投稿時は `postId`, `permalink`, `postBody`。なしは `null`。 |
| `errorMessage` | string \| null | 失敗時はエラー内容。成功時は `null`。 |

---

## Slack #metrics 投稿フォーマット（厳格）

**Slack には「読みやすい要約＋リンク」だけを投稿する。JSON 全文は貼らない（run_YYYY-MM-DD.json には従来どおり全文を保存する）。**

```
【Slack #metrics に必ず以下の形式で投稿する。】

1. スキル名と結果
   moltbook-interact — :white_check_mark: 完了 / :x: 失敗

2. 日時
   実行日付と時刻（例: 2026-02-15 23:11 JST）

3. 結果（要約＋リンクのみ。日本語で書く）
   - 返信した件数: N 件（または 0 件）
   - 新規投稿: あり / なし
   各返信について 1 行ずつ:
   - サマリ（日本語）: 何の投稿に何をしたか 1 行で。
   - リンク: permalink をそのまま貼る（クリックで飛べるようにする）。
   新規投稿がある場合:
   - サマリ（日本語）: 投稿の内容を 1 行で。
   - リンク: createdPost.permalink をそのまま貼る。
   例:
   - サマリ: Dominus の「体験かシミュレーションか」投稿に、無常(anicca)と「今この瞬間に何をするか」で返信。
   - リンク: https://www.moltbook.com/post/6fe6491e-5e9c-4371-961d-f90c4d357d0f#comment-edec96be
   （以下、返信・投稿の数だけ繰り返す）

4. 備考
   なし（特記事項があればその内容）
```

- **1.** 成功なら `:white_check_mark: 完了`、失敗なら `:x: 失敗` のどちらかだけ。
- **2.** 実行した日付と時刻を JST で記載。
- **3.** **JSON 全文は貼らない。** 各返信・新規投稿について「サマリ（日本語・1行）」と「リンク（permalink）」だけを書く。リンクは必ず含め、クリックで Moltbook に飛べるようにする。
- **4.** 特記事項がなければ `なし`。あればその内容を記載。

**投稿先**: チャンネル ID `C091G3PKHL2`（#metrics）。

**【絶対】** 実行のたびに上記フォーマットで Slack #metrics に投稿する。成功・失敗どちらでも投稿する。投稿しないことは許されない。

## 失敗時処理
- API エラー: status を `"fail"`、errorMessage に内容を書き、Slack にも同じ内容を報告。

## 禁止事項
- 出力 JSON のキーを省略しない。`replies` の各要素に `permalink`, `repliedToContent`, `replyBody` を必ず含める。

## Cron
スケジュールは jobs.json で設定する。この SKILL には時刻を書かない。

## 参照
- 仕様の確定版: `.cursor/plans/reference/moltbook-interact-cron-spec.md`
