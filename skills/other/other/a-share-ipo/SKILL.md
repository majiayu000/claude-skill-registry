---
name: a-share-ipo
description: A股IPO/新股分析。当用户说"IPO"、"新股"、"打新"、"上市"、"申购"、"新股分析"、"XX要上市了"、"最近有什么新股"、"新股值不值得打"、"注册制"时触发。基于 akshare 新股数据和 cn-stock-data 行情数据，分析新股基本面、发行定价、首日表现预测、打新策略。支持研报风格（formal）和快速解读风格（brief）。
---

# A股 IPO / 新股分析助手

## Data Sources

```bash
SCRIPTS="$SKILLS_ROOT/cn-stock-data/scripts"

# 新股申购信息（akshare）
python -c "import akshare as ak; df=ak.stock_xgsglb_em(symbol='全部股票'); print(df.head(10).to_json(orient='records', force_ascii=False))"

# 新股上市后行情
python "$SCRIPTS/cn_stock_data.py" kline --code [CODE] --freq daily --start [上市日期]

# 新股财务数据
python "$SCRIPTS/cn_stock_data.py" finance --code [CODE]

# 同行业公司行情（估值对标）
python "$SCRIPTS/cn_stock_data.py" quote --code [可比公司代码]
```

补充：通过 web 搜索获取招股说明书摘要、发行定价分析、机构报价等。

## Workflow

### Step 1 — 确定分析模式
| 模式 | 触发词 | 重点 |
|------|--------|------|
| 即将申购 | "打新""申购""值不值得打" | 发行定价合理性、中签率预估、申购建议 |
| 已上市追踪 | "上市表现""新股走势" | 首日/首周表现、开板预测、持有建议 |
| 打新策略 | "最近新股""打新策略" | 批量筛选、资金分配、收益测算 |

### Step 2 — 数据获取
1. 调用 `stock_xgsglb_em` 获取新股列表（发行价、发行PE、中签率、申购代码）
2. 获取可比公司行情与估值数据（同行业已上市公司）
3. 如已上市，拉取上市后 K 线行情

### Step 3 — 基本面分析
- 行业定位与主营业务
- 核心财务指标：营收增速、净利润率、ROE、资产负债率
- 竞争优势与风险因素
- 募资用途合理性

### Step 4 — 估值分析
- 发行 PE vs 行业平均 PE（溢价/折价率）
- 可比公司法：选 3-5 家同业，对比 PE/PB/PS
- 发行价合理性评级：低估 / 合理 / 偏高 / 高估
- 破发概率定性判断

### Step 5 — 输出
**formal 模式**：完整研报格式，含数据表格、估值对标、风险提示
**brief 模式**：一句话结论 + 核心数据 + 操作建议

## Rules

1. **注册制破发常态化** — 不可默认"新股必赚"，必须做估值分析后给结论
2. **打新门槛差异**：
   - 沪市主板：持有沪市市值 ≥1万元（每万元1个申购单位）
   - 深市主板/创业板：持有深市市值 ≥1万元（每5000元1个申购单位）
   - 科创板：需开通权限（≥50万资产 + 2年交易经验）
   - 创业板：需开通权限（≥10万资产 + 2年交易经验）
   - 北交所：需开通权限（≥50万资产 + 2年交易经验）
3. **上市前5日无涨跌幅限制**（科创板/创业板/北交所），主板仍有44%首日涨幅限制
4. **弃购后果** — 连续12个月内累计弃购3次，将被列入限制名单6个月
5. **数据时效** — 新股数据变化快，分析时标注数据获取时间
6. **风险提示** — 每次输出末尾必须包含风险提示

## Reference

详见 [references/ipo-guide.md](references/ipo-guide.md)
