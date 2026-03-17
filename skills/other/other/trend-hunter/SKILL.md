---
name: trend-hunter
description: "X/TikTok/Reddit からトレンドを収集し、VPS の workspace(trends/hooks) に保存する"
metadata: {"openclaw":{"emoji":"🕵️","os":["linux"]}}
---

# trend-hunter

## 実行方法（重要）

**このスキルに「起動するスクリプト」や「実行可能ファイル」はない。** 実行するとは、この SKILL.md 全文を読み、以下の手順を **あなたが** `run_terminal_cmd`・ファイル書き・API 呼び出しで行うこと。  
- X 検索: `run_terminal_cmd` で `cd ~/.openclaw/skills/x-research && bun run x-search.ts search "..." --limit 20` を実行。  
- TikTok: Apify API を curl 等で呼ぶ。  
- Reddit: `~/.openclaw/skills/reddit-cli` の手順に従い検索。  
- 結果は **slot 別** に書く。`~/.openclaw/workspace/trends/{9am|9pm}/YYYY-MM-DD.json` と `~/.openclaw/workspace/hooks/{9am|9pm}/YYYY-MM-DD.json`（マージしない）。  
「スクリプトやプロセスが見つかりません」と返答せず、上記のとおり実行すること。

---

## 目的
バズっている話題を **X / TikTok / Reddit の 3 スキルだけ**（x-research, tiktok-scraper, reddit-cli）から収集し、トレンドを **slot 別** `trends/9am/YYYY-MM-DD.json` または `trends/9pm/YYYY-MM-DD.json` に書き、投稿用 1 本を **slot 別** `hooks/9am/YYYY-MM-DD.json` または `hooks/9pm/YYYY-MM-DD.json` に書く。保存先は VPS ローカル（Anicca 内）のみ。**1 日 1 ファイルにマージせず、9am と 9pm で別ファイルにする。**

注: 相対パスの実行（例: `./run_trend_hunter.sh`）が必要になった場合は、`workdir: "{baseDir}"`（または `cd {baseDir}`）でスキルディレクトリを起点にすること。

## 保存先（Anicca 内・slot 別・フルパス）

| 種類 | フルパス（slot は 9am または 9pm） |
|------|-------------------------------------|
| トレンド狩り結果のみ | `/home/anicca/.openclaw/workspace/trends/{slot}/YYYY-MM-DD.json` |
| 投稿用 1 本 | `/home/anicca/.openclaw/workspace/hooks/{slot}/YYYY-MM-DD.json` |

VPS 相対: `~/.openclaw/workspace/trends/9am/`, `~/.openclaw/workspace/trends/9pm/`, `~/.openclaw/workspace/hooks/9am/`, `~/.openclaw/workspace/hooks/9pm/`。**x-poster / tiktok-poster は `hooks/9am/` または `hooks/9pm/` の YYYY-MM-DD.json を読む。**

## Slack 報告
**【絶対】** 実行結果を Slack #metrics（チャンネル ID: `C091G3PKHL2`）に投稿する。成功でも失敗でも必ず投稿する。要約禁止。**以下をそのままこの形式で投稿する。**

```
【Slack #metrics に必ず以下の形式で投稿する。要約禁止。】

1. スキル名と結果
   trend-hunter ({slot}, {date}) — :white_check_mark: 完了 / :x: 失敗

2. 日時
   実行日付と時刻（例: 2026-02-15 05:00 JST）

3. ソース結果（そのまま）
   X / TikTok / Reddit の取得件数・スキップ理由を省略せず書く。

4. 保存ファイルの内容（全文）
   - trends/{slot}/{date}.json の内容を整形してそのまま貼る（全トレンドの hook, source, trendContext, pattern, analysis）。
   - hooks/{slot}/{date}.json の内容を整形してそのまま貼る（X の postText、TikTok の caption, imageUrl, imagePrompt, reasons）。省略しない。

5. 備考（あれば）
   Apify/Reddit エラー等
```

---

## フロー（trend-hunter → x-poster / tiktok-poster）

**trend-hunter は 1 日 2 回、5am と 5pm に動く。cron の payload で渡される slot と date をそのまま使う。時刻を推測したり `date` を実行したりしない。**

