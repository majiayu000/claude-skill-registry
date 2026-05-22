---
name: keyword-mega-extractor
description: mega-researchと連携して複合キーワード・ロングテール・ニッチ・関連・売れるキーワード・急上昇キーワードを抽出。SEO/PPC/コンテンツマーケティング向け。
argument-hint: "[シードキーワード] [--type=all|longtail|niche|trending|buying]"
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Bash(curl:*, python:*, node:*)
model: opus
---

# keyword-mega-extractor - キーワード最強抽出システム

## 概要

mega-researchの検索結果を解析し、多様なキーワードを自動抽出するシステム。

```
┌─────────────────────────────────────────────────────────────────────┐
│              KEYWORD MEGA EXTRACTOR SYSTEM                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [シードKW入力]                                                     │
│       │                                                             │
│       ▼                                                             │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              mega-research 統合検索                          │   │
│  │  Tavily | SerpAPI | Brave | NewsAPI | Reddit | Perplexity   │   │
│  └────────────────────────────┬────────────────────────────────┘   │
│                               │                                     │
│       ┌───────────────────────┼───────────────────────┐            │
│       ▼                       ▼                       ▼            │
│  ┌─────────┐           ┌─────────┐           ┌─────────┐          │
│  │ Google  │           │ People  │           │ Related │          │
│  │Suggest  │           │Also Ask │           │ Search  │          │
│  └────┬────┘           └────┬────┘           └────┬────┘          │
│       │                     │                     │                │
│       └─────────────────────┼─────────────────────┘                │
│                             ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    キーワード分類エンジン                     │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │ ✅ 複合キーワード    「シードKW + 修飾語」                     │   │
│  │ ✅ ロングテール      3語以上、低競合・高CVR                    │   │
│  │ ✅ ニッチキーワード  検索ボリューム低・競合少                   │   │
│  │ ✅ 関連キーワード    共起語・類義語                            │   │
│  │ ✅ 売れるキーワード  購買意図が高い                            │   │
│  │ ✅ 急上昇キーワード  トレンド上昇中                            │   │
│  │ ✅ 質問キーワード    「〜とは」「〜方法」                       │   │
│  │ ✅ 比較キーワード    「A vs B」「おすすめ」                     │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                             │                                       │
│                             ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                      出力ファイル                             │   │
│  │  keywords.json | keywords.csv | analysis.md                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## キーワード分類

### 1. 複合キーワード（Compound Keywords）
シードキーワードに修飾語を追加したもの。

```
シード: 「投資信託」
複合: 「投資信託 おすすめ 2026」「投資信託 初心者 始め方」
```

### 2. ロングテールキーワード（Long-tail Keywords）
3語以上の具体的なフレーズ。低競合・高コンバージョン率。

```
シード: 「投資信託」
ロングテール:
  - 「投資信託 初心者 おすすめ ランキング 2026」
  - 「投資信託 毎月分配型 やめたほうがいい 理由」
  - 「新NISA 投資信託 積立 シミュレーション」
```

### 3. ニッチキーワード（Niche Keywords）
検索ボリューム低め、競合が少ない狙い目。

```
シード: 「投資信託」
ニッチ:
  - 「投資信託 繰上償還 リスク 対策」
  - 「投資信託 為替ヘッジあり なし どっち」
  - 「eMAXIS Slim 全世界株式 楽天VTI 比較」
```

### 4. 関連キーワード（Related Keywords）
共起語、類義語、関連トピック。

```
シード: 「投資信託」
関連:
  - 「ETF」「インデックスファンド」「アクティブファンド」
  - 「信託報酬」「分配金」「基準価額」
  - 「つみたてNISA」「iDeCo」
```

### 5. 売れるキーワード（Buying Intent Keywords）
購買意図が高いキーワード。アフィリエイト・ECに最適。

```
購買意図シグナル:
  - 「おすすめ」「ランキング」「比較」
  - 「口コミ」「評判」「レビュー」
  - 「最安値」「キャンペーン」「クーポン」
  - 「買い方」「申し込み方法」

例:
  - 「投資信託 おすすめ 証券会社 比較」
  - 「SBI証券 投資信託 口座開設 キャンペーン」
```

### 6. 急上昇キーワード（Trending Keywords）
最近検索が急増しているキーワード。

```
データソース:
  - Google Trends
  - NewsAPI（ニュース頻出度）
  - Reddit（バズ投稿）

例:
  - 「オルカン 暴落 買い時」
  - 「新NISA 枠 復活」
```

### 7. 質問キーワード（Question Keywords）
疑問形のキーワード。コンテンツ制作に最適。

```
パターン:
  - 「〜とは」「〜って何」
  - 「〜方法」「〜やり方」「〜手順」
  - 「なぜ〜」「どうして〜」
  - 「いつ〜」「どこで〜」

例:
  - 「投資信託とは わかりやすく」
  - 「投資信託 売り時 タイミング いつ」
```

### 8. 比較キーワード（Comparison Keywords）
比較検討段階のユーザー向け。

```
パターン:
  - 「A vs B」「A B 比較」「A B 違い」
  - 「A B どっち」「A B どちらがいい」

例:
  - 「投資信託 ETF 違い」
  - 「SBI証券 楽天証券 どっち」
```

## 使い方

```bash
# 全種類のキーワードを抽出
/keyword-mega-extractor 投資信託

# ロングテールのみ
/keyword-mega-extractor 投資信託 --type=longtail

# 売れるキーワードのみ
/keyword-mega-extractor プログラミングスクール --type=buying

