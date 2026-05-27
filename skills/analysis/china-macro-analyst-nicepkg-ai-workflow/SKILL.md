---
name: china-macro-analyst
description: Analyze China macroeconomic data, PBOC monetary policy, fiscal policy, and their impact on A-share and HK stock markets. Track GDP, CPI, PPI, PMI, social financing, and interpret policy signals. Use when user asks about 中国宏观经济, 央行政策, economic data impact on markets, or needs to understand policy implications for investment.
---

# 中国宏观分析 (China Macro Analyst)

## Overview

Analyze China's macroeconomic environment, monetary policy, fiscal policy, and their implications for equity markets. Interpret key economic indicators, policy signals, and their potential impact on different sectors and investment strategies.

## Key Economic Indicators

### Growth Indicators
| Indicator | Chinese | Frequency | Release |
|-----------|---------|-----------|---------|
| GDP Growth | GDP增速 | Quarterly | ~15th of month after quarter |
| Industrial Production | 工业增加值 | Monthly | ~15th |
| Retail Sales | 社会消费品零售总额 | Monthly | ~15th |
| Fixed Asset Investment | 固定资产投资 | Monthly | ~15th |

### Price Indicators
| Indicator | Chinese | Frequency | Key Levels |
|-----------|---------|-----------|------------|
| CPI | 居民消费价格指数 | Monthly | Target ~3% |
| PPI | 工业生产者出厂价格指数 | Monthly | Deflation < 0% |
| Core CPI | 核心CPI (剔除食品能源) | Monthly | |

### Activity Indicators
| Indicator | Chinese | Frequency | Key Levels |
|-----------|---------|-----------|------------|
| Manufacturing PMI | 制造业PMI | Monthly | Expansion > 50 |
| Non-Mfg PMI | 非制造业PMI | Monthly | Expansion > 50 |
| Caixin PMI | 财新PMI | Monthly | Private sector focus |

### Financial Indicators
| Indicator | Chinese | Frequency |
|-----------|---------|-----------|
| Social Financing | 社会融资规模 | Monthly |
| M2 Growth | M2增速 | Monthly |
| New RMB Loans | 新增人民币贷款 | Monthly |
| LPR | 贷款市场报价利率 | Monthly (20th) |

### External Indicators
| Indicator | Chinese | Frequency |
|-----------|---------|-----------|
| Exports | 出口 | Monthly |
| Imports | 进口 | Monthly |
| Trade Balance | 贸易顺差 | Monthly |
| FX Reserves | 外汇储备 | Monthly |
| RMB Exchange Rate | 人民币汇率 | Daily |

## Data Sources

**Official Sources:**
- 国家统计局 (stats.gov.cn) - GDP, CPI, PPI, Industrial Production
- 中国人民银行 (pbc.gov.cn) - Monetary data, interest rates
- 海关总署 (customs.gov.cn) - Trade data
- 财政部 (mof.gov.cn) - Fiscal data

**Search Strategy:**
- "[指标名称] [月份]" e.g., "中国CPI 12月"
- "央行 [政策类型]" e.g., "央行降准"
- "[行业] 政策" e.g., "房地产政策 最新"

## Analysis Framework

### 1. Economic Data Interpretation

**GDP Analysis:**
```markdown
### GDP数据解读

| 指标 | 本期 | 上期 | 预期 | 解读 |
|-----|------|-----|------|------|
| GDP同比 | X.X% | X.X% | X.X% | 高于/低于/符合预期 |
| GDP环比 | X.X% | X.X% | | |

**分项分析:**
- 第一产业: X.X% (农业)
- 第二产业: X.X% (工业/制造业)
- 第三产业: X.X% (服务业)

**市场影响:**
[分析对股市、债市、汇率的潜在影响]
```

**Inflation Analysis:**
```markdown
### 通胀数据解读

| 指标 | 本月 | 上月 | 同比 | 环比 |
|-----|------|-----|------|------|
| CPI | | | X.X% | X.X% |
| 核心CPI | | | X.X% | |
| PPI | | | X.X% | X.X% |

**CPI分项:**
- 食品: X.X% (猪肉、蔬菜等)
- 非食品: X.X%
- 服务: X.X%
- 商品: X.X%

**PPI分项:**
- 生产资料: X.X%
- 生活资料: X.X%

**投资含义:**
- CPI上行: [对消费股、债券的影响]
- PPI上行: [对上游资源股、中游制造的影响]
- CPI-PPI剪刀差: [对利润分配的影响]
```

**PMI Analysis:**
```markdown
### PMI数据解读

| 指标 | 本月 | 上月 | 荣枯线 |
|-----|------|-----|-------|
| 制造业PMI | XX.X | XX.X | 50 |
| 非制造业PMI | XX.X | XX.X | 50 |
| 综合PMI | XX.X | XX.X | 50 |

**制造业分项:**
- 生产指数: XX.X
- 新订单指数: XX.X
- 新出口订单: XX.X
- 原材料库存: XX.X
- 从业人员: XX.X

**信号解读:**
- PMI > 50: 经济扩张
- PMI < 50: 经济收缩
- 连续X月高于/低于荣枯线
```