| cron | 渡される slot | やること |
|------|----------------|----------|
| 5am | 9am | その日の 9am 用を用意。直近 9pm 投稿のメトリクス取得 → 学習 JSON → トレンド検索 → trends 保存 → 1 本選んで hooks に slot 9am で書く。 |
| 5pm | 9pm | その日の 9pm 用を用意。直近 9am 投稿のメトリクス取得 → 学習 JSON → トレンド検索 → trends 保存 → 1 本選んで hooks に slot 9pm で書く。 |

### trend-hunter の実行手順（毎回この順）

1. **payload の slot と date をそのまま使う**（推測・date 実行禁止）。
2. **直近の該当投稿のメトリクス取得・学習**（下記「メトリクス取得：X と TikTok」の API を使う）。結果を **`workspace/trend-hunter/metrics_YYYY-MM-DD.json`** に書く。
3. **トレンド検索**（x-research, tiktok-scraper, reddit-cli の 3 スキル）。
4. **trends/{slot}/YYYY-MM-DD.json** に発見したトレンドのみ保存（slot は 9am または 9pm。投稿文はまだ作らない）。
5. 候補から **payload の slot 用に 1 本を選び**、**hooks/{slot}/YYYY-MM-DD.json** に書く（その slot の 1 ファイルだけ。マージしない）。

### x-poster / tiktok-poster の実行（cron 9:00 と 21:00）

- **9:00 の cron（morning）:** **workspace/hooks/9am/YYYY-MM-DD.json** を読む。X 用 `postText` / TikTok 用 `caption` と `imageUrl`（空なら tiktok-poster が imagePrompt で FAL 生成）をその場で X と TikTok に投稿する。
- **21:00 の cron（evening）:** **workspace/hooks/9pm/YYYY-MM-DD.json** を読む。同上。

---

## 必須 env（すべて VPS の `~/.openclaw/.env` に置く）

| キー | 説明 |
|------|------|
| `X_BEARER_TOKEN` | X 検索・X メトリクス（x-research と Blotato 解決後の X API v2） |
| `BLOTATO_API_KEY` | メトリクス用（Blotato GET /v2/posts/{postSubmissionId}） |
| `APIFY_API_TOKEN` | TikTok（tiktok-scraper スキル・Apify） |
| `REDDIT_SESSION` | reddit-cli スキル用（Cookie 認証。`~/.openclaw/.env` に設定。REDDAPI_API_KEY は不要） |
| （ops/heartbeat 等と連携する場合のみ必要に応じて） |  |

## 実行順序（必ずこの順）

1. **payload の slot と date をそのまま使う。**
2. **直近投稿のメトリクス取得・学習**（下記「メトリクス取得：X と TikTok」の API を使う）。結果を **workspace/trend-hunter/metrics_YYYY-MM-DD.json** に書く。
3. トレンド検索（x-research, tiktok-scraper, reddit-cli の 3 スキル）。
4. トレンドを **trends/{slot}/YYYY-MM-DD.json** に保存（slot は 9am または 9pm。出力形式その 1）。
5. 候補から **payload の slot 用に 1 本を選び**、**hooks/{slot}/YYYY-MM-DD.json** にその slot だけ保存（出力形式その 2。マージしない）。

## メトリクス取得：X と TikTok（一文ずつ）

**X:** Blotato の `GET https://backend.blotato.com/v2/posts/{postSubmissionId}`（ヘッダ `blotato-api-key`）で tweet ID を取得し、その ID で X API v2 の `GET https://api.x.com/2/tweets?ids={tweetId}&tweet.fields=public_metrics,created_at`（ヘッダ `Authorization: Bearer {X_BEARER_TOKEN}`）を叩き、`data[0].public_metrics` の impression_count / like_count / retweet_count / reply_count を使う。

**TikTok:** Blotato の `GET https://backend.blotato.com/v2/posts/{postSubmissionId}` のレスポンスに TikTok の再生数・いいね等があればそれを使い、なければ「TikTok: 未取得」とだけ書く。

## メトリクス・学習の出力先

| 種類 | フルパス |
|------|----------|
| メトリクス＋学習メモ | `/home/anicca/.openclaw/workspace/trend-hunter/metrics_YYYY-MM-DD.json` |

VPS 相対: `~/.openclaw/workspace/trend-hunter/metrics_YYYY-MM-DD.json`。中身は「どの投稿（postSubmissionId/slot）・いつ・数値・学習メモ」を自由形式でよい。

## 必須スキル（X / TikTok / Reddit の 3 つのみ）

