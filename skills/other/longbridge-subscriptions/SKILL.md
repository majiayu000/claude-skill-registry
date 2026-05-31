---
name: longbridge-subscriptions
description: |
  List active real-time WebSocket subscriptions in the current Longbridge CLI session — symbols, sub_types (quote / depth / trades / brokers), candlestick periods. Diagnostic only; rarely needed in day-to-day use. Requires longbridge login. Triggers: "我订阅了哪些实时数据", "实时连接状态", "推送状态", "我訂閱了什麼", "推送狀態", "active subscriptions", "websocket subscriptions", "real-time stream status".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: account_read
  requires_login: true
  default_install: false
---

# longbridge-subscriptions

Diagnostic listing of the active real-time subscriptions in the current `longbridge` CLI session.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

`default_install: false` — not installed by default. Manual symlink only.

## When to use

- *"我现在订阅了哪些实时推送"* → run
- *"为什么没收到 NVDA 实时报价"* → diagnostic
- *"实时数据"* (ambiguous) → ask back: subscriptions vs quotes vs watchlist?

## CLI

```bash
longbridge subscriptions --format json
```

Returns an array of `{symbol, sub_types: [...], candlestick_periods: [...]}` for every active subscription in this CLI session.

## Local-only

The Longbridge MCP service is stateless HTTP — it has **no** WebSocket session concept and **no** equivalent tool. This skill requires the local `longbridge` CLI (which holds the OAuth + WebSocket session).

If `longbridge` is not installed, tell the user this skill is local-only and they need to install longbridge-terminal.

## Error handling

If `longbridge` is missing, surface the message — there is no MCP fallback. If stderr says `not logged in`, tell the user to run `longbridge auth login`.

## File layout

```
longbridge-subscriptions/
└── SKILL.md          # prompt-only, no scripts/
```
