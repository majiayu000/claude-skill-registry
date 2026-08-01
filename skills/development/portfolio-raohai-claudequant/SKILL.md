---
name: portfolio-raohai-claudequant
description: 查看持仓概况 - 显示所有持仓股票的实时行情和涨跌幅
---

# Portfolio

查看持仓概况 - 显示所有持仓股票的实时行情和涨跌幅

## Description

获取配置的所有持仓股票的最新行情数据，以表格形式展示股票代码、名称、最新价和涨跌幅。

## Arguments

无需参数

## Dependencies

- Python 3.9+
- pandas
- akshare
- python-dotenv

## Configuration

需要在 `.env` 文件中配置：
```env
PORTFOLIO_SYMBOLS=600519,000858,601318
```

## Examples

```bash
/portfolio
```

## Output

```
📊 持仓概况

代码         名称      最新价    涨跌幅
----------------------------------------
600519.SH   贵州茅台  1650.00   +2.50%
000858.SZ   五粮液     158.60   +1.80%
601318.SH   中国平安    45.20   -0.50%
```

## Natural Language Triggers

Claude 会在以下情况自动调用此 skill：

- "查看持仓"
- "我的股票现在怎么样"
- "持仓概况"
- "当前持仓的状况是怎样的"
- "帮我看看持仓"

## Exit Codes

- `0` - 成功获取持仓数据
- `1` - 配置错误或数据获取失败

## Notes

- 股票代码会自动识别市场（沪深北）并添加后缀
- 行情数据可能有15分钟延迟
- 如果持仓列表为空，请检查 `.env` 配置
