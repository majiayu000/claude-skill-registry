---
name: akshare-customer-churn
description: 用于基于AkShare数据接口的单企业客户流失风险识别场景。适用于金融工作中的基础任务单元。
---

# AkShare 单企业客户流失风险识别 Skill

## 数据来源
本 Skill 基于 AkShare 的公开数据接口，对“某一个企业（通常对应 A 股上市公司）”做客户流失风险识别。核心数据源如下：

1. `stock_financial_abstract` / `stock_financial_abstract_ths`
   - 用途：获取企业财务摘要。
   - 用于提取营业收入同比等经营指标，识别客户需求走弱、收入增速放缓等风险。

2. `stock_financial_analysis_indicator` / `stock_financial_analysis_indicator_em`
   - 用途：获取财务分析指标。
   - 用于提取销售毛利率、应收账款周转率、存货周转率、经营现金流质量等代理指标。

3. `stock_zygc_ym` / `stock_zygc_em`
   - 用途：获取主营构成数据。
   - 用于识别收入结构是否过度集中，判断企业对单一产品、区域或客户群体的依赖风险。

4. `stock_mda_ym`
   - 用途：获取管理层讨论与分析文本。
   - 用于识别管理层是否披露客户集中、订单压力、续费下降、竞争加剧、渠道变化等信号。

5. `stock_news_em`
   - 用途：获取企业相关公开新闻。
   - 用于识别大客户流失、合作终止、订单减少、退货、投诉、渠道退出等事件风险。

> 说明：AkShare 主要聚合公开市场与公开披露数据，并不直接提供企业内部客户名单或真实 churn 标签。因此本 Skill 识别的是“客户流失风险代理信号”，不是企业 CRM 里的真实客户流失率。

## 功能
该 Skill 面向单一企业的客户流失风险预警，主要功能包括：

1. 自动拉取企业公开财务、主营构成、管理层讨论与相关新闻数据。
2. 通过规则引擎识别收入增速放缓、毛利率下滑、应收账款周转恶化、存货周转变差、经营现金流质量下降等风险。
3. 结合主营构成数据识别收入结构过度集中带来的客户依赖风险。
4. 对管理层讨论与新闻文本执行关键词检索，识别客户流失、合作终止、订单减少、续费下降、需求疲软、渠道退出等信号。
5. 输出综合风险分数、风险等级、命中规则条目、证据摘要，以及 Markdown 报告与 JSON 结果。

输出核心字段包括：

- `overall_risk_score`: 综合风险分数，范围 0~100
- `overall_risk_level`: 综合风险等级，取值 `low` / `medium` / `high`
- `rule_hit_count`: 命中规则数量
- `risk_items`: 风险条目明细
- `data_status`: 各类数据实际拉取情况
- `disclaimer`: 方法说明与边界提醒

## 使用示例
### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行脚本
```bash
python script/main.py --symbol 600519 --company-name 贵州茅台 \
  --output-json result.json \
  --output-md report.md
```

### 3. 输出结果
脚本会：

- 在终端打印完整 JSON 结果
- 生成 `result.json`
- 生成 `report.md`

输出示例节选：
```json
{
  "symbol": "600519",
  "company_name": "贵州茅台",
  "summary": {
    "overall_risk_score": 36.0,
    "overall_risk_level": "low",
    "high_risk_count": 0,
    "medium_risk_count": 3,
    "low_risk_count": 1,
    "rule_hit_count": 4
  }
}
```

## 交易说明
1. 本 Skill 用于识别“客户流失风险代理信号”，不是买卖点模型，也不是违约预测或审计结论。
2. 风险分数高，表示企业可能存在客户稳定性、续费能力、订单质量、渠道健康度方面的压力，但并不直接等同于财务造假、经营危机或股价下跌。
3. 风险分数低，也不代表企业一定不存在真实流失风险；公开数据通常滞后于企业内部 CRM 和订单系统。
4. 若你将该 Skill 用于投研或交易，请至少结合以下信息二次验证：
   - 企业内部客户数、留存率、复购率、续费率
   - 客诉、退货、退款与服务 SLA 数据
   - 大客户合同续签情况
   - 订单金额、回款周期与区域渠道变化
5. 若用于自动化策略，建议加入：
   - 时间窗与行业对比
   - 企业内部真实 churn 标签
   - 更细粒度的 NLP 模型
   - 人工复核阈值与异常回溯机制

## License
本 Skill 的代码部分以 MIT License 提供；但底层数据来自 AkShare 及其上游公开网站。

使用者需要自行遵守：

- AkShare 项目许可证与使用约定
- 各上游网站与公开数据源的使用条款
- 所在地区关于数据抓取、研究使用、信息披露与交易合规的要求
