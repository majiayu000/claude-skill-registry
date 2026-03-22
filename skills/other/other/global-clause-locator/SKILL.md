---
name: global-clause-locator
description: 用于条款定位场景。适用于金融工作中的基础任务单元。
---

# global-clause-locator

## 数据来源
- 国家法律法规数据库（全国人大官方）：用于公开法律、行政法规、司法解释等检索。
- 中国证监会官网：用于上市公司监管规则、章程指引、股东会规则等公开制度文本。
- 上海证券交易所、深圳证券交易所、巨潮资讯：用于上市公司公告、章程、定期报告、治理制度等公开披露材料。
- 用户提供的公网可访问 PDF/HTML 链接，或本地公开文件。

## 功能
- 对法律条文或公司报告进行条款定位。
- 支持关键词、短句形式查询。
- 自动切分章节、条文、段落，并给出最相关片段。
- 尝试识别“第X条 / 第X章”等条款编号线索。
- 可作为上层问答、合规审核、法务检索的基础能力。

## 使用示例
```bash
python script/main.py   --source "https://www.csrc.gov.cn/csrc/c101954/c7547791/content.shtml"   --query "利润分配 现金分红"   --topk 5
```

```bash
python script/main.py   --source "./samples/company_charter.pdf"   --query "关联交易 回避表决"
```

## 交易说明
- 输入支持本地文件路径或公网可访问链接。
- 适合检索上市公司章程、制度、年报、公告，以及公开法律法规文本。
- 输出为 JSON，包括排序、相关度分数、条款线索、片段正文。
- 本 skill 用于信息检索与定位，不构成法律意见、投资建议或审计结论。

## License
MIT License. See `LICENSE`.
