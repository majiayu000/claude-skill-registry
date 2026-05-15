# Gate DEX Market Skill

A market data and token information query Skill providing read-only access to on-chain public data.

## Overview

`gate-dex-market` is a Gate DEX MCP Skill built on 7 public query tools from the Gate DEX MCP Server, providing AI Agents with on-chain market data, token information, and security audit capabilities.

**Key Features:**

- All tools query public data — **no authentication required** (no `mcp_token` needed)
- Read-only operations — no on-chain writes involved
- Multi-chain support (ETH, BSC, etc.)

## Tools

| # | Tool Name | Function | Key Parameters |
|---|-----------|----------|----------------|
| 1 | `market_get_kline` | K-line data | `chain`, `token_address`, `interval`, `limit` |
| 2 | `market_get_tx_stats` | On-chain transaction statistics | `chain`, `token_address`, `period` |
| 3 | `market_get_pair_liquidity` | Trading pair liquidity | `chain`, `token_address` |
| 4 | `token_get_coin_info` | Token details | `chain`, `token_address` |
| 5 | `token_ranking` | Token rankings | `chain`, `sort_by`, `order`, `limit` |
| 6 | `token_get_coins_range_by_created_at` | New token discovery | `chain`, `start_time`, `end_time`, `limit` |
| 7 | `token_get_risk_info` | Security risk audit | `chain`, `address` |

## Workflows

| Flow | Scenario | Tools Involved |
|------|----------|----------------|
| A | View token market data | `market_get_kline` + `market_get_tx_stats` + `market_get_pair_liquidity` (parallel) |
| B | View token details | `token_get_coin_info` |
| C | Token rankings | `token_ranking` |
| D | Security audit | `token_get_risk_info` |
| E | New token discovery | `token_get_coins_range_by_created_at` |

All workflows must pass the MCP Server connection check (Step 0) before execution.

## Prerequisites

Ensure the Gate DEX MCP Server is configured in your AI coding tool before use:

```
Name: gate-dex-mcp
Type: HTTP
URL: https://your-mcp-server-domain/mcp
```

See [mcp-skills/README.md](../README.md) for detailed configuration instructions.

## File Structure

```
gate-dex-market/
├── README.md          # This file — Skill description
├── SKILL.md           # Agent instruction file (tool specs, workflows, security rules)
└── CHANGELOG.md       # Changelog
```
