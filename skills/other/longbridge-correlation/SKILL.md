---
name: longbridge-correlation
description: |
  Multi-asset correlation and cointegration analysis via Longbridge Securities — computes Pearson / Spearman return correlation matrix for 2–10 symbols, rolling 60-day correlation, Engle-Granger cointegration (ADF unit root), and spread half-life (AR(1) estimate). Used for portfolio decorrelation and pairs-trading pre-screening. Triggers: "相关性", "协整", "相关系数", "相关矩阵", "滚动相关", "去相关", "多标的相关", "相關性", "協整", "相關係數", "相關矩陣", "滾動相關", "去相關", "correlation", "cointegration", "correlation matrix", "rolling correlation", "Pearson", "Spearman", "decorrelation", "multi-asset correlation", "ADF test", "相关分析", "相關分析", "pairwise correlation".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
  requires_mcp: false
  tier: analysis
---

# longbridge-correlation

Computes pairwise return correlations and cointegration statistics for a basket of 2–10 symbols. Helps identify diversification opportunities, highly correlated pairs (pairs-trading candidates), and portfolio concentration risks.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- User supplies 2–10 symbols and asks for correlation analysis, whether two stocks move together, rolling correlation trends, or pairs-trading pre-screening.
- Triggers: "AAPL MSFT GOOGL 相关矩阵", "TSLA 和 NVDA 滚动相关", "correlation matrix for my watchlist", "协整检验 700.HK 5.HK".

## Workflow

1. For each symbol, fetch 252 daily candles:
   `longbridge kline <SYMBOL> --period day --count 252 --format json`
2. Align all series on `time`; drop dates missing in any series.
3. Compute daily log-returns for each symbol.
4. **Pearson correlation matrix**: pairwise Pearson correlation of returns; flag pairs with |ρ| > 0.8 (high) or < 0.2 (low).
5. **Spearman correlation** (rank-based, robust to outliers): compute alongside Pearson for comparison.
6. **Rolling 60-day correlation** for the highest-correlated pair: show trend over time.
7. **Cointegration screen** (for pairs only):
   - OLS spread residuals → ADF test → report p-value and verdict
   - Half-life = −ln(2) / OLS slope of Δspread ~ spread_{t-1}
8. Output correlation matrix heatmap description (text-based) and a summary of key relationships.

Run `longbridge kline --help` to confirm current flag names.

## CLI

```bash
longbridge kline --help

# Repeat for each symbol (2–10)
longbridge kline <SYMBOL> --period day --count 252 --format json
```

## Output

| Metric | 简体 | 繁體 | English |
|---|---|---|---|
| Pearson ρ matrix | 皮尔森相关矩阵 | 皮爾森相關矩陣 | Pearson correlation matrix |
| Spearman ρ | 斯皮尔曼相关 | 斯皮爾曼相關 | Spearman correlation |
| Rolling 60d corr | 60日滚动相关 | 60日滾動相關 | 60-day rolling correlation |
| ADF p-value | 协整 p 值 | 協整 p 值 | ADF p-value |
| Half-life | 半衰期（天） | 半衰期（天） | Half-life (days) |
| Cluster | 相关聚类 | 相關聚類 | Correlation cluster |

Present: (1) full correlation matrix table with colour coding (high ≥ 0.8 = red, low ≤ 0.2 = green); (2) rolling-correlation narrative; (3) cointegration results if relevant; (4) portfolio implication note. Cite **Longbridge Securities** / **数据来源：长桥证券** / **數據來源：長橋證券**.

## Error handling

| Situation | 简体回复 | 繁體回復 | English reply |
|---|---|---|---|
| `command not found: longbridge` | 回退到 MCP 或提示安装 longbridge-terminal | 回退到 MCP 或提示安裝 longbridge-terminal | Fall back to MCP or install longbridge-terminal |
| `not logged in` / `unauthorized` | 请运行 `longbridge auth login` | 請執行 `longbridge auth login` | Run `longbridge auth login` |
| Only 1 symbol provided | 至少需要2个标的才能计算相关性 | 至少需要2個標的 | Need at least 2 symbols |
| > 10 symbols | 最多支持10个标的，请精简列表 | 最多支持10個標的 | Max 10 symbols; please reduce list |
| Other stderr | 直接显示原始错误 | 直接顯示原始錯誤 | Surface verbatim |

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime.

## Related skills

- `longbridge-kline` — raw OHLCV data
- `longbridge-pairs-trading` — execute a pairs trade after correlation pre-screen
- `longbridge-multifactor` — factor correlation and collinearity check
- `longbridge-performance-attribution` — covariance matrix for factor decomposition

## File layout

```
longbridge-correlation/
└── SKILL.md
```
