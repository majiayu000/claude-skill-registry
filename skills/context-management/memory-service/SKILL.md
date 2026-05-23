---
name: memory_service
description: |
  记忆检索服务。让 Agent 自主决定是否需要回忆过去的对话。
  **使用场景**：
  1. 用户问"之前我们讨论过什么"、"上次说的那个..."
  2. 需要参考之前的上下文来回答当前问题
  3. 用户提到某个之前讨论过的主题
  **不要滥用**：简单问题（如写代码、解释概念）不需要检索记忆
client_class: MemoryServiceClient
default_method: search
---

## 功能

使用 **Rerank + LLM** 两阶段检索，让 Agent 可以：
- 智能搜索与当前问题相关的历史对话
- LLM 理解上下文和指代关系（如"上次说的那个"）
- 按时间范围筛选记忆

## 调用方式

```python
from services.memory_service.client import MemoryServiceClient

client = MemoryServiceClient()

# 语义搜索相关记忆
results = client.search(
    query="用户之前问过关于 Docker 的问题",
    session_id="current_session_id",  # 必填：限定在当前会话内搜索
    limit=5  # 返回最相关的 5 条
)

# 获取最近的对话历史
recent = client.get_recent(
    session_id="session_id",
    limit=10
)
```

## 检索流程

```
1. 从数据库获取最近 50 条消息
        ↓
2. Rerank 模型初筛 → top 10 候选
        ↓
3. LLM 精选 + 整合 → 最相关的 N 条
        ↓
4. 返回结果（含相关性评分）
```
