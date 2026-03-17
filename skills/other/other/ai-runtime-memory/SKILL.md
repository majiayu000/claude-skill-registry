---
name: ai-runtime-memory
description: AI Runtime分层记忆系统，支持SQL风格的事件查询、时间线管理，以及记忆的智能固化和检索，用于项目历史追踪和经验传承
license: MIT
version: 1.0.0
---

# AI Runtime 记忆系统

## 概述

AI Runtime的记忆系统采用分层架构，模拟人类大脑的记忆机制，实现持续存在和认知主体性。系统分为三个层次，通过专门的工具支持SQL风格查询和智能管理。

## 核心功能

### 三层记忆架构
- **短期记忆**: 当前会话上下文，7±2组块限制
- **长期记忆**: 跨项目技术知识，结构化知识图谱
- **情景记忆**: 项目历史事件，支持复杂时间线查询

### 查询能力
- SQL风格条件查询（WHERE/ORDER BY/LIMIT）
- 多格式输出（table/json）
- 时间范围和标签过滤
- 全文搜索支持

## 快速开始

### 基本查询
```bash
# 进入记忆系统目录
cd .ai-runtime/memory

# 查看今天的事件
python3 memory_cli.py query --where "date='$(date +%Y-%m-%d)'"

# 查看架构决策
python3 memory_cli.py query --where "tags CONTAINS 'architecture' AND type='decision'"
```

### 使用便捷脚本
```bash
# 查看今天的事件
./scripts/memory-query.sh today

# 查看本周统计
./scripts/memory-query.sh week

# 搜索关键词
./scripts/memory-query.sh search "认证"
```

## 渐进式披露文档架构

基于 anthropics/skills 设计，按需加载详细信息：

### 核心架构
- **[系统架构详解](references/core/architecture.md)** - 分层记忆系统设计和实现原理

### 使用指南
- **[工具使用指南](references/guides/tools.md)** - memory_cli.py 和 memory_discovery.py 详细用法

### 高级主题
- **[维护指南](references/advanced/maintenance.md)** - 记忆固化、清理和质量保证

### 实践示例
- **[使用示例](references/examples/examples.md)** - 从基础查询到高级分析的完整示例

## 事件记录格式

### YAML Front Matter
```yaml
---
id: unique-event-id
type: event|decision|error|meeting
level: day
timestamp: "2025-11-14T10:30:00"
tags: [architecture, decision]
---
```

### 目录结构
```
episodic/
└── 2025/11/14/
    └── event-description.md
```

## 编程接口

```python
from memory_discovery import MemoryDiscovery

# 初始化
discovery = MemoryDiscovery('.ai-runtime/memory')

# 查询
events = discovery.query(
    where="date>='2025-11-14' AND tags CONTAINS 'architecture'",
    order_by="timestamp desc",
    limit=20
)

# 格式化输出
output = discovery.format_events(events, format_type="table")
```

## 相关命令

- `/runtime.remember` - 记录新记忆事件
- `/runtime.think` - 基于记忆进行思考
- `/runtime.explore` - 探索和分析记忆模式

## 维护建议

- 定期运行 `./scripts/memory-query.sh stats` 检查系统状态
- 每周审查 `./scripts/memory-query.sh week` 的活动记录
- 每月归档重要事件到 long-term 记忆层

---

*基于 anthropics/skills 渐进式披露架构设计*
