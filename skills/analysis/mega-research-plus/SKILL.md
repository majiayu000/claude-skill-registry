---
name: mega-research-plus
description: 8つの検索ソース（Tavily/SerpAPI/Brave/NewsAPI/Perplexity/Twitter/DuckDuckGo/WebSearch）を統合した最強リサーチシステム。API版＋MCP版＋組み込み版を完全統合。
argument-hint: "[トピック] [--mode=deep|quick|news|social|free]"
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Bash(curl:*, python:*, node:*)
model: opus
---

# mega-research-plus - 最強統合リサーチシステム v2

## 概要

8つの検索ソースを統合し、用途に応じて最適な情報収集を行う最強リサーチスキル。
API版、MCP版、組み込み版を完全統合。

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MEGA RESEARCH PLUS SYSTEM v2                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      API LAYER (要キー)                              │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  │   │
│  │  │ Tavily  │  │ SerpAPI │  │ Brave   │  │ NewsAPI │  │Perplexity│  │   │
│  │  │AI検索   │  │Google   │  │広範囲   │  │ニュース │  │AI要約   │  │   │
│  │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  │   │
│  └───────┼───────────┼───────────┼───────────┼───────────┼──────────┘   │
│          │           │           │           │           │               │
│  ┌───────┼───────────┼───────────┼───────────┼───────────┼──────────┐   │
│  │       │           │     MCP LAYER (無料)  │           │          │   │
│  │  ┌────┴────┐  ┌───┴───┐                                          │   │
│  │  │ Twitter │  │DuckDuck│                                          │   │
│  │  │  X/SNS  │  │Go/Bing │                                          │   │
│  │  └────┬────┘  └───┬───┘                                           │   │
│  └───────┼───────────┼──────────────────────────────────────────────┘   │
│          │           │                                                   │
│  ┌───────┼───────────┼──────────────────────────────────────────────┐   │
│  │       │    BUILT-IN LAYER (組み込み)                              │   │
│  │  ┌────┴───────────┴────┐                                          │   │
│  │  │     WebSearch       │                                          │   │
│  │  │   (Anthropic API)   │                                          │   │
│  │  └──────────┬──────────┘                                          │   │
│  └─────────────┼────────────────────────────────────────────────────┘   │
│                │                                                         │
│          ┌─────┴─────┐                                                   │
│          │ 統合エンジン │                                                   │
│          │ ・重複排除   │                                                   │
│          │ ・スコアリング│                                                   │
│          │ ・クロス検証 │                                                   │
│          │ ・AI要約    │                                                   │
│          └─────┬─────┘                                                   │
│                │                                                         │
│          ┌─────┴─────┐                                                   │
│          │  レポート   │                                                   │
│          └───────────┘                                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 統合ソース一覧（8種類）

| # | ソース | 種別 | 特徴 | 用途 | 制限 |
|---|--------|------|------|------|------|
| 1 | **Tavily** | API | AI検索特化、高精度 | セマンティック検索、事実確認 | 1,000/月 |
| 2 | **SerpAPI** | API | Google検索結果 | SERP分析、競合調査 | 100/月 |
| 3 | **Brave** | API | プライバシー重視 | 広範囲Web検索 | 2,000/月 |
| 4 | **NewsAPI** | API | ニュース集約 | 最新ニュース、トレンド | 100/日 |
| 5 | **Perplexity** | API | AI検索+要約 | 要約生成、引用付き回答 | 課金制 |
| 6 | **Twitter/X** | MCP | SNS | コミュニティ、トレンド | Cookie認証 |
| 7 | **DuckDuckGo** | MCP | APIキー不要 | 無料検索 | 無制限 |
| 8 | **WebSearch** | 組込 | Claude内蔵 | フォールバック | 制限あり |

## 使い方

```bash
# 徹底調査（全ソース使用）
/mega-research-plus AIエージェント市場の最新動向 --mode=deep

# クイック検索（3秒以内）
/mega-research-plus Next.js 15の新機能 --mode=quick

# ニュース特化
/mega-research-plus 生成AI規制 --mode=news

# SNS・コミュニティ特化
/mega-research-plus Claude Code 評判 --mode=social

# APIキー不要（配布向け）
/mega-research-plus 投資信託 始め方 --mode=free
```

## リサーチモード

### 1. Deep Mode（徹底調査）
全APIを使用した徹底調査。クロス検証で信頼性を高める。

```
使用ソース: Tavily + SerpAPI + Brave + NewsAPI + Perplexity + Twitter
実行時間: 30-60秒
出力: 50件以上のソース + 詳細レポート

フロー:
1. Tavily → 高精度ファクト収集（10-20件）
2. SerpAPI → Google上位結果取得（10件）
3. Brave → 広範囲Web検索（20件）
4. NewsAPI → 最新ニュース（10件）
5. Twitter → SNSトレンド（10ツイート）
6. Perplexity → AI要約生成
7. 統合 → 重複排除 + スコアリング + クロス検証
```

### 2. Quick Mode（高速検索）
2-3秒で結果を返す。

```
使用ソース: Tavily + Brave + WebSearch
実行時間: 2-3秒
出力: 15件 + 簡潔な回答
```

### 3. News Mode（ニュース特化）
最新ニュースとトレンドに特化。

```
使用ソース: NewsAPI + Perplexity + SerpAPI(Google News)
実行時間: 5-10秒
出力: ニュース一覧 + トレンド分析
```

### 4. Social Mode（SNS特化）
SNSとコミュニティの声を収集。

