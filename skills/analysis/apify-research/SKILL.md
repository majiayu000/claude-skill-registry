# Apify Research Skill

高度なウェブスクレイピング・SNSデータ抽出スキル。

## Description

Apify MCP経由でSNS、検索エンジン、ECサイトから構造化データを自動抽出する高度なリサーチスキル。数千の既製スクレイパー（Actor）にアクセス可能。

## Triggers

このスキルは以下のキーワードで自動的にトリガーされます：

- 「Instagramを調査」「Instagram分析」
- 「Twitter/Xを調べて」「ツイート抽出」
- 「Amazon商品をリサーチ」「EC分析」
- 「Google検索結果を取得」「SERP分析」
- 「LinkedIn調査」「B2Bリサーチ」
- 「SNSスクレイピング」「ウェブ抽出」

## Available Actors

### SNS系

| Actor | 機能 | 出力 |
|-------|------|------|
| `instagram-scraper` | Instagram投稿・プロフィール | JSON/CSV |
| `twitter-scraper` | X/Twitterツイート・プロフィール | JSON/CSV |
| `tiktok-scraper` | TikTok動画・プロフィール | JSON/CSV |
| `youtube-scraper` | YouTube動画メタデータ | JSON/CSV |
| `linkedin-scraper` | LinkedInプロフィール | JSON/CSV |

### 検索エンジン系

| Actor | 機能 | 出力 |
|-------|------|------|
| `google-search-scraper` | Google検索結果 | JSON/CSV |
| `google-maps-scraper` | Googleマップ店舗情報 | JSON/CSV |
| `bing-search-scraper` | Bing検索結果 | JSON/CSV |

### EC系

| Actor | 機能 | 出力 |
|-------|------|------|
| `amazon-scraper` | Amazon商品情報・レビュー | JSON/CSV |
| `ebay-scraper` | eBay商品情報 | JSON/CSV |
| `shopify-scraper` | Shopifyストア商品 | JSON/CSV |

### 汎用

| Actor | 機能 | 出力 |
|-------|------|------|
| `web-scraper` | 汎用ウェブスクレイピング | JSON/CSV |
| `cheerio-scraper` | 高速HTMLパース | JSON/CSV |
| `puppeteer-scraper` | JavaScript対応スクレイピング | JSON/CSV |

## Workflow

```
1. ユーザーリクエスト分析
   └─ ターゲットプラットフォーム特定
   └─ 抽出項目の明確化

2. Actor選択
   └─ 最適なApify Actorを選択
   └─ 入力パラメータ設定

3. スクレイピング実行
   └─ Apify MCP経由でActor実行
   └─ 進捗モニタリング

4. データ構造化
   └─ JSON/CSVでデータ取得
   └─ 必要に応じてクレンジング

5. レポート生成
   └─ 分析サマリー作成
   └─ インサイト抽出
```

## Usage Examples

### Instagram競合分析

```
「@competitor_account のInstagram投稿を分析して、
エンゲージメント率が高い投稿の特徴をまとめて」

→ instagram-scraper でプロフィール・投稿取得
→ エンゲージメント分析
→ 成功パターンをレポート
```

### Amazon市場調査

```
「"ワイヤレスイヤホン" のAmazon上位20商品を調査して、
価格帯、レビュー評価、主要機能をまとめて」

→ amazon-scraper で商品情報取得
→ 価格・評価分析
→ 競合マトリクス作成
```

### Google検索順位チェック

```
「"Claude Code 使い方" で検索して、
上位10サイトのタイトル・URL・スニペットを取得」

→ google-search-scraper でSERP取得
→ 競合コンテンツ分析
→ SEO改善提案
```

## Required MCP

- `apify` (defer_loading: true)

## Environment Variables

```bash
APIFY_API_TOKEN=apify_api_xxxxx  # Apify APIトークン
```

## Cost

| 項目 | 料金 |
|------|------|
| 無料枠 | 月$5相当のクレジット |
| Compute unit | $0.25/unit |
| 一般的なスクレイピング | $0.01-0.50/リクエスト |

**コスト最適化Tips:**
- 小規模テストから開始
- 必要なフィールドのみ取得
- スケジューリングで分散実行

## Output Format

### JSON出力例

```json
{
  "source": "instagram",
  "actor": "instagram-scraper",
  "timestamp": "2026-02-03T12:00:00Z",
  "results": [
    {
      "username": "example_user",
      "followers": 10000,
      "posts": [
        {
          "id": "xxx",
          "likes": 500,
          "comments": 50,
          "caption": "...",
          "timestamp": "..."
        }
      ]
    }
  ],
  "metadata": {
    "total_items": 100,
    "cost_estimate": "$0.15"
  }
}
```

## Integration with Other Skills

- `/research-free` → 無料リサーチで概要把握 → `/apify-research` で詳細データ取得
- `/mega-research` → Apifyデータをソースとして活用
- `/lp-analysis` → 競合LP分析にApifyデータを使用

## Limitations

- レート制限: サイトによって異なる
- 利用規約: 各サイトのToSを確認すること
- データ鮮度: リアルタイムではなくスナップショット

## References

- [Apify MCP Server](https://github.com/apify/apify-mcp-server)
- [Apify Store](https://apify.com/store)
- [Apify Documentation](https://docs.apify.com/)
