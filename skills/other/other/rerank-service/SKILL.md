---
name: rerank-service
description: 文档重排序服务（Reranker）。基于深度学习模型对检索候选结果进行细粒度相关性打分与重新排序，显著提升检索结果的精准度（Top-K 准确率）。
---

## 功能
根据查询语句对候选文档进行相关性评分和排序，提升检索准确性。

## 调用方式
```python
from services.rerank_service.client import RerankServiceClient

client = RerankServiceClient()

query = "什么是机器学习？"
documents = [
    "机器学习是人工智能的一个分支，通过数据训练模型。",
    "今天天气很好，适合出去散步。",
    "深度学习是机器学习的子领域，使用神经网络。"
]

# 完整重排序结果
result = client.rerank(query, documents, top_n=2)

# 简化结果：(索引, 分数, 文档) 元组列表
ranked = client.rerank_documents(query, documents, top_n=2)

# 只获取最相关的文档索引
indices = client.get_top_indices(query, documents, top_n=2)  # -> [0, 2]
```

## 返回格式
```json
{
  "id": "rerank-xxx",
  "model": "BAAI/bge-reranker-v2-m3",
  "results": [
    {
      "index": 0,
      "document": {"text": "机器学习是人工智能的一个分支..."},
      "relevance_score": 0.999
    },
    {
      "index": 2,
      "document": {"text": "深度学习是机器学习的子领域..."},
      "relevance_score": 0.098
    }
  ]
}
```
