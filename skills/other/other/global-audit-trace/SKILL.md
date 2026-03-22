---
name: global-audit-trace
description: 用于审计追踪场景。适用于金融工作中的基础任务单元。
---

# Global Audit Trace Check Skill

## 名称
Global Audit Trace Check

## 简介
本 Skill 使用公网可查的法律法规、交易所规则、上市公司公告与定期报告，对某个上市企业执行“留痕与审计校验”。

它的目标不是替代法律意见、审计意见或交易所监管判断，而是为风控、合规、内审、投研或审阅团队提供一个可复核的自动化核验框架：
- 先查询与校验目标相关的法律法规与自律规则；
- 再抓取上市公司公开披露材料；
- 最后输出带来源 URL、抓取时间、文本哈希、命中规则、风险等级的留痕化结果。

---

## 数据来源
本 Skill 仅使用公网可查数据，优先使用官方来源：

### 1. 法律法规 / 监管规则
- 中国证监会：上市公司信息披露管理办法、行政规章、规范性文件
- 全国人大 / 中国政府公开法源：公司法、证券法等
- 上海证券交易所：股票上市规则、自律监管指引、规范运作规则
- 深圳证券交易所：股票上市规则、自律监管指引、信息披露事务管理相关规则
- 财政部 / 企业内部控制规范体系相关公开资料（可按需扩展）

### 2. 上市公司公开披露材料
- 巨潮资讯（CNINFO）静态公告 PDF 链接
- 上海证券交易所上市公司公开页面
- 深圳证券交易所上市公司公开页面
- 上市公司官网中的公司治理、投资者关系、制度文件、联系方式页面

### 3. 典型可校验文档类型
- 年度报告 / 半年度报告 / 季度报告
- 审计报告
- 内部控制自我评价报告
- 内部控制审计报告
- 董事会、监事会、股东大会决议公告
- 信息披露管理制度、内幕信息知情人登记制度、内部审计制度等制度文件

---

## 功能

### 1. 法律法规查询
输入关键词后，从官方监管与法源网站抓取相关规则，并返回：
- 标题
- 发布机构
- 来源 URL
- 生效或发布时间（若可提取）
- 与“留痕”“审计”“信息披露”“内部控制”相关的命中摘要

### 2. 企业公开资料抓取
根据企业名称、证券代码及外部 URL，抓取上市企业公开资料并抽取关键字段，例如：
- 公司名称
- 证券代码
- 交易所
- 法定代表人
- 董事会秘书
- 办公地址
- 联系电话 / 邮箱
- 审计机构名称
- 审计意见类型
- 内控评价结论
- 制度文件是否存在
- 决议公告是否可检索

### 3. 留痕校验
为每一次抓取和判断生成可复核留痕：
- source_url
- fetched_at
- sha256
- parser
- matched_rule_ids
- evidence_snippet

### 4. 审计校验
基于公开披露内容执行规则校验，默认包含以下维度：
- 是否存在审计报告或年度审计信息
- 是否存在内部控制自我评价报告
- 是否披露审计机构或审计意见类型
- 是否可识别董事会 / 审计委员会 / 内审相关表述
- 是否存在信息披露管理制度或内部审计制度线索
- 关键字段在不同材料之间是否出现明显冲突

### 5. 风险分级输出
输出 LOW / MEDIUM / HIGH 风险等级，并按条目展示：
- 校验项目
- 规则依据
- 结果
- 证据
- 风险等级
- 备注

---

## 使用示例

### 1. 查询法规
```bash
python script/fetch_regulations.py --keyword 信息披露 审计 留痕 --max-items 10 --output data/regulations.json
```

### 2. 抓取某上市企业公开资料
```bash
python script/fetch_company_profile.py \
  --company-name 上海悦心健康集团股份有限公司 \
  --stock-code 002162 \
  --annual-report-url https://static.cninfo.com.cn/finalpage/2025-08-26/d139527a-8b5b-409a-b051-13c688736fec.PDF \
  --company-site https://www.cimic.com \
  --output data/company_profile.json
```

### 3. 进行留痕与审计校验
```bash
python script/check_audit_trace.py \
  --company-json data/company_profile.json \
  --regulations-json data/regulations.json \
  --output data/audit_trace_result.json
```

### 4. 一键运行演示
```bash
python script/run_demo.py
```

---

## 交易说明
1. 本 Skill 不直接连接券商交易系统、OMS、EMS 或下单接口。
2. 本 Skill 不产生买卖建议，不构成投资建议、法律意见或审计鉴证意见。
3. 本 Skill 输出仅基于公开可查资料，适合作为：
   - 合规预筛查
   - 信息披露一致性复核
   - 尽调辅助
   - 风险提示线索生成
4. 若将本 Skill 用于投研、风控或审批流程，建议由人工复核：
   - 法规适用范围
   - 文档版本有效性
   - 公告发布时间先后顺序
   - 具体事实与监管口径
5. 当公开网页结构变化、PDF 无法解析或公司披露口径不统一时，可能出现漏检或误检。

---

## License
本 Skill 代码示例采用 MIT License 发布。

说明：
- Skill 自身代码使用 MIT License；
- 第三方公开网站内容、公告 PDF、法律法规正文版权归原发布机构或权利人所有；
- 使用者应遵守目标网站 robots、服务条款、版权及合规要求。

---

## 输出结果示例
```json
{
  "company": "上海悦心健康集团股份有限公司",
  "stock_code": "002162",
  "overall_risk": "MEDIUM",
  "checks": [
    {
      "check_name": "内部控制评价报告存在性",
      "status": "pass",
      "risk_level": "LOW",
      "matched_rule_ids": ["DISCLOSURE-001", "AUDIT-002"],
      "evidence": "在年报或相关公告中识别到‘内部控制自我评价报告’字样"
    },
    {
      "check_name": "审计机构字段一致性",
      "status": "warning",
      "risk_level": "MEDIUM",
      "matched_rule_ids": ["DISCLOSURE-002"],
      "evidence": "不同文档中审计机构表述不完全一致，建议人工复核"
    }
  ],
  "trace": [
    {
      "source_url": "https://static.cninfo.com.cn/...PDF",
      "fetched_at": "2026-03-13T10:00:00Z",
      "sha256": "..."
    }
  ]
}
```
