---
name: a-share-concept
description: A股概念板块/题材分析/热点概念追踪。当用户说"概念板块"、"题材"、"热点板块"、"概念股"、"XX概念"、"AI概念"、"新能源概念"、"XX板块有哪些股票"、"今天什么板块涨了"、"风口"、"概念板块分析"、"热点题材"时触发。MUST USE when user asks about concept/thematic sectors, hot topics, or which concept boards are trending in A-shares. 基于 adata 概念板块数据和 cn-stock-data 行情数据，分析概念板块构成、走势、龙头股、资金流向。支持研报风格（formal）和快速解读风格（brief）。
---

# A股概念板块/题材分析

## 数据源

```bash
SCRIPTS="$SKILLS_ROOT/cn-stock-data/scripts"

# 概念板块列表（adata）
python -c "import adata; df=adata.stock.info.concept_constituent(wait_time=0); print(df.head(20).to_json(orient='records', force_ascii=False))"

# 概念板块成分股（adata，需指定 concept_code）
python -c "import adata; df=adata.stock.info.concept_constituent(concept_code='BK0655'); print(df.to_json(orient='records', force_ascii=False))"

# 成分股行情
python "$SCRIPTS/cn_stock_data.py" quote --code [CODE1],[CODE2],...

# 成分股K线
python "$SCRIPTS/cn_stock_data.py" kline --code [CODE] --freq daily --start [日期]

# 成分股资金流向
python "$SCRIPTS/cn_stock_data.py" fund_flow --code [CODE]
```

补充：通过 web 搜索获取概念板块热度、新闻催化剂、政策驱动因素。

## Workflow

1. **确定分析对象**：指定概念板块 / 今日热门概念 / 概念对比
2. **数据获取**：概念成分股列表 + 各股行情 + 资金流向
3. **板块分析**：
   - 整体表现（涨跌幅、成交额、换手率）
   - 龙头股识别（市值最大 / 涨幅最大 / 资金流入最多）
   - 板块内分化程度（涨跌比、标准差）
4. **驱动因素分析**：
   - 政策驱动（政策文件、会议精神）
   - 事件驱动（技术突破、订单落地）
   - 资金驱动（游资炒作、机构加仓）
5. **输出**：按用户偏好输出 formal（研报风格）或 brief（快速解读）

## 关键规则

1. 概念板块与行业板块不同：一只股票可属于多个概念
2. 题材炒作往往短期性强，需区分"长期逻辑"和"短期炒作"
3. 概念板块数据来源不统一（东财/同花顺/adata 分类可能不同），以 adata 为准
4. 龙头股判断标准：最先涨停 + 成交量最大 + 市值辨识度最高

## 参考资料

- [概念板块分析指南](references/concept-guide.md)
