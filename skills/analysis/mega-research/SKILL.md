---
name: mega-research
description: |
  6つの検索API（Tavily/SerpAPI/Brave/NewsAPI/Reddit/Perplexity）を統合した最強リサーチシステム。
  深層調査から出典付きレポート生成まで自動実行。
  Use when: (1) user says「徹底調査」「深層リサーチ」「完全調査」「mega-research」,
  (2) user needs multi-source research with citations,
  (3) user wants market analysis, competitor research, or trend analysis,
  (4) user mentions「出典付き」「クロス検証」「複数ソース」.
  Do NOT use for: simple fact-checking (use research-free), single-source lookups,
  or when API keys are not configured.
argument-hint: "[トピック] [--mode=deep|quick|news|trend]"
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Bash(curl:*, python:*, node:*)
model: opus
---

# mega-research - 最強統合リサーチシステム

## 概要

6つの検索APIを統合し、用途に応じて最適な情報収集を行う最強リサーチスキル。

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MEGA RESEARCH SYSTEM                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐              │
│  │ Tavily  │  │ SerpAPI │  │ Brave   │  │ NewsAPI │              │
│  │AI検索特化│  │Google結果│  │広範囲Web │  │ニュース  │              │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘              │
│       │            │            │            │                     │
│       └────────────┼────────────┼────────────┘                     │
│                    │            │                                   │
│              ┌─────┴────┐  ┌────┴─────┐                           │
│              │ Reddit   │  │Perplexity│                           │
│              │コミュニティ│  │AI要約    │                           │
│              └────┬─────┘  └────┬─────┘                           │
│                   │             │                                   │
│                   └──────┬──────┘                                   │
│                          │                                          │
│                    ┌─────┴─────┐                                   │
│                    │ 統合エンジン │                                   │
│                    │ ・重複排除   │                                   │
│                    │ ・スコアリング│                                   │
│                    │ ・クロス検証 │                                   │
│                    └─────┬─────┘                                   │
│                          │                                          │
│                    ┌─────┴─────┐                                   │
│                    │  レポート   │                                   │
│                    └───────────┘                                   │
└─────────────────────────────────────────────────────────────────────┘
```

## 統合API一覧

| API | 特徴 | 用途 | 月間制限 |
|-----|------|------|---------|
| **Tavily** | AI検索特化、高精度 | セマンティック検索、事実確認 | 1,000 |
| **SerpAPI** | Google検索結果 | SERP分析、競合調査 | 100 |
| **Brave Search** | プライバシー重視、広範囲 | 一般Web検索 | 2,000 |
| **NewsAPI** | ニュース集約 | 最新ニュース、トレンド | 100/日 |
| **Reddit API** | コミュニティ意見 | ユーザーレビュー、議論 | - |
| **Perplexity** | AI検索+要約 | 要約生成、引用付き回答 | 課金制 |

## 使い方

```bash
# 基本リサーチ（全API使用）
/mega-research AIエージェント市場の最新動向

# クイック検索（Tavily + Brave）
/mega-research Next.js 15の新機能 --mode=quick

# ニュース特化（NewsAPI + Perplexity）
/mega-research 生成AI規制 --mode=news

# トレンド分析（Reddit + NewsAPI）
/mega-research 仮想通貨市場 --mode=trend

# 深層調査（全API + クロス検証）
/mega-research 量子コンピューティング投資機会 --mode=deep
```

## リサーチモード

### 1. Deep Mode（デフォルト）
全APIを使用した徹底調査。クロス検証で信頼性を高める。

```
実行フロー:
1. Tavily → 高精度ファクト収集（10-20件）
2. SerpAPI → Google上位結果取得（10件）
3. Brave → 広範囲Web検索（20件）
4. NewsAPI → 最新ニュース（10件）
5. Reddit → コミュニティ意見（5スレッド）
6. Perplexity → AI要約生成
7. 統合 → 重複排除 + スコアリング + クロス検証
8. レポート → 出典付きマークダウン
```

### 2. Quick Mode
高速検索。2-3秒で結果を返す。

```
使用API: Tavily + Brave
出力: 簡潔な回答 + 主要ソース3-5件
```

### 3. News Mode
ニュースとトレンドに特化。

```
使用API: NewsAPI + Perplexity + Google News (SerpAPI)
出力: 最新ニュース一覧 + トレンド分析
```

### 4. Trend Mode
コミュニティの声とトレンドを分析。

```
使用API: Reddit + NewsAPI + Brave
出力: コミュニティ反応 + トレンドスコア
```

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
│   ├── reddit.json      # Reddit結果
│   └── perplexity.json  # Perplexity結果
├── analysis.json        # 統合分析結果
├── report.md            # 最終レポート
└── summary.txt          # 1行要約
```

