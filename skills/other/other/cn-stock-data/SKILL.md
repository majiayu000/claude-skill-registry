---
description: 中国A股/港股/美股统一数据抽象层。屏蔽 akshare/efinance/adata/pysnowball/ashare 五个数据源的 API 差异，提供统一代码格式（SH600519）、统一字段名（英文 snake_case）、智能路由和自动 Fallback。当用户需要获取股票行情、实时报价、资金流向、财务指标、北向资金等金融数据时使用此 skill。
---

# cn-stock-data 统一金融数据层

## 核心能力
- **统一代码格式**: `SH600519` / `SZ000001` / `HK00700` / `AAPL.O`，也接受纯数字 `600519`（自动推断市场）
- **统一返回字段**: 英文 snake_case（date, open, close, high, low, volume, amount, pct_change 等）
- **智能路由**: 每种数据类型有最优源优先级链，自动 fallback
- **跨市场**: 港股/美股自动路由到 pysnowball

## 数据类型 & 路由优先级
| 类型 | 命令 | 路由链 |
|------|------|--------|
| K线 | `kline` | efinance → akshare → adata → ashare → snowball |
| 实时行情 | `quote` | efinance → adata → snowball |
| 资金流向 | `fund_flow` | efinance → adata → snowball |
| 财务指标 | `finance` | adata(43字段) → akshare → snowball |
| 北向资金 | `north_flow` | adata（独占） |
| 跨市场 | 自动 | snowball（独占） |

## CLI 用法

```bash
SCRIPTS_DIR="$SKILLS_ROOT/cn-stock-data/scripts"

# K线（日/周/月/分钟）
python "$SCRIPTS_DIR/cn_stock_data.py" kline --code SH600519 --freq daily --start 2026-01-01

# 实时行情（支持多只，逗号分隔）
python "$SCRIPTS_DIR/cn_stock_data.py" quote --code SH600519,SZ000001

# 跨市场行情（自动路由到 snowball）
python "$SCRIPTS_DIR/cn_stock_data.py" quote --code HK00700,AAPL.O

# 资金流向
python "$SCRIPTS_DIR/cn_stock_data.py" fund_flow --code SZ000001

# 财务指标
python "$SCRIPTS_DIR/cn_stock_data.py" finance --code SH600519

# 北向资金
python "$SCRIPTS_DIR/cn_stock_data.py" north_flow

# 强制指定数据源
python "$SCRIPTS_DIR/cn_stock_data.py" kline --code SH600519 --source akshare

# 检查各源可用状态
python "$SCRIPTS_DIR/cn_stock_data.py" status
```

## 统一返回格式（JSON）
```json
{
  "ok": true,
  "source": "efinance",
  "fallback_used": false,
  "code": "SH600519",
  "data_type": "kline",
  "count": 30,
  "data": [
    {"date": "2026-03-14", "open": 1880.0, "close": 1895.5, "high": 1900.0, "low": 1875.0, "volume": 25000, "amount": 47000000, "pct_change": 0.82}
  ]
}
```

## 频率参数
`--freq`: daily, weekly, monthly, 1min, 5min, 15min, 30min, 60min

## 代码格式支持
| 输入 | 解析结果 |
|------|---------|
| `SH600519` | 上交所贵州茅台 |
| `SZ000001` | 深交所平安银行 |
| `600519` | 自动推断→SH600519 |
| `000001` | 自动推断→SZ000001 |
| `HK00700` | 港股腾讯 |
| `AAPL.O` | 美股苹果 |

## 编程接口（Python import）
```python
import sys; sys.path.insert(0, "$SKILLS_ROOT/cn-stock-data/scripts")
from routing import execute_with_fallback, get_available_sources

# K线
result = execute_with_fallback("kline", "get_kline", code="SH600519", freq="daily", start="2026-01-01")
if result["ok"]:
    for row in result["data"][:3]:
        print(row)

# 行情
result = execute_with_fallback("quote", "get_quote", code="SH600519", codes=["SH600519", "SZ000001"])

# 状态检查
print(get_available_sources())
```

## 注意事项
- pysnowball 的 kline/finance/fund_flow 需要 token（从 xueqiu.com cookie 获取），无 token 时自动跳过
- ashare 只支持 K 线（日/周/月/分钟），无行情/资金流/财务
- akshare K 线只支持日/周/月，不支持分钟级
- 分钟级 K 线优先用 efinance，fallback 到 ashare
