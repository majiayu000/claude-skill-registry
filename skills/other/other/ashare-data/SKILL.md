---
name: ashare-data
description: "Ashare 最轻量 A 股行情获取工具（3.2k Stars），基于新浪+腾讯双核心数据源，零依赖（仅需 requests+pandas），无需注册，支持日/周/月线及 1m/5m/15m/30m/60m 分钟级K线。当用户需要快速获取 A 股/指数行情而其他数据源不可用时，Ashare 是最可靠的回退方案——它使用新浪为主、腾讯为备的双核心架构，自动切换，极少出错。"
---

# Ashare 轻量行情数据工具

## 定位

Ashare 是 GitHub 上 3.2k Stars 的极简 A 股行情库，**单文件、零配置、零注册**。核心只有一个函数 `get_price()`，用新浪+腾讯双数据源自动切换，稳定性极高。

它的价值不在于数据丰富度（只有行情K线），而在于**可靠性**——当 akshare、efinance、adata 因为上游网站改版或反爬而暂时不可用时，Ashare 几乎总是能正常工作。

## 依赖

```bash
pip install requests pandas
```

无需安装额外包，requests 和 pandas 通常已存在于 Python 环境中。

## 使用

唯一脚本：`scripts/quote_data.py`

### 单只股票行情

```bash
# 日线（最近30天）
python quote_data.py quote --code sh000001 --count 30

# 周线
python quote_data.py quote --code sh600519 --freq 1w --count 20

# 月线
python quote_data.py quote --code sz000001 --freq 1M --count 12

# 5分钟线
python quote_data.py quote --code sh600519 --freq 5m --count 48

# 指定结束日期
python quote_data.py quote --code sh600519 --freq 1d --count 60 --end 2026-01-31
```

### 批量获取

```bash
python quote_data.py multi --code sh600519,sz000001,sh000300 --count 10
```

### 代码格式

| 格式 | 说明 | 示例 |
|------|------|------|
| sh + 代码 | 上海证券交易所 | sh600519（茅台）、sh000001（上证指数） |
| sz + 代码 | 深圳证券交易所 | sz000001（平安银行） |
| 代码.XSHG | JoinQuant 格式（沪） | 000001.XSHG |
| 代码.XSHE | JoinQuant 格式（深） | 000001.XSHE |

### 支持的周期

| 周期 | 参数 | 数据源 |
|------|------|--------|
| 日线 | 1d | 新浪（主）→ 腾讯（备） |
| 周线 | 1w | 新浪（主）→ 腾讯（备） |
| 月线 | 1M | 新浪（主）→ 腾讯（备） |
| 1分钟 | 1m | 腾讯（独占） |
| 5分钟 | 5m | 新浪（主）→ 腾讯（备） |
| 15分钟 | 15m | 新浪（主）→ 腾讯（备） |
| 30分钟 | 30m | 新浪（主）→ 腾讯（备） |
| 60分钟 | 60m | 新浪（主）→ 腾讯（备） |

### 返回字段

time, open, close, high, low, volume（前复权）

## 与其他数据源的关系

Ashare **只做行情K线**，没有财务、资金流、北向资金等数据。它的定位是：

- **行情获取的最终回退方案**：当其他源全部不可用时，Ashare 大概率还能工作
- **最快的行情查询**：单文件、零配置、响应快
- **分钟级K线的补充源**：1m 数据只有腾讯有，Ashare 是获取它的最简方式

使用优先级建议：
1. 先尝试 efinance-data / akshare-finance（数据最全）
2. 如果挂了，尝试 adata-source
3. 如果还挂了，用 ashare-data（几乎不会挂）

## 注意事项

1. 数据来源为新浪财经和腾讯财经公开接口
2. 返回数据为前复权（qfq）
3. 非交易时段返回最近交易日数据
4. count 参数控制返回K线根数，不是天数