```
使用ソース: Twitter + DuckDuckGo + Brave
実行時間: 10-20秒
出力: ツイート + コミュニティ反応
```

### 5. Free Mode（APIキー不要）
配布向け。APIキーなしで動作。

```
使用ソース: WebSearch + DuckDuckGo (MCP)
実行時間: 5-10秒
出力: 20件 + 基本レポート
```

## API呼び出し実装

### Tavily API

```bash
curl -X POST "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "'"${TAVILY_API_KEY}"'",
    "query": "'"${QUERY}"'",
    "search_depth": "advanced",
    "include_answer": true,
    "include_raw_content": true,
    "max_results": 10
  }'
```

### SerpAPI

```bash
curl "https://serpapi.com/search.json?engine=google&q=${QUERY}&api_key=${SERPAPI_KEY}&num=10"
```

### Brave Search

```bash
curl "https://api.search.brave.com/res/v1/web/search?q=${QUERY}" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: ${BRAVE_API_KEY}"
```

### NewsAPI

```bash
curl "https://newsapi.org/v2/everything?q=${QUERY}&apiKey=${NEWSAPI_KEY}&sortBy=publishedAt&pageSize=10"
```

### Perplexity API

```bash
curl -X POST "https://api.perplexity.ai/chat/completions" \
  -H "Authorization: Bearer ${PERPLEXITY_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-3.1-sonar-large-128k-online",
    "messages": [{"role": "user", "content": "'"${QUERY}"'についての最新情報を要約してください。"}]
  }'
```

### Twitter/X (MCP経由)

```
MCPツール: twitter-client
機能: get_tweet, search_tweets, get_user_tweets
```

### DuckDuckGo (MCP経由)

```
MCPツール: open-websearch
機能: search_duckduckgo, search_bing, search_brave
```

### WebSearch (組み込み)

```
Claude Code組み込みのWebSearchツールを直接使用
```

## 環境変数

APIキーは **`.env`ファイル**で安全に管理してください（`.gitignore`に含まれています）。

### 設定方法

1. プロジェクトルートの`.env`ファイルを編集:

```bash
# Research & Search APIs (mega-research-plus)
TAVILY_API_KEY=your-tavily-api-key
SERPAPI_KEY=your-serpapi-key
BRAVE_SEARCH_API_KEY=your-brave-api-key
NEWSAPI_KEY=your-newsapi-key
PERPLEXITY_API_KEY=your-perplexity-api-key

# Twitter/X Cookie認証
TWITTER_AUTH_TOKEN=your-auth-token
TWITTER_CT0=your-ct0
TWITTER_TWID=your-twid
```

2. または `.env.example` をコピーして編集:

```bash
cp .env.example .env
# 実際のAPIキーを入力
```

### APIキー取得先

| API | URL | 無料枠 |
|-----|-----|--------|
| Tavily | https://tavily.com/ | 1,000 req/month |
| SerpAPI | https://serpapi.com/ | 100 req/month |
| Brave Search | https://brave.com/search/api/ | 2,000 req/month |
| NewsAPI | https://newsapi.org/ | 100 req/day |
| Perplexity | https://www.perplexity.ai/settings/api | 課金制 |

## 出力形式

### research/runs/<timestamp>__<slug>/

```
├── input.yaml           # 入力パラメータ
├── evidence.jsonl       # 収集した証拠（全ソース）
├── sources/
│   ├── tavily.json      # Tavily結果
│   ├── serpapi.json     # SerpAPI結果
│   ├── brave.json       # Brave結果
│   ├── newsapi.json     # NewsAPI結果
│   ├── perplexity.json  # Perplexity結果
│   ├── twitter.json     # Twitter結果
│   └── websearch.json   # WebSearch結果
├── analysis.json        # 統合分析結果
├── report.md            # 最終レポート
└── summary.txt          # 1行要約
```

## レポート形式

```markdown
# [トピック] 調査レポート

**調査日**: YYYY-MM-DD
**使用ソース**: Tavily, SerpAPI, Brave, NewsAPI, Perplexity, Twitter, WebSearch
**ソース数**: XX件（重複排除後）
**信頼度スコア**: 85/100

## エグゼクティブサマリー

[3-5文の要約]

## 主要な発見

### 1. [発見タイトル]
[詳細]
**信頼度**: 高 | **ソース**: [1][2][3]

## SNSトレンド（Twitter）

> "..." - @user (+1.2k likes)

## 最新ニュース

1. [タイトル](URL) - YYYY-MM-DD

## 出典一覧

[1] [タイトル](URL) - Tavily
[2] [タイトル](URL) - Google (SerpAPI)
...
```

## スコアリングアルゴリズム

```
信頼度スコア =
  (ドメイン権威度 × 0.25) +
  (情報鮮度 × 0.20) +
  (クロス検証率 × 0.30) +
  (引用数 × 0.15) +
  (SNSエンゲージメント × 0.10)
```

## ベストプラクティス

1. **具体的なクエリを使用**
   - ❌ "AI"
   - ✅ "2026年 生成AIエージェント市場規模 予測"

2. **モードを適切に選択**
   - 事実確認 → quick
   - 市場調査 → deep
   - ニュース → news
   - 口コミ・評判 → social
   - 配布用 → free

3. **レート制限に注意**
   - deep modeは1日5回程度に抑える
   - quick/freeは頻繁に使用OK

## 関連スキル

- `mega-research` - 従来版（6 API）
- `research-free` - APIキー不要版
- `keyword-mega-extractor` - キーワード抽出
- `gpt-researcher` - 自律型深層リサーチ
- `research-cited-report` - 出典付きレポート
