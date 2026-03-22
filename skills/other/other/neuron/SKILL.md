---
name: neuron
description: "分布式AI节点系统，实现跨局域网节点的任务分发、并行处理和结果聚合"
---

# Neuron - 分布式AI节点系统

Neuron 将独立的 OpenClaw 实例转变为分布式神经网络，实现跨多个节点的智能任务处理。

## 核心功能

- **节点发现**：通过UDP广播自动发现局域网内的其他Neuron节点
- **任务分发**：将任务分发给所有可用节点进行并行处理
- **结果聚合**：收集多个节点的响应并综合成最终答案
- **知识共享**：向网络广播最终结果实现集体学习

## 使用方法

### 基础使用

当用户提出问题时，Neuron 会自动：
1. 发现网络中的可用节点
2. 将任务分发给所有节点
3. 并行收集响应
4. 综合结果返回最终答案

### 直接调用

```python
# 执行分布式任务（自动分发）
context.call_skill("neuron", question="您的问题")

# 本地处理（不分发）
context.call_skill("neuron", question="您的问题", distribute=False)
```

### Python API

```python
from scripts.neuron_skill import NeuronProcessor

processor = NeuronProcessor()

# 获取活跃节点
nodes = processor.get_active_nodes()

# 处理任务
result = processor.execute("您的问题", context=context)
```

## 配置

### 节点ID

首次运行时会自动生成唯一的节点ID并永久保存到 `scripts/node_identity.json`。如需自定义，可手动修改该文件中的 `node_id` 字段。

### 配置文件

编辑 `scripts/config.json` 调整以下参数：

```json
{
  "discovery_port": 83668,
  "broadcast_interval": 5,
  "node_timeout": 15,
  "task_timeout": 30,
  "max_parallel_tasks": 10
}
```

### 防火墙设置

允许UDP端口83668的入站连接：

```bash
# Windows PowerShell
New-NetFirewallRule -DisplayName "Neuron Discovery" -Direction Inbound -Protocol UDP -LocalPort 83668 -Action Allow
```

## 工作流程

### 发起节点工作流

1. 接收用户查询
2. 发现可用节点
3. 将任务分发给所有节点
4. 聚合结果
5. 综合最终答案
6. 向网络广播结果

### 执行节点工作流

1. 接收分发的任务
2. 使用AI模型本地处理
3. 将结果返回给发起节点
4. 从广播的最终结果中学习

## 使用场景

✅ **适合使用此技能的情况：**
- 需要多视角分析的复杂推理任务
- 需要并行处理的大规模数据分析
- 不同节点具有不同上下文/知识的任务
- 需要冗余处理以提高可靠性的场景

❌ **不适合使用此技能的情况：**
- 简单的单节点查询
- 需要实时同步的任务
- 低延迟要求
- 网络受限的环境

## 工具接口

### NeuronProcessor

分布式任务处理的核心类，提供以下方法：

- `execute(question, context, distribute=True)`：执行任务
- `get_active_nodes()`：获取活跃节点列表
- `get_status()`：获取系统状态
- `get_task_memory(task_id)`：获取任务记忆

## 故障排除

### 节点无法互相发现
- 检查UDP端口83668的防火墙设置
- 验证所有节点是否在同一网络段
- 确保节点ID唯一

### 高延迟
- 减少 `task_timeout` 配置值
- 减小 `broadcast_interval` 加快发现速度
- 减少分发节点数量

## 安全注意事项

⚠️ 仅在受信任的网络环境中使用
🚫 不要将UDP端口83668暴露到公共互联网
🔐 如有需要，加密敏感任务数据
