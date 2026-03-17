---
name: deepsearch-service
description: 基于 LLM 的深度迭代搜索与推理服务。擅长处理复杂问题，通过自动分解查询、多轮迭代检索、信息评估与验证，最终生成全面且结构化的深度分析报告。
---

## 功能
基于 LLM 的迭代式深度搜索服务，能够：
1. 将复杂问题分解为多个子查询
2. 迭代搜索收集多源信息
3. 评估信息充分性，动态调整搜索策略
4. 综合生成结构化分析报告

## 适用场景
- 复杂问题需要多角度分析
- 需要综合多个来源的信息
- 要求生成完整的研究报告

## 调用方式
```python
from services.deepsearch_service.client import DeepSearchClient

client = DeepSearchClient()

# 健康检查
status = client.health_check()

# 深度搜索（默认参数）
result = client.search("Python异步编程的最佳实践有哪些？")

# 自定义参数
result = client.search(
    query="如何设计一个高可用的微服务架构？",
    max_iterations=3,          # 最大迭代次数 (1-5)
    queries_per_iteration=3,   # 每轮查询数 (1-5)
    depth_level="deep"         # 搜索深度: quick/normal/deep
)

# 获取报告和来源
print(result["report"])
for source in result["sources"]:
    print(f"- {source['title']}: {source['url']}")
```

## 返回格式
```json
{
  "query": "Python异步编程的最佳实践有哪些？",
  "report": "# Python异步编程最佳实践\n\n## 1. 核心概念...",
  "sources": [
    {
      "title": "Python官方asyncio文档",
      "url": "https://docs.python.org/...",
      "relevance": 0.95,
      "snippet": "asyncio是Python标准库中的异步I/O框架..."
    }
  ],
  "iterations": [
    {
      "iteration": 1,
      "queries": ["Python asyncio 教程", "async await 用法"],
      "results_count": 6,
      "key_findings": ["asyncio是标准库组件"]
    }
  ],
  "total_iterations": 2,
  "total_sources": 8,
  "elapsed_seconds": 45.32,
  "search_timestamp": "2025-12-28T18:30:00"
}
```

## 与 websearch_service 的区别

| 特性 | WebSearch | DeepSearch |
|------|-----------|------------|
| 搜索模式 | 单轮搜索 | 迭代多轮搜索 |
| 查询策略 | 直接使用输入 | LLM 分解/优化 |
| 输出格式 | 结构化列表 | 综合报告 + 来源 |
| 响应时间 | 10-30s | 30-120s |