## レポート形式

```markdown
# [トピック] 調査レポート

**調査日**: YYYY-MM-DD
**使用API**: Tavily, SerpAPI, Brave, NewsAPI, Reddit, Perplexity
**ソース数**: XX件（重複排除後）
**信頼度スコア**: 85/100

## エグゼクティブサマリー

[3-5文の要約]

## 主要な発見

### 1. [発見タイトル]
[詳細]
**信頼度**: 高 | **ソース**: [1][2][3]

### 2. [発見タイトル]
...

## データ分析

| 指標 | 値 | 出典 |
|-----|-----|------|
| ... | ... | ... |

## コミュニティの声（Reddit）

> "..." - r/technology (+1.2k upvotes)

## 最新ニュース

1. [タイトル](URL) - YYYY-MM-DD
2. ...

## 矛盾・不確実な点

- [矛盾点1]: ソースAとソースBで相違
- [不確実]: 公式発表なし

## 出典一覧

[1] [タイトル](URL) - Tavily
[2] [タイトル](URL) - Google (SerpAPI)
...
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
    "messages": [{"role": "user", "content": "'"${QUERY}"'についての最新情報を要約してください。出典URLも含めてください。"}]
  }'
```

## 環境変数

```bash
# .envまたは~/.zshrcに追加
export TAVILY_API_KEY="tvly-xxxxxxxxxxxxxxxxxxxxxxxx"
export SERPAPI_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export BRAVE_API_KEY="BSAxxxxxxxxxxxxxxxxxxxxxxxx"
export NEWSAPI_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export PERPLEXITY_API_KEY="pplx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

**APIキー取得先**:
- Tavily: https://tavily.com/
- SerpAPI: https://serpapi.com/
- Brave: https://brave.com/search/api/
- NewsAPI: https://newsapi.org/
- Perplexity: https://www.perplexity.ai/settings/api

## スコアリングアルゴリズム

各ソースの信頼度を以下で計算:

```
信頼度スコア =
  (ドメイン権威度 × 0.3) +
  (情報鮮度 × 0.2) +
  (クロス検証率 × 0.3) +
  (引用数 × 0.2)
```

| ドメイン種別 | 権威度 |
|-------------|--------|
| .gov, .edu | 100 |
| 主要メディア | 90 |
| 専門サイト | 80 |
| 一般サイト | 60 |
| フォーラム | 40 |

## ベストプラクティス

1. **具体的なクエリを使用**
   - ❌ "AI"
   - ✅ "2026年 生成AIエージェント市場規模 予測"

2. **モードを適切に選択**
   - 事実確認 → quick
   - 市場調査 → deep
   - ニュース → news
   - 口コミ → trend

3. **レート制限に注意**
   - deep modeは1日5回程度に抑える
   - quickは無制限に近い

4. **結果の検証**
   - 複数ソースで確認された情報を優先
   - 単一ソースの情報は「要検証」とマーク

## 関連スキル

- `keyword-mega-extractor` - キーワード抽出
- `gpt-researcher` - 自律型深層リサーチ
- `research-cited-report` - 出典付きレポート

## トラブルシューティング

### よくあるエラーと対処法

#### Error: API key not found
**原因**: 環境変数が設定されていない
**対処**:
```bash
# 環境変数を確認
echo $TAVILY_API_KEY
echo $SERPAPI_KEY

# 未設定なら追加
export TAVILY_API_KEY="tvly-xxxxx"
```

#### Error: Rate limit exceeded
**原因**: API呼び出し回数制限を超過
**対処**:
- deep modeは1日5回程度に抑える
- quick modeを使用する
- 60秒待ってリトライ

#### Error: No results found
**原因**: クエリが曖昧または専門的すぎる
**対処**:
- より具体的なキーワードを使用
- 英語でも検索を試す
- quick modeで部分検索

#### Error: Timeout
**原因**: API応答が遅い（Perplexity等）
**対処**:
- `--mode=quick`で高速検索
- 特定APIをスキップ
- ネットワーク接続を確認
