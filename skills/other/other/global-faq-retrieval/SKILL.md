---
name: global-faq-retrieval
description: 用于FAQ检索场景。适用于金融工作中的基础任务单元。
---

# global-faq-retrieval

## 数据来源
- 国家法律法规数据库中的公开法条与规章。
- 证监会、上交所、深交所发布的公开监管规则、制度解释材料。
- 上市公司公开年报、半年报、公告、章程、制度文件。
- 用户提供的公网链接或本地公开文件。

## 功能
- 对法律条文或公司报告进行 FAQ 式检索。
- 用户输入自然语言问题，返回最相关的依据片段。
- 适合法务 FAQ、制度 FAQ、投研 FAQ、公司资料问答场景。
- 可作为 RAG / 智能问答的检索层组件。

## 使用示例
```bash
python script/main.py   --source "https://www.sse.com.cn/disclosure/listedinfo/announcement/"   --question "上市公司对外担保需不需要董事会审议？"
```

```bash
python script/main.py   --source "./samples/annual_report.pdf"   --question "公司核心产品主要卖给哪些客户？"
```

## 交易说明
- 输入问题越具体，返回结果越稳定。
- 结果为“答案依据片段”，不是自动生成的最终权威答复。
- 建议在上层系统中把检索片段再交给 LLM 生成最终回答。
- 本 skill 只使用公开文本，不接入企业私有数据库。

## License
MIT License. See `LICENSE`.
