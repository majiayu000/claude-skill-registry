---
name: rancher-capacity-analysis
description: This skill should be used when the user asks to "node capacity", "cluster capacity", "resource usage", "node health", "overloaded", "node status", "how much capacity", "resource utilization", "容量", "节点分析", "资源使用", "节点健康", "负载", "扩容", "容量规划", or discusses cluster capacity planning and node resource analysis (集群容量规划和节点资源分析).
version: 1.0.0
---

# Rancher 容量分析

分析集群容量、节点健康和资源利用率，用于容量规划和问题发现。

## 可用 Sub-Agent

### 1. `rancher-node-analyzer`
**用于**: 节点健康分析、资源利用率、容量规划

**何时调用**:
- 用户要求"节点状态"或"节点健康"
- 用户要求"容量分析"或"资源使用率"
- 用户关心"哪些节点负载高"
- 需要多节点对比分析

**传递参数**:
```json
{
  "cluster": "c-abc123",
  "node_name": "",
  "analysis_type": "comprehensive",
  "include_pods": true,
  "include_util": true
}
```

### 2. `rancher-cluster-explorer`
**用于**: 多集群容量对比

**何时调用**:
- 用户要求对比多个集群的容量
- 用户关心"哪个集群有空间"
- 跨集群容量规划

## 并行执行模式

### 模式 1: 多节点对比
```
用户: "对比所有 worker 节点的负载"

→ 启动 rancher-node-analyzer
   参数: { cluster: "c-abc123", analysis_type: "capacity", include_util: true }
→ 展示各节点对比表格
```

### 模式 2: 多集群容量对比
```
用户: "production 和 staging 哪个集群有更多空间？"

→ 并行启动：
  Agent 1: rancher-node-analyzer（production 集群）
  Agent 2: rancher-node-analyzer（staging 集群）
→ 对比容量数据
→ 给出建议
```

### 模式 3: 全面容量审查
```
用户: "集群容量全面审查"

→ 并行启动：
  Agent 1: rancher-cluster-explorer（集群概览 + 项目列表）
  Agent 2: rancher-node-analyzer（节点详细分析）
→ 生成综合容量报告
```

## 决策树

```
用户查询提到：
├─ "节点状态" / "node health" / "节点问题"
│  └─ 使用: rancher-node-analyzer（analysis_type: "health"）
│
├─ "容量" / "capacity" / "资源使用率"
│  └─ 使用: rancher-node-analyzer（analysis_type: "capacity"，include_util: true）
│
├─ "哪些节点负载高" / "overloaded nodes"
│  └─ 使用: rancher-node-analyzer（include_util: true，sortBy: "cpu.util"）
│
├─ "多集群容量对比"
│  └─ 并行启动多个 rancher-node-analyzer
│
└─ "全面审查" / "容量规划"
   └─ 并行启动 cluster-explorer + node-analyzer
```

## 工作流

### 步骤 1: 解析用户请求
- 关注哪个集群？（需要集群 ID）
- 关注哪个节点？（具体节点还是所有节点）
- 需要什么级别的分析？（快速概览 vs 深入分析）

### 步骤 2: 确定 Agent 策略
- 单集群节点分析 → 一个 node-analyzer
- 多集群对比 → 多个 Agent 并行
- 全面审查 → cluster-explorer + node-analyzer

### 步骤 3: 启动 Sub-Agent
```
Task({
  subagent_type: "general-purpose",
  description: "分析集群 " + cluster + " 的容量",
  prompt: `你是 rancher-node-analyzer。分析集群 ${cluster} 的节点健康状况和资源利用率。包含实际使用率数据。`
})
```

### 步骤 4: 展示报告和建议

## 响应格式

### 容量概览
```
## 集群容量分析: production (c-abc123)

### 资源汇总
| 资源 | 总容量 | 已请求 | 已限制 | 实际使用 |
|------|--------|--------|--------|----------|
| CPU | 40 cores | 26 cores (65%) | 48 cores (120%) | 18 cores (45%) |
| 内存 | 128 GiB | 89.6 GiB (70%) | 115.2 GiB (90%) | 76.8 GiB (60%) |
| Pod | 550 | 215 (39%) | - | - |

### 节点详情
| 节点 | 状态 | CPU请求 | CPU使用 | 内存请求 | 内存使用 | Pod数 |
|------|------|---------|---------|----------|----------|-------|
| node-1 | Ready | 65% | 45% | 70% | 60% | 42/110 |
| node-2 | Ready | 85% | 72% | 88% | 78% | 65/110 |
| node-3 | Ready | 50% | 30% | 55% | 45% | 38/110 |

### 告警
- ⚠️ node-2: CPU 请求 85% - 接近容量上限
- ⚠️ node-2: 内存请求 88% - 建议关注

### 建议
1. node-2 负载较高，考虑迁移部分工作负载
2. 集群整体 CPU 过度分配（limits 120%），需要关注突发场景
3. 建议添加 1 个 worker 节点以提供缓冲空间
```

## 容量规划阈值

| 指标 | 健康 | 关注 | 危险 |
|------|------|------|------|
| CPU 请求 | < 70% | 70-85% | > 85% |
| 内存请求 | < 75% | 75-90% | > 90% |
| CPU 实际使用 | < 60% | 60-80% | > 80% |
| 内存实际使用 | < 70% | 70-85% | > 85% |
| Pod 数量 | < 80% | 80-95% | > 95% |

## 错误处理

- **metrics-server 未安装**: 无法获取实际利用率，仅展示请求/限制数据
- **节点不可达**: 标记为 NotReady，展示最后已知状态
- **数据不完整**: 说明缺失部分，基于可用数据给出建议
