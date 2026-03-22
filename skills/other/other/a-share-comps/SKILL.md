---
name: a-share-comps
description: A股可比公司分析/行业估值对标。当用户说"可比公司"、"估值对标"、"行业估值"、"comps"、"comparable company"、"同行对比"、"XX跟同行比怎么样"、"XX板块估值"、"可比公司分析"、"comps analysis"时触发。MUST USE when user asks about comparable company analysis, peer valuation comparison, or industry valuation benchmarking (comps). 通过 cn-stock-data 获取标的及可比公司的财务指标和实时行情，构建多维度估值对标表。输出 Excel（公式驱动）或 Markdown 对比表。支持投行估值表风格（formal）和快速对标表风格（brief）。
---

# A 股可比公司分析

## 数据源

```bash
SCRIPTS="$SKILLS_ROOT/cn-stock-data/scripts"

# 各公司财务指标
python "$SCRIPTS/cn_stock_data.py" finance --code [CODE]

# 各公司实时行情（市值、PE、PB 等）
python "$SCRIPTS/cn_stock_data.py" quote --code [CODE1],[CODE2],[CODE3]

# 各公司近 1 年日线（用于股价走势对比）
python "$SCRIPTS/cn_stock_data.py" kline --code [CODE] --freq daily --start [1年前日期]
```

**补充**：通过 web 搜索确认行业分类、可比公司池选择的合理性。

## Workflow

### Step 1: 确定标的与可比公司池

1. 明确标的公司（用户指定的代码/名称）
2. 确定可比公司池：
   - 用户直接给出 → 使用
   - 用户说"同行"/"行业对比" → 通过 web 搜索确认行业分类，选 5-10 家同行业上市公司
   - 选择标准：同行业、相似业务模式、相近市值规模

**可比公司选择注意事项**：
- A 股同行为主，港股/美股同行可用 cn-stock-data 跨市场获取
- 避免选择ST/*ST公司
- 标注哪些是直接可比（业务高度相似）vs 间接可比（同行业但模式不同）

### Step 2: 数据获取

对标的和每家可比公司获取：
1. `finance` — 最新财务指标（ROE、毛利率、净利率、增速等）
2. `quote` — 实时行情（市值、PE、PB）
3. 如需更多估值数据（EV/EBITDA、PS 等），需要计算：
   - EV = 市值 + 有息负债 - 现金（从财务数据估算）
   - PS = 市值 / 收入

### Step 3: 构建估值表

参见 `references/valuation-metrics.md` 的指标定义和行业处理规则。

**核心估值列（必含）**：
| 代码 | 名称 | 市值(亿) | PE(TTM) | PB | ROE(%) | 营收增速(%) | 净利润增速(%) | 毛利率(%) | 净利率(%) |

**进阶列（formal 模式）**：
| EV/EBITDA | PS | PEG | 资产负债率(%) | 经营现金流/利润 | 股息率(%) |

### Step 4: 统计分析

计算可比公司组的：
- **均值** / **中位数** / **最大值** / **最小值**
- 标的公司所处的**百分位排名**
- 标注标的哪些指标优于/低于中位数

### Step 5: 输出

**Excel 输出规则（formal 模式）：**
- 所有派生值必须是 **Excel 公式**，不是硬编码数字
- 输入数据（从 cn-stock-data 获取的原始值）用蓝色字体
- 公式计算结果用黑色字体
- 统计行（均值/中位数）用粗体
- 标的公司行用黄色底色高亮
- 包含条件格式：PE 低于中位数=绿色，高于=红色

**Markdown 输出（brief 模式）：**
- 直接输出 Markdown 表格
- 在表格下方用 1-2 句话总结标的的估值位置

## 风格说明

| 维度 | formal（投行估值表） | brief（快速对标表） |
|------|-------------------|--------------------|
| 输出格式 | Excel (.xlsx) | Markdown 表格 |
| 指标列数 | 12-15 列 | 6-8 列 |
| 统计行 | 均值+中位数+最大+最小 | 仅中位数 |
| 图表 | PE/PB 散点图数据 | 无 |
| 结论 | 客观描述估值位置 | 可加个人判断 |
| 免责声明 | 需要 | 不需要 |

## 关键规则

1. **公式优先于硬编码**：在 Excel 中，PE 不应直接写入数字，而应该是 `=市值单元格/净利润单元格`
2. **数据来源标注**：每个数字都应能追溯到 cn-stock-data 的哪个字段
3. **行业调整**：银行/保险用 PB 而非 PE；科技用 PS 或 EV/Revenue；地产看 NAV
4. **不给买卖建议**：formal 模式只陈述事实（"标的 PE 处于可比组 25 百分位"），不说"建议买入"
