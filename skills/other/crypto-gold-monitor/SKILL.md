---
name: crypto-gold-monitor
description: "加密货币与贵金属价格监控 / Crypto & Precious Metals Price Monitor - 监控BTC/ETH实时价格、黄金(XAU)/白银(XAG)走势，免费API无需Key"
metadata: {"marketbot":{"emoji":"🪙","requires":{"bins":["bash","curl","python3"]}}}
---

# 加密货币与贵金属价格监控 / Crypto & Precious Metals Price Monitor

实时监控比特币、以太坊、黄金、白银价格走势，支持多币种对比和价格提醒。

Real-time monitoring of Bitcoin, Ethereum, Gold, and Silver prices with multi-currency comparison.

## 功能特性 / Features

- ₿ **比特币 / Bitcoin** - 实时价格 (USD/CNY)、24h涨跌
- Ξ **以太坊 / Ethereum** - 实时价格 (USD/CNY)、24h涨跌
- 🥇 **黄金 / Gold** - XAU/USD 实时价格 (USD/CNY)
- 🥈 **白银 / Silver** - XAG/USD 实时价格 (USD/CNY)
- 💱 **汇率显示 / Exchange Rate** - 实时USD/CNY汇率

## 使用方法 / Usage

首先赋予执行权限 / First grant execution permission:

```bash
chmod +x crypto-monitor.sh
```

### 1. 查看所有价格 / View All Prices

```bash
./crypto-monitor.sh
# or
./crypto-monitor.sh all
```

### 2. 刷新频率 / Refresh Rate

```bash
# 建议通过 cron 或 watch 运行
watch -n 60 ./crypto-monitor.sh
```

## 数据来源 / Data Sources

- **CoinGecko API** (免费，无需API Key)
- **GoldAPI.io** / **Yahoo Finance**