# 急上昇キーワード
/keyword-mega-extractor AI --type=trending

# ニッチキーワード
/keyword-mega-extractor 副業 --type=niche
```

## 出力形式

### keywords/<seed>__<timestamp>/

```
├── input.yaml                # 入力パラメータ
├── keywords.json             # 全キーワードデータ
├── keywords.csv              # CSV形式（Excel/スプレッドシート用）
├── by_type/
│   ├── compound.json         # 複合キーワード
│   ├── longtail.json         # ロングテール
│   ├── niche.json            # ニッチ
│   ├── related.json          # 関連
│   ├── buying.json           # 売れる
│   ├── trending.json         # 急上昇
│   ├── question.json         # 質問
│   └── comparison.json       # 比較
├── analysis.md               # 分析レポート
└── content_ideas.md          # コンテンツアイデア
```

### keywords.json 形式

```json
{
  "seed": "投資信託",
  "extracted_at": "2026-02-02T10:00:00Z",
  "total_keywords": 150,
  "keywords": [
    {
      "keyword": "投資信託 おすすめ 2026",
      "type": "buying",
      "search_volume": "estimated: high",
      "competition": "medium",
      "buying_intent": 0.8,
      "trending_score": 0.6,
      "source": ["serpapi", "tavily"],
      "related_content_ideas": [
        "2026年版投資信託おすすめランキング",
        "初心者向け投資信託の選び方"
      ]
    }
  ]
}
```

### analysis.md 形式

```markdown
# キーワード分析レポート: 投資信託

## サマリー

| 指標 | 値 |
|------|-----|
| シードキーワード | 投資信託 |
| 抽出キーワード数 | 150 |
| ロングテール率 | 45% |
| 購買意図スコア平均 | 0.65 |

## キーワード分布

| タイプ | 件数 | 割合 |
|--------|------|------|
| 複合 | 30 | 20% |
| ロングテール | 45 | 30% |
| ニッチ | 15 | 10% |
| 関連 | 25 | 17% |
| 売れる | 20 | 13% |
| 急上昇 | 5 | 3% |
| 質問 | 10 | 7% |

## トップ10 売れるキーワード

| # | キーワード | 購買意図 | 競合度 |
|---|-----------|---------|--------|
| 1 | 投資信託 おすすめ 証券会社 | 0.9 | 高 |
| 2 | SBI証券 投資信託 手数料 比較 | 0.85 | 中 |
...

## コンテンツ戦略提案

### 優先度高（購買意図 + 低競合）

1. **「投資信託 繰上償還 リスク 対策」**
   - 検索意図: 情報収集
   - コンテンツ案: 「知らないと損！投資信託の繰上償還リスクと3つの対策」

2. ...
```

## キーワード抽出アルゴリズム

### 1. Google Suggest 取得（SerpAPI）

```bash
curl "https://serpapi.com/search.json?engine=google_autocomplete&q=${SEED}&api_key=${SERPAPI_KEY}"
```

### 2. People Also Ask 取得（SerpAPI）

```bash
curl "https://serpapi.com/search.json?engine=google&q=${SEED}&api_key=${SERPAPI_KEY}"
# → related_questions を抽出
```

### 3. Related Searches 取得

```bash
# Brave Search
curl "https://api.search.brave.com/res/v1/web/search?q=${SEED}" \
  -H "X-Subscription-Token: ${BRAVE_API_KEY}"
# → query.related_results を抽出
```

### 4. Reddit キーワード抽出

```bash
curl "https://www.reddit.com/search.json?q=${SEED}&sort=hot&limit=50"
# → タイトルから共起語を抽出
```

### 5. NewsAPI トレンド検出

```bash
curl "https://newsapi.org/v2/everything?q=${SEED}&sortBy=publishedAt&apiKey=${NEWSAPI_KEY}"
# → 頻出キーワードを抽出
```

## 購買意図スコア計算

```
購買意図スコア (0-1) =
  (購買シグナル語含有 × 0.4) +
  (比較語含有 × 0.3) +
  (行動語含有 × 0.3)

購買シグナル語: おすすめ, ランキング, 比較, 口コミ, レビュー, 最安値
比較語: vs, 違い, どっち
行動語: 買い方, 申し込み, 登録, 始め方
```

## トレンドスコア計算

```
トレンドスコア (0-1) =
  (ニュース出現頻度 × 0.4) +
  (Reddit投稿数 × 0.3) +
  (Google検索増加率 × 0.3)
```

## ユースケース

### 1. SEO記事企画

```bash
/keyword-mega-extractor プログラミング学習 --type=longtail
→ 「プログラミング 独学 1年 ロードマップ」などを取得
→ content_ideas.md で記事タイトル案を自動生成
```

### 2. アフィリエイト

```bash
/keyword-mega-extractor クレジットカード --type=buying
→ 「クレジットカード 年会費無料 還元率 比較」などを取得
→ 購買意図の高いKWでコンテンツ作成
```

### 3. PPC広告

```bash
/keyword-mega-extractor 転職エージェント --type=all
→ keywords.csv をGoogle Ads/Yahoo広告にインポート
→ 入札単価の参考に competition スコアを使用
```

### 4. コンテンツマーケティング

```bash
/keyword-mega-extractor SaaS --type=question
→ 「SaaSとは」「SaaS 導入メリット」などを取得
→ FAQ/ヘルプセンターコンテンツに活用
```

## 関連スキル

- `mega-research` - 統合リサーチシステム
- `taiyo-style-sales-letter` - セールスレター作成
- `seo-content-optimizer` - SEOコンテンツ最適化
