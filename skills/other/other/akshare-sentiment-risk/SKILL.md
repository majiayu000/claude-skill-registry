---
name: akshare-sentiment-risk
description: 用于基于AkShare数据的情绪风险分析场景。适用于金融工作中的基础任务单元。
---

# AkShare 单股票舆情风险识别 Skill

## 数据来源
本 Skill 使用 AkShare 提供的数据接口来完成单只股票的舆情风险识别，核心依赖如下：

1. `stock_news_em`
   - 用途：获取个股新闻数据。
   - 典型用途：抓取指定股票相关新闻标题、发布时间、来源、链接等信息。
2. `stock_js_weibo_report`
   - 用途：获取微博舆情报告中近期受关注的股票。
   - 典型用途：将股票热度作为风险放大因子，用于辅助判断舆情传播强度。

建议安装最新版 `akshare`，因为 `stock_news_em` 在 AkShare 更新日志中多次修复，旧版本可能出现字段变化或调用失败。

## 功能
该 Skill 面向“单只股票”的舆情风险识别，功能包括：

1. 拉取指定股票的新闻数据。
2. 对新闻标题与正文进行规则化风险打分。
3. 识别监管、诉讼、违约、退市、经营异常、减持、股权冻结等高风险关键词。
4. 结合微博热度进行舆情传播强度修正。
5. 输出单篇新闻风险分数、总体风险分数、总体风险等级以及高风险新闻列表。

输出结果字段包括：

- `overall_risk_score`: 综合风险分数，范围 0~100
- `overall_risk_level`: 综合风险等级，取值 `low` / `medium` / `high`
- `article_count`: 参与分析的新闻条数
- `high_risk_count`: 高风险新闻数量
- `medium_risk_count`: 中风险新闻数量
- `weibo_hotness_rank`: 微博热度排行指数（如可获取）
- `articles`: 风险最高的新闻明细

## 使用示例
### 1. 安装依赖
```bash
pip install akshare pandas
```

### 2. 运行脚本
```bash
python script/main.py --symbol 000001 --stock-name 平安银行 --limit 50 --output result.json
```

### 3. 输出说明
脚本会在终端打印 JSON，并把完整结果保存到 `result.json`。

示例输出节选：
```json
{
  "symbol": "000001",
  "stock_name": "平安银行",
  "summary": {
    "overall_risk_score": 42.6,
    "overall_risk_level": "medium",
    "article_count": 28,
    "high_risk_count": 3,
    "medium_risk_count": 7,
    "hotness_adjustment": 4.6
  }
}
```

## 交易说明
1. 本 Skill 的目标是识别“舆情风险”，不是给出直接买卖信号。
2. 舆情风险高，并不等于股价必然下跌；舆情风险低，也不等于股价必然上涨。
3. 建议将本 Skill 作为投研、合规、风控或事件驱动策略中的辅助模块，与公告、财务、估值、资金流、行业景气度等因子联合使用。
4. 当新闻接口字段变化、数据源短时不可用、或同名股票新闻混杂时，结果可能偏离实际，需要人工复核。
5. 若用于自动化交易系统，建议增加：
   - 新闻去重与时间窗控制
   - 更细粒度情感模型
   - 公告/研报/社媒多源交叉验证
   - 人工审核阈值

## License
本 Skill 代码示例以 MIT License 提供；但底层数据来自 AkShare 及其对应上游网站。

使用者需要自行遵守：
- AkShare 项目许可证
- 上游数据源的使用条款
- 适用的证券、数据合规与研究使用规范
