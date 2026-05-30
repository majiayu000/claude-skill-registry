---
name: longbridge-chanlun
description: |
  缠论形态识别——自动检测顶底分型、笔（上升笔/下降笔）、线段、中枢，生成一买/二买/三买/一卖/二卖/三卖信号。依赖 czsc 库。Triggers: "缠论", "分型", "笔", "中枢", "线段", "一买", "二买", "三买", "一卖", "二卖", "三卖", "缠中说禅", "缠师", "纏論", "分型", "筆", "中樞", "線段", "一買", "二買", "三買", "一賣", "二賣", "三賣", "chanlun", "chan theory", "bi", "zhongshu", "buy point", "sell point", "fractal top bottom", "Chan theory".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
  requires_mcp: false
  tier: read
---

# longbridge-chanlun

缠论（Chan Theory）形态识别引擎：基于 OHLCV 日线数据，自动检测顶底分型、笔、线段、中枢，并生成一买/一卖、二买/二卖、三买/三卖信号。

## Requirements

> ⚠️ **额外依赖 / Extra dependency required**
>
> 此 skill 依赖第三方 Python 库 **czsc**，使用前需手动安装：
>
> ```bash
> pip install czsc
> ```
>
> 若环境无法安装，LLM 将回退到手动实现基础分型逻辑（精度较低）。
> This skill requires the **czsc** Python library. Install it before use: `pip install czsc`

> **Response language**: match the user's input language —
> Simplified Chinese / Traditional Chinese / English.

## When to use

- 用户询问缠论相关分析：*"AAPL.US 缠论分析"*、*"700.HK 现在在哪个买点"*、*"帮我看看 TSLA 的中枢"*
- 识别分型（顶分型/底分型）、笔（上升笔/下降笔）、线段结构
- 判断当前买卖点类型（一买/二买/三买/一卖/二卖/三卖）
- 用户提到"缠中说禅"、"缠师"、"缠论买点"等关键词

## Workflow

1. 从用户输入提取标的代码，标准化为 `<CODE>.<MARKET>` 格式。
2. 获取日线 OHLCV 数据（300 根 K 线）：
   ```bash
   longbridge kline <SYMBOL> --period day --count 300 --format json
   ```
3. 将 JSON 数据转换为 czsc 所需的 `RawBar` 列表格式（字段：`dt`, `open`, `high`, `low`, `close`, `vol`）。
4. 使用 czsc 库解析缠论结构：
   ```python
   import czsc
   from czsc import CZSC
   # bars: list of czsc.RawBar
   c = CZSC(bars)
   # 分型: c.fx_list
   # 笔: c.bi_list
   # 线段: c.seg_list (if available)
   # 中枢: c.zs_list (if available)
   ```
5. 读取最近的笔序列和中枢，匹配买卖点逻辑：
   - **一买**：下降笔触及中枢下沿后出现底分型
   - **二买**：中枢震荡后上升笔回撤不破中枢低点出现底分型
   - **三买**：突破中枢上沿后回调不破中枢高点出现底分型
   - 卖点逻辑对称（一卖/二卖/三卖）
6. 输出分析结论：当前所处买卖点、最近中枢区间、最近分型位置。

> 若环境未安装 czsc，提示用户先运行 `pip install czsc`，然后重试。
> 若不确定 CLI 参数，先运行 `longbridge kline --help` 查看最新参数。

## CLI

```bash
# 获取日线数据（主要数据源）
longbridge kline AAPL.US --period day --count 300 --format json

# 若需更短周期辅助判断（可选）
longbridge kline 700.HK --period week --count 100 --format json
```

## Output

以自然语言呈现，包含：

- **当前买卖点**：一买 / 二买 / 三买 / 一卖 / 二卖 / 三卖（或"暂无明确信号"）
- **最近中枢区间**：[中枢低点, 中枢高点]（含价格）
- **最近分型**：类型（顶/底）+ 价格 + 日期
- **最近笔**：方向（上升/下降）+ 起止价格
- **数据来源**：Longbridge Securities / 数据来源：长桥证券 / 數據來源：長橋證券

## Error handling

| 情形 | 简体回复 | 繁體回覆 / English |
|---|---|---|
| `command not found: longbridge` | 尝试 MCP fallback；否则请安装 longbridge-terminal | 嘗試 MCP fallback；否則請安裝 longbridge-terminal / Try MCP fallback; otherwise install longbridge-terminal |
| stderr 含 `not logged in` | 请运行 `longbridge auth login` | 請運行 `longbridge auth login` / Run `longbridge auth login` |
| Python 环境缺少 czsc | 请运行 `pip install czsc` 后重试 | 請運行 `pip install czsc` 後重試 / Run `pip install czsc` then retry |
| czsc 版本不兼容 | 请运行 `pip install --upgrade czsc` | 請運行 `pip install --upgrade czsc` / Run `pip install --upgrade czsc` |
| 其他 stderr | 原样返回错误，不静默重试 | 原樣返回錯誤，不靜默重試 / Surface verbatim, never retry silently |

## MCP fallback

若 CLI 不可用且已配置 MCP：

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

## Related skills

| 用户询问 | 路由至 |
|---|---|
| 实时股价/行情 | `longbridge-quote` |
| K线图/历史价格 | `longbridge-kline` |
| 艾略特波浪 | `longbridge-elliott` |
| 谐波形态 | `longbridge-harmonic` |
| 聪明钱/SMC | `longbridge-smc` |
| 资金流向 | `longbridge-capital-flow` |

## File layout

```
longbridge-chanlun/
└── SKILL.md
```