| ソース | スキル（VPS 上のディレクトリ名） | コマンド例 |
|--------|----------------------------------|-----------|
| X | x-research | `cd ~/.openclaw/skills/x-research && bun run x-search.ts search "meditation viral" --limit 20` |
| TikTok | tiktok-scraper | Apify API `POST https://api.apify.com/v2/acts/clockworks~tiktok-scraper/runs` |
| Reddit | **reddit-cli**（`~/.openclaw/skills/reddit-cli`） | `cd ~/.openclaw/skills/reddit-cli && node scripts/reddit-cli.js search "習慣 瞑想" 10`（`REDDIT_SESSION` を `~/.openclaw/.env` に設定。VPS IP がブロックされる場合は失敗するが、X + TikTok のみで続行） |

---

## 出力形式その 1：trends/YYYY-MM-DD.json（トレンドのみ・投稿しない）

他アカウントのバズった「そのままの hook」と、source・trendContext・pattern・**analysis**（なぜバズったか）を書く。**platform 配列は不要**（source で十分）。**出力する JSON の値はプレースホルダーとする。例はこのセクションの JSON の外に書く。**

```json
{
  "date": "YYYY-MM-DD",
  "source": "trend-hunter",
  "trends": [
    {
      "id": "tr-001",
      "hook": "（バズったそのままの文言）",
      "source": "x または tiktok または reddit",
      "trendContext": "（そのトレンドがどこで・なぜ起きているか 1〜2 文）",
      "pattern": "（再現用の短い型）",
      "category": "（カテゴリ）",
      "analysis": "（なぜバズったか）"
    }
  ]
}
```

**例（参考・JSON の外）:** hook: "I tried meditating for 30 days and here's what happened to my anxiety" / source: "tiktok" / trendContext: "TikTok で「30日チャレンジ＋不安の変化」系が伸びている。" / pattern: "[習慣] + [30日] → 試した → 結果が変わった" / analysis: "30日という具体数字と before/after が明確でクリックされやすい。"

- **source（各要素）:** `"x"` \| `"tiktok"` \| `"reddit"`
- **trendContext:** そのトレンドがどこで・なぜ起きているかの要約（1〜2文）。
- **pattern:** 再現用の短い型。例: `"[彼氏] + [疑い] → 一緒に試した → 反応が変わった"`
- **analysis:** なぜバズったかの簡潔な理由（構成・数字・感情フック・プラットフォーム特性など）。

---

## 出力形式その 2：hooks/YYYY-MM-DD.json（Blotato に schedule する 1 本）

トレンドを元に **投稿 1 本** を書く。X 用 **postText** は **実際に X に載せる 1 ツイート**（**280 文字以内**）。TikTok 用 **caption** は長くてよい（最大 2200 文字）。**reasons** は具体的に（どの tr-xxx、どの pattern を参考にしたか）。**出力する JSON の値はプレースホルダーとする。** 日本市場・日本語前提。

```json
{
  "date": "YYYY-MM-DD",
  "slot": "9am または 9pm",
  "scheduledTime": "YYYY-MM-DDTHH:mm:ss+09:00",
  "entries": [
    {
      "id": "hook-001",
      "platform": "x",
      "postText": "（X に載せる 1 ツイート・280 文字以内）",
      "reasons": ["（参考にした tr-xxx と pattern）"]
    },
    {
      "id": "hook-001",
      "platform": "tiktok",
      "caption": "（TikTok 用キャプション・最大 2200 文字）",
      "imageUrl": "（FAL 等で生成した画像 URL。imagePrompt から生成）",
      "imagePrompt": "（FAL で画像生成するためのプロンプト。TikTok 用サムネイルに必須。caption の内容を視覚化する英文プロンプト）",
      "reasons": ["（参考にした tr-xxx と trendContext）"]
    }
  ]
}
```

