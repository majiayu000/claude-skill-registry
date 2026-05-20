---
name: tavily-search
description: 使用Tavily API进行网络搜索，获取实时信息、回答问题或研究主题
tool_name: tavily_search
category: search
priority: 8
tags: ["search", "research", "real-time", "information"]
version: 1.0
---

# 工具调用示例（Tavily Search）

当您决定调用 tavily_search 工具时，您的响应应该是一个包含 tool_name 和 parameters 字段的 JSON 对象。parameters 字段的值应是工具所需的参数对象。

## ✅ 正确示例

**parameters 字段内容:**
```json
{"query": "latest AI news"}
```

**完整工具调用响应示例:**
```json
{"tool_name": "tavily_search", "parameters": {"query": "latest AI news"}}
```

## ❌ 错误示例 (请避免以下常见错误)

- **在 JSON 中嵌入 Markdown 分隔符:** 
  ```json
  "```json\n{\"query\": \"latest AI news\"}\n```"
  ```
  (Qwen 模型会将此作为 JSON 字符串的一部分，导致解析失败)

- **参数名错误:** 
  ```json
  {"q": "latest AI news"}
  ```
  (应为 "query" 而非 "q")

- **参数值错误:** 
  ```json
  {"query": 123}
  ```
  (query 参数值应为字符串，而不是数字)

## 关键指令
1. **查询构建**: 查询应该具体且相关
2. **实时性**: 适用于需要最新信息的问题
3. **验证**: 可用于验证其他信息来源

## 使用场景
1. 获取实时新闻和信息
2. 回答需要最新数据的问题
3. 研究特定主题的背景信息
4. 验证事实和数据的准确性

## 最佳实践
- 查询应该具体且相关
- 对于复杂问题，可以分解为多个搜索查询
- 结合搜索结果进行综合分析
- 优先使用英文关键词获取更准确的结果

## 示例查询
- "2024年人工智能最新发展"
- "OpenAI最新模型发布信息"
- "比特币当前价格和趋势"
- "Python 3.12新特性详解"
