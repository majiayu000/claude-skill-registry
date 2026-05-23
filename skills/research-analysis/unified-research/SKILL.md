---
name: unified-research
description: |
  複数のリサーチAPI（Tavily/SerpAPI/Brave/NewsAPI/Perplexity）を統合した情報収集。
  Use when: (1) user says「リサーチして」「調べて」「情報を集めて」「深掘りして」,
  (2) user wants multi-source research,
  (3) user mentions「ファクトチェック」「情報収集」.
  Do NOT use for: APIキー不要の簡易調査（research-freeを使用）、
  最強の徹底調査（mega-researchを使用）。
---

# Unified Research Skill

複数のリサーチAPIを統合した高品質な情報収集スキル。

## When to Use This Skill

以下の場合に使用:
- トピックについて深くリサーチしたい時
- 信頼性の高い情報源から情報を集めたい時
- ファクトベースのコンテンツを作成したい時
- 複数の検索エンジンの結果を比較したい時

**トリガーワード**: 「リサーチして」「調べて」「情報を集めて」「深掘りして」

## 統合API

| API | 特徴 | 用途 |
|-----|------|------|
| **Tavily** | AI検索特化 | 高品質なセマンティック検索 |
| **SerpAPI** | Google検索 | 構造化された検索結果 |
| **Brave Search** | プライバシー重視 | 広範なWeb検索 |
| **NewsAPI** | ニュース集約 | 最新ニュース取得 |
| **Perplexity** | AI検索+引用 | サマリー生成と引用付き回答 |

## Quick Start

```bash
cd /Users/matsumototoshihiko/Desktop/dev/\ kindlenote0201/kindle-content-empire

# 単一クエリでリサーチ
npx ts-node packages/worker/src/research/run-unified-research.ts single "新NISA 2024"

# 新NISA専用リサーチ（7クエリ自動実行）
npx ts-node packages/worker/src/research/run-unified-research.ts nisa

# トピックリサーチ（5クエリ自動実行）
npx ts-node packages/worker/src/research/run-unified-research.ts topic "投資信託"
```

## API使用例

### TypeScriptから使用

```typescript
import { unifiedSearch, researchTopic } from './unified-research';

// 単一クエリ
const result = await unifiedSearch('新NISA 2024', {
  tavily: true,
  serpapi: true,
  brave: true,
  newsapi: false,  // ニュースは必要時のみ
  perplexity: true,
});

console.log(`ソース数: ${result.sources.length}`);
console.log(`ファクト数: ${result.facts.length}`);
console.log(`AIサマリー: ${result.summary}`);

// トピックリサーチ（複数クエリ）
const results = await researchTopic('仮想通貨', true);
```

## 出力形式

### ResearchResult

```typescript
interface ResearchResult {
  query: string;           // 検索クエリ
  sources: ResearchSource[]; // 情報ソース一覧
  summary?: string;        // AIサマリー（Perplexity）
  facts: string[];         // 抽出されたファクト
  timestamp: Date;         // 実行日時
  apiUsed: string[];       // 使用したAPI一覧
}
```

### ResearchSource

```typescript
interface ResearchSource {
  title: string;           // タイトル
  url: string;             // URL
  snippet: string;         // スニペット/要約
  source: string;          // ソースAPI名
  publishedAt?: string;    // 公開日（ニュースの場合）
  score?: number;          // 関連度スコア（Tavilyの場合）
}
```

## 環境変数

`.env`ファイルに以下のAPIキーを設定:

```env
# Research APIs
TAVILY_API_KEY=your_tavily_key
SERPAPI_KEY=your_serpapi_key
BRAVE_SEARCH_API_KEY=your_brave_key
NEWSAPI_KEY=your_newsapi_key
PERPLEXITY_API_KEY=your_perplexity_key
```

## レート制限

| API | 制限 | 対策 |
|-----|------|------|
| Tavily | 1000 req/month (Free) | 重要クエリのみ使用 |
| SerpAPI | 100 req/month (Free) | キャッシュ活用 |
| Brave | 2000 req/month (Free) | 並列実行制限 |
| NewsAPI | 100 req/day (Free) | ニュース時のみ |
| Perplexity | 課金制 | サマリー必要時のみ |

## ベストプラクティス

1. **適切なAPI選択**: 目的に応じてAPIを選択
   - 一般検索: Tavily + Brave
   - Google結果: SerpAPI
   - ニュース: NewsAPI
   - AIサマリー: Perplexity

2. **レート制限対策**:
   - 並列リクエストは5つまで
   - リクエスト間に1秒のディレイ

3. **結果の検証**:
   - 複数ソースで情報をクロスチェック
   - 公式情報源を優先

## ファイル構成

```
packages/worker/src/research/
├── unified-research.ts      # メインモジュール
├── run-unified-research.ts  # CLI実行スクリプト
├── enhanced-research.ts     # WebSearch統合版
├── keyword-research.ts      # キーワードリサーチ
└── deep-research.ts         # 従来版（DuckDuckGo）
```

## トラブルシューティング

| 問題 | 解決策 |
|------|--------|
| APIキーエラー | `.env`ファイルを確認 |
| レート制限 | 待機時間を増やす |
| タイムアウト | タイムアウト値を増加 |
| 空の結果 | クエリを調整、別APIを試す |

## 関連スキル

- `research-cited-report`: 出典付きレポート生成
- `gpt-researcher`: 自律型深層リサーチ
- `context7-docs`: 最新ドキュメント取得
