---
name: claudequant
description: A股量化分析工具，提供实时行情、技术分析、资金流向和持仓分析。使用 AkShare 数据源（免费无需 Token）。当用户询问股票行情、A股分析、持仓查询、技术指标时触发此 skill。
---

# ClaudeQuant - A股持仓分析

A股量化分析工具，使用 AkShare 数据源（免费无需 Token）。

## 使用方法

```bash
cd /home/nanobot/.nanobot/workspace/skills/claudequant

# 查看持仓概况
python cli.py portfolio

# 获取实时行情
python cli.py quote <股票代码>

# 技术分析
python cli.py technical <股票代码>

# 完整分析报告
python cli.py analyze
```

## 配置持仓

编辑 `.env` 文件：
```env
PORTFOLIO_SYMBOLS=600519,000858,601318
```

## 股票代码格式

- 深圳：000001
- 上海：600519
- 北交所：430090

系统自动识别市场。
