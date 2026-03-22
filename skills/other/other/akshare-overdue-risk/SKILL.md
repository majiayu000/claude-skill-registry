---
name: akshare-overdue-risk
description: 用于基于AkShare数据的逾期风险识别场景。适用于金融工作中的基础任务单元。
---

# AkShare 企业逾期风险识别 Skill

## Skill 名称
**overdue-risk-enterprise**

## 功能
本 Skill 基于 **AkShare** 的 A 股公开财务数据，对单一企业进行**逾期风险识别**。默认演示企业为 **荣盛发展（002146）**，也支持替换为其他 A 股上市公司。

识别逻辑聚焦于企业最容易触发逾期或信用压力的几类公开信号：

1. **短债资金压力**：短期借款与应付票据相对货币资金的压力。
2. **经营现金流覆盖能力**：经营活动现金流对流动负债的覆盖情况。
3. **应收账款负担**：应收账款占收入比例过高时，意味着回款压力偏大。
4. **利润现金含量**：利润是否真正转化为现金流。
5. **收入变化率**：收入下滑会加大未来逾期与偿债压力。

输出结果包括：
- 企业基础信息
- 逾期风险总分（0-100，分数越高风险越高）
- 风险等级（低风险 / 中风险 / 高风险）
- 各项指标值、单项评分与解释
- 风险预警列表

---

## 数据来源
本 Skill 使用 AkShare 官方公开接口抓取数据，核心来源如下：

1. **A 股股票列表与基础匹配**
   - 接口：`stock_zh_a_spot_em`
   - 用途：将企业名称映射为股票代码，或根据代码补足企业名称。

2. **资产负债表（按报告期）**
   - 接口：`stock_balance_sheet_by_report_em`
   - 来源页：东方财富财务分析页
   - 用途：提取货币资金、短期借款、应付票据、流动负债、应收账款等科目。

3. **利润表（按报告期）**
   - 接口：`stock_profit_sheet_by_report_em`
   - 来源页：东方财富财务分析页
   - 用途：提取营业收入、净利润，并与上期对比计算收入变化率。

4. **现金流量表（按报告期）**
   - 接口：`stock_cash_flow_sheet_by_report_em`
   - 来源页：东方财富财务分析页
   - 用途：提取经营活动产生的现金流量净额，用于判断企业真实回款与偿债能力。

> 说明：本 Skill 使用的是公开披露数据，因此更适合作为**企业逾期风险初筛工具**，而不是替代尽调、评级报告或司法/征信数据。

---

## 文件结构
```text
akshare-overdue-risk-enterprise/
├── skill.md
└── script/
    ├── fetch_data.py
    ├── risk_model.py
    ├── run_demo.py
    └── requirements.txt
```

---

## 使用示例
### 1) 安装依赖
```bash
pip install -r script/requirements.txt
```

### 2) 运行默认示例（荣盛发展）
```bash
python script/run_demo.py
```

### 3) 指定企业名称
```bash
python script/run_demo.py --company 万科A
```

### 4) 指定股票代码
```bash
python script/run_demo.py --company 002146
```

### 5) 指定输出文件
```bash
python script/run_demo.py --company 荣盛发展 --output output/rongsheng_report.json
```

### 输出样例（示意）
```json
{
  "overdue_risk_score": 68.4,
  "risk_level": "中风险",
  "metrics": [
    {
      "name": "短债资金压力",
      "value": 1.3271,
      "metric_score": 25.0,
      "direction": "lower_is_better",
      "evidence": "(短期借款 + 应付票据) / 货币资金"
    }
  ],
  "warnings": [
    "短债资金压力偏弱: (短期借款 + 应付票据) / 货币资金"
  ]
}
```

---

## 交易说明
1. 本 Skill **不执行任何交易、下单、撤单或自动投资动作**。
2. 结果仅用于**识别企业公开财报中的潜在逾期/偿债压力**，适合作为投前初筛、授信辅助或舆情核查前的财务补充。
3. 若模型输出为“中风险”或“高风险”，建议进一步结合以下信息二次核验：
   - 企业公告与债务重组进展
   - 票据、债券或贷款违约事件
   - 诉讼、被执行人、限制消费等司法数据
   - 销售回款、融资渠道、再融资进展
4. 由于财报披露存在时滞，模型结果反映的是**公开报表口径下的阶段性风险特征**，不代表实时信用状态。
5. 该 Skill 输出不构成投资建议、信用评级结论或法律意见。

---

## License
### 本 Skill 代码 License
建议以 **MIT License** 方式使用和二次开发本 Skill 自带脚本。

### 第三方依赖 License
- **AkShare**：MIT License
- 其他 Python 依赖请以各自官方 License 为准

使用、分发或二次开发时，请保留第三方项目的原始版权与 License 声明。
