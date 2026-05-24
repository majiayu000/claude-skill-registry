---
name: gpt-researcher
description: Use this skill for comprehensive research tasks requiring deep investigation, multiple source validation, and citation-backed reports. Triggers on keywords like "research", "investigate", "deep dive", "comprehensive analysis", "literature review", or when needing validated, sourced information.
---

# GPT Researcher - Autonomous Deep Research

This skill enables autonomous deep research that explores and validates numerous sources, generating comprehensive reports with citations.

## Problem Solved

Standard web search tools:
- Return raw results requiring manual filtering
- Often contain irrelevant sources
- Waste context window space
- Require manual source validation

GPT Researcher:
- Autonomously explores hundreds of sources
- Validates and filters for relevance
- Generates structured reports with citations
- Focuses on trusted, up-to-date information

## When to Use

- Comprehensive research on any topic
- Market analysis and competitive research
- Technical deep dives
- Literature reviews
- Fact-checking and source validation
- Generating research reports

## Available Tools

### 1. deep_research
Performs thorough, comprehensive research on a topic.

```
Input: "AIエージェントフレームワークの2026年トレンド"
Output: 詳細な調査レポート（複数ソース、引用付き）
```

### 2. quick_search
Fast web search optimized for speed over comprehensiveness.

```
Input: "Next.js 15 release date"
Output: 簡潔な検索結果
```

### 3. write_report
Generates a structured report from research results.

### 4. get_research_sources
Retrieves the list of sources used in research.

### 5. get_research_context
Accesses the full context of completed research.

## Example Usage

### Comprehensive Research

```
User: AIコーディングエージェントの最新動向を調査して

AI: [Calls deep_research]
    [Explores 50+ sources]
    [Validates and filters relevant information]
    [Generates report with citations]

Output:
# AIコーディングエージェント 2026年動向レポート

## エグゼクティブサマリー
...

## 主要プレイヤー分析
1. Claude Code [Source: Anthropic Blog]
2. Cursor [Source: TechCrunch]
3. Windsurf [Source: Verge]
...

## 引用
[1] https://...
[2] https://...
```

### Quick Fact Check

```
User: LangGraphの最新バージョンは？

AI: [Calls quick_search]
    [Returns fast result]
```

### Market Research

```
User: 予測市場プラットフォームの競合分析をして

AI: [Calls deep_research with market analysis focus]
    [Analyzes competitors]
    [Compares features, pricing, market share]
    [Generates competitive analysis report]
```

## Required Environment Variables

GPT Researcher requires these API keys:

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for LLM | Yes |
| `TAVILY_API_KEY` | Tavily API key for web search | Yes |

## Setup

1. Set environment variables in your shell:
   ```bash
   export OPENAI_API_KEY="your-key"
   export TAVILY_API_KEY="your-key"
   ```

2. Or add to `.env` file in project root

## Research Quality

GPT Researcher outperforms other research tools:

| Tool | Citation Quality | Information Coverage |
|------|-----------------|---------------------|
| Perplexity | Medium | Medium |
| OpenAI Deep Research | High | High |
| **GPT Researcher** | **Highest** | **Highest** |

*Based on Carnegie Mellon University's DeepResearchGym benchmark (May 2025)*

## Best Practices

1. **Be specific with research queries**
   ```
   ❌ "AIについて調べて"
   ✅ "2026年のAIエージェントフレームワーク市場規模と主要プレイヤー"
   ```

2. **Use for substantial research tasks**
   - Simple facts → Context7 or quick_search
   - Deep investigation → deep_research

3. **Request specific output formats**
   ```
   「競合分析レポートを表形式で作成して」
   「SWOT分析を含めて」
   ```

4. **Combine with other tools**
   - Context7 for documentation
   - GPT Researcher for market/trend analysis

## Integration with TAISUN

GPT Researcher is automatically available via MCP. The system will:
1. Detect research-related queries
2. Select appropriate tool (deep_research or quick_search)
3. Validate and synthesize sources
4. Return comprehensive, cited results

## Source

- [GPT Researcher GitHub](https://github.com/assafelovic/gpt-researcher)
- [GPTR MCP Server](https://github.com/assafelovic/gptr-mcp)
- [Documentation](https://docs.gptr.dev/)