- **postText:** **実際に X に投稿する 1 ツイート**。280 文字以内。スレッド番号（1/3 等）や URL は含めず、その 1 本だけで完結する・そのまま投稿できる文にする。日本市場・日本語前提の場合は日本語で書く。
- **caption:** TikTok 用。最大 2200 文字まで可。ハッシュタグ・改行可。日本語で書く。
- **imagePrompt:** TikTok 用サムネイル画像を FAL で生成するためのプロンプト（英文）。caption の内容を視覚化する。**必須。** trend-hunter はここに英文プロンプトを書くだけ。画像生成は **tiktok-poster** が FAL で行う。
- **imageUrl:** **プレースホルダーとしてキーだけ用意し、空文字 `""` でよい。** tiktok-poster が imagePrompt を FAL に渡して画像を生成し、得た URL をここに埋めてから投稿する。trend-hunter は imageUrl を生成しない。
- **reasons:** どの `tr-xxx` のどの pattern / trendContext を参考にしたか、具体的に書く。
**例（JSON の外）:** postText "30日瞑想してみた。不安に、実際に起きたこと。"（日本市場・日本語）

---

## SKILL.md 用プロンプト全文（trends と hooks・日本語・例付き）

以下を LLM に渡して trends と hooks を生成させる。

---

### トレンド出力（trends/YYYY-MM-DD.json）用プロンプト

「あなたが、X / TikTok / Reddit から取得した生のトレンド候補を、次のルールで **trends/YYYY-MM-DD.json** 用の JSON にまとめよ。

- 各要素に必ず含める: id（tr-001 形式）, hook（そのままの文言）, source（x|tiktok|reddit）, trendContext（そのトレンドがどこで・なぜ起きているか 1〜2 文）, pattern（再現用の短い型）, category, **analysis**（なぜバズったか。構成・数字・感情フック・プラットフォーム特性を簡潔に）。
- **platform 配列は使わない。** source で十分。
- 投稿はまだ生成しない。発見したトレンドの記録のみ。」

**例（1 件）:**  
hook: "I tried meditating for 30 days and here's what happened to my anxiety"  
source: "tiktok"  
trendContext: "TikTok で「30日チャレンジ＋不安の変化」系が伸びている。"  
pattern: "[習慣] + [30日] → 試した → 結果が変わった"  
analysis: "30日という具体数字と before/after が明確でクリックされやすい。"

---

### 投稿 1 本生成（hooks/YYYY-MM-DD.json）用プロンプト

「上記 trends のうち 1 本を選び、**hooks/{slot}/YYYY-MM-DD.json** 用の投稿を 1 本生成せよ（slot は 9am または 9pm）。

- **X 用 postText:** 実際に X に載せる **1 ツイート**。**280 文字以内**。スレッドの 1 本目としても単体としても成立する文にする。例: 「30日瞑想してみた。不安に実際に起きたこと。」
- **TikTok 用 caption:** 長くてよい（最大 2200 文字）。ハッシュタグ・改行可。例: 「30日瞑想で不安が変わった。何が起きたか。 #meditation #mindfulness」
- **TikTok 用 imagePrompt:** FAL でサムネイル画像を生成するための**英文プロンプト**。caption の内容を視覚化する。**必須。** 例: "A person meditating peacefully at sunrise, soft lighting, mindfulness, calm atmosphere, high quality thumbnail for social media"
- **TikTok 用 imageUrl:** **空でよい（プレースホルダー）。** tiktok-poster が imagePrompt から FAL で画像を生成し、URL を埋めてから投稿する。
- **reasons:** どの tr-xxx のどの pattern / trendContext を参考にしたか、具体的に書く。例: 「tr-001 の pattern を採用」「anxiety は 13 ProblemType と直結」。

---

## 入力
- **cron 起動時（5am または 5pm）:** payload に slot（9am または 9pm）と date（今日）が含まれる。その slot と date をそのまま使い、上記実行順序に従う。
- 手動: `workspace/ops/proposals.json` に `skillName: "trend-hunter"`, `steps: [{ kind: "run_trend_scan" }]` を追加。その場合は payload またはメッセージで slot と date を指定する。

## 失敗時処理
- 429/5xx: リトライ（最大3回）または DLQ。
- クレジット枯渇: ops event + Slack（24h 重複抑止）。
- **Reddit ブロック（VPS IP）:** reddit-cli が「Blocked」等で失敗する場合、Reddit をスキップし X + TikTok のみで続行。web_search は使わない。

## 禁止事項
- 送信（投稿）しない。収集と 2 種類の JSON 保存のみ。
- Railway に hook/trend を保存しない。

## Cron
**5am と 5pm の 2 本（12 時間ごと）。** payload に slot と date が入る。5am → slot 9am・今日の date、5pm → slot 9pm・今日の date。Blotato への schedule は **別 cron**（x-poster / tiktok-poster が 9:00 と 21:00 に hooks を読んで投稿）。