### 2. Monetary Policy Analysis

**PBOC Policy Tools:**
```markdown
### 货币政策工具

**利率工具:**
| 利率 | 当前 | 上次调整 | 方向 |
|-----|------|---------|------|
| 1年LPR | X.XX% | [日期] | 降/升/持平 |
| 5年LPR | X.XX% | [日期] | 降/升/持平 |
| MLF利率 | X.XX% | [日期] | |
| 逆回购利率 | X.XX% | [日期] | |
| 存款准备金率 | X.X% | [日期] | |

**数量工具:**
| 工具 | 本周操作 | 到期量 | 净投放 |
|-----|---------|-------|-------|
| 逆回购 | XXX亿 | XXX亿 | +/-XXX亿 |
| MLF | XXX亿 | XXX亿 | +/-XXX亿 |
| 国库定存 | XXX亿 | | |

**政策信号:**
[解读央行政策取向: 宽松/中性/收紧]
```

**Policy Interpretation:**
- 降准: 释放长期流动性，利好银行、地产
- 降息: 降低融资成本，利好成长股
- 结构性工具: 定向支持特定领域 (科技、绿色、小微)
- 窗口指导: 关注信贷投向变化

### 3. Fiscal Policy Analysis

**Fiscal Data:**
```markdown
### 财政数据

| 指标 | 本月 | 累计 | 同比 |
|-----|------|-----|------|
| 财政收入 | XXXX亿 | XXXX亿 | X.X% |
| 财政支出 | XXXX亿 | XXXX亿 | X.X% |
| 财政赤字 | | XXXX亿 | |

**地方债:**
- 新增专项债额度: XXXX亿
- 已发行: XXXX亿
- 发行进度: XX%

**投资方向:**
[财政支出重点领域: 基建、民生、科技等]
```

### 4. Sector Policy Analysis

**Key Policy Areas:**
```markdown
### 行业政策追踪

**房地产:**
- 限购/限贷政策变化
- 房贷利率调整
- 保交楼政策
- 房企融资政策

**科技/半导体:**
- 自主可控政策
- 科技补贴
- 出口管制应对

**新能源:**
- 新能源汽车补贴
- 光伏/风电政策
- 储能政策

**消费:**
- 促消费政策
- 消费券发放
- 家电下乡/以旧换新

**金融:**
- 金融监管政策
- 注册制改革
- 对外开放措施
```

### 5. Market Impact Assessment

**Impact Matrix:**
| Economic Event | A股影响 | 港股影响 | 受益板块 | 受损板块 |
|----------------|---------|---------|---------|---------|
| 降准 | + | + | 银行、地产 | - |
| 降息 | + | + | 成长股 | 银行 |
| CPI上行 | - | - | 消费 | 成长股 |
| PMI超预期 | + | + | 周期股 | 防御股 |
| 人民币升值 | + | + | 航空、造纸 | 出口股 |
| 人民币贬值 | - | - | 纺织出口 | 航空 |

## Output Templates

### Economic Data Report
```markdown
# [指标名称] 数据解读 [日期]

## 数据概览
[核心数据表格]

## 数据解读
[数据含义分析]

## 市场影响
- **对A股:** [影响分析]
- **对港股:** [影响分析]
- **对债市:** [影响分析]
- **对汇率:** [影响分析]

## 投资建议
- 受益板块: [列出]
- 规避板块: [列出]
- 操作建议: [具体建议]
```

### Policy Analysis Report
```markdown
# [政策名称] 政策解读

## 政策要点
1. [要点1]
2. [要点2]
3. [要点3]

## 政策背景
[出台背景分析]

## 行业影响
| 行业 | 影响程度 | 影响方向 | 分析 |
|-----|---------|---------|------|
| | 高/中/低 | 正面/负面 | |

## 相关标的
- **直接受益:** [股票列表]
- **间接受益:** [股票列表]
- **可能受损:** [股票列表]

## 投资策略
[基于政策的投资策略建议]
```

## Example Queries

**经济数据:**
- "最新CPI数据怎么解读"
- "PMI对股市有什么影响"
- "GDP增速低于预期意味着什么"
- "社融数据分析"

**货币政策:**
- "央行最近有什么政策"
- "降准对股市的影响"
- "LPR下调利好哪些板块"
- "当前货币政策取向分析"

**财政政策:**
- "专项债发行情况"
- "财政政策对基建股的影响"
- "政府工作报告解读"

**行业政策:**
- "房地产政策最新变化"
- "新能源政策分析"
- "科技自主可控相关政策"
- "促消费政策有哪些"

**综合分析:**
- "当前宏观经济形势分析"
- "政策环境对投资的影响"
- "下半年宏观展望"
