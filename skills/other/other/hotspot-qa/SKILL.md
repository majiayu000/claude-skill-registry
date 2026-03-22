---
name: hotspot-qa
description: 面向基金品牌与内容领域的热点问答任务Skill，围绕「热点问答助手」场景提供信息抽取、结构化分析与结果输出。
---

# 热点问答助手 Skill

## 数据来源

### 1. 输入类型

- 基金公告/定期报告/招募说明书/产品说明材料
- 净值与收益时间序列、持仓与资产配置披露
- 销售/服务记录、客户反馈与问答素材(如适用)
- 合规口径与品牌内容规范(如适用)

### 2. 主要数据要素

- 品牌调性与内容规范
- 热点事件与市场数据
- 产品亮点与关键图表素材
- 受众画像与传播渠道反馈
- 合规审校规则与对外口径

### 3. 质量要求

- 输入信息尽量完整，包含时间区间、基金代码与核心指标
- 若来自 OCR/截图，请尽量校对错字与断行
- 对于未披露的数据需明确标注“缺失/待补充”

---

## 核心能力

- 围绕目标人群输出结构化内容草稿与关键卖点
- 控制语气风格与风险提示，形成可直接使用的内容模板
- 基于输入资料组织问题清单与标准回答
- 提供引用来源与口径一致性说明

---

## 输出结构

### 1. 基础字段

- skill
- domain
- scene
- input_summary
- key_findings
- data_quality
- limitations

### 2. 场景扩展模块(按需输出)

- content
- draft
- key_points
- compliance_notes
- qa
- questions
- answers
- citations

---

## 使用示例

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行脚本

```bash
python scripts/main.py --input sample.txt --output-json result.json --output-md report.md
```

### 3. 输出示例

```json
{
  "skill": "热点问答助手",
  "domain": "品牌与内容",
  "scene": "热点问答",
  "input_summary": {
    "fund_code": "000000",
    "fund_name": "示例基金",
    "period": "2024Q4",
    "data_coverage": "净值/持仓/披露/市场"
  },
  "key_findings": [
    "关键结论1",
    "关键结论2"
  ],
  "data_quality": {
    "has_text": true,
    "text_length": 1200
  },
  "limitations": [
    "仅基于输入信息形成初步判断"
  ]
}
```

---

## 注意事项与限制

- 仅对输入文本进行结构化与初步判断，不替代人工投研或合规结论
- 若缺少关键数据(持仓、基准、时间区间)，结果需明确提示不完整
- 输出建议应结合实际业务口径与监管要求复核

---

## 适用场景

- 业务条线: 品牌与内容
- 场景/能力: 热点问答
- 典型用户: 研究员、产品经理、渠道与客服、合规审查或内容运营人员

---

## License

- 代码部分遵循 MIT License
- 数据来源与披露口径需遵循对应数据供应商与监管要求
